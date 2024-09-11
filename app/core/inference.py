from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import os

from app.ml_models_utils.ml_model_loaders import ModelManager
from app.utils.s3_utils import download_image_from_s3
from app.utils.image_utils import preprocess_image
from app.schemas.request import InferenceRequest

# Create FastAPI app instance
app = FastAPI()

# Define model paths dynamically
current_path = os.getcwd()
model_paths = {
    'Grape': os.path.join(current_path, 'app', 'ml_models', 'ml_model_weights', 'Grape', 'best_model_weights.h5'),
    'Guava': os.path.join(current_path, 'app', 'ml_models', 'ml_model_weights', 'Guava', 'best_model_weights.h5'),
    'Lemon': os.path.join(current_path, 'app', 'ml_models', 'ml_model_weights', 'Lemon', 'best_model_weights.h5'),
    'Mango': os.path.join(current_path, 'app', 'ml_models', 'ml_model_weights', 'Mango', 'best_model_weights.h5'),
    'Pomegranate': os.path.join(current_path, 'app', 'ml_models', 'ml_model_weights', 'Pomegranate', 'best_model_weights.h5')
}

# Initialize the model manager
model_manager = ModelManager(model_paths)

@app.post("/predict")
async def run_inference(request: InferenceRequest):
    """
    Run inference on an image from an S3 presigned URL using a specified model.
    
    :param request: InferenceRequest object containing model_name and presigned_url.
    :return: Inference result.
    """
    try:
        # Download and preprocess the image
        image = download_image_from_s3(request.presigned_url)
        preprocessed_image = preprocess_image(image)

        # Load the appropriate model
        model = model_manager.load_model(request.model_name)

        # Run prediction
        predictions = model.predict(preprocessed_image)
        predicted_class = np.argmax(predictions, axis=1)[0]
        
        return {"predicted_class": int(predicted_class), "predictions": predictions.tolist()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
