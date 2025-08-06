@echo off
echo ========================================
echo   DEPLOYING TO GITHUB "image2" REPOSITORY
echo ========================================
echo.

echo Step 1: Create GitHub Repository
echo --------------------------------
echo 1. Open browser and go to: https://github.com/new
echo 2. Repository name: image2
echo 3. Description: Professional PDF and Image Processing Tools
echo 4. Set to: Public
echo 5. DO NOT add README, .gitignore, or license
echo 6. Click "Create repository"
echo.

echo Step 2: GitHub will show you these commands:
echo -------------------------------------------
echo git remote add origin https://github.com/YOURUSERNAME/image2.git
echo git branch -M main  
echo git push -u origin main
echo.

echo Step 3: Copy YOUR actual commands from GitHub and run them below:
echo ----------------------------------------------------------------

pause

echo.
echo Ready to run GitHub commands? 
echo Replace YOURUSERNAME with your actual GitHub username:
echo.

set /p username="Enter your GitHub username: "

echo.
echo Running deployment commands...
echo.

git remote add origin https://github.com/%username%/image2.git
git branch -M main
git push -u origin main

echo.
echo ========================================
echo   DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Your website will be available at:
echo https://%username%.github.io/image2
echo.
echo Next: Enable GitHub Pages in repository settings
echo.

pause
