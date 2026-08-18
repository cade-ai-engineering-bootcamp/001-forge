import asyncio

import httpx
import pytest
from fastapi import FastAPI

from forge.api import create_app
from forge.config import Settings
from forge.errors import (
    ApplicationError,
    ConflictError,
    DependencyUnavailableError,
    InvalidInputError,
    ResourceNotFoundError,
)

ERROR_CASES = [
    (InvalidInputError, 400),
    (ResourceNotFoundError, 404),
    (ConflictError, 409),
    (DependencyUnavailableError, 503),
    (ApplicationError, 500),
]


async def request(app: FastAPI, path: str) -> httpx.Response:
    transport = httpx.ASGITransport(app=app, raise_app_exceptions=False)
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        return await client.get(path)


def app_that_raises(exception: Exception) -> FastAPI:
    app = create_app(settings=Settings(_env_file=None))

    @app.get("/test/error")
    async def raise_test_error() -> None:
        raise exception

    return app


@pytest.mark.parametrize(("error_type", "expected_status"), ERROR_CASES)
def test_application_errors_map_to_safe_http_responses(
    error_type: type[ApplicationError],
    expected_status: int,
) -> None:
    internal_detail = "Private application diagnostic"
    error = error_type(internal_detail=internal_detail)

    response = asyncio.run(request(app_that_raises(error), "/test/error"))

    assert response.status_code == expected_status
    assert response.headers["content-type"] == "application/json"
    assert response.json() == error.to_public_dict()
    assert internal_detail not in response.text


def test_unexpected_errors_return_a_generic_response_without_details() -> None:
    private_detail = "Private unexpected failure detail"
    error = RuntimeError(private_detail)

    response = asyncio.run(request(app_that_raises(error), "/test/error"))

    assert response.status_code == 500
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {
        "code": "internal_server_error",
        "message": "An unexpected error occurred.",
    }
    assert private_detail not in response.text
    assert "RuntimeError" not in response.text
    assert "Traceback" not in response.text
