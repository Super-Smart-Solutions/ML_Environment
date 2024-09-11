import os
import uvicorn
from app.core.config import settings
from app.core.gunicorn_runner import GunicornApplication
from app.api.inference import app  # Import the FastAPI app

def main() -> None:
    """Entrypoint of the application."""
    if settings.reload:
        uvicorn.run(
            "app.api.inference:app",
            workers=settings.workers_count,
            host=settings.host,
            port=settings.port,
            reload=settings.reload,
            # loglevel=settings.log_level.value.lower(),
            factory=True,
        )
    else:
        # Gunicorn in production for better stability
        GunicornApplication(
            "app.api.inference:app",
            host=settings.host,
            port=settings.port,
            workers=settings.workers_count,
            factory=True,
            accesslog="-",
            # loglevel=settings.log_level.value.lower(),
            access_log_format='%r "-" %s "-" %Tf',
        ).run()



# Entry point for running the app
if __name__ == "__main__":
    main()
