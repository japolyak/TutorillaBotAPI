from database.models import TutorCourse, Subject, PrivateCourse
from sqlalchemy import asc, func
from sqlalchemy.orm import Session
from database.models import PrivateClass


def get_private_course_classes(db: Session, course_id: int, page: int = 1, per_page: int = 3):
    offset = (page - 1) * per_page
    db_classes = (
        db.query(PrivateClass)
        .order_by(asc(PrivateClass.schedule_datetime))
        .filter(PrivateClass.private_course_id == course_id)
        .offset(offset)
        .limit(per_page)
        .all()
    )
    total = (
        db.query(func.count(PrivateClass.id))
        .filter(PrivateClass.private_course_id == course_id)
        .scalar()
    )

    return db_classes, total


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


# TODO - Consider rewriting this function
def get_tutor_private_course(db: Session, user_id: int, private_course_id: int):
    db_courses = db.query(PrivateCourse).filter(PrivateCourse.id == private_course_id).first()

    return db_courses


def enroll_student_to_course(db: Session, user_id: int, course_id: int):
    db_course = PrivateCourse(student_id=user_id, course_id=course_id)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course

