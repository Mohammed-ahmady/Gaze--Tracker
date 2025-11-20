# Quick Start: Run with Comprehensive Logging

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Eye Tracking System - Comprehensive Logging Enabled" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Check if old calibration exists
if (Test-Path "calibration_15point.json" -or Test-Path "calibration_15point.pkl") {
    Write-Host "⚠️  Old calibration files detected!" -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Delete old calibration and start fresh? (y/n)"
    
    if ($response -eq 'y' -or $response -eq 'Y') {
        Remove-Item "calibration_15point.json" -ErrorAction SilentlyContinue
        Remove-Item "calibration_15point.pkl" -ErrorAction SilentlyContinue
        Write-Host "✓ Old calibration deleted" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Using existing calibration (may cause issues with new logging)" -ForegroundColor Yellow
    }
    Write-Host ""
}

# Run the tracker
Write-Host "Starting Eye Tracker..." -ForegroundColor Green
Write-Host "IMPORTANT TIPS:" -ForegroundColor Yellow
Write-Host "  - During calibration, LOOK AT each red circle with your EYES" -ForegroundColor White
Write-Host "  - Keep your HEAD still, only move your EYES" -ForegroundColor White
Write-Host "  - Pay special attention to TOP and BOTTOM points" -ForegroundColor White
Write-Host "  - Don't just stare at the center!" -ForegroundColor White
Write-Host ""
Write-Host "Press Q when done to generate analysis report" -ForegroundColor Cyan
Write-Host ""

python enhanced_tracker.py

# After tracker exits, show log location
Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Session Complete!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Find the most recent log directory
$logDirs = Get-ChildItem -Path "logs" -Directory -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending
if ($logDirs.Count -gt 0) {
    $latestLog = $logDirs[0].FullName
    Write-Host "📊 Logs saved to:" -ForegroundColor Cyan
    Write-Host "   $latestLog" -ForegroundColor White
    Write-Host ""
    Write-Host "📄 Quick Check:" -ForegroundColor Yellow
    Write-Host "   1. Read: $latestLog\analysis.txt" -ForegroundColor White
    Write-Host "   2. Check training errors (should be < 40px)" -ForegroundColor White
    Write-Host "   3. Review recommendations" -ForegroundColor White
    Write-Host ""
    
    # Show analysis.txt if it exists
    $analysisFile = Join-Path $latestLog "analysis.txt"
    if (Test-Path $analysisFile) {
        Write-Host "=" * 60 -ForegroundColor Green
        Write-Host "ANALYSIS REPORT:" -ForegroundColor Green
        Write-Host "=" * 60 -ForegroundColor Green
        Get-Content $analysisFile
        Write-Host ""
    }
    
    Write-Host "For detailed analysis guide, see README_LOGGING.md" -ForegroundColor Cyan
} else {
    Write-Host "⚠️  No log files found. Check for errors above." -ForegroundColor Yellow
}

Write-Host ""
