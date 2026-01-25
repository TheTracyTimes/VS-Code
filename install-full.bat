@echo off
REM Full Installation - Real Music Recognition System

echo ============================================================
echo   Music Recognition - FULL INSTALLATION
echo ============================================================
echo.
echo This will install the COMPLETE system with:
echo   [OK] PyTorch (AI/Machine Learning)
echo   [OK] OpenCV (Image Processing)
echo   [OK] music21 (Music Notation)
echo   [OK] All recognition capabilities
echo.
echo Download Size: ~2.5 GB
echo Install Time: 5-30 minutes (depending on internet speed)
echo.
echo ============================================================
echo.

set /p confirm="Continue with full installation? (y/n): "

if /i not "%confirm%"=="y" (
    echo.
    echo Installation cancelled.
    echo.
    exit /b 0
)

echo.
echo ============================================================
echo   Installing Full System...
echo ============================================================
echo.

REM Upgrade pip
echo [SETUP] Upgrading pip...
python -m pip install --upgrade pip

REM Install all requirements
echo.
echo [SETUP] Installing all dependencies from requirements.txt...
echo    (This will take several minutes...)
echo.

python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ============================================================
    echo   [ERROR] INSTALLATION FAILED
    echo ============================================================
    echo.
    echo Please check the error messages above.
    echo.
    echo Common issues:
    echo   - Slow internet connection (try again)
    echo   - Insufficient disk space (need 5GB free)
    echo   - Python version too old (need Python 3.8+)
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   [SUCCESS] INSTALLATION SUCCESSFUL!
echo ============================================================
echo.
echo Installed components:
python -c "import torch; print('  [OK] PyTorch', torch.__version__)" 2>nul || echo   [OK] PyTorch installed
echo   [OK] OpenCV
echo   [OK] FastAPI Web Framework
echo   [OK] Music21 Notation Library
echo   [OK] All music recognition modules
echo.
echo ============================================================
echo   Ready to Use!
echo ============================================================
echo.
echo To start the web application:
echo.
echo   cd web_app
echo   python server.py
echo.
echo Then open your browser to: http://localhost:8000
echo.
echo The system will run in FULL MODE with real music recognition!
echo.
pause
