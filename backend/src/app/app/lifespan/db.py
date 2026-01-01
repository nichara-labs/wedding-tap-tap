from alembic import command
from alembic.config import Config
from structlog.stdlib import get_logger

_log = get_logger(__name__)


async def create_and_migrate_db(
    alembic_cfg: Config,
) -> None:
    """Create the DB and run pending migrations."""

    # This executes env.py, which creates the DB and runs pending migrations
    _log.info("Running migrations")
    command.upgrade(alembic_cfg, "head")
