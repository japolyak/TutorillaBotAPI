from sqlalchemy.orm import Session
from .models import User, Subject, TutorCourse, PrivateCourse


def insert_mock_data(engine):
    with Session(engine) as session:
        user1 = User(
            id=1, first_name="Firstname1", last_name="Lastname1", email="test1@test.com",
            normalized_email="test1@test.com", phone_number="+1", is_tutor=True
        )
        user2 = User(
            id=2, first_name="Firstname2", last_name="Lastname2", email="test2@test.com",
            normalized_email="test2@test.com", phone_number="+2", is_tutor=True
        )
        user3 = User(
            id=3, first_name="Firstname3", last_name="Lastname3", email="test3@test.com",
            normalized_email="test3@test.com", phone_number="+3", is_tutor=True
        )
        user4 = User(
            id=4, first_name="Firstname4", last_name="Lastname4", email="test4@test.com",
            normalized_email="test4@test.com", phone_number="+4", is_tutor=True
        )
        user5 = User(
            id=5, first_name="Firstname5", last_name="Lastname5", email="test5@test.com",
            normalized_email="test5@test.com", phone_number="+5", is_tutor=True
        )
        user6 = User(
            id=6, first_name="Firstname6", last_name="Lastname6", email="test6@test.com",
            normalized_email="test6@test.com", phone_number="+6", is_tutor=True
        )
        user7 = User(
            id=7, first_name="Firstname7", last_name="Lastname7", email="test7@test.com",
            normalized_email="test7@test.com", phone_number="+7", is_tutor=True
        )
        user8 = User(
            id=8, first_name="Firstname8", last_name="Lastname8", email="test8@test.com",
            normalized_email="test8@test.com", phone_number="+8", is_student=True
        )
        user9 = User(
            id=9, first_name="Firstname9", last_name="Lastname9", email="test9@test.com",
            normalized_email="test9@test.com", phone_number="+9", is_student=True
        )
        user10 = User(
            id=10, first_name="Firstname10", last_name="Lastname10", email="test10@test.com",
            normalized_email="test10@test.com", phone_number="+10", is_student=True
        )
        user11 = User(
            id=11, first_name="Firstname11", last_name="Lastname11", email="test11@test.com",
            normalized_email="test11@test.com", phone_number="+11", is_student=True
        )
        user12 = User(
            id=12, first_name="Firstname12", last_name="Lastname12", email="test12@test.com",
            normalized_email="test12@test.com", phone_number="+12", is_student=True
        )
        user13 = User(
            id=13, first_name="Firstname13", last_name="Lastname13", email="test13@test.com",
            normalized_email="test13@test.com", phone_number="+13", is_student=True
        )
        user14 = User(
            id=14, first_name="Firstname14", last_name="Lastname14", email="test14@test.com",
            normalized_email="test14@test.com", phone_number="+14", is_student=True
        )
        artem = User(
            id=360375967, first_name="Artem", last_name="Kryvolap", email="artemkryvolap@gmail.com",
            normalized_email="artemkryvolap@gmail.com", phone_number="+123456789", is_tutor=True, is_student=True
        )
        admin = User(
            id=6453257754, first_name="Admin", last_name="Main", email="artemuo1337@gmail.com",
            normalized_email="artemuo1337@gmail.com", phone_number="+1234567890", is_tutor=True, is_student=True
        )

        polish = Subject(name="Polish")
        english = Subject(name="English")
        math = Subject(name="Math")
        physics = Subject(name="Physics")
        chemistry = Subject(name="Chemistry")

        tutor_course1 = TutorCourse(tutor_id=2, subject_id=2)
        tutor_course2 = TutorCourse(tutor_id=2, subject_id=3)
        tutor_course3 = TutorCourse(tutor_id=3, subject_id=4)
        tutor_course4 = TutorCourse(tutor_id=3, subject_id=3)
        tutor_course5 = TutorCourse(tutor_id=4, subject_id=5)
        tutor_course6 = TutorCourse(tutor_id=4, subject_id=4)
        tutor_course7 = TutorCourse(tutor_id=5, subject_id=5)
        tutor_course8 = TutorCourse(tutor_id=6, subject_id=1)
        tutor_course9 = TutorCourse(tutor_id=360375967, subject_id=4)
        tutor_course10 = TutorCourse(tutor_id=360375967, subject_id=3)
        tutor_course11 = TutorCourse(tutor_id=360375967, subject_id=1)
        tutor_course12 = TutorCourse(tutor_id=360375967, subject_id=2)

        session.add_all([user1, user2, user3, user4, user5, user6, user7, user8, user9, user10, user11, user12, user13,
                         user14, artem, admin])
        session.add_all([polish, english, math, physics, chemistry])
        session.add_all([tutor_course1, tutor_course2, tutor_course3, tutor_course4, tutor_course5, tutor_course6,
                         tutor_course7, tutor_course8, tutor_course9, tutor_course10, tutor_course11, tutor_course12])

        session.commit()
