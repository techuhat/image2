# Azure App Service Deployment Script
# Upload your files to Azure App Service

param(
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroupName = "imagetool_group",
    
    [Parameter(Mandatory=$true)]
    [string]$AppName = "imagetool",
    
    [Parameter(Mandatory=$false)]
    [string]$SubscriptionName = "Azure for Students"
)

Write-Host "🚀 Starting Azure App Service Deployment..." -ForegroundColor Green

# Login to Azure (if not already logged in)
Write-Host "Checking Azure login status..." -ForegroundColor Yellow
try {
    az account show --output none
    Write-Host "✅ Already logged in to Azure" -ForegroundColor Green
} catch {
    Write-Host "Please login to Azure..." -ForegroundColor Yellow
    az login
}

# Set subscription
if ($SubscriptionName) {
    Write-Host "Setting subscription to: $SubscriptionName" -ForegroundColor Yellow
    az account set --subscription "$SubscriptionName"
}

# Get app service details
Write-Host "Getting app service details..." -ForegroundColor Yellow
$appDetails = az webapp show --resource-group $ResourceGroupName --name $AppName --output json | ConvertFrom-Json

if ($appDetails) {
    Write-Host "✅ Found app service: $($appDetails.defaultHostName)" -ForegroundColor Green
    $appUrl = "https://$($appDetails.defaultHostName)"
    Write-Host "App URL: $appUrl" -ForegroundColor Cyan
} else {
    Write-Host "❌ App service not found!" -ForegroundColor Red
    exit 1
}

# Create deployment package
Write-Host "Creating deployment package..." -ForegroundColor Yellow
$deployFiles = @(
    "app.py",
    "requirements.txt", 
    "run.py",
    ".env.example",
    "index.html",
    "script.js",
    "styles.min.css",
    "tailwind-complete.css",
    "manifest.json",
    "service-worker.js",
    "favicon.ico",
    "about.html",
    "contact.html",
    "privacy.html",
    "terms.html",
    "robots.txt",
    "sitemap.xml",
    "CNAME",
    "tools/",
    "assets/",
    "css/",
    "images/",
    "js/"
)

# Deploy using ZIP deployment
Write-Host "Deploying to Azure App Service..." -ForegroundColor Yellow

# Create a zip file for deployment
Compress-Archive -Path $deployFiles -DestinationPath "azure-deployment.zip" -Force

# Deploy the zip file
az webapp deployment source config-zip --resource-group $ResourceGroupName --name $AppName --src "azure-deployment.zip"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Deployment successful!" -ForegroundColor Green
    Write-Host "🌐 Your app is available at: $appUrl" -ForegroundColor Cyan
    Write-Host "🔧 Backend API: $appUrl/health" -ForegroundColor Cyan
    
    # Test the deployment
    Write-Host "Testing deployment..." -ForegroundColor Yellow
    try {
        $response = Invoke-RestMethod -Uri "$appUrl/ping" -Method GET -TimeoutSec 30
        Write-Host "✅ Backend is responding: $response" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Backend might still be starting up. Check in a few minutes." -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
}

# Cleanup
Remove-Item "azure-deployment.zip" -ErrorAction SilentlyContinue

Write-Host "🎉 Azure deployment complete!" -ForegroundColor Green
