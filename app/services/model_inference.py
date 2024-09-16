from app.utils.s3_utils import download_image_from_s3
from app.utils.image_utils import preprocess_image
from app.ml_models_utils.ml_model_loaders import ModelManager
from app.schemas.response import InferenceResponse
import numpy as np

# Instantiate ModelManager
model_manager = ModelManager()

from typing import List

async def run_inference_service(model_name: str, presigned_url: str) -> InferenceResponse:
    # Load model from cache or S3
    model = model_manager.load_model(model_name)

    # Download and preprocess the image from S3
    image = download_image_from_s3(presigned_url)
    preprocessed_image = preprocess_image(image)

    # Run inference
    predictions = model.predict(preprocessed_image)
    predicted_class = np.argmax(predictions, axis=1)[0]

    # Check if predictions is already a flat list of floats
    if isinstance(predictions, np.ndarray):
        # Convert to a flat list of floats
        prediction_list = predictions.flatten().tolist()
    elif isinstance(predictions, list):
        # If predictions is a nested list, flatten it
        prediction_list = [float(item) for sublist in predictions for item in sublist]
    else:
        raise ValueError("Predictions should be a numpy array or a list of floats")

    # Return an InferenceResponse object
    return InferenceResponse(predicted_class=predicted_class, predictions=prediction_list)
