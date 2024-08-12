from pydantic import BaseModel

class InferenceResponse(BaseModel):
    prediction: dict
