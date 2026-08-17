"""Predictable logging configuration for Forge."""

import logging
import sys
from typing import Final

import structlog
from structlog.typing import Processor

from forge.config import LogLevel

LOGGER_NAME: Final = "forge"

_LOG_LEVEL_VALUES: Final[dict[LogLevel, int]] = {
    LogLevel.DEBUG: logging.DEBUG,
    LogLevel.INFO: logging.INFO,
    LogLevel.WARNING: logging.WARNING,
    LogLevel.ERROR: logging.ERROR,
    LogLevel.CRITICAL: logging.CRITICAL,
}


def configure_logging(*, log_level: LogLevel, json_output: bool) -> None:
    """Configure Forge logging with one replaceable standard-library handler."""
    level = _LOG_LEVEL_VALUES[log_level]
    shared_processors: list[Processor] = [
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
    ]

    renderer: Processor
    if json_output:
        renderer = structlog.processors.JSONRenderer(sort_keys=True)
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=False)

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
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
