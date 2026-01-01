import pytest
from alembic import command
from alembic.config import Config
from alembic.util.exc import CommandError
from fastapi.testclient import TestClient
from sqlalchemy import URL
from sqlalchemy_utils import database_exists

from app.entrypoint import create_app
from app.settings import Settings

pytestmark = pytest.mark.anyio


class TestCreateMigrateDb:
    def test_db_created_if_not_exists(
        self, settings_with_new_db: Settings, new_db_url: URL, alembic_cfg: Config
    ) -> None:
        """Test that the DB is created on app initialization, if it does not exist."""
        assert not database_exists(new_db_url)

        # Entering the TestClient context manager triggers the lifespan functions
        with TestClient(create_app(settings_with_new_db, alembic_cfg=alembic_cfg)):
            assert database_exists(new_db_url)

    def test_migrations_applied_blank_db(
        self, alembic_cfg: Config, settings_with_new_db: Settings
    ) -> None:
        """Test that migrations are applied to a blank db"""
        with pytest.raises(CommandError, match="Target database is not up to date"):
            command.check(alembic_cfg)
        with TestClient(create_app(settings_with_new_db, alembic_cfg)):
            command.check(alembic_cfg)
