# app/core/config.py

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """
    APP_NAME: str = "Pest Identification ML API"
    host: str = "127.0.0.1"
    port: int = 8000
    # no. of workers for uvicorn
    # using 1 in dev envionment 
    # should be more in production
    workers_count: int = 1
    # Enable uvicorn reloading
    # Should be False in production for stability
    reload: bool = True

    # Current Environment
    ENVIRONMENT: str = "dev"

    #AWS S3
    S3_BUCKET_NAME: str = ""
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_BUCKET_NAME: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="ML_APIS_",
        env_file_encoding="utf-8",
    )

# Instantiate the settings
settings = Settings()
