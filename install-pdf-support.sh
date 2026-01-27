#!/bin/bash

echo "=============================================="
echo "  Installing PDF Support"
echo "=============================================="
echo ""

# Check for poppler
echo "Step 1: Checking for Poppler (system dependency)..."
if command -v pdftoppm &> /dev/null; then
    echo "✅ Poppler is already installed"
else
    echo "❌ Poppler not found"
    echo ""
    echo "Poppler is required for PDF processing."
    echo ""
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "To install on Mac:"
        echo "  brew install poppler"
        echo ""
        echo "Don't have Homebrew? Install it first:"
        echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "To install on Linux:"
        echo "  Ubuntu/Debian: sudo apt-get install poppler-utils"
        echo "  Fedora: sudo dnf install poppler-utils"
    fi
    echo ""
    read -p "Have you installed poppler? Press Enter to continue or Ctrl+C to cancel..."
fi

echo ""
echo "Step 2: Installing Python packages..."
pip3.11 install pdf2image PyPDF2

if [ $? -eq 0 ]; then
    echo ""
    echo "=============================================="
    echo "  ✅ PDF SUPPORT INSTALLED!"
    echo "=============================================="
    echo ""
    echo "Installed:"
    echo "  ✓ pdf2image"
    echo "  ✓ PyPDF2"
    echo ""
    echo "You can now:"
    echo "  1. Upload PDF files to the web app"
    echo "  2. Process scanned sheet music PDFs"
    echo ""
    echo "Start the server with:"
    echo "  cd web_app && python3.11 server.py"
    echo ""
else
    echo ""
    echo "=============================================="
    echo "  ❌ INSTALLATION FAILED"
    echo "=============================================="
    echo ""
    echo "Please check the error messages above."
    exit 1
fi
