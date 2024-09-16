import os
import tempfile
import boto3
import tensorflow as tf
from tensorflow import keras
from app.core.config import settings  # Import settings for AWS credentials
from fastapi import HTTPException



class ModelManager:
    def __init__(self):
        self.model_cache = {}

    def load_model(self, model_name: str):
        """
        Load a model from cache if it exists; otherwise, download from S3 and load into cache.
        """
        if model_name in self.model_cache:
            return self.model_cache[model_name]
        
        model_s3_key = f"{model_name}/best_model_weights.h5"
        model = self._load_model_from_s3(settings.AWS_BUCKET_NAME, model_s3_key)
        
        # Cache the model after loading
        self.model_cache[model_name] = model
        return model

    def _load_model_from_s3(self, bucket_name: str, model_key: str):
        """
        Download the model file from S3 and load it into memory.
        """
        try:
            print(f"Loading model from S3: {bucket_name}/{model_key}")

            # Initialize S3 client using credentials from settings
            s3_client = boto3.client(
                's3',
                region_name=settings.AWS_DEFAULT_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )

            # Create a temporary file to store the downloaded model
            with tempfile.NamedTemporaryFile(delete=False, suffix='.h5') as temp_file:
                temp_filepath = temp_file.name

            # Download the model file from S3
            s3_client.download_file(bucket_name, model_key, temp_filepath)
            print(f"Model downloaded to temporary file: {temp_filepath}")

            # Load the model from the temporary file
            model = keras.models.load_model(temp_filepath, compile=False)

            # Delete the temporary file after loading the model
            os.unlink(temp_filepath)
            print("Temporary file deleted after loading model.")
            
            return model
        except Exception as e:
            print(f"Error loading model from S3: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to load model from S3: {str(e)}")


