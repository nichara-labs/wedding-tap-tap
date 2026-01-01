#! /usr/bin/env bash
set -euo pipefail

OPENAPI_SPEC_PATH=/tmp/openapi.json

# Relative to the scripts/ directory
SETTINGS_YAML=../iac/backend/prod.env.yaml

# Relative to frontend/
TS_OUT_PATH=src/types/schema.d.ts

# cd to the project root directory
parent_path=$(
    cd "$(dirname "${BASH_SOURCE[0]}")"
    pwd -P
)
cd "${parent_path}/.."

uv run --directory backend scripts/openapi.py "$OPENAPI_SPEC_PATH" "$SETTINGS_YAML"

cd frontend

pnpm exec openapi-typescript "$OPENAPI_SPEC_PATH" --output "$TS_OUT_PATH"
