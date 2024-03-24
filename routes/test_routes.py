from fastapi import APIRouter
from bot_client.message_sender import send_test_message
from config import my_tg_id


router = APIRouter()

@router.post("/")
async def root():
    send_test_message(my_tg_id)
    return {"message": "Hello World!"}
