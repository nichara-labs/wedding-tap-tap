from typing import TYPE_CHECKING, Annotated, TypedDict, Unpack

from fastapi import Depends

if TYPE_CHECKING:
    from openai import AsyncOpenAI

    from app.db.session import DatabaseSessionManager
    from app.services.oauth.google import GoogleProvider


class AppStateNotSetError(Exception):
    """Raised when the app state is not set before it is accessed."""


class _AppStateArgs(TypedDict):
    db_session_manager: DatabaseSessionManager
    google_provider: GoogleProvider
    llm: AsyncOpenAI


class _AppState:
    """Contains singleton instances that are initialized at startup and are available to all routes as dependencies."""

    def __init__(self, **kwargs: Unpack[_AppStateArgs]) -> None:
        self.db_session_manager = kwargs["db_session_manager"]
        self.google_provider = kwargs["google_provider"]
        self.llm = kwargs["llm"]


class _StateDict(TypedDict):
    state: None | _AppState


_vars: _StateDict = {"state": None}


def _get_app_state() -> _AppState:
    state = _vars["state"]
    if not state:
        raise AppStateNotSetError
    return state


AppStateDep = Annotated[_AppState, Depends(_get_app_state)]
