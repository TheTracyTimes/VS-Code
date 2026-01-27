#!/bin/bash

echo "=============================================="
echo "AUTOMATIC FILE RECOVERY"
echo "=============================================="
echo ""

# Check if we're in the right directory
if [ ! -f "verify_installation.py" ]; then
    echo "❌ Error: Please run this script from the VS-Code directory"
    exit 1
fi

echo "Step 1: Checking current branch..."
current_branch=$(git branch --show-current)
echo "Current branch: $current_branch"

if [ "$current_branch" != "claude/handwritten-music-llm-qDHLY" ]; then
    echo "⚠️  You're on the wrong branch!"
    echo "Switching to claude/handwritten-music-llm-qDHLY..."
    git checkout claude/handwritten-music-llm-qDHLY
    if [ $? -ne 0 ]; then
        echo "❌ Failed to switch branches"
        exit 1
    fi
fi

echo ""
echo "Step 2: Fetching latest changes from remote..."
git fetch origin claude/handwritten-music-llm-qDHLY
if [ $? -ne 0 ]; then
    echo "❌ Failed to fetch from remote"
    exit 1
fi

echo ""
echo "Step 3: Checking for deleted files..."
deleted_files=$(git status --short | grep "^ D" | wc -l)
if [ $deleted_files -gt 0 ]; then
    echo "⚠️  Found $deleted_files deleted files"
    echo "Restoring them..."
    git restore music_recognition/
    echo "✅ Files restored"
else
    echo "✅ No deleted files found"
fi

echo ""
echo "Step 4: Pulling latest changes..."
git pull origin claude/handwritten-music-llm-qDHLY
if [ $? -ne 0 ]; then
    echo "⚠️  Pull failed. Trying merge strategy..."
    git pull --rebase origin claude/handwritten-music-llm-qDHLY
    if [ $? -ne 0 ]; then
        echo "❌ Pull still failed. You may need to manually resolve conflicts."
        exit 1
    fi
fi

echo ""
echo "Step 5: Verifying installation..."
python3 verify_installation.py

echo ""
echo "=============================================="
echo "RECOVERY COMPLETE"
echo "=============================================="
echo ""
echo "Next steps:"
echo "1. If verification passed, run: bash install-full.sh"
echo "2. Then start server: cd web_app && python3.11 server.py"
echo "3. Open browser: localhost:8000"
echo ""
