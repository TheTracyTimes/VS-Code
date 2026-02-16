#!/bin/bash
# Local development server with config generation

echo "🔧 Setting up local development environment..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please create .env from .env.example and add your credentials"
    exit 1
fi

# Cleanup function to remove config files when server stops
cleanup() {
    echo ""
    echo "🧹 Cleaning up config files..."
    rm -rf public/config/
    echo "✅ Config files removed"
    echo "👋 Server stopped"
    exit 0
}

# Set trap to cleanup on exit
trap cleanup EXIT INT TERM

# Generate config files from environment variables
echo "📝 Generating config files from .env..."
export $(cat .env | grep -v '^#' | xargs)
bash build.sh

# Check if config files were created
if [ ! -f "public/config/firebase-config.js" ]; then
    echo "❌ Failed to generate config files"
    exit 1
fi

echo "✅ Config files generated"
echo ""
echo "⚠️  SECURITY NOTICE:"
echo "   - Server binds to 127.0.0.1 (localhost only)"
echo "   - Config files will be automatically deleted when server stops"
echo "   - Config files contain API keys but are in .gitignore"
echo "   - These API keys are meant for client-side use (see SECURITY.md)"
echo ""
echo "🚀 Starting development server..."
echo "📍 Server will be available at: http://127.0.0.1:8000"
echo ""
echo "📋 Available pages:"
echo "   - Home: http://127.0.0.1:8000/"
echo "   - Registration: http://127.0.0.1:8000/forms/registration.html"
echo "   - Volunteer: http://127.0.0.1:8000/forms/volunteer.html"
echo "   - Vendor: http://127.0.0.1:8000/forms/vendor.html"
echo ""
echo "🛑 Press Ctrl+C to stop the server and clean up config files"
echo ""

# Start Python simple HTTP server bound to localhost only
cd public && python3 -m http.server 8000 --bind 127.0.0.1
