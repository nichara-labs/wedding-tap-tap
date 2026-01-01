from datetime import UTC, datetime
from typing import TYPE_CHECKING, Literal
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User

SubscriptionStatus = Literal[
    "active",
    "canceled",
    "incomplete",
    "incomplete_expired",
    "past_due",
    "paused",
    "trialing",
    "unpaid",
]

Product = Literal["pro"]


class Subscription(Base):
    """Mirrors the user's Stripe subscription, if any."""

    __tablename__ = "subscription"
    __table_args__ = (
        # Allow replacing a subscription on a user in the same transaction
        UniqueConstraint(
            "user_id",
            deferrable=True,
            initially="DEFERRED",
        ),
    )

    user_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("user.id"))
    stripe_subscription_id: Mapped[str] = mapped_column(String)
    stripe_customer_id: Mapped[str] = mapped_column(String)
    product: Mapped[Product]
    current_period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    current_period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    cancel_at_period_end: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    """This is taken from the Stripe Subscription object, not on instance creation."""

    # Relationships
    user: Mapped["User"] = relationship(
        back_populates="subscription",
        init=False,
        single_parent=True,
    )

    @property
    def is_active(self) -> bool:
        now = datetime.now(UTC)
        return self.current_period_start <= now <= self.current_period_end
