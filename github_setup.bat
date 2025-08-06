@echo off
echo ========================================
echo   GITHUB REPOSITORY SETUP GUIDE
echo ========================================
echo.
echo ✅ Git initialized and committed locally!
echo.

echo Next Steps:
echo -----------

echo Step 1: Create GitHub Repository
echo --------------------------------
echo 1. Go to: https://github.com
echo 2. Login to your account
echo 3. Click "New repository" (+ icon, top right)
echo 4. Repository name: image2
echo 5. Description: Professional PDF and Image Processing Tools
echo 6. Set to: Public (for GitHub Pages)
echo 7. DO NOT check "Add a README file"
echo 8. DO NOT check "Add .gitignore"
echo 9. DO NOT check "Choose a license"
echo 10. Click "Create repository"
echo.

echo Step 2: Connect Local to GitHub
echo -------------------------------
echo GitHub will show you commands like:
echo.
echo git remote add origin https://github.com/YOURUSERNAME/image2.git
echo git branch -M main
echo git push -u origin main
echo.
echo Copy and run those commands here!
echo.

echo Step 3: After Pushing to GitHub
echo -------------------------------
echo 1. Go to your repository on GitHub
echo 2. Settings ^> Pages
echo 3. Source: Deploy from a branch
echo 4. Branch: main
echo 5. Folder: / (root)
echo 6. Save
echo.
echo Your site will be: https://YOURUSERNAME.github.io/image2
echo.

echo Step 4: Deploy Backend to Railway
echo ---------------------------------
echo 1. Visit: https://railway.app
echo 2. Login with GitHub
echo 3. New Project ^> Deploy from GitHub repo
echo 4. Select: image2 repository
echo 5. Configure: Root Directory = deta-backend
echo 6. Deploy!
echo.

echo Step 5: Update Backend URL
echo --------------------------
echo 1. Get Railway URL: https://xyz.up.railway.app
echo 2. Edit: tools/pdf-to-doc.html (line 808)
echo 3. Update: baseUrl: 'https://your-railway-url'
echo 4. Git add, commit, push
echo.

echo 🎯 Total time needed: 10-15 minutes
echo 🎯 Total cost: $0 (free tiers)
echo.

pause
