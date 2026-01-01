from openai import AsyncOpenAI

from app.app.dependencies._state import _AppState, _vars
from app.db.session import DatabaseSessionManager
from app.services.oauth.google import GoogleProvider
from app.settings import (
    Settings,
)


async def init_dependencies(settings: Settings) -> None:
    """Initialize dependencies."""
    # Initialize individual components
    db_manager = DatabaseSessionManager.from_settings(settings.db)
    google_provider = GoogleProvider(settings.auth.google)
    llm = AsyncOpenAI(
        base_url=settings.llm.base_url,
        api_key=settings.llm.api_key.value.get_secret_value(),
    )

    # Create AppState with initialized components
    _vars["state"] = _AppState(
        db_session_manager=db_manager, google_provider=google_provider, llm=llm
    )
