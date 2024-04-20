from fastapi import status, APIRouter, Depends
from .data_transfer_models import SubjectDto, Role
from sqlalchemy.orm import Session
from database.db_setup import session
from database.crud import subject_crud
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Literal


router = APIRouter()


@router.get(path="/users/{user_id}/available/{is_available}/", status_code=status.HTTP_200_OK,
            summary="Gets users subjects by user id", response_model=list[SubjectDto])
async def get_subjects(user_id: int, is_available: bool, role: Literal[Role.Student, Role.Tutor], db: Session = Depends(session)):
    role_to_function = {
        Role.Student: subject_crud.get_student_subjects,
        Role.Tutor: subject_crud.get_tutor_subjects
    }

    subjects_function = role_to_function.get(role)

    subjects = jsonable_encoder(subjects_function(db, user_id, is_available))

    return JSONResponse(status_code=status.HTTP_200_OK, content=subjects)
