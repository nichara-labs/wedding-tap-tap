from typing import Annotated

from pydantic import Field, PrivateAttr, model_serializer

from app.settings._base import BaseModelNoExtra


class _ParameterNotFetchedError(Exception): ...


class SsmParameter[T](BaseModelNoExtra):
    """
    Represents a single value from a parameter stored in AWS Systems Manager (SSM) Parameter Store.

    Parameters are fetched on app startup. The `value` property can be used to access the parameter value.
    """

    override: Annotated[
        T | None,  # None is used to indicate that the parameter is not set
        Field(
            description="Bypass parameter retrieval and use this value directly. Intended for local development only."
        ),
    ] = None
    _internal_value: T | None = PrivateAttr(default=None)

    @property
    def value(self) -> T:
        """Return the value of the parameter. Raises an error if it has not yet been fetched."""
        if self.override is not None:
            return self.override
        if self._internal_value:
            return self._internal_value
        raise _ParameterNotFetchedError

    @model_serializer()
    def serialize(self) -> T | None:
        """Used when printing settings during app initialization."""
        try:
            return self.value
        except _ParameterNotFetchedError:  # During openapi schema generation
            return None
