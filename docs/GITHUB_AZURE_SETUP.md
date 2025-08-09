# GitHub Actions के साथ Azure Deployment Setup

## 🎯 Overview
यह guide आपको GitHub Actions के साथ automatic Azure deployment setup करने में मदद करेगा।

## 📋 Prerequisites
- ✅ Azure App Service (imagetool) - Already created
- ✅ GitHub Repository (techuhat/image2) - Ready
- 🔄 Azure Publish Profile - Need to get

## 🔑 Step 1: Azure Publish Profile निकालें

### Method 1: Azure Portal से
1. **Azure Portal खोलें**: https://portal.azure.com
2. **App Service ढूंढें**: Search "imagetool"
3. **Overview page** पर जाएं
4. **Get publish profile** button click करें
5. `.PublishSettings` file download होगी

### Method 2: Azure CLI से (Alternative)
```bash
az webapp deployment list-publishing-profiles --name imagetool --resource-group imagetool_group --xml
```

## 🔒 Step 2: GitHub Secrets में Add करें

1. **GitHub Repository खोलें**: https://github.com/techuhat/image2
2. **Settings** → **Secrets and variables** → **Actions**
3. **New repository secret** click करें
4. **Name**: `AZURE_WEBAPP_PUBLISH_PROFILE`
5. **Value**: Publish profile file का पूरा content paste करें
6. **Add secret** click करें

## 🚀 Step 3: GitHub Actions Trigger करें

### Auto Trigger:
- Backend code change करके push करें
- Workflow automatically run होगा

### Manual Trigger:
1. **Actions** tab पर जाएं
2. **Deploy to Azure App Service** workflow select करें
3. **Run workflow** click करें

## 📊 Step 4: Deployment Status Check करें

### GitHub Actions में:
- ✅ Build successful
- ✅ Dependencies installed
- ✅ Tests passed
- ✅ Deployed to Azure
- ✅ Endpoints tested

### Azure में:
- **URL**: https://imagetool.azurewebsites.net/health
- **Status**: Should return backend capabilities
- **Logs**: Azure Portal → App Service → Log stream

## 🔧 Workflow Features

### ✅ **Automatic Build**
- Python 3.10 setup
- Dependencies installation
- Library testing

### ✅ **Smart Deployment**
- Only backend files deployed
- Web.config for Azure created
- Environment optimized

### ✅ **Testing**
- Import testing
- Endpoint health checks
- Deployment verification

### ✅ **Triggers**
- Push to main branch
- Backend code changes
- Manual workflow dispatch

## 🎯 Expected Results

After successful deployment:

```bash
# These should work:
https://imagetool.azurewebsites.net/ping          # Returns "pong"
https://imagetool.azurewebsites.net/health        # Returns capabilities
https://imagetool.azurewebsites.net/pdf-to-docx   # PDF conversion endpoint
https://imagetool.azurewebsites.net/compress-pdf  # PDF compression endpoint
```

## 🐛 Troubleshooting

### Common Issues:
1. **Publish Profile Invalid**: Re-download from Azure Portal
2. **Secret Not Set**: Check GitHub repository secrets
3. **Build Fails**: Check Python dependencies
4. **Deployment Fails**: Check Azure logs

### Debug Commands:
```bash
# Check workflow status
# Go to GitHub → Actions → Latest workflow run

# Check Azure logs
# Azure Portal → imagetool → Log stream

# Test endpoints manually
curl https://imagetool.azurewebsites.net/health
```

## 🎉 Next Steps

1. **Get Publish Profile** from Azure Portal
2. **Add to GitHub Secrets** as `AZURE_WEBAPP_PUBLISH_PROFILE`
3. **Push this commit** to trigger first deployment
4. **Check Actions tab** for deployment status
5. **Test backend endpoints** once deployed

Your GitHub → Azure integration will be complete! 🚀
