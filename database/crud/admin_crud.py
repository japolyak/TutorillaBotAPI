from datetime import datetime
from sqlalchemy import desc
from sqlalchemy.orm import Session
from database.models import UserRequest


def get_users_requests(db: Session, role: str):
    if role == "tutor":
        return db.query(UserRequest).filter(UserRequest.tutor_role).all()

    if role == "student":
        return db.query(UserRequest).filter(UserRequest.student_role).all()


def get_user_request(db: Session, role_request_id: int):
    print(role_request_id)
    db_user_request = db.query(UserRequest).filter(UserRequest.id == role_request_id).first()

    return db_user_request
