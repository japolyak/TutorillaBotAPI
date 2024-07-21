from fastapi import APIRouter
from src.routers.api_enpoints import APIEndpoints


router = APIRouter()


@router.get(APIEndpoints.Home.Get)
async def root():
    return {"message": f"Welcome home!"}
