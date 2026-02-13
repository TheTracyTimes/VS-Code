# Google Sheets Security Setup Guide

## Overview

This guide explains how to securely configure client-side Google Sheets integration using API Key and OAuth 2.0 Client ID.

## Security Architecture

### Client-Side Approach (Current Implementation)
- **API Key**: Used to identify your application and restrict API access
- **OAuth 2.0**: Users authenticate with their own Google account
- **Authorization**: Users only access sheets they have permission to edit

### Why This is Secure

1. **API Key Restrictions**: The key is restricted to your domain and specific APIs
2. **User Authentication**: Each user must sign in with their Google account
3. **Google's Authorization**: Users explicitly grant permission to access sheets
4. **No Credential Exposure**: No service account credentials in client code
5. **Granular Access Control**: Users only access sheets shared with them

## Required Security Configuration

### 1. Restrict Your API Key

**CRITICAL**: Your API key is visible in client-side code. You MUST restrict it.

#### Steps to Restrict API Key:

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project
3. Navigate to **APIs & Services** → **Credentials**
4. Find your API key: `AIzaSyBuGOqgq-M6Q9bNeW29xihdRqGHDWbiEew`
5. Click on the API key to edit it

#### Apply These Restrictions:

**A. Application Restrictions** (Choose ONE):
- **HTTP referrers (websites)** - RECOMMENDED
  - Add your website URLs:
    ```
    https://yourdomain.com/*
    https://www.yourdomain.com/*
    http://localhost:* (for testing only)
    ```

**B. API Restrictions**:
- Select "Restrict key"
- Enable ONLY these APIs:
  - ✅ Google Sheets API
  - ❌ Disable all others

6. Click **Save**

### 2. Configure OAuth 2.0 Client ID

Your OAuth Client ID is already configured: `506893960681-9nb4cq1jkgg7d5bvuf527ah0sh93j5ad.apps.googleusercontent.com`

#### Verify OAuth Settings:

1. Go to **APIs & Services** → **Credentials**
2. Find your OAuth 2.0 Client ID
3. Click to edit

#### Required Settings:

**A. Authorized JavaScript origins**:
```
https://yourdomain.com
https://www.yourdomain.com
http://localhost (for testing)
```

**B. Authorized redirect URIs**:
```
https://yourdomain.com
https://www.yourdomain.com
http://localhost (for testing)
```

4. Click **Save**

### 3. Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Configure the following:

**App Information**:
- App name: `Sarasota Gospel Temple Admin`
- User support email: Your admin email
- App logo: (Optional)

**Scopes**:
- Click "Add or Remove Scopes"
- Add: `https://www.googleapis.com/auth/spreadsheets`
- This allows editing Google Sheets

**Test Users** (if app is not published):
- Add email addresses of admin users who will sync data

3. Click **Save and Continue**

### 4. Share Google Sheets with Admin Users

For each spreadsheet (Registrations, Volunteers, Vendors):

1. Open the Google Sheet
2. Click **Share**
3. Add the email addresses of admin users
4. Set permission to **Editor**
5. Click **Send**

## How Authentication Works

### For Admin Users (Dashboard):

1. Admin clicks "📊 Sync to Google Sheets"
2. Google OAuth popup appears
3. Admin signs in with their Google account
4. Admin grants permission to access sheets
5. Data is synced directly to Google Sheets
6. Admin can revoke access anytime

### For Form Submissions:

- Form submissions save to Firebase (works without Google auth)
- Google Sheets sync happens only when admin manually syncs
- This is MORE secure than auto-sync with service accounts

## Security Best Practices

### ✅ DO:

1. **Keep API key restricted** to your domain and Google Sheets API only
2. **Use HTTPS** for your website (required for OAuth)
3. **Limit admin access** to trusted users only
4. **Review OAuth consent** screen regularly
5. **Monitor API usage** in Google Cloud Console
6. **Use Firebase Authentication** for admin dashboard access

### ❌ DON'T:

1. **Never remove API restrictions** - this would allow anyone to use your key
2. **Don't add unnecessary scopes** - only use Sheets API
3. **Don't share admin credentials** - each admin should have their own Google account
4. **Don't commit service account keys** to Git (not applicable here)

## Testing Your Security

### Verify API Key Restrictions:

1. Try using the API key from a different domain
2. It should fail with a 403 error
3. This confirms domain restrictions are working

### Verify OAuth Flow:

1. Open dashboard as admin
2. Click "Sync to Google Sheets"
3. You should see Google sign-in popup
4. After signing in, sync should work
5. If not signed in, sync should fail gracefully

### Verify Permissions:

1. Try syncing with a user who doesn't have sheet access
2. It should fail with "Permission denied" error
3. This confirms authorization is working

## Monitoring

### Check API Usage:

1. Go to **APIs & Services** → **Dashboard**
2. View Google Sheets API usage
3. Monitor for unusual activity

### Check OAuth Activity:

1. Users can view connected apps at: https://myaccount.google.com/permissions
2. Users can revoke access anytime
3. You can see OAuth grants in Cloud Console

## Troubleshooting

### "API key not valid" Error:
- Check API key restrictions in Cloud Console
- Ensure your domain is in allowed HTTP referrers
- Verify Google Sheets API is enabled

### "Permission denied" Error:
- Ensure user has Editor access to the spreadsheet
- Check OAuth scope includes spreadsheets
- Verify user has granted permission

### "Origin not allowed" Error:
- Add your domain to Authorized JavaScript origins
- Include both http://localhost and https://yourdomain.com

## Summary

This client-side implementation is secure when properly configured because:

1. ✅ API key is restricted to your domain and specific API
2. ✅ Users authenticate with their own Google accounts
3. ✅ Users only access sheets they're granted permission to
4. ✅ No service account credentials in client code
5. ✅ Google handles all authentication and authorization
6. ✅ Users can revoke access anytime

**Next Steps:**
1. Apply API key restrictions in Google Cloud Console
2. Verify OAuth Client ID settings
3. Share sheets with admin users
4. Test the sync functionality
5. Monitor API usage regularly
