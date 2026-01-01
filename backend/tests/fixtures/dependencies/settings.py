from collections.abc import Callable
from typing import override

import pytest
from pydantic import BaseModel, SecretStr
from sqlalchemy import URL

from app.db.session import DatabaseSessionManager
from app.settings import DatabaseSettings, Settings, get_settings
from app.settings._builder import SettingsBuilder
from app.settings._ssm_parameter import SsmParameter
from app.utils import cache


class FakeSettingsBuilder[M: BaseModel](SettingsBuilder[M]):
    """Does not call AWS Secret Manager to validate secrets."""

    @override
    @cache
    def _get_parameter(self, path: str, region: str) -> str:
        return "10"  # Needs to be able to be interpreted as both an int/str


@pytest.fixture
def fake_settings_builder() -> FakeSettingsBuilder[Settings]:
    return FakeSettingsBuilder(Settings)


@pytest.fixture
def get_fake_settings(
    settings: Settings,
) -> Callable[[], Settings]:
    """Fake settings getter for FastAPI dependency, or as a drop-in replacement for get_settings."""

    def _get_fake_settings() -> Settings:
        return settings

    return _get_fake_settings


@pytest.fixture
def settings(
    fake_settings_builder: FakeSettingsBuilder[Settings],
) -> Settings:
    """Get application settings for testing."""
    return get_settings(fake_settings_builder)


@pytest.fixture
def settings_with_new_db(settings: Settings, new_db_url: URL) -> Settings:
    """Settings with the DB name replaced with a new one that does not exist."""
    _settings = settings.model_copy(deep=True)
    params = DatabaseSessionManager.validate_url(new_db_url)
    db_settings = DatabaseSettings(
        hostname=SsmParameter(override=params["host"]),
        hostname_unpooled=SsmParameter(override=params["host"]),
        name=SsmParameter(override=params["database"]),
        port=SsmParameter(override=params["port"]),
        username=SsmParameter(override=params["username"]),
        password=SsmParameter(override=SecretStr(params["password"])),
    )
    _settings.db = db_settings

    return _settings
