# app/ml_models_utils/ml_model_loaders.py

import os
import tempfile
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, LayerNormalization, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import backend as K
import boto3

class ModelManager:
    def __init__(self, model_paths, use_s3=False, s3_bucket=None):
        """
        Initialize ModelManager to handle loading models locally or from S3.

        Args:
            model_paths (dict): A dictionary of plant names and their corresponding model paths.
            use_s3 (bool): Set to True if models are stored in S3.
            s3_bucket (str): The name of the S3 bucket (if using S3).
        """
        self.model_paths = model_paths
        self.models = {}
        self.use_s3 = use_s3
        self.s3_bucket = s3_bucket
        if use_s3:
            self.s3_client = boto3.client('s3')

    def load_all_models(self):
        """
        Load all models defined in the model_paths dictionary.
        """
        for plant_name in self.model_paths:
            self.load_model(plant_name)

    def load_model(self, plant_name: str):
        """
        Load a specific model based on plant name, either locally or from S3.

        Args:
            plant_name (str): The name of the plant (e.g., 'Mango', 'Guava').
        
        Returns:
            Model: The loaded Keras model.
        """
        if plant_name in self.models:
            return self.models[plant_name]
        
        if plant_name not in self.model_paths:
            raise ValueError(f"Model for plant '{plant_name}' not found.")

        model_path = self.model_paths[plant_name]

        if self.use_s3:
            model = self.load_model_from_s3(plant_name, model_path)
        else:
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"The model file at {model_path} was not found.")
            model = self.build_and_load_model(plant_name, model_path)

        self.models[plant_name] = model
        return model

    def load_model_from_s3(self, plant_name, model_key):
        """
        Load a model file from S3 and build the model.

        Args:
            plant_name (str): The name of the plant.
            model_key (str): The S3 key for the model file.
        
        Returns:
            Model: The loaded Keras model.
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix='.h5') as temp_file:
            temp_filepath = temp_file.name
        
        self.s3_client.download_file(self.s3_bucket, model_key, temp_filepath)
        
        model = self.build_and_load_model(plant_name, temp_filepath)
        
        os.unlink(temp_filepath)
        
        return model

    def build_and_load_model(self, plant_name, model_path):
        """
        Build and load the model architecture, compile it, and load its weights.

        Args:
            plant_name (str): The name of the plant (used for determining class count).
            model_path (str): The file path to the model weights.
        
        Returns:
            Model: The compiled Keras model with loaded weights.
        """
        cls_no = self.get_class_number(plant_name)
        image_size = (256, 256)
        base_model = InceptionV3(include_top=False, weights='imagenet', input_shape=(*image_size, 3))

        # Build the custom classification layers on top of InceptionV3
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(512, activation='relu')(x)
        x = LayerNormalization()(x)
        x = Dropout(0.3)(x)
        x = Dense(256, activation='relu')(x)
        x = LayerNormalization()(x)
        x = Dense(256, activation='relu')(x)
        x = LayerNormalization()(x)
        x = Dropout(0.3)(x)

        if plant_name in ['Lemon', 'Pomegranate']:
            predictions = Dense(cls_no, activation='sigmoid')(x)
            loss_function = 'binary_crossentropy'
        else:
            predictions = Dense(cls_no, activation='softmax')(x)
            loss_function = 'categorical_crossentropy'

        model = Model(inputs=base_model.input, outputs=predictions)

        # Compile the model with custom metrics
        model.compile(
            optimizer=Adam(learning_rate=0.0001),
            loss=loss_function,
            metrics=['accuracy', self.f1_m, self.precision_m, self.recall_m]
        )

        model.load_weights(model_path)
        return model

    @staticmethod
    def get_class_number(plant_name):
        """
        Get the number of output classes for the given plant name.
        
        Args:
            plant_name (str): The name of the plant.
        
        Returns:
            int: The number of classes for the plant.
        """
        if plant_name == 'Mango':
            return 8
        elif plant_name == 'Guava':
            return 5
        elif plant_name == 'Grape':
            return 3
        else:
            return 2

    @staticmethod
    def recall_m(y_true, y_pred):
        """
        Custom recall metric.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

    @staticmethod
    def precision_m(y_true, y_pred):
        """
        Custom precision metric.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision

    @staticmethod
    def f1_m(y_true, y_pred):
        """
        Custom F1-score metric.
        """
        precision = ModelManager.precision_m(y_true, y_pred)
        recall = ModelManager.recall_m(y_true, y_pred)
        return 2 * ((precision * recall) / (precision + recall + K.epsilon()))
