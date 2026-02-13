# Google Sheets Security Setup Checklist

## Overview
This checklist guides you through securing your Google Sheets API integration. **You must complete ALL steps** to ensure security.

---

## Prerequisites
- [ ] Google Cloud Console access
- [ ] Project: Your project with the API key and OAuth client
- [ ] Your website domain (e.g., `sarasotagospeltemple.com`)

---

## Step 1: Restrict API Key (CRITICAL)

### 1.1 Navigate to API Key
- [ ] Go to [Google Cloud Console](https://console.cloud.google.com)
- [ ] Select your project
- [ ] Click **APIs & Services** → **Credentials**
- [ ] Find API key: `AIzaSyBuGOqgq-M6Q9bNeW29xihdRqGHDWbiEew`
- [ ] Click on the API key name to edit

### 1.2 Set Application Restrictions
- [ ] Under **Application restrictions**, select **HTTP referrers (websites)**
- [ ] Click **Add an item** and add your domains:
  ```
  https://yourdomain.com/*
  https://*.yourdomain.com/*
  http://localhost:*
  http://127.0.0.1:*
  ```
  Replace `yourdomain.com` with your actual domain

### 1.3 Set API Restrictions
- [ ] Under **API restrictions**, select **Restrict key**
- [ ] Click **Select APIs**
- [ ] Check ONLY: **Google Sheets API**
- [ ] Uncheck all other APIs
- [ ] Click **OK**

### 1.4 Save Changes
- [ ] Click **Save** at the bottom
- [ ] Wait for "Credentials saved" confirmation

**✅ Verification**: Try accessing the API from a different domain - it should fail with 403 error.

---

## Step 2: Configure OAuth 2.0 Client ID

### 2.1 Navigate to OAuth Client
- [ ] In **APIs & Services** → **Credentials**
- [ ] Find OAuth 2.0 Client ID: `506893960681-9nb4cq1jkgg7d5bvuf527ah0sh93j5ad.apps.googleusercontent.com`
- [ ] Click on the client ID name to edit

### 2.2 Add Authorized JavaScript Origins
- [ ] Under **Authorized JavaScript origins**, add:
  ```
  https://yourdomain.com
  https://www.yourdomain.com
  http://localhost
  http://127.0.0.1
  ```
  Replace `yourdomain.com` with your actual domain

### 2.3 Add Authorized Redirect URIs
- [ ] Under **Authorized redirect URIs**, add:
  ```
  https://yourdomain.com
  https://www.yourdomain.com
  http://localhost
  http://127.0.0.1
  ```
  Replace `yourdomain.com` with your actual domain

### 2.4 Save Changes
- [ ] Click **Save**
- [ ] Wait for confirmation

**✅ Verification**: OAuth should only work from your authorized domains.

---

## Step 3: Configure OAuth Consent Screen

### 3.1 Navigate to Consent Screen
- [ ] Go to **APIs & Services** → **OAuth consent screen**
- [ ] If not already configured, select **External** user type
- [ ] Click **Create** or **Edit**

### 3.2 App Information
- [ ] **App name**: `Sarasota Gospel Temple Admin Dashboard` (or your choice)
- [ ] **User support email**: Your admin email
- [ ] **App logo**: Upload your church logo (optional)
- [ ] **Application home page**: Your website URL
- [ ] **Application privacy policy link**: Your privacy policy URL
- [ ] **Authorized domains**: Add your domain (e.g., `yourdomain.com`)
- [ ] **Developer contact information**: Your email

### 3.3 Scopes
- [ ] Click **Add or Remove Scopes**
- [ ] Find and select: `https://www.googleapis.com/auth/spreadsheets`
  - Scope description: "See, edit, create, and delete all your Google Sheets spreadsheets"
- [ ] Click **Update**
- [ ] Click **Save and Continue**

### 3.4 Test Users (if app not published)
If your app is in "Testing" mode:
- [ ] Click **Add Users**
- [ ] Add email addresses of admin users who will sync data:
  ```
  admin1@example.com
  admin2@example.com
  ```
- [ ] Click **Save and Continue**

### 3.5 Summary
- [ ] Review all settings
- [ ] Click **Back to Dashboard**

**✅ Verification**: Check that your app shows "Testing" or "Published" status.

---

## Step 4: Share Google Sheets with Admin Users

For each spreadsheet, you need to grant access to admin users.

### 4.1 Registrations Sheet
- [ ] Open [Registrations Sheet](https://docs.google.com/spreadsheets/d/1q7vxkgof14p6OpHehTySIU6c0qNpbencA6E09agYJTg/edit)
- [ ] Click **Share** button (top right)
- [ ] Add admin email addresses
- [ ] Set permission to **Editor**
- [ ] Uncheck "Notify people"
- [ ] Click **Share**

### 4.2 Volunteers Sheet
- [ ] Open [Volunteers Sheet](https://docs.google.com/spreadsheets/d/1T45QcAsY7m5SO8gSQKTvHI_PFFa4qx1x6dwW3iwG0s0/edit)
- [ ] Click **Share** button
- [ ] Add admin email addresses
- [ ] Set permission to **Editor**
- [ ] Click **Share**

### 4.3 Vendors Sheet
- [ ] Open [Vendors Sheet](https://docs.google.com/spreadsheets/d/1V6G2KN1vvTB5Ng249rg9K6ijbUT7tou_jaE9ygALxeM/edit)
- [ ] Click **Share** button
- [ ] Add admin email addresses
- [ ] Set permission to **Editor**
- [ ] Click **Share**

**✅ Verification**: Admin users should receive email notifications (if enabled) or can access sheets directly.

---

## Step 5: Test the Implementation

### 5.1 Test API Key Restrictions
- [ ] Open your admin dashboard
- [ ] Open browser console (F12)
- [ ] Look for: `✅ Google API Client initialized with API key`
- [ ] Look for: `✅ Google Identity Services initialized`
- [ ] Look for: `✅ Google Sheets API ready`

**If you see errors**:
- Check that your domain is in authorized referrers
- Check that Google Sheets API is enabled
- Wait 5-10 minutes for changes to propagate

### 5.2 Test OAuth Flow
- [ ] Sign in to admin dashboard
- [ ] Click **📊 Sync to Google Sheets** button
- [ ] Google sign-in popup should appear
- [ ] Sign in with an admin Google account
- [ ] Grant permission when prompted
- [ ] Check console for: `✅ OAuth token received`

**If OAuth fails**:
- Verify admin email is in test users (if app in testing mode)
- Check JavaScript origins include your domain
- Check redirect URIs include your domain

### 5.3 Test Sync Functionality
- [ ] After OAuth authentication, sync should proceed
- [ ] Check console for: `🔄 Syncing X records to Google Sheets...`
- [ ] Check console for: `✅ Successfully synced X records to Google Sheets`
- [ ] Open the Google Sheet and verify data appears

**If sync fails**:
- Check that admin has Editor access to spreadsheet
- Verify spreadsheet IDs are correct in config
- Check browser console for specific error messages

### 5.4 Test from Different Domain (Security Check)
- [ ] Try accessing your site from a different domain or IP
- [ ] API calls should fail with 403 errors
- [ ] This confirms restrictions are working

---

## Step 6: Enable HTTPS (Production)

For production deployment, you MUST use HTTPS:

### 6.1 SSL Certificate
- [ ] Obtain SSL certificate (Let's Encrypt, Cloudflare, etc.)
- [ ] Install certificate on your web server
- [ ] Configure automatic HTTP to HTTPS redirect

### 6.2 Update OAuth Settings
- [ ] Remove `http://localhost` from authorized origins
- [ ] Remove `http://127.0.0.1` from authorized origins
- [ ] Keep only HTTPS URLs

### 6.3 Update API Key Restrictions
- [ ] Remove `http://localhost:*` from referrers
- [ ] Remove `http://127.0.0.1:*` from referrers
- [ ] Keep only HTTPS URLs

**✅ Verification**: All API calls should work over HTTPS only.

---

## Step 7: Monitor and Maintain

### 7.1 Set Up Monitoring
- [ ] Go to **APIs & Services** → **Dashboard**
- [ ] Monitor Google Sheets API usage
- [ ] Set up quota alerts (optional)

### 7.2 Review Access Regularly
- [ ] Periodically review test users list
- [ ] Remove users who no longer need access
- [ ] Update spreadsheet sharing as needed

### 7.3 Check for Unusual Activity
- [ ] Monitor API usage for spikes
- [ ] Review OAuth grants periodically
- [ ] Update restrictions if domain changes

---

## Troubleshooting

### "API key not valid" Error
**Cause**: API key restrictions are too strict or not propagated yet

**Fix**:
- [ ] Wait 5-10 minutes for changes to propagate
- [ ] Check domain is correctly added to HTTP referrers
- [ ] Verify wildcard patterns include `/*` suffix
- [ ] Check Google Sheets API is enabled for the key

### "Origin not allowed by Access-Control-Allow-Origin"
**Cause**: Domain not in authorized JavaScript origins

**Fix**:
- [ ] Add your domain to authorized JavaScript origins
- [ ] Include both `https://domain.com` and `https://www.domain.com`
- [ ] Wait 5-10 minutes for changes to propagate

### "Access blocked: This app's request is invalid"
**Cause**: Redirect URI mismatch

**Fix**:
- [ ] Ensure redirect URIs match JavaScript origins
- [ ] Include the exact URL where OAuth callback happens
- [ ] Remove any trailing slashes

### "Permission denied" during sync
**Cause**: User doesn't have edit access to spreadsheet

**Fix**:
- [ ] Share spreadsheet with user's Google account
- [ ] Set permission to **Editor** (not Viewer)
- [ ] User must sign in with the same account that has access

### "This app is blocked" message
**Cause**: App not verified or user not in test users

**Fix**:
- [ ] Add user to test users list in OAuth consent screen
- [ ] Or publish your app (requires verification for production)

---

## Security Best Practices

- [ ] **Never** remove API restrictions - always keep APIs limited
- [ ] **Never** make API key unrestricted - always use HTTP referrer restrictions
- [ ] **Never** commit API keys to Git (already handled via `.gitignore`)
- [ ] **Always** use HTTPS in production
- [ ] **Regularly** review and update test users list
- [ ] **Monitor** API usage for unusual activity
- [ ] **Limit** spreadsheet access to only necessary users
- [ ] **Use** Firebase Authentication for admin dashboard access

---

## Completion Checklist

Before going live, ensure ALL items are checked:

- [ ] API key has HTTP referrer restrictions
- [ ] API key is limited to Google Sheets API only
- [ ] OAuth client has authorized JavaScript origins
- [ ] OAuth client has authorized redirect URIs
- [ ] OAuth consent screen is configured
- [ ] Test users are added (if in testing mode)
- [ ] All spreadsheets shared with admin users
- [ ] Tested OAuth flow successfully
- [ ] Tested sync functionality successfully
- [ ] HTTPS is enabled for production
- [ ] HTTP URLs removed from production config
- [ ] API usage monitoring is set up

---

## Need Help?

If you encounter issues:
1. Check the [detailed setup guide](./GOOGLE_SHEETS_SECURITY_SETUP.md)
2. Review the troubleshooting section above
3. Check browser console for specific error messages
4. Review Google Cloud Console audit logs

---

**Status**: 🔴 NOT SECURE until all items above are completed

**Once completed**: 🟢 SECURE - Ready for production use
