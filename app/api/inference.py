from fastapi import APIRouter, HTTPException
from app.schemas.request import InferenceRequest
from app.schemas.response import InferenceResponse
from app.services.model_inference import run_inference_service

router = APIRouter()

@router.post("/predict", response_model=InferenceResponse)
async def run_inference(request: InferenceRequest):
    try:
        result = await run_inference_service(request.model_name, request.presigned_url)
        if not result:
            raise HTTPException(status_code=400, detail=f"model {request.model_name} not found, try to reload.")        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/reload_models/{model_name}")
async def reload_model(model_name: str):
    pass
