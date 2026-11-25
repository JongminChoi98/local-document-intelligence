#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$PROJECT_ROOT/config/open-webui/.env"

if [[ ! -f "$ENV_FILE" ]]; then
    echo "Environment file not found: $ENV_FILE"
    exit 1
fi

set -a
source "$ENV_FILE"
set +a

export DATA_DIR="$PROJECT_ROOT/storage/open-webui"

mkdir -p "$DATA_DIR"
cd "$DATA_DIR"

exec open-webui serve --host 127.0.0.1 --port 8080
