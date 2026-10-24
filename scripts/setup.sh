#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"
PYTHON_BIN="${THOORIGA_PYTHON:-python3.12}"
command -v "$PYTHON_BIN" >/dev/null || { echo 'Python 3.12 is required. Install it or set THOORIGA_PYTHON to its executable.' >&2; exit 1; }
command -v node >/dev/null || { echo 'Install Node.js 22 or newer.' >&2; exit 1; }
command -v npm >/dev/null || { echo 'npm is required; install Node.js with npm.' >&2; exit 1; }
"$PYTHON_BIN" -c 'import sys; assert sys.version_info[:2] == (3, 12), "Use Python 3.12 for the pinned environment"'
node -e 'if (Number(process.versions.node.split(".")[0]) < 22) { console.error("Node.js 22 or newer is required"); process.exit(1); }'
if [[ ! -e .venv ]]; then "$PYTHON_BIN" -m venv .venv; fi
[[ -x .venv/bin/python ]] || { echo 'The .venv directory is not a usable Linux environment. Remove only this project .venv and rerun setup.' >&2; exit 1; }
.venv/bin/python -c 'import sys; assert sys.version_info[:2] == (3, 12), "Recreate this project .venv with Python 3.12"'
.venv/bin/python -m pip install -r requirements.txt
(cd frontend && npm ci)
echo 'Dependencies installed. Install Ollama separately, then run: ollama pull gemma3:4b'
echo 'Start backend: bash scripts/start-backend.sh'
echo 'Start frontend in another terminal: bash scripts/start-frontend.sh'
