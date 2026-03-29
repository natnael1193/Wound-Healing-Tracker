import numpy as np
from PIL import Image
import cv2

def preprocess(image: Image.Image):
    # Convert PIL to numpy array first for better performance
    img_array = np.array(image)
    
    # Use OpenCV for faster resizing
    resized = cv2.resize(img_array, (256, 256), interpolation=cv2.INTER_LINEAR)
    
    # Normalize in-place for better memory efficiency
    normalized = resized.astype(np.float32) / 255.0

    # shape: (H, W, C) → (1, H, W, C)
    image = np.expand_dims(normalized, axis=0)

    return image