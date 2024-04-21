from sqlalchemy.orm import Session
from src.database.models import UserRequest
from typing import Literal
from src.models import Role


def get_users_requests(db: Session, role: Literal[Role.Tutor, Role.Student]):
    query = db.query(UserRequest)

    if role == Role.Tutor:
        query = query.filter(UserRequest.tutor_role)
    else:
        query = query.filter(UserRequest.student_role)

    return query.all()


def get_user_request(db: Session, role_request_id: int):
    query = db.query(UserRequest).filter(UserRequest.id == role_request_id)

    return query.first()
