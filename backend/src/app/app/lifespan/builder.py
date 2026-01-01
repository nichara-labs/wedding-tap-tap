from collections.abc import AsyncGenerator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from functools import partial
from typing import Self

from fastapi import FastAPI

from app.typedefs import LifespanTask


class LifespanBuilder:
    def __init__(self) -> None:
        self.lifespan_tasks: list[LifespanTask] = []

    def add[**P](
        self,
        func: LifespanTask[P],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Self:
        """Add a task which should run when the application starts. It can optionally return a cleanup function which will be run when the application stops."""
        self.lifespan_tasks.append(partial(func, *args, **kwargs))
        return self

    def build(self) -> Callable[[FastAPI], AbstractAsyncContextManager[None]]:
        """
        Build the lifespan function for FastAPI.

        Note: tasks are awaited sequentially, not in parallel. Cleanup functions are executed in the reverse order the tasks were added.
        """

        @asynccontextmanager
        async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
            cleanup_stack = [await task() for task in self.lifespan_tasks]
            yield
            # Cleanup in reverse order
            for cleanup in reversed(cleanup_stack):
                if cleanup:
                    await cleanup()

        return lifespan
