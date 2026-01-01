import pytest
from sqlalchemy.exc import MissingGreenlet
from uuid6 import uuid7

from app.db.repositories import UserRepo
from app.db.repositories.base import (
    MultipleObjectsReturnedError,
    ObjectNotFoundError,
)
from app.db.schema import User
from tests.fixtures.repos.story import StoryFactory
from tests.fixtures.repos.user import UserFactory

pytestmark = pytest.mark.anyio


class TestGetByField:
    """Tests for the base repository class. The User object is used."""

    async def test_exists(self, user_repo: UserRepo, user: User) -> None:
        fetched_user = await user_repo.get_by_field(lambda u: u.id == user.id)
        assert fetched_user is not None
        assert fetched_user.id == user.id
        assert fetched_user.email == user.email

    async def test_does_not_exist(self, user_repo: UserRepo) -> None:
        # Non-existent UUID
        assert await user_repo.get_by_field(lambda u: u.id == uuid7()) is None

    async def test_multiple_clauses(self, user_repo: UserRepo, user: User) -> None:
        fetched_user = await user_repo.get_by_field(
            lambda u: [u.id == user.id, u.email == user.email]
        )
        assert fetched_user is not None
        assert fetched_user.id == user.id
        assert fetched_user.email == user.email

    async def test_multiple_clauses_does_not_exist(self, user_repo: UserRepo) -> None:
        assert (
            await user_repo.get_by_field(
                lambda u: [u.id == uuid7(), u.email == "non-existent@email.com"]
            )
            is None
        )

    async def test_raises_if_multiple(
        self, user_repo: UserRepo, user_factory: UserFactory
    ) -> None:
        [await user_factory() for _ in range(2)]
        with pytest.raises(
            MultipleObjectsReturnedError, match="Multiple User objects returned"
        ):
            await user_repo.get_by_field(lambda _: [])

    async def test_eager(
        self,
        story_factory: StoryFactory,
        user_factory: UserFactory,
        user_repo: UserRepo,
    ) -> None:
        """Test that we can fetch attributes via selectinload when eager attributes are passed"""
        user = await user_factory()
        story = await story_factory(
            user_id=user.id, title="Test", description="Test", prompt="Test"
        )
        user = story.user
        assert user is not None

        # Reload the user with eager_load
        loaded_user = await user_repo.get_by_field_or_raise(
            lambda u: u.id == user.id, eager_load=[User.stories]
        )
        assert loaded_user.stories is not None

    async def test_no_eager_loading(
        self,
        story_factory: StoryFactory,
        user_factory: UserFactory,
        user_repo: UserRepo,
    ) -> None:
        """Test that fetching related attributes (i.e. where another record's foreign key points to this record's primary key, such as User.chats or AsyncSagemakerJob.transcript) without eager loading raises an error"""

        user = await user_factory()
        story = await story_factory(
            user_id=user.id, title="Test", description="Test", prompt="Test"
        )
        user = story.user
        assert user is not None

        # Reload the user WITHOUT eager_load
        loaded_user = await user_repo.get_by_field_or_raise(lambda u: u.id == user.id)
        with pytest.raises(MissingGreenlet):
            assert loaded_user.stories is not None


class TestGetByFieldOrRaise:
    async def test_raises_with_non_existent_id(self, user_repo: UserRepo) -> None:
        non_existent_id = uuid7()
        with pytest.raises(ObjectNotFoundError, match="User not found"):
            assert await user_repo.get_by_field_or_raise(
                lambda u: u.id == non_existent_id
            )

    async def test_no_raise_when_exists(self, user_repo: UserRepo, user: User) -> None:
        fetched_user = await user_repo.get_by_field_or_raise(lambda u: u.id == user.id)
        assert fetched_user is not None


class TestGetByFieldMultiple:
    async def test_get_multiple(
        self, user_repo: UserRepo, user_factory: UserFactory
    ) -> None:
        """Test that we can fetch multiple users."""
        [await user_factory() for _ in range(2)]
        _users = await user_repo.get_by_field_multiple(lambda _: [])
        assert len(_users) == 2


class TestGetOrCreate:
    async def test_create_no_eager(self, user_repo: UserRepo) -> None:
        """Test that attempting to access non-eagerly loaded relations raises an error."""
        user = await user_repo.create_or_update(
            User(
                sub=uuid7().hex,
                email=uuid7().hex,
                email_verified=True,
                name="Test User",
                provider="google",
            )
        )
        with pytest.raises(MissingGreenlet):
            assert user.chats == []

    async def test_create_eager(self, user_repo: UserRepo) -> None:
        """Test that attempting to access eagerly loaded relations works."""
        user = await user_repo.create_or_update(
            User(
                sub=uuid7().hex,
                email=uuid7().hex,
                email_verified=True,
                name="Test User",
                provider="google",
            ),
            eager_load=[User.chats],
        )
        assert user.chats == []

    async def test_update(self, user_repo: UserRepo, user: User) -> None:
        """Test that we can update a user."""
        new_email = "changed@test.com"
        user.email = new_email

        # Commit the update
        new_user = await user_repo.create_or_update(user)

        # Check
        assert (
            await user_repo.get_by_field_or_raise(lambda u: u.id == new_user.id)
        ).email == new_email


class TestDelete:
    async def test_delete(self, user_repo: UserRepo, user: User) -> None:
        await user_repo.delete(user)
        assert await user_repo.get_by_field(lambda u: u.id == user.id) is None
