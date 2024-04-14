from database.models import TutorCourse, Subject, PrivateCourse
from sqlalchemy import asc, func
from sqlalchemy.orm import Session, joinedload
from database.models import PrivateClass
import json
from datetime import datetime


def get_private_course_classes(db: Session, items_per_page: int, course_id: int, page: int = 1):
    offset = (page - 1) * items_per_page
    db_classes = (
        db.query(PrivateClass)
        .order_by(asc(PrivateClass.schedule_datetime))
        .filter(PrivateClass.private_course_id == course_id)
        .offset(offset)
        .limit(items_per_page)
        .all()
    )
    total = (
        db.query(func.count(PrivateClass.id))
        .filter(PrivateClass.private_course_id == course_id)
        .scalar()
    )

    return db_classes, total


def get_private_course_classes_for_month(db: Session, course_id: int, month: int, year: int):
    start_date = datetime(year, month - 1, 25)
    finish_date = datetime(year, month + 1, 5)

    db_classes = (
        db.query(PrivateClass)
        .filter(
            PrivateClass.private_course_id == course_id,
            PrivateClass.schedule_datetime >= start_date,
            PrivateClass.schedule_datetime <= finish_date
        )
        .all()
    )

    return db_classes


def get_private_courses(db: Session, user_id: int, subject_name: str, role: str):
    if role == "tutor":
        db_courses = (
            db.query(PrivateCourse)
            .join(PrivateCourse.course)
            .join(TutorCourse.subject)
            .filter(TutorCourse.tutor_id == user_id, Subject.name == subject_name)
            .all()
        )
    else: # role == "student"
        db_courses = (
            db.query(PrivateCourse)
            .join(PrivateCourse.course)
            .join(TutorCourse.subject)
            .filter(PrivateCourse.student_id == user_id, Subject.name == subject_name)
            .all()
        )

    return db_courses


def get_private_course_by_course_id(db: Session, private_course_id: int):
    db_course = (
        db.query(PrivateCourse)
        .options(
            joinedload(PrivateCourse.student),
                  joinedload(PrivateCourse.course).joinedload(TutorCourse.tutor),
                  joinedload(PrivateCourse.course).joinedload(TutorCourse.subject))
        .filter(PrivateCourse.id == private_course_id)
        .first()
    )

    return db_course


def enroll_student_to_course(db: Session, user_id: int, course_id: int):
    db_course = db.query(TutorCourse).filter(TutorCourse.id == course_id).first()

    db_course = PrivateCourse(student_id=user_id, course_id=course_id, price=db_course.price)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course


def schedule_class(db: Session, course_id: int, schedule: datetime, assignment: json):
    db_class = PrivateClass(private_course_id=course_id, schedule_datetime=schedule, assignment=assignment)
    db.add(db_class)
    db.commit()
    db.refresh(db_class)

    return db_class
