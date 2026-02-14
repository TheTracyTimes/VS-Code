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
- ✅ Admin access to your website files
- ✅ The three forms (registration, volunteer, vendor) already working

---

## Manual Setup Steps

### 1️⃣ Create or Select Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click the project dropdown at the top
3. Either:
   - Select an existing project, OR
   - Click **New Project** and create one (e.g., "Sarasota Gospel Temple Forms")
4. Make note of your project name

### 2️⃣ Enable Google Sheets API

1. In Google Cloud Console, go to **APIs & Services → Library**
2. Search for **"Google Sheets API"**
3. Click **Enable**

### 3️⃣ Configure OAuth Consent Screen

1. In the left sidebar, go to **APIs & Services → OAuth consent screen**
2. Select **External** as the user type
3. Click **CREATE**
4. Fill in the required fields:
   - **App name**: Sarasota Gospel Temple Forms (or your preferred name)
   - **User support email**: Your email address
   - **Developer contact**: Your email address
5. Click **SAVE AND CONTINUE**
6. On the "Scopes" page, click **ADD OR REMOVE SCOPES**
7. Search for "Google Sheets API"
8. Check the box for: `https://www.googleapis.com/auth/spreadsheets`
9. Click **UPDATE** then **SAVE AND CONTINUE**
10. On "Test users" page, click **SAVE AND CONTINUE**
11. Review and click **BACK TO DASHBOARD**

### 4️⃣ Create API Credentials

#### Create API Key (for read access)

1. Go to **APIs & Services → Credentials**
2. Click **CREATE CREDENTIALS** → **API key**
3. Copy the API key that appears
4. Click **RESTRICT KEY** (recommended)
5. Under "API restrictions":
   - Select "Restrict key"
   - Check only "Google Sheets API"
6. Under "Application restrictions":
   - Select "HTTP referrers (web sites)"
   - Add your domain (e.g., `https://yourdomain.com/*`)
7. Click **SAVE**
8. **Keep this API key safe** - you'll need it for Step 6

#### Create OAuth 2.0 Client ID (for write access)

1. Still in **Credentials**, click **CREATE CREDENTIALS** → **OAuth client ID**
2. Select **Web application** as the application type
3. Give it a name: "Forms Web Client"
4. Under **Authorized JavaScript origins**, add:
   - `http://localhost` (for testing)
   - `http://localhost:8000` (for testing)
   - `https://yourdomain.com` (your actual production domain)
   - `https://www.yourdomain.com` (with www)
5. Click **CREATE**
6. Copy the **Client ID** (looks like: `123456789-abc123.apps.googleusercontent.com`)
7. **Keep this Client ID safe** - you'll need it for Step 6

### 5️⃣ Create Google Sheets

1. Go to [Google Sheets](https://sheets.google.com)
2. Create THREE new spreadsheets:
   - "2026 Meeting - Registrations"
   - "2026 Meeting - Volunteers"
   - "2026 Meeting - Vendors"

3. For each spreadsheet, add the appropriate headers:

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

4. For **each spreadsheet**, click the **Share** button and configure:
   - Under "General access", you can either:
     - Set to **Anyone with the link** → **Viewer** (public read access)
     - OR keep as **Restricted** and share with specific email addresses
   - The admin who uses the sync feature will authenticate via OAuth
5. Note the **Spreadsheet ID** from each URL:

```
https://docs.google.com/spreadsheets/d/1q7vxkgof14p6OpHehTySIU6c0qNpbencA6E09agYJTg/edit
                                      ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
                                      This is the Spreadsheet ID
```

**Keep these IDs safe** - you'll need:
- Registrations Spreadsheet ID
- Volunteers Spreadsheet ID
- Vendors Spreadsheet ID

### 6️⃣ Configure Google Sheets API (OAuth Method)

**This project uses Google Sheets API with OAuth authentication (client-side), NOT Firebase Functions.**

1. Open the file `config/google-sheets-config.js` in your website code

2. Replace the placeholder values with your actual credentials:

```javascript
const GOOGLE_SHEETS_CONFIG = {
    // Replace with your API Key from Step 2
    apiKey: 'YOUR_GOOGLE_API_KEY',

    // Replace with your Client ID from Step 2
    clientId: 'YOUR_CLIENT_ID.apps.googleusercontent.com',

    // Replace with your Spreadsheet IDs from Step 5
    spreadsheetIds: {
        registrations: 'YOUR_REGISTRATIONS_SPREADSHEET_ID',
        volunteers: 'YOUR_VOLUNTEERS_SPREADSHEET_ID',
        vendors: 'YOUR_VENDORS_SPREADSHEET_ID'
    },

    // ... rest of the config (don't change)
};
```

3. Save the file

**Security Note**: The Google Sheets API key and OAuth Client ID are safe to expose in client-side code when properly restricted. Make sure to:
- Restrict your API key to your domain in Google Cloud Console
- Configure authorized domains for your OAuth Client ID

### 7️⃣ Deploy Your Website

Once configured, deploy your website:

**For Netlify:**
- See `NETLIFY_DEPLOYMENT.md` for deployment instructions
- Add your credentials as Netlify environment variables

**For other hosting:**
- Upload your files to your web server
- Ensure `config/google-sheets-config.js` has your credentials

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

### Error: "Google Sheets is not configured yet"

**Solution**: Check that you've replaced all placeholder values in `config/google-sheets-config.js` and the file is uploaded to your server.

### Error: "Authentication failed"

**Solutions**:
1. Verify your OAuth Client ID is correct in `config/google-sheets-config.js`
2. Check that your domain is added to Authorized JavaScript origins in Google Cloud Console
3. Try clearing browser cache and cookies
4. Make sure OAuth consent screen is configured

### Error: "Permission denied"

**Solutions**:
1. Check spreadsheet sharing settings - make sure your Google account has access
2. Verify the Spreadsheet IDs are correct in `config/google-sheets-config.js`
3. Make sure Google Sheets API is enabled in Google Cloud Console
4. Authenticate via the admin dashboard sync button (OAuth)

### Error: "API key invalid"

**Solutions**:
1. Verify your API key is correct in `config/google-sheets-config.js`
2. Check that the API key is restricted to Google Sheets API
3. Ensure your domain is added to the HTTP referrer restrictions

### Rows not appearing in spreadsheet

**Solutions**:
1. Check browser console for errors (F12 → Console tab)
2. Verify the Spreadsheet ID is correct
3. Make sure the spreadsheet isn't deleted or moved
4. Check that you've authenticated via OAuth (for manual sync)
5. Verify automatic sync is configured in the form submission code

### API quota exceeded

Google Sheets API has usage limits:
- **Read requests**: 300 per minute per project
- **Write requests**: 300 per minute per project

**Solutions**:
- Wait a few minutes and try again
- Consider batching updates
- Request a quota increase from Google Cloud Console

---

## How It Works

### Automatic Sync (Form Submissions)

```
User fills out form → Submits form → Data saved to Firebase → Data synced to Google Sheets via API
```

- Happens automatically on every form submission
- Uses Google Sheets API with your API key
- Non-blocking: Form submission succeeds even if Sheets sync fails

### Manual Sync (Admin Dashboard)

```
Admin clicks sync button → Authenticates with Google OAuth → All Firebase data synced to Sheet
```

- Syncs ALL existing data from Firebase
- Requires admin to authenticate with Google (one-time)
- Uses OAuth 2.0 for secure write access
- Useful for bulk updates or recovering from sync failures

### Security

✅ **API Key** is restricted to Google Sheets API and your domain
✅ **OAuth Client ID** only works with authorized redirect URIs
✅ **No private keys** in client-side code
✅ **Admin authentication** required for write access via OAuth
✅ **Spreadsheet permissions** control who can view/edit data

---

## Files Modified

- `config/google-sheets-config.js` - Google Sheets API configuration
- `public/js/google-sheets-service.js` - Frontend service for Google Sheets API
- `public/admin/dashboard.html` - Admin UI with sync buttons
- `.env` - Environment variables for development (contains your credentials)

---

## Maintenance

### Update Spreadsheet IDs

If you create new spreadsheets:

1. Update `config/google-sheets-config.js` with the new spreadsheet IDs
2. Redeploy your website or update Netlify environment variables

### Rotate API Credentials

If you need to rotate your API key or OAuth Client ID:

1. Create new credentials in Google Cloud Console
2. Update `config/google-sheets-config.js` with the new values
3. Delete the old credentials in Google Cloud Console
4. Redeploy your website

---

## Support

For issues, check:
- Browser console (F12) for JavaScript errors
- Google Cloud Console: [Error Reporting](https://console.cloud.google.com/errors)
- Google Cloud Console: [API Dashboard](https://console.cloud.google.com/apis/dashboard) for API usage

**Contact**:
- Email: sarasotagospel@gmail.com
- Phone: 941-800-5211

---

## Additional Resources

- [Google Sheets API Docs](https://developers.google.com/sheets/api)
- [OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Google API Client Library for JavaScript](https://github.com/google/google-api-javascript-client)
- [Netlify Deployment Guide](./NETLIFY_DEPLOYMENT.md) - For deploying your site
