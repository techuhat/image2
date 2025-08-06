@echo off
echo.
echo ========================================
echo   STEP 1: DEPLOY BACKEND TO DETA SPACE
echo ========================================
echo.

echo Installing Deta CLI...
echo Run this command in PowerShell (as Administrator):
echo.
echo iwr https://get.deta.dev/cli.ps1 -useb ^| iex
echo.
pause

echo.
echo Login to Deta Space...
echo.
deta login
echo.
pause

echo.
echo Navigating to backend folder...
cd /d "%~dp0deta-backend"
echo Current directory: %cd%
echo.

echo Creating new Deta Space project...
echo.
deta space new
echo.
pause

echo.
echo Deploying to Deta Space...
echo.
deta space push
echo.
pause

echo.
echo Getting your app information...
echo.
deta space info
echo.
echo ========================================
echo   IMPORTANT: COPY YOUR APP URL!
echo ========================================
echo.
echo You should see something like:
echo https://your-app-name-1-x1234567.deta.app
echo.
echo COPY THIS URL - You'll need it next!
echo.
pause

echo.
echo ========================================
echo   NEXT STEPS:
echo ========================================
echo.
echo 1. Copy your Deta Space app URL from above
echo 2. Run: update_frontend.bat
echo 3. Update the URL in that script
echo 4. Push to GitHub
echo 5. Enable GitHub Pages
echo.
echo Your backend is now live! 🚀
echo.
pause
