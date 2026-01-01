from typing import Any

import pytest

from app.services.utils import log_time


class _TestError(Exception): ...


def test_log_time() -> None:
    """Check that log_fn is still called even if an exception was raised."""
    was_called = False

    def should_be_called(*_args: Any, **_kwargs: Any) -> None:
        nonlocal was_called
        was_called = True

    with pytest.raises(_TestError), log_time(should_be_called):
        raise _TestError
    assert was_called
