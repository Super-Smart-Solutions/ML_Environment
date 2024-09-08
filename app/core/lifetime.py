from typing import Awaitable, Callable

def register_startup_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application startup.

    :param app: the fastAPI application.
    :return: event handler.
    """

    @app.on_event("startup")
    async def _startup() -> None:
        app.middleware_stack = None
        app.middleware_stack = app.build_middleware_stack()

    return _startup


def register_shutdown_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: event handler.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:
        pass
    return _shutdown