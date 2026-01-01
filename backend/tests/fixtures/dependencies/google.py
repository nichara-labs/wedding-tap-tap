from typing import Any

import pytest
from authlib.integrations.starlette_client.apps import StarletteOAuth2App
from fastapi import Request
from starlette.responses import RedirectResponse

from app.services.oauth.base import BaseOAuthProvider
from app.services.oauth.google import GoogleProvider
from app.settings import Settings
from app.settings.groups.oauth.google import GoogleProviderSettings

pytestmark = pytest.mark.anyio


class FakeClient(StarletteOAuth2App):
    async def authorize_redirect(
        self,
        request: Request,  # noqa: ARG002
        redirect_uri: str | None = None,
        **_kwargs: Any,
    ) -> RedirectResponse:
        return RedirectResponse(redirect_uri or "http://redirect")

    async def load_server_metadata(self) -> dict[str, Any]:
        return {
            "end_session_endpoint": "http://end_session",
            "token_endpoint": "http://token",
        }


class FakeGoogleProvider(GoogleProvider):
    def __init__(self, settings: GoogleProviderSettings) -> None:
        self._fake_client = FakeClient(settings.name)
        super().__init__(settings)

    @property
    def client(self) -> StarletteOAuth2App:
        """Fake client with caching."""
        return self._fake_client


@pytest.fixture
def google_provider(settings: Settings) -> BaseOAuthProvider:
    return FakeGoogleProvider(settings.auth.google)
