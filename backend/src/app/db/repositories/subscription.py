from uuid import UUID

from structlog import getLogger

from app.db.schema import Subscription
from app.models import SubscriptionStatus

from .base import BaseRepo

_log = getLogger(__name__)


class SubscriptionRepo(BaseRepo[Subscription]):
    @property
    def _model(self) -> type[Subscription]:
        return Subscription

    async def get_active_subscription(self, user_id: UUID) -> SubscriptionStatus | None:
        """Return the active subscription for a user, if present."""

        sub = await self.get_by_field(lambda s: s.user_id == user_id)
        if not sub or not sub.is_active:
            return None
        return SubscriptionStatus(
            product=sub.product,
            current_period_end=sub.current_period_end,
            cancel_at_period_end=sub.cancel_at_period_end,
        )
