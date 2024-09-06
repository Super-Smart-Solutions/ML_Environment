from PIL import Image
import numpy as np

def preprocess_image(image: Image.Image, target_size=(256, 256)):
    """
    Preprocess the image for model inference.

    :param image: PIL image to preprocess.
    :param target_size: Tuple specifying target image size.
    :return: Preprocessed image as numpy array.
    """
    image = image.resize(target_size)
    image_array = np.array(image)
    image_array = image_array / 255.0  # Normalize to [0, 1]
    return np.expand_dims(image_array, axis=0)
