from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.utils.response import success_response
from app.db.dependency import get_db
from sqlalchemy.orm import Session
from app.schemas.user import UserUpdateRequest, UserMe

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/me")
def get_me(current_user = Depends(get_current_user)):
    return success_response(current_user, "User retrieved successfully")

@router.put("/update")
def update_user_info(request: UserUpdateRequest, current_user = Depends(get_current_user),  db: Session = Depends(get_db)):
    from app.services.user_service import update_user
    result = update_user(db, current_user, request.name)
    return result

