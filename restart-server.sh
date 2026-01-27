#!/bin/bash

echo "=============================================="
echo "  Restarting Music Recognition Server"
echo "=============================================="
echo ""

# Find and kill any existing server
PID=$(lsof -ti:8000)

if [ ! -z "$PID" ]; then
    echo "Stopping existing server (PID: $PID)..."
    kill $PID 2>/dev/null
    sleep 2
    
    # Force kill if still running
    if lsof -ti:8000 > /dev/null 2>&1; then
        echo "Force stopping..."
        kill -9 $PID 2>/dev/null
        sleep 1
    fi
fi

# Check if port is now free
if lsof -ti:8000 > /dev/null 2>&1; then
    echo "❌ Port 8000 is still in use!"
    echo ""
    echo "Try manually:"
    echo "  1. Find the process: lsof -ti:8000"
    echo "  2. Kill it: kill -9 <PID>"
    echo "  3. Then run: cd web_app && python3.11 server.py"
    exit 1
fi

echo "✅ Port 8000 is free"
echo ""

# Check if we're in the right directory
if [ ! -d "web_app" ]; then
    echo "❌ Error: web_app directory not found"
    echo "Please run this script from the VS-Code directory"
    exit 1
fi

# Start the server
echo "Starting server with Python 3.11..."
echo ""
echo "=============================================="
echo ""

cd web_app
python3.11 server.py
