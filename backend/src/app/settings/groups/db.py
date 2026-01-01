from pathlib import Path

from pydantic import Field, FilePath, SecretStr
from sqlalchemy import URL

from app.settings._base import BaseModelNoExtra
from app.settings._ssm_parameter import SsmParameter


class DatabaseSettings(BaseModelNoExtra):
    hostname: SsmParameter[str]
    hostname_unpooled: SsmParameter[str] = Field(
        description="Hostname to connect to the DB without connection pooling. Used for migrations."
    )
    name: SsmParameter[str]
    port: SsmParameter[int]
    username: SsmParameter[str]
    password: SsmParameter[SecretStr]
    alembic_ini_path: FilePath = Field(
        default=Path("alembic.ini"),
        description="Path to the alembic.ini file, relative to the project root",
    )

    def to_url(self, drivername: str) -> URL:
        return URL.create(
            drivername=drivername,
            username=self.username.value,
            password=self.password.value.get_secret_value(),
            host=self.hostname.value,
            port=self.port.value,
            database=self.name.value,
        )
