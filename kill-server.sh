#!/bin/bash

echo "=============================================="
echo "  Stopping Music Recognition Server"
echo "=============================================="
echo ""

# Find the process using port 8000
PID=$(lsof -ti:8000)

if [ -z "$PID" ]; then
    echo "✅ No server is running on port 8000"
    echo ""
    echo "You can now start the server with:"
    echo "  cd web_app && python3.11 server.py"
    echo ""
else
    echo "Found server process: $PID"
    echo "Stopping it..."
    
    kill $PID
    
    # Wait a moment for it to stop
    sleep 1
    
    # Check if it's really stopped
    if lsof -ti:8000 > /dev/null 2>&1; then
        echo "⚠️  Process didn't stop gracefully. Force killing..."
        kill -9 $PID
        sleep 1
    fi
    
    # Final check
    if lsof -ti:8000 > /dev/null 2>&1; then
        echo "❌ Failed to stop the server"
        echo "You may need to restart your computer or manually kill process $PID"
    else
        echo "✅ Server stopped successfully!"
        echo ""
        echo "You can now start it again with:"
        echo "  cd web_app && python3.11 server.py"
    fi
    echo ""
fi
