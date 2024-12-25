from app.utils.s3_utils import download_image_from_s3
from app.utils.image_utils import preprocess_image
# from app.ml_models_utils.model_manager import ModelManager
from app.schemas.inference_scheme import InferenceResponse
import numpy as np
from app.utils.custom_exceptions import ModelNotFoundError, ImageProcessingError
from app.utils.model_utils import model_manager, get_disease_name
# Instantiate ModelManager
# model_manager = ModelManager()
import gc

from typing import List

async def run_inference_service(model_name: str, presigned_url: str) -> InferenceResponse:
    # Load model from cache or S3
    model = model_manager.loaded_models.get(model_name, None)
    if not model:
        raise ModelNotFoundError(f"Model {model_name} is not loaded.")

    # Download and preprocess the image from S3
    try:
        image = download_image_from_s3(presigned_url)
        preprocessed_image = preprocess_image(image)
    except Exception as e:
        raise ImageProcessingError(f"Image Processing error {str(e)}")

    lock = model_manager.model_locks.get(model_name)
    if not lock:
        raise ModelNotFoundError(f"Model {model_name} lock not found.")
    with lock:
        # Run inference
        predictions = model.predict(preprocessed_image)
    
    print("predictions: ", predictions)

    # Check if predictions is already a flat list of floats
    if isinstance(predictions, np.ndarray):
        # Convert to a flat list of floats
        prediction_list = predictions.flatten().tolist()
    elif isinstance(predictions, list):
        # If predictions is a nested list, flatten it
        prediction_list = [float(item) for sublist in predictions for item in sublist]
    else:
        raise ValueError("Predictions should be a numpy array or a list of floats")


    if len(prediction_list) == 1:
        predicted_class_index = 1 if prediction_list[0] >= 0.5 else 0
        if prediction_list:
            confidence = prediction_list[0]
        else:
            confidence = 1.0 - float(prediction_list[0])
        is_healthy = False
    else:
        predicted_class_index = np.argmax(prediction_list)
        confidence = prediction_list[predicted_class_index]
        is_healthy = True if confidence < 0.6 else False
        

    
    # print("predictions list: ", prediction_list)
    # print("predictions index: ", predicted_class_index)
    # print("confidence", confidence, type(confidence))


    try:
        if not is_healthy:
            disease_name = get_disease_name(model_name, predicted_class_index)
        else:
            disease_name = "healthy"
    except Exception as e:
        raise e

    # print("class: ", disease_name, type(disease_name) )

    #Free Memory (SAFETY!)
    del image
    del preprocessed_image
    gc.collect()
    # Return an InferenceResponse object
    return InferenceResponse(predicted_class=disease_name, confidence=str(confidence))
