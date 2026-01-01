from app.settings._ssm_parameter import SsmParameter

from .base import BaseProviderSettings


class GoogleProviderSettings(BaseProviderSettings):
    """
    Google OAuth 2.0 provider configuration.

    See parameters here https://developers.google.com/identity/openid-connect/openid-connect
    """

    name: str = "google"
    client_secret: SsmParameter[str]
