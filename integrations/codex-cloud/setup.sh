#!/usr/bin/env bash
set -euo pipefail

: "${PROJECT_GUIDES_COMMIT:?Set PROJECT_GUIDES_COMMIT to the full 40-character commit SHA to install.}"

script_dir=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
exec "$script_dir/maintenance.sh" "$PROJECT_GUIDES_COMMIT"
