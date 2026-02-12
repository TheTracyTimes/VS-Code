#!/bin/bash
# Local development server with config generation

echo "🔧 Setting up local development environment..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please create .env from .env.example and add your credentials"
    exit 1
fi

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
echo "🚀 Starting development server..."
echo "📍 Server will be available at: http://localhost:8000"
echo ""
echo "📋 Available pages:"
echo "   - Home: http://localhost:8000/"
echo "   - Registration: http://localhost:8000/forms/registration.html"
echo "   - Volunteer: http://localhost:8000/forms/volunteer.html"
echo "   - Vendor: http://localhost:8000/forms/vendor.html"
echo ""
echo "⚠️  Note: Config files are in .gitignore and will NOT be committed"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Start Python simple HTTP server
cd public && python3 -m http.server 8000
