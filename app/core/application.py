from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.inference import router as inference_router
from app.api.healthcheck import router as healthcheck_router
from app.core.lifetime import register_startup_event, register_shutdown_event

def get_app() -> FastAPI:
    """
    Get FastAPI application.
    This is the main constructor of an application.
    :return: application.
    """
    app = FastAPI(
        title="Pest Identification ML API",
        version="1.0.0",
    )
    
    # Register app startup and shutdown events
    register_startup_event(app)
    register_shutdown_event(app)
    
    # CORS setup
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(inference_router, prefix="/api/inference", tags=["Inference"])
    app.include_router(healthcheck_router, prefix="/api/healthcheck", tags=["Healthcheck"])

    

    return app
