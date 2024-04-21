from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import Response, status
from typing import Any


class ResponseBuilder:
    @classmethod
    def error_response(cls, status_code: int = status.HTTP_400_BAD_REQUEST, message: str = 'Bad request'):
        return JSONResponse(status_code=status_code, content=jsonable_encoder({"detail": message}))

    @classmethod
    def success_response(cls, status_code: int = status.HTTP_200_OK, content: Any = None):
        if not content:
            return Response(status_code=status_code)

        return JSONResponse(status_code=status_code, content=jsonable_encoder(content))
