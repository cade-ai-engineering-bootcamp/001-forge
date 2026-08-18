"""FastAPI application construction for Forge."""

from importlib.metadata import version
from typing import Literal

from fastapi import FastAPI, status
from pydantic import BaseModel

from forge.config import Settings, load_settings
from forge.logging import configure_logging


class HealthResponse(BaseModel):
    """Typed response returned by Forge's liveness endpoint."""

    status: Literal["ok"] = "ok"


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

    @app.get(
        "/health",
        response_model=HealthResponse,
        status_code=status.HTTP_200_OK,
    )
    async def health() -> HealthResponse:
        """Confirm that the Forge HTTP process can respond to requests."""
        return HealthResponse()

    return app
