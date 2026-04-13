def smooth_area(previous_area, current_area, alpha=0.3):
    if previous_area is None:
        return current_area
    return alpha * current_area + (1 - alpha) * previous_area
