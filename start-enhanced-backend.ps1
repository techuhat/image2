#!/usr/bin/env pwsh
# Enhanced Backend Startup Script

Write-Host "🚀 Starting Enhanced PDF Toolkit Backend..." -ForegroundColor Green

Set-Location "D:\toolkit-main\src\backend"

Write-Host "📍 Current Location: $(Get-Location)" -ForegroundColor Yellow
Write-Host "🐍 Python Path: D:\toolkit-main\backend-env\Scripts\python.exe" -ForegroundColor Yellow

# Start the enhanced backend
& "D:\toolkit-main\backend-env\Scripts\python.exe" "app_enhanced.py"
