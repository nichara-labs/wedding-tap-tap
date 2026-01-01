import argparse
import json
from pathlib import Path

import yaml
from fastapi.openapi.utils import get_openapi

from app.entrypoint import create_app
from app.settings import Settings


def _generate_openapi_spec(p: Path, settings_yaml: Path) -> None:
    unparsed_yaml = yaml.safe_load(settings_yaml.read_text())
    app = create_app(Settings.model_validate(unparsed_yaml), only_routes=True)

    with p.open("w") as f:
        openapi_spec = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            routes=app.routes,
        )
        json.dump(openapi_spec, f, indent=2)


if __name__ == "__main__":
    """Print the OpenAPI spec."""
    parser = argparse.ArgumentParser(description="Generate OpenAPI spec")
    parser.add_argument(
        "output",
        type=str,
        help="Output file path",
    )
    parser.add_argument(
        "settings",
        type=str,
        help="Path to an applications settings.yaml file used to initialize the app",
    )
    args = parser.parse_args()
    output = Path(args.output)
    settings_yaml = Path(args.settings)
    _generate_openapi_spec(output, settings_yaml)
    print(f"Generated OpenAPI spec at {output}")  # noqa: T201
