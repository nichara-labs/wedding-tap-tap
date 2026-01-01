from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, params
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import DatabaseSessionManager

from ._state import AppStateDep


async def _get_db_session(app_state: AppStateDep) -> AsyncGenerator[AsyncSession]:
    """Yield an SQLAlchemy AsyncSession for query usage."""
    async with app_state.db_session_manager.session() as session:
        yield session


def _get_db_session_manager(app_state: AppStateDep) -> DatabaseSessionManager:
    return app_state.db_session_manager


DbSessionDep = Annotated[AsyncSession, Depends(_get_db_session)]

db_session_manager_dependency: params.Depends = Depends(_get_db_session_manager)

DbSessionManagerDep = Annotated[DatabaseSessionManager, db_session_manager_dependency]
