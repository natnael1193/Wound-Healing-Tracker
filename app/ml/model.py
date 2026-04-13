import os
import numpy as np
import tensorflow as tf
from tensorflow import keras

MODEL_PATH = os.path.join(os.path.dirname(__file__), "weights", "v1_wound_unet_model.keras")

model = None

def get_model():
    global model
    if model is None:
        # Check TensorFlow version
        print(f"TensorFlow version: {tf.__version__}")
        
        # Load model (same path as notebook)
        print(f"Loading model from: {MODEL_PATH}")
        
        try:
            model = keras.models.load_model(MODEL_PATH, compile=False)
            print("✅ Model loaded successfully!")
            print(f"Model input shape: {model.input_shape}")
            print(f"Model output shape: {model.output_shape}")
        except Exception as e:
            print(f"❌ Model loading failed: {e}")
            # Create a mock model for development
            model = MockModel()
    return model

class MockModel:
    def predict(self, input_data):
        # Return a mock prediction (same shape as input but with single channel)
        return np.random.random((1, 256, 256, 1))