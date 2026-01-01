import pytest
from httpx import AsyncClient

from tests.fixtures.common import ClientWithLogin

pytestmark = pytest.mark.anyio


@pytest.fixture
def logout_url() -> str:
    return "/v1/auth/logout"


@pytest.fixture
def me_url() -> str:
    return "/v1/auth/me"


async def test_logout_without_login_does_not_raise(
    client: AsyncClient, logout_url: str
) -> None:
    """Test that a client that is not logged in, can still logout without raising an error."""
    assert (await client.get(logout_url)).status_code == 307


async def test_initiate_logout_clears_cookies(
    client_with_login: ClientWithLogin, logout_url: str, me_url: str
) -> None:
    """Test that the initiate logout clears cookies."""
    client = client_with_login["client"]
    await client.get(logout_url)
    assert (await client.get(me_url)).status_code == 401
