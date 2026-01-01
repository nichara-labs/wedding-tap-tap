from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Query, Request
from pydantic import BaseModel
from structlog.stdlib import get_logger

from app.api.utils import get_route_prefix
from app.app.dependencies import DbSessionDep, SettingsDep
from app.db.repositories import UserRepo
from app.db.schema.user import Provider
from app.services.oauth.typedefs import UserInfo
from app.typedefs import SessionData

_log = get_logger(__name__)

router = APIRouter(prefix=get_route_prefix(), tags=["dev"])


class _DevLoginParams(BaseModel):
    sub: str | None = None
    email: str | None = None
    name: str | None = None
    provider: Provider


@router.post("/login")
async def login(
    request: Request,
    settings: SettingsDep,
    db: DbSessionDep,
    params: Annotated[_DevLoginParams, Query()],
) -> SessionData:
    """Login as a user (testing only)."""
    users = UserRepo(db)
    user = await users.get_or_create(
        new_user_bonus=settings.llm.new_user_bonus_lorestones,
        provider=params.provider,
        user_info=UserInfo(
            email=params.email or uuid4().hex,
            email_verified=True,
            name=params.name or uuid4().hex,
            sub=params.sub or uuid4().hex,
        ),
    )
    session_data = SessionData.from_user(user)
    request.session[settings.session.user_data_key] = session_data.model_dump(
        mode="json"
    )
    return session_data


@router.post("/error")
async def error() -> None:
    """Raise an internal server error (RuntimeError). Used to test HTTP 500 responses."""
    msg = "Test error"
    raise ValueError(msg)


@router.get("/echo")
async def echo_get(param: str) -> str:
    """Echo back the value of the query parameter."""
    return param


class _EchoPostParams(BaseModel):
    param: str


@router.post("/echo")
async def echo_post(param: _EchoPostParams) -> str:
    """Echo back the value of the query parameter."""
    return param.param


@router.delete("/echo")
async def echo_delete(param: str) -> str:
    """Echo back the value of the query parameter."""
    return param
