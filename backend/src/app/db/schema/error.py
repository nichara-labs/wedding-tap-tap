from datetime import datetime
from typing import Literal

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.schema.base import Base

ErrorSource = Literal["frontend", "backend"]


class Error(Base):
    """Represents either frontend or backend errors."""

    __tablename__ = "error"

    source: Mapped[ErrorSource]
    message: Mapped[str | None] = mapped_column(default=None)
    meta: Mapped[str | None] = mapped_column(default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=None
    )
