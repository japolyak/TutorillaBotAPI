from fastapi import status, Depends, APIRouter
from bot_client.message_sender import send_decline_message
from routers.data_transfer_models import UserDto, UserRequestDto, Role
from database.crud import user_crud, admin_crud
from sqlalchemy.orm import Session
from database.db_setup import session
from typing import Literal
from builders.response_builder import ResponseBuilder
from routers.api_enpoints import APIEndpoints


router = APIRouter(prefix=APIEndpoints.Admin.Prefix, tags=["admin"])


@router.get(path=APIEndpoints.Admin.GetRequests, status_code=status.HTTP_200_OK, response_model=list[UserRequestDto],
            summary="Get all requests by role")
async def get_requests(role: Literal[Role.Student], db: Session = Depends(session)):
    # TODO - rewrite
    response_models = admin_crud.get_users_requests(db=db, role=role)

    if response_models is None:
        return ResponseBuilder.error_response(message=f'Requests for {role} were not found')

    return ResponseBuilder.success_response(content=response_models)


@router.get(path=APIEndpoints.Admin.GetRequest, status_code=status.HTTP_200_OK, response_model=UserRequestDto,
            summary="Get request by request id")
async def get_request(role_request_id: int, db: Session = Depends(session)):
    # TODO - rewrite
    db_request = admin_crud.get_user_request(db=db, role_request_id=role_request_id)

    if db_request is None:
        return ResponseBuilder.error_response(message='User request was not found')

    return ResponseBuilder.success_response(content=UserRequestDto.model_validate(db_request))


@router.put(path=APIEndpoints.Admin.AcceptRole, status_code=status.HTTP_200_OK, response_model=UserDto,
            summary="Accept user role request")
async def accept_role(user_id: int, role: Literal[Role.Student], db: Session = Depends(session)):
    # TODO - rewrite
    db_user = user_crud.get_user(db=db, user_id=user_id)

    if db_user is None:
        return ResponseBuilder.error_response(message='User was not found')

    if db_user.is_tutor:
        return ResponseBuilder.error_response(message='User has tutor role')

    if db_user.is_student:
        return ResponseBuilder.error_response(message='User has student role')

    response_model = user_crud.accept_role_request(db=db, user_id=user_id, role=role)

    if not response_model:
        return ResponseBuilder.error_response(message='Role request was not found')

    return ResponseBuilder.success_response(content=response_model)


@router.put(path=APIEndpoints.Admin.DeclineRole, status_code=status.HTTP_200_OK, summary="Decline user role request")
async def decline_student_role(user_id: int, db: Session = Depends(session)):
    # TODO - rewrite
    db_user = user_crud.get_user(db=db, user_id=user_id)

    if db_user is None:
        return ResponseBuilder.error_response(message='User was not found')

    declination = user_crud.decline_role_request(db=db, user_id=user_id)

    if not declination:
        return ResponseBuilder.error_response(message='Role request was not found')

    send_decline_message(db_user.id)

    return ResponseBuilder.success_response()
