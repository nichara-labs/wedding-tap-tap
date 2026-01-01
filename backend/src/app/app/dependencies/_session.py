from typing import Annotated, Any

from fastapi import (
    Depends,
    HTTPException,
    Request,
    WebSocket,
    WebSocketException,
)
from pydantic import ValidationError
from structlog.contextvars import bind_contextvars
from structlog.stdlib import get_logger

from app.typedefs import SessionData

from ._settings import SettingsDep

_logger = get_logger(__name__)


def _get_session_data(request: Request, settings: SettingsDep) -> SessionData:
    """
    Parse session data from the request (the SessionMiddleware has already decrypted it). Also binds parameters to logging context.

    If the user is not logged in, session data is an empty dictionary and so validation will fail with a 401, automatically raised on the route.
    """
    try:
        _raw = request.session[settings.session.user_data_key]
    except KeyError:
        raise HTTPException(status_code=401, detail="User is not logged in") from None
    return _parse(_raw)


def _maybe_get_session_data(
    request: Request, settings: SettingsDep
) -> SessionData | None:
    """Attempt to get session data from the request if it exists."""
    try:
        _raw = request.session[settings.session.user_data_key]
        return _parse(_raw)
    except HTTPException, KeyError:
        return None


def _get_session_data_ws(ws: WebSocket, settings: SettingsDep) -> SessionData:
    """Same as get_session_data, but for websockets."""
    try:
        _raw = ws.session[settings.session.user_data_key]
    except KeyError:
        raise WebSocketException(code=1008, reason="User is not logged in") from None
    return _parse(_raw)


def _parse(raw: Any) -> SessionData:
    try:
        parsed = SessionData.model_validate(raw)
    except ValidationError as e:
        _logger.warning("Failed to parse session data", exc_info=e)
        raise HTTPException(status_code=401, detail="Session data is invalid") from e
    bind_contextvars(
        user_id=parsed.user_id,
        email=parsed.email,
        name=parsed.name,
        provider=parsed.provider,
    )
    return parsed


SessionDataDep = Annotated[SessionData, Depends(_get_session_data)]
MaybeSessionDataDep = Annotated[SessionData | None, Depends(_maybe_get_session_data)]
WsSessionDataDep = Annotated[SessionData, Depends(_get_session_data_ws)]

# Alias
RequiresLoginDep = Depends(_get_session_data)
"""Requires a logged-in user. Alias for SessionDataDep, meant for use in routers to protect routes."""
RequiresLoginDepWs = Depends(_get_session_data_ws)
