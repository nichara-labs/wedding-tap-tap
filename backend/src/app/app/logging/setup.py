import logging

import alembic
import structlog
from structlog.processors import ExceptionRenderer
from structlog.tracebacks import ExceptionDictTransformer
from structlog.typing import Processor

import app
from app.app.logging.processors import (
    add_correlation,
    add_git_commit,
    drop_color_message_key,
)


async def setup_logging(
    commit_sha: str,
    log_level: str,
    *,
    debug: bool = False,
) -> None:
    """
    Set up logging for the application.

    Args:
        commit_sha: The git commit SHA to include in logs.
        log_level: The log level to use.
        debug: If true, logs to console and does not cache the logger (so we can capture logs). Otherwise, logs as JSON and caches the created logger.

    Logging can subsequently be done via:

    ```python
    from structlog.stdlib import get_logger

    _log = get_logger()
    _log.info("Hello, world!")
    # 2025-01-02T10:12:23.598378Z [info     ] Hello, world!                  filename=entrypoint.py func_name=create_app lineno=26
    ```
    """

    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        drop_color_message_key,
        add_correlation,
        add_git_commit(commit_sha),
        # Replace an exc_info field with an exception string field using Python's built-in traceback formatting.
        # Without this, we'd get a Traceback object in exc_info instead.
        # https://www.structlog.org/en/stable/api.html#structlog.processors.format_exc_info
        structlog.processors.format_exc_info
        if debug
        # When not in debug, capture structured stack traces without traversing potentially detached ORM locals.
        else ExceptionRenderer(
            ExceptionDictTransformer(show_locals=False, use_rich=False)
        ),
    ]

    # The BoundLogger that is returned by structlog.get_logger().
    wrapper_class = structlog.make_filtering_bound_logger(
        logging.getLevelNamesMapping()[log_level]
    )

    structlog.configure(
        processors=[
            *processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=wrapper_class,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=not debug,
    )

    renderer = (
        # Don't print verbose exception tracebacks
        structlog.dev.ConsoleRenderer(exception_formatter=structlog.dev.plain_traceback)
        if debug
        else structlog.processors.JSONRenderer()
    )

    _configure_uvicorn_logging()
    _set_structlog_as_root_logger_handler(processors=processors, renderer=renderer)

    # We set different logging levels for library code and our code
    # https://www.electricmonk.nl/log/2017/08/06/understanding-pythons-logging-module/
    logging.getLogger().setLevel(logging.WARNING)  # Library code, including SQLALchemy
    logging.getLogger(app.__name__).setLevel(log_level)
    logging.getLogger(alembic.__name__).setLevel(log_level)


def _configure_uvicorn_logging() -> None:
    """
    Configure logging for uvicorn.

    Stops uvicorn.access logs from propagating, and routes other uvicorn log types to our root logger.
    """
    # Clear log handlers for uvicorn
    for _log in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        logging.getLogger(_log).handlers.clear()

    # Allow propagation of uvicorn logs to our structlog root logger
    for _log in ["uvicorn", "uvicorn.error"]:
        logging.getLogger(_log).propagate = True

    # Disable uvicorn access log propagation as we log them ourselves in our logging middleware.
    logging.getLogger("uvicorn.access").propagate = False


def _set_structlog_as_root_logger_handler(
    processors: list[Processor], renderer: Processor
) -> None:
    """
    Configure structlog as our root logger, which will be used for all structlog and stdlib logs.

    `processors`: List of Processors to be used for logging entries which do NOT originate within structlog
    `renderer`: Processor to be used for rendering the final log line.

    See https://www.structlog.org/en/stable/standard-library.html#rendering-using-structlog-based-formatters-within-logging
    """

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=processors,  # These run ONLY on `logging` entries that do NOT originate within structlog
        processors=[
            # # Remove _record & _from_structlog.
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)  # Root logger
