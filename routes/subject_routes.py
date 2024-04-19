from fastapi import status, APIRouter, Depends, HTTPException
from .data_transfer_models import SubjectDto, Role
from sqlalchemy.orm import Session
from database.db_setup import session
from database.crud import subject_crud
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Literal


router = APIRouter()


@router.get(path="/available-subjects/users/{user_id}/", status_code=status.HTTP_200_OK,
            response_model=list[SubjectDto], summary="Get available courses to teach or learn by user id")
async def get_available_courses(user_id: int, role: Literal[Role.Student, Role.Tutor], db: Session = Depends(session)):
    # TODO - rewrite
    if role == Role.Student:
        db_available_subjects = subject_crud.get_available_subjects_student(db=db, user_id=user_id)
        subjects = jsonable_encoder(db_available_subjects)

        return JSONResponse(status_code=status.HTTP_200_OK, content=subjects)

    db_available_subjects = subject_crud.get_available_subjects_tutor(db=db, user_id=user_id)
    subjects = jsonable_encoder(db_available_subjects)

    return JSONResponse(status_code=status.HTTP_200_OK, content=subjects)


@router.get(path="/users/{user_id}/", status_code=status.HTTP_200_OK, summary="Gets users subjects by user id",
            response_model=list[SubjectDto])
async def get_subjects(user_id: int, role: Literal[Role.Student, Role.Tutor], db: Session = Depends(session)):
    # TODO - rewrite
    if role == "student":
        db_student_subjects = subject_crud.get_student_subjects(db=db, user_id=user_id)
        subjects = jsonable_encoder(db_student_subjects)

        return JSONResponse(status_code=status.HTTP_200_OK, content=subjects)

    db_tutor_subjects = subject_crud.get_tutor_courses(db=db, user_id=user_id)
    subjects = jsonable_encoder(db_tutor_subjects)

    return JSONResponse(status_code=status.HTTP_200_OK, content=subjects)
