"""Typed, environment-driven configuration for Forge."""

from enum import StrEnum
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    """Supported Forge runtime environments."""

    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class LogLevel(StrEnum):
    """Supported application logging thresholds."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Settings(BaseSettings):
    """Validated Forge settings loaded from external configuration."""

    model_config = SettingsConfigDict(
        env_prefix="FORGE_",
        env_ignore_empty=True,
        extra="ignore",
    )

    environment: Environment = Environment.DEVELOPMENT
    log_level: LogLevel = LogLevel.INFO
    log_json: bool = False
    api_key: SecretStr | None = None


def load_settings(env_file: Path | None = Path(".env")) -> Settings:
    """Return a fresh settings instance, optionally reading a dotenv file."""
    # Pydantic's generated MyPy signature omits this supported runtime keyword.
    return Settings(_env_file=env_file)  # type: ignore[call-arg]
