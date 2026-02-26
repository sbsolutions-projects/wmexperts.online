# WMexperts Index Updater - PowerShell Script
# Run this script to update the index page with the latest blog posts

Write-Host "Updating WMexperts index page..." -ForegroundColor Cyan

# Check if Python is installed
$pythonVersion = python --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Python version: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Run the update script
python update-index.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Error occurred during index update" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
} else {
    Write-Host ""
    Write-Host "✅ Index page updated successfully!" -ForegroundColor Green
}

Read-Host "Press Enter to exit"
