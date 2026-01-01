from abc import ABC, abstractmethod
from typing import Any

from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client.apps import StarletteOAuth2App
from authlib.oauth2.rfc6749.wrappers import OAuth2Token
from fastapi import Request
from starlette.responses import RedirectResponse

from app.settings.groups.oauth.base import BaseProviderSettings


class BaseOAuthProvider(ABC):
    def __init__(self, settings: BaseProviderSettings, **client_kwargs: Any) -> None:
        """Initialize the provider."""
        self.settings = settings
        self.oauth = OAuth()
        self.oauth.register(
            name=settings.name,
            server_metadata_url=settings.configuration_endpoint,
            client_id=settings.client_id,
            **client_kwargs,
        )

    @abstractmethod
    async def get_redirect_response(
        self, request: Request, redirect_uri: str
    ) -> RedirectResponse:
        """Construct the redirect response for the authorization endpoint with the requested scopes."""

    @abstractmethod
    async def get_access_token(
        self, request: Request, **client_kwargs: Any
    ) -> OAuth2Token:
        """
        Exchange authorization code from the request for an access token.

        The `id_token` containing information from the UserInfo endpoint is [included](https://docs.authlib.org/en/latest/client/frameworks.html#parsing-id-token).

        Note: As per the RFC, the access_token is meant to be opaque to the client and no parsing should be attempted.
        """

    @property
    def client(self) -> StarletteOAuth2App:
        # This method returns a cached copy of the client if it exists, otherwise it creates a new one.
        client = self.oauth.create_client(self.settings.name)
        if client is None:
            msg = f"Client '{self.settings.name}' not found in OAuth registry"
            raise ValueError(msg)
        return client
