from fastapi import APIRouter, HTTPException
from app.schemas.inference_scheme import InferenceRequest, InferenceResponse
from app.services.model_inference import run_inference_service
from app.utils.custom_exceptions import ModelNotFoundError, ImageProcessingError

router = APIRouter()

@router.post("/predict", response_model=InferenceResponse)
async def run_inference(request: InferenceRequest):
    try:
        result = await run_inference_service(request.model_name.lower(), request.presigned_url)
        if not result:
            raise HTTPException(status_code=500, detail="inference failed.")        
        return result
    except ModelNotFoundError as e:
        raise HTTPException(status_code=503, detail=f"Model not available, try to reload. details {str(e)}")
    except ImageProcessingError as e:
        raise HTTPException(status_code=422, detail=str(e))
    else:
        raise HTTPException(status_code=500)



