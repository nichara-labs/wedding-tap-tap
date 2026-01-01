from typing import Any, override

from authlib.oauth2.rfc6749.wrappers import OAuth2Token
from fastapi import Request
from starlette.responses import RedirectResponse

from app.services.oauth.typedefs import UserInfo
from app.settings.groups.oauth.google import GoogleProviderSettings

from .base import BaseOAuthProvider


class GoogleProvider(BaseOAuthProvider):
    """Google OAuth 2.0 provider."""

    scopes = ("openid", "email", "profile")

    def __init__(self, settings: GoogleProviderSettings) -> None:
        self.settings = settings
        super().__init__(settings)

    @override
    async def get_redirect_response(
        self, request: Request, redirect_uri: str
    ) -> RedirectResponse:
        return await self.client.authorize_redirect(
            request,
            redirect_uri,
            scope=" ".join(self.scopes),
            prompt="select_account",  # Always let the user select the account
        )

    @override
    async def get_access_token(
        self, request: Request, **client_kwargs: Any
    ) -> OAuth2Token:
        return await self.client.authorize_access_token(
            request, client_secret=self.settings.client_secret.value, **client_kwargs
        )

    def get_user_info(self, token: OAuth2Token) -> UserInfo:
        user_info = token["userinfo"]
        if not isinstance(user_info, dict):
            msg = "No user_info in token"
            raise TypeError(msg)
        return UserInfo(
            email=user_info["email"],
            email_verified=user_info["email_verified"],
            sub=user_info["sub"],
            name=user_info["name"],
            picture=user_info.get("picture"),
        )
