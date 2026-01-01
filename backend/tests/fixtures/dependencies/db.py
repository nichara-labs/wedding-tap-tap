from collections.abc import AsyncIterator, Callable, Generator
from typing import TypedDict
from uuid import uuid4

import pytest
from sqlalchemy import URL, create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils import create_database
from testcontainers.postgres import PostgresContainer

from app.db.schema import Base
from app.db.session import DatabaseSessionManager

pytestmark = pytest.mark.anyio


class _DbUrls(TypedDict):
    sync: URL
    async_: URL


@pytest.fixture
def get_db_session(
    db_session: AsyncSession,
) -> Callable[[], AsyncIterator[AsyncSession]]:
    """
    Dependency function for getting database sessions.

    Returns a new session on each call.
    """

    async def _get_db_session() -> AsyncIterator[AsyncSession]:
        yield db_session

    return _get_db_session


@pytest.fixture
async def db_session(
    db_session_manager: DatabaseSessionManager,
) -> AsyncIterator[AsyncSession]:
    """
    A shared AsyncSession for a single test.

    Use this in repo fixtures to ensure all repos in a test use the same session instance.
    """
    async with db_session_manager.session() as session:
        yield session


@pytest.fixture
def db_session_manager(db_urls: _DbUrls) -> DatabaseSessionManager:
    sync_engine = create_engine(db_urls["sync"])
    create_database(sync_engine.url)
    Base.metadata.create_all(sync_engine)

    return DatabaseSessionManager.from_url(db_urls["async_"])


@pytest.fixture(scope="session")
def postgres() -> Generator[PostgresContainer]:
    """Spin up a postgres container and return the instance."""
    with PostgresContainer(
        "postgres:16",
        # Using a tmpfs mount speeds up tests by ~25%
        # https://docs.docker.com/engine/storage/tmpfs
        tmpfs={"/var/lib/postgresql/data": ""},
        driver=None,
    ) as container:
        yield container


@pytest.fixture
def db_urls(postgres: PostgresContainer) -> _DbUrls:
    """Sync and async URLs to the same database."""
    db_name = uuid4().hex
    url = create_engine(
        # If no driver is set, it will attempt to load psycopg2 and fail
        postgres.get_connection_url(driver="psycopg")
    ).url._replace(database=db_name)
    return {
        "sync": url._replace(drivername="postgresql+psycopg"),
        "async_": url._replace(drivername="asyncpg"),
    }


@pytest.fixture
def new_db_url(postgres: PostgresContainer) -> URL:
    """Sync URL to database, different from that in db_urls."""
    engine = create_engine(postgres.get_connection_url(driver="psycopg"))
    return engine.url._replace(database=uuid4().hex)
