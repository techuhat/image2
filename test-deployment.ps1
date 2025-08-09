# Azure App Test Script
param(
    [string]$AppUrl = "https://imagetool-h4dmewahfmg4bkej.eastasia-01.azurewebsites.net"
)

Write-Host "🧪 Testing Azure App: $AppUrl" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Gray

$endpoints = @(
    "/ping",
    "/health", 
    "/"
)

foreach ($endpoint in $endpoints) {
    $url = $AppUrl + $endpoint
    Write-Host "Testing: $url" -ForegroundColor Yellow
    
    try {
        $response = Invoke-RestMethod -Uri $url -Method GET -TimeoutSec 30
        Write-Host "✅ Success: $response" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Write-Host ""
}

Write-Host "🎉 Testing complete!" -ForegroundColor Cyan
