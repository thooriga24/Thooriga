$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path (Join-Path $ProjectRoot 'frontend\node_modules'))) { throw 'Run scripts/setup.ps1 first.' }
if (-not (Get-Command npm.cmd -ErrorAction SilentlyContinue)) { throw 'Install Node.js with npm.' }
Push-Location (Join-Path $ProjectRoot 'frontend')
try {
    & npm.cmd run dev
    if ($LASTEXITCODE -ne 0) { throw 'Frontend stopped with an error.' }
} finally { Pop-Location }
