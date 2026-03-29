from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class WoundCreate(BaseModel):
    location: Optional[str] = None
    description: Optional[str] = None


class WoundResponse(BaseModel):
    id: UUID
    location: Optional[str]
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True