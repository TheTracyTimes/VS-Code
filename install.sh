#!/bin/bash

# Installation Script for Music Recognition Web App
# This script helps you install the necessary dependencies

echo "================================================"
echo "  Music Recognition Web App - Setup"
echo "================================================"
echo ""
echo "You have TWO installation options:"
echo ""
echo "1. QUICK DEMO (Web app only - 100MB)"
echo "   - Runs web interface immediately"
echo "   - Creates sample PDFs to show workflow"
echo "   - No real music recognition (demo mode)"
echo ""
echo "2. FULL INSTALL (Complete system - 2.5GB)"
echo "   - Real music recognition with AI"
echo "   - Processes actual handwritten music"
echo "   - Includes PyTorch (~2GB)"
echo ""
echo "================================================"
echo ""

read -p "Which installation? (1=Quick Demo, 2=Full Install): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "📦 Installing QUICK DEMO (Web App Only)..."
    echo ""
    pip install fastapi uvicorn[standard] python-multipart websockets aiofiles reportlab
    echo ""
    echo "✅ Quick demo installed!"
    echo ""
    echo "To start the web app:"
    echo "  cd web_app"
    echo "  ./start.sh"
    echo ""
    echo "Note: This will run in DEMO MODE (sample files only)"
    echo "      To enable real processing, run this installer again"
    echo "      and choose option 2."
    echo ""

elif [ "$choice" = "2" ]; then
    echo ""
    echo "📦 Installing FULL SYSTEM (with PyTorch)..."
    echo ""
    echo "⚠️  This will download ~2.5GB of data"
    echo "⚠️  May take 5-15 minutes depending on your internet"
    echo ""
    read -p "Continue? (y/n): " confirm

    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        echo ""
        echo "Installing all dependencies from requirements.txt..."
        pip install -r requirements.txt
        echo ""
        echo "✅ Full system installed!"
        echo ""
        echo "To start the web app with REAL processing:"
        echo "  cd web_app"
        echo "  ./start.sh"
        echo ""
        echo "The system will now digitize actual handwritten music!"
        echo ""
    else
        echo ""
        echo "Installation cancelled."
        echo ""
    fi
else
    echo ""
    echo "Invalid choice. Please run the installer again."
    echo ""
fi

echo "================================================"
