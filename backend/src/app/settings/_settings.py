from pathlib import Path

from pydantic import Base64Str, computed_field
from pydantic_settings import BaseSettings
from structlog.stdlib import get_logger

from app.settings._base import BaseModelNoExtra
from app.settings._builder import SettingsBuilder
from app.settings.groups.app import AppSettings
from app.settings.groups.auth import AuthSettings
from app.settings.groups.aws import AwsSettings
from app.settings.groups.db import DatabaseSettings
from app.settings.groups.llm import LlmSettings
from app.settings.groups.session import SessionSettings
from app.settings.groups.stripe import StripeSettings
from app.typedefs.env import Environment
from app.utils import cache

_logger = get_logger(__name__)


class Settings(BaseModelNoExtra):
    """
    Top level settings for the app.

    Regenerate JSON schema after making changes with `python scripts/schema.py schema.json`.
    """

    app: AppSettings
    auth: AuthSettings
    aws: AwsSettings
    db: DatabaseSettings
    session: SessionSettings
    stripe: StripeSettings
    llm: LlmSettings

    @computed_field
    @property
    def is_local(self) -> bool:
        """Whether we are running locally."""
        return self.app.env == Environment.local

    @computed_field
    @property
    def is_prod(self) -> bool:
        """Whether we are in production."""
        return self.app.env == Environment.prod


class CommitDetails(BaseSettings):
    """Env vars are automatically passed in via arguments on docker build."""

    COMMIT_SHA: str = "local"
    COMMIT_TIMESTAMP: float = 0


class _RawSettings(BaseSettings):
    """Settings read directly from an environment variable."""

    APP_SETTINGS_B64: Base64Str | None = None


@cache
def get_settings(builder: SettingsBuilder | None = None) -> Settings:
    """
    Build and return the app's settings. Value is cached.

    Checks for the following in order:
        - `APP_SETTINGS_B64` environment variable (in standard base64)
        - `env.yaml` in the root directory
    """
    _env = _RawSettings.model_validate({})

    if _env.APP_SETTINGS_B64:
        _logger.info("APP_SETTINGS_B64 is set, decoding...")
        raw_settings = _env.APP_SETTINGS_B64
    else:
        _logger.info("APP_SETTINGS_B64 is unset, loading from env.yaml instead")
        raw_settings = (
            Path(__file__).parent.parent.parent.parent / "env.yaml"
        ).read_text()

    _builder = builder or SettingsBuilder(Settings)

    return _builder.build(
        raw_settings=raw_settings,
        aws_region_func=lambda s: s.aws.region,
        ssm_prefix_func=lambda s: s.app.ssm_prefix,
    )


@cache
def get_commit_info() -> CommitDetails:
    """Return commit information."""
    return CommitDetails.model_validate({})
