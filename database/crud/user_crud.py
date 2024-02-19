from sqlalchemy.orm import Session
from database.models import User, UserRequest
from routes.schemas import UserBaseDto
from datetime import datetime

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserBaseDto):

    normalized_email = user.email.lower()

    db_user = User(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone_number=user.phone_number,
        normalized_email=normalized_email,
        time_zone=user.time_zone
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def apply_tutor_role(db: Session, user):
    db_user_request = UserRequest(
        user_id=user.id,
        request_datetime=datetime.now(),
        tutor_role=True
    )

    db.add(db_user_request)
    db.commit()
    db.refresh(db_user_request)
    return db_user_request


# def apply_student_role(db: Session, user_id: int):
#     db_user = db.query(User).filter(User.id == user_id).first()
#     db_user.is_student = True
#     db.commit()
#     db.refresh(db_user)
#     return db_user


def apply_student_role(db: Session, user):
    db_user_request = UserRequest(
        user_id=user.id,
        request_datetime=datetime.now(),
        student_role=True
    )

    db.add(db_user_request)
    db.commit()
    db.refresh(db_user_request)
    return db_user_request


def accept_role_request(db: Session, user_id: int, role: str):
    db_user_request = db.query(UserRequest).filter(UserRequest.user_id == user_id).first()

    if db_user_request is None:
        return None

    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        return None

    if role == "student":
        db_user.is_student = True
    elif role == "tutor":
        db_user.is_tutor = True

    db_user.is_active = True

    db.delete(db_user_request)
    db.commit()
    db.refresh(db_user)

    return db_user


def decline_role_request(db: Session, user_id: int) -> bool:
    db_user_request = db.query(UserRequest).filter(UserRequest.user_id == user_id).first()

    if db_user_request is None:
        return False

    db.delete(db_user_request)
    db.commit()

    return True
