from fastapi import APIRouter, Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from functions.telegram_valdiator import init_data_is_valid
from database.crud import user_crud
from database.db_setup import get_db
from urllib.parse import parse_qs
import json
from routes.schemas import UserDto

router = APIRouter()


@router.get(path="/me/", status_code=status.HTTP_200_OK, response_model=UserDto)
async def validate_telegram_user(request: Request, db: Session = Depends(get_db)):
    init_data: None or str = request.headers.get("Init-Data")

    if not init_data:
        raise HTTPException(status_code=400, detail="Bad request")

    if not init_data_is_valid(init_data):
        raise HTTPException(status_code=400, detail="Bad request")

    parsed_query = parse_qs(init_data)
    parsed_user = json.loads(parsed_query.get('user', [''])[0])
    user_id = parsed_user['id']

    db_user = user_crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user
