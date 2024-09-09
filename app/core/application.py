# type: ignore

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
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

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Total-Count"],
    )

    # ROUTERS.
    app.include_router(inference_router, prefix="/api/inference", tags=["Inference"])
    app.include_router(healthcheck_router, prefix="/api/healthcheck", tags=["Healthcheck"])

    return app