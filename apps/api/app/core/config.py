from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Harmoniza CRM API"
    environment: str = "development"
    database_url: str = "sqlite:///./harmoniza_crm.db"
    secret_key: str = "dev-secret-change-me-at-least-32-chars"
    access_token_expire_minutes: int = 60 * 24
    jwt_algorithm: str = "HS256"
    cors_origins: str = ""

    @field_validator("database_url", "secret_key", "cors_origins", mode="before")
    @classmethod
    def normalize_env_string(cls, value: str) -> str:
        if not isinstance(value, str):
            return value

        normalized = value.strip()
        if len(normalized) >= 2 and normalized[0] == normalized[-1] and normalized[0] in {'"', "'"}:
            normalized = normalized[1:-1].strip()
        return normalized

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
