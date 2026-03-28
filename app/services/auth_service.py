from sqlalchemy.orm import Session
from app.db.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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