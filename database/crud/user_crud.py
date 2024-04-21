from sqlalchemy.orm import Session
from database.models import User, UserRequest
from typing import Literal
from routers.data_transfer_models import Role


def get_user(db: Session, user_id: int):
    query = db.query(User).filter(User.id == user_id)

    return query.first()


def accept_role_request(db: Session, user_id: int, role: Literal[Role.Tutor, Role.Student]):
    db_user_request = db.query(UserRequest).filter(UserRequest.user_id == user_id).first()

    if db_user_request is None:
        return None

    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        return None

    if role == Role.Student:
        db_user.is_student = True
    elif role == Role.Tutor:
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
