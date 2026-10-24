"""Dependency-free release sanity checks; does not stand in for live AI testing."""
from pathlib import Path
import hashlib
import sys

root = Path(__file__).resolve().parents[1]
required = [
    '.github/workflows/ci.yml', '.github/workflows/pages.yml',
    'frontend/package-lock.json', 'frontend/package.json',
    'frontend/src/main.tsx', 'frontend/public/logo.png', 'frontend/public/favicon.png',
    'backend/app.py', 'backend/samples/ATTRIBUTION.md',
    'requirements.txt', 'README.md', 'LICENSE', 'PRIVACY.md',
    'THIRD_PARTY_NOTICES.md', 'CONTRIBUTING.md', 'SECURITY.md',
    'docs/HACKTOBERFEST_SUBMISSION.md', 'docs/DEV_ARTICLE.md',
    'scripts/verify.ps1', 'scripts/verify.sh', 'site/index.html',
]
missing = [path for path in required if not (root / path).is_file()]
if missing:
    print('Missing required project files:', *missing, sep='\n  - ', file=sys.stderr)
    sys.exit(1)
if (root / '.env').exists() or (root / '.venv').exists() or (root / 'frontend/node_modules').exists():
    print('Working directories or secrets must be excluded from source release packaging.', file=sys.stderr)
    sys.exit(1)
logo = (root / 'frontend/public/logo.png').read_bytes()
public_logo = (root / 'site/assets/logo.png').read_bytes()
assert logo == public_logo, 'App and showcase logo disagree'
assert (root / 'frontend/public/favicon.png').read_bytes() == (root / 'site/assets/favicon.png').read_bytes(), 'App and showcase favicons disagree'
print(f'PASS release audit: {len(required)} expected files; consistent branding; logo SHA256 {hashlib.sha256(logo).hexdigest()[:12]}')
print('NOT CHECKED: npm install, real Ollama/Gemma inference, laptop privacy audit, or live hosting.')
