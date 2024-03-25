from sqlalchemy import not_, exists, and_, select, distinct
from sqlalchemy.orm import Session
from database.models import TutorCourse, Subject, PrivateCourse, User


def get_student_subjects(db: Session, user_id: int):
    db_student_courses = (
        db.query(Subject)
        .join(Subject.tutor_courses)
        .join(TutorCourse.private_courses)
        .filter(PrivateCourse.student_id == user_id)
        .all()
    )

    return db_student_courses


def get_tutor_courses(db: Session, user_id: int):
    db_tutor_courses = (
        db.query(Subject)
        .join(Subject.tutor_courses)
        .filter(TutorCourse.tutor_id == user_id)
        .all()
    )
    return db_tutor_courses


def get_available_subjects_student(db: Session, user_id: int):
    student_courses = select(PrivateCourse.course_id).where(PrivateCourse.student_id == user_id)

    tutor_courses = select(TutorCourse.id).where(TutorCourse.tutor_id == user_id)

    uninvolved_courses = (db.query(Subject)
                          .join(Subject.tutor_courses)
                          .filter(TutorCourse.id.notin_(student_courses), TutorCourse.id.notin_(tutor_courses))
                          .all())

    return uninvolved_courses


def get_available_subjects_tutor(db: Session, user_id: int):
    db_available_courses = (
        db.query(Subject)
        .except_(db.query(Subject)
                 .join(Subject.tutor_courses)
                 .filter(TutorCourse.tutor_id == user_id))
        .all()
    )

    return db_available_courses
