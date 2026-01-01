import stripe

from app.settings.groups.stripe import StripeSettings


async def add_stripe_api_key(settings: StripeSettings) -> None:
    """Add Stripe API key to the Stripe client."""
    stripe.api_key = settings.api_key.value.get_secret_value()
