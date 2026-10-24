$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $Python)) { throw 'Run scripts/setup.ps1 first.' }
Push-Location $ProjectRoot
try {
    & $Python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --no-access-log
    if ($LASTEXITCODE -ne 0) { throw 'Backend stopped with an error.' }
} finally { Pop-Location }
