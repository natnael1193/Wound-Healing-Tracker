from typing import Any, Optional
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = 200
):

    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": jsonable_encoder(data)
        }
    )


def error_response(
    message: str = "Error",
    status_code: int = 400,
    data: Optional[Any] = None
):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": None
        }
    )