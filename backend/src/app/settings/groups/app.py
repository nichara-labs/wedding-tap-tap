from pydantic import Field, HttpUrl

from app.settings._base import BaseModelNoExtra
from app.typedefs import Environment, LogLevel
from app.typedefs.settings import NoLeadingTrailingSlashes, PathPrefix


class AppSettings(BaseModelNoExtra):
    """General app settings."""

    ssm_prefix: NoLeadingTrailingSlashes = Field(
        description="Prefix for all SSM parameters used by the app, without leading/trailing slashes.",
        default="forgotten_tome",
    )
    api_prefix: PathPrefix = Field(
        validate_default=True,
        description="The URL prefix for all API endpoints, e.g. `/api`.). Should not end with a slash.",
        default="/api",
    )
    env: Environment
    log_level: LogLevel = "DEBUG"
    frontend_url: HttpUrl = Field(
        description="The frontend URL. Used for CORS, OAuth redirection after callback, etc."
    )
    frontend_app_url: HttpUrl = Field(
        description="The frontend URL for the actual product. The user is redirected here after OAuth login, app logout, or from the Stripe payment/billing portal."
    )
    backend_url: HttpUrl = Field(
        description="The backend URL, excluding the api prefix, e.g. https://domain.com"
    )
