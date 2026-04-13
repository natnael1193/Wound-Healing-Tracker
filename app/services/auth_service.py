from sqlalchemy.orm import Session
from app.db.models.user import User
from passlib.context import CryptContext
from app.core.security import verify_password, create_access_token
from app.utils.response import success_response, error_response

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "supersecretkey"  # change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def hash_password(password: str):
    return pwd_context.hash(password)

def create_user(db: Session, email: str, name: str, password: str):
    hashed_pw = hash_password(password)

    user = User(
        email=email,
        name=name,
        password_hash=hashed_pw
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return success_response(user, "User created successfully")


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    
    if not verify_password(password, user.password_hash):
        return None
    
    return user


def login_user(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)
    if not user:
        return error_response("Invalid credentials", 401)
    token = create_access_token({"sub": str(user.id)})
    return success_response({"access_token": token, "token_type": "bearer", "user": user}, "User logged in successfully")