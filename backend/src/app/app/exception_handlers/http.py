from typing import cast

from fastapi import HTTPException, Request, Response
from fastapi.responses import JSONResponse

from app.models import ErrorDetail


async def http_exception_handler(_request: Request, exc: Exception) -> Response:
    """
    Add status code to HTTPException responses.

    Workaround because React Query doesn't have access to the status code otherwise.
    """
    http_exc = cast("HTTPException", exc)
    return JSONResponse(
        content=ErrorDetail(
            detail=http_exc.detail, status_code=http_exc.status_code
        ).model_dump(),
        status_code=http_exc.status_code,
    )
