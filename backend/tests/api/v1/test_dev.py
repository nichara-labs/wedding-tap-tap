import pytest
from fastapi.routing import APIRoute

from app.entrypoint import create_app
from app.settings import Settings
from app.typedefs.env import Environment

pytestmark = pytest.mark.anyio


@pytest.fixture
def login_url() -> str:
    return "/v1/dev/login"


@pytest.fixture
def prod_settings(settings: Settings) -> Settings:
    copy = settings.model_copy(deep=True)
    copy.app.env = Environment.prod
    return copy


async def test_dev_login_in_local(settings: Settings, login_url: str) -> None:
    assert settings.app.env == Environment.local
    app = create_app(settings)
    route = next(
        r for r in app.routes if isinstance(r, APIRoute) and r.path == login_url
    )
    assert route is not None


async def test_dev_login_404_in_prod(
    prod_settings: Settings,
    login_url: str,
) -> None:
    """Test that the dev login endpoint is not available in production."""
    app = create_app(prod_settings)
    with pytest.raises(StopIteration):
        next(r for r in app.routes if isinstance(r, APIRoute) and r.path == login_url)
