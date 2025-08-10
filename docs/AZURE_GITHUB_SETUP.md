# Azure GitHub Actions OIDC Setup

## 🚀 GitHub Actions Azure Deployment Setup

This guide will help you set up OIDC (OpenID Connect) authentication between GitHub Actions and Azure for secure deployment without storing client secrets.

## ✅ Fixed Issues

The following GitHub Actions errors have been resolved:

1. ❌ `Unable to get ACTIONS_ID_TOKEN_REQUEST_URL env variable`
2. ❌ `Unexpected input(s) 'client-secret'`
3. ✅ Updated to use azure/login@v2 with OIDC authentication

## 📋 Prerequisites

1. Azure subscription with an App Service created
2. GitHub repository with workflow files
3. Azure CLI or Azure Portal access

## 🔧 Setup Steps

### Step 1: Create Azure Service Principal

```bash
# Create service principal for GitHub Actions
az ad sp create-for-rbac --name "github-actions-imagetool" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group-name} \
  --json-auth
```

This will output something like:
```json
{
  "clientId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "clientSecret": "your-secret-here",
  "subscriptionId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "tenantId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

### Step 2: Configure OIDC Federation

#### Option A: Using Azure CLI
```bash
# Create federated credential for main branch
az ad app federated-credential create \
  --id {clientId} \
  --parameters '{
    "name": "github-actions-main",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:techuhat/image2:ref:refs/heads/main",
    "description": "GitHub Actions for main branch",
    "audiences": ["api://AzureADTokenExchange"]
  }'

# Create federated credential for workflow_dispatch
az ad app federated-credential create \
  --id {clientId} \
  --parameters '{
    "name": "github-actions-workflow",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:techuhat/image2:environment:Production",
    "description": "GitHub Actions for workflow dispatch",
    "audiences": ["api://AzureADTokenExchange"]
  }'
```

#### Option B: Using Azure Portal
1. Go to Azure Active Directory → App registrations
2. Find your service principal
3. Go to "Certificates & secrets" → "Federated credentials"
4. Click "Add credential"
5. Configure:
   - **Federated credential scenario**: GitHub Actions deploying Azure resources
   - **Organization**: techuhat
   - **Repository**: image2
   - **Entity type**: Branch
   - **GitHub branch name**: main
   - **Name**: github-actions-main

### Step 3: Set GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these **Repository secrets**:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `AZURE_CLIENT_ID` | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` | Service Principal Client ID |
| `AZURE_TENANT_ID` | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` | Azure Tenant ID |
| `AZURE_SUBSCRIPTION_ID` | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` | Azure Subscription ID |

**Note**: You do NOT need `AZURE_CLIENT_SECRET` when using OIDC authentication!

### Step 4: Verify Workflow Configuration

Your workflow file should have these permissions set:

```yaml
permissions:
  id-token: write   # Required for OIDC authentication
  contents: read    # Required for actions/checkout
```

And use the Azure login action like this:

```yaml
- name: Azure Login
  uses: azure/login@v2
  with:
    client-id: ${{ secrets.AZURE_CLIENT_ID }}
    tenant-id: ${{ secrets.AZURE_TENANT_ID }}
    subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
    auth-type: IDENTITY
```

## 🧪 Testing the Setup

1. Push changes to the main branch or trigger workflow manually
2. Check GitHub Actions logs for successful authentication
3. Verify deployment to Azure App Service

## 🔍 Troubleshooting

### Common Issues:

1. **`OIDC token validation failed`**
   - Check federated credential configuration
   - Ensure subject matches your repository path exactly

2. **`Authentication failed`**
   - Verify all three secrets are set correctly
   - Check service principal has correct permissions

3. **`Deployment failed`**
   - Check Azure App Service configuration
   - Verify startup.py file is created correctly

### Debug Commands:

```bash
# Check service principal
az ad sp show --id {clientId}

# Check federated credentials
az ad app federated-credential list --id {clientId}

# Test authentication locally
az login --service-principal -u {clientId} -t {tenantId} --federated-token {token}
```

## 📚 Additional Resources

- [Azure OIDC Documentation](https://docs.microsoft.com/en-us/azure/developer/github/connect-from-azure)
- [GitHub Actions Azure Login](https://github.com/Azure/login)
- [Azure Web Apps Deploy Action](https://github.com/Azure/webapps-deploy)

## ✅ Success Indicators

When everything is working correctly, you should see:

1. ✅ Azure login step completes without errors
2. ✅ Deployment completes successfully
3. ✅ Health check endpoints respond correctly
4. ✅ App is accessible at: https://imagetool-h4dmewahfmg4bkej.eastasia-01.azurewebsites.net

---

**Last Updated**: August 10, 2025  
**Status**: Ready for deployment 🚀
