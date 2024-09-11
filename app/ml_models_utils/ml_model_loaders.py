from tensorflow.keras.models import Model, load_model
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, LayerNormalization, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import backend as K
import os

class ModelManager:
    def __init__(self, model_paths):
        """
        Initializes the ModelManager with a dictionary of model paths.

        :param model_paths: Dictionary with plant names as keys and model paths as values.
        """
        self.model_paths = model_paths
        self.models = {}

    def load_model(self, plant_name: str, cls_no: int = 2):
        """
        Loads and returns the model for the given plant.

        :param plant_name: The name of the plant.
        :param cls_no: Number of classes for the classification.
        :return: A compiled Keras model ready for inference.
        """
        if plant_name in self.models:
            return self.models[plant_name]
        
        if plant_name not in self.model_paths:
            raise ValueError(f"Model for plant '{plant_name}' not found.")

        model_path = self.model_paths[plant_name]

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"The model file at {model_path} was not found.")
        
        # Adjust cls_no to 8 if the plant_name is Mango
        if plant_name == 'Mango':
            cls_no = 8

        # Adjust cls_no to 5 if the plant_name is Guava
        if plant_name == 'Guava':
            cls_no = 5 

        # Adjust cls_no to 3 if the plant_name is Grape
        if plant_name == 'Grape':
            cls_no = 3         

        image_size = (256, 256)
        base_model = InceptionV3(include_top=False, weights='imagenet', input_shape=(*image_size, 3))

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

        def recall_m(y_true, y_pred):
            true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
            possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
            recall = true_positives / (possible_positives + K.epsilon())
            return recall

        def precision_m(y_true, y_pred):
            true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
            predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
            precision = true_positives / (predicted_positives + K.epsilon())
            return precision

        def f1_m(y_true, y_pred):
            precision = precision_m(y_true, y_pred)
            recall = recall_m(y_true, y_pred)
            return 2 * ((precision * recall) / (precision + recall + K.epsilon()))

        model.compile(
            optimizer=Adam(learning_rate=0.0001),
            loss=loss_function,
            metrics=['accuracy', f1_m, precision_m, recall_m]
        )

        model.load_weights(model_path)
        self.models[plant_name] = model
        return model
