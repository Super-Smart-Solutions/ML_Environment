import requests
from PIL import Image
from io import BytesIO
import aioboto3
from functools import wraps
from typing import Optional, Callable
import asyncio
from app.core.config import settings
import os
from pathlib import Path

def download_image_from_s3(presigned_url: str) -> Image.Image:
    """
    Downloads an image from an AWS S3 presigned URL.

    :param presigned_url: The presigned URL for the S3 object.
    :return: A PIL image object.
    """
    response = requests.get(presigned_url)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))
    return image


async def s3_download_object(bucket_name: str, key: str, file_path: str):
    """
    A helper function to downloads an S3 object.

    :param bucket_name: The name of the S3 bucket.
    :param key: key name of the S3 object
    :file_path: path to write the downloaded object
    :return: path of the downloaded file.
    """
    #print("raw_path", file_path)

    saved_file_path = Path(file_path).joinpath(key)
    saved_file_dir= saved_file_path.parent
    #print("file_path", saved_file_path)
    #print("dir_path", saved_file_dir)
    if saved_file_path.is_file():
        return saved_file_path
    if not os.path.exists(saved_file_dir):
        os.makedirs(saved_file_dir, exist_ok=True)
    async with aioboto3.Session().client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_DEFAULT_REGION
    ) as s3_client:
        try:
            await s3_client.download_file(bucket_name, key, saved_file_path)
            return saved_file_path
        except Exception as e:
            raise e

def s3_download_object_decorator(bucket_name: str, file_path: str, modify_function: Optional[Callable] = None):
    """
    A decorator to add S3 utility wrapper to any function.

    :param bucket_name: The name of the S3 bucket.
    :param file_path: path to write the downloaded object
    :param modify_function: a callable function to apply modification on downloaded object

    :return: decorator
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(object_key: str,*args, **kwargs):
            downloaded_file_path = await s3_download_object(bucket_name, object_key, file_path)
            if modify_function:
                result = await modify_function(downloaded_file_path)
                return await func(result, *args, **kwargs)
            return await func(downloaded_file_path, *args, **kwargs)
        return wrapper
    return decorator
