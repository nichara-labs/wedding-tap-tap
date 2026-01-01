import argparse
import json
from pathlib import Path

from app.settings._settings import Settings


def _generate_schema() -> str:
    schema = Settings.model_json_schema()
    return json.dumps(schema, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate the schema for the application settings"
    )
    parser.add_argument("output", type=str, help="Output file path for the schema")
    args = parser.parse_args()
    with Path.open(args.output, "w") as f:
        f.write(_generate_schema() + "\n")
        print(f"Schema written to {args.output}")  # noqa: T201
