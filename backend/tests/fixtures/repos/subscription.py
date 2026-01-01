from datetime import UTC, datetime, timedelta
from typing import Protocol
from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from uuid6 import uuid7

from app.db.repositories import SubscriptionRepo
from app.db.schema import Subscription

pytestmark = pytest.mark.anyio


class SubscriptionFactory(Protocol):
    """Create a subscription for the specified user."""

    async def __call__(self, user_id: UUID) -> Subscription: ...


@pytest.fixture
def subscription_repo(db_session: AsyncSession) -> SubscriptionRepo:
    return SubscriptionRepo(db_session)


@pytest.fixture
def subscription_factory(subscription_repo: SubscriptionRepo) -> SubscriptionFactory:
    async def _subscription_factory(user_id: UUID) -> Subscription:
        subscription = await subscription_repo.create_or_update(
            Subscription(
                user_id=user_id,
                stripe_customer_id=uuid7().hex,
                product="pro",
                stripe_subscription_id=uuid7().hex,
                current_period_start=datetime.now(UTC) - timedelta(days=15),
                current_period_end=datetime.now(UTC) + timedelta(days=15),
                cancel_at_period_end=False,
                created_at=datetime.now(UTC) - timedelta(days=15),
            )
        )
        await subscription_repo.session.commit()
        return subscription

    return _subscription_factory
