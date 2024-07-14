from fastapi import APIRouter
from src.routers.api_enpoints import APIEndpoints


router = APIRouter(prefix=APIEndpoints.Test.Prefix, tags=["test"])


@router.get(APIEndpoints.Test.Get)
async def root():
    return {"message": f"Hello World!"}
