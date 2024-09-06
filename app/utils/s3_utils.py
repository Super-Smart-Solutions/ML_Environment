import io
from io import BytesIO
from PIL import Image
import requests


def download_image_from_s3(presigned_url: str):
    """
    Downloads an image from an AWS S3 presigned URL.

    :param presigned_url: The presigned URL for the S3 object.
    :return: A PIL image object.
    """
    response = requests.get(presigned_url)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))
    return image

