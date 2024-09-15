# type: ignore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.inference import router as inference_router
from app.api.healthcheck import router as healthcheck_router
from app.core.lifetime import register_startup_event, register_shutdown_event

def get_app() -> FastAPI:
    app = FastAPI(title="ML API")
    
    # CORS setup
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(inference_router, prefix="/api")
    app.include_router(healthcheck_router)

    # Register app startup and shutdown events
    register_startup_event(app)
    register_shutdown_event(app)

    return app
