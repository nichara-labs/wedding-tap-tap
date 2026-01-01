from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse
from structlog.stdlib import get_logger

from app.api.route_map import RouteMap
from app.api.utils import get_route_prefix, make_uri
from app.app.dependencies import (
    AppDep,
    DbSessionDep,
    GoogleProviderDep,
    SettingsDep,
)
from app.db.repositories.user import UserRepo
from app.services.oauth.typedefs import UserInfo
from app.typedefs import SessionData

_log = get_logger(__name__)

router = APIRouter(prefix=get_route_prefix(), tags=["auth"])


@router.get("/authorize")
async def authorize(
    request: Request, registry: GoogleProviderDep, app: AppDep, settings: SettingsDep
) -> RedirectResponse:
    """Redirect user to the provider's OAuth login for authorization."""
    redirect_uri = make_uri(settings, app.url_path_for(RouteMap.GOOGLE_CALLBACK))
    return await registry.get_redirect_response(request, redirect_uri)


@router.get("/callback", name=RouteMap.GOOGLE_CALLBACK)
async def google(
    request: Request,
    provider: GoogleProviderDep,
    db: DbSessionDep,
    settings: SettingsDep,
) -> Response:
    """Process the OAuth callback from the provider, mark user as logged in and redirect user-agent to the frontend."""

    access_token = await provider.get_access_token(request)

    user_info = provider.get_user_info(access_token)

    users = UserRepo(db)

    user = await users.get_or_create(
        new_user_bonus=settings.llm.new_user_bonus_lorestones,
        provider="google",
        user_info=UserInfo(
            sub=user_info.sub,
            email=user_info.email,
            email_verified=user_info.email_verified,
            name=user_info.name,
            picture=user_info.picture,
        ),
    )
    request.session[settings.session.user_data_key] = SessionData.from_user(
        user
    ).model_dump(mode="json")

    _log.info("User logged in", email=user_info.email, name=user_info.name)

    return RedirectResponse(str(settings.app.frontend_app_url))
