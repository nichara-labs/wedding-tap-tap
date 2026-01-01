import pytest

from app.db.repositories import UserRepo
from app.services.oauth.typedefs import UserInfo

pytestmark = pytest.mark.anyio


class TestUserRepo:
    async def test_get_or_create(self, user_repo: UserRepo) -> None:
        """Test that we can create a non-existent user, and that we can fetch that user."""
        sub = "123"
        email = "test@test.com"
        assert await user_repo.get_by_field(lambda u: u.sub == sub) is None

        # Create the user
        await user_repo.get_or_create(
            new_user_bonus=100,
            provider="google",
            user_info=UserInfo(
                sub=sub,
                email=email,
                email_verified=True,
                name="Test User",
                picture=None,
            ),
        )

        # Fetch the created user and verify fields
        user = await user_repo.get_or_create(
            new_user_bonus=100,
            provider="google",
            user_info=UserInfo(
                sub=sub,
                email=email,
                email_verified=True,
                name="Test User",
                picture=None,
            ),
        )
        assert user.provider == "google"
        assert user.sub == sub
        assert user.email == email
