import json
from typing import Literal
from sqlalchemy.orm import Session
from src.database.db_setup import session
from fastapi import status, APIRouter, Depends
from src.routers.api_enpoints import APIEndpoints
from src.database.crud import private_courses_crud
from src.builders.response_builder import ResponseBuilder
from src.routers.sql_statement_repository import sql_statements
from src.functions.time_transformator import transform_class_time
from src.bot_client.message_sender import send_notification_about_new_class
from src.models import (PaginatedList, NewClassDto, ClassDto, Role, PrivateCourseInlineDto, ItemsDto,
                        PrivateClassDto)


router = APIRouter()


@router.get(path=APIEndpoints.PrivateCourses.GetClasses, status_code=status.HTTP_200_OK,
            response_model=PaginatedList[PrivateClassDto], summary="Get classes of the course")
async def get_classes_for_bot(course_id: int, user_id: int, role: Literal[Role.Tutor, Role.Student], page: int, db: Session = Depends(session)):
    result = db.execute(sql_statements.get_classes, {"p1": user_id, "p2": course_id, "p3": page, "p4": role})

    total_count = None
    user_timezone = None
    classes: list[PrivateClassDto] = []

    for row in result.fetchall():
        if row[0] is None:
            return ResponseBuilder.error_response(message=row[4])

        if total_count is None or user_timezone is None:
            total_count = row[1]
            user_timezone = row[3]

        new_time = transform_class_time(row[2], row[3])

        private_class = PrivateClassDto(id=row[0], schedule_datetime=new_time, status=row[4])
        classes.append(private_class)

    pages = total_count // 3 + (0 if total_count % 3 == 0 else 1)

    response_model = PaginatedList[PrivateClassDto](
        items=classes,
        total=total_count,
        current_page=page,
        pages=pages)

    return ResponseBuilder.success_response(content=response_model)


@router.get(path=APIEndpoints.PrivateCourses.GetClassesByDate, status_code=status.HTTP_200_OK,
            response_model=ItemsDto[ClassDto], summary="Get classes of the course for specific month")
async def get_classes_by_date(private_course_id: int, month: int, year: int, db: Session = Depends(session)):
    db_classes = private_courses_crud.get_private_course_classes_for_month(db, private_course_id, month, year)

    if not db_classes:
        return ResponseBuilder.success_response(content=ItemsDto(items=[]))

    classes = [ClassDto(date=db_class[0], status=db_class[1]) for db_class in db_classes]

    return ResponseBuilder.success_response(content=ItemsDto[ClassDto](items=classes))


@router.get(path=APIEndpoints.PrivateCourses.Get, status_code=status.HTTP_200_OK,
            response_model=ItemsDto[PrivateCourseInlineDto], summary="Get private courses for user by subject name")
async def get_private_courses(user_id: int, subject_name: str, role: Literal[Role.Tutor, Role.Student], db: Session = Depends(session)):
    private_courses = private_courses_crud.get_private_courses(db, user_id, subject_name, role)

    if not private_courses:
        return ResponseBuilder.success_response(content=ItemsDto(items=[]))

    private_courses = [PrivateCourseInlineDto.from_tuple(pc) for pc in private_courses]

    return ResponseBuilder.success_response(content=ItemsDto[PrivateCourseInlineDto](items=private_courses))


@router.post(path=APIEndpoints.PrivateCourses.Enroll, status_code=status.HTTP_201_CREATED,
             summary="Enroll student to course")
async def enroll_in_course(user_id: int, private_course_id: int, db: Session = Depends(session)):
    # TODO: Rewrite
    private_courses_crud.enroll_student_to_course(db=db, user_id=user_id, course_id=private_course_id)
    return ResponseBuilder.success_response(status.HTTP_201_CREATED)


@router.post(path=APIEndpoints.PrivateCourses.AddNewClass, status_code=status.HTTP_201_CREATED,
             summary="Add new class for private course")
async def add_new_class(private_course_id: int, role: Literal[Role.Tutor, Role.Student],
                        new_class: NewClassDto, db: Session = Depends(session)):
    schedule = new_class.date
    assignment = {
        "sources": [source.model_dump_json() for source in new_class.sources]
    }

    params = {
        'pc_id': private_course_id,
        'sender_role': role,
        'sc_schedule_datetime': schedule,
        'sc_assignment': json.dumps(assignment),
        'recipient_id': None,
        'recipient_timezone': None,
        'sender_name': None,
        'subject_name': None,
        'error': None
    }

    result = db.execute(sql_statements.schedule_class_and_get_course, params)

    result_row = result.fetchall()[0]

    db.commit()
    db.close()
    recipient_id, recipient_timezone, sender_name, subject_name, error_msg = result_row

    if error_msg:
        return ResponseBuilder.error_response(message=error_msg)

    class_date = transform_class_time(schedule, recipient_timezone).strftime('%H:%M %d-%m-%Y')

    send_notification_about_new_class(recipient_id, sender_name, subject_name, class_date)

    return ResponseBuilder.success_response(status.HTTP_201_CREATED)
