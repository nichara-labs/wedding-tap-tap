from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import BaseModel

from app.db.schema import Error, ErrorSource


class ErrorModel(BaseModel):
    id: UUID
    source: ErrorSource
    message: str | None
    meta: str | None
    created_dt: datetime

    @classmethod
    def from_error(cls, error: Error) -> Self:
        return cls(
            id=error.id,
            source=error.source,
            message=error.message,
            meta=error.meta,
            created_dt=error.created_at,
        )


class CreateErrorRequest(BaseModel):
    message: str | None = None
    meta: str | None = None
