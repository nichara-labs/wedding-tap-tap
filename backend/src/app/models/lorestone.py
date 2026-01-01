from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.db.schema.lorestone_transaction import TransactionCategory


class LorestoneBalance(BaseModel):
    balance: int = Field(ge=0)


class LorestoneDailyClaimResponse(LorestoneBalance):
    claimed_amount: int = Field(ge=0)
    claimed_at: datetime
    next_claim_at: datetime


class LorestoneCheckDailyClaimResponse(BaseModel):
    claimed: bool


class LorestoneTransactionModel(BaseModel):
    id: UUID
    user_id: UUID
    balance_before_transaction: int
    balance_after_transaction: int
    amount: int
    category: TransactionCategory
    created_at: datetime
