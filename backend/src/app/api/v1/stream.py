import asyncio
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import APIRouter, Query, Request
from fastapi.responses import StreamingResponse
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import getLogger

from app.api.utils import get_route_prefix
from app.app.dependencies import DbSessionDep

router = APIRouter(prefix=get_route_prefix(), tags=["stream"])

_log = getLogger(__name__)


@router.get("/test")
async def stream_test(
    duration: Annotated[
        int, Query(ge=1, le=180, description="Seconds to stream (max 179)")
    ],
    request: Request,
    db: DbSessionDep,
    delay: Annotated[
        int, Query(ge=0, description="Optional start delay in seconds")
    ] = 0,
    lock_id: int = 10,
) -> StreamingResponse:
    """
    Stream a test sequence of words, one per second, optionally with a start delay.

    Useful to check for gateway timeouts in production.
    """
    return StreamingResponse(
        _word_stream(duration, request, db, lock_id, delay),
        media_type="text/plain; charset=utf-8",
    )


async def _word_stream(
    duration: int, request: Request, db: AsyncSession, lock_id: int, delay: int
) -> AsyncIterator[str]:
    """Yield one word per second for the requested duration."""
    try:
        unlock_status = (
            await db.execute(func.pg_try_advisory_lock(lock_id))
        ).scalar_one()
        if not unlock_status:
            _log.warning("Failed to obtain lock")
            yield "Failed to obtain lock"
            return
        await asyncio.sleep(delay)
        for i in range(duration):
            if await request.is_disconnected():
                _log.info("disconnected")
                break
            yield f"word_{i + 1} "
            await asyncio.sleep(1)
        _log.info("Stream done")

    except asyncio.CancelledError:
        _log.info("Stream task was cancelled (client disconnected or shutdown)")


@router.get("/check-lock")
async def check_lock(db: DbSessionDep, lock_id: int) -> dict:
    """Check the status of a lock."""
    is_lock_acquired = (
        await db.execute(func.pg_try_advisory_lock(lock_id))
    ).scalar_one()
    return {"lock_status": "unlocked" if is_lock_acquired else "locked"}
