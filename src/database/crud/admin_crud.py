from sqlalchemy.orm import Session
from src.database.models import UserRequest, User
from typing import Literal
from src.models import Role
from sqlalchemy import case, literal_column


def get_users_requests(db: Session, role: Literal[Role.Tutor, Role.Student]):
    requested_role = case((UserRequest.student_role, literal_column(f"'{Role.Student}'")),
                          else_=literal_column(f"'{Role.Tutor}'"))

    query = (db.query(UserRequest.id, User.id, User.first_name, User.last_name, User.email, requested_role)
             .join(UserRequest.user))

    if role == Role.Tutor:
        query = query.filter(UserRequest.tutor_role)
    else:
        query = query.filter(UserRequest.student_role)

    return query.all()


def get_user_request(db: Session, request_id: int):
    requested_role = case((UserRequest.student_role, literal_column(f"'{Role.Student}'")),
                          else_=literal_column(f"'{Role.Tutor}'"))

    query = (db.query(UserRequest.id, User.id, User.first_name, User.last_name, User.email, requested_role)
             .join(UserRequest.user)
             .filter(request_id == UserRequest.id))

    return query.first()
