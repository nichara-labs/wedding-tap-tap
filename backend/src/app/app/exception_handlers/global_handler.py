from contextlib import AsyncExitStack
from typing import TYPE_CHECKING

from fastapi.dependencies.utils import (
    get_parameterless_sub_dependant,
    solve_dependencies,
)
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from structlog.contextvars import bind_contextvars
from structlog.stdlib import get_logger

import app
from app.app.dependencies._db import db_session_manager_dependency
from app.db.repositories import ErrorRepo
from app.models import ErrorDetail

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

_log = get_logger(f"{app.__name__}.server.exception")


_err_resp = JSONResponse(
    status_code=500,
    content=ErrorDetail(
        detail="Internal Server Error (same origin request)",
        status_code=500,
    ).model_dump(),
)


async def log_uncaught_exception(request: Request, exc: Exception) -> Response:
    """
    Log uncaught exceptions in the app to the DB.

    Note:
    - This handler's response is only used on same-origin requests. For cross-origin requests, CORSErrorHandlingMiddleware.simple_response() is used.
    - ServerErrorMiddleware wraps this handler, so it still calls its logging handlers.
    - Uses a different AsyncSession than that of the Request to avoid SQLAlchemy concurrency exceptions

    Testing notes: db_session_dependency needs to be mocked out to a function which returns a test DB session (which should be different from the one in the request).
    """
    bind_contextvars(path=request.url.path)
    try:
        async with AsyncExitStack() as stack:
            solved = await solve_dependencies(
                request=request,
                dependant=get_parameterless_sub_dependant(
                    depends=db_session_manager_dependency, path="/"
                ),
                async_exit_stack=stack,
                embed_body_fields=False,
                dependency_overrides_provider=request.app,  # TODO Not type checked
            )
            call = db_session_manager_dependency.dependency
            if not call:
                await _log.aerror(
                    "Failed to log error to DB, no callable found for dependency"
                )
                return _err_resp

            # Get a new session, to avoid SQLAlchemy concurrency exceptions https://docs.sqlalchemy.org/en/20/errors.html#error-isce
            # I still don't understand why this is necessary, but it is.
            db_session: AsyncSession = await stack.enter_async_context(
                call(**solved.values).session()
            )
            await ErrorRepo(db_session).from_exception(
                exc, msg=repr(exc), path=request.url.path
            )
    except Exception as e:  # noqa: BLE001
        await _log.aerror("Failed to log error to DB", exc_info=e)

    return _err_resp
