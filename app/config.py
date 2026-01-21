from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Database configuration
    database_url: str = "postgresql://nba_user:nba_password@localhost:5432/nba_predictions"

    # Application environment
    environment: str = "development"  # development, staging, production
    debug: bool = True
    log_level: str = "INFO"

    # API keys
    odds_api_key: str = ""

    # Security
    secret_key: str = "development-secret-key-change-in-production"

    # NBA API settings
    nba_api_timeout: int = 30
    nba_api_delay: float = 0.6  # Seconds between requests to avoid rate limiting

    # Model settings
    model_version: str = "v1"
    prediction_confidence_threshold: float = 0.55

    # Tell pydantic-settings to load from .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # DATABASE_URL and database_url both work
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

