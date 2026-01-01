from collections.abc import AsyncGenerator, Callable, Sequence

from sqlalchemy import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession

type DbSession = AsyncGenerator[AsyncSession]

type WhereFunc[T] = Callable[[type[T]], Sequence[ColumnElement] | ColumnElement]
