from fastapi import status, APIRouter, Depends
import json
from typing import Literal
from src.bot_client.message_sender import send_notification_about_new_class
from src.models import (PrivateCourseDto, SourceDto, PrivateClassBaseDto, PaginatedList, NewClassDto, ClassDto, Role,
                        PrivateCourseInlineDto, ItemsDto)
from sqlalchemy.orm import Session
from src.database.db_setup import session
from src.functions.time_transformator import transform_class_time
from src.database.crud import private_courses_crud
from src.routers.sql_statement_repository import sql_statements
from datetime import timezone, timedelta
from src.builders.response_builder import ResponseBuilder
from src.routers.api_enpoints import APIEndpoints


router = APIRouter(prefix=APIEndpoints.PrivateCourses.Prefix, tags=["private-courses"])


@router.get(path=APIEndpoints.PrivateCourses.GetClasses, status_code=status.HTTP_200_OK, response_model=PaginatedList,
            summary="Get classes of the course")
async def get_classes(course_id: int, role: Literal[Role.Tutor, Role.Student], page: int, db: Session = Depends(session)):
    # TODO - rewrite
    items_per_page = 3
    db_classes, count = private_courses_crud.get_private_course_classes(db, items_per_page, course_id, page)
    pages = 1 + count // items_per_page

    private_course_dto = None
    classes: list[PrivateClassBaseDto] = []

    for db_class in db_classes:
        if not private_course_dto:
            private_course_dto = PrivateCourseDto.model_validate(db_class.private_course)

        sources = [SourceDto(**json.loads(item)) for item in db_class.assignment.get('sources', [])]

        new_time = transform_class_time(db_class.private_course, db_class.schedule_datetime, role)

        class_dto = PrivateClassBaseDto(
            id=db_class.id,
            schedule_datetime=new_time,
            assignment=sources,
            is_scheduled=db_class.is_scheduled,
            has_occurred=db_class.has_occurred,
            is_paid=db_class.is_paid
        )
        classes.append(class_dto)

    response_model: PaginatedList[PrivateClassBaseDto] = PaginatedList[PrivateClassBaseDto](items=classes,
                                                                                            total=count,
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
    db_private_courses = private_courses_crud.get_private_courses(db, user_id, subject_name, role)

    if not db_private_courses:
        return ResponseBuilder.success_response(content=ItemsDto(items=[]))

    private_courses = [PrivateCourseInlineDto(id=pc[0], person_name=pc[1], subject_name=pc[2]) for pc in db_private_courses]

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
        return ResponseBuilder.error_response(message='Class addition was not successful')

    new_timezone = timezone(timedelta(hours=recipient_timezone))

    class_date = schedule.astimezone(new_timezone).strftime('%H:%M %d-%m-%Y')

    send_notification_about_new_class(recipient_id, sender_name, subject_name, class_date)

    return ResponseBuilder.success_response(status.HTTP_201_CREATED)
