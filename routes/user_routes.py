from fastapi import status, Depends, APIRouter, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from routes.data_transfer_models import UserDto, UserBaseDto, Role
from database.crud import user_crud
from sqlalchemy.orm import Session
from database.db_setup import session
from routes.sql_statement_repository import sql_statements
from datetime import datetime
from typing import Literal


router = APIRouter()


@router.get(path="/{user_id}/", status_code=status.HTTP_200_OK, response_model=UserDto, summary="Gets user by id")
async def get_user(user_id: int, db: Session = Depends(session)):
    db_user = user_crud.get_user(db=db, user_id=user_id)

    if db_user is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'User was not found'})

    user = jsonable_encoder(db_user)

    return JSONResponse(status_code=status.HTTP_200_OK, content=user)


@router.post(path="/", status_code=status.HTTP_201_CREATED, summary="Adds a new user")
async def add_user(user: UserBaseDto, db: Session = Depends(session)):
    params = {
        'u_id': user.id,
        'u_first_name': user.first_name,
        'u_last_name': user.last_name,
        'u_email': user.email,
        'u_normalized_email': user.email.lower(),
        'u_time_zone': user.time_zone,
        'u_locale': user.locale,
        'error': None
    }

    result = db.execute(sql_statements.add_user, params)

    error_msg = result.fetchall()[0][0]

    db.commit()
    db.close()

    if not error_msg:
        return Response(status_code=status.HTTP_201_CREATED)

    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'User addition was not successful'})


@router.post(path="/{user_id}/apply-role/{role}/", status_code=status.HTTP_201_CREATED)
async def apply_for_role(user_id: int, role: Literal[Role.Student, Role.Tutor], db: Session = Depends(session)):
    params = {
        'u_id': user_id,
        'u_student': role == Role.Student,
        'u_tutor': role == Role.Tutor,
        'u_request_datetime': datetime.now(),
        'error': None
    }

    result = db.execute(sql_statements.add_user_role_request, params)

    error_msg = result.fetchall()[0][0]

    db.commit()
    db.close()

    if error_msg is not None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'Role application was not successful'})

    return Response(status_code=status.HTTP_201_CREATED)
