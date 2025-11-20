# GazeAssist Setup Script for Windows (PowerShell)
# Automatically creates virtual environment and installs dependencies

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "               GazeAssist Smart Setup (Windows)                      " -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.9-3.12 from https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

# Extract version number
if ($pythonVersion -match "Python 3\.(\d+)") {
    $minorVersion = [int]$matches[1]
    
    if ($minorVersion -ge 7 -and $minorVersion -le 12) {
        Write-Host "Python version is compatible!" -ForegroundColor Green
    } elseif ($minorVersion -ge 13) {
        Write-Host ""
        Write-Host "WARNING: Python 3.13+ is not supported by MediaPipe!" -ForegroundColor Red
        Write-Host "Please install Python 3.11 or 3.12 instead." -ForegroundColor Yellow
        Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
        Write-Host ""
        exit 1
    } else {
        Write-Host "WARNING: Python 3.$minorVersion is too old. Please use 3.9-3.12" -ForegroundColor Yellow
    }
} else {
    Write-Host "Could not detect Python version. Continuing anyway..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Choose installation method:" -ForegroundColor White
Write-Host "  [1] Quick Install (system-wide packages)" -ForegroundColor White
Write-Host "  [2] Virtual Environment (recommended - isolated packages)" -ForegroundColor White
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
$choice = Read-Host "Enter choice (1 or 2)"

if ($choice -eq "2") {
    Write-Host ""
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Virtual environment created!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Activating virtual environment..." -ForegroundColor Yellow
        & ".\venv\Scripts\Activate.ps1"
        Write-Host "Virtual environment activated!" -ForegroundColor Green
    } else {
        Write-Host "Failed to create virtual environment!" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "Running smart installer..." -ForegroundColor Yellow
python install_smart.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=====================================================================" -ForegroundColor Green
    Write-Host "                    Setup Complete!                                  " -ForegroundColor Green
    Write-Host "=====================================================================" -ForegroundColor Green
    Write-Host ""
    
    if ($choice -eq "2") {
        Write-Host "IMPORTANT: Virtual environment is active!" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "To run GazeAssist in the future:" -ForegroundColor White
        Write-Host "  1. Activate environment: .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
        Write-Host "  2. Run program: python version1\main.py" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "To deactivate: deactivate" -ForegroundColor White
    } else {
        Write-Host "To run GazeAssist:" -ForegroundColor White
        Write-Host "  Version 1: python version1\main.py" -ForegroundColor Cyan
        Write-Host "  Version 2: python version2\enhanced_tracker.py" -ForegroundColor Cyan
    }
    Write-Host ""
    Write-Host "First time? Test your camera:" -ForegroundColor Yellow
    Write-Host "  python scripts\test_camera.py" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "Setup failed! Check errors above." -ForegroundColor Red
    Write-Host ""
    exit 1
}
