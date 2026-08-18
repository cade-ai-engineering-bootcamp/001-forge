"""ASGI runtime entry point for Forge."""

from forge.api import create_app

app = create_app()
