from fastapi import status, Depends, HTTPException, APIRouter
from .schemas import UserDto, UserBaseDto
from database.crud import user_crud
from sqlalchemy.orm import Session
from database.db_setup import get_db


router = APIRouter()


@router.get(path="/{user_id}/", status_code=status.HTTP_200_OK, response_model=UserDto)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print(db_user)
    return db_user


@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=UserDto)
async def create_user(user: UserBaseDto, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db=db, user_id=user.id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")

    new_user = user_crud.create_user(db, user=user)
    return new_user


@router.post(path="/{user_id}/apply-role/{role}/", status_code=status.HTTP_201_CREATED)
async def apply_student_role(user_id: int, role: str, db: Session = Depends(get_db)):
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
