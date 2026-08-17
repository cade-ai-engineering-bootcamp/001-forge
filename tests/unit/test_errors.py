import json
import logging
from collections.abc import Iterator

import pytest
import structlog

from forge.config import LogLevel
from forge.errors import (
    ApplicationError,
    ConflictError,
    DependencyUnavailableError,
    InvalidInputError,
    ResourceNotFoundError,
)
from forge.logging import LOGGER_NAME, clear_context, configure_logging

ERROR_CASES = [
    (
        ApplicationError,
        "application_error",
        "The application could not complete the operation.",
    ),
    (InvalidInputError, "invalid_input", "The supplied input is invalid."),
    (
        ResourceNotFoundError,
        "resource_not_found",
        "The requested resource was not found.",
    ),
    (
        ConflictError,
        "conflict",
        "The operation conflicts with the current state.",
    ),
    (
        DependencyUnavailableError,
        "dependency_unavailable",
        "A required service is temporarily unavailable.",
    ),
]


@pytest.fixture
def reset_logging_state() -> Iterator[None]:
    """Remove logging state created by the error logging test."""
    yield

    clear_context()
    forge_logger = logging.getLogger(LOGGER_NAME)
    for handler in forge_logger.handlers:
        handler.close()
    forge_logger.handlers.clear()
    forge_logger.setLevel(logging.NOTSET)
    forge_logger.propagate = True
    structlog.reset_defaults()


@pytest.mark.parametrize(("error_type", "code", "message"), ERROR_CASES)
def test_errors_have_stable_public_contracts(
    error_type: type[ApplicationError],
    code: str,
    message: str,
) -> None:
    error = error_type()

    assert error.code == code
    assert str(error) == message
    assert error.to_public_dict() == {"code": code, "message": message}


@pytest.mark.parametrize(
    "error_type",
    [
        InvalidInputError,
        ResourceNotFoundError,
        ConflictError,
        DependencyUnavailableError,
    ],
)
def test_known_errors_are_caught_through_the_base_class(
    error_type: type[ApplicationError],
) -> None:
    with pytest.raises(ApplicationError):
        raise error_type()


def test_internal_detail_is_available_but_absent_from_public_representations() -> None:
    internal_detail = "Dependency timed out while contacting a private endpoint."
    error = DependencyUnavailableError(internal_detail=internal_detail)

    assert error.internal_detail == internal_detail
    assert internal_detail not in str(error)
    assert internal_detail not in repr(error)
    assert internal_detail not in str(error.to_public_dict())


def test_exception_chaining_preserves_the_original_cause() -> None:
    cause = RuntimeError("Private low-level failure")

    with pytest.raises(DependencyUnavailableError) as captured:
        try:
            raise cause
        except RuntimeError as error:
            raise DependencyUnavailableError(
                internal_detail="The dependency operation failed."
            ) from error

    assert captured.value.__cause__ is cause
    assert str(cause) not in str(captured.value)
    assert str(cause) not in str(captured.value.to_public_dict())


def test_logging_an_error_does_not_expose_its_internal_detail(
    capsys: pytest.CaptureFixture[str],
    reset_logging_state: None,
) -> None:
    configure_logging(log_level=LogLevel.INFO, json_output=True)
    internal_detail = "Private dependency diagnostic"
    error = DependencyUnavailableError(internal_detail=internal_detail)

    structlog.get_logger("forge.test").error(
        "operation_failed",
        error=error,
        error_code=error.code,
    )

    output = capsys.readouterr().out
    payload = json.loads(output)
    assert payload["error_code"] == "dependency_unavailable"
    assert internal_detail not in output
