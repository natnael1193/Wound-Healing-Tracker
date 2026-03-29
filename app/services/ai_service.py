from PIL import Image
import numpy as np
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from app.ml.model import get_model
from app.ml.preprocess import preprocess
from app.ml.postprocess import postprocess

executor = ThreadPoolExecutor(max_workers=2)

def predict_wound_sync(image_path: str):
    """Synchronous prediction function for thread pool"""
    start_time = time.time()
    
    # Model loading
    model_start = time.time()
    model = get_model()
    if model is None:
        raise Exception("Model not available")
    model_time = time.time() - model_start
    
    # Image loading
    image_start = time.time()
    image = Image.open(image_path).convert("RGB")
    image_time = time.time() - image_start
    
    # Preprocessing
    preprocess_start = time.time()
    input_data = preprocess(image)
    preprocess_time = time.time() - preprocess_start
    
    # Prediction
    prediction_start = time.time()
    prediction = model.predict(input_data)
    prediction_time = time.time() - prediction_start
    
    # Postprocessing
    postprocess_start = time.time()
    mask = postprocess(prediction)
    postprocess_time = time.time() - postprocess_start
    
    # Area calculation
    area_start = time.time()
    area = float(np.sum(mask))
    area_time = time.time() - area_start
    
    total_time = time.time() - start_time
    
    print(f"Performance breakdown - Total: {total_time:.3f}s, Model: {model_time:.3f}s, "
          f"Image: {image_time:.3f}s, Preprocess: {preprocess_time:.3f}s, "
          f"Prediction: {prediction_time:.3f}s, Postprocess: {postprocess_time:.3f}s, "
          f"Area: {area_time:.3f}s")
    
    return mask, area

async def predict_wound(image_path: str):
    """Async prediction with thread pool execution"""
    loop = asyncio.get_event_loop()
    mask, area = await loop.run_in_executor(executor, predict_wound_sync, image_path)
    return mask, area