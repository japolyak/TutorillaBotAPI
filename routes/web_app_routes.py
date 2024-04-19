from fastapi import APIRouter, Request, status, Depends
from sqlalchemy.orm import Session
from functions.telegram_valdiator import init_data_is_valid
from database.crud import user_crud
from database.db_setup import session
from urllib.parse import parse_qs
import json
from routes.data_transfer_models import UserDto
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get(path="/me/", status_code=status.HTTP_200_OK, response_model=UserDto,
            summary="Validates telegram user and returns user data")
async def validate_telegram_user(request: Request, db: Session = Depends(session)):
    init_data: None or str = request.headers.get("Init-Data")

    if not init_data:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'message': 'Telegram Init-Data is missing'})

    if not init_data_is_valid(init_data):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'message': 'Telegram Init-Data validation failed'})

    parsed_query = parse_qs(init_data)
    parsed_user = json.loads(parsed_query.get('user', [''])[0])
    user_id = parsed_user['id']

    db_user = user_crud.get_user(db=db, user_id=user_id)

    if db_user is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'User was not found'})

    user = jsonable_encoder(db_user)

    return JSONResponse(status_code=status.HTTP_200_OK, content=user)
