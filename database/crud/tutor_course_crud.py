from sqlalchemy.orm import Session
from database.models import TutorCourse, Subject


def add_course(db: Session, user_id: int, subject_id: int):
    db_course = TutorCourse(tutor_id=user_id, subject_id=subject_id)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course

def get_available_courses_by_subject(db: Session, user_id: int, subject_name: str):
    db_available_courses = (
        db.query(TutorCourse)
        .join(TutorCourse.subject)
        .filter(Subject.name == subject_name, TutorCourse.is_active, TutorCourse.tutor_id != user_id)
        .all()
    )

    return db_available_courses