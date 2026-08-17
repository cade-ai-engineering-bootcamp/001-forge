import json
import logging
from collections.abc import Iterator

import pytest
import structlog

from forge.config import LogLevel
from forge.logging import LOGGER_NAME, configure_logging


@pytest.fixture(autouse=True)
def reset_logging_state() -> Iterator[None]:
    """Remove logging state created by each test."""
    yield

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
