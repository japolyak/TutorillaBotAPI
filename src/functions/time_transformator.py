from datetime import timezone, timedelta, datetime
from typing import Literal
from src.models import Role


def transform_class_time(some_data: datetime, time_zone: float) -> datetime:
    new_timezone = timezone(timedelta(hours=time_zone))

    return some_data.astimezone(new_timezone)
