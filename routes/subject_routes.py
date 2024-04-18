from fastapi import status, APIRouter, Depends, HTTPException
from .data_transfer_models import SubjectDto
from sqlalchemy.orm import Session
from database.db_setup import session
from database.crud import subject_crud

router = APIRouter()


@router.get(path="/available-subjects/users/{user_id}/", status_code=status.HTTP_200_OK,
            response_model=list[SubjectDto], description="Get available courses")
async def get_available_courses(user_id: int, role: str, db: Session = Depends(session)):
    if role not in ("tutor", "student"):
        raise HTTPException(status_code=400)

    if role == "student":
        db_available_subjects = subject_crud.get_available_subjects_student(db=db, user_id=user_id)
        return db_available_subjects

    db_available_subjects = subject_crud.get_available_subjects_tutor(db=db, user_id=user_id)
    return db_available_subjects


@router.get(path="/users/{user_id}/", status_code=status.HTTP_200_OK,
            response_model=list[SubjectDto], description="Get private courses")
async def get_subjects(user_id: int, role: str, db: Session = Depends(session)):
    if role not in ("tutor", "student"):
        raise HTTPException(status_code=400)

    if role == "student":
        db_student_subjects = subject_crud.get_student_subjects(db=db, user_id=user_id)
        return db_student_subjects

    db_tutor_subjects = subject_crud.get_tutor_courses(db=db, user_id=user_id)
    return db_tutor_subjects
