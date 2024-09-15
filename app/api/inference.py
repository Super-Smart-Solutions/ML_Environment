from fastapi import APIRouter, HTTPException
from app.schemas.request import InferenceRequest
from app.services.model_inference import run_inference_service

router = APIRouter()

@router.post("/predict")
async def run_inference(request: InferenceRequest):
    try:
        result = await run_inference_service(request.model_name, request.presigned_url)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/reload_model/{model_name}")
async def reload_model(model_name: str):
    try:
        result = await run_inference_service.reload_model(model_name)
        return {"message": f"Model {model_name} reloaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
