# Google Sheets Sync Fix Guide

## Problem Summary

The Google Sheets sync stopped working after adding security to the site because:

1. **Security changes moved authentication from client-side to server-side**
   - Old implementation: Client-side OAuth (worked before)
   - New implementation: Firebase Functions with Google Service Account (more secure)

2. **Firebase Secrets are not configured in production**
   - Your `.env` file has all the correct values locally
   - But Firebase Functions in production need these values as **Firebase Secrets**
   - Local `.env` file is only used during local development

## What You Need to Do

### Step 1: Authenticate with Firebase CLI

If you haven't already, authenticate with Firebase:

```bash
firebase login
```

This will open your browser to sign in with your Google account.

### Step 2: Run the Setup Script

We've created a script that will automatically configure all Firebase Secrets from your `.env` file:

```bash
./setup-firebase-secrets.sh
```

This script will:
- ✅ Load configuration from your `.env` file
- ✅ Set `GOOGLE_SERVICE_ACCOUNT_JSON` secret
- ✅ Set `GOOGLE_SHEETS_REGISTRATIONS_ID` secret
- ✅ Set `GOOGLE_SHEETS_VOLUNTEERS_ID` secret
- ✅ Set `GOOGLE_SHEETS_VENDORS_ID` secret

### Step 3: Share Google Sheets with Service Account

**CRITICAL:** Each Google Sheet must be shared with your service account email.

**Service Account Email:**
```
firebase-sheets-sync@sarasota-gospel-temple-486615.iam.gserviceaccount.com
```

**For each Google Sheet:**

1. **Registrations Sheet:**
   - URL: https://docs.google.com/spreadsheets/d/1q7vxkgof14p6OpHehTySIU6c0qNpbencA6E09agYJTg
   - Click **Share** button
   - Add: `firebase-sheets-sync@sarasota-gospel-temple-486615.iam.gserviceaccount.com`
   - Permission: **Editor**
   - Click **Send**

2. **Volunteers Sheet:**
   - URL: https://docs.google.com/spreadsheets/d/1T45QcAsY7m5SO8gSQKTvHI_PFFa4qx1x6dwW3iwG0s0
   - Click **Share** button
   - Add: `firebase-sheets-sync@sarasota-gospel-temple-486615.iam.gserviceaccount.com`
   - Permission: **Editor**
   - Click **Send**

3. **Vendors Sheet:**
   - URL: https://docs.google.com/spreadsheets/d/1V6G2KN1vvTB5Ng249rg9K6ijbUT7tou_jaE9ygALxeM
   - Click **Share** button
   - Add: `firebase-sheets-sync@sarasota-gospel-temple-486615.iam.gserviceaccount.com`
   - Permission: **Editor**
   - Click **Send**

### Step 4: Deploy Firebase Functions

After configuring secrets, redeploy your Firebase Functions:

```bash
firebase deploy --only functions
```

This will deploy the functions with access to the newly configured secrets.

### Step 5: Test the Sync

1. Open your admin dashboard: https://sarasota-gospel-temple.web.app/admin.html
2. Sign in as admin
3. Go to any section (Registrations, Volunteers, or Vendors)
4. Click **Sync to Sheets**
5. Check for success message

If you see errors:
- Open browser console (F12 > Console) for detailed error messages
- Check Firebase Functions logs: `firebase functions:log`
- Refer to [GOOGLE_SHEETS_TROUBLESHOOTING.md](./GOOGLE_SHEETS_TROUBLESHOOTING.md)

## Manual Setup (Alternative)

If you prefer to set secrets manually instead of using the script:

```bash
# 1. Authenticate with Firebase
firebase login

# 2. Set service account JSON
firebase functions:secrets:set GOOGLE_SERVICE_ACCOUNT_JSON
# When prompted, paste the entire JSON content from your .env file

# 3. Set registrations spreadsheet ID
echo "1q7vxkgof14p6OpHehTySIU6c0qNpbencA6E09agYJTg" | firebase functions:secrets:set GOOGLE_SHEETS_REGISTRATIONS_ID

# 4. Set volunteers spreadsheet ID
echo "1T45QcAsY7m5SO8gSQKTvHI_PFFa4qx1x6dwW3iwG0s0" | firebase functions:secrets:set GOOGLE_SHEETS_VOLUNTEERS_ID

# 5. Set vendors spreadsheet ID
echo "1V6G2KN1vvTB5Ng249rg9K6ijbUT7tou_jaE9ygALxeM" | firebase functions:secrets:set GOOGLE_SHEETS_VENDORS_ID

# 6. Deploy functions
firebase deploy --only functions
```

## Verification Checklist

Before testing, verify all of these:

- [ ] Firebase CLI is authenticated (`firebase login`)
- [ ] All 4 Firebase Secrets are configured
- [ ] Registrations sheet is shared with service account (Editor access)
- [ ] Volunteers sheet is shared with service account (Editor access)
- [ ] Vendors sheet is shared with service account (Editor access)
- [ ] Firebase Functions are deployed with latest code
- [ ] You're using the correct Firebase project (sarasota-gospel-temple)

## Why This Happened

The security implementation moved Google Sheets authentication from:
- **Before:** Client-side OAuth (less secure, but simpler)
- **After:** Server-side service account (more secure, requires Firebase Secrets)

The benefits of the new approach:
- ✅ More secure (credentials never exposed to client)
- ✅ No OAuth popup for users
- ✅ Better error handling
- ✅ Consistent authentication
- ✅ Works reliably across all browsers

## Common Errors After Setup

### "Service account does not have access to spreadsheet"
- **Solution:** Share the sheet with the service account email (Editor access)

### "Missing spreadsheet ID for [type]"
- **Solution:** Verify the secret is set: `firebase functions:secrets:access GOOGLE_SHEETS_[TYPE]_ID`

### "Invalid Google service account credentials format"
- **Solution:** Re-set the `GOOGLE_SERVICE_ACCOUNT_JSON` secret with valid JSON

## Need Help?

Check these resources:
- [GOOGLE_SHEETS_TROUBLESHOOTING.md](./GOOGLE_SHEETS_TROUBLESHOOTING.md) - Comprehensive error reference
- [GOOGLE_SHEETS_SETUP.md](./GOOGLE_SHEETS_SETUP.md) - Full setup guide
- Firebase Functions logs: `firebase functions:log`
- Browser console: F12 > Console tab

## Technical Details

**Firebase Functions using secrets:**
- Location: `functions/index.js` (lines 293-581)
- Functions: `appendToSheet`, `syncAllToSheet`
- Secrets accessed via: `defineSecret()` and `secret.value()`

**Service Account:**
- Email: `firebase-sheets-sync@sarasota-gospel-temple-486615.iam.gserviceaccount.com`
- Project: `sarasota-gospel-temple-486615`
- Type: Google Cloud Service Account

**Spreadsheet IDs:**
- Registrations: `1q7vxkgof14p6OpHehTySIU6c0qNpbencA6E09agYJTg`
- Volunteers: `1T45QcAsY7m5SO8gSQKTvHI_PFFa4qx1x6dwW3iwG0s0`
- Vendors: `1V6G2KN1vvTB5Ng249rg9K6ijbUT7tou_jaE9ygALxeM`
