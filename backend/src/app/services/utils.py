import base64
import time
from collections.abc import Callable, Generator
from contextlib import contextmanager
from typing import Any

import brotli
from pydantic import BaseModel


def compress_model(params: BaseModel) -> str:
    """Compress a Pydantic model into a base64 string with Brotli."""
    return base64.b64encode(
        brotli.compress(params.model_dump_json().encode("utf-8"))
    ).decode("utf-8")


@contextmanager
def log_time(log_fn: Callable, *args: Any, **kwargs: Any) -> Generator[None]:
    """
    Context manager to log the time taken for a block of code to execute.

    Passes `time_taken_ms` as a keyword argument to the logging function.

    Args:
        log_fn: The logging function which will be called with the time taken.
        args: Positional arguments to pass to the logging function.
        kwargs: Keyword arguments to pass to the logging function.

    Note: If an exception was raised in the context handler, the `log_fn` will still be called and the exception will be re-raised after.

    Usage:

    ```python
    with log_time(logger.info, "Processing data"):
        some_operation()
    # Logs:
    # Processing data, time_taken_ms=123
    ```
    """
    start = time.time_ns()
    try:
        yield
    finally:
        end = time.time_ns()
        formatted = round((start - end) / 1e6)
        log_fn(*args, time_taken_ms=formatted, **kwargs)
