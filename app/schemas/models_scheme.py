from pydantic import BaseModel
from typing import List

class ModelReloadRequest(BaseModel):
    model_name: str
