#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
test -f frontend/dist/index.html || { echo 'Build first: (cd frontend && npm run build)' >&2; exit 2; }
test -x .venv/bin/python || { echo 'Run bash scripts/setup.sh first.' >&2; exit 2; }
echo 'Private local deployment: http://127.0.0.1:8000'
exec .venv/bin/python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --no-access-log
