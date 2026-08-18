"""FastAPI application construction for Forge."""

from importlib.metadata import version

from fastapi import FastAPI

from forge.config import Settings, load_settings
from forge.logging import configure_logging


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
    return app
