# 🚀 RAILWAY DEPLOYMENT GUIDE
# ================================

## Why Railway?
- ✅ GitHub integration
- ✅ Free tier with good limits
- ✅ Automatic deployments
- ✅ Simple setup
- ✅ Custom domains
- ✅ Environment variables

## Step-by-Step Railway Deployment:

### 1. Prepare Your Repository
```bash
# Make sure your code is pushed to GitHub
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### 2. Deploy to Railway
1. Visit: https://railway.app
2. Click "Login" → "Login with GitHub"
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your toolkit repository
6. Select "deta-backend" folder as root directory

### 3. Configure Environment
- Root Directory: `deta-backend`
- Start Command: `uvicorn main:app --host=0.0.0.0 --port=$PORT`
- Python Version: 3.11

### 4. Deploy
- Click "Deploy"
- Wait for build to complete
- Get your app URL (e.g., https://your-app.railway.app)

### 5. Update Frontend
In `tools/pdf-to-doc.html`, update:
```javascript
baseUrl: 'https://your-app.railway.app',
```

## Railway Configuration File
Create `railway.toml` in deta-backend folder:

```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "uvicorn main:app --host=0.0.0.0 --port=$PORT"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

## Cost: FREE TIER
- 512 MB RAM
- 1 GB Disk
- $5 monthly credit (enough for small apps)
- No credit card required for free tier
