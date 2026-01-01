from app.settings._base import BaseModelNoExtra
from app.settings.groups.oauth.google import GoogleProviderSettings


class AuthSettings(BaseModelNoExtra):
    google: GoogleProviderSettings
