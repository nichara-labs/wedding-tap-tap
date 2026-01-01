import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories import ErrorRepo

pytestmark = pytest.mark.anyio


@pytest.fixture
def error_repo(db_session: AsyncSession) -> ErrorRepo:
    return ErrorRepo(db_session)
