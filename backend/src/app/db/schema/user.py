from datetime import datetime
from typing import TYPE_CHECKING, Literal

from sqlalchemy import DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base

if TYPE_CHECKING:
    from .chat import Chat
    from .lorestone_transaction import LorestoneTransaction
    from .message import Message
    from .story_genre import Story
    from .subscription import Subscription


Provider = Literal["google", "email"]


class User(Base):
    __tablename__ = "user"

    __table_args__ = (UniqueConstraint("provider", "sub", name="uq_user_provider_sub"),)

    name: Mapped[str]
    email: Mapped[str]
    email_verified: Mapped[bool]
    provider: Mapped[Provider]
    sub: Mapped[str] = mapped_column(unique=True, index=True)
    """Note: for the email provider, this is the user's email address."""
    picture: Mapped[str | None] = mapped_column(default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=None
    )

    # Relationships
    subscription: Mapped["Subscription | None"] = relationship(
        back_populates="user",
        init=False,
        cascade="all, delete-orphan",
    )
    chats: Mapped[list["Chat"]] = relationship(
        back_populates="user",
        init=False,
        cascade="all, delete-orphan",
    )
    lorestone_transactions: Mapped[list["LorestoneTransaction"]] = relationship(
        back_populates="user",
        init=False,
        cascade="all, delete-orphan",
    )
    messages: Mapped[list["Message"]] = relationship(
        back_populates="user",
        init=False,
        cascade="all, delete-orphan",
    )
    stories: Mapped[list["Story"]] = relationship(back_populates="user", init=False)
