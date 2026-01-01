from alembic.config import Config
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, status
from starlette.exceptions import HTTPException
from starlette.middleware.sessions import SessionMiddleware
from structlog.stdlib import get_logger

from app.api.route_map import RouteMap
from app.api.v1 import (
    auth,
    chats,
    dev,
    email,
    errors,
    generate,
    healthz,
    lorestones,
    stories,
    stream,
    stripe,
    subscription,
    users,
)
from app.api.v1.oauth import google
from app.app.exception_handlers.global_handler import log_uncaught_exception
from app.app.exception_handlers.http import http_exception_handler
from app.app.lifespan import (
    LifespanBuilder,
    add_stripe_api_key,
    create_and_migrate_db,
    init_dependencies,
)
from app.app.logging.setup import setup_logging
from app.app.middleware.cors import CORSErrorHandlingMiddleware
from app.app.middleware.log import HttpLogMiddleware
from app.models import ErrorDetail
from app.settings import (
    SessionSettings,
    Settings,
    get_commit_info,
)
from app.typedefs.env import Environment

_log = get_logger(__name__)


def create_app(
    settings: Settings,
    alembic_cfg: Config | None = None,
    *,
    only_routes: bool = False,
) -> FastAPI:
    """Initialize logging, routes, dependencies and middleware.

    Args:
        settings: Application settings. If not provided, settings will be loaded from environment.
        alembic_cfg: Alembic configuration for database migrations. If not provided, it will be loaded from settings.
        only_routes: If True, only add routes and skip adding middleware or exception handlers. Useful for OpenAPI generation.
    """

    _alembic_cfg = alembic_cfg or Config(settings.db.alembic_ini_path)
    _log.info("Settings loaded:\n%s", settings.model_dump_json(indent=2))
    commit_info = get_commit_info()

    lifespan = (
        LifespanBuilder()
        .add(create_and_migrate_db, _alembic_cfg)
        .add(init_dependencies, settings)
        .add(
            setup_logging,
            commit_info.COMMIT_SHA,
            settings.app.log_level,
            debug=settings.app.env == Environment.local,
        )
        .add(add_stripe_api_key, settings.stripe)
        .build()
    )

    app = FastAPI(
        title="Forgotten Tome",
        version=commit_info.COMMIT_SHA,
        root_path=settings.app.api_prefix,
        lifespan=lifespan,
        openapi_url="/openapi.json" if settings.is_local else None,
        responses={
            k: {"model": ErrorDetail}
            for k in [
                status.HTTP_400_BAD_REQUEST,
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
                status.HTTP_404_NOT_FOUND,
                status.HTTP_429_TOO_MANY_REQUESTS,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            ]
        },
    )

    _add_routes(app, is_dev=settings.is_local)

    if only_routes:
        return app

    _add_middleware(app, settings)

    # Global exception handler
    app.add_exception_handler(Exception, log_uncaught_exception)
    app.add_exception_handler(HTTPException, http_exception_handler)
    return app


def _add_routes(
    app: FastAPI,
    *,
    is_dev: bool,
) -> None:
    routers = [
        auth.router,
        chats.router,
        email.router,
        errors.router,
        healthz.router,
        lorestones.router,
        stripe.router,
        subscription.router,
        users.router,
        google.router,
        stream.router,
        generate.router,
        stories.router,
    ]

    if is_dev:
        routers.append(dev.router)

    for router in routers:
        app.include_router(router)


def _add_middleware(app: FastAPI, settings: Settings) -> None:
    """Add middleware to the app. The last middleware added is the first to run on a request, and the last to run on a response."""
    app.add_middleware(CorrelationIdMiddleware)
    app.add_middleware(
        HttpLogMiddleware,
        unlogged_paths=[
            f"{settings.app.api_prefix}{app.url_path_for(RouteMap.HEALTHZ)}"
        ],
    )
    _add_session_middleware(app, settings.session)
    _add_cors_middleware(app, settings)


def _add_session_middleware(app: FastAPI, s: SessionSettings) -> None:
    app.add_middleware(
        SessionMiddleware,
        secret_key=s.signing_key.value.get_secret_value(),
        session_cookie=s.cookie_name,
        max_age=s.max_age,
        same_site=s.same_site,
        https_only=s.secure,
    )


def _add_cors_middleware(app: FastAPI, settings: Settings) -> None:
    app.add_middleware(
        CORSErrorHandlingMiddleware,
        # HttpUrl adds a trailing slash, which causes CORSMiddleware to reject
        # https://github.com/pydantic/pydantic/issues/7186
        allow_origins=[str(settings.app.frontend_url).rstrip("/")],
        allow_methods=["*"],
        allow_headers=["X-Requested-With", "X-Request-ID"],
        expose_headers=["X-Request-ID"],
        allow_credentials=True,
    )
