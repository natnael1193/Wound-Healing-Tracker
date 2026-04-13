def validate_area(area):
    if area is None:
        return None
    if area < 50:  # threshold
        return None
    return area


def calculate_healing(baseline, current):
    if baseline is None or current is None:
        return None

    if baseline == 0:
        return None

    healing = ((baseline - current) / baseline) * 100

    return max(0, min(100, healing))