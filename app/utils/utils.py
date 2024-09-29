from app.core.config import settings
import json
import asyncio
import os

def initialize_model_version()->bool:
	if not os.path.exists(settings.WEIGHTS_DIR):
		os.makedirs(settings.WEIGHTS_DIR, exist_ok=True)

	if not os.path.exists(settings.VERSIONS_PATH):
		with open(settings.VERSIONS_PATH, 'w') as json_file:
			json.dump({"models": {}}, json_file)

def update_model_version(model_name: str, version: str):
	# Check if the JSON file exists; if not, create an empty one
	if not os.path.exists(settings.VERSIONS_PATH):
		raise FileNotFoundError

	# Load the existing data from the JSON file
	with open(settings.VERSIONS_PATH, 'r') as json_file:
		data = json.load(json_file)

	# Update or add the version for the given model_name
	data["models"][model_name] = {"version": version}

	# Save the updated data back to the JSON file
	with open(settings.VERSIONS_PATH, 'w') as json_file:
		json.dump(data, json_file, indent=4)

	print(f"Updated {model_name} with version {version}")
	
def get_model_version(model_name: str) -> str | None:
	if not os.path.exists(settings.VERSIONS_PATH):
		raise FileNotFoundError

	with open(settings.VERSIONS_PATH, 'r') as json_file:
		data = json.load(json_file)

	if model_name in data.get("models", {}):
		return data["models"][model_name]["version"]
	else:
		return None


