from cachetools import TTLCache
from fastapi import APIRouter
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.route_map import RouteMap
from app.api.utils import get_route_prefix
from app.app.dependencies import CommitInfoDep, DbSessionDep, SettingsDep
from app.services.aws.client import get_client
from app.settings import AwsSettings
from app.typedefs import Environment

router = APIRouter(prefix=get_route_prefix(), tags=["health"])

_KEY = "healthcheck"
_cache = TTLCache(
    maxsize=1, ttl=7200
)  # Save money for Neon DB by letting it idle for longer


class _AwsStsIdentity(BaseModel):
    UserId: str
    Account: str
    Arn: str


class _Checks(BaseModel):
    aws_identity: _AwsStsIdentity


class HealthCheckModel(BaseModel):
    environment: Environment
    commit_sha: str
    commit_timestamp: float = Field(description="Unix Timestamp (measured in seconds)")


@router.get("", name=RouteMap.HEALTHZ)
async def healthcheck(
    commit_info: CommitInfoDep, settings: SettingsDep, db: DbSessionDep
) -> HealthCheckModel:
    """Checks for DB connectivity."""
    checks = _cache.get(_KEY)
    if checks is None:
        checks = await _checks(settings.aws, db)
        _cache[_KEY] = checks

    return HealthCheckModel(
        environment=settings.app.env,
        commit_sha=commit_info.COMMIT_SHA,
        commit_timestamp=commit_info.COMMIT_TIMESTAMP,
    )


async def _checks(settings: AwsSettings, db: AsyncSession) -> _Checks:
    identity = _AwsStsIdentity.model_validate(
        get_client("sts", settings.region).get_caller_identity()
    )
    await db.execute(text("SELECT 1"))
    return _Checks(aws_identity=identity)
