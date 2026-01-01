from abc import ABC
from datetime import datetime
from typing import Literal, Self
from uuid import UUID

from pydantic import BaseModel

from app.db.schema import Message
from app.db.schema.message import MessageRole, MessageStatus

_EventType = Literal["delta", "usage"]


class MessageModel(BaseModel):
    id: UUID
    chat_id: UUID
    role: MessageRole
    status: MessageStatus
    content: str
    created_at: datetime
    parent: UUID | None
    children: list[UUID]

    @classmethod
    def from_message(cls, message: Message) -> Self:
        return cls(
            id=message.id,
            chat_id=message.chat_id,
            status=message.status,
            parent=message.parent_id,
            role=message.role,
            content=message.content,
            created_at=message.created_at,
            children=[c.id for c in message.children],
        )


class _Event(BaseModel, ABC):
    """An event in a server-sent event stream."""

    type_: _EventType

    def serialize_event(self) -> str:
        return f"event: message\ndata: {self.model_dump_json()}\n\n"


class DeltaEvent(_Event):
    type_: _EventType = "delta"
    v: str
    """The chunk content."""
