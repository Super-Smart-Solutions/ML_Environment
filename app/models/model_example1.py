import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
from io import BytesIO
from PIL import Image

# Load the pre-trained MobileNetV2 model
model = MobileNetV2(weights='imagenet')

def predict(file, params):
    # Convert the uploaded file into a PIL image
    img = Image.open(BytesIO(file.read()))
    img = img.resize((224, 224))  # MobileNetV2 expects 224x224 images
    
    # Preprocess the image for the model
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Make predictions
    predictions = model.predict(img_array)
    
    # Decode the predictions to get human-readable labels
    decoded_predictions = decode_predictions(predictions, top=3)[0]

    # Structure the response
    results = [{"label": label, "description": description, "confidence": float(confidence)}
               for (_, label, description, confidence) in decoded_predictions]
    
    return {"predictions": results}
