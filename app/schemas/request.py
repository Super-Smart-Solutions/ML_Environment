from pydantic import BaseModel

class InferenceRequest(BaseModel):
    model_name: str
    presigned_url: str
