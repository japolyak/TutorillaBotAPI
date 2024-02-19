import json
from datetime import datetime
from sqlalchemy.orm import Session
from database.models import PrivateClass


def schedule_class(db: Session, course_id: int, schedule: datetime, assignment: json):
    db_class = PrivateClass(private_course_id=course_id, schedule_datetime=schedule, assignment=assignment)
    db.add(db_class)
    db.commit()
    db.refresh(db_class)

    return db_class
