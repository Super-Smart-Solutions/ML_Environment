from fastapi import APIRouter, UploadFile, File
from app.models import model_1, model_2
from app.schemas.request import InferenceRequest
from app.schemas.response import InferenceResponse

inference_router = APIRouter()

@inference_router.post("/inference", response_model=InferenceResponse)
async def run_inference(file: UploadFile = File(...), model_name: str = "model_1", params: InferenceRequest = None):
    if model_name == "model_1":
        prediction = model_1.predict(file.file, params)
    elif model_name == "model_2":
        prediction = model_2.predict(file.file, params)
    else:
        return {"error": "Model not found"}
    
    return {"prediction": prediction}
