import json
import logging
from collections.abc import Iterator

import pytest
import structlog

from forge.config import LogLevel
from forge.logging import (
    LOGGER_NAME,
    REDACTED_VALUE,
    bind_context,
    clear_context,
    configure_logging,
)


@pytest.fixture(autouse=True)
def reset_logging_state() -> Iterator[None]:
    """Remove logging state created by each test."""
    clear_context()
    yield

    clear_context()
    forge_logger = logging.getLogger(LOGGER_NAME)
    for handler in forge_logger.handlers:
        handler.close()
    forge_logger.handlers.clear()
    forge_logger.setLevel(logging.NOTSET)
    forge_logger.propagate = True
    structlog.reset_defaults()


def test_human_readable_logging(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging(log_level=LogLevel.INFO, json_output=False)

    structlog.get_logger("forge.test").info("service_started")

    output = capsys.readouterr().out.strip()
    assert "service_started" in output
    assert "info" in output
    assert not output.startswith("{")


def test_json_logging(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging(log_level=LogLevel.INFO, json_output=True)

    structlog.get_logger("forge.test").info("service_started")

    payload = json.loads(capsys.readouterr().out)
    assert payload["event"] == "service_started"
    assert payload["level"] == "info"
    assert payload["timestamp"].endswith("Z")


def test_standard_library_logs_use_the_selected_renderer(
    capsys: pytest.CaptureFixture[str],
) -> None:
    configure_logging(log_level=LogLevel.INFO, json_output=True)

    logging.getLogger("forge.test").info("standard_library_event")

    payload = json.loads(capsys.readouterr().out)
    assert payload["event"] == "standard_library_event"
    assert payload["level"] == "info"


def test_configuration_leaves_root_handlers_unchanged() -> None:
    root_logger = logging.getLogger()
    original_handlers = tuple(root_logger.handlers)

    configure_logging(log_level=LogLevel.INFO, json_output=False)

    assert tuple(root_logger.handlers) == original_handlers


def test_log_level_filters_lower_priority_events(
    capsys: pytest.CaptureFixture[str],
) -> None:
    configure_logging(log_level=LogLevel.WARNING, json_output=True)
    logger = structlog.get_logger("forge.test")

    logger.info("filtered_event")
    logger.warning("visible_event")

    output_lines = capsys.readouterr().out.strip().splitlines()
    assert len(output_lines) == 1
    assert json.loads(output_lines[0])["event"] == "visible_event"


def test_repeated_configuration_does_not_duplicate_messages(
    capsys: pytest.CaptureFixture[str],
) -> None:
    configure_logging(log_level=LogLevel.INFO, json_output=False)
    configure_logging(log_level=LogLevel.INFO, json_output=False)

    forge_logger = logging.getLogger(LOGGER_NAME)
    structlog.get_logger("forge.test").info("single_event")

    output_lines = capsys.readouterr().out.strip().splitlines()
    assert len(forge_logger.handlers) == 1
    assert len(output_lines) == 1
    assert "single_event" in output_lines[0]


def test_bound_context_is_included_and_sensitive_context_is_redacted(
    capsys: pytest.CaptureFixture[str],
) -> None:
    configure_logging(log_level=LogLevel.INFO, json_output=True)
    bind_context(
        request_id="req-123",
        component="health",
        api_key="context-secret",
    )

    structlog.get_logger("forge.test").info("request_started")

    payload = json.loads(capsys.readouterr().out)
    assert payload["request_id"] == "req-123"
    assert payload["component"] == "health"
    assert payload["api_key"] == REDACTED_VALUE
    assert "context-secret" not in str(payload)


def test_cleared_context_does_not_leak_into_later_events(
    capsys: pytest.CaptureFixture[str],
) -> None:
    configure_logging(log_level=LogLevel.INFO, json_output=True)
    bind_context(request_id="req-123")
    clear_context()

    structlog.get_logger("forge.test").info("context_cleared")

    payload = json.loads(capsys.readouterr().out)
    assert "request_id" not in payload


def test_nested_sensitive_fields_are_redacted_without_hiding_safe_fields(
    capsys: pytest.CaptureFixture[str],
) -> None:
    configure_logging(log_level=LogLevel.INFO, json_output=True)

    structlog.get_logger("forge.test").info(
        "request_received",
        token_count=250,
        headers={
            "Authorization": "Bearer nested-secret",
            "Content-Type": "application/json",
            "X-API-Key": "nested-api-key",
        },
        attempts=[{"client_secret": "nested-client-secret"}],
        credentials=({"refresh_token": "nested-refresh-token"},),
        labels={1: "safe-label"},
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["token_count"] == 250
    assert payload["headers"]["Content-Type"] == "application/json"
    assert payload["headers"]["Authorization"] == REDACTED_VALUE
    assert payload["headers"]["X-API-Key"] == REDACTED_VALUE
    assert payload["attempts"][0]["client_secret"] == REDACTED_VALUE
    assert payload["credentials"][0]["refresh_token"] == REDACTED_VALUE
    assert payload["labels"]["1"] == "safe-label"
    assert "nested-secret" not in str(payload)
    assert "nested-api-key" not in str(payload)
    assert "nested-client-secret" not in str(payload)
    assert "nested-refresh-token" not in str(payload)


def test_standard_library_extra_fields_follow_the_redaction_policy(
    capsys: pytest.CaptureFixture[str],
) -> None:
    configure_logging(log_level=LogLevel.INFO, json_output=True)

    logging.getLogger("forge.test").info(
        "standard_library_context",
        extra={"request_id": "req-456", "access_token": "stdlib-secret"},
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["request_id"] == "req-456"
    assert payload["access_token"] == REDACTED_VALUE
    assert "stdlib-secret" not in str(payload)


def test_human_readable_output_does_not_contain_sensitive_values(
    capsys: pytest.CaptureFixture[str],
) -> None:
    configure_logging(log_level=LogLevel.INFO, json_output=False)

    structlog.get_logger("forge.test").info(
        "credentials_received",
        password="human-secret",
        metadata={"session_cookie": "human-cookie"},
    )

    output = capsys.readouterr().out
    assert REDACTED_VALUE in output
    assert "human-secret" not in output
    assert "human-cookie" not in output
