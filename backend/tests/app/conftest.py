from collections.abc import AsyncGenerator, Callable, Coroutine

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient, Response

from app.settings import Settings

pytestmark = pytest.mark.anyio


@pytest.fixture
def echo_endpoint() -> str:
    return "/v1/dev/echo"


@pytest.fixture
def error_endpoint() -> str:
    return "/v1/dev/error"


@pytest.fixture
def test_data() -> str:
    return "testparam"


@pytest.fixture
def origin(settings: Settings) -> str:
    """Get the frontend URL from the settings (the origin)."""
    # We need to strip the trailing slash - CORSMiddleware compares the URL without the trailing slash
    return str(settings.app.frontend_url).rstrip("/")


@pytest.fixture
async def get_error_resp_frontend_origin(
    client_no_raise: AsyncClient, origin: str, error_endpoint: str
) -> Callable[[], Coroutine[None, None, Response]]:
    async def _call() -> Response:
        return await client_no_raise.post(error_endpoint, headers={"origin": origin})

    return _call


@pytest.fixture
async def get_error_resp_no_origin(
    client_no_raise: AsyncClient, error_endpoint: str
) -> Callable[[], Coroutine[None, None, Response]]:
    async def _call() -> Response:
        return await client_no_raise.post(error_endpoint)

    return _call


@pytest.fixture
async def client_no_raise(app: FastAPI) -> AsyncGenerator[AsyncClient]:
    """A test client with that does not raise app exceptions."""
    async with (
        AsyncClient(
            transport=ASGITransport(app=app, raise_app_exceptions=False),
            base_url="https://test",  # Must be https otherwise our cookie with Secure=True won't work
        ) as ac
    ):
        yield ac
