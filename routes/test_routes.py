from fastapi import APIRouter
from routes.api_enpoints import APIEndpoints


router = APIRouter(prefix=APIEndpoints.Test.Prefix, tags=["test"])


@router.post(APIEndpoints.Test.Post)
async def root():
    return {"message": "Hello World!"}
