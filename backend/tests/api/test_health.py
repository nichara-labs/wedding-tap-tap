import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from moto import mock_aws

from app.api.route_map import RouteMap
from app.api.v1.healthz import HealthCheckModel
from app.settings import Settings

pytestmark = pytest.mark.anyio


@pytest.fixture
def health_url(app: FastAPI) -> str:
    return app.url_path_for(RouteMap.HEALTHZ)


async def test_health(client: AsyncClient, health_url: str, settings: Settings) -> None:
    """Test that the healthcheck works."""
    with mock_aws():
        response = await client.get(health_url)
        assert response.status_code == 200
        assert (
            HealthCheckModel.model_validate_json(response.content).environment
            == settings.app.env
        )
