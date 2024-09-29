from app.core.config import settings
import json
from app.services.model_inference import model_manager
import asyncio
from app.utils.s3_utils import s3_download_object_decorator
from app.utils.utils import update_model_version, initialize_model_version

MODEL_CLASSES = {}

@s3_download_object_decorator(
	bucket_name=settings.AWS_WEIGHTS_BUCKET_NAME,
	file_path=settings.WEIGHTS_DIR
)
async def get_classes(downloaded_file_path, object_key: str = ""):
	global MODEL_CLASSES
	try:
		with open(downloaded_file_path, 'r') as file:
			MODEL_CLASSES = json.load(file)

	except Exception as e:
		raise e


async def preload_models():
	try:
		initialize_model_version()
		result = await get_classes(object_key="classes.json")
	except Exception as e:
		raise e

	for i in MODEL_CLASSES.keys():
		result = await model_manager._load_model_from_s3(i)

	return True
