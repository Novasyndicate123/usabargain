# NovaBargains Full Runner Script - PowerShell

$projectPath = "$env:USERPROFILE\Desktop\NovaBargains"
$venvActivate = "$projectPath\venv\Scripts\Activate.ps1"
$scraperScript = "$projectPath\scraper_live.py"
$initDbScript = "$projectPath\init_db.py"
$logDir = "$projectPath\logs"
$logFile = "$logDir\scraper_log_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"

Set-Location -Path $projectPath

if (!(Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir | Out-Null
}

if (!(Test-Path $venvActivate)) {
    Write-Host "ERROR: Virtual environment not found at $venvActivate" -ForegroundColor Red
    exit 1
}

Write-Host "Activating NovaBargains virtual environment..." -ForegroundColor Green
& $venvActivate

Write-Host "Running database initialization..." -ForegroundColor Cyan
python $initDbScript

Write-Host "Running scraper_live.py..." -ForegroundColor Cyan
python $scraperScript 2>&1 | Tee-Object -FilePath $logFile -Append

Write-Host "Done. Logs saved to $logFile" -ForegroundColor Green
