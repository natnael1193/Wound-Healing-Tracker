from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.utils.response import success_response

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/me")
def get_me(current_user = Depends(get_current_user)):
    return success_response(current_user, "User retrieved successfully")
