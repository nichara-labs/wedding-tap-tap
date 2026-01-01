from collections.abc import Callable
from itertools import chain
from unittest.mock import AsyncMock, Mock, call

import pytest

from app.app.lifespan import LifespanBuilder

pytestmark = pytest.mark.anyio


@pytest.fixture
def task_builder() -> Callable[[], AsyncMock]:
    """Return a factory for creating tasks."""

    def build(*, empty_callback: bool = False) -> AsyncMock:
        task = AsyncMock()

        # The cleanup function
        task.return_value = None if empty_callback else AsyncMock()
        return task

    return build


class TestLifespanBuilder:
    async def test_run_tasks_and_cleanup_tasks_in_order(
        self, task_builder: Callable[[], AsyncMock]
    ) -> None:
        """Check that tasks are run in order, and their cleanup is called in reverse order."""
        builder = LifespanBuilder()

        # Create a mock object to track the order of calls
        tasks_manager = Mock()
        [tasks_manager.attach_mock(task_builder(), f"task_{i}") for i in range(3)]

        # Add tasks to the builder
        tasks = [getattr(tasks_manager, f"task_{i}") for i in range(3)]
        [builder.add(tasks) for tasks in tasks]
        lifespan = builder.build()

        # Trigger the lifespan function
        async with lifespan(Mock()):
            pass

        task_calls = [
            # Check tasks were run in order
            getattr(call, f"task_{i}")()
            for i in range(3)
        ]

        task_cleanup_calls = list(
            chain.from_iterable(  # Flatten the list of lists
                # Check cleanup tasks were run in reverse order
                [
                    # This check for __bool__ is necessary, because the builder checks whether the cleanup task is None
                    # The AsyncMock records this access
                    getattr(call, f"task_{i}")().__bool__,
                    getattr(call, f"task_{i}")()(),
                ]
                for i in range(2, -1, -1)
            )
        )

        assert tasks_manager.mock_calls == task_calls + task_cleanup_calls

    async def test_cleanup_was_awaited(
        self, task_builder: Callable[[], AsyncMock]
    ) -> None:
        """Check that cleanup tasks are awaited."""
        builder = LifespanBuilder()
        task = task_builder()
        # Build and call the lifespan function
        async with builder.add(task).build()(Mock()):
            pass
        task.return_value.assert_awaited()
