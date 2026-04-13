#!/usr/bin/env python3

# Exact same code as working notebook
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image

def preprocess(image):
    # Convert PIL to numpy array first for better performance
    img_array = np.array(image)
    
    # Use OpenCV for faster resizing
    resized = cv2.resize(img_array, (256, 256), interpolation=cv2.INTER_LINEAR)
    
    # Normalize in-place for better memory efficiency
    normalized = resized.astype(np.float32) / 255.0

    # shape: (H, W, C) → (1, H, W, C)
    image = np.expand_dims(normalized, axis=0)

    return image

def main():
    print("=== Testing with exact notebook code ===")
    
    # Check TensorFlow version
    print(f"TensorFlow version: {tf.__version__}")
    
    # Load model (same path as notebook)
    MODEL_PATH = "./ml/weights/wound_unet_model.h5"
    print(f"Loading model from: {MODEL_PATH}")
    
    try:
        model = keras.models.load_model(MODEL_PATH, compile=False)
        print("✅ Model loaded successfully!")
        print(f"Model input shape: {model.input_shape}")
        print(f"Model output shape: {model.output_shape}")
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return

    # Load and preprocess the image (same path as notebook)
    img_path = "./uploads/image_472ceef6895947869031256d98e98329.png"
    print(f"Loading image from: {img_path}")
    
    try:
        image = Image.open(img_path).convert("RGB")
        img = preprocess(image)
        
        print(f"✅ Image loaded and preprocessed!")
        print(f"Image shape: {img.shape}")
        print(f"Image dtype: {img.dtype}")
    except Exception as e:
        print(f"❌ Image processing failed: {e}")
        return

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
        
        # Save prediction visualization
        plt.figure(figsize=(10, 5))
        
        plt.subplot(1, 2, 1)
        plt.imshow(image, cmap='gray')
        plt.title("Original Image")
        
        plt.subplot(1, 2, 2)
        plt.imshow(pred[0], cmap='gray')
        plt.title("Wound Prediction")
        
        plt.tight_layout()
        plt.savefig('./prediction_result.png', dpi=150, bbox_inches='tight')
        print("✅ Result saved to prediction_result.png")
        
        # Show plot
        plt.show()
        
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
