@echo off
REM Super Lightweight Installation - NO PyTorch!

echo ================================================
echo   Music Recognition - Lightweight Install
echo ================================================
echo.
echo This installs the web app WITHOUT PyTorch
echo.
echo [INSTALLING] Lightweight dependencies...
echo    (Only ~50MB - takes 1 minute)
echo.

python -m pip install -q --upgrade pip
python -m pip install fastapi uvicorn[standard] python-multipart websockets aiofiles reportlab

echo.
echo [SUCCESS] Installation complete!
echo.
echo ================================================
echo   Ready to Start!
echo ================================================
echo.
echo Run the web app:
echo   cd web_app
echo   python server.py
echo.
echo Then open: http://localhost:8000
echo.
echo Note: The app runs in DEMO MODE (creates sample PDFs)
echo       This is perfect for:
echo       - Seeing how the interface works
echo       - Understanding the workflow
echo       - Testing with your team
echo.
echo No PyTorch needed!
echo.
pause
