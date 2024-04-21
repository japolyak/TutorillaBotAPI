from fastapi import status, APIRouter, Depends
from .data_transfer_models import SubjectDto, Role
from sqlalchemy.orm import Session
from database.db_setup import session
from database.crud import subject_crud
from typing import Literal
from builders.response_builder import ResponseBuilder
from routers.api_enpoints import APIEndpoints


router = APIRouter(prefix=APIEndpoints.Subjects.Prefix, tags=["subjects"])


@router.get(path=APIEndpoints.Subjects.Get, status_code=status.HTTP_200_OK,
            summary="Gets users subjects by user id", response_model=list[SubjectDto])
async def get_subjects(user_id: int, is_available: bool, role: Literal[Role.Student, Role.Tutor], db: Session = Depends(session)):
    role_to_function = {
        Role.Student: subject_crud.get_student_subjects,
        Role.Tutor: subject_crud.get_tutor_subjects
    }

    subjects_func = role_to_function.get(role)

    response_models = subjects_func(db, user_id, is_available)

    if not response_models:
        return ResponseBuilder.success_response(content=[])

    return ResponseBuilder.success_response(content=response_models)
