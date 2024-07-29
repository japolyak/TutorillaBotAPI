from src.database.models import TutorCourse, Subject, PrivateCourse, User, PrivateClass
from src.models import Role, ClassStatus
from sqlalchemy import asc, func, case, literal_column, select
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from typing import Literal


def get_private_course_classes_for_month(db: Session, course_id: int, month: int, year: int):
    start_date = datetime(year, month - 1, 24)
    finish_date = datetime(year, month + 1, 6)

    status = (case((PrivateClass.is_paid, literal_column(f"'{ClassStatus.Paid}'")),
                   (PrivateClass.has_occurred, literal_column(f"'{ClassStatus.Occurred}'")),
                   else_=literal_column(f"'{ClassStatus.Scheduled}'")))

    query = (db.query(PrivateClass.schedule_datetime, status).filter(
        course_id == PrivateClass.private_course_id,
        PrivateClass.schedule_datetime >= start_date,
        PrivateClass.schedule_datetime <= finish_date)
    )

    return query.all()


def get_private_courses(db: Session, user_id: int, subject_name: str, role: Literal[Role.Tutor, Role.Student]):
    sub_query = (
        select(func.count())
        .where(PrivateClass.private_course_id == PrivateCourse.id)
        .correlate(PrivateCourse)
        .as_scalar()
    )

    query = (db.query(
        PrivateCourse.id,
        Subject.name,
        User.first_name,
        sub_query
    )
             .join(PrivateCourse.tutor_course)
             .join(TutorCourse.subject)
             .filter(subject_name == Subject.name))

    if role == Role.Student:
        query = query.join(TutorCourse.tutor).filter(user_id == PrivateCourse.student_id)
    else:
        query = query.join(PrivateCourse.student).filter(user_id == TutorCourse.tutor_id)

    return query.all()


def get_private_course_by_course_id(db: Session, private_course_id: int):
    query = (
        db.query(PrivateCourse)
        .options(
            joinedload(PrivateCourse.student),
            joinedload(PrivateCourse.tutor_course).joinedload(TutorCourse.tutor),
            joinedload(PrivateCourse.tutor_course).joinedload(TutorCourse.subject))
        .filter(private_course_id == PrivateCourse.id))

    return query.first()


def enroll_student_to_course(db: Session, user_id: int, course_id: int):
    db_course = db.query(TutorCourse).filter(course_id == TutorCourse.id).first()

    db_course = PrivateCourse(student_id=user_id, course_id=course_id, price=db_course.price)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course
