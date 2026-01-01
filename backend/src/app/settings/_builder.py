from collections.abc import Callable

import yaml
from pydantic import (
    BaseModel,
    TypeAdapter,
)
from structlog.stdlib import get_logger

from app.services.aws.client import get_client
from app.settings._ssm_parameter import SsmParameter
from app.utils import cache, model_apply

_log = get_logger(__name__)


class SettingsBuilder[M: BaseModel]:
    """
    A class for building settings from a raw settings string in YAML.

    Fetches and replaces values for all Secret objects in the model.

    Usage:

    ```python
    class MySettings(BaseModel):
        my_secret: Secret[str]
        aws_region: str

    # Read raw settings from a file or environment variable
    raw_settings = ...

    # Build settings
    settings = SettingsBuilder(MySettings).build(raw_settings, lambda settings: settings.aws_region)
    ```
    """

    def __init__(self, model: type[M]) -> None:
        """
        Args:
            model: The Pydantic class to use for parsing.
        """
        self.model = model

    def build(
        self,
        raw_settings: str,
        aws_region_func: Callable[[M], str],
        ssm_prefix_func: Callable[[M], str],
    ) -> M:
        """
        Parse a string containing the settings in YAML, recursively fetch and set values on all SsmParameter objects in the resulting model, and returns it.

        Args:
            raw_settings: The raw settings string in YAML.
            aws_region_func: A function that takes the parsed settings and returns the AWS region to use for fetching secrets.
            ssm_prefix_func: A function that takes the parsed settings and returns the SSM prefix (without leading/trailing slashes) to use for fetching secrets. Typically the app name.
        """
        settings = self._parse_raw_settings(raw_settings)
        aws_region = aws_region_func(settings)
        ssm_prefix = ssm_prefix_func(settings)

        return model_apply(
            settings, SsmParameter, self._set_parameter, aws_region, ssm_prefix
        )

    def _parse_raw_settings(self, raw_settings: str) -> M:
        unparsed_yaml = yaml.safe_load(raw_settings)
        return TypeAdapter(self.model).validate_python(unparsed_yaml)

    def _set_parameter[T](
        self, parameter: SsmParameter[T], aws_region: str, ssm_prefix: str
    ) -> None:
        """Fetch the parameter specified by the ARN from AWS SSM Parameter Store, parse value corresponding to the key and and set it on the parameter object."""
        if parameter.override:
            return

        # Extract the type argument of the SsmParameter
        # TODO: Remove this once Pydantic supports extracting generic args from BaseModels
        # https://github.com/pydantic/pydantic/issues/3559
        type_ = parameter.__pydantic_generic_metadata__["args"][0]

        ta: TypeAdapter[T] = TypeAdapter(type_)

        path_to_parameter = f"/{ssm_prefix}/{parameter.path_from_parent()}"

        raw_value = self._get_parameter(path_to_parameter, aws_region)

        parameter._internal_value = ta.validate_python(raw_value)  # noqa: SLF001

    @cache
    def _get_parameter(self, path: str, region: str) -> str:
        """Fetch the parameter specified by the path from AWS SSM Parameter Store."""
        client = get_client("ssm", region)
        try:
            return (
                client.get_parameter(Name=path, WithDecryption=True)
                .get("Parameter", {})
                .get("Value", "{}")
            )
        except Exception:
            _log.error(f"Error fetching parameter {path} from SSM Parameter Store")
            raise
