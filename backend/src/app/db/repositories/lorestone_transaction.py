from collections.abc import Sequence
from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from structlog import getLogger

from app.db.schema import LorestoneTransaction
from app.db.schema.lorestone_transaction import TransactionCategory
from app.models.lorestone import LorestoneTransactionModel

from .base import BaseRepo

_log = getLogger(__name__)


class LorestoneTransactionRepo(BaseRepo[LorestoneTransaction]):
    @property
    def _model(self) -> type[LorestoneTransaction]:
        return LorestoneTransaction

    async def has_transactions_in_range(
        self,
        user_id: UUID,
        category: TransactionCategory | None,
        start: datetime,
        end: datetime,
    ) -> bool:
        """Check whether the user has at least one transaction in the supplied window."""
        stmt = (
            select(func.count())
            .select_from(LorestoneTransaction)
            .where(
                LorestoneTransaction.user_id == user_id,
                LorestoneTransaction.created_at >= start,
                LorestoneTransaction.created_at < end,
            )
        )
        if category:
            stmt = stmt.where(LorestoneTransaction.category == category)
        count = await self.session.scalar(stmt)
        return bool(count)

    async def get_user_transactions(
        self,
        user_id: UUID,
        category: TransactionCategory | None,
        start: datetime,
        end: datetime,
    ) -> Sequence[LorestoneTransactionModel]:
        """Return the transactions for a user within a time range, optionally filtered by type."""
        stmt = select(LorestoneTransaction).where(
            LorestoneTransaction.user_id == user_id,
            LorestoneTransaction.created_at >= start,
            LorestoneTransaction.created_at < end,
        )
        if category:
            stmt = stmt.where(LorestoneTransaction.category == category)
        result = await self.session.scalars(stmt)

        return [
            LorestoneTransactionModel(
                id=x.id,
                user_id=x.user_id,
                balance_before_transaction=x.balance_before_transaction,
                balance_after_transaction=x.balance_after_transaction,
                amount=x.amount,
                category=x.category,
                created_at=x.created_at,
            )
            for x in result
        ]

    async def get_current_balance(self, user_id: UUID) -> int:
        """Return the user's latest known lorestone balance."""
        stmt = (
            select(LorestoneTransaction.balance_after_transaction)
            .where(LorestoneTransaction.user_id == user_id)
            .order_by(
                LorestoneTransaction.created_at.desc(),
            )
            .limit(1)
        )
        balance = await self.session.scalar(stmt)
        return balance or 0

    async def create_transaction(
        self,
        *,
        user_id: UUID,
        amount: int,
        category: TransactionCategory,
        additional_info: str | None = None,
    ) -> LorestoneTransaction:
        """Create a new transaction and return the persisted instance."""
        balance_before = await self.get_current_balance(user_id)
        balance_after = balance_before + amount
        if balance_after < 0:
            msg = "Lorestone balance cannot be negative"
            raise ValueError(msg)

        tx = LorestoneTransaction(
            user_id=user_id,
            balance_before_transaction=balance_before,
            balance_after_transaction=balance_after,
            amount=amount,
            category=category,
            additional_info=additional_info,
        )
        return await self.create_or_update(tx)
