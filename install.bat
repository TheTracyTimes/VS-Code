@echo off
REM Installation Script for Music Recognition Web App (Windows)

echo ================================================
echo   Music Recognition Web App - Setup
echo ================================================
echo.
echo You have TWO installation options:
echo.
echo 1. QUICK DEMO (Web app only - 100MB)
echo    - Runs web interface immediately
echo    - Creates sample PDFs to show workflow
echo    - No real music recognition (demo mode)
echo.
echo 2. FULL INSTALL (Complete system - 2.5GB)
echo    - Real music recognition with AI
echo    - Processes actual handwritten music
echo    - Includes PyTorch (~2GB)
echo.
echo ================================================
echo.

set /p choice="Which installation? (1=Quick Demo, 2=Full Install): "

if "%choice%"=="1" (
    echo.
    echo [INSTALLING] QUICK DEMO (Web App Only)...
    echo.
    python -m pip install fastapi uvicorn[standard] python-multipart websockets aiofiles reportlab
    echo.
    echo [SUCCESS] Quick demo installed!
    echo.
    echo To start the web app:
    echo   cd web_app
    echo   start.bat
    echo.
    echo Note: This will run in DEMO MODE (sample files only)
    echo       To enable real processing, run this installer again
    echo       and choose option 2.
    echo.
) else if "%choice%"=="2" (
    echo.
    echo [INSTALLING] FULL SYSTEM (with PyTorch)...
    echo.
    echo WARNING: This will download ~2.5GB of data
    echo WARNING: May take 5-15 minutes depending on your internet
    echo.
    set /p confirm="Continue? (y/n): "

    if /i "%confirm%"=="y" (
        echo.
        echo Installing all dependencies from requirements.txt...
        python -m pip install -r requirements.txt
        echo.
        echo [SUCCESS] Full system installed!
        echo.
        echo To start the web app with REAL processing:
        echo   cd web_app
        echo   start.bat
        echo.
        echo The system will now digitize actual handwritten music!
        echo.
    ) else (
        echo.
        echo Installation cancelled.
        echo.
    )
) else (
    echo.
    echo Invalid choice. Please run the installer again.
    echo.
)

echo ================================================
pause
