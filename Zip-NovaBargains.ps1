# PowerShell Script to Package NovaBargains Folder

# Set your project path
$projectPath = "$env:USERPROFILE\Desktop\NovaEmpire\NovaBargains"
$zipPath = "$env:USERPROFILE\Desktop\NovaBargains.zip"

# Move to project directory
Set-Location -Path $projectPath

# Remove old ZIP if it exists
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
    Write-Host "Old ZIP archive removed."
}

# Create new ZIP archive including all core files and 'data' folder
Compress-Archive -Path @(
    "$projectPath\app.py",
    "$projectPath\database.py",
    "$projectPath\models.py",
    "$projectPath\requirements.txt",
    "$projectPath\README.md",
    "$projectPath\data\*"
) -DestinationPath $zipPath

# Final confirmation
if (Test-Path $zipPath) {
    Write-Host "`n✅ NovaBargains.zip created at: $zipPath" -ForegroundColor Green
} else {
    Write-Host "`n❌ Failed to create ZIP archive." -ForegroundColor Red
}
