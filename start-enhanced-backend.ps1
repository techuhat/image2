#!/usr/bin/env powershell
# Enhanced Backend Startup Script for Production
# Version 3.0 - Production Ready with Enhanced Features

Write-Host "🚀 Starting Enhanced PDF Toolkit Backend v3.0..." -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path "backend-env")) {
    Write-Host "❌ Virtual environment not found. Please run setup first." -ForegroundColor Red
    Write-Host "Run: ./deploy-simple.ps1" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "📦 Activating virtual environment..." -ForegroundColor Cyan
& .\backend-env\Scripts\Activate.ps1

# Check if enhanced dependencies are installed
Write-Host "� Checking enhanced dependencies..." -ForegroundColor Cyan

# Install additional dependencies for enhanced version
try {
    Write-Host "📥 Installing enhanced dependencies..." -ForegroundColor Yellow
    pip install psutil python-magic-bin
    Write-Host "✅ Enhanced dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Some enhanced dependencies failed to install. Continuing with basic features..." -ForegroundColor Yellow
}

# Set environment variables for production
$env:FLASK_APP = "src/backend/app_enhanced.py"
$env:FLASK_ENV = "production"
$env:PORT = "5000"
$env:SECRET_KEY = "production-secret-key-change-this"
$env:CACHE_SALT = "enhanced-cache-salt"

# Create necessary directories
Write-Host "� Creating directories..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path "cache" | Out-Null
New-Item -ItemType Directory -Force -Path "temp" | Out-Null
New-Item -ItemType Directory -Force -Path "uploads" | Out-Null
New-Item -ItemType Directory -Force -Path "logs" | Out-Null

Write-Host "🌟 Enhanced Features:" -ForegroundColor Magenta
Write-Host "  ✅ Advanced Security Validation" -ForegroundColor White
Write-Host "  ✅ Resource Monitoring" -ForegroundColor White
Write-Host "  ✅ Rate Limiting & Error Tracking" -ForegroundColor White
Write-Host "  ✅ Background Cache Cleanup" -ForegroundColor White
Write-Host "  ✅ Concurrent Operation Control" -ForegroundColor White
Write-Host "  ✅ Enhanced Error Handling" -ForegroundColor White
Write-Host "  ✅ System Health Monitoring" -ForegroundColor White

Write-Host ""
Write-Host "🔧 Configuration:" -ForegroundColor Blue
Write-Host "  📍 Backend: Enhanced Production v3.0" -ForegroundColor White
Write-Host "  🌐 Port: 5000" -ForegroundColor White
Write-Host "  🛡️ Security: Enhanced" -ForegroundColor White
Write-Host "  📊 Monitoring: Enabled" -ForegroundColor White
Write-Host "  🔄 Concurrency: 5 max operations" -ForegroundColor White

Write-Host ""
Write-Host "🌐 Starting server..." -ForegroundColor Green
Write-Host "📱 Frontend URL: https://techuhat.github.io/image2/" -ForegroundColor Cyan
Write-Host "🔗 API Health: http://localhost:5000/health" -ForegroundColor Cyan
Write-Host "📊 API Stats: http://localhost:5000/stats" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Blue

# Start the enhanced Flask application
try {
    python src/backend/app_enhanced.py
} catch {
    Write-Host "❌ Failed to start enhanced backend. Trying fallback..." -ForegroundColor Red
    Write-Host "🔄 Starting basic backend..." -ForegroundColor Yellow
    python src/backend/app.py
}

Write-Host "🛑 Enhanced backend stopped." -ForegroundColor Red
