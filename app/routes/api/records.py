import uuid
import os
import shutil
from uuid import UUID
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.services.wound_service import get_user_wound
from app.services.ml_pipeline import process_wound_area
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.db.dependency import get_db
from app.utils.response import success_response
from app.utils.storage import save_file
from app.utils.image import save_mask, create_overlay
from app.services.ai_service import predict_wound
from app.services.record_service import create_record, get_records_list
from app.services.ml_pipeline import process_wound_area
from app.db.models.wound import Wound
from app.db.models.record import WoundRecord

router = APIRouter(prefix="/records", tags=["Records"])


@router.post("/wounds/{wound_id}")
async def upload_record(
    wound_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Save image
    filename = f"{uuid.uuid4()}.png"
    image_path = f"media/{filename}"

    os.makedirs("media", exist_ok=True)

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run ML model
    mask, raw_area = await predict_wound(image_path)

    # Save mask (optional)
    mask_path = f"media/mask_{filename}"
    overlay_path = f"media/overlay_{filename}"

    # assume you already have these utils
    from app.utils.image import save_mask, create_overlay

    mask_path = save_mask(mask)
    overlay_path = create_overlay(image_path, mask)

    # Process area
    area, healing = process_wound_area(
        db=db,
        wound_id=wound_id,
        raw_area=raw_area
    )

    # Save record
    record = WoundRecord(
        wound_id=wound_id,
        image_url=image_path,
        mask_url=mask_path,
        overlay_url=overlay_path,
        area=area,
        healing_score=healing,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "data": {
            "id": str(record.id),
            "area": record.area,
            "healing_score": record.healing_score,
            "overlay_url": record.overlay_url,
        }
    }



@router.get("/wounds/{wound_id}")
def get_records(
    wound_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Check wound belongs to user
    wound = get_user_wound(db, current_user['id'], wound_id)
    
    if not wound:
        raise HTTPException(status_code=403, detail="Wound not found or not accessible")
    
    # Get records
    wound.records = get_records_list(db, wound_id)
    # print("get_records(db, wound_id)", get_records_list(db, wound_id))
    return success_response(wound, "Wound retrieved successfully")


@router.get("/wounds/{wound_id}/predict")
def predict_wound_endpoint(
    wound_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    raw_area: float = None
):
    smoothed_area, healing_score = process_wound_area(
        db=db,
        wound_id=wound_id,
        raw_area=raw_area
    )
    return success_response({"smoothed_area": smoothed_area, "healing_score": healing_score}, "Prediction completed successfully")