from uuid import UUID
from sqlalchemy.orm import Session
from app.db.models.record import WoundRecord

def create_record(db: Session, wound_id, image_url, mask_url, overlay_url, area):
    record = WoundRecord(
        wound_id=wound_id,
        image_url=image_url,
        mask_url=mask_url,
        overlay_url=overlay_url,
        area=area
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


def get_records_list(db: Session, wound_id):
    records = db.query(WoundRecord).filter(WoundRecord.wound_id == UUID(wound_id)).order_by(WoundRecord.created_at.desc()).all()
    
    return records

