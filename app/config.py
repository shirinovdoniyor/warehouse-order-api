from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Warehouse Order API"
    environment: str = "development"
    database_url: str = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/warehouse"
    )
    test_database_url: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
