from sqlalchemy.orm import Session
from sqlalchemy import Engine
from src.database.models import User, Subject, TutorCourse, PrivateCourse, PrivateClass, Textbook
from src.models import SourceDto
from src.config import my_tg_id, admin_tg_id


def insert_mock_data(engine: Engine):
    with Session(engine) as session:
        user1 = User(
            id=1, is_active=True, time_zone=1, first_name="Firstname1", last_name="Lastname1", email="test1@test.com",
            normalized_email="test1@test.com", is_tutor=True, locale="en-US"
        )
        user2 = User(
            id=2, is_active=True, time_zone=1, first_name="Firstname2", last_name="Lastname2", email="test2@test.com",
            normalized_email="test2@test.com", is_tutor=True, locale="en-US"
        )
        user3 = User(
            id=3, is_active=True, time_zone=1, first_name="Firstname3", last_name="Lastname3", email="test3@test.com",
            normalized_email="test3@test.com", is_tutor=True, locale="en-US"
        )
        user4 = User(
            id=4, is_active=True, time_zone=1, first_name="Firstname4", last_name="Lastname4", email="test4@test.com",
            normalized_email="test4@test.com", is_student=True, locale="en-US"
        )
        user5 = User(
            id=5, is_active=True, time_zone=-1, first_name="Firstname8", last_name="Lastname8", email="test8@test.com",
            normalized_email="test8@test.com", is_student=True, locale="en-US"
        )
        user6 = User(
            id=6, is_active=True, time_zone=1, first_name="Firstname9", last_name="Lastname9", email="test9@test.com",
            normalized_email="test9@test.com", is_student=True, locale="en-US"
        )
        artem = User(
            id=my_tg_id, first_name="Artem", is_active=True, time_zone=1, last_name="Kryvolap", email="me@me.com",
            normalized_email="me@me.com", is_tutor=True, is_student=True, locale="en-US"
        )
        admin = User(
            id=admin_tg_id, first_name="Admin", is_active=True, time_zone=1, last_name="Main", email="admin@admin.com",
            normalized_email="admin@admin.com", is_admin=True, locale="en-US"
        )

        polish = Subject(name="Polish")
        english = Subject(name="English")

        session.add_all([user1, user2, user3, user4, user5, user6, artem, admin])
        session.add_all([polish, english])
        session.commit()

        tutor_course1 = TutorCourse(tutor_id=user1.id, subject_id=polish.id, price=10)
        tutor_course2 = TutorCourse(tutor_id=user2.id, subject_id=english.id, price=10)
        tutor_course3 = TutorCourse(tutor_id=user3.id, subject_id=english.id, price=10)
        tutor_course4 = TutorCourse(tutor_id=my_tg_id, subject_id=english.id, price=10)

        session.add_all([tutor_course1, tutor_course2, tutor_course3, tutor_course4])
        session.commit()

        hurra_1 = Textbook(title="Hurra po Polsku 1", tutor_course_id=tutor_course1.id)
        hurra_2 = Textbook(title="Hurra po Polsku 2", tutor_course_id=tutor_course1.id)
        hurra_3 = Textbook(title="Hurra po Polsku 3", tutor_course_id=tutor_course1.id)
        umiesz_zdasz = Textbook(title="Umiesz? zdasz!", tutor_course_id=tutor_course1.id)
        czas_na_czasownik = Textbook(title="Czas na czasownik", tutor_course_id=tutor_course1.id)

        session.add_all([hurra_1, hurra_2, hurra_3, umiesz_zdasz, czas_na_czasownik])
        session.commit()

        private_course1 = PrivateCourse(student_id=user4.id, tutor_course_id=tutor_course4.id, price=10)
        private_course2 = PrivateCourse(student_id=user5.id, tutor_course_id=tutor_course4.id, price=10)
        private_course3 = PrivateCourse(student_id=user6.id, tutor_course_id=tutor_course4.id, price=10)
        private_course4 = PrivateCourse(student_id=my_tg_id, tutor_course_id=tutor_course1.id, price=10)
        private_course5 = PrivateCourse(student_id=my_tg_id, tutor_course_id=tutor_course2.id, price=10)
        private_course6 = PrivateCourse(student_id=my_tg_id, tutor_course_id=tutor_course3.id, price=10)

        session.add_all([private_course1, private_course2, private_course3, private_course4, private_course5, private_course6])
        session.commit()

        source_one = SourceDto(title="Assignment 1", assignment="Do this").model_dump_json()
        source_two = SourceDto(title="Assignment 2", assignment="Do this again").model_dump_json()

        assignments = {
            "sources": [source_one, source_two]
        }

        private_class1 = PrivateClass(private_course_id=private_course1.id, schedule_datetime="2021-06-01 12:00:00", assignment=assignments)
        private_class2 = PrivateClass(private_course_id=private_course1.id, schedule_datetime="2021-06-01 12:00:00", assignment=assignments, is_scheduled=True, has_occurred=True)
        private_class3 = PrivateClass(private_course_id=private_course1.id, schedule_datetime="2021-06-01 12:00:00", assignment=assignments, is_scheduled=True, has_occurred=True, is_paid=True)
        private_class4 = PrivateClass(private_course_id=private_course2.id, schedule_datetime="2021-06-01 12:00:00", assignment=assignments, is_scheduled=True, has_occurred=True)
        private_class5 = PrivateClass(private_course_id=private_course4.id, schedule_datetime="2021-06-01 12:00:00", assignment=assignments, is_scheduled=True)
        private_class6 = PrivateClass(private_course_id=private_course4.id, schedule_datetime="2021-06-01 12:00:00", assignment=assignments, is_scheduled=True, has_occurred=True)

        session.add_all([private_class1, private_class2, private_class3, private_class4, private_class5, private_class6])
        session.commit()
