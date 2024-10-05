from app.core.config import settings
import json
from app.ml_models_utils.model_manager import ModelManager
import asyncio
from app.utils.s3_utils import s3_download_object_decorator
from app.utils.utils import update_model_version, initialize_model_version
from app.utils.custom_exceptions import ModelNotFoundError

model_manager = ModelManager()


#MODEL_CLASSES = {}

@s3_download_object_decorator(
	bucket_name=settings.AWS_WEIGHTS_BUCKET_NAME,
	file_path=settings.WEIGHTS_DIR
)
async def get_classes(downloaded_file_path, object_key: str = ""):
	try:
		with open(downloaded_file_path, 'r') as file:
			model_manager.class_dict = json.load(file)
	except Exception as e:
		raise e


async def preload_models():
	try:
		initialize_model_version()
		result = await get_classes(object_key="classes.json")
	except Exception as e:
		raise e

	for i in model_manager.class_dict.keys():
		result = await model_manager._load_model_from_s3(i)

	return True

def get_disease_name(model_name:str, disease_index:int) -> str:
	plant = model_manager.class_dict.get(model_name, None)
	if plant:
		disease_name = plant.get(str(disease_index), None)
		return disease_name if disease_name else ""
	raise ModelNotFoundError(f"Model {model_name} is not found in classes.")