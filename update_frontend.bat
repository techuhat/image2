@echo off
echo.
echo ========================================
echo   STEP 2: UPDATE FRONTEND WITH BACKEND URL
echo ========================================
echo.

echo INSTRUCTIONS:
echo.
echo 1. Open: tools\pdf-to-doc.html
echo 2. Go to line 808 (around BACKEND_CONFIG)
echo 3. Find this line:
echo    baseUrl: 'https://your-app-name-1-x1234567.deta.app',
echo.
echo 4. Replace with YOUR actual Deta Space URL
echo    Example: baseUrl: 'https://imagepdf-toolkit-1-a2b3c4d5.deta.app',
echo.

echo Opening the file for you...
start notepad "tools\pdf-to-doc.html"
echo.

echo After updating the URL:
echo.
echo 5. Save the file
echo 6. Run: git add .
echo 7. Run: git commit -m "Connect to Deta Space backend"
echo 8. Run: git push origin main
echo.

echo ========================================
echo   STEP 3: ENABLE GITHUB PAGES
echo ========================================
echo.
echo 1. Go to your GitHub repository
echo 2. Settings → Pages
echo 3. Source: Deploy from branch
echo 4. Branch: main
echo 5. Folder: / (root)
echo 6. Click Save
echo.
echo Your site will be live at:
echo https://yourusername.github.io/toolkit
echo.

echo ========================================
echo   TESTING
echo ========================================
echo.
echo 1. Visit your GitHub Pages site
echo 2. Go to Tools → PDF to DOC
echo 3. Select "Deta Space Processing"
echo 4. Upload a PDF and test conversion
echo.

pause
