from sqlalchemy.orm import InstrumentedAttribute

from app.db.schema import User
from app.db.schema.lorestone_transaction import LorestoneTransaction
from app.db.schema.user import Provider
from app.services.oauth.typedefs import UserInfo

from .base import BaseRepo
from .lorestone_transaction import LorestoneTransactionRepo


class UserRepo(BaseRepo[User]):
    @property
    def _model(self) -> type[User]:
        return User

    async def get_or_create(
        self,
        new_user_bonus: int,
        provider: Provider,
        user_info: UserInfo,
        eager_load: list[InstrumentedAttribute] | None = None,
    ) -> User:
        """
        Get a user by their sub and provider, else create with the provided details.

        If the user is new, also adds lorestones to their account as a welcome bonus.
        """
        user = await self.get_by_field(
            lambda u: [u.provider == provider, u.sub == user_info.sub],
            eager_load=eager_load,
        )
        if user:
            return user

        # New user
        new_user = await self.create_or_update(
            User(
                provider=provider,
                sub=user_info.sub,
                email=user_info.email,
                email_verified=user_info.email_verified,
                name=user_info.name,
                picture=user_info.picture,
            ),
            eager_load=eager_load,
        )
        await LorestoneTransactionRepo(self.session).create_or_update(
            LorestoneTransaction(
                user_id=new_user.id,
                category="new_user_bonus",
                amount=new_user_bonus,
                balance_before_transaction=0,
                balance_after_transaction=new_user_bonus,
            )
        )
        return new_user
