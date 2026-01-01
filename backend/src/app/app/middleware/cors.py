from starlette.datastructures import Headers
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.types import Receive, Scope, Send
from structlog.stdlib import get_logger

import app
from app.models import ErrorDetail

_log = get_logger(f"{app.__name__}.middleware.CORSErrorHandlingMiddleware")


class CORSErrorHandlingMiddleware(CORSMiddleware):
    """
    CORSMiddleware, with a patched `simple_response()` that catches exceptions during response handling and returns a 500 response with the required CORS headers added. Exceptions are re-raised.

    This fixes the default behavior of ServerErrorMiddleware not adding CORS headers on unhandled exceptions from cross-origin requests.

    Written as a Pure ASGI Middleware, to overcome limitations with BaseHTTPMiddleware [not propagating ContextVars]((https://www.starlette.io/middleware/#limitations)).
    """

    async def simple_response(
        self, scope: Scope, receive: Receive, send: Send, request_headers: Headers
    ) -> None:
        """Note that this handle will only be used for cross-origin requests."""
        try:
            await super().simple_response(scope, receive, send, request_headers)
        except Exception:
            _log.error(
                "Handling exception from cross-origin request",
                path=Request(scope).url.path,
            )

            # Since the application threw an exception, there are no response content messages to base upon, so we write our own.
            await self.send(
                {"type": "http.response.start", "status": 500, "more_body": False},
                send,
                request_headers,
            )
            await self.send(
                {
                    "type": "http.response.body",
                    "body": ErrorDetail(
                        detail="Internal Server Error (cross-origin request)",
                        status_code=500,
                    )
                    .model_dump_json()
                    .encode(),
                    "more_body": False,
                },
                send,
                request_headers,
            )

            # Reraise the exception. This allows our global exception handler to log the error, or for test clients to raise the error within the test case.
            raise
