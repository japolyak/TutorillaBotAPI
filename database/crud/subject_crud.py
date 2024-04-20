from sqlalchemy import select
from sqlalchemy.orm import Session
from database.models import TutorCourse, Subject, PrivateCourse


def get_student_subjects(db: Session, user_id: int, available: bool):
    sub_query = select(1).select_from(PrivateCourse).where(PrivateCourse.course_id == TutorCourse.id).exists()

    query = (db.query(Subject)
             .join(Subject.tutor_courses)
             .filter(TutorCourse.tutor_id != user_id,
                     ~sub_query if available else sub_query))

    if available:
        query = query.filter(TutorCourse.is_active)

    return query.all()


def get_tutor_subjects(db: Session, user_id: int, available: bool):
    sub_query = (select(1)
                 .select_from(TutorCourse)
                 .filter(TutorCourse.tutor_id == user_id, TutorCourse.subject_id == Subject.id)
                 .exists())

    query = db.query(Subject).filter(~sub_query if available else sub_query)

    return query.all()
