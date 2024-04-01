from fastapi import status, Depends, HTTPException, APIRouter, Request
from bot_client.message_sender import send_decline_message
from .schemas import UserDto, UserRequestDto
from database.crud import user_crud, admin_crud
from sqlalchemy.orm import Session
from database.db_setup import get_db


router = APIRouter()


@router.get(path="/role-requests/{role}/", status_code=status.HTTP_200_OK, response_model=list[UserRequestDto])
async def get_requests(role: str, db: Session = Depends(get_db)):
    db_requests = admin_crud.get_users_requests(db=db, role=role)
    if db_requests is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_requests


@router.get(path="/user-requests/{role_request_id}/", status_code=status.HTTP_200_OK, response_model=UserRequestDto)
async def get_requests(role_request_id: int, db: Session = Depends(get_db)):
    db_request = admin_crud.get_user_request(db=db, role_request_id=role_request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")

    return db_request


@router.put(path="/users/{user_id}/accept-role/{role}/", status_code=status.HTTP_200_OK, response_model=UserDto)
async def accept_student_role(user_id: int, role: str, db: Session = Depends(get_db)):
    # admin_id: None or str = request.headers.get("Sender-Id")
    # if not admin_id:
    #     raise HTTPException(status_code=400, detail="Bad request")
    #
    # db_admin = user_crud.get_user(db=db, user_id=int(admin_id))
    #
    # if db_admin is None:
    #     raise HTTPException(status_code=404, detail="User not found")
    #
    # if not db_admin.is_admin:
    #     raise HTTPException(status_code=400, detail="Access denied")

    db_user = user_crud.get_user(db=db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user.is_tutor:
        raise HTTPException(status_code=400, detail="User has tutor role")

    if db_user.is_student:
        raise HTTPException(status_code=400, detail="User has student role")

    acceptance = user_crud.accept_role_request(db=db, user_id=user_id, role=role)

    if not acceptance:
        raise HTTPException(status_code=404, detail="Users request not found")

    # send_accept_message(db_user)

    return acceptance


@router.put(path="/users/{user_id}/decline-role/", status_code=status.HTTP_200_OK)
async def accept_student_role(user_id: int, db: Session = Depends(get_db)):
    # admin_id: None or str = request.headers.get("Sender-Id")
    # if not admin_id:
    #     raise HTTPException(status_code=400, detail="Bad request")
    #
    # db_admin = user_crud.get_user(db=db, user_id=int(admin_id))
    #
    # if db_admin is None:
    #     raise HTTPException(status_code=404, detail="User not found")
    #
    # if not db_admin.is_admin:
    #     raise HTTPException(status_code=400, detail="Access denied")

    db_user = user_crud.get_user(db=db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    declination = user_crud.decline_role_request(db=db, user_id=user_id)

    if not declination:
        raise HTTPException(status_code=404, detail="Users request not found")

    send_decline_message(db_user.id)

    return status.HTTP_200_OK
