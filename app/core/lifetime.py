from fastapi import FastAPI

def register_startup_event(app: FastAPI):
    @app.on_event("startup")
    async def startup_event():
        print("Application startup")

def register_shutdown_event(app: FastAPI):
    @app.on_event("shutdown")
    async def shutdown_event():
        print("Application shutdown")
