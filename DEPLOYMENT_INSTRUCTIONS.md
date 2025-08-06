# 🚀 Complete Deployment Instructions

## 📋 Overview
- **Frontend**: GitHub Pages (Static files)
- **Backend**: Deta Space (Serverless)
- **Total Cost**: $0 (Free tiers)

---

## Step 1: Deploy Backend to Deta Space

### 1.1 Install Deta CLI (Windows PowerShell)
```powershell
iwr https://get.deta.dev/cli.ps1 -useb | iex
```

### 1.2 Login to Deta
```bash
deta login
```
- Follow browser login process
- Complete authentication

### 1.3 Deploy Backend
```bash
# Navigate to backend folder
cd d:\toolkit-main\deta-backend

# Create new Deta Space project
deta space new

# Deploy to Deta Space
deta space push

# Get your app URL
deta space info
```

### 1.4 Note Your App URL
You'll get something like:
```
https://imagepdf-toolkit-1-a2b3c4d5.deta.app
```
**COPY THIS URL - You'll need it in Step 2!**

---

## Step 2: Update Frontend Configuration

### 2.1 Update Backend URL
Edit `tools/pdf-to-doc.html` line 808:

**Change this:**
```javascript
baseUrl: 'https://your-app-name-1-x1234567.deta.app',
```

**To your actual URL:**
```javascript
baseUrl: 'https://imagepdf-toolkit-1-a2b3c4d5.deta.app',
```

### 2.2 Commit Changes
```bash
# In your main directory
git add .
git commit -m "Update backend URL for Deta Space deployment"
git push origin main
```

---

## Step 3: Deploy Frontend to GitHub Pages

### 3.1 Enable GitHub Pages
1. Go to your GitHub repository
2. Settings → Pages
3. Source: Deploy from branch
4. Branch: main
5. Folder: / (root)
6. Click Save

### 3.2 Access Your Site
Your site will be available at:
```
https://yourusername.github.io/toolkit
```

---

## Step 4: Test Everything

### 4.1 Test Backend Health
Visit: `https://your-deta-app.deta.app/health`

Should return:
```json
{
  "status": "healthy",
  "libraries": {
    "pdf2docx": true,
    "pymupdf": true,
    "python_docx": true
  }
}
```

### 4.2 Test Frontend Tool
1. Go to your GitHub Pages site
2. Navigate to PDF to DOC tool
3. Select "Deta Space Processing" mode
4. Upload a PDF file
5. Convert and download

---

## Step 5: Troubleshooting

### Backend Issues
```bash
# Check logs
deta space logs

# Redeploy if needed
deta space push

# Check status
deta space info
```

### Frontend Issues
- Check browser console for errors
- Verify backend URL is correct
- Test backend health endpoint directly
- Ensure GitHub Pages is enabled

### CORS Issues
If you get CORS errors, update `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourusername.github.io"],  # Your GitHub Pages URL
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

---

## 📊 Final Architecture

```
[GitHub Pages Frontend]  →  [Deta Space Backend]
├── Static HTML/CSS/JS      ├── FastAPI Server
├── Client-side tools       ├── PDF2DOCX Processing
├── Modern UI/UX           ├── Auto-scaling
└── Free hosting           └── Free tier (100MB files)
```

---

## 🎉 Success Checklist

- [ ] ✅ Deta CLI installed
- [ ] ✅ Deta Space account created
- [ ] ✅ Backend deployed to Deta Space
- [ ] ✅ Backend URL copied
- [ ] ✅ Frontend updated with backend URL
- [ ] ✅ Changes committed to GitHub
- [ ] ✅ GitHub Pages enabled
- [ ] ✅ Site accessible
- [ ] ✅ Backend health check passes
- [ ] ✅ PDF conversion test successful

---

## 🔄 Future Updates

### Update Backend:
```bash
cd deta-backend
deta space push
```

### Update Frontend:
```bash
git add .
git commit -m "Update frontend"
git push origin main
```

---

## 💰 Cost Breakdown

### Free Forever:
- **GitHub Pages**: Unlimited static hosting
- **Deta Space**: 
  - 100,000 requests/month
  - 10GB storage
  - 100GB bandwidth

### Estimated Usage:
- **Small team/personal**: 100% free
- **Medium usage**: Still free (generous limits)
- **High usage**: Very affordable scaling

---

**🎯 Result: Professional PDF processing tool with zero monthly costs!**
