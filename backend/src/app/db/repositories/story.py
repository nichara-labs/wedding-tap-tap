from uuid import UUID

from app.db.repositories import ChatRepo
from app.db.schema import Chat, Story

from .base import BaseRepo


class StoryRepo(BaseRepo[Story]):
    @property
    def _model(self) -> type[Story]:
        return Story

    async def get_by_chat_id(self, chat_id: UUID) -> Story:
        """Get the story associated with a chat."""
        return (
            await ChatRepo(self.session).get_by_field_or_raise(
                lambda c: c.id == chat_id, eager_load=[Chat.story]
            )
        ).story
