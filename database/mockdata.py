from sqlalchemy.orm import Session
from sqlalchemy import Engine
from .models import User, Subject, TutorCourse, PrivateCourse, PrivateClass
from routes.schemas import SourceDto


def insert_mock_data(engine: Engine):
    with Session(engine) as session:
        user1 = User(
            id=1, is_active=True, time_zone=1, first_name="Firstname1", last_name="Lastname1", email="test1@test.com",
            normalized_email="test1@test.com", phone_number="+1", is_tutor=True, locale="en-US"
        )
        user2 = User(
            id=2, is_active=True, time_zone=1, first_name="Firstname2", last_name="Lastname2", email="test2@test.com",
            normalized_email="test2@test.com", phone_number="+2", is_tutor=True, locale="en-US"
        )
        user3 = User(
            id=3, is_active=True, time_zone=1, first_name="Firstname3", last_name="Lastname3", email="test3@test.com",
            normalized_email="test3@test.com", phone_number="+3", is_tutor=True, locale="en-US"
        )
        user4 = User(
            id=4, is_active=True, time_zone=1, first_name="Firstname4", last_name="Lastname4", email="test4@test.com",
            normalized_email="test4@test.com", phone_number="+4", is_student=True, locale="en-US"
        )
        user5 = User(
            id=5, is_active=True, time_zone=1, first_name="Firstname8", last_name="Lastname8", email="test8@test.com",
            normalized_email="test8@test.com", phone_number="+8", is_student=True, locale="en-US"
        )
        user6 = User(
            id=6, is_active=True, time_zone=1, first_name="Firstname9", last_name="Lastname9", email="test9@test.com",
            normalized_email="test9@test.com", phone_number="+9", is_student=True, locale="en-US"
        )
        artem = User(
            id=360375967, first_name="Artem", is_active=True, time_zone=1, last_name="Kryvolap", email="artemkryvolap@gmail.com",
            normalized_email="artemkryvolap@gmail.com", phone_number="+123456789", is_tutor=True, is_student=True, locale="pl-PL"
        )
        admin = User(
            id=6453257754, first_name="Admin", is_active=True, time_zone=1, last_name="Main", email="artemuo1337@gmail.com",
            normalized_email="artemuo1337@gmail.com", phone_number="+1234567890", is_admin=True, locale="en-US"
        )

        polish = Subject(name="Polish")
        english = Subject(name="English")

        tutor_course1 = TutorCourse(tutor_id=1, subject_id=1, price=10)
        tutor_course2 = TutorCourse(tutor_id=2, subject_id=2, price=10)
        tutor_course3 = TutorCourse(tutor_id=3, subject_id=2, price=10)
        tutor_course4 = TutorCourse(tutor_id=360375967, subject_id=2, price=10)

        private_course1 = PrivateCourse(student_id=4, course_id=4, price=10)
        private_course2 = PrivateCourse(student_id=5, course_id=4, price=10)
        private_course3 = PrivateCourse(student_id=6, course_id=4, price=10)
        private_course4 = PrivateCourse(student_id=360375967, course_id=1, price=10)
        private_course5 = PrivateCourse(student_id=360375967, course_id=2, price=10)
        private_course6 = PrivateCourse(student_id=360375967, course_id=3, price=10)

        source_one = SourceDto(title="Assignment 1", assignment="Do this").model_dump_json()
        source_two = SourceDto(title="Assignment 2", assignment="Do this again").model_dump_json()

        assignments = {
            "sources": [source_one, source_two]
        }

        private_class1 = PrivateClass(private_course_id=1, schedule_datetime="2021-06-01 12:00:00", assignment=assignments)
        private_class2 = PrivateClass(private_course_id=1, schedule_datetime="2021-06-01 12:00:00", assignment=assignments, is_scheduled=True, has_occurred=True)
        private_class3 = PrivateClass(private_course_id=1, schedule_datetime="2021-06-01 12:00:00", assignment=assignments, is_scheduled=True, has_occurred=True, is_paid=True)
        private_class4 = PrivateClass(private_course_id=2, schedule_datetime="2021-06-01 12:00:00", assignment=assignments, is_scheduled=True, has_occurred=True)
        private_class5 = PrivateClass(private_course_id=4, schedule_datetime="2021-06-01 12:00:00", assignment=assignments, is_scheduled=True)
        private_class6 = PrivateClass(private_course_id=4, schedule_datetime="2021-06-01 12:00:00", assignment=assignments, is_scheduled=True, has_occurred=True)

        session.add_all([user1, user2, user3, user4, user5, user6, artem, admin])
        session.add_all([polish, english])
        session.add_all([tutor_course1, tutor_course2, tutor_course3, tutor_course4])
        session.add_all([private_course1, private_course2, private_course3, private_course4, private_course5, private_course6])
        session.add_all([private_class1, private_class2, private_class3, private_class4, private_class5, private_class6])

        session.commit()
