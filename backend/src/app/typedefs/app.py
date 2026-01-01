from collections.abc import Callable, Coroutine
from typing import Any, Literal, Self
from uuid import UUID

from pydantic import BaseModel

from app.db.schema import User
from app.db.schema.user import Provider


class SessionData(BaseModel):
    """Serialized session data for the user. Only present for logged-in users. Session data is signed (preventing tampering) but NOT encrypted."""

    user_id: UUID
    """Id of the user, as in the DB."""
    picture: str | None = None
    name: str | None = None
    email: str
    provider: Provider

    @classmethod
    def from_user(cls, user: User) -> Self:
        return cls(
            user_id=user.id,
            name=user.name,
            email=user.email,
            provider=user.provider,
            picture=user.picture,
        )


type LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "NOTSET"]

type LifespanTask[**P] = Callable[P, Coroutine[Any, Any, TaskCleanupFunc | None]]
"""A lifespan task that returns a cleanup function."""

type TaskCleanupFunc = Callable[[], Coroutine[Any, Any, Any]]
"""The cleanup function returned by a lifespan task."""
