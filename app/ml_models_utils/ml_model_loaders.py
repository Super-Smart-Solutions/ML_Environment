import os
import boto3
import tensorflow as tf
from tensorflow import keras
from app.core.config import settings  # Import settings for AWS credentials
from fastapi import HTTPException

class ModelManager:
    def __init__(self):
        # Set the model directory to the specified path
        self.model_cache = {}
        self.model_directory = r'C:\Users\ahmed\sss_models'  # Use raw string for Windows path

        # Create the model directory if it doesn't exist
        os.makedirs(self.model_directory, exist_ok=True)

    def load_model(self, model_name: str):
        """
        Load a model from cache if it exists; otherwise, download from S3 and load into cache.
        """
        if model_name in self.model_cache:
            return self.model_cache[model_name]

        # Define the path for the model file
        model_file_path = os.path.join(self.model_directory, f"{model_name}_best_model_weights.h5")

        # Check if model file exists locally
        if os.path.exists(model_file_path):
            print(f"Loading model from local file: {model_file_path}")
            model = keras.models.load_model(model_file_path, compile=False)
        else:
            model_s3_key = f"{model_name}/best_model_weights.h5"
            model = self._load_model_from_s3(settings.AWS_BUCKET_NAME, model_s3_key, model_file_path)

        # Cache the model after loading
        self.model_cache[model_name] = model
        return model

    def _load_model_from_s3(self, bucket_name: str, model_key: str, local_file_path: str):
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

            # Download the model file from S3
            s3_client.download_file(bucket_name, model_key, local_file_path)
            print(f"Model downloaded to: {local_file_path}")

            # Load the model from the downloaded file
            model = keras.models.load_model(local_file_path, compile=False)
            return model
        except Exception as e:
            print(f"Error loading model from S3: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to load model from S3: {str(e)}")
