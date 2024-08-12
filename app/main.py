from fastapi import FastAPI
from app.api.inference import inference_router
from app.api.healthcheck import healthcheck_router

app = FastAPI()

app.include_router(inference_router)
app.include_router(healthcheck_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the ML API"}
