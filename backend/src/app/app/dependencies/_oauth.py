from typing import Annotated

from fastapi import Depends

from app.services.oauth.google import GoogleProvider

from ._state import AppStateDep


async def _get_google_provider(app_state: AppStateDep) -> GoogleProvider:
    """Get the Google OAuth provider from the app state."""
    return app_state.google_provider


GoogleProviderDep = Annotated[GoogleProvider, Depends(_get_google_provider)]
