from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from structlog.stdlib import get_logger

from app.api.utils import get_route_prefix
from app.app.dependencies import (
    SessionDataDep,
    SettingsDep,
)
from app.typedefs import SessionData

router = APIRouter(prefix=get_route_prefix(), tags=["auth"])

_log = get_logger(__name__)


@router.get("/me")
async def me(session: SessionDataDep) -> SessionData:
    """Return user information if the user is logged in, else 401."""
    return session


@router.get("/logout")
async def logout(request: Request, settings: SettingsDep) -> RedirectResponse:
    """Log out the user from this app and return them to the frontend homepage. Note: this is not a front-channel logout."""
    request.session.pop(settings.session.user_data_key, None)
    return RedirectResponse(str(settings.app.frontend_app_url))
