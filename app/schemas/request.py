from pydantic import BaseModel

class InferenceRequest(BaseModel):
    param1: int = 10
    param2: str = "default"
