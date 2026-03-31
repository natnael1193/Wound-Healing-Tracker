from fastapi import APIRouter
from app.services.ai_service import predict_wound

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/predict")
def predict():
    img_path = "./uploads/image_472ceef6895947869031256d98e98329.png"
    return predict_wound(img_path)