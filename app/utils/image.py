import cv2
import numpy as np
from uuid import uuid4
import os

MASK_DIR = "masks"
os.makedirs(MASK_DIR, exist_ok=True)

OVERLAY_DIR = "overlays"
os.makedirs(OVERLAY_DIR, exist_ok=True)

def save_mask(mask):
    filename = f"mask_{uuid4().hex}.png"
    path = os.path.join(MASK_DIR, filename)

    mask_img = (mask * 255).astype(np.uint8)
    cv2.imwrite(path, mask_img)

    return path


def create_overlay(image_path, mask):
    if len(mask.shape) == 3:
        mask = mask.squeeze()

    # Load image
    image = cv2.imread(image_path)
    image = cv2.resize(image, (mask.shape[1], mask.shape[0]))

    # Create colored mask
    mask_colored = np.zeros_like(image)
    mask_colored[:, :, 2] = mask * 255  # red

    # Blend
    overlay = cv2.addWeighted(image, 0.7, mask_colored, 0.3, 0)

    # Save
    filename = f"overlay_{uuid4().hex}.png"
    path = os.path.join(OVERLAY_DIR, filename)

    cv2.imwrite(path, overlay)

    return path