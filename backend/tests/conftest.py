from pathlib import Path

import pytest

pytestmark = pytest.mark.anyio


def _as_module(fixture_path: Path) -> str:
    """Convert a path to a module import string."""
    return (
        str(fixture_path.relative_to(Path(__file__).parent.parent))
        .replace("/", ".")
        .replace("\\", ".")
        .replace(".py", "")
    )


# Load all fixtures from the fixtures directory excluding files starting with __.
pytest_plugins = [
    _as_module(fixture)
    for fixture in Path(__file__).parent.glob("fixtures/**/[!__]*.py")
]


@pytest.fixture
def anyio_backend() -> str:
    """
    Run all async tests using asyncio as the backend for anyio.

    Must be in the top level conftest.py.
    """
    return "asyncio"
