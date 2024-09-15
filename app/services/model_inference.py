from app.utils.s3_utils import download_image_from_s3
from app.utils.image_utils import preprocess_image
from app.ml_models_utils.ml_model_loaders import ModelManager
from app.core.config import settings
import numpy as np

model_cache = {}

async def run_inference_service(model_name: str, presigned_url: str):
    # Load model from cache or S3
    model = get_model(model_name)

    # Download and preprocess the image from S3
    image = download_image_from_s3(presigned_url)
    preprocessed_image = preprocess_image(image)

    # Run inference
    predictions = model.predict(preprocessed_image)
    predicted_class = np.argmax(predictions, axis=1)[0]

    return {"predicted_class": predicted_class, "predictions": predictions.tolist()}

def get_model(model_name: str):
    if model_name not in model_cache:
        model_s3_key = f"{model_name}/best_model_weights.h5"
        model_cache[model_name] = ModelManager().load_model(model_name)
    return model_cache[model_name]
