"""Predictable logging configuration for Forge."""

import logging
import sys
from collections.abc import Mapping
from typing import Final

import structlog
from structlog.typing import EventDict, Processor

from forge.config import LogLevel

LOGGER_NAME: Final = "forge"
REDACTED_VALUE: Final = "[REDACTED]"

_LOG_LEVEL_VALUES: Final[dict[LogLevel, int]] = {
    LogLevel.DEBUG: logging.DEBUG,
    LogLevel.INFO: logging.INFO,
    LogLevel.WARNING: logging.WARNING,
    LogLevel.ERROR: logging.ERROR,
    LogLevel.CRITICAL: logging.CRITICAL,
}
_SENSITIVE_FIELD_NAMES: Final[frozenset[str]] = frozenset(
    {
        "api_key",
        "authorization",
        "cookie",
        "password",
        "secret",
        "set_cookie",
        "token",
    }
)
_SENSITIVE_FIELD_SUFFIXES: Final[tuple[str, ...]] = (
    "_api_key",
    "_authorization",
    "_cookie",
    "_password",
    "_secret",
    "_token",
)


def bind_context(**values: object) -> None:
    """Bind values to the current execution context for future log events."""
    structlog.contextvars.bind_contextvars(**values)


def clear_context() -> None:
    """Clear all Forge logging values from the current execution context."""
    structlog.contextvars.clear_contextvars()


def _is_sensitive_field(field_name: str) -> bool:
    normalized_name = field_name.casefold().replace("-", "_")
    return normalized_name in _SENSITIVE_FIELD_NAMES or normalized_name.endswith(
        _SENSITIVE_FIELD_SUFFIXES
    )


def _redact_nested(value: object) -> object:
    if isinstance(value, Mapping):
        return {
            key: (
                REDACTED_VALUE
                if isinstance(key, str) and _is_sensitive_field(key)
                else _redact_nested(nested_value)
            )
            for key, nested_value in value.items()
        }
    if isinstance(value, list):
        return [_redact_nested(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_redact_nested(item) for item in value)
    return value


def _redact_sensitive_data(
    _: object,
    __: str,
    event_dict: EventDict,
) -> EventDict:
    for key, value in event_dict.items():
        event_dict[key] = (
            REDACTED_VALUE if _is_sensitive_field(key) else _redact_nested(value)
        )
    return event_dict


def configure_logging(*, log_level: LogLevel, json_output: bool) -> None:
    """Configure Forge logging with one replaceable standard-library handler."""
    level = _LOG_LEVEL_VALUES[log_level]
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        _redact_sensitive_data,
    ]

    renderer: Processor
    if json_output:
        renderer = structlog.processors.JSONRenderer(sort_keys=True)
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=False)

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=[structlog.stdlib.ExtraAdder(), *shared_processors],
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    forge_logger = logging.getLogger(LOGGER_NAME)
    for existing_handler in forge_logger.handlers:
        existing_handler.close()
    forge_logger.handlers.clear()
    forge_logger.addHandler(handler)
    forge_logger.setLevel(level)
    forge_logger.propagate = False

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=False,
    )
