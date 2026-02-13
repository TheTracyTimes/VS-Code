# Google Sheets Sync Troubleshooting Guide

This guide helps you diagnose and fix Google Sheets synchronization errors.

## Common Error Messages

### "Error syncing to Google Sheets: internal"

This generic error typically indicates one of the following issues:

1. **Missing Firebase Secrets** - Required secrets are not configured
2. **Invalid Credentials** - Service account JSON is malformed
3. **Missing Spreadsheet IDs** - Spreadsheet IDs are not configured
4. **Permission Issues** - Service account lacks access to spreadsheets

## Required Configuration

### 1. Firebase Secrets

You need to configure the following secrets in Firebase:

#### Google Service Account
- **Secret Name:** `GOOGLE_SERVICE_ACCOUNT_JSON`
- **Value:** The full JSON content of your Google Cloud service account key file
- **Format:** Valid JSON starting with `{"type": "service_account", ...}`

#### Spreadsheet IDs
- **Secret Name:** `GOOGLE_SHEETS_REGISTRATIONS_ID`
- **Value:** The spreadsheet ID for registrations (from the URL)

- **Secret Name:** `GOOGLE_SHEETS_VOLUNTEERS_ID`
- **Value:** The spreadsheet ID for volunteers (from the URL)

- **Secret Name:** `GOOGLE_SHEETS_VENDORS_ID`
- **Value:** The spreadsheet ID for vendors (from the URL)

### 2. Finding Your Spreadsheet ID

The spreadsheet ID is in the Google Sheets URL:
```
https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_HERE/edit
                                        ^^^^^^^^^^^^^^^^^^^
```

Example:
```
https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
```
The spreadsheet ID is: `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`

### 3. Service Account Permissions

**CRITICAL:** You must share each Google Sheet with your service account email.

1. Open your service account JSON file
2. Find the `client_email` field (looks like `your-service@project.iam.gserviceaccount.com`)
3. Open each Google Sheet
4. Click **Share** button
5. Add the service account email
6. Give it **Editor** permission
7. Click **Send**

## Error Message Reference

### "Missing spreadsheet ID for [type]"
**Cause:** The spreadsheet ID secret is not configured in Firebase.

**Solution:**
1. Set the Firebase secret for the missing type:
   - Registrations: `GOOGLE_SHEETS_REGISTRATIONS_ID`
   - Volunteers: `GOOGLE_SHEETS_VOLUNTEERS_ID`
   - Vendors: `GOOGLE_SHEETS_VENDORS_ID`

### "Spreadsheet not found"
**Cause:** The spreadsheet ID is incorrect or the spreadsheet was deleted.

**Solution:**
1. Verify the spreadsheet exists
2. Check the ID is correct (copy from URL)
3. Update the Firebase secret with the correct ID

### "Service account does not have access to spreadsheet"
**Cause:** The service account hasn't been given permission to access the spreadsheet.

**Solution:**
1. Find your service account email in the JSON credentials (`client_email` field)
2. Open the Google Sheet
3. Click Share
4. Add the service account email with Editor access

### "Invalid Google service account credentials format"
**Cause:** The service account JSON is malformed or invalid.

**Solution:**
1. Download a fresh copy of your service account key from Google Cloud Console:
   - Go to IAM & Admin > Service Accounts
   - Click on your service account
   - Go to Keys tab
   - Add Key > Create New Key > JSON
2. Copy the ENTIRE contents of the downloaded JSON file
3. Update the `GOOGLE_SERVICE_ACCOUNT_JSON` secret in Firebase

### "Google Sheets not configured"
**Cause:** The service account credentials are missing entirely.

**Solution:**
1. Create a service account in Google Cloud Console (see setup guide)
2. Download the JSON key file
3. Set the `GOOGLE_SERVICE_ACCOUNT_JSON` secret in Firebase

## How to Set Firebase Secrets

### Using Firebase CLI:
```bash
# Set the service account JSON
firebase functions:secrets:set GOOGLE_SERVICE_ACCOUNT_JSON

# When prompted, paste the entire JSON content

# Set spreadsheet IDs
firebase functions:secrets:set GOOGLE_SHEETS_REGISTRATIONS_ID
# Paste the spreadsheet ID when prompted

firebase functions:secrets:set GOOGLE_SHEETS_VOLUNTEERS_ID
# Paste the spreadsheet ID when prompted

firebase functions:secrets:set GOOGLE_SHEETS_VENDORS_ID
# Paste the spreadsheet ID when prompted
```

### Using Firebase Console:
1. Go to https://console.firebase.google.com
2. Select your project
3. Go to Functions > Secrets
4. Click "Add Secret"
5. Enter the secret name and value
6. Click "Save"

## Verification Checklist

Before syncing, verify:

- [ ] Service account JSON is configured in Firebase secrets
- [ ] All three spreadsheet IDs are configured in Firebase secrets
- [ ] Each Google Sheet exists and is accessible
- [ ] Service account email has Editor access to all sheets
- [ ] Firebase Functions are deployed with the latest code
- [ ] You're using the correct Firebase project

## Testing the Configuration

1. Open the admin dashboard
2. Go to Registrations, Volunteers, or Vendors section
3. Click "Sync to Sheets"
4. Check the browser console (F12 > Console) for detailed error logs
5. Check Firebase Functions logs for server-side errors:
   ```bash
   firebase functions:log
   ```

## Getting the Service Account Email

If you need to find your service account email:

1. **From the JSON file:**
   - Open your service account JSON
   - Look for the `client_email` field
   - Copy that email address

2. **From Google Cloud Console:**
   - Go to https://console.cloud.google.com
   - Go to IAM & Admin > Service Accounts
   - Find your service account in the list
   - The email is shown in the "Email" column

## Still Having Issues?

If you've verified all the above and still get errors:

1. Check Firebase Functions logs for detailed error messages
2. Verify the service account has the "Google Sheets API" enabled in Google Cloud Console
3. Try creating new spreadsheets and sharing them with the service account
4. Ensure your Firebase project is on a paid plan (Blaze) as Functions needs external API access

## Additional Resources

- [Google Sheets Setup Guide](./GOOGLE-SHEETS-SETUP.md)
- [Firebase Functions Documentation](https://firebase.google.com/docs/functions)
- [Google Cloud Service Accounts](https://cloud.google.com/iam/docs/service-accounts)
