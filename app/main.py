import tensorflow as tf
from tensorflow import keras
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import boto3
from PIL import Image
import os
import io
import tempfile
from tensorflow import keras
from app.utils.s3_utils import download_image_from_s3
from app.utils.image_utils import preprocess_image

app = FastAPI()

# Initialize the S3 client
s3_client = boto3.client(
    's3',
    region_name='eu-central-1',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# Dictionary to store loaded models
model_cache = {}

class InferenceRequest(BaseModel):
    model_name: str
    presigned_url: str

def load_model_from_s3(bucket_name, model_key):
    """
    Load a .h5 model file from S3 into memory using a temporary file.
    """
    try:
        print(f"Loading model from S3: {bucket_name}/{model_key}")
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.h5') as temp_file:
            temp_filepath = temp_file.name
        
        # Download the file from S3 to the temporary file
        s3_client.download_file(bucket_name, model_key, temp_filepath)
        
        print(f"Model downloaded to temporary file: {temp_filepath}")
        
        # Load the model from the temporary file
        model = keras.models.load_model(temp_filepath, compile=False)
        
        # Delete the temporary file
        os.unlink(temp_filepath)
        print(f"Temporary file deleted")
        
        print(f"Model loaded successfully")
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        if 'temp_filepath' in locals() and os.path.exists(temp_filepath):
            os.unlink(temp_filepath)
            print(f"Temporary file deleted due to error")
        raise HTTPException(status_code=500, detail=f"Failed to load model from S3: {str(e)}")

def get_model(model_name, bucket_name):
    """
    Get the model from cache or load it from S3 if not cached.
    """
    if model_name not in model_cache:
        model_s3_key = f"{model_name}/best_model_weights.h5"
        model_cache[model_name] = load_model_from_s3(bucket_name, model_s3_key)
    return model_cache[model_name]


def preprocess_image(image: Image.Image) -> np.ndarray:
    """
    Preprocess the image for model input.
    
    :param image: Input image as a PIL.Image.Image object.
    :return: Preprocessed image as a NumPy array.
    """
    # Convert PIL Image to NumPy array
    image = np.array(image)
    
    # Resize the image to (256, 256) if it's not already that size
    if image.shape[:2] != (256, 256):
        image = tf.image.resize(image, (256, 256))
    
    # Ensure the image has 3 channels
    if image.shape[-1] != 3:
        image = tf.image.grayscale_to_rgb(image)
    
    # Normalize the image
    image = image / 255.0
    
    # Ensure the output is a numpy array with shape (256, 256, 3)
    return np.array(image, dtype=np.float32)


@app.post("/predict")
async def run_inference(request: InferenceRequest):
    try:
        s3_bucket_name = 'ml-model-weights-sss'
        
        # Get or load the model
        model = get_model(request.model_name, s3_bucket_name)
        
        # Download and preprocess the image from the presigned URL
        image = download_image_from_s3(request.presigned_url)
        preprocessed_image = preprocess_image(image)
        
        # Ensure the image has the correct shape
        # Remove any extra dimensions and ensure it's (256, 256, 3)
        if preprocessed_image.ndim == 4:
            preprocessed_image = preprocessed_image[0]  # Remove batch dimension if present
        elif preprocessed_image.ndim > 4:
            raise ValueError(f"Unexpected input shape: {preprocessed_image.shape}")
        
        # Add batch dimension
        preprocessed_image = np.expand_dims(preprocessed_image, axis=0)
        
        print(f"Input shape: {preprocessed_image.shape}")  # Debug print
        
        # Run prediction
        predictions = model.predict(preprocessed_image)
        predicted_class = np.argmax(predictions, axis=1)[0]
        
        return {"predicted_class": int(predicted_class), "predictions": predictions.tolist()}
    except Exception as e:
        print(f"Error in run_inference: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/reload_model/{model_name}")
async def reload_model(model_name: str):
    try:
        s3_bucket_name = 'ml-model-weights-sss'
        model_s3_key = f"{model_name}/best_model_weights.h5"
        model_cache[model_name] = load_model_from_s3(s3_bucket_name, model_s3_key)
        return {"message": f"Model {model_name} reloaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))