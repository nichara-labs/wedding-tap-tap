"""Stripe payment integration endpoints."""

from datetime import UTC, datetime
from typing import Any, cast
from uuid import UUID

import stripe
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool
from structlog.contextvars import bind_contextvars
from structlog.stdlib import get_logger

from app.api.utils import get_route_prefix
from app.app.dependencies import SettingsDep
from app.app.dependencies._db import DbSessionDep
from app.app.dependencies._session import SessionDataDep
from app.db.repositories import UserRepo
from app.db.repositories.subscription import SubscriptionRepo
from app.db.schema import Subscription, User
from app.models import StripeCheckoutResponse

_log = get_logger(__name__)

router = APIRouter(prefix=get_route_prefix(), tags=["Stripe Payments"])


@router.post("/checkout")
async def create_checkout_session(
    settings: SettingsDep, session_data: SessionDataDep, db: DbSessionDep
) -> StripeCheckoutResponse:
    """Create a Stripe checkout session for subscription."""
    user = await UserRepo(db).get_by_field_or_raise(
        lambda u: u.id == session_data.user_id, eager_load=[User.subscription]
    )
    # If the user already has a Stripe Customer, reuse it; otherwise pass their email
    existing_customer_id = (
        user.subscription.stripe_customer_id if user.subscription else None
    )

    customer_args: stripe.params.checkout.SessionCreateParams = (
        {"customer": existing_customer_id}
        if existing_customer_id
        else {"customer_email": session_data.email}
    )

    session = await run_in_threadpool(
        stripe.checkout.Session.create,
        client_reference_id=str(session_data.user_id),
        line_items=[
            {
                "price": settings.stripe.pro_product_price,
                "quantity": 1,
            },
        ],
        mode="subscription",
        success_url=str(settings.app.frontend_app_url),
        cancel_url=str(settings.app.frontend_app_url),
        allow_promotion_codes=True,
        **cast("dict[str, Any]", customer_args),
    )

    _log.info("Checkout session created", session_id=session.id)

    if not session.url:
        _log.error("Checkout session URL is empty", session_id=session.id)
        raise HTTPException(status_code=500, detail="Failed to create checkout session")

    return StripeCheckoutResponse(session_id=session.id, url=session.url)


@router.get("/portal")
async def create_billing_portal_session(
    settings: SettingsDep, session_data: SessionDataDep, db: DbSessionDep
) -> RedirectResponse:
    """Create a Stripe Billing Portal session and redirect the user to manage billing."""
    user = await UserRepo(db).get_by_field_or_raise(
        lambda u: u.id == session_data.user_id, eager_load=[User.subscription]
    )

    if user.subscription is None or not user.subscription.stripe_customer_id:
        raise HTTPException(status_code=404, detail="No subscription found for user")

    _log.info(
        "Creating billing portal session",
        user_id=session_data.user_id,
        email=session_data.email,
    )
    portal = await run_in_threadpool(
        stripe.billing_portal.Session.create,
        customer=user.subscription.stripe_customer_id,
        return_url=str(settings.app.frontend_app_url),
    )

    if not portal.url:
        _log.error("Billing portal session URL is empty")
        raise HTTPException(
            status_code=500, detail="Failed to create billing portal session"
        )

    return RedirectResponse(portal.url)


supported_webhook_events = {
    "checkout.session.completed",
    "customer.subscription.updated",
    "customer.subscription.deleted",
}


@router.post("/webhook")
async def stripe_webhook(  # noqa: C901
    request: Request,
    settings: SettingsDep,
    db: DbSessionDep,
) -> None:
    """Handle Stripe webhook events."""
    # Get the webhook data and signature
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    if not sig_header:
        _log.error("Missing Stripe signature header")
        raise HTTPException(status_code=400, detail="Missing Stripe signature header")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe.webhook_secret.value.get_secret_value()
        )
    except ValueError as e:
        _log.exception("Invalid payload")
        raise HTTPException(status_code=400, detail="Invalid payload") from e
    except stripe.SignatureVerificationError as e:
        _log.exception("Invalid signature")
        raise HTTPException(status_code=400, detail="Invalid signature") from e

    bind_contextvars(event_type=event.type, event_id=event.id)
    _log.info("Received Stripe webhook")

    if event.type not in supported_webhook_events:
        _log.info("Unhandled Stripe webhook event type")
        return
    _log.info("Handling Stripe webhook event", event_type=event.type)

    if event.type == "account.external_account.updated":
        _log.info("Handling account.external_account.updated event")
        # Handle the event here

    # Get the subscription & user_id
    if event.type == "checkout.session.completed":
        session = await run_in_threadpool(
            stripe.checkout.Session.retrieve,
            event.data.object["id"],
            expand=["subscription", "line_items"],
        )
        subscription = session.subscription
        if not isinstance(subscription, stripe.Subscription):
            _log.error("Invalid subscription object")
            raise HTTPException(status_code=400, detail="Invalid subscription object")
        bind_contextvars(checkout_session_id=session.id)
        if not session.client_reference_id:
            msg = "No client_reference_id in checkout session"
            _log.error(msg)
            raise HTTPException(status_code=400, detail=msg)
        user_id = UUID(session.client_reference_id)
    else:
        subscription = event.data.object
        if not isinstance(subscription, stripe.Subscription):
            _log.error("Invalid subscription object")
            raise HTTPException(status_code=400, detail="Invalid subscription object")
        user_id = (
            await SubscriptionRepo(db).get_by_field_or_raise(
                lambda s: s.stripe_customer_id == subscription.customer,
                eager_load=[Subscription.user],
            )
        ).user.id
        if event.type == "customer.subscription.deleted":
            await SubscriptionRepo(db).delete_by_field(
                lambda s: s.stripe_subscription_id == subscription.id
            )
            _log.info("Deleted subscription", subscription_id=subscription.id)
            return

    await _handle_update(user_id, db, subscription, settings.stripe.pro_product_id)


async def _handle_update(
    user_id: UUID,
    db: AsyncSession,
    subscription: stripe.Subscription,
    pro_product_id: str,
) -> None:
    item = next(
        (
            i
            for i in subscription.get("items", {}).get("data", [])
            if getattr(i, "price", None)
            and getattr(i.price, "product", None) == pro_product_id
        ),
        None,
    )

    # As long as the product is in the line items, consider it a valid subscription
    if item is None:
        msg = "Pro Product ID not found in line items, not creating subscription"
        _log.error(msg)
        raise HTTPException(status_code=400, detail=msg)

    user = await UserRepo(db).get_by_field_or_raise(lambda u: u.id == user_id)

    sub = Subscription(
        user_id=user.id,
        stripe_customer_id=str(subscription.customer),
        product="pro",
        stripe_subscription_id=subscription.id,
        current_period_start=datetime.fromtimestamp(item.current_period_start, tz=UTC),
        current_period_end=datetime.fromtimestamp(item.current_period_end, tz=UTC),
        cancel_at_period_end=subscription.cancel_at_period_end,
        created_at=datetime.fromtimestamp(subscription.created, tz=UTC),
    )

    user.subscription = sub
    await UserRepo(db).create_or_update(user)
