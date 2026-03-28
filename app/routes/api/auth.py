from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserLoginRequest
from app.services.auth_service import create_user, login_user
from app.db.dependency import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user.email, user.name, user.password)

@router.post("/login")
def login(user: UserLoginRequest, db: Session = Depends(get_db)):
        return login_user(db, user.email, user.password)

