"""FastAPI application construction for Forge."""

from importlib.metadata import version
from typing import Literal, cast

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from forge.config import Settings, load_settings
from forge.errors import (
    ApplicationError,
    ConflictError,
    DependencyUnavailableError,
    InvalidInputError,
    ResourceNotFoundError,
)
from forge.logging import configure_logging


class HealthResponse(BaseModel):
    """Typed response returned by Forge's liveness endpoint."""

    status: Literal["ok"] = "ok"


class ErrorResponse(BaseModel):
    """Typed, public-safe error returned by Forge's HTTP boundary."""

    code: str
    message: str


def _status_code_for_application_error(error: ApplicationError) -> int:
    if isinstance(error, InvalidInputError):
        return status.HTTP_400_BAD_REQUEST
    if isinstance(error, ResourceNotFoundError):
        return status.HTTP_404_NOT_FOUND
    if isinstance(error, ConflictError):
        return status.HTTP_409_CONFLICT
    if isinstance(error, DependencyUnavailableError):
        return status.HTTP_503_SERVICE_UNAVAILABLE
    return status.HTTP_500_INTERNAL_SERVER_ERROR


async def _handle_application_error(
    _: Request,
    exception: Exception,
) -> JSONResponse:
    error = cast(ApplicationError, exception)
    response = ErrorResponse(**error.to_public_dict())
    return JSONResponse(
        status_code=_status_code_for_application_error(error),
        content=response.model_dump(),
    )


async def _handle_unexpected_error(
    _: Request,
    __: Exception,
) -> JSONResponse:
    response = ErrorResponse(
        code="internal_server_error",
        message="An unexpected error occurred.",
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.model_dump(),
    )


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create a configured Forge application with injectable settings."""
    resolved_settings = settings if settings is not None else load_settings()
    configure_logging(
        log_level=resolved_settings.log_level,
        json_output=resolved_settings.log_json,
    )

    app = FastAPI(
        debug=False,
        title="Forge",
        version=version("forge-ai-starter-kit"),
    )
    app.state.settings = resolved_settings
    app.add_exception_handler(ApplicationError, _handle_application_error)
    app.add_exception_handler(Exception, _handle_unexpected_error)

    @app.get(
        "/health",
        response_model=HealthResponse,
        status_code=status.HTTP_200_OK,
    )
    async def health() -> HealthResponse:
        """Confirm that the Forge HTTP process can respond to requests."""
        return HealthResponse()

    return app
