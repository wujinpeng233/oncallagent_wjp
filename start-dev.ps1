# Start dev environment: MySQL + FastAPI. Fail fast on any error.

$ErrorActionPreference = "Stop"

$projectDir = $PSScriptRoot
$python = "C:\Users\30521\.conda\envs\fastapi\python.exe"
$appPort = 8000

Set-Location -LiteralPath $projectDir

# 1. Check Docker engine
cmd /c "docker info >nul 2>&1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Docker engine is not running. Start Docker Desktop first." -ForegroundColor Red
    exit 1
}
Write-Host "[1/3] Docker engine OK" -ForegroundColor Green

# 2. Start MySQL and wait until ready (max 60s)
Write-Host "[2/3] Starting MySQL..."
docker compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] docker compose up -d failed with exit code $LASTEXITCODE" -ForegroundColor Red
    exit 1
}

$ready = $false
for ($i = 1; $i -le 30; $i++) {
    cmd /c "docker exec oncall-agent-mysql mysqladmin ping -uoncall -poncall --silent >nul 2>&1"
    if ($LASTEXITCODE -eq 0) {
        $ready = $true
        break
    }
    Start-Sleep -Seconds 2
}
if (-not $ready) {
    Write-Host "[ERROR] MySQL not ready within 60s. Check: docker compose ps" -ForegroundColor Red
    exit 1
}
Write-Host "      MySQL is ready" -ForegroundColor Green

# 3. Start FastAPI in foreground (Ctrl+C to stop)
Write-Host "[3/3] Starting FastAPI on port $appPort ..."
& $python -m uvicorn main:app --reload --host 127.0.0.1 --port $appPort
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Uvicorn exited with code $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}
