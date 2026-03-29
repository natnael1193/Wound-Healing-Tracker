from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.wound import WoundCreate
from app.services.wound_service import create_wound, get_user_wounds
from app.core.dependencies import get_current_user
from app.db.dependency import get_db
from app.utils.response import success_response
from uuid import UUID

router = APIRouter(prefix="/wounds", tags=["Wounds"])


@router.post("/")
def create_new_wound(
    data: WoundCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    wound = create_wound(
        db=db,
        user_id=UUID(current_user['id']),
        location=data.location,
        description=data.description
    )

    return success_response(wound, "Wound created successfully")


@router.get("/")
def list_wounds(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    # return current_user['id']
    wounds = get_user_wounds(db, current_user['id'])
    return success_response(wounds, "Wounds fetched successfully")