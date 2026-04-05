from app.db.models.record import WoundRecord

def get_wound_progress(db, wound_id):
    records = (
        db.query(WoundRecord)
        .filter(WoundRecord.wound_id == wound_id)
        .order_by(WoundRecord.created_at)
        .all()
    )

    timeline = []

    valid_records = [r for r in records if r.area and r.area > 0]

    if not valid_records:
        return []

    first_area = valid_records[0].area

    for r in valid_records:
        healing = ((first_area - r.area) / first_area) * 100

        timeline.append({
            "date": r.created_at,
            "area": r.area,
            "healing_percent": round(healing, 2)
        })

    return timeline


 
    