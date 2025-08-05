
$ScriptPath = "$env:USERPROFILE\Desktop\NovaBargains\scraper_live.ps1"
$PythonScript = "$env:USERPROFILE\Desktop\NovaBargains\scraper_live.py"
$ActivateVenv = "$env:USERPROFILE\Desktop\NovaBargains\venv\Scripts\Activate.ps1"

$ScriptContent = @"
& '$ActivateVenv'
python "$PythonScript"
"@

Set-Content -Path $ScriptPath -Value $ScriptContent
Write-Output "✅ Scraper launcher saved to $ScriptPath"
