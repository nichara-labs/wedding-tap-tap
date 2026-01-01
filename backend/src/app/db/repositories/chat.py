from uuid import UUID

from sqlalchemy.orm import InstrumentedAttribute

from app.db.repositories.base import BaseRepo
from app.db.schema import Chat


class ChatRepo(BaseRepo[Chat]):
    """Repository helpers for `Chat` models."""

    @property
    def _model(self) -> type[Chat]:
        return Chat

    async def get_for_user_or_raise(
        self,
        chat_id: UUID,
        user_id: UUID,
        eager_load: list[InstrumentedAttribute] | None = None,
    ) -> Chat:
        return await self.get_by_field_or_raise(
            lambda c: [c.id == chat_id, c.user_id == user_id], eager_load=eager_load
        )
