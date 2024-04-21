from database.models import TutorCourse, Subject, PrivateCourse, User, PrivateClass
from routers.data_transfer_models import Role, ClassStatus
from sqlalchemy import asc, func, case, literal_column
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from typing import Literal


def get_private_course_classes(db: Session, items_per_page: int, course_id: int, page: int = 1):
    offset = (page - 1) * items_per_page

    query_one = (
        db.query(PrivateClass)
        .order_by(asc(PrivateClass.schedule_datetime))
        .filter(PrivateClass.private_course_id == course_id)
        .offset(offset)
        .limit(items_per_page))

    query_two = (
        db.query(func.count(PrivateClass.id))
        .filter(PrivateClass.private_course_id == course_id))

    return query_one.all(), query_two.scalar()


def get_private_course_classes_for_month(db: Session, course_id: int, month: int, year: int):
    start_date = datetime(year, month - 1, 24)
    finish_date = datetime(year, month + 1, 6)

    status = (case((PrivateClass.is_paid, literal_column(f"'{ClassStatus.Paid}'")),
                   (PrivateClass.has_occurred, literal_column(f"'{ClassStatus.Occurred}'")),
                   else_=literal_column(f"'{ClassStatus.Scheduled}'")))

    query = (db.query(PrivateClass.schedule_datetime, status)
             .filter(
        PrivateClass.private_course_id == course_id,
        PrivateClass.schedule_datetime >= start_date,
        PrivateClass.schedule_datetime <= finish_date))

    return query.all()


def get_private_courses(db: Session, user_id: int, subject_name: str, role: Literal[Role.Tutor, Role.Student]):
    query = (db.query(PrivateCourse.id, Subject.name, User.first_name)
             .join(PrivateCourse.course)
             .join(TutorCourse.subject)
             .filter(Subject.name == subject_name))

    if role == Role.Student:
        query = query.join(TutorCourse.tutor).filter(PrivateCourse.student_id == user_id)
    else:
        query = query.join(PrivateCourse.student).filter(TutorCourse.tutor_id == user_id)

    return query.all()


def get_private_course_by_course_id(db: Session, private_course_id: int):
    query = (
        db.query(PrivateCourse)
        .options(
            joinedload(PrivateCourse.student),
                  joinedload(PrivateCourse.course).joinedload(TutorCourse.tutor),
                  joinedload(PrivateCourse.course).joinedload(TutorCourse.subject))
        .filter(PrivateCourse.id == private_course_id))

    return query.first()


def enroll_student_to_course(db: Session, user_id: int, course_id: int):
    db_course = db.query(TutorCourse).filter(TutorCourse.id == course_id).first()

    db_course = PrivateCourse(student_id=user_id, course_id=course_id, price=db_course.price)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course
