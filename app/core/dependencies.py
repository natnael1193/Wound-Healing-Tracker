from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.security import SECRET_KEY, ALGORITHM
from app.db.dependency import get_db
from app.db.models.user import User
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),  
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    # return user_id
    user = db.query(User).filter(User.id == user_id).first()
    user = {
        "name": user.name,
        "email": user.email,
        "id": str(user.id),  # Convert UUID to string
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

