from fastapi import APIRouter, HTTPException
from app.utils.model_utils import model_manager
from app.utils.custom_exceptions import ModelLoadingError
from app.schemas.models_scheme import ModelReloadRequest


router = APIRouter()

@router.post("/reload", status_code=200)
async def reload_model(request: ModelReloadRequest):
    #check if model_name is correct
    if not (request.model_name in model_manager.class_dict.keys()):
        raise HTTPException(status_code=503, detail=f"Model name is not found in class list.")

    try:
        result = await model_manager._load_model_from_s3(request.model_name)
        return(f"Model {request.model_name} loaded successfully")
    except ModelLoadingError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))