import pytest
from alembic.config import Config

from app.settings import Settings


@pytest.fixture
def alembic_cfg(settings_with_new_db: Settings) -> Config:
    """Alembic config for a new database"""
    cfg = Config(settings_with_new_db.db.alembic_ini_path)
    cfg.set_main_option("is_testing", "True")
    cfg.set_main_option(
        "sqlalchemy.url",
        settings_with_new_db.db.to_url(
            drivername="postgresql+psycopg"
        ).render_as_string(hide_password=False),
    )
    return cfg
