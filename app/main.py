# app/main.py

from fastapi import FastAPI
#from app.core.config import settings  # Configuration module
from app.api.inference import router as inference_router
from app.api.healthcheck import router as healthcheck_router
from app.core.lifetime import register_startup_event, register_shutdown_event
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Pest Identification ML API",
    version="1.0.0"
)

# Include API routes
app.include_router(inference_router, prefix="/api/v1/inference", tags=["Inference"])
app.include_router(healthcheck_router, prefix="/api/v1/healthcheck", tags=["Healthcheck"])

#Register startup and shutdown events
register_startup_event(app)
register_shutdown_event(app)


# Entry point for running the app directly (if not using a dedicated ASGI server)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
