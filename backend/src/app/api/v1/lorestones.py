from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, HTTPException
from structlog.stdlib import get_logger

from app.api.utils import get_route_prefix
from app.app.dependencies import DbSessionDep, SessionDataDep
from app.app.dependencies._settings import SettingsDep
from app.db.repositories.lorestone_transaction import (
    LorestoneTransactionRepo,
)
from app.models import (
    LorestoneBalance,
    LorestoneCheckDailyClaimResponse,
    LorestoneDailyClaimResponse,
)

router = APIRouter(prefix=get_route_prefix(), tags=["lorestones"])
_log = get_logger(__name__)


@router.get("")
async def get_balance(db: DbSessionDep, session: SessionDataDep) -> LorestoneBalance:
    """Return the player's current lorestone balance."""

    transactions = LorestoneTransactionRepo(db)
    balance = await transactions.get_current_balance(session.user_id)
    return LorestoneBalance(balance=balance)


@router.get("/daily")
async def check_daily_bonus_claimed(
    db: DbSessionDep,
    session: SessionDataDep,
) -> LorestoneCheckDailyClaimResponse:
    """Check whether the daily lorestone bonus has been claimed today."""

    transactions = LorestoneTransactionRepo(db)

    now = datetime.now(UTC)
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day_start + timedelta(days=1)

    already_claimed = await transactions.has_transactions_in_range(
        session.user_id,
        category="daily_bonus",
        start=day_start,
        end=day_end,
    )
    return LorestoneCheckDailyClaimResponse(claimed=already_claimed)


@router.post("/daily")
async def claim_daily_bonus(
    settings: SettingsDep,
    db: DbSessionDep,
    session: SessionDataDep,
) -> LorestoneDailyClaimResponse:
    """Grant the daily lorestone bonus. May only be claimed once per UTC day."""

    transactions = LorestoneTransactionRepo(db)

    now = datetime.now(UTC)
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day_start + timedelta(days=1)

    already_claimed = await transactions.has_transactions_in_range(
        session.user_id,
        category="daily_bonus",
        start=day_start,
        end=day_end,
    )
    if already_claimed:
        _log.info("Daily bonus already claimed", user_id=str(session.user_id))
        raise HTTPException(status_code=429, detail="Daily bonus already claimed")

    tx = await transactions.create_transaction(
        user_id=session.user_id,
        amount=settings.llm.daily_bonus_lorestones,
        category="daily_bonus",
    )

    next_claim_at = day_end

    return LorestoneDailyClaimResponse(
        balance=tx.balance_after_transaction,
        claimed_amount=tx.amount,
        claimed_at=tx.created_at,
        next_claim_at=next_claim_at,
    )
