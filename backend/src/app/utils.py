import base64
from collections.abc import Callable
from functools import cache as _cache
from functools import wraps
from hashlib import sha256
from typing import Any, Concatenate
from uuid import UUID

from pydantic import BaseModel


def cache[**P, T](f: Callable[P, T]) -> Callable[P, T]:
    """Return wrapper for functools.cache which preserves types on the wrapped function."""

    cached_func = _cache(f)

    @wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        return cached_func(*args, **kwargs)

    return wrapper


def model_apply[M: BaseModel, T, **P](
    model: M,
    target: type[T],
    f: Callable[Concatenate[T, P], Any],
    *args: P.args,
    **kwargs: P.kwargs,
) -> M:
    """Recursively apply a function to all fields of a Pydantic BaseModel that are of a certain type."""
    for _, value in model:
        if isinstance(value, target):
            f(value, *args, **kwargs)
        elif isinstance(value, BaseModel):
            model_apply(value, target, f, *args, **kwargs)
    return model


def is_base64(s: str) -> bool:
    """Check if a string is base64 encoded."""
    return base64.b64encode(base64.b64decode(s)).decode() == s


class Pipe[TIn, T]:
    """
    A simple data processing pipeline that allows chaining of functions with type safety.

    Each function in the pipeline takes the output of the previous function as its input.

    Usage:

    ```python
    def parse_int(s: str) -> int:
        return int(s.strip())

    def to_ratio(n: int) -> float:
        return n / 100.0

    def label(v: float) -> dict[str, float]:
        return {"score": v}

    pipe = Pipe(str).then(parse_int).then(to_ratio).then(label).run("  123  ")
    ```
    """

    def __init__(
        self, input_type: type[TIn], func: Callable[[TIn], T] = lambda x: x
    ) -> None:
        self._func = func
        self._input_type = input_type

    def then[U](self, f: Callable[[T], U]) -> Pipe[TIn, U]:
        """Add a step to the pipeline that transforms the value."""

        def _chain(x: TIn) -> U:
            return f(self._func(x))

        return Pipe[TIn, U](self._input_type, _chain)

    def tap(self: Pipe[TIn, T], f: Callable[[T], Any]) -> Pipe[TIn, T]:
        """Run a side-effecting step that does not modify the value."""

        def _tap(x: T) -> T:
            f(x)
            return x

        return self.then(_tap)

    def run(self: Pipe[TIn, T], x: TIn) -> T:
        return self._func(x)


def uuid_to_int_64(uuid: UUID, prefix: str | None = None) -> int:
    """Return a 64-bit integer derived from the SHA256 hash of an optional prefix and the UUID bytes."""
    hasher = sha256()
    if prefix:
        hasher.update(prefix.encode("utf-8"))
    hasher.update(uuid.bytes)
    return int.from_bytes(hasher.digest()[:8], signed=True)
