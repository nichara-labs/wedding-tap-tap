from typing import Annotated

from fastapi import Depends, FastAPI, Request


async def get_app(request: Request) -> FastAPI:
    """Get the FastAPI application instance from the request."""
    return request.app


AppDep = Annotated[FastAPI, Depends(get_app)]
