#!/bin/bash

# Full Installation - Real Music Recognition System
# Downloads PyTorch and all dependencies for actual music processing

echo "============================================================"
echo "  Music Recognition - FULL INSTALLATION"
echo "============================================================"
echo ""
echo "This will install the COMPLETE system with:"
echo "  ✓ PyTorch (AI/Machine Learning)"
echo "  ✓ OpenCV (Image Processing)"
echo "  ✓ music21 (Music Notation)"
echo "  ✓ All recognition capabilities"
echo ""
echo "Download Size: ~2.5 GB"
echo "Install Time: 5-30 minutes (depending on internet speed)"
echo ""
echo "============================================================"
echo ""

read -p "Continue with full installation? (y/n): " confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo ""
    echo "Installation cancelled."
    echo ""
    exit 0
fi

echo ""
echo "============================================================"
echo "  Checking System Dependencies..."
echo "============================================================"
echo ""

# Check for poppler (needed for pdf2image)
if command -v pdftoppm &> /dev/null; then
    echo "✅ Poppler (PDF processing) is installed"
else
    echo "⚠️  Poppler not found - needed for PDF processing"
    echo ""
    echo "To install poppler:"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  Mac: brew install poppler"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "  Ubuntu/Debian: sudo apt-get install poppler-utils"
        echo "  Fedora: sudo dnf install poppler-utils"
    fi
    echo ""
    echo "You can continue without it, but PDF upload won't work."
    echo ""
    read -p "Continue anyway? (y/n): " continue_without_poppler
    if [ "$continue_without_poppler" != "y" ] && [ "$continue_without_poppler" != "Y" ]; then
        echo ""
        echo "Installation cancelled. Install poppler first, then run this script again."
        exit 0
    fi
fi

echo ""
echo "============================================================"
echo "  Installing Full System..."
echo "============================================================"
echo ""

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install all requirements
echo ""
echo "📦 Installing all dependencies from requirements.txt..."
echo "   (This will take several minutes...)"
echo ""

pip install -r requirements.txt

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "  ✅ INSTALLATION SUCCESSFUL!"
    echo "============================================================"
    echo ""
    echo "Installed components:"
    echo "  ✓ PyTorch $(python -c 'import torch; print(torch.__version__)' 2>/dev/null || echo 'installed')"
    echo "  ✓ OpenCV"
    echo "  ✓ FastAPI Web Framework"
    echo "  ✓ Music21 Notation Library"
    echo "  ✓ All music recognition modules"
    echo ""
    echo "============================================================"
    echo "  🚀 READY TO USE!"
    echo "============================================================"
    echo ""
    echo "To start the web application:"
    echo ""
    echo "  cd web_app"
    echo "  python server.py"
    echo ""
    echo "Then open your browser to: http://localhost:8000"
    echo ""
    echo "The system will run in FULL MODE with real music recognition!"
    echo ""
else
    echo ""
    echo "============================================================"
    echo "  ⚠️  INSTALLATION FAILED"
    echo "============================================================"
    echo ""
    echo "Please check the error messages above."
    echo ""
    echo "Common issues:"
    echo "  - Slow internet connection (try again)"
    echo "  - Insufficient disk space (need 5GB free)"
    echo "  - Python version too old (need Python 3.8+)"
    echo ""
    exit 1
fi
