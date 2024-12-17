import os
import aioboto3
from app.core.config import settings
from fastapi import HTTPException
from functools import lru_cache
from app.utils.s3_utils import s3_download_object_decorator
import asyncio

import numpy as np
from tensorflow.keras.models import load_model
import threading
from app.utils.custom_exceptions import ModelLoadingError


class ModelManager:
    def __init__(self):
        self.model_directory = settings.WEIGHTS_DIR
        self.loaded_models ={}
        self.class_dict = {}
        self.model_locks = {}

    @lru_cache(maxsize=10)
    def load_model(self, model_name: str):
        """
        Load a model from weight file, and saves it to cache.
        """

        # Define the path for the model file
        model_file_path = os.path.join(self.model_directory,"models",f"{model_name.lower()}", f"{model_name.lower()}_model.h5")

        # Check if model file exists locally
        if os.path.exists(model_file_path):
            #print(f"Loading model from local file: {model_file_path}")
            lock = self.model_locks.setdefault(model_name, threading.Lock())
            with lock:
                try:
                    model = load_model(model_file_path)
                except Exception as e:
                    raise e
                if not model:
                    raise ModelLoadingError(f"Model {model_name} failed to load")
                self.loaded_models[model_name] = model
        else:
            #print(f"File not found: {model_file_path}")
            raise FileNotFoundError(f"Model {model_name} not found at {model_file_path}")


    
    async def _load_model_from_s3(self, model_name: str):
        """
        Download the model file from S3 and load it into memory.
        """
        print(f"Loading model from S3: {settings.AWS_WEIGHTS_BUCKET_NAME}/{model_name}")

        @s3_download_object_decorator(
        bucket_name=settings.AWS_WEIGHTS_BUCKET_NAME,
        file_path=settings.WEIGHTS_DIR
        )
        async def _get_model(downloaded_file_path, object_key: str=""):
            return True if os.path.exists(downloaded_file_path) else False


        model_key = f"models/{model_name.lower()}/{model_name.lower()}_model.h5"
        result = await _get_model(object_key=model_key)

        if result:
            # Load the model from the downloaded file
            self.load_model(model_name.lower())
        else:
            raise Exception(f"Failed to retrive model {model_name}, from bucket {settings.AWS_WEIGHTS_BUCKET_NAME}.")