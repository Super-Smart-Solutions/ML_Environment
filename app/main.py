import os

import uvicorn
from app.core.config import settings
from app.core.gunicorn_runner import GunicornApplication


def main() -> None:
    """Entrypoint of the application."""
    if settings.reload:
        uvicorn.run(
            "app.core.application:get_app",
            workers=settings.workers_count,
            host=settings.host,
            port=settings.port,
            reload=settings.reload,
            loglevel=settings.log_level.value.lower(),
            factory=True,
        )
    else:
        # gunicorn in production for better stability
        # reload is off,
        GunicornApplication(
            "app.core.application:get_app",
            host=settings.host,
            port=settings.port,
            workers=settings.workers_count,
            factory=True,
            accesslog="-",
            loglevel=settings.log_level.value.lower(),
            access_log_format='%r "-" %s "-" %Tf',
        ).run()



# Entry point for running the app directly (if not using a dedicated ASGI server)
if __name__ == "__main__":
    main()
