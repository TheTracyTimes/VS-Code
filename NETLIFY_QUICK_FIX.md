# 🚀 Quick Fix for Netlify Deployment

Since your site is already connected to Netlify, you just need to:

## Step 1: Verify Environment Variables (CRITICAL)

Go to your Netlify dashboard:
1. **Site settings** → **Environment variables**
2. Check if these **17 variables** are set:

### Quick Checklist:
```
□ FIREBASE_API_KEY
□ FIREBASE_AUTH_DOMAIN
□ FIREBASE_PROJECT_ID
□ FIREBASE_STORAGE_BUCKET
□ FIREBASE_MESSAGING_SENDER_ID
□ FIREBASE_APP_ID
□ FIREBASE_MEASUREMENT_ID

□ EMAILJS_SERVICE_ID
□ EMAILJS_PUBLIC_KEY
□ EMAILJS_TEMPLATE_REGISTRATION
□ EMAILJS_TEMPLATE_VENDOR
□ EMAILJS_TEMPLATE_VOLUNTEER

□ GOOGLE_SHEETS_API_KEY
□ GOOGLE_SHEETS_CLIENT_ID
□ GOOGLE_SHEETS_REGISTRATIONS_ID
□ GOOGLE_SHEETS_VOLUNTEERS_ID
□ GOOGLE_SHEETS_VENDORS_ID
```

### ⚠️ CRITICAL: Add These Template IDs

If the EmailJS template variables are missing or incorrect, add them:

```
EMAILJS_TEMPLATE_REGISTRATION = registration_confirmation
EMAILJS_TEMPLATE_VENDOR = vendor_confirmation
EMAILJS_TEMPLATE_VOLUNTEER = volunteer_confirmation
```

### ⚠️ CRITICAL: Add These Spreadsheet IDs

If the Google Sheets ID variables are missing or incorrect, add them:

```
GOOGLE_SHEETS_REGISTRATIONS_ID = 1q7vxkgof14p6OpHehTySIU6c0qNpbencA6E09agYJTg
GOOGLE_SHEETS_VOLUNTEERS_ID = 1T45QcAsY7m5SO8gSQKTvHI_PFFa4qx1x6dwW3iwG0s0
GOOGLE_SHEETS_VENDORS_ID = 1V6G2KN1vvTB5Ng249rg9K6ijbUT7tou_jaE9ygALxeM
```

## Step 2: Trigger Redeploy

After verifying/adding environment variables:

1. Go to **Deploys** tab in Netlify
2. Click **"Trigger deploy"** → **"Deploy site"**
3. Or click **"Retry deploy"** if the last deploy failed
4. Wait 1-2 minutes for build to complete

### Why Redeploy?

The latest commits include:
- ✅ EmailJS template IDs exported to window object
- ✅ Proper config file generation in build.sh
- ✅ All fixes for email notifications and Google Sheets sync

## Step 3: Check Build Log

While the build is running:
1. Click on the deploying build
2. Check the **Deploy log**
3. Look for:
   ```
   Config files generated successfully!
     - public/config/firebase-config.js
     - public/config/google-sheets-config.js
   ```
4. Make sure there are no errors

### Common Build Errors:

**"bash: command not found"**
- Should not happen, but if it does, check netlify.toml exists

**"Environment variable not set"**
- Missing environment variables in Netlify settings
- Go back to Step 1

## Step 4: Test After Deployment

Once deployed, visit your site and test:

### Quick Test:
1. Open browser console (F12)
2. Go to one of the forms
3. Check for these console messages:
   ```
   Firebase initialized successfully
   EmailJS initialized
   Google API Client initialized successfully
   ```

### Full Test:
1. Submit a test form (use your own email)
2. Check:
   - [ ] Form submits without errors
   - [ ] You receive confirmation email
   - [ ] Data appears in Firebase Firestore
   - [ ] Data appears in Google Sheet

## Troubleshooting

### "Firebase initialization error"
**Fix:** Check Firebase environment variables in Netlify
- Make sure all 7 Firebase variables are set correctly

### "EmailJS not defined" or emails not sending
**Fix:** Check EmailJS environment variables
- Make sure `EMAILJS_SERVICE_ID` and `EMAILJS_PUBLIC_KEY` are set
- Make sure template IDs are set:
  - `EMAILJS_TEMPLATE_REGISTRATION=registration_confirmation`
  - `EMAILJS_TEMPLATE_VENDOR=vendor_confirmation`
  - `EMAILJS_TEMPLATE_VOLUNTEER=volunteer_confirmation`

### "Google Sheets not syncing"
**Fix:** Check Google Sheets environment variables
- Make sure `GOOGLE_SHEETS_API_KEY` and `GOOGLE_SHEETS_CLIENT_ID` are set
- Make sure all 3 spreadsheet ID variables are set with the IDs above

### Build succeeds but forms don't work
**Check:**
1. Open deployed site's console (F12)
2. Look for JavaScript errors
3. Check if config files were generated:
   - Visit `https://your-site.netlify.app/config/firebase-config.js`
   - Should show Firebase config (not a 404 error)

## What Was Fixed in Latest Commits

The code on branch `claude/analyze-photos-design-CqXcK` now includes:

1. **EmailJS Template IDs** - Added to build.sh and exported to window
2. **Google Sheets IDs** - Properly configured in build process
3. **Config Generation** - build.sh properly generates all needed files
4. **Security** - Proper credential handling

## Quick Reference: Where to Find Your Values

To see your current environment variable values:
```bash
cat .env
```

Then copy each value to Netlify's environment variables section.

## Need Help?

If issues persist:
1. Share the Netlify deploy log
2. Share browser console errors
3. Contact: sarasotagospel@gmail.com or 941-800-5211

## Summary

**Most likely issue:** Missing environment variables in Netlify

**Quick fix:**
1. Add the 17 environment variables to Netlify
2. Make sure template IDs and spreadsheet IDs are exactly as shown above
3. Trigger a new deploy
4. Test forms

That's it! 🎉
