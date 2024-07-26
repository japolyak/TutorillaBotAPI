from sqlalchemy import String, BigInteger, Boolean, ForeignKey, UniqueConstraint, DateTime, Integer, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped
from typing import List


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, autoincrement=False, primary_key=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="false")
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    normalized_email: Mapped[str] = mapped_column(String(255), unique=True)
    time_zone: Mapped[float] = mapped_column(Float)
    locale: Mapped[str] = mapped_column(String(10), server_default="en-US")
    is_tutor: Mapped[bool] = mapped_column(Boolean, server_default="false")
    is_student: Mapped[bool] = mapped_column(Boolean, server_default="false")
    is_admin: Mapped[bool] = mapped_column(Boolean, server_default="false")

    tutor_courses: Mapped[List["TutorCourse"]] = relationship(
        back_populates="tutor", cascade="all, delete-orphan"
    )

    private_courses: Mapped[List["PrivateCourse"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )

    users_requests: Mapped[List["UserRequest"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class UserRequest(Base):
    __tablename__ = "users_requests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    request_datetime: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    tutor_role: Mapped[bool] = mapped_column(Boolean, server_default="false")
    student_role: Mapped[bool] = mapped_column(Boolean, server_default="false")

    user: Mapped["User"] = relationship(back_populates="users_requests")

    UniqueConstraint(user_id, name="unique_user_request")


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)

    tutor_courses: Mapped[List["TutorCourse"]] = relationship(
        back_populates="subject", cascade="all, delete-orphan"
    )


class TutorCourse(Base):
    __tablename__ = "tutor_courses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tutor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="true")
    price: Mapped[int] = mapped_column(Integer)

    tutor: Mapped["User"] = relationship(back_populates="tutor_courses")
    subject: Mapped["Subject"] = relationship(back_populates="tutor_courses")

    UniqueConstraint(tutor_id, subject_id, name="unique_tutor_subject")

    private_courses: Mapped[List["PrivateCourse"]] = relationship(
        back_populates="tutor_course", cascade="all, delete-orphan"
    )

    textbooks: Mapped[List["Textbook"]] = relationship(
        back_populates="tutor_course", cascade="all, delete-orphan"
    )


class PrivateCourse(Base):
    __tablename__ = "private_courses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("tutor_courses.id"))
    price: Mapped[int] = mapped_column(Integer)

    student:Mapped["User"] = relationship(back_populates="private_courses")
    tutor_course:Mapped["TutorCourse"] = relationship(back_populates="private_courses")

    UniqueConstraint(student_id, course_id, name="unique_student_course")

    private_classes: Mapped[List["PrivateClass"]] = relationship(
        back_populates="private_course", cascade="all, delete-orphan"
    )


class PrivateClass(Base):
    __tablename__ = "private_classes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    private_course_id: Mapped[int] = mapped_column(ForeignKey("private_courses.id"))
    schedule_datetime: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    assignment: Mapped[JSONB] = mapped_column(JSONB)
    is_scheduled: Mapped[bool] = mapped_column(Boolean, server_default="true")
    has_occurred: Mapped[bool] = mapped_column(Boolean, server_default="false")
    is_paid: Mapped[bool] = mapped_column(Boolean, server_default="false")

    private_course: Mapped["PrivateCourse"] = relationship(back_populates="private_classes")


class Textbook(Base):
    __tablename__ = "textbooks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    tutor_course_id: Mapped[int] = mapped_column(ForeignKey("tutor_courses.id"))

    tutor_course: Mapped["TutorCourse"] = relationship(back_populates="textbooks")

    UniqueConstraint(title, tutor_course_id, name="unique_textbook_tutor_course")
