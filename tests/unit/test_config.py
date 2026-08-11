import logging
from pathlib import Path

import pytest
from pydantic import ValidationError

from forge.config import Environment, LogLevel, load_settings

FORGE_ENVIRONMENT_VARIABLES = (
    "FORGE_ENVIRONMENT",
    "FORGE_LOG_LEVEL",
    "FORGE_LOG_JSON",
    "FORGE_API_KEY",
)


@pytest.fixture(autouse=True)
def isolate_forge_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Prevent a developer's shell environment from influencing these tests."""
    for variable in FORGE_ENVIRONMENT_VARIABLES:
        monkeypatch.delenv(variable, raising=False)


def test_load_settings_uses_safe_defaults() -> None:
    settings = load_settings(env_file=None)

    assert settings.environment is Environment.DEVELOPMENT
    assert settings.log_level is LogLevel.INFO
    assert settings.log_json is False
    assert settings.api_key is None


def test_load_settings_returns_fresh_instances() -> None:
    first = load_settings(env_file=None)
    second = load_settings(env_file=None)

    assert first is not second


def test_load_settings_reads_typed_dotenv_values(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "FORGE_ENVIRONMENT=test\n"
        "FORGE_LOG_LEVEL=DEBUG\n"
        "FORGE_LOG_JSON=true\n"
        "FORGE_API_KEY=dotenv-secret\n",
        encoding="utf-8",
    )

    settings = load_settings(env_file=env_file)

    assert settings.environment is Environment.TEST
    assert settings.log_level is LogLevel.DEBUG
    assert settings.log_json is True
    assert settings.api_key is not None
    assert settings.api_key.get_secret_value() == "dotenv-secret"


def test_environment_overrides_dotenv(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "FORGE_ENVIRONMENT=test\nFORGE_LOG_LEVEL=DEBUG\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("FORGE_ENVIRONMENT", "production")

    settings = load_settings(env_file=env_file)

    assert settings.environment is Environment.PRODUCTION
    assert settings.log_level is LogLevel.DEBUG


@pytest.mark.parametrize(
    ("variable", "value", "field"),
    [
        ("FORGE_ENVIRONMENT", "staging", "environment"),
        ("FORGE_LOG_LEVEL", "TRACE", "log_level"),
        ("FORGE_LOG_JSON", "sometimes", "log_json"),
    ],
)
def test_invalid_values_identify_the_affected_field(
    variable: str,
    value: str,
    field: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(variable, value)

    with pytest.raises(ValidationError) as error:
        load_settings(env_file=None)

    assert field in str(error.value)


def test_empty_api_key_is_treated_as_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FORGE_API_KEY", "")

    settings = load_settings(env_file=None)

    assert settings.api_key is None


def test_secret_is_masked_in_representations_and_logs(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    secret = "representation-secret"
    monkeypatch.setenv("FORGE_API_KEY", secret)
    settings = load_settings(env_file=None)
    assert settings.api_key is not None

    logger = logging.getLogger("forge.config.test")
    with caplog.at_level(logging.INFO, logger=logger.name):
        logger.info("Loaded settings: %s", settings)

    renderings = (
        repr(settings),
        str(settings),
        repr(settings.api_key),
        str(settings.api_key),
        caplog.text,
    )

    assert all(secret not in rendered for rendered in renderings)
    assert "**********" in repr(settings)
