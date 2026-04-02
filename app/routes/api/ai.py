from fastapi import APIRouter, File, UploadFile, Depends
from app.services.ai_service import predict_wound
from app.utils.storage import save_file
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/predict")
def predict(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    # img_path = "./uploads/image_472ceef6895947869031256d98e98329.png"
    img_path = save_file(file)
    return predict_wound(img_path)