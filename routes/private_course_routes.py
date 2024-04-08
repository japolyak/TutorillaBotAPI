from fastapi import status, APIRouter, Depends, HTTPException
import json
from bot_client.message_sender import send_notification_about_new_class
from .schemas import PrivateCourseDto, SourceDto, PrivateClassBaseDto, PaginatedList, NewClassDto
from sqlalchemy.orm import Session
from database.db_setup import get_db
from functions.time_transformator import transform_class_time
from database.crud import private_courses_crud
import datetime


router = APIRouter()


@router.get(path="/{course_id}/classes/", status_code=status.HTTP_200_OK,
            response_model=PaginatedList, description="Get classes of the course")
async def get_classes(course_id: int, role: str, page: int, db: Session = Depends(get_db)):
    if role not in ["tutor", "student"]:
        raise HTTPException(status_code=400)

    items_per_page = 5
    db_classes, count = private_courses_crud.get_private_course_classes(db, items_per_page, course_id, page)
    pages = 1 + count // items_per_page

    private_course_dto = None
    classes: list[PrivateClassBaseDto] = []

    for db_class in db_classes:
        if not private_course_dto:
            private_course_dto = PrivateCourseDto.model_validate(db_class.private_course)

        sources = [SourceDto(**json.loads(item)) for item in db_class.assignment.get('sources', [])]

        new_time = transform_class_time(db_class.private_course, db_class.schedule_datetime, role)
        print(new_time)

        class_dto = PrivateClassBaseDto(
            id=db_class.id,
            private_course=PrivateCourseDto.model_validate(db_class.private_course),
            schedule_datetime=new_time,
            assignment=sources,
            is_scheduled=db_class.is_scheduled,
            has_occurred=db_class.has_occurred,
            is_paid=db_class.is_paid
        )
        classes.append(class_dto)

    result: PaginatedList[PrivateClassBaseDto] = PaginatedList[PrivateClassBaseDto](items=classes, total=count,
                                                                                    current_page=page, pages=pages)

    return result


@router.get(path="/users/{user_id}/subjects/{subject_name}/", status_code=status.HTTP_200_OK,
            response_model=list[PrivateCourseDto], description="Get private courses")
async def get_private_courses(user_id: int, subject_name: str, role: str, db: Session = Depends(get_db)):
    db_private_courses = private_courses_crud.get_private_courses(db=db, user_id=user_id, subject_name=subject_name, role=role)

    return db_private_courses


@router.get(path="/{private_course_id}/users/{user_id}/", status_code=status.HTTP_200_OK,
            description="Get private courses")
async def get_private_courses(user_id: int, private_course_id: int, db: Session = Depends(get_db)):
    db_private_course = private_courses_crud.get_private_course_by_course_id(db=db, private_course_id=private_course_id)

    if not db_private_course:
        raise HTTPException(status_code=404, detail="Private course not found")

    return status.HTTP_200_OK


@router.post(path="/{private_course_id}/users/{user_id}/", status_code=status.HTTP_201_CREATED,
             response_model=PrivateCourseDto, description="Enroll student to course")
async def get_private_courses(user_id: int, private_course_id: int, db: Session = Depends(get_db)):
    db_course = private_courses_crud.enroll_student_to_course(db=db, user_id=user_id, course_id=private_course_id)
    return db_course


@router.post(path="/{private_course_id}/new-class/{role}/", status_code=status.HTTP_201_CREATED,
             description="Add new class for private course")
async def add_new_class(private_course_id: int, role: str, new_class: NewClassDto, db: Session = Depends(get_db)):
    """
    Adds new class for private course from telegram web app
    """
    schedule = new_class.date
    assignment = {
        "sources": [source.model_dump_json() for source in new_class.sources]
    }

    private_courses_crud.schedule_class(db=db, course_id=private_course_id, schedule=schedule, assignment=assignment)

    private_course = private_courses_crud.get_private_course_by_course_id(db, private_course_id)

    if role == "tutor":
        sender_id = private_course.course.tutor.id

        recipient_name = private_course.student.first_name

        test_baba = transform_class_time(private_course, new_class.date, "tutor").strftime('%H:%M %d-%m-%Y')
    else:
        sender_id = private_course.student.id

        recipient_name = private_course.course.tutor.first_name

        test_baba = transform_class_time(private_course, new_class.date, "student").strftime('%H:%M %d-%m-%Y')

    send_notification_about_new_class(sender_id, recipient_name, private_course.course.subject.name, test_baba)

    return private_course
