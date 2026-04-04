from uuid import UUID
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.services.wound_service import get_user_wound
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.db.dependency import get_db
from app.utils.response import success_response
from app.utils.storage import save_file
from app.utils.image import save_mask, create_overlay
from app.services.ai_service import predict_wound
from app.services.record_service import create_record, get_records_list
from app.db.models.wound import Wound

router = APIRouter(prefix="/records", tags=["Records"])


@router.post("/wounds/{wound_id}")
async def upload_record(
    wound_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Check wound belongs to user
    wound = db.query(Wound).filter(Wound.id == wound_id).first()
    
    if not wound or str(wound.user_id) != current_user['id']:
        raise HTTPException(status_code=403, detail="Not allowed")

    # Save image
    image_path = save_file(file)


    # Run AI
    mask, area = await predict_wound(image_path)


    # Save mask
    mask_path = save_mask(mask)

    # Create overlay
    overlay_path = create_overlay(image_path, mask)

    # Save record in DB
    record = create_record(
        db,
        wound_id=wound_id,
        image_url=image_path,
        mask_url=mask_path,
        overlay_url=overlay_path,
        area=area
    )

    return success_response(record, "Record created successfully")



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
