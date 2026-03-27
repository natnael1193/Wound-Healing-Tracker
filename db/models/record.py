import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..base import Base

class WoundRecord(Base):
    __tablename__ = "wound_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    wound_id = Column(UUID(as_uuid=True), ForeignKey("wounds.id"), nullable=False)
    
    image_url = Column(String, nullable=False)
    mask_url = Column(String, nullable=True)      
    area = Column(Float, nullable=True)           
    healing_score = Column(Float, nullable=True)  
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    wound = relationship("Wound", back_populates="records")