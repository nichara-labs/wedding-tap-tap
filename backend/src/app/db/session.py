import contextlib
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Self, TypedDict, Unpack

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import AsyncAdaptedQueuePool, Pool
from structlog.stdlib import get_logger

if TYPE_CHECKING:
    from app.settings import DatabaseSettings

_log = get_logger(__name__)


class DbConnectionParams(TypedDict):
    username: str
    password: str
    host: str
    port: int
    database: str


class InvalidSqlalchemyUrlError(Exception): ...


class DatabaseSessionManager:
    """
    Async DB session manager for use in FastAPI dependency injectors.

    References:
    - https://github.com/ThomasAitken/demo-fastapi-async-sqlalchemy/blob/main/backend/app/database.py
    - https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html
    """

    def __init__(
        self,
        poolclass: type[Pool] = AsyncAdaptedQueuePool,
        **kwargs: Unpack[DbConnectionParams],
    ) -> None:
        """Create this class using an AsyncSession."""
        connection_url = URL.create("postgresql+asyncpg", **kwargs)
        self._engine = create_async_engine(
            connection_url,
            poolclass=poolclass,
            pool_pre_ping=True,  # Neon DB: Wake up database
        )
        self._sessionmaker = async_sessionmaker(
            autocommit=False,
            bind=self._engine,
            # Allows us to access attributes even after committing.
            # This lets us avoid having to use Session.refresh() after commit() in tests after commit()
            # Does not affect running of the app since we never access committed objects (commit() is only called at the end of the route handler).
            # Recommended by https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-orm
            expire_on_commit=False,
            # Prevent the session from being used, after it is closed
            # This avoids confusion in tests, where the Session is returned instead of being yielded in a context manager
            # https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.close_resets_only
            close_resets_only=False,
        )
        _log.info("Database session established")

    @classmethod
    def from_settings(cls, db: DatabaseSettings) -> Self:
        return cls.from_url(db.to_url(drivername="postgresql+asyncpg"))

    @classmethod
    def from_url(cls, url: URL, poolclass: type[Pool] = AsyncAdaptedQueuePool) -> Self:
        """Create from an SQLAlchemy URL."""
        return cls(
            **cls.validate_url(url),
            poolclass=poolclass,
        )

    @classmethod
    def validate_url(cls, url: URL) -> DbConnectionParams:
        """Validate an SQLAlchemy URL and return the connection parameters."""
        if (
            not url.username
            or not url.password
            or not url.host
            or not url.port
            or not url.database
        ):
            raise InvalidSqlalchemyUrlError
        return {
            "username": url.username,
            "password": url.password,
            "host": url.host,
            "port": url.port,
            "database": url.database,
        }

    def get_connection_url(self) -> URL:
        """Returns the (async) connection URL used by the instance."""
        return self._engine.url

    async def close(self) -> None:
        await self._engine.dispose()

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        session = self._sessionmaker()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.aclose()
