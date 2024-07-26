from sqlalchemy import String, BigInteger, Boolean, ForeignKey, UniqueConstraint, DateTime, Integer, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, MappedColumn, Relationship
from typing import List


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: MappedColumn[int] = mapped_column(BigInteger, autoincrement=False, primary_key=True, index=True)
    is_active: MappedColumn[bool] = mapped_column(Boolean, server_default="false")
    first_name: MappedColumn[str] = mapped_column(String(255))
    last_name: MappedColumn[str] = mapped_column(String(255))
    email: MappedColumn[str] = mapped_column(String(255), unique=True)
    normalized_email: MappedColumn[str] = mapped_column(String(255), unique=True)
    time_zone: MappedColumn[float] = mapped_column(Float)
    locale: MappedColumn[str] = mapped_column(String(10), server_default="en-US")
    is_tutor: MappedColumn[bool] = mapped_column(Boolean, server_default="false")
    is_student: MappedColumn[bool] = mapped_column(Boolean, server_default="false")
    is_admin: MappedColumn[bool] = mapped_column(Boolean, server_default="false")

    tutor_courses: Relationship[List["TutorCourse"]] = relationship(
        back_populates="tutor", cascade="all, delete-orphan"
    )

    private_courses: Relationship[List["PrivateCourse"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )

    users_requests: Relationship[List["UserRequest"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class UserRequest(Base):
    __tablename__ = "users_requests"

    id: MappedColumn[int] = mapped_column(primary_key=True, index=True)
    user_id: MappedColumn[int] = mapped_column(ForeignKey("users.id"))
    request_datetime: MappedColumn[DateTime] = mapped_column(DateTime(timezone=True))
    tutor_role: MappedColumn[bool] = mapped_column(Boolean, server_default="false")
    student_role: MappedColumn[bool] = mapped_column(Boolean, server_default="false")

    user: Relationship["User"] = relationship(back_populates="users_requests")

    UniqueConstraint(user_id, name="unique_user_request")


class Subject(Base):
    __tablename__ = "subjects"

    id: MappedColumn[int] = mapped_column(primary_key=True, index=True)
    name: MappedColumn[str] = mapped_column(String(255), unique=True)

    tutor_courses: Relationship[List["TutorCourse"]] = relationship(
        back_populates="subject", cascade="all, delete-orphan"
    )


class TutorCourse(Base):
    __tablename__ = "tutor_courses"

    id: MappedColumn[int] = mapped_column(primary_key=True, index=True)
    tutor_id: MappedColumn[int] = mapped_column(ForeignKey("users.id"))
    subject_id: MappedColumn[int] = mapped_column(ForeignKey("subjects.id"))
    is_active: MappedColumn[bool] = mapped_column(Boolean, server_default="true")
    price: MappedColumn[int] = mapped_column(Integer)

    tutor: Relationship["User"] = relationship(back_populates="tutor_courses")
    subject: Relationship["Subject"] = relationship(back_populates="tutor_courses")

    UniqueConstraint(tutor_id, subject_id, name="unique_tutor_subject")

    private_courses: Relationship[List["PrivateCourse"]] = relationship(
        back_populates="tutor_course", cascade="all, delete-orphan"
    )

    textbooks: Relationship[List["Textbook"]] = relationship(
        back_populates="tutor_course", cascade="all, delete-orphan"
    )


class PrivateCourse(Base):
    __tablename__ = "private_courses"

    id: MappedColumn[int] = mapped_column(primary_key=True, index=True)
    student_id: MappedColumn[int] = mapped_column(ForeignKey("users.id"))
    course_id: MappedColumn[int] = mapped_column(ForeignKey("tutor_courses.id"))
    price: MappedColumn[int] = mapped_column(Integer)

    student: Relationship["User"] = relationship(back_populates="private_courses")
    tutor_course: Relationship["TutorCourse"] = relationship(back_populates="private_courses")

    UniqueConstraint(student_id, course_id, name="unique_student_course")

    private_classes: Relationship[List["PrivateClass"]] = relationship(
        back_populates="private_course", cascade="all, delete-orphan"
    )


class PrivateClass(Base):
    __tablename__ = "private_classes"

    id: MappedColumn[int] = mapped_column(primary_key=True, index=True)
    private_course_id: MappedColumn[int] = mapped_column(ForeignKey("private_courses.id"))
    schedule_datetime: MappedColumn[DateTime] = mapped_column(DateTime(timezone=True))
    assignment: MappedColumn[JSONB] = mapped_column(JSONB)
    is_scheduled: MappedColumn[bool] = mapped_column(Boolean, server_default="true")
    has_occurred: MappedColumn[bool] = mapped_column(Boolean, server_default="false")
    is_paid: MappedColumn[bool] = mapped_column(Boolean, server_default="false")

    private_course: Relationship["PrivateCourse"] = relationship(back_populates="private_classes")


class Textbook(Base):
    __tablename__ = "textbooks"

    id: MappedColumn[int] = mapped_column(primary_key=True, index=True)
    title: MappedColumn[str] = mapped_column(String(255))
    tutor_course_id: MappedColumn[int] = mapped_column(ForeignKey("tutor_courses.id"))

    tutor_course: Relationship["TutorCourse"] = relationship(back_populates="textbooks")

    UniqueConstraint(title, tutor_course_id, name="unique_textbook_tutor_course")
