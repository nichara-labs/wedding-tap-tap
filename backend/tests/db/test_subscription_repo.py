from datetime import UTC, datetime, timedelta
from uuid import UUID

import pytest
from uuid6 import uuid7

from app.db.repositories import UserRepo
from app.db.schema import Subscription, User

pytestmark = pytest.mark.anyio


def create_sub(user_id: UUID) -> Subscription:
    return Subscription(
        user_id=user_id,
        stripe_customer_id=uuid7().hex,
        product="pro",
        stripe_subscription_id=uuid7().hex,
        current_period_start=datetime.now(UTC) - timedelta(days=15),
        current_period_end=datetime.now(UTC) + timedelta(days=15),
        cancel_at_period_end=False,
        created_at=datetime.now(UTC) - timedelta(days=15),
    )


class TestSubscriptionRepo:
    async def test_assign_new_subscription(
        self, user: User, user_repo: UserRepo
    ) -> None:
        """Tests that we can assign a subscription when user.subscription is None."""
        assert user.subscription is None

        sub = create_sub(user.id)
        user.subscription = sub

        _user = await user_repo.create_or_update(user)
        assert _user.subscription is not None

    async def test_update_subscription_in_place(
        self,
        user_with_subscription: User,
        user_repo: UserRepo,
    ) -> None:
        """Tests that we can update a subscription in-place when one already exists."""
        _user = user_with_subscription
        old_sub = _user.subscription
        assert old_sub is not None

        # Replace the subscription
        new_sub = create_sub(_user.id)
        _user.subscription = new_sub
        updated_user = await user_repo.create_or_update(_user)
        updated_sub = updated_user.subscription

        assert updated_sub is not None
        assert updated_sub.stripe_subscription_id == new_sub.stripe_subscription_id
        assert old_sub.stripe_subscription_id != updated_sub.stripe_subscription_id
