#!/bin/bash

echo "=============================================="
echo "  Checking python-multipart Version"
echo "=============================================="
echo ""

echo "Checking with python3.11..."
version=$(python3.11 -c "import multipart; print(multipart.__version__)" 2>/dev/null)

if [ $? -eq 0 ]; then
    echo "✅ python-multipart is installed"
    echo "   Version: $version"
    echo ""
    
    if [[ "$version" < "0.0.9" ]]; then
        echo "❌ Version is TOO OLD (need 0.0.9 or higher)"
        echo ""
        echo "To fix, run:"
        echo "  bash upgrade-multipart.sh"
    else
        echo "✅ Version is good (0.0.9+)"
        echo ""
        echo "The multipart upgrade is installed correctly."
        echo "The 11-file limit should be fixed."
    fi
else
    echo "❌ python-multipart is NOT installed"
    echo ""
    echo "To install, run:"
    echo "  pip3.11 install 'python-multipart>=0.0.9'"
fi

echo ""
echo "=============================================="
