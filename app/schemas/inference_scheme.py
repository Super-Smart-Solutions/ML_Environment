from pydantic import BaseModel
from typing import List

class InferenceRequest(BaseModel):
    model_name: str
    presigned_url: str


class InferenceResponse(BaseModel):
    predicted_class: str
    confidence: str