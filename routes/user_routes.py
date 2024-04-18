from fastapi import status, Depends, HTTPException, APIRouter, Response
from .schemas import UserDto, UserBaseDto
from database.crud import user_crud
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from database.db_setup import session, cursor
import logging

router = APIRouter()


@router.get(path="/{user_id}/", status_code=status.HTTP_200_OK, response_model=UserDto)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print(db_user)
    return db_user

@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def add_user(user: UserBaseDto, db: Session = Depends(session)):
    stmnt = text("CALL add_user(:u_id, :u_first_name, :u_last_name, :u_email, :u_normalized_email, :u_time_zone, :u_locale, :error)")
    params = {'u_id': user.id, 'u_first_name': user.first_name, 'u_last_name': user.last_name, 'u_email': user.email, 'u_normalized_email': user.email.lower(), 'u_time_zone': user.time_zone, 'u_locale': user.locale, 'error': None}

    result = db.execute(stmnt, params)

    new_user = user_crud.create_user(db, user=user)
    return new_user
    error_msg = result.fetchall()[0][0]

    db.commit()
    db.close()

    if not error_msg:
        return Response(status_code=status.HTTP_201_CREATED)

    logging.error(error_msg)

    return Response("User Already exists", status_code=status.HTTP_400_BAD_REQUEST)


@router.post(path="/{user_id}/apply-role/{role}/", status_code=status.HTTP_201_CREATED)
async def apply_for_role(user_id: int, role: str, db: Session = Depends(get_db)):
    """
    Applies role to user
    """
    db_user = user_crud.get_user(db=db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user.is_student and role == "student":
        raise HTTPException(status_code=400, detail="User has student role")

    if db_user.is_tutor and role == "tutor":
        raise HTTPException(status_code=400, detail="User has tutor role")

    if db_user.users_requests:
        raise HTTPException(status_code=400, detail="User already made a role request")

    if role == "student":
        user_crud.apply_student_role(db=db, user=db_user)
    elif role == "tutor":
        user_crud.apply_tutor_role(db=db, user=db_user)

    return status.HTTP_201_CREATED
