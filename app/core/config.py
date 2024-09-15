import enum
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
class LogLevel(str, enum.Enum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"

class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """
    APP_NAME: str = "Pest Identification ML API"
    host: str = "0.0.0.0"
    port: int = 8000
    # no. of workers for uvicorn
    # using 1 in dev envionment 
    # should be more in production
    workers_count: int = 1
    # Enable uvicorn reloading
    # Should be False in production for stability
    reload: bool = True

    # Current Environment
    ENVIRONMENT: str = os.getenv('NAME', 'dev')
    log_level: LogLevel = LogLevel.INFO

    #AWS S3
    AWS_DEFAULT_REGION: str = ""
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
