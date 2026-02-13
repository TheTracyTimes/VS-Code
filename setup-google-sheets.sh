#!/bin/bash
# Google Sheets Setup Script for Firebase
# This script helps you configure Google Sheets integration

echo "======================================"
echo "Google Sheets Integration Setup"
echo "======================================"
echo ""

# Check if firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo "❌ Firebase CLI not found. Installing..."
    npm install -g firebase-tools
fi

echo "Step 1: Login to Firebase"
firebase login

echo ""
echo "Step 2: Select your Firebase project"
firebase use sarasota-gospel-temple

echo ""
echo "======================================"
echo "Now we'll set up the Firebase Secrets"
echo "======================================"
echo ""
echo "You'll need:"
echo "  1. Service account JSON file path"
echo "  2. Three Google Sheets spreadsheet IDs"
echo ""

# Set service account JSON
echo "Step 3: Set Google Service Account credentials"
read -p "Enter path to your service account JSON file: " SERVICE_ACCOUNT_PATH

if [ -f "$SERVICE_ACCOUNT_PATH" ]; then
    echo "Setting GOOGLE_SERVICE_ACCOUNT_JSON secret..."
    firebase functions:secrets:set GOOGLE_SERVICE_ACCOUNT_JSON < "$SERVICE_ACCOUNT_PATH"
    echo "✅ Service account configured!"
else
    echo "❌ File not found: $SERVICE_ACCOUNT_PATH"
    exit 1
fi

echo ""
echo "Step 4: Set Google Sheets Spreadsheet IDs"
echo "Get these from your Google Sheets URLs:"
echo "https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit"
echo ""

read -p "Enter Registrations Spreadsheet ID: " REG_ID
echo "$REG_ID" | firebase functions:secrets:set GOOGLE_SHEETS_REGISTRATIONS_ID

read -p "Enter Volunteers Spreadsheet ID: " VOL_ID
echo "$VOL_ID" | firebase functions:secrets:set GOOGLE_SHEETS_VOLUNTEERS_ID

read -p "Enter Vendors Spreadsheet ID: " VEN_ID
echo "$VEN_ID" | firebase functions:secrets:set GOOGLE_SHEETS_VENDORS_ID

echo ""
echo "✅ All secrets configured!"
echo ""
echo "======================================"
echo "Step 5: Deploy Firebase Functions"
echo "======================================"
read -p "Deploy functions now? (y/n): " DEPLOY

if [ "$DEPLOY" = "y" ] || [ "$DEPLOY" = "Y" ]; then
    echo "Deploying functions with secrets..."
    firebase deploy --only functions
    echo ""
    echo "✅ Deployment complete!"
else
    echo "⚠️  Remember to deploy later with: firebase deploy --only functions"
fi

echo ""
echo "======================================"
echo "Setup Complete! 🎉"
echo "======================================"
echo ""
echo "Your Google Sheets integration is now configured."
echo ""
echo "To test:"
echo "1. Go to your admin dashboard"
echo "2. Click '📊 Sync to Google Sheets' button"
echo "3. Check your Google Sheets for data"
echo ""
echo "Note: Forms will now automatically sync to Google Sheets when submitted!"
echo ""
