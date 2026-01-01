from collections.abc import Callable

import pytest
from httpx import AsyncClient
from pydantic import HttpUrl
from structlog.testing import capture_logs

from app.api.utils import get_route_prefix, make_uri
from app.settings import Settings

pytestmark = pytest.mark.anyio


@pytest.fixture
def echo_endpoint() -> str:
    return "/v1/dev/echo"


def test_get_route_prefix() -> None:
    """
    Test the route prefix generation functionality:

    1. Ensures the returned path always starts with '/'
    2. Verifies correct path construction from calling module to 'until'
    3. Confirms proper underscore to hyphen conversion
    """
    assert get_route_prefix("api") == f"/{__name__.split('.')[2].replace('_', '-')}"


async def test_api_prefix_is_added_to_request_path(
    client: AsyncClient, echo_endpoint: str, settings: Settings
) -> None:
    """
    Test that the client adds the API prefix to the request path.

    E.g. if the API prefix is '/api' and the request path is '/echo', then client.get('/echo') should send a request to '/api/echo'.

    This is a behavior of the test client.
    """
    with capture_logs() as cap_logs:
        await client.get(echo_endpoint)
        assert cap_logs[-1].get("path") == settings.app.api_prefix + echo_endpoint


@pytest.fixture
def make_settings(settings: Settings) -> Callable[[str, str], Settings]:
    def _make(backend_url: str, api_prefix: str) -> Settings:
        settings.app.backend_url = HttpUrl(backend_url)
        settings.app.api_prefix = api_prefix
        return settings

    return _make


def test_make_url(make_settings: Callable[[str, str], Settings]) -> None:
    """Test the make_url utility function."""
    assert (
        make_uri(make_settings("http://localhost:8000", "/api"), "test-path")
        == "http://localhost:8000/api/test-path"
    )


def test_make_url_strips_slashes(make_settings: Callable[[str, str], Settings]) -> None:
    assert (
        make_uri(make_settings("http://localhost:8000", "/api/"), "/test-path/")
        == "http://localhost:8000/api/test-path"
    )


def test_make_url_no_api_prefix(make_settings: Callable[[str, str], Settings]) -> None:
    assert (
        make_uri(make_settings("http://localhost:8000", ""), "test-path")
        == "http://localhost:8000/test-path"
    )
