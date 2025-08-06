# 🚀 Railway Deployment Guide

## Quick Setup (5 Minutes)

### Step 1: Prepare Repository
✅ Backend files cleaned and optimized
✅ Railway configuration added
✅ Ready for deployment

### Step 2: Deploy to Railway

1. **Visit Railway**: https://railway.app
2. **Login** with GitHub account
3. **New Project** → **Deploy from GitHub repo**
4. **Select** your toolkit repository
5. **Configure**:
   - **Root Directory**: `deta-backend`
   - **Start Command**: Auto-detected from Procfile
   - **Environment**: Python 3.11

### Step 3: Get Your URL
After deployment, Railway will give you a URL like:
```
https://your-app-name-production-xyz.up.railway.app
```

### Step 4: Update Frontend
In `tools/pdf-to-doc.html`, line 808, update:
```javascript
baseUrl: 'https://your-railway-app.up.railway.app',
```

### Step 5: Push to GitHub
```bash
git add .
git commit -m "Railway deployment ready"
git push origin main
```

### Step 6: Enable GitHub Pages
1. Repository → Settings → Pages
2. Source: Deploy from branch
3. Branch: main
4. Save

## 🎯 Final Architecture
```
GitHub Pages (Frontend) → Railway (Backend)
     ↓                        ↓
Static HTML/CSS/JS        FastAPI + PDF2DOCX
Free hosting              Free 5$/month credit
```

## 🔧 Benefits of Railway
- ✅ **5$/month free credit** (plenty for PDF processing)
- ✅ **Auto-deploy** from GitHub
- ✅ **Zero configuration** needed
- ✅ **Fast deployment** (< 2 minutes)
- ✅ **Automatic HTTPS**
- ✅ **Great performance**

## 🚀 Ready to Deploy!
Your backend is now optimized for Railway. Follow the steps above!
