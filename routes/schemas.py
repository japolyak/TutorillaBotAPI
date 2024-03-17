from pydantic import BaseModel
from typing import List, Generic, TypeVar
from datetime import datetime

T = TypeVar('T')


class PaginatedList(BaseModel, Generic[T]):
    items: List[T]
    total: int
    current_page: int
    pages: int

    class Config:
        from_attributes = True


class UserBaseDto(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    time_zone: float

    class Config:
        from_attributes = True


class UserDto(UserBaseDto):
    locale: str
    normalized_email: str | None = None
    is_active: bool | None = None
    is_tutor: bool | None = None
    is_student: bool | None = None
    is_admin: bool | None = None

    class Config:
        from_attributes = True


class UserRequestDto(BaseModel):
    id: int
    request_datetime: datetime
    user: UserDto
    tutor_role: bool
    student_role: bool

    class Config:
        from_attributes = True


class SubjectDto(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class TutorCourseDto(BaseModel):
    id: int
    tutor: UserDto
    subject: SubjectDto
    is_active: bool
    price: int

    class Config:
        from_attributes = True


class PrivateCourseDto(BaseModel):
    id: int
    student: UserDto
    course: TutorCourseDto
    price: int

    class Config:
        from_attributes = True


class SourceDto(BaseModel):
    title: str
    assignment: str

    class Config:
        from_attributes = True


class NewClassDto(BaseModel):
    date: datetime
    sources: List[SourceDto]

    class Config:
        from_attributes = True


class PrivateClassBaseDto(BaseModel):
    id: int
    schedule_datetime: datetime
    assignment: List[SourceDto]
    is_scheduled: bool
    has_occurred: bool
    is_paid: bool

    class Config:
        from_attributes = True


# TODO - rename model
class PrivateClassDto(BaseModel):
    private_course: PrivateCourseDto
    classes: List[PrivateClassBaseDto]

    class Config:
        from_attributes = True
