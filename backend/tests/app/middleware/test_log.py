from collections.abc import Callable, Coroutine

import pytest
from fastapi import FastAPI
from httpx import AsyncClient, Response
from moto import mock_aws
from structlog.testing import capture_logs

from app.api.route_map import RouteMap

pytestmark = pytest.mark.anyio


@pytest.fixture
def health_url(app: FastAPI) -> str:
    return app.url_path_for(RouteMap.HEALTHZ)


async def test_request_logged_in_exceptions(
    get_error_resp_frontend_origin: Callable[[], Coroutine[None, None, Response]],
) -> None:
    """Test that request logging works even when exceptions are raised by the app"""
    with capture_logs() as cap_logs:
        resp = await get_error_resp_frontend_origin()

        # Find the log entry
        log = next(log for log in cap_logs if log.get("path") == resp.url.path)

        assert log.get("method") == "POST"


async def test_healthcheck_not_logged(client: AsyncClient, health_url: str) -> None:
    with mock_aws(), capture_logs() as cap_logs:
        resp = await client.get(health_url)
        assert not any(
            # Check the path component (i.e. /api/healthcheck)
            str(log.get("path")).startswith(resp.url.path)
            for log in cap_logs
        )
