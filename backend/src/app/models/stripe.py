from pydantic import BaseModel


class StripeCheckoutResponse(BaseModel):
    """Response model for checkout session creation."""

    session_id: str
    url: str


class StripeSessionStatusResponse(BaseModel):
    """Response model for session status retrieval."""

    status: str
    customer_email: str | None
    amount_total: int | None
    currency: str | None
