# Alternative: Manual Publish Profile Creation

Since basic authentication is disabled, here's how to create a manual publish profile:

## 📋 Manual Publish Profile Template

Create a file with this content and save as `imagetool.PublishSettings`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<publishData>
  <publishProfile 
    profileName="imagetool - Web Deploy" 
    publishMethod="MSDeploy" 
    publishUrl="imagetool.scm.azurewebsites.net" 
    msdeploysite="imagetool" 
    userName="$imagetool" 
    userPWD="[PASSWORD_FROM_AZURE]" 
    destinationAppUrl="https://imagetool.azurewebsites.net" 
    SQLServerDBConnectionString="" 
    mySQLDBConnectionString="" 
    hostingProviderForumLink="" 
    controlPanelLink="http://windows.azure.com" 
    webSystem="WebSites">
    <databases />
  </publishProfile>
  <publishProfile 
    profileName="imagetool - FTP" 
    publishMethod="FTP" 
    publishUrl="ftp://waws-prod-dm1-xxx.ftp.azurewebsites.windows.net/site/wwwroot" 
    ftpPassiveMode="True" 
    userName="imagetool\\$imagetool" 
    userPWD="[PASSWORD_FROM_AZURE]" 
    destinationAppUrl="https://imagetool.azurewebsites.net" 
    SQLServerDBConnectionString="" 
    mySQLDBConnectionString="" 
    hostingProviderForumLink="" 
    controlPanelLink="http://windows.azure.com" 
    webSystem="WebSites">
    <databases />
  </publishProfile>
</publishData>
```

## 🔑 Get Password from Azure Portal

1. **Azure Portal** → **imagetool App Service**
2. **Deployment Center** → **FTPS credentials**
3. **Copy Username and Password**
4. **Replace [PASSWORD_FROM_AZURE]** in template above
5. **Save as publish profile**

## 📤 Alternative: Use Azure CLI

```bash
# Enable basic auth (if you have Azure CLI)
az webapp auth update --resource-group imagetool_group --name imagetool --enable-basic-auth true

# Then download publish profile
az webapp deployment list-publishing-profiles --resource-group imagetool_group --name imagetool --xml
```
