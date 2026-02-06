# Google Sheets Integration Setup Guide

This guide will help you set up automatic syncing of form submissions to Google Sheets, similar to how Google Forms works.

## Overview

Once configured, your Firebase form data will automatically sync to Google Sheets:
- **Automatic Sync**: New form submissions are automatically added to Google Sheets
- **Manual Sync**: Admin dashboard includes "Sync to Google Sheets" buttons to sync all existing data
- **Three Separate Sheets**: One for registrations, one for volunteers, and one for vendors

## Prerequisites

- A Google account
- Admin access to your website
- The three forms (registration, volunteer, vendor) already working with Firebase

## Step 1: Create Google Spreadsheets

1. Go to [Google Sheets](https://sheets.google.com)
2. Create THREE new spreadsheets:
   - "2026 Meeting - Registrations"
   - "2026 Meeting - Volunteers"
   - "2026 Meeting - Vendors"

3. For each spreadsheet, note the **Spreadsheet ID** from the URL:
   ```
   https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit
   ```
   Example: `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`

4. Keep these IDs handy - you'll need them later.

## Step 2: Set Up Google Cloud Project

### 2.1 Create a Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click the project dropdown at the top
3. Click "New Project"
4. Name it "Sarasota Gospel Temple Forms" (or similar)
5. Click "Create"
6. Wait for the project to be created, then select it

### 2.2 Enable Google Sheets API

1. In the left sidebar, go to **APIs & Services** → **Library**
2. Search for "Google Sheets API"
3. Click on "Google Sheets API"
4. Click **ENABLE**

### 2.3 Configure OAuth Consent Screen

1. In the left sidebar, go to **APIs & Services** → **OAuth consent screen**
2. Select **External** as the user type
3. Click **CREATE**
4. Fill in the required fields:
   - **App name**: Sarasota Gospel Temple Forms
   - **User support email**: Your email address
   - **Developer contact**: Your email address
5. Click **SAVE AND CONTINUE**
6. On the "Scopes" page, click **ADD OR REMOVE SCOPES**
7. Filter for "Google Sheets API"
8. Check the box for: `https://www.googleapis.com/auth/spreadsheets`
9. Click **UPDATE** then **SAVE AND CONTINUE**
10. On "Test users" page, click **SAVE AND CONTINUE**
11. Review and click **BACK TO DASHBOARD**

### 2.4 Create API Credentials

#### Create API Key (for read access)

1. Go to **APIs & Services** → **Credentials**
2. Click **CREATE CREDENTIALS** → **API key**
3. Copy the API key that appears
4. Click **RESTRICT KEY** (recommended)
5. Under "API restrictions":
   - Select "Restrict key"
   - Check only "Google Sheets API"
6. Click **SAVE**
7. **Keep this API key safe** - you'll need it for configuration

#### Create OAuth 2.0 Client ID (for write access)

1. Still in **Credentials**, click **CREATE CREDENTIALS** → **OAuth client ID**
2. Select **Web application** as the application type
3. Give it a name: "Forms Web Client"
4. Under **Authorized JavaScript origins**, add:
   - `http://localhost` (for testing)
   - `http://localhost:8000` (for testing)
   - `http://localhost:3000` (for testing)
   - `https://your-actual-domain.com` (your production domain)
   - `https://www.your-actual-domain.com` (with www)
5. Under **Authorized redirect URIs**, add the same URLs as above
6. Click **CREATE**
7. Copy the **Client ID** (it will look like: `123456789-abc123.apps.googleusercontent.com`)
8. **Keep this Client ID safe** - you'll need it for configuration

## Step 3: Configure the Integration

1. Open the file `/config/google-sheets-config.js` in your website code

2. Replace the placeholder values:

```javascript
const GOOGLE_SHEETS_CONFIG = {
    // Replace with your API Key from Step 2.4
    apiKey: 'YOUR_GOOGLE_API_KEY',

    // Replace with your Client ID from Step 2.4
    clientId: 'YOUR_CLIENT_ID.apps.googleusercontent.com',

    // Replace with your Spreadsheet IDs from Step 1
    spreadsheetIds: {
        registrations: 'YOUR_REGISTRATIONS_SPREADSHEET_ID',
        volunteers: 'YOUR_VOLUNTEERS_SPREADSHEET_ID',
        vendors: 'YOUR_VENDORS_SPREADSHEET_ID'
    },

    // ... rest of the config (don't change)
};
```

3. Save the file

## Step 4: Configure Spreadsheet Permissions

For each of your three spreadsheets:

1. Open the spreadsheet in Google Sheets
2. Click the **Share** button (top right)
3. Under "General access", change to:
   - **Anyone with the link** → **Editor**
   OR
   - Add specific email addresses that should have access
4. Click **Done**

**Security Note**: The spreadsheets will only be writable when an admin authenticates through the admin dashboard. Public form submissions use a secure API that only adds rows, not reads or modifies existing data.

## Step 5: Test the Integration

### Test Automatic Sync (Form Submission)

1. Open one of your forms (e.g., registration form)
2. Fill out and submit the form
3. Check the corresponding Google Sheet
4. You should see a new row added with the form data

**Note**: If the automatic sync fails, the form submission will still succeed and be saved to Firebase. The sync is non-blocking.

### Test Manual Sync (Admin Dashboard)

1. Log into your admin dashboard
2. Click one of the "📊 Sync to Google Sheets" buttons
3. You'll be prompted to authenticate with Google (first time only)
4. Select your Google account and grant permissions
5. The existing Firebase data will be synced to the Google Sheet

## Step 6: Deploy to Production

When deploying to your production website:

1. Make sure you added your production domain to the **Authorized JavaScript origins** in Step 2.4
2. Update the OAuth consent screen if needed
3. Test the integration on the live site

## How It Works

### Automatic Sync (Form Submissions)

```
User fills out form → Submits form → Data saved to Firebase → Data synced to Google Sheets
```

- Happens automatically on every form submission
- Non-blocking: Form submission succeeds even if Sheets sync fails
- No authentication required (uses API key)

### Manual Sync (Admin Dashboard)

```
Admin clicks sync button → Authenticates with Google → All Firebase data synced to Sheet
```

- Syncs ALL existing data from Firebase
- Requires admin to authenticate with Google (one-time)
- Useful for bulk updates or recovering from sync failures

### Data Structure

Each spreadsheet will have:
- **Header row** (automatically created): Column names
- **Data rows**: One row per form submission
- **Formatting**: Headers are bold with gray background, frozen

## Troubleshooting

### "Google Sheets is not configured yet" error

- Check that you've replaced all placeholder values in `google-sheets-config.js`
- Make sure the file is saved and uploaded to your server

### "Authentication failed" error

- Verify your Client ID is correct in `google-sheets-config.js`
- Check that your domain is added to Authorized JavaScript origins
- Try clearing browser cache and cookies

### "Permission denied" error

- Check spreadsheet sharing settings (Step 4)
- Verify the Spreadsheet IDs are correct
- Make sure Google Sheets API is enabled in Google Cloud Console

### Rows not appearing in spreadsheet

- Check browser console for errors (F12 → Console tab)
- Verify the Spreadsheet ID is correct
- Make sure the spreadsheet isn't deleted or moved
- Check that the spreadsheet is shared correctly

### API quota exceeded

Google Sheets API has usage limits:
- **Read requests**: 300 per minute per project
- **Write requests**: 300 per minute per project

If you hit these limits:
- Wait a few minutes and try again
- Consider batching updates instead of real-time sync
- Request a quota increase from Google Cloud Console

## Security Best Practices

1. **Keep credentials private**: Never commit `google-sheets-config.js` with real credentials to public repositories
2. **Use environment variables**: For production, consider storing credentials in environment variables
3. **Restrict API key**: Always restrict your API key to only Google Sheets API
4. **Monitor usage**: Regularly check Google Cloud Console for unusual API usage
5. **Limit spreadsheet access**: Only share spreadsheets with people who need access

## Getting Help

If you encounter issues:

1. Check the browser console for error messages (F12 → Console)
2. Review the [Google Sheets API documentation](https://developers.google.com/sheets/api)
3. Check the [OAuth 2.0 documentation](https://developers.google.com/identity/protocols/oauth2)
4. Contact your web developer with specific error messages

## Additional Features

### Viewing Real-Time Updates

- Open the Google Sheet in your browser
- New submissions will appear automatically (you may need to refresh)
- Multiple people can view the same sheet simultaneously

### Exporting Data

From Google Sheets, you can:
- Download as Excel (.xlsx)
- Download as CSV
- Download as PDF
- Copy data to other spreadsheets

### Creating Charts and Pivot Tables

Google Sheets allows you to:
- Create charts from your data
- Build pivot tables for analysis
- Use formulas to calculate statistics
- Share visualizations with your team

## Next Steps

Once configured, your Google Sheets will:
- ✅ Automatically receive new form submissions
- ✅ Allow manual bulk syncing from admin dashboard
- ✅ Provide easy data export and sharing
- ✅ Enable collaborative data analysis
- ✅ Work just like Google Forms!

---

**Questions?** Refer to the Firebase and EmailJS setup guides for related configuration:
- `FIREBASE-EMAILJS-SETUP.md` - Firebase and email configuration
- `FORMS_OVERVIEW.md` - Form structure and functionality
