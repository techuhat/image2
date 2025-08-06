@echo off
echo ========================================
echo   DETA CLI INSTALLATION GUIDE
echo ========================================
echo.

echo Method 1: Direct GitHub Download (Works with Network Issues)
echo --------------------------------------------------------
echo 1. Visit: https://github.com/deta/deta-cli/releases/latest
echo 2. Download: deta-windows-amd64.exe
echo 3. Rename to: deta.exe
echo 4. Place in C:\deta\ folder
echo 5. Add C:\deta to PATH environment variable
echo.
echo Step-by-step PATH setup:
echo a. Windows Key + R, type: sysdm.cpl
echo b. Advanced tab ^> Environment Variables
echo c. Under System Variables, find PATH
echo d. Click Edit ^> New ^> Add: C:\deta
echo e. Click OK ^> OK ^> OK
echo f. Restart terminal
echo.

echo Method 2: PowerShell (if network works)
echo -----------------------------------
echo 1. Open PowerShell as Administrator
echo 2. Run: Set-ExecutionPolicy RemoteSigned -Force
echo 3. Run: iwr https://github.com/deta/deta-cli/releases/latest/download/deta-windows-amd64.exe -OutFile deta.exe
echo 4. Move deta.exe to C:\deta\
echo 5. Add C:\deta to PATH
echo.

echo Method 3: Using chocolatey (if installed)
echo -----------------------------------------
echo choco install deta
echo.

echo After installation, verify with:
echo deta --help
echo.

echo Then proceed with:
echo deta login
echo.

pause
