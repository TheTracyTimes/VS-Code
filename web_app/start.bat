@echo off
REM Music Recognition Web App Launcher for Windows

echo ==========================================
echo   Music Recognition Web Application
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [SETUP] Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo [SETUP] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo [SETUP] Installing dependencies...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt

echo.
echo ==========================================
echo   Starting Server...
echo ==========================================
echo.
echo Open your browser to:
echo.
echo     http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python server.py

pause
