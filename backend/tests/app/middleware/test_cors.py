import json
from collections.abc import Callable, Coroutine

import pytest
from httpx import AsyncClient, Response
from structlog.testing import capture_logs

from app.models import ErrorDetail

pytestmark = pytest.mark.anyio


def _assert_cors_response_headers(resp: Response, origin: str) -> None:
    """
    Assert that the response contains the required CORS headers for the browser to access the response.

    https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#the_http_response_headers
    """
    assert resp.headers["access-control-allow-credentials"] == "true"
    assert resp.headers["access-control-allow-origin"] == origin


class TestCorsBaseMiddlewareHeaders:
    """Test that our middleware sets correct CORS headers, like CORSMiddleware."""

    @pytest.fixture(autouse=True)
    def _fixtures(
        self,
        test_data: str,
        echo_endpoint: str,
        error_endpoint: str,
        origin: str,
        client: AsyncClient,
    ) -> None:
        self.client = client
        self.test_data = test_data
        self.echo_endpoint = echo_endpoint
        self.error_endpoint = error_endpoint
        self.origin = origin

    @pytest.mark.parametrize("method", ["GET", "POST", "DELETE"])
    async def test_preflight(self, method: str) -> None:
        """Test preflight request with frontend origin contains the correct CORS headers."""
        resp = await self.client.options(
            self.echo_endpoint,
            headers={"origin": self.origin, "Access-Control-Request-Method": method},
        )
        _assert_cors_response_headers(resp, self.origin)
        assert method in resp.headers["Access-Control-Allow-Methods"]

    async def test_get(self) -> None:
        """Test GET request with frontend origin contains the required CORS headers."""
        resp = await self.client.get(
            self.echo_endpoint,
            headers={"origin": self.origin},
            params={"param": self.test_data},
        )
        _assert_cors_response_headers(resp, self.origin)
        assert resp.content.decode() == f'"{self.test_data}"'

    async def test_get_with_invalid_parameters(self) -> None:
        """Test that GET request with invalid parameters returns 422 and contains the required CORS headers."""
        resp = await self.client.get(
            self.echo_endpoint,
            headers={"origin": self.origin},
            params={"NON_EXISTENT": "some data"},
        )
        _assert_cors_response_headers(resp, self.origin)
        assert json.loads(resp.content) == {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "param"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }

    async def test_delete(self) -> None:
        """Test DELETE request with frontend origin contains the required CORS headers. DELETE is one of the CORS non-safelisted methods."""
        resp = await self.client.delete(
            self.echo_endpoint,
            headers={"origin": self.origin},
            params={"param": self.test_data},
        )
        _assert_cors_response_headers(resp, self.origin)
        assert resp.content.decode() == f'"{self.test_data}"'

    @pytest.mark.parametrize("method", ["GET", "POST", "DELETE"])
    async def test_preflight_invalid_origin(
        self,
        method: str,
    ) -> None:
        """Test OPTIONS request with invalid origin returns 400 for all methods."""
        resp = await self.client.options(
            self.echo_endpoint,
            headers={"origin": "invalid.com", "Access-Control-Request-Method": method},
        )
        assert resp.status_code == 400
        assert resp.text == "Disallowed CORS origin"

    async def test_get_no_origin(self) -> None:
        """Test that when no origin header is set, no CORS headers are returned."""
        resp = await self.client.get(self.echo_endpoint)
        assert "access-control-allow-credentials" not in resp.headers
        assert "access-control-allow-origin" not in resp.headers


class TestCorsErrorHandlingMiddleware:
    @pytest.fixture(autouse=True)
    def _fixtures(
        self,
        error_endpoint: str,
        origin: str,
        client: AsyncClient,
        get_error_resp_frontend_origin: Callable[[], Coroutine[None, None, Response]],
        get_error_resp_no_origin: Callable[[], Coroutine[None, None, Response]],
    ) -> None:
        self.client = client
        self.error_endpoint = error_endpoint
        self.origin = origin
        self.get_error_resp_frontend_origin = get_error_resp_frontend_origin
        self.get_error_resp_no_origin = get_error_resp_no_origin

    async def test_cors_headers_present_on_cross_origin(self) -> None:
        """Test CORS headers are present on cross-origin request errors."""
        resp = await self.get_error_resp_frontend_origin()
        _assert_cors_response_headers(resp, self.origin)
        assert (
            resp.content.decode()
            == ErrorDetail(
                detail="Internal Server Error (cross-origin request)", status_code=500
            ).model_dump_json()
        )

    async def test_no_cors_headers_when_not_cross_origin(self) -> None:
        """Test CORS headers are not present on non-cross-origin request errors."""
        resp = await self.get_error_resp_no_origin()
        assert "access-control-allow-credentials" not in resp.headers
        assert "access-control-allow-origin" not in resp.headers

    async def test_logging_on_cross_origin(self) -> None:
        """Test that the middleware logs cross-origin request errors"""
        with capture_logs() as cap_logs:
            await self.get_error_resp_frontend_origin()
            log = next(
                log
                for log in cap_logs
                if log.get("event") == "Handling exception from cross-origin request"
            )
            assert log.get("path") == self.error_endpoint

    async def test_no_logging_when_not_cross_origin(self) -> None:
        """Test that the middleware doesn't log non-cross-origin request errors"""
        with capture_logs() as cap_logs:
            await self.get_error_resp_no_origin()
            assert not any(
                log.get("event") == "Handling exception from cross-origin request"
                for log in cap_logs
            )
