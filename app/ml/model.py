import os
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "weights", "wound_unet_model.h5")

model = None

def get_model():
    global model
    if model is None:
        try:
            # Only import tensorflow when needed
            from tensorflow import keras
            import tensorflow as tf
            
            print("Configuring TensorFlow...")
            
            # Basic configuration first
            tf.config.set_soft_device_placement(True)
            
            # Try GPU optimization only if available
            gpus = tf.config.experimental.list_physical_devices('GPU')
            if gpus:
                try:
                    tf.config.experimental.set_memory_growth(gpus[0], True)
                    print("GPU memory growth enabled")
                except RuntimeError as e:
                    print(f"GPU config failed: {e}")
            
            # Load model without heavy optimizations first
            print("Loading model weights...")
            model = keras.models.load_model(MODEL_PATH, compile=False)
            
            # Simple compile for inference
            print("Compiling model for inference...")
            model.compile()
            
            print("Real model loaded successfully")
            
        except Exception as e:
            print(f"Warning: Could not load model: {e}")
            print("Using mock model for development")
            # Create a mock model for development
            model = MockModel()
    return model

def preload_model():
    """Preload the model at application startup"""
    import threading
    
    def load_model():
        try:
            print("Preloading ML model...")
            get_model()
            print("Model preloading complete")
        except Exception as e:
            print(f"Model loading failed: {e}")
            print("Using mock model")
            global model
            model = MockModel()
    
    # Run in separate thread to avoid blocking startup
    thread = threading.Thread(target=load_model)
    thread.daemon = True
    thread.start()
    print("Model preloading started in background...")

class MockModel:
    def predict(self, input_data):
        # Return a mock prediction (same shape as input but with single channel)
        return np.random.random((1, 256, 256, 1))