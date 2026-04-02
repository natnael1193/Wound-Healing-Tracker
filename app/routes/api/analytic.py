from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.db.dependency import get_db
from app.services.analytics_service import get_wound_progress
from app.utils.response import success_response

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/wounds/{wound_id}/progress")
def wound_progress(
    wound_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    timeline = get_wound_progress(db, wound_id)

    if not timeline:
        raise HTTPException(status_code=404, detail="No records found")

    return success_response(timeline, "Healing progress fetched")