from sqlalchemy.orm import Session
from database.models import TutorCourse, Subject, User
from routers.data_transfer_models import NewTutorCourseDto


def add_course(db: Session, user_id: int, course: NewTutorCourseDto):

    db_course = TutorCourse(tutor_id=user_id, subject_id=course.subject_id, price=course.price)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course


def get_available_courses_by_subject(db: Session, user_id: int, subject_name: str):
    query = (
        db.query(TutorCourse.id, TutorCourse.price, Subject.name, User.first_name)
        .join(TutorCourse.subject)
        .join(TutorCourse.tutor)
        .filter(Subject.name == subject_name, TutorCourse.is_active, TutorCourse.tutor_id != user_id)
    )

    return query.all()
