from datetime import datetime
from typing import TYPE_CHECKING, Literal
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base

if TYPE_CHECKING:
    from .message import Message
    from .story_genre import Story
    from .user import User

ChatStatus = Literal["in_progress", "completed", "failed", "not_started"]


class Chat(Base):
    """
    Represents a chat based off a story.

    Note that the system/story prompt will not be updated in an existing chat.
    """

    __tablename__ = "chat"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    story_id: Mapped[UUID] = mapped_column(ForeignKey("story.id"))
    title: Mapped[str | None] = mapped_column(default=None)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=None, index=True
    )
    status: Mapped[ChatStatus] = mapped_column(default="not_started", index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=None
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="chats", init=False)
    story: Mapped["Story"] = relationship(back_populates="chats", init=False)
    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat", init=False, cascade="all, delete-orphan"
    )
