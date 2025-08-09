# 🔐 Azure Publish Profile Setup Guide

## Issue Fixed
GitHub Actions workflow was failing with authentication error:
```
Login failed with Error: Using auth-type: SERVICE_PRINCIPAL. Not all values are present.
```

## ✅ Solution Applied
Switched from federated identity to **publish profile authentication** (more reliable).

## 📋 Action Required: Setup Publish Profile

### Step 1: Get Publish Profile from Azure Portal

1. **Open Azure Portal**: https://portal.azure.com
2. **Search**: "imagetool" 
3. **Click**: Your App Service (imagetool)
4. **Overview Tab**: Click **"Get publish profile"** button
5. **Download**: `imagetool.PublishSettings` file will download

### Step 2: Add to GitHub Secrets

1. **Open**: Downloaded `.PublishSettings` file in notepad
2. **Copy**: The entire XML content
3. **Go to**: https://github.com/techuhat/image2/settings/secrets/actions
4. **Click**: "New repository secret"
5. **Name**: `AZUREAPPSERVICE_PUBLISHPROFILE_IMAGETOOL`
6. **Value**: Paste the entire XML content from publish profile
7. **Click**: "Add secret"

### Step 3: Trigger Deployment

After adding the secret:
- The workflow will automatically trigger on next push
- Or manually trigger: GitHub → Actions → "Run workflow"

## 🎯 Expected Result

After adding the publish profile secret:

```bash
✅ Build Job: Dependencies install successfully
✅ Deploy Job: Authenticates with publish profile  
✅ Deployment: Completes successfully
✅ Backend: Live at https://imagetool.azurewebsites.net
```

## 🔍 Verify Deployment

Test these endpoints after successful deployment:

```bash
# Health check
https://imagetool.azurewebsites.net/health

# Simple ping  
https://imagetool.azurewebsites.net/ping

# PDF tools endpoints
https://imagetool.azurewebsites.net/pdf-to-docx
https://imagetool.azurewebsites.net/compress-pdf
```

## 🚨 Important Notes

- **Publish Profile**: Contains sensitive authentication info
- **Keep Secure**: Never commit publish profile to code
- **GitHub Secrets**: Encrypted and secure storage
- **Regular Rotation**: Regenerate publish profile periodically

## 🎉 Once Complete

Your GitHub → Azure deployment will be fully automated:
- Push backend changes → Automatic deployment
- Manual triggers available
- Full CI/CD pipeline operational

**Next: Get publish profile from Azure Portal and add to GitHub secrets!**
