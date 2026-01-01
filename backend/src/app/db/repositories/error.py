import json
from traceback import format_tb
from typing import TYPE_CHECKING, Any

from app.db.schema import Error

from .base import BaseRepo

if TYPE_CHECKING:
    from app.models import CreateErrorRequest


class ErrorRepo(BaseRepo[Error]):
    @property
    def _model(self) -> type[Error]:
        return Error

    async def from_exception(
        self, exc: Exception, msg: str | None = None, **kwargs: Any
    ) -> Error:
        exc_tb = "".join(format_tb(exc.__traceback__))
        try:
            json_meta = json.dumps(kwargs, sort_keys=True)
        except Exception as e:  # noqa: BLE001
            json_meta = json.dumps({"meta": f"Failed to parse args: {e!r}"})

        return await self.create_or_update(
            Error(
                source="backend",
                message=msg,
                meta=json.dumps({"traceback": exc_tb, "kwargs": json_meta}),
            )
        )

    async def from_request(self, params: CreateErrorRequest) -> Error:
        """Create a frontend error from the request object."""
        return await self.create_or_update(
            Error(
                source="frontend",
                message=params.message,
                meta=params.meta,
            )
        )
