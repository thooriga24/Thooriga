$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $Python)) { throw 'Run scripts\setup.ps1 first.' }
if (-not (Test-Path (Join-Path $ProjectRoot 'frontend\dist\index.html'))) { throw 'Build the UI first: cd frontend; npm.cmd run build' }
Push-Location $ProjectRoot
try {
    Write-Host 'Thooriga production UI + API: http://127.0.0.1:8000'
    Write-Host 'AI model: Ollama must be running locally at 127.0.0.1:11434'
    & $Python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --no-access-log
} finally { Pop-Location }
