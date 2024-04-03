from datetime import timezone, timedelta, datetime


def transform_class_time(db_class, role: str) -> datetime:
    # TODO - remake by abstracting from db_class
    match role:
        case "tutor":
            time_zone = db_class.private_course.course.tutor.time_zone
        case "student":
            time_zone = db_class.private_course.student.time_zone
        case _:
            time_zone = 0

    new_timezone = timezone(timedelta(hours=time_zone))

    return db_class.schedule_datetime.astimezone(new_timezone)
