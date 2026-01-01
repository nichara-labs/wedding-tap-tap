from uuid import UUID

from sqlalchemy import MetaData, Uuid
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
)
from uuid6 import uuid7


class Base(DeclarativeBase, MappedAsDataclass, AsyncAttrs):
    """
    Base class for all models.

    Note: You need to include your model in the __all__ list in the __init__.py file of the schema package for Alembic to be able to detect it during migration autogeneration.
    """

    id: Mapped[UUID] = mapped_column(
        Uuid, primary_key=True, default_factory=uuid7, init=False
    )

    # Standardize the naming convention for indexes, unique constraints, etc.
    # https://alembic.sqlalchemy.org/en/latest/naming.html
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )
