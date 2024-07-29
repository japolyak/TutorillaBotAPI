from sqlalchemy import String, BigInteger, Boolean, ForeignKey, UniqueConstraint, DateTime, Integer, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped, MappedColumn
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
        "TutorCourse", back_populates="tutor", cascade="all, delete-orphan"
    )

    private_courses: Mapped[List["PrivateCourse"]] = relationship(
        "PrivateCourse", back_populates="student", cascade="all, delete-orphan"
    )

    user_request: Mapped["UserRequest"] = relationship("UserRequest", uselist=False, back_populates="user")


class UserRequest(Base):
    __tablename__ = "users_requests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    request_datetime: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    tutor_role: Mapped[bool] = mapped_column(Boolean, server_default="false")
    student_role: Mapped[bool] = mapped_column(Boolean, server_default="false")

    user: Mapped["User"] = relationship("User", back_populates="user_request")


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)

    tutor_courses: Mapped[List["TutorCourse"]] = relationship(
        "TutorCourse", back_populates="subject", cascade="all, delete-orphan"
    )


class TutorCourse(Base):
    __tablename__ = "tutor_courses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tutor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="true")
    price: Mapped[int] = mapped_column(Integer)

    tutor: Mapped["User"] = relationship("User", back_populates="tutor_courses")
    subject: Mapped["Subject"] = relationship("Subject", back_populates="tutor_courses")

    __table_args__ = (UniqueConstraint(tutor_id, subject_id, name="unique_tutor_subject"),)

    private_courses: Mapped[List["PrivateCourse"]] = relationship(
        "PrivateCourse", back_populates="tutor_course", cascade="all, delete-orphan"
    )

    textbooks: Mapped[List["Textbook"]] = relationship(
        "Textbook", back_populates="tutor_course", cascade="all, delete-orphan"
    )


class PrivateCourse(Base):
    __tablename__ = "private_courses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    tutor_course_id: Mapped[int] = mapped_column(ForeignKey("tutor_courses.id"))
    price: Mapped[int] = mapped_column(Integer)

    student: Mapped["User"] = relationship("User", back_populates="private_courses")
    tutor_course: Mapped["TutorCourse"] = relationship("TutorCourse", back_populates="private_courses")

    __table_args__ = (UniqueConstraint(student_id, tutor_course_id, name="unique_student_course"),)

    private_classes: Mapped[List["PrivateClass"]] = relationship(
        "PrivateClass", back_populates="private_course", cascade="all, delete-orphan"
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

    private_course: Mapped["PrivateCourse"] = relationship("PrivateCourse", back_populates="private_classes")


class Textbook(Base):
    __tablename__ = "textbooks"

    id: MappedColumn[int] = mapped_column(primary_key=True, index=True)
    title: MappedColumn[str] = mapped_column(String(255))
    tutor_course_id: MappedColumn[int] = mapped_column(ForeignKey("tutor_courses.id"))

    tutor_course: Mapped["TutorCourse"] = relationship("TutorCourse", back_populates="textbooks")

    __table_args__ = (UniqueConstraint(title, tutor_course_id, name="unique_textbook_tutor_course"),)
