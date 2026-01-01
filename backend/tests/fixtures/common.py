import urllib.parse
from base64 import standard_b64encode
from collections.abc import AsyncGenerator, Callable
from pathlib import Path
from typing import TypedDict

import pytest
from fastapi import Depends, FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dev import _DevLoginParams
from app.app.dependencies._db import _get_db_session
from app.app.dependencies._oauth import _get_google_provider
from app.app.dependencies._settings import _get_settings
from app.app.exception_handlers import global_handler
from app.db.schema import User
from app.db.session import DatabaseSessionManager
from app.entrypoint import create_app
from app.services.oauth.google import GoogleProvider
from app.settings import Settings
from app.settings._settings import _RawSettings

pytestmark = pytest.mark.anyio

TEST_ENV_YAML_PATH = Path(__file__).parent.parent / "test.env.yaml"
"""Path to the yaml file containing settings for testing."""


@pytest.fixture
def dev_login_url() -> str:
    return "/v1/dev/login"


@pytest.fixture
async def app(
    get_fake_settings: Callable[[], Settings],
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
    db_session: AsyncSession,
    db_session_manager: DatabaseSessionManager,
    google_provider: GoogleProvider,
) -> FastAPI:
    """A FastAPI instance with fake dependencies"""

    app = create_app(settings)
    app.dependency_overrides[_get_db_session] = lambda: db_session
    app.dependency_overrides[_get_settings] = get_fake_settings
    app.dependency_overrides[_get_google_provider] = lambda: google_provider

    # Patch the global exception handler to use the test database session manager, as it doesn't use dependency_overrides
    monkeypatch.setattr(
        global_handler,
        "db_session_manager_dependency",
        Depends(lambda: db_session_manager),
    )

    return app


@pytest.fixture
async def client(app: FastAPI, settings: Settings) -> AsyncGenerator[AsyncClient]:
    """
    A test client for making requests.

    Note: Lifespan functions are NOT called: entering the context manager of AsyncClient does not trigger lifespan functions on the app, unlike TestClient.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=urllib.parse.urljoin(
            "https://test", settings.app.api_prefix
        ),  # Must be https otherwise our cookie with Secure=True won't work
    ) as ac:
        yield ac


class ClientWithLogin(TypedDict):
    client: AsyncClient
    user: User


@pytest.fixture
async def client_with_login(
    client: AsyncClient, user: User, dev_login_url: str
) -> ClientWithLogin:
    """Returns a logged-in client and the user that was created."""
    await client.post(
        dev_login_url,
        params=_DevLoginParams(
            provider=user.provider,
            sub=user.sub,
            email=user.email,
            name=user.name,
        ).model_dump(),
    )
    return {"client": client, "user": user}


@pytest.fixture(autouse=True)
def prevent_aws_calls(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure that we never use the real AWS credentials by setting environment variables to dummy values (Boto3 preferentially reads from environment variables, even if `~/.aws/credentials` is present)."""

    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_SECURITY_TOKEN", "testing")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "testing")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")

    monkeypatch.setenv(
        next(iter(_RawSettings.model_fields.keys())),
        standard_b64encode(TEST_ENV_YAML_PATH.read_bytes()).decode(),
    )


@pytest.fixture(autouse=True)
def load_settings_into_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Load settings from the yaml file containing test settings into the app settings environment key."""
    monkeypatch.setenv(
        next(iter(_RawSettings.model_fields.keys())),
        standard_b64encode(TEST_ENV_YAML_PATH.read_bytes()).decode(),
    )
