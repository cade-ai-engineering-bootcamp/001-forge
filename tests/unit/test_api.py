import asyncio
import importlib
import sys
from importlib.metadata import version

import httpx
from fastapi import FastAPI

import forge.api
from forge.api import create_app
from forge.config import Environment, LogLevel, Settings


async def request_health(app: FastAPI) -> httpx.Response:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        return await client.get("/health")


def test_create_app_uses_injected_settings_and_configures_logging(
    monkeypatch,
) -> None:
    settings = Settings(
        environment=Environment.TEST,
        log_level=LogLevel.WARNING,
        log_json=True,
        _env_file=None,
    )
    logging_arguments = {}

    def fail_if_settings_are_loaded():
        raise AssertionError("Injected settings should bypass external loading")

    def record_logging_configuration(*, log_level, json_output):
        logging_arguments.update(
            log_level=log_level,
            json_output=json_output,
        )

    monkeypatch.setattr(forge.api, "load_settings", fail_if_settings_are_loaded)
    monkeypatch.setattr(
        forge.api,
        "configure_logging",
        record_logging_configuration,
    )

    app = create_app(settings=settings)

    assert app.debug is False
    assert app.title == "Forge"
    assert app.version == version("forge-ai-starter-kit")
    assert app.state.settings is settings
    assert logging_arguments == {
        "log_level": LogLevel.WARNING,
        "json_output": True,
    }


def test_create_app_loads_settings_when_they_are_not_injected(monkeypatch) -> None:
    settings = Settings(_env_file=None)
    monkeypatch.setattr(forge.api, "load_settings", lambda: settings)
    monkeypatch.setattr(forge.api, "configure_logging", lambda **_: None)

    app = create_app()

    assert app.state.settings is settings


def test_health_returns_typed_liveness_response(monkeypatch) -> None:
    monkeypatch.setattr(forge.api, "configure_logging", lambda **_: None)
    app = create_app(settings=Settings(_env_file=None))

    response = asyncio.run(request_health(app))

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"status": "ok"}

    response_schema = app.openapi()["paths"]["/health"]["get"]["responses"]["200"]
    assert response_schema["content"]["application/json"]["schema"] == {
        "$ref": "#/components/schemas/HealthResponse"
    }


def test_runtime_module_exposes_factory_created_asgi_app(monkeypatch) -> None:
    expected_app = FastAPI()
    monkeypatch.setattr(forge.api, "create_app", lambda: expected_app)
    sys.modules.pop("forge.main", None)

    runtime_module = importlib.import_module("forge.main")

    assert runtime_module.app is expected_app
