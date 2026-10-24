#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
test -x .venv/bin/python || { echo 'Run bash scripts/setup.sh first.' >&2; exit 2; }
echo '== Backend tests =='
.venv/bin/python -m pytest -q
echo '== Frontend unit tests and build =='
(cd frontend && npm test && npm run build)
echo '== Ollama status =='
if command -v ollama >/dev/null 2>&1; then ollama list || true; else echo 'Ollama unavailable: actual inference not verified.'; fi
echo 'Command checks finished. Live image inference still needs manual verification.'
