import pytest

from app.services.oauth.google import GoogleProvider

pytestmark = pytest.mark.anyio


class TestOAuthRegistry:
    @pytest.fixture(autouse=True)
    def _fixtures(self, google_provider: GoogleProvider) -> None:
        self.registry = google_provider

    def test_client_is_cached(self) -> None:
        """Test that the internal call to `client` is cached."""
        client = self.registry.client
        client2 = self.registry.client
        assert client is client2
