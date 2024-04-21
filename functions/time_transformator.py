from datetime import timezone, timedelta, datetime
from typing import Literal
from routers.data_transfer_models import Role


def transform_class_time(private_course, some_data: datetime, role: Literal[Role.Tutor, Role.Student]) -> datetime:
    # TODO - remake by abstracting from db_class
    match role:
        case "tutor":
            time_zone = private_course.course.tutor.time_zone
        case "student":
            time_zone = private_course.student.time_zone
        case _:
            time_zone = 0

    new_timezone = timezone(timedelta(hours=time_zone))

    return some_data.astimezone(new_timezone)
