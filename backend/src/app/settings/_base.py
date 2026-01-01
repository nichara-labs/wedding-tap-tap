# ruff: noqa: SLF001
from typing import Any

from pydantic import BaseModel, PrivateAttr
from pydantic.config import ConfigDict


class BaseModelNoExtra(BaseModel):
    """
    Base model that forbids extra fields and tracks parent-child relationships.

    This model automatically attaches parent references to child instances.
    """

    model_config = ConfigDict(extra="forbid")

    _parent: BaseModelNoExtra | None = PrivateAttr(default=None)
    _name_in_parent: str | None = PrivateAttr(default=None)

    def model_post_init(self, __context: Any) -> None:  # noqa: PYI063
        self._attach_children()

    # Recursively attach parent information
    def _attach_children(self) -> None:
        for attr, value in self.__dict__.items():
            self._maybe_attach(attr, value)

    def _maybe_attach(self, attr: str, value: Any) -> None:
        if isinstance(value, BaseModelNoExtra):
            value._parent = self
            value._name_in_parent = attr
            value._attach_children()

    def path_from_parent(self, sep: str = "/") -> str:
        """Return the path from the root of the model tree to this instance, with the specified separator."""
        parts: list[str] = []
        node: BaseModelNoExtra | None = self
        while node is not None and node._name_in_parent is not None:
            parts.append(node._name_in_parent)
            node = node._parent
        return sep.join(reversed(parts))
