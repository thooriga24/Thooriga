$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $PSScriptRoot
if (-not (Get-Command py -ErrorAction SilentlyContinue)) { throw 'Install Python 3.12 with the Windows Python launcher (py).' }
if (-not (Get-Command node -ErrorAction SilentlyContinue)) { throw 'Install Node.js 22 or newer.' }
if (-not (Get-Command npm.cmd -ErrorAction SilentlyContinue)) { throw 'npm.cmd is required; install Node.js with npm.' }
Push-Location $ProjectRoot
try {
    & py -3.12 -c "import sys; assert sys.version_info[:2] == (3, 12), 'Python 3.12 required'"
    if ($LASTEXITCODE -ne 0) { throw 'Python 3.12 was not found.' }
    & node -e "if (Number(process.versions.node.split('.')[0]) < 22) { console.error('Node.js 22 or newer is required'); process.exit(1); }"
    if ($LASTEXITCODE -ne 0) { throw 'Upgrade Node.js before running setup.' }
    if (-not (Test-Path '.venv')) {
        & py -3.12 -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw 'Could not create the Python virtual environment.' }
    }
    $Python = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
    if (-not (Test-Path $Python)) { throw 'This project .venv is not a Windows environment. Remove only this project .venv and rerun setup.' }
    & $Python -c "import sys; assert sys.version_info[:2] == (3, 12), 'Recreate this project .venv with Python 3.12'"
    if ($LASTEXITCODE -ne 0) { throw 'The virtual environment must use Python 3.12.' }
    & $Python -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw 'Python dependency installation failed.' }
    Push-Location (Join-Path $ProjectRoot 'frontend')
    try {
        & npm.cmd ci
        if ($LASTEXITCODE -ne 0) { throw 'Frontend dependency installation failed.' }
    } finally { Pop-Location }
    Write-Host 'Dependencies installed. Install Ollama separately, then run: ollama pull gemma3:4b'
    Write-Host 'Start backend and frontend in separate terminals using the scripts in scripts/.'
} finally { Pop-Location }
