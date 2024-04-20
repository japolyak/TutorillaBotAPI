from fastapi import APIRouter


router = APIRouter()


@router.post("/")
async def root():
    return {"message": "Hello World!"}
