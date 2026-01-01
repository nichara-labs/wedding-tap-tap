import pytest
from alembic.config import Config
from fastapi.testclient import TestClient

from app.entrypoint import create_app
from app.settings import Settings


def test_alembic_logs(
    alembic_cfg: Config,
    settings_with_new_db: Settings,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """
    Test that alembic logs are captured by the logger.

    Note that since Alembic logs to the standard logging module, we use the pytest caplog fixture instead of structlog's.
    """
    with TestClient(create_app(settings_with_new_db, alembic_cfg)):
        assert any(log.name == "alembic.runtime.migration" for log in caplog.records)
