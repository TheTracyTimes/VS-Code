#!/bin/bash

# ⚠️ DEPRECATED - This script is no longer needed
#
# This project now uses Google Sheets API with OAuth (client-side),
# NOT Firebase Functions with service accounts.
#
# Please see: GOOGLE-SHEETS-SETUP.md for current setup instructions
#
# This script is kept for reference only.

set -e

echo "============================================"
echo "⚠️  DEPRECATION NOTICE"
echo "============================================"
echo ""
echo "This script is DEPRECATED and no longer used."
echo ""
echo "This project now uses Google Sheets API with OAuth"
echo "authentication, which does NOT require Firebase secrets"
echo "or service accounts."
echo ""
echo "Please see: GOOGLE-SHEETS-SETUP.md"
echo "Or: NETLIFY_DEPLOYMENT.md"
echo ""
echo "======================================"
echo ""
read -p "Do you want to continue anyway? (y/n): " CONTINUE
if [ "$CONTINUE" != "y" ] && [ "$CONTINUE" != "Y" ]; then
    echo "Setup cancelled."
    exit 0
fi

echo ""
echo "============================================"
echo "Firebase Secrets Setup for Google Sheets"
echo "============================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Firebase CLI is authenticated
echo "Checking Firebase authentication..."
if ! firebase projects:list &> /dev/null; then
    echo -e "${RED}Error: Not authenticated with Firebase${NC}"
    echo ""
    echo "Please run: firebase login"
    echo "Then run this script again."
    exit 1
fi

echo -e "${GREEN}✓ Firebase CLI is authenticated${NC}"
echo ""

# Load .env file
if [ ! -f ".env" ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    exit 1
fi

# Extract values from .env
echo "Loading configuration from .env file..."
source .env

# Set Firebase Secrets
echo ""
echo "Setting Firebase Secrets..."
echo ""

# 1. Set Google Service Account JSON
echo "1. Setting GOOGLE_SERVICE_ACCOUNT_JSON..."
if [ -z "$GOOGLE_SERVICE_ACCOUNT_JSON" ]; then
    echo -e "${RED}Error: GOOGLE_SERVICE_ACCOUNT_JSON not found in .env${NC}"
    exit 1
fi

echo "$GOOGLE_SERVICE_ACCOUNT_JSON" | firebase functions:secrets:set GOOGLE_SERVICE_ACCOUNT_JSON
echo -e "${GREEN}✓ GOOGLE_SERVICE_ACCOUNT_JSON configured${NC}"
echo ""

# 2. Set Registrations Spreadsheet ID
echo "2. Setting GOOGLE_SHEETS_REGISTRATIONS_ID..."
if [ -z "$GOOGLE_SHEETS_REGISTRATIONS_ID" ]; then
    echo -e "${RED}Error: GOOGLE_SHEETS_REGISTRATIONS_ID not found in .env${NC}"
    exit 1
fi

echo "$GOOGLE_SHEETS_REGISTRATIONS_ID" | firebase functions:secrets:set GOOGLE_SHEETS_REGISTRATIONS_ID
echo -e "${GREEN}✓ GOOGLE_SHEETS_REGISTRATIONS_ID configured${NC}"
echo ""

# 3. Set Volunteers Spreadsheet ID
echo "3. Setting GOOGLE_SHEETS_VOLUNTEERS_ID..."
if [ -z "$GOOGLE_SHEETS_VOLUNTEERS_ID" ]; then
    echo -e "${RED}Error: GOOGLE_SHEETS_VOLUNTEERS_ID not found in .env${NC}"
    exit 1
fi

echo "$GOOGLE_SHEETS_VOLUNTEERS_ID" | firebase functions:secrets:set GOOGLE_SHEETS_VOLUNTEERS_ID
echo -e "${GREEN}✓ GOOGLE_SHEETS_VOLUNTEERS_ID configured${NC}"
echo ""

# 4. Set Vendors Spreadsheet ID
echo "4. Setting GOOGLE_SHEETS_VENDORS_ID..."
if [ -z "$GOOGLE_SHEETS_VENDORS_ID" ]; then
    echo -e "${RED}Error: GOOGLE_SHEETS_VENDORS_ID not found in .env${NC}"
    exit 1
fi

echo "$GOOGLE_SHEETS_VENDORS_ID" | firebase functions:secrets:set GOOGLE_SHEETS_VENDORS_ID
echo -e "${GREEN}✓ GOOGLE_SHEETS_VENDORS_ID configured${NC}"
echo ""

# Success summary
echo ""
echo "============================================"
echo -e "${GREEN}All Firebase Secrets configured successfully!${NC}"
echo "============================================"
echo ""
echo "Service Account Email (for sharing sheets):"
echo -e "${YELLOW}firebase-sheets-sync@sarasota-gospel-temple-486615.iam.gserviceaccount.com${NC}"
echo ""
echo "NEXT STEPS:"
echo ""
echo "1. Share each Google Sheet with the service account email above (Editor access)"
echo "   - Registrations: https://docs.google.com/spreadsheets/d/$GOOGLE_SHEETS_REGISTRATIONS_ID"
echo "   - Volunteers: https://docs.google.com/spreadsheets/d/$GOOGLE_SHEETS_VOLUNTEERS_ID"
echo "   - Vendors: https://docs.google.com/spreadsheets/d/$GOOGLE_SHEETS_VENDORS_ID"
echo ""
echo "2. Deploy Firebase Functions:"
echo "   firebase deploy --only functions"
echo ""
echo "3. Test the sync from the admin dashboard"
echo ""
