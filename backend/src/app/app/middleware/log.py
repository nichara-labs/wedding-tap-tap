import time

from asgiref.typing import (
    ASGIReceiveCallable,
    ASGISendCallable,
    ASGISendEvent,
    HTTPScope,
    Scope,
    WebSocketScope,
)
from pydantic import BaseModel
from starlette.types import ASGIApp, Receive, Send
from starlette.types import Scope as StarletteScope
from structlog.stdlib import get_logger

import app

_log = get_logger(f"{app.__name__}.api.access")


class _RequestLog(BaseModel):
    """A request logger."""

    client_ip: str | None = None
    http_version: str | None = None
    path: str | None = None
    query_string: str | None = None
    headers: dict[str, str] | None = None
    """Request headers."""
    status_code: int | None = None
    method: str | None = None
    """Will be None for websocket connections."""
    time_taken_s: float = 0


class HttpLogMiddleware:
    """
    Log basic information for HTTP requests.

    See ASGI specs for scope here https://asgi.readthedocs.io/en/latest/specs/www.html.
    """

    _logged_headers = (
        "user-agent",
        "content-type",
        "content-length",
        "accept",
        "x-forwarded-for",
        "cf-connecting-ip",
        "x-request-id",
    )

    def __init__(self, app: ASGIApp, unlogged_paths: list[str] | None = None) -> None:
        """
        Args:
            app: The ASGI app to wrap.
            unlogged_paths: List of URL paths (with the api prefix) that should not be logged by the middleware. If a request's path matches any path in this list, it will be skipped during logging.
        """
        self.app = app
        self._unlogged_paths = unlogged_paths or []

    async def __call__(
        self, scope: StarletteScope, receive: Receive, send: Send
    ) -> None:
        # Starlette's Scope/Receive/Send types are not compatible with that from asgiref
        await self._process(scope, receive, send)  # pyright:ignore[reportArgumentType]

    async def _process(
        self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable
    ) -> None:
        # We process both HTTP and Websocket events
        if scope["type"] == "lifespan":
            return await self.app(scope, receive, send)  # pyright:ignore[reportArgumentType]

        request_log = _RequestLog(
            headers=self._get_headers(scope),
            client_ip=self._get_client_ip(scope),
            method=scope.get("method"),
            path=scope["path"],
            http_version=scope.get("http_version"),
            query_string=scope["query_string"].decode(encoding="utf-8"),
        )

        async def add_response_status(message: ASGISendEvent) -> None:
            """Inspect our app's response and extract the status code."""

            # We are only concerned with http responses
            if message["type"] == "http.response.start":
                request_log.status_code = message["status"]

            await send(message)

        # Run the request through the app and log the time taken
        start_time = time.perf_counter_ns()
        try:
            await self.app(scope, receive, add_response_status)  # pyright:ignore[reportArgumentType]
        finally:
            # Always log regardless of whether errors are thrown
            if scope["path"] not in self._unlogged_paths:
                request_log.time_taken_s = round(
                    (time.perf_counter_ns() - start_time) / 10.0**9, 2
                )

                _log.info(
                    f"{request_log.method} {request_log.path}",
                    **request_log.model_dump(),
                )

        return None

    def _get_client_ip(self, scope: HTTPScope | WebSocketScope) -> str | None:
        headers = self._get_headers(scope)
        if ips := headers.get("x-forwarded-for"):
            return ips.split(",")[0]
        return scope["client"][0] if scope["client"] else None

    def _get_headers(self, scope: HTTPScope | WebSocketScope) -> dict[str, str]:
        headers_lowercase = {
            k.decode("utf-8").lower(): v.decode("utf-8") for k, v in scope["headers"]
        }
        return {k: v for k, v in headers_lowercase.items() if k in self._logged_headers}
