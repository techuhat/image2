# Alternative Azure Login method using creds (Service Principal Secret)
# Use this if OIDC setup is not complete

# In the Azure Login step, use this instead:
- name: Azure Login (Service Principal)
  uses: azure/login@v2
  with:
    creds: ${{ secrets.AZURE_CREDENTIALS }}

# Where AZURE_CREDENTIALS is a JSON secret containing:
# {
#   "clientId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
#   "clientSecret": "your-secret-here",
#   "subscriptionId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", 
#   "tenantId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
# }

# This method doesn't require OIDC setup but stores client secret
# OIDC method is more secure but requires additional Azure configuration
