from sqlalchemy.orm import Session
from app.db.models.user import User
from passlib.context import CryptContext
from jose import jwt
from app.db.models.user import User
from app.core.security import verify_password, create_access_token

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

    return user


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
        return None

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": user}