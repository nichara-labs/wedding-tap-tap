from collections.abc import Callable, Coroutine
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories import UserRepo
from app.db.schema import User

from .subscription import SubscriptionFactory

type UserFactory = Callable[[], Coroutine[None, None, User]]

pytestmark = pytest.mark.anyio


@pytest.fixture
async def user_repo(db_session: AsyncSession) -> UserRepo:
    return UserRepo(db_session)


@pytest.fixture
async def user(user_factory: UserFactory) -> User:
    """Creates and returns a new user."""
    return await user_factory()


@pytest.fixture
def user_factory(user_repo: UserRepo) -> UserFactory:
    async def _user_factory() -> User:
        user = await user_repo.create_or_update(
            User(
                name=uuid4().hex,
                email=f"{uuid4().hex}@example.com",
                email_verified=True,
                provider="google",
                sub=uuid4().hex,
            ),
            # Eager load all properties
            eager_load=[User.subscription],
        )
        await user_repo.session.commit()
        return user

    return _user_factory


@pytest.fixture
async def user_with_subscription(
    user: User,
    subscription_factory: SubscriptionFactory,
    user_repo: UserRepo,
) -> User:
    """A user with an active subscription"""
    await subscription_factory(user.id)
    await user_repo.session.refresh(user, attribute_names=["subscription"])
    return user
