# 🔐 Azure Federated Credentials Setup Guide

## 📋 Overview
This guide will help you configure Azure federated credentials for GitHub OIDC authentication to fix the authentication error:
```
No matching federated identity record found for presented assertion subject
```

## 🎯 Current Configuration
After the workflow fix, your GitHub workflow will present these claims:

- **Issuer**: `https://token.actions.githubusercontent.com`
- **Subject**: `repo:techuhat/image2:ref:refs/heads/main`
- **Audience**: `api://AzureADTokenExchange`

## 🛠️ Step-by-Step Setup

### 1. 🔍 Find Your Azure App Registration
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Find or create your app registration for the deployment

### 2. 📝 Add Federated Credential
1. In your App Registration, go to **Certificates & secrets**
2. Click on **Federated credentials** tab
3. Click **+ Add credential**
4. Select **GitHub Actions deploying Azure resources**

### 3. ⚙️ Configure the Credential
Fill in these **exact** values:

| Field | Value |
|-------|--------|
| **Issuer** | `https://token.actions.githubusercontent.com` |
| **Subject identifier** | `repo:techuhat/image2:ref:refs/heads/main` |
| **Name** | `GitHubActions-imagetool-main` |
| **Description** | `GitHub Actions OIDC for imagetool deployment from main branch` |

### 4. 🔑 Required GitHub Secrets
Ensure these secrets are set in your GitHub repository:

1. Go to your GitHub repo: `https://github.com/techuhat/image2`
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Add these secrets:

| Secret Name | Value Source |
|-------------|--------------|
| `AZURE_CLIENT_ID` | App Registration → Application (client) ID |
| `AZURE_TENANT_ID` | Azure Active Directory → Tenant ID |
| `AZURE_SUBSCRIPTION_ID` | Your Azure Subscription ID |

### 5. 🎯 Find Required IDs

#### Get Client ID:
1. In your App Registration → **Overview**
2. Copy **Application (client) ID**

#### Get Tenant ID:
1. Azure Active Directory → **Overview**
2. Copy **Tenant ID**

#### Get Subscription ID:
1. Navigate to **Subscriptions** in Azure Portal
2. Copy your **Subscription ID**

## 🔧 Alternative: Broader Subject Pattern
If you want to allow deployments from any branch, use this subject pattern instead:
```
repo:techuhat/image2:ref:refs/heads/*
```

## 📚 Additional Resources
- [Azure OIDC Setup Guide](https://docs.microsoft.com/en-us/azure/active-directory/develop/workload-identity-federation-create-trust-github)
- [GitHub Azure Login Action](https://github.com/Azure/login#configure-federated-credentials-for-your-environment)

## ✅ Testing
After setup, trigger your GitHub workflow. The authentication should now work without the "No matching federated identity record" error.

## 🚨 Troubleshooting
If you still get authentication errors:

1. **Double-check subject pattern**: Must match exactly `repo:techuhat/image2:ref:refs/heads/main`
2. **Verify issuer**: Must be `https://token.actions.githubusercontent.com`
3. **Check audience**: Must be `api://AzureADTokenExchange`
4. **Confirm secrets**: All three Azure secrets must be correctly set in GitHub
5. **Wait time**: After creating federated credential, wait 5-10 minutes for propagation

---
*Updated: August 10, 2025*
