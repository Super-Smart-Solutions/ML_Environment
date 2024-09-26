import os
import aioboto3
from tensorflow import keras
from app.core.config import settings  # Import settings for AWS credentials
from fastapi import HTTPException
from functools import lru_cache
from app.utils.s3_utils import s3_download_object_decorator


class ModelManager:
    def __init__(self):
        self.model_directory = settings.WEIGHTS_DIR


    @lru_cache(maxsize=10)
    def load_model(self, model_name: str):
        """
        Load a model from weight file, and saves it to cache.
        """

        # Define the path for the model file
        model_file_path = os.path.join(self.model_directory,"{model_name}", f"{model_name}_model.keras")

        # Check if model file exists locally
        if os.path.exists(model_file_path):
            print(f"Loading model from local file: {model_file_path}")
            return keras.models.load_model(model_file_path, compile=False)
        else:
            print(f"File not found: {model_file_path}")
            raise FileNotFoundError(f"Model {model_name} not found at {model_file_path}")



    
    async def _load_model_from_s3(self, bucket_name: str, model_name: str):
        """
        Download the model file from S3 and load it into memory.
        """
        try:
            print(f"Loading model from S3: {bucket_name}/{model_name}")

            # Initialize S3 client using aioboto3
            async with aioboto3.client(
                's3',
                region_name=settings.AWS_DEFAULT_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            ) as s3_client:

                model_key = f"{model_name}/{model_name}_model.keras"
                file_path = os.path.join(self.model_directory, model_key)

                # Create the directory for the weights
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                # Download the model file from S3
                await s3_client.download_file(bucket_name, model_key, file_path)
                print(f"Model downloaded to: {file_path}")

                # Load the model from the downloaded file
                # model = keras.models.load_model(file_path, compile=False)
                return self.load_model(model_name)

        except Exception as e:
            print(f"Error loading model from S3: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to load model from S3: {str(e)}")

