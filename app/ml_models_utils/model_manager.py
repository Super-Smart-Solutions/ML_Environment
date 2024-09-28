import os
import aioboto3
# import tensorflow as tf
# from tensorflow import keras
from app.core.config import settings  # Import settings for AWS credentials
from fastapi import HTTPException
from functools import lru_cache
from app.utils.s3_utils import s3_download_object_decorator
import asyncio

# import numpy as np
# import keras
# It can be used to reconstruct the model identically.
# reconstructed_model = keras.models.load_model(r"C:\Users\ahmed\sss_models\Mango_best_model_weights.keras")
# print(reconstructed_model)
# from tensorflow.keras.models import load_model
# from tensorflow.keras.optimizers import Adam
# from tensorflow.keras.metrics import Precision, Recall, AUC
# from tensorflow.keras.layers import LayerNormalization
# from tensorflow.keras import backend as K

# K.clear_session()
# # Define a dictionary of custom objects
# custom_objects = {
#     'Adam': Adam,
#     'Precision': Precision,
#     'Recall': Recall,
#     'AUC': AUC,
#     'LayerNormalization': LayerNormalization
# }
import numpy as np
# import tensorflow as tf
# from tensorflow import keras
# from keras import layers
# import keras
from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import Precision, Recall, AUC
from tensorflow.keras.layers import LayerNormalization
from tensorflow.keras import backend as K


class ModelManager:
    def __init__(self):
        self.model_directory = settings.WEIGHTS_DIR


    @lru_cache(maxsize=10)
    def load_model(self, model_name: str):
        """
        Load a model from weight file, and saves it to cache.
        """

        # Define the path for the model file
        model_file_path = os.path.join(self.model_directory,"models",f"{model_name}", f"{model_name}_model.keras")

        # Check if model file exists locally
        if os.path.exists(model_file_path):
            print(f"Loading model from local file: {model_file_path}")
            return keras.models.load_model(model_file_path)
        else:
            print(f"File not found: {model_file_path}")
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


        # model_key = f"models/{model_name}/{model_name}_model.keras"
        # result = await _get_model(object_key=model_key)
        result = True

        if result:
            # Load the model from the downloaded file
            return self.load_model(model_name)
        else:
            raise Exception(f"Failed to retrive model {model_name}, from bucket {settings.AWS_WEIGHTS_BUCKET_NAME}.")