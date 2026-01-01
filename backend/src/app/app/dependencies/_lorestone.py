from typing import Annotated

from fastapi import Depends, HTTPException

from app.db.repositories import LorestoneTransactionRepo

from ._db import DbSessionDep
from ._session import SessionDataDep


async def _require_positive_lorestone_balance(
    db: DbSessionDep, session: SessionDataDep
) -> None:
    current_balance = await LorestoneTransactionRepo(db).get_current_balance(
        session.user_id
    )
    if current_balance <= 0:
        raise HTTPException(
            status_code=402,
            detail="Insufficient lorestones. Please top up your lorestones.",
        )


RequiresPositiveLorestoneBalanceDep = Annotated[
    None, Depends(_require_positive_lorestone_balance)
]
