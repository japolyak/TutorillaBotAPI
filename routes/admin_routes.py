from fastapi import status, Depends, APIRouter, Response
from bot_client.message_sender import send_decline_message
from .data_transfer_models import UserDto, UserRequestDto, Role
from database.crud import user_crud, admin_crud
from sqlalchemy.orm import Session
from database.db_setup import session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Literal

router = APIRouter()


@router.get(path="/role-requests/{role}/", status_code=status.HTTP_200_OK, response_model=list[UserRequestDto],
            summary="Get all requests by role")
async def get_requests(role: Literal[Role.Student], db: Session = Depends(session)):
    # TODO - rewrite
    db_requests = admin_crud.get_users_requests(db=db, role=role)

    if db_requests is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': f'Requests for {role} were not found'})

    requests = jsonable_encoder(db_requests)

    return JSONResponse(status_code=status.HTTP_200_OK, content=requests)


@router.get(path="/user-requests/{role_request_id}/", status_code=status.HTTP_200_OK, response_model=UserRequestDto,
            summary="Get request by request id")
async def get_requests(role_request_id: int, db: Session = Depends(session)):
    # TODO - rewrite
    db_request = admin_crud.get_user_request(db=db, role_request_id=role_request_id)

    if db_request is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'User request was not found'})

    user_request = jsonable_encoder(UserRequestDto.model_validate(db_request))

    return JSONResponse(status_code=status.HTTP_200_OK, content=user_request)


@router.put(path="/users/{user_id}/accept-role/{role}/", status_code=status.HTTP_200_OK, response_model=UserDto,
            summary="Accept user role request")
async def accept_role(user_id: int, role: Literal[Role.Student], db: Session = Depends(session)):
    # TODO - rewrite
    db_user = user_crud.get_user(db=db, user_id=user_id)

    if db_user is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'User was not found'})

    if db_user.is_tutor:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'User has tutor role'})

    if db_user.is_student:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'User has student role'})

    acceptance = user_crud.accept_role_request(db=db, user_id=user_id, role=role)

    if not acceptance:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'Role request was not found'})

    user = jsonable_encoder(acceptance)

    return JSONResponse(status_code=status.HTTP_200_OK, content=user)


@router.put(path="/users/{user_id}/decline-role/", status_code=status.HTTP_200_OK, summary="Decline user role request")
async def decline_student_role(user_id: int, db: Session = Depends(session)):
    # TODO - rewrite
    db_user = user_crud.get_user(db=db, user_id=user_id)

    if db_user is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'User was not found'})

    declination = user_crud.decline_role_request(db=db, user_id=user_id)

    if not declination:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'Role request was not found'})

    send_decline_message(db_user.id)

    return Response()
