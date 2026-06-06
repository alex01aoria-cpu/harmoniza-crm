from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Harmoniza CRM API"
    environment: str = "development"
    database_url: str = "sqlite:///./harmoniza_crm.db"
    secret_key: str = "dev-secret-change-me-at-least-32-chars"
    access_token_expire_minutes: int = 60 * 24
    jwt_algorithm: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
