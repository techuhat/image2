# Simple Azure Deployment Script
# This script creates a deployment package without requiring Azure CLI

param(
    [string]$AppName = "imagetool"
)

Write-Host "🚀 Creating deployment package for $AppName..." -ForegroundColor Green

# Create deployment directory
$deployDir = ".\deployment-package"
if (Test-Path $deployDir) {
    Remove-Item $deployDir -Recurse -Force
}
New-Item -ItemType Directory -Path $deployDir | Out-Null

# Copy backend files
Write-Host "📁 Copying backend files..." -ForegroundColor Yellow
Copy-Item ".\src\backend\*" -Destination $deployDir -Recurse -Force

# Copy requirements.txt from root
Copy-Item ".\requirements.txt" -Destination $deployDir -Force

# Create web.config for Azure App Service
$webConfig = @"
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <add name="PythonHandler" path="*" verb="*" modules="httpPlatformHandler" resourceType="Unspecified"/>
    </handlers>
    <httpPlatform processPath="python" arguments="startup.py" stdoutLogEnabled="true" stdoutLogFile=".\logs\python.log" startupTimeLimit="60" requestTimeout="604800">
      <environmentVariables>
        <environmentVariable name="PYTHONPATH" value="." />
        <environmentVariable name="PORT" value="8000" />
      </environmentVariables>
    </httpPlatform>
  </system.webServer>
</configuration>
"@

$webConfig | Out-File -FilePath "$deployDir\web.config" -Encoding UTF8

# Create ZIP package
Write-Host "📦 Creating ZIP package..." -ForegroundColor Yellow
$zipPath = ".\azure-deployment.zip"
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}

Compress-Archive -Path "$deployDir\*" -DestinationPath $zipPath -Force

Write-Host "✅ Deployment package created: $zipPath" -ForegroundColor Green
Write-Host "" -ForegroundColor White
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Go to Azure Portal: https://portal.azure.com" -ForegroundColor White
Write-Host "2. Navigate to your App Service: $AppName" -ForegroundColor White
Write-Host "3. Go to Deployment Center > Kudu > Advanced Tools" -ForegroundColor White
Write-Host "4. Click 'Go' to open Kudu console" -ForegroundColor White
Write-Host "5. Drag and drop the $zipPath file to /site/wwwroot/" -ForegroundColor White
Write-Host "6. Wait for deployment to complete" -ForegroundColor White
Write-Host "" -ForegroundColor White
Write-Host "🌐 Your app will be available at: https://$AppName.azurewebsites.net" -ForegroundColor Green

# Test the package contents
Write-Host "" -ForegroundColor White
Write-Host "📋 Package contents:" -ForegroundColor Yellow
Get-ChildItem $deployDir -Recurse | ForEach-Object { 
    $relativePath = $_.FullName.Replace((Resolve-Path $deployDir).Path + "\", "")
    Write-Host "  $relativePath" -ForegroundColor Gray
}

# Cleanup
Remove-Item $deployDir -Recurse -Force

Write-Host "" -ForegroundColor White
Write-Host "🎉 Deployment package ready!" -ForegroundColor Green
