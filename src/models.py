from pydantic import BaseModel
from typing import List, Generic, TypeVar, Tuple
from datetime import datetime
from enum import StrEnum

T = TypeVar('T')


class ClassStatus(StrEnum):
    Scheduled = 'scheduled'
    Occurred = 'occurred'
    Paid = 'paid'


class Role(StrEnum):
    Admin = 'admin'
    Tutor = 'tutor'
    Student = 'student'


class PaginatedList(BaseModel, Generic[T]):
    items: List[T]
    total: int
    current_page: int
    pages: int

    class Config:
        from_attributes = True


class ItemsDto(BaseModel, Generic[T]):
    items: List[T]

    class Config:
        from_attributes = True


class UserBaseDto(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    time_zone: float
    locale: str

    class Config:
        from_attributes = True


class UserDto(UserBaseDto):
    normalized_email: str | None = None
    is_active: bool | None = None
    is_tutor: bool | None = None
    is_student: bool | None = None
    is_admin: bool | None = None

    class Config:
        from_attributes = True


class UserRequestDto(BaseModel):
    id: int
    user_id: int
    user_first_name: str
    user_last_name: str
    user_email: str
    user_role: Role

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


class TutorCourseInlineDto(BaseModel):
    id: int
    tutor_name: str
    subject_name: str
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


class PrivateCourseInlineDto(BaseModel):
    id: int
    person_name: str
    subject_name: str
    number_of_classes: int

    @classmethod
    def from_tuple(cls, values: Tuple[int, str, str, int]):
        if len(values) != 4:
            raise ValueError("List must contain exactly two elements: [name, age]")

        return cls(id=values[0], person_name=values[1], subject_name=values[2], number_of_classes=values[3])

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


class PrivateClassDto(BaseModel):
    id: int
    schedule_datetime: datetime
    status: ClassStatus


class PrivateClassBaseDto(BaseModel):
    id: int
    schedule_datetime: datetime
    assignment: List[SourceDto]
    is_scheduled: bool
    has_occurred: bool
    is_paid: bool

    class Config:
        from_attributes = True


class NewTutorCourseDto(BaseModel):
    subject_id: int
    price: int

    class Config:
        from_attributes = True


class ClassDto(BaseModel):
    date: datetime
    status: ClassStatus

    class Config:
        from_attributes = True
