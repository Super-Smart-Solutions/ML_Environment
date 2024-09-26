from app.utils.s3_utils import s3_download_object_decorator
from app.core.config import settings
import json


MODEL_CLASSES = {}

@s3_download_object_decorator(
	bucket_name=settings.AWS_WEIGHTS_BUCKET_NAME,
	object_key="classes.json",
	file_path=settings.WEIGHTS_DIR
)
async def get_classes(downloaded_file_path, *args, **kwargs):
	try:
		with open(downloaded_file_path, 'r') as file:
			MODEL_CLASSES = json.load(file)
	except Exception as e:
		raise e
	
		
