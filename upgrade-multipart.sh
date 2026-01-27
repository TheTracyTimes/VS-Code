#!/bin/bash

echo "=============================================="
echo "  Upgrading python-multipart"
echo "=============================================="
echo ""
echo "This fixes the file upload limit issue."
echo ""

echo "Step 1: Uninstalling old version (0.0.6)..."
pip3.11 uninstall -y python-multipart 2>/dev/null || pip3 uninstall -y python-multipart

echo ""
echo "Step 2: Installing new version (0.0.9+)..."
pip3.11 install "python-multipart>=0.0.9" || pip3 install "python-multipart>=0.0.9"

if [ $? -eq 0 ]; then
    echo ""
    echo "=============================================="
    echo "  ✅ UPGRADE SUCCESSFUL!"
    echo "=============================================="
    echo ""
    echo "The file upload limit has been fixed."
    echo ""
    echo "Now restart your server:"
    echo "  bash restart-server.sh"
    echo ""
    echo "You should now be able to upload 12+ files at once!"
    echo ""
else
    echo ""
    echo "=============================================="
    echo "  ❌ UPGRADE FAILED"
    echo "=============================================="
    echo ""
    echo "Please check the error messages above."
    exit 1
fi
