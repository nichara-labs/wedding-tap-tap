from datetime import datetime
from typing import TYPE_CHECKING, Literal
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.schema.base import Base

if TYPE_CHECKING:
    from .chat import Chat
    from .user import User

MessageRole = Literal["user", "assistant", "system"]
MessageStatus = Literal["in_progress", "completed", "failed"]


class Message(Base):
    """Represents a chat message sent by the user to the LLM."""

    __tablename__ = "message"

    content: Mapped[str]
    user_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("user.id"))
    chat_id: Mapped[UUID] = mapped_column(ForeignKey("chat.id", ondelete="CASCADE"))
    role: Mapped[MessageRole]
    status: Mapped[MessageStatus] = mapped_column(default="in_progress")
    """Whether more messages are allowed to be sent after this one."""
    parent_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("message.id"), default=None
    )
    """The id of the parent message. The parent is the message immediately preceding this message in a chat. A message may have only one parent, but may have multiple children (for example, if the user edits a message and resends it)."""
    model: Mapped[str | None] = mapped_column(String(100), default=None)
    """The model used to generate the response, if this was an assistant message."""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=None, index=True
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="messages", init=False)
    # https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.remote_side
    parent: Mapped["Message"] = relationship(
        back_populates="children", init=False, remote_side="Message.id"
    )
    children: Mapped[list["Message"]] = relationship(
        back_populates="parent", init=False
    )
    chat: Mapped["Chat"] = relationship(back_populates="messages", init=False)
