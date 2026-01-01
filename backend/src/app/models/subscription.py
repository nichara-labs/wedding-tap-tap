from datetime import datetime

from pydantic import BaseModel

from app.db.schema.subscription import Product


class SubscriptionStatus(BaseModel):
    """An active subscription."""

    product: Product
    """Product the user is subscribed to."""
    current_period_end: datetime
    cancel_at_period_end: bool
    """Whether the user's subscription is set to auto renew, or will be cancelled once the current subscription period is over."""
