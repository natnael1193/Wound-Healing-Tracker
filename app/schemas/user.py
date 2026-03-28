from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str    


class UserUpdateRequest(BaseModel):
    name: str
    # email: EmailStr

# Add a simple user model for responses that excludes sensitive data
class UserMe(BaseModel):
    id: str  # Convert UUID to string for JSON serialization
    email: EmailStr
    name: str
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_user(cls, user):
        return cls(
            id=str(user.id),  # Convert UUID to string
            email=user.email,
            name=user.name,
            created_at=user.created_at,
            updated_at=user.updated_at
        )