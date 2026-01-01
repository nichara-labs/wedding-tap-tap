from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from structlog.stdlib import get_logger

from app.db.schema import Message
from app.db.schema.message import MessageRole

from .base import BaseRepo, ObjectNotFoundError

_log = get_logger(__name__)


class MessageRepo(BaseRepo[Message]):
    @property
    def _model(self) -> type[Message]:
        return Message

    @classmethod
    def root_to_leaf(cls, leaf: Message, messages: Sequence[Message]) -> list[Message]:
        """Build a message chain from a leaf message up to the root, returning a list of Messages in chronological order."""
        tree = [leaf]
        current = leaf
        while current.parent_id:
            parent = next((m for m in messages if m.id == current.parent_id), None)
            if not parent:
                break
            tree.append(parent)
            current = parent
        tree.reverse()
        return tree

    async def get_first_message_by_type_or_raise(
        self,
        chat_id: UUID,
        user_id: UUID,
        allowed_types: Sequence[MessageRole] = (
            "user",
            "assistant",
        ),
    ) -> Message:
        """Return the oldest message in a chat which matches the alllowed type."""
        stmt = (
            select(self._model)
            .where(self._model.chat_id == chat_id)
            .where(self._model.user_id == user_id)
            .where(self._model.role.in_(allowed_types))
            .order_by(self._model.created_at.asc())
        )
        res = await self.session.scalar(stmt)
        if not res:
            msg = f"No {self._model.__name__} found matching the query"
            await _log.aerror(
                msg, chat_id=chat_id, user_id=user_id, allowed_types=allowed_types
            )
            raise ObjectNotFoundError(msg)
        return res
