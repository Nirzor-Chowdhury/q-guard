from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env."""

    model_config = SettingsConfigDict(
        env_prefix="QGUARD_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Q-Guard"
    app_version: str = "0.1.0"

    environment: Literal["development", "test", "staging", "production"] = (
        "development"
    )

    api_host: str = "127.0.0.1"
    api_port: int = Field(default=8000, ge=1, le=65535)
    log_level: str = "INFO"

    secure_mode: bool = True

    database_url: str = ""

    qkd_simulator_url: str = "http://127.0.0.1:8100"

    cors_origins: str = "http://127.0.0.1:3000,http://localhost:3000"

    @property
    def cors_origin_list(self) -> list[str]:
        """Return configured CORS origins as a normalized list."""
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    """Return one cached settings object for the running process."""
    return Settings()
