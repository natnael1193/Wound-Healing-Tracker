from sqlalchemy.orm import Session
from app.db.models.record import WoundRecord

def create_record(db: Session, wound_id, image_url, mask_url, area):
    record = WoundRecord(
        wound_id=wound_id,
        image_url=image_url,
        mask_url=mask_url,
        area=area
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record