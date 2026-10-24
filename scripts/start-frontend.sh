#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
[[ -d "$PROJECT_ROOT/frontend/node_modules" ]] || { echo 'Run bash scripts/setup.sh first.' >&2; exit 1; }
cd "$PROJECT_ROOT/frontend"
exec npm run dev
