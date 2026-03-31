import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2
from PIL import Image
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from app.ml.model import get_model
from app.ml.preprocess import preprocess
from app.ml.postprocess import postprocess
from app.utils.response import success_response, error_response

executor = ThreadPoolExecutor(max_workers=2)

def predict_wound(image_path: str):
    print("=== Testing with exact notebook code ===")
    
    # Check TensorFlow version
    print(f"TensorFlow version: {tf.__version__}")
    
    # Get the loaded model
    model = get_model()
    print(f"Image Type: {type(image_path)}")
    
    # Load and preprocess image (same path as notebook)
    print(f"Loading image from: {image_path}")
    
    try:
        image = Image.open(image_path).convert("RGB")
        img = preprocess(image)
        
        print(f"✅ Image loaded and preprocessed!")
        print(f"Image shape: {img.shape}")
        print(f"Image dtype: {img.dtype}")
    except Exception as e:
        print(f"❌ Image processing failed: {e}")
        return None, None

    # Predict (same as notebook)
    print("Running prediction...")
    try:
        pred = model.predict(img)
        
        print(f"✅ Prediction successful!")
        print(f"Prediction shape: {pred.shape}")
        print(f"Prediction dtype: {pred.dtype}")
        
        # Show some stats
        print(f"Prediction min: {pred.min():.3f}")
        print(f"Prediction max: {pred.max():.3f}")
        print(f"Prediction mean: {pred.mean():.3f}")
        
        # Postprocess to get mask
        mask = postprocess(pred)
        
        # Calculate area
        area = float(np.sum(mask))
        
        # Calculate additional stats
        non_zero_pixels = int(np.sum(mask > 0))
        total_pixels = mask.size
        coverage_percentage = (non_zero_pixels / total_pixels) * 100
        
        response = {
            "area": area,
            "shape": list(mask.shape),
            "stats": {
                "wound_pixels": non_zero_pixels,
                "total_pixels": total_pixels,
                "coverage_percentage": round(coverage_percentage, 2),
                "prediction_min": float(pred.min()),
                "prediction_max": float(pred.max()),
                "prediction_mean": float(pred.mean())
            },
            "mask_preview": {
                "sample": mask[::50, ::50].tolist(),  # Sample every 50th pixel for preview
                "sample_shape": [mask[::50, ::50].shape[0], mask[::50, ::50].shape[1]]
            }
        }
        return success_response(data=response, message="Prediction successful")
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        import traceback
        traceback.print_exc()
        return error_response(message="Prediction failed", status_code=500)