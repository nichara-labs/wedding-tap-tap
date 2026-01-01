from datetime import datetime
from typing import Annotated, Self
from uuid import UUID

from pydantic import BaseModel, StringConstraints

from app.db.schema import Chat
from app.db.schema.chat import ChatStatus


class ChatModel(BaseModel):
    id: UUID
    title: str | None
    story_id: UUID
    updated_at: datetime
    status: ChatStatus
    created_at: datetime

    @classmethod
    def from_chat(cls, chat: Chat) -> Self:
        return cls(
            id=chat.id,
            title=chat.title,
            story_id=chat.story_id,
            updated_at=chat.updated_at,
            status=chat.status,
            created_at=chat.created_at,
        )


class ChatWithStoryModel(BaseModel):
    id: UUID
    title: str | None
    story_id: UUID
    updated_at: datetime
    status: ChatStatus
    created_at: datetime
    story_title: str

    @classmethod
    def from_chat(cls, chat: Chat, story_title: str) -> Self:
        return cls(
            id=chat.id,
            title=chat.title,
            story_id=chat.story_id,
            updated_at=chat.updated_at,
            status=chat.status,
            created_at=chat.created_at,
            story_title=story_title,
        )


class CreateChatRequest(BaseModel):
    story_id: UUID


class UpdateChatRequest(BaseModel):
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
