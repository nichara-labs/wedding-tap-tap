from datetime import datetime
from typing import TYPE_CHECKING, Literal
from uuid import UUID

from sqlalchemy import JSON, CheckConstraint, DateTime, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base

if TYPE_CHECKING:
    from .user import User

TransactionCategory = Literal[
    "new_user_bonus", "daily_bonus", "purchase", "admin_adjustment", "story_generation"
]


class LorestoneTransaction(Base):
    """Lorestone transactions with running balance."""

    __tablename__ = "lorestone_transaction"
    user_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("user.id"), nullable=False, index=True
    )
    balance_before_transaction: Mapped[int] = mapped_column(
        CheckConstraint(
            "balance_before_transaction >= 0",
            name="check_balance_before_transaction_positive",
        )
    )
    balance_after_transaction: Mapped[int] = mapped_column(
        CheckConstraint(
            "balance_after_transaction >= 0",
            name="check_balance_after_transaction_positive",
        )
    )
    amount: Mapped[int]
    category: Mapped[TransactionCategory]
    message_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("message.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        default=None,
    )
    """The message that triggered this transaction, if applicable."""
    additional_info: Mapped[str | None] = mapped_column(JSON, default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=None, index=True
    )

    # Relationships
    user: Mapped["User"] = relationship(
        back_populates="lorestone_transactions", init=False
    )
