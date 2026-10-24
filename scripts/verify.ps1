$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $Python)) { throw 'Missing .venv. Run scripts\setup.ps1 first.' }
Push-Location $ProjectRoot
try {
    Write-Host '== Backend tests =='
    & $Python -m pytest -q
    if ($LASTEXITCODE -ne 0) { throw 'Backend tests failed' }
    Write-Host '== Frontend unit tests and build =='
    Push-Location (Join-Path $ProjectRoot 'frontend')
    try {
        & npm.cmd test
        if ($LASTEXITCODE -ne 0) { throw 'Frontend tests failed' }
        & npm.cmd run build
        if ($LASTEXITCODE -ne 0) { throw 'Frontend build failed' }
    } finally { Pop-Location }
    Write-Host '== Ollama status =='
    if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
        Write-Warning 'Ollama not installed. Actual Gemma inference unverified.'
    } else {
        & ollama list
        try { $response = Invoke-RestMethod http://127.0.0.1:11434/api/tags -TimeoutSec 5; Write-Host ('Available models: ' + ($response.models.name -join ', ')) }
        catch { Write-Warning 'Ollama server offline or not reachable on loopback.' }
    }
    Write-Host 'Build and test command checks complete. Image-dependent inference still requires an in-app live test.'
} finally { Pop-Location }
