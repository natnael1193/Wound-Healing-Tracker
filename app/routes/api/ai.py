from fastapi import APIRouter, File, UploadFile, Depends
from app.services.ai_service import predict_wound_from_path
from app.utils.storage import save_file
from app.core.dependencies import get_current_user
from app.utils.response import success_response

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/predict")
async def predict(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    # img_path = "./uploads/image_472ceef6895947869031256d98e98329.png"
    img_path = save_file(file)
    return success_response(await predict_wound_from_path(img_path), "Wound prediction successful")