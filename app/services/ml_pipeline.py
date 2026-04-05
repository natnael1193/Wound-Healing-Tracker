from app.services.smoothing_service import smooth_area
from app.services.metrics_service import validate_area, calculate_healing
from app.db.models.record import WoundRecord

def process_wound_area(db, wound_id, raw_area):
    # get last record
    last_record = (
        db.query(WoundRecord)
        .filter(WoundRecord.wound_id == wound_id)
        .order_by(WoundRecord.created_at.desc())
        .first()
    )

    previous_area = last_record.area if last_record else None

    # validate
    valid_area = validate_area(raw_area)

    # smooth
    if valid_area is not None:
        smoothed_area = smooth_area(previous_area, valid_area)
    else:
        smoothed_area = previous_area

    # get baseline
    first_record = (
        db.query(WoundRecord)
        .filter(WoundRecord.wound_id == wound_id)
        .order_by(WoundRecord.created_at.asc())
        .first()
    )

    baseline_area = first_record.area if first_record else smoothed_area

    # calculate healing
    healing_percent = calculate_healing(baseline_area, smoothed_area)

    return smoothed_area, healing_percent



# Validate area (remove bad predictions)
def validate_area(area):
    if area is None:
        return None
    if area < 50:  # ignore noise
        return None
    return area


# Smooth area (EMA)
def smooth_area(prev, current, alpha=0.3):
    if prev is None:
        return current
    return alpha * current + (1 - alpha) * prev


# Healing %
def calculate_healing(baseline, current):
    if baseline is None or current is None:
        return None
    if baseline == 0:
        return None

    healing = ((baseline - current) / baseline) * 100
    return max(0, min(100, healing))


# MAIN FUNCTION (this is what you use)
def process_area(db, wound_id, raw_area):
    # get last record
    last = (
        db.query(WoundRecord)
        .filter(WoundRecord.wound_id == wound_id)
        .order_by(WoundRecord.created_at.desc())
        .first()
    )

    prev_area = last.area if last else None

    # 🔹 validate
    valid = validate_area(raw_area)

    # 🔹 smooth
    if valid is not None:
        smoothed = smooth_area(prev_area, valid)
    else:
        smoothed = prev_area

    # 🔹 get baseline (first record)
    first = (
        db.query(WoundRecord)
        .filter(WoundRecord.wound_id == wound_id)
        .order_by(WoundRecord.created_at.asc())
        .first()
    )

    baseline = first.area if first else smoothed

    # 🔹 healing %
    healing = calculate_healing(baseline, smoothed)

    return smoothed, healing