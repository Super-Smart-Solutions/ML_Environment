from pydantic import BaseModel
from typing import List

class InferenceResponse(BaseModel):
    predicted_class: int
    predictions: List[float]
