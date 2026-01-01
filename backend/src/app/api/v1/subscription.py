from fastapi import APIRouter

from app.api.utils import get_route_prefix
from app.app.dependencies import (
    DbSessionDep,
    RequiresLoginDep,
    SessionDataDep,
)
from app.db.repositories import SubscriptionRepo
from app.models.subscription import SubscriptionStatus

router = APIRouter(
    prefix=get_route_prefix(), tags=["subscription"], dependencies=[RequiresLoginDep]
)


@router.get("/status")
async def get_subscription_status(
    session: SessionDataDep, db: DbSessionDep
) -> SubscriptionStatus | None:
    """Return whether the current user has an active subscription."""
    return await SubscriptionRepo(db).get_active_subscription(session.user_id)
