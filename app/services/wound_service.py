from sqlalchemy.orm import Session
from app.db.models.wound import Wound
from uuid import UUID

def create_wound(db: Session, user_id, location=None, description=None):
    wound = Wound(
        user_id=user_id,
        location=location,
        description=description
    )

    db.add(wound)
    db.commit()
    db.refresh(wound)

    return wound


def get_user_wounds(db: Session, user_id: str):
    # return user_id
    return db.query(Wound).filter(Wound.user_id == UUID(user_id)).all()


def get_user_wound(db: Session, user_id: str, wound_id: str):
    return db.query(Wound).filter(Wound.user_id == UUID(user_id)).filter(Wound.id == UUID(wound_id)).first()

