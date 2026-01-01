from alembic import context
from sqlalchemy import URL
from sqlalchemy.engine import create_engine
from sqlalchemy_utils import create_database, database_exists
from structlog.stdlib import get_logger

from app.db.schema.base import Base
from app.settings import get_settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Logging is configured in the application, not here.

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:

_logger = get_logger(__name__)


def get_url() -> URL | str:
    """Get the database URL from the environment."""
    if config.get_main_option("is_testing", "False") == "True":
        url = config.get_main_option("sqlalchemy.url")
        if not url:
            raise ValueError
        return url
    db_s = get_settings().db
    return URL.create(
        drivername="postgresql+psycopg",
        username=db_s.username.value,
        password=db_s.password.value.get_secret_value(),
        host=db_s.hostname_unpooled.value,
        port=db_s.port.value,
        database=db_s.name.value,
    )


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine, though an Engine is acceptable here as well.  By skipping the Engine creation we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the script output.
    """

    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    url = get_url()
    connectable = create_engine(url)
    if not database_exists(url):
        _logger.info(
            "Creating database %s as it does not exist",
            url.database if isinstance(url, URL) else url,
        )
        create_database(url)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()
    _logger.info("Migrations completed")


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
