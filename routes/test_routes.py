from fastapi import APIRouter, status, HTTPException
from bot_client.message_sender import send_test_message
from config import my_tg_id


router = APIRouter()


@router.post("/")
async def root():
    return {"message": "Hello World!"}
