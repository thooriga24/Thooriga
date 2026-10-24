#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"
[[ -x .venv/bin/python ]] || { echo 'Run bash scripts/setup.sh first.' >&2; exit 1; }
exec .venv/bin/python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --no-access-log
