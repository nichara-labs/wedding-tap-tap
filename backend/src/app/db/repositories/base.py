from abc import ABC, abstractmethod
from collections.abc import Iterable, Sequence
from typing import Any

from sqlalchemy import ColumnElement, CursorResult, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute, selectinload
from structlog.stdlib import get_logger

from app.db.schema import Base
from app.typedefs import WhereFunc

_logger = get_logger(__name__)


class MultipleObjectsReturnedError(Exception): ...


class ObjectNotFoundError(Exception): ...


class BaseRepo[T: Base](ABC):
    """
    Abstract base class for database managers.

    Note: We don't commit() here, only flush(). The call to commit is done on exiting the context manager in the DatabaseSessionManager. This lets us rollback any changes to the DB if an error occured in the request handler.
    """

    @property
    @abstractmethod
    def _model(self) -> type[T]:
        """
        Return the model class for this manager.

        Not meant to be called - exists to allow type checkers to infer the correct generic type of subclasses.
        """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_field(
        self,
        where_func: WhereFunc[T],
        eager_load: list[InstrumentedAttribute] | None = None,
    ) -> T | None:
        """
        Get an object by a field, or None if it doesn't exist.

        Raises an error if multiple objects are returned.

        Args:
            where_func: A function that takes the model class and returns a list of column expressions to use in the WHERE clause.
            eager_load: A list of fields to load eagerly using selectinload. This is required when using the AsyncSession, otherwise accessing relationships on the object will fail.
        """
        res = await self._get_by_field(where_func, eager_load)
        if len(res) > 1:
            msg = f"Multiple {self._model.__name__} objects returned"
            raise MultipleObjectsReturnedError(msg)
        return res[0] if res else None

    async def get_by_field_multiple(
        self,
        where_func: WhereFunc[T] = lambda _: [],
        eager_load: list[InstrumentedAttribute] | None = None,
    ) -> Sequence[T]:
        """Like get_by_field, but returns a list of objects instead of raising an error if multiple are found."""
        return await self._get_by_field(where_func, eager_load)

    async def get_by_field_or_raise(
        self,
        where_func: WhereFunc[T],
        eager_load: list[InstrumentedAttribute] | None = None,
    ) -> T:
        """Get an object by a field, or raise an error if it doesn't exist. Arguments are the same as get_by_field."""
        obj = await self.get_by_field(where_func, eager_load)
        if obj is None:
            msg = f"{self._model.__name__} not found"
            raise ObjectNotFoundError(msg)
        return obj

    async def create_or_update(
        self, obj: T, eager_load: list[InstrumentedAttribute[Any]] | None = None
    ) -> T:
        """
        Create or update an object. Will only perform an update when the object is in the session (i.e. Pending or Persistent). Otherwise, a new instance is created.

        For more info, see the [documentation](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-object-states).
        """
        self.session.add(obj)
        await self.session.flush()
        _obj = self._model.__name__
        _logger.debug("DB: Created %s", _obj, obj=_obj)

        # We need to refetch the object so we can eagerly load relationships.
        return await self.get_by_field_or_raise(
            lambda _: self._model.id == obj.id, eager_load
        )

    async def delete(self, obj: T) -> None:
        """Delete an object."""
        await self.session.delete(obj)
        await self.session.flush()
        id_ = getattr(obj, "id", None)
        _obj = self._model.__name__
        _logger.debug("DB: Deleted %s", _obj, obj=_obj, id=id_)

    async def delete_by_field(self, where_func: WhereFunc[T]) -> int:
        """Delete an object (or objects) by a field. Returns the number of objects deleted."""
        stmt = delete(self._model).where(*self._to_where_clauses(where_func))
        res = await self.session.execute(stmt)
        await self.session.flush()
        _logger.debug(
            "Deleted object",
            obj=self._model.__name__,
            stmt=str(stmt),
            params=stmt.compile().params,
        )
        if not isinstance(res, CursorResult):
            # https://docs.sqlalchemy.org/en/20/changelog/changelog_20.html#change-2.0.44-typing
            err = "Result was not an instance of CursorResult, no rowcount attribute"
            raise TypeError(err)
        return res.rowcount

    async def delete_by_field_or_raise(self, where_func: WhereFunc[T]) -> int:
        """Delete an object (or objects) by a field, or raise an error if no objects were deleted. Arguments are the same as delete_by_field."""
        count = await self.delete_by_field(where_func)
        if count == 0:
            msg = f"No {self._model.__name__} found for the query"
            raise ObjectNotFoundError(msg)
        return count

    async def _get_by_field(
        self,
        where_func: WhereFunc[T],
        eager_load: list[InstrumentedAttribute[Any]] | None = None,
    ) -> Sequence[T]:
        stmt = select(self._model).where(*self._to_where_clauses(where_func))
        if eager_load:
            stmt = stmt.options(selectinload(*eager_load))
        res = (await self.session.scalars(stmt)).all()
        _obj = self._model.__name__
        _logger.debug(
            "DB: Get %s",
            _obj,
            result_count=len(res),
            obj=_obj,
            stmt=str(stmt),
            params=stmt.compile().params,
        )
        return res

    def _to_where_clauses(self, where_func: WhereFunc[T]) -> Sequence[ColumnElement]:
        """Convert a where function to a list of where clauses."""
        where_result = where_func(self._model)
        return where_result if isinstance(where_result, Iterable) else [where_result]
