"""Stripe payment settings."""

from pydantic import Field, SecretStr

from app.settings._base import BaseModelNoExtra
from app.settings._ssm_parameter import SsmParameter


class StripeSettings(BaseModelNoExtra):
    """Stripe payment integration settings."""

    api_key: SsmParameter[SecretStr] = Field(
        description="Stripe secret key for API authentication"
    )
    webhook_secret: SsmParameter[SecretStr] = Field(
        description="Stripe webhook secret for signature verification"
    )
    pro_product_id: str = Field(
        description="Stripe product ID for the Pro subscription. If it is present in any item in a user's Stripe Subscription, they will be considered a Pro user.",
        min_length=1,
    )
    pro_product_price: str = Field(
        description="Stripe product price ID for the Pro subscription.",
        min_length=1,
    )
