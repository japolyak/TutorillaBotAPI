from fastapi import status, APIRouter, Depends
from routes.data_transfer_models import TutorCourseDto, NewTutorCourseDto
from database.crud import tutor_course_crud
from sqlalchemy.orm import Session
from database.db_setup import session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


router = APIRouter()


@router.post(path="/users/{user_id}/", status_code=status.HTTP_201_CREATED,
             response_model=TutorCourseDto, description="Add course for tutor")
async def add_course(new_tutor_course: NewTutorCourseDto, user_id: int, db: Session = Depends(session)):
    # TODO - rewrite
    db_course = tutor_course_crud.add_course(db=db, user_id=user_id, course=new_tutor_course)
    course = jsonable_encoder(db_course)

    return JSONResponse(status_code=status.HTTP_200_OK, content=course)


@router.get(path="/users/{user_id}/subject-name/{subject_name}/", status_code=status.HTTP_200_OK,
            response_model=list[TutorCourseDto], description="Get available tutors")
async def get_available_tutors(user_id: int, subject_name: str, db: Session = Depends(session)):
    # TODO - rewrite
    db_tutors = tutor_course_crud.get_available_courses_by_subject(db=db, user_id=user_id, subject_name=subject_name)
    tutors = jsonable_encoder(db_tutors)

    return JSONResponse(status_code=status.HTTP_200_OK, content=tutors)
