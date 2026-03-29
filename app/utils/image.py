import cv2
import numpy as np
from uuid import uuid4
import os

MASK_DIR = "masks"
os.makedirs(MASK_DIR, exist_ok=True)

def save_mask(mask):
    filename = f"mask_{uuid4().hex}.png"
    path = os.path.join(MASK_DIR, filename)

    mask_img = (mask * 255).astype(np.uint8)
    cv2.imwrite(path, mask_img)

    return path