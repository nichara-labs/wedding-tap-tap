from datetime import datetime
from typing import TYPE_CHECKING, Literal
from uuid import UUID

from sqlalchemy import Column, DateTime, ForeignKey, Table, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.schema.base import Base

if TYPE_CHECKING:
    from .chat import Chat
    from .user import User

MessageRole = Literal["user", "assistant", "system"]


genre_story_association = Table(
    "genre_story",
    Base.metadata,
    Column(
        "story_id", Uuid, ForeignKey("story.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "genre_id", Uuid, ForeignKey("genre.id", ondelete="CASCADE"), primary_key=True
    ),
)


class Story(Base):
    """A story which can be used as a base to play from."""

    __tablename__ = "story"

    title: Mapped[str]
    description: Mapped[str]
    prompt: Mapped[str]
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("user.id"))
    """The user who created the story. May be None, if the user who created this story deleted their account."""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=None, index=True
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, index=True
    )

    # Relationships
    user: Mapped["User | None"] = relationship(back_populates="stories", init=False)
    chats: Mapped[list["Chat"]] = relationship(back_populates="story", init=False)
    genres: Mapped[list["Genre"]] = relationship(
        secondary=genre_story_association,
        back_populates="stories",
        init=False,
        cascade="all, delete",
    )


class Genre(Base):
    """A story genre that can be attached to one or more stories."""

    __tablename__ = "genre"

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]

    # Relationships
    stories: Mapped[list["Story"]] = relationship(
        secondary=genre_story_association,
        back_populates="genres",
        init=False,
        passive_deletes=True,
    )
