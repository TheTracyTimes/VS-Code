# Google Sheets Integration Setup Guide

This guide will help you connect your Firebase forms to Google Sheets.

## Quick Start

Run the automated setup script:

```bash
./setup-google-sheets.sh
```

Or follow the manual steps below.

---

## Prerequisites

Before you begin, make sure you have:
- ✅ A Google Cloud account
- ✅ Firebase CLI installed (`npm install -g firebase-tools`)
- ✅ Firebase project set up (`sarasota-gospel-temple`)

---

## Manual Setup Steps

### 1️⃣ Create Google Cloud Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select or create a project
3. Navigate to **APIs & Services → Credentials**
4. Click **Create Credentials → Service Account**
5. Fill in:
   - **Name**: `firebase-sheets-sync`
   - **Description**: `Service account for syncing Firebase data to Google Sheets`
6. Click **Create and Continue**
7. Grant role: **Editor**
8. Click **Done**
9. Click on the service account you just created
10. Go to **Keys** tab
11. Click **Add Key → Create new key**
12. Choose **JSON** format
13. Download the JSON file (save it securely!)

**Example JSON file** (`service-account.json`):
```json
{
  "type": "service_account",
  "project_id": "your-project",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-sheets-sync@your-project.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "..."
}
```

### 2️⃣ Enable Google Sheets API

1. In Google Cloud Console, go to **APIs & Services → Library**
2. Search for **"Google Sheets API"**
3. Click **Enable**

### 3️⃣ Create Google Sheets

Create 3 spreadsheets with these headers:

#### **Registrations Sheet**
```
Timestamp | ID | First Name | Last Name | Phone | Email | Pastor Name | Assembly Name | Services | Airport Transport | Local Transport | Has Children | Number of Children | VBS Attendance | Nursery Attendance
```

#### **Volunteers Sheet**
```
Timestamp | ID | First Name | Last Name | Phone | Email | Committees | Availability | Committee Assignments
```

#### **Vendors Sheet**
```
Timestamp | ID | Business Name | First Name | Last Name | Phone | Email | Website | Pastor Name | Assembly Name | Selling | Goods Type | Table Staffed | Availability | Status | Approved
```

### 4️⃣ Share Sheets with Service Account

For **each of the 3 spreadsheets**:

1. Open the Google Sheet
2. Click the **Share** button
3. Add the **service account email** from your JSON file
   - Find `client_email` in the JSON file
   - Example: `firebase-sheets-sync@your-project.iam.gserviceaccount.com`
4. Give it **Editor** permissions
5. Click **Send**

⚠️ **Important**: If you forget this step, you'll get "Permission denied" errors!

### 5️⃣ Get Spreadsheet IDs

For each sheet, copy the Spreadsheet ID from the URL:

```
https://docs.google.com/spreadsheets/d/1q7vxkgof14p6OpHehTySIU6c0qNpbencA6E09agYJTg/edit
                                      ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
                                      This is the Spreadsheet ID
```

You'll need:
- Registrations Spreadsheet ID
- Volunteers Spreadsheet ID
- Vendors Spreadsheet ID

### 6️⃣ Configure Firebase Secrets

**Option A: Using the Firebase Console**

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project: `sarasota-gospel-temple`
3. Go to **Functions** → **Secrets**
4. Add the following secrets:
   - `GOOGLE_SERVICE_ACCOUNT_JSON` - Paste the entire JSON file contents
   - `GOOGLE_SHEETS_REGISTRATIONS_ID` - Your registrations spreadsheet ID
   - `GOOGLE_SHEETS_VOLUNTEERS_ID` - Your volunteers spreadsheet ID
   - `GOOGLE_SHEETS_VENDORS_ID` - Your vendors spreadsheet ID

**Option B: Using Firebase CLI** (Recommended)

```bash
# 1. Login to Firebase
firebase login

# 2. Select your project
firebase use sarasota-gospel-temple

# 3. Set service account JSON
firebase functions:secrets:set GOOGLE_SERVICE_ACCOUNT_JSON < /path/to/service-account.json

# 4. Set spreadsheet IDs (replace with your actual IDs)
echo "1q7vxkgof14p6OpHehTySIU6c0qNpbencA6E09agYJTg" | firebase functions:secrets:set GOOGLE_SHEETS_REGISTRATIONS_ID
echo "1T45QcAsY7m5SO8gSQKTvHI_PFFa4qx1x6dwW3iwG0s0" | firebase functions:secrets:set GOOGLE_SHEETS_VOLUNTEERS_ID
echo "1V6G2KN1vvTB5Ng249rg9K6ijbUT7tou_jaE9ygALxeM" | firebase functions:secrets:set GOOGLE_SHEETS_VENDORS_ID
```

### 7️⃣ Deploy Firebase Functions

```bash
# Deploy functions with the new secrets
firebase deploy --only functions
```

This will deploy:
- `appendToSheet` - Syncs individual form submissions
- `syncAllToSheet` - Bulk syncs all data from admin dashboard

---

## Testing

### Test Automatic Sync

1. Go to your website: https://sarasotagospel.com
2. Fill out any form (registration/volunteer/vendor)
3. Submit the form
4. Check your Google Sheet - a new row should appear!

### Test Manual Sync

1. Go to the admin dashboard: https://sarasotagospel.com/admin/dashboard.html
2. Login with admin credentials
3. Navigate to any section (Registrations/Volunteers/Vendors)
4. Click **"📊 Sync to Google Sheets"** button
5. Check your Google Sheet - all data should be synced!

---

## Troubleshooting

### Error: "Permission denied"
**Solution**: Make sure you shared the Google Sheets with the service account email (`client_email` from JSON file)

### Error: "Google Sheets not configured"
**Solution**: Check that all Firebase Secrets are set correctly:
```bash
firebase functions:secrets:access GOOGLE_SERVICE_ACCOUNT_JSON
firebase functions:secrets:access GOOGLE_SHEETS_REGISTRATIONS_ID
firebase functions:secrets:access GOOGLE_SHEETS_VOLUNTEERS_ID
firebase functions:secrets:access GOOGLE_SHEETS_VENDORS_ID
```

### Error: "Invalid credentials"
**Solution**: Verify your service account JSON is valid and the Google Sheets API is enabled

### Data not appearing in sheets
**Solutions**:
1. Check Firebase Functions logs: `firebase functions:log`
2. Verify sheet names are "Sheet1" (or update range in `functions/index.js:346`)
3. Ensure service account has Editor permissions on the sheets

### Check Firebase Functions Logs

```bash
# View recent logs
firebase functions:log

# View logs in real-time
firebase functions:log --follow
```

---

## How It Works

### Architecture

```
┌─────────────┐
│ User Fills  │
│ Form        │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ Frontend JavaScript │
│ (registration-form) │
└──────┬──────────────┘
       │ Calls Firebase Function
       ▼
┌──────────────────────────────┐
│ Firebase Cloud Function      │
│ (appendToSheet)              │
│                              │
│ - Validates data             │
│ - Gets credentials from      │
│   Firebase Secrets           │
│ - Authenticates with Google  │
└──────┬───────────────────────┘
       │
       ▼
┌─────────────────┐
│ Google Sheets   │
│ API             │
│                 │
│ Appends new row │
└─────────────────┘
```

### Security

✅ **Service account credentials** are stored in Firebase Secrets (not in code)
✅ **Spreadsheet IDs** are stored in Firebase Secrets
✅ **No credentials** are exposed in client-side code
✅ **Google Sheets API** access is controlled by service account permissions

---

## Files Modified

- `functions/index.js` - Contains `appendToSheet` and `syncAllToSheet` functions
- `public/js/google-sheets-service.js` - Frontend service for calling Cloud Functions
- `public/admin/dashboard.html` - Admin UI with sync buttons
- `.env.example` - Example environment variables (for local dev)

---

## Maintenance

### Update Spreadsheet IDs

If you create new spreadsheets:

```bash
echo "NEW_SPREADSHEET_ID" | firebase functions:secrets:set GOOGLE_SHEETS_REGISTRATIONS_ID
firebase deploy --only functions
```

### Rotate Service Account Credentials

If you need to rotate the service account:

1. Create a new service account key in Google Cloud Console
2. Update the Firebase Secret:
   ```bash
   firebase functions:secrets:set GOOGLE_SERVICE_ACCOUNT_JSON < new-service-account.json
   ```
3. Deploy functions:
   ```bash
   firebase deploy --only functions
   ```
4. Delete the old service account key in Google Cloud Console

---

## Support

For issues, check:
- Firebase Functions logs: `firebase functions:log`
- Google Cloud Console: [Error Reporting](https://console.cloud.google.com/errors)
- Browser console (F12) when testing frontend

**Contact**:
- Email: sarasotagospel@gmail.com
- Phone: 941-800-5211

---

## Additional Resources

- [Firebase Secrets Manager Docs](https://firebase.google.com/docs/functions/config-env#secret-manager)
- [Google Sheets API Docs](https://developers.google.com/sheets/api)
- [Service Account Auth Guide](https://cloud.google.com/iam/docs/service-accounts)
