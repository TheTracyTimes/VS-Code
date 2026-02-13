# Quick Security Setup (5 Minutes)

## ⚠️ CRITICAL - Do This NOW Before Testing

Your API integration **is NOT secure** until you complete these steps.

---

## Step 1: Restrict API Key (2 minutes)

1. Go to: https://console.cloud.google.com/apis/credentials
2. Click on API key: `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXX` (your actual API key)
3. Under **Application restrictions**:
   - Select: `HTTP referrers (websites)`
   - Add your domain: `https://yourdomain.com/*`
   - Add for testing: `http://localhost:*`
4. Under **API restrictions**:
   - Select: `Restrict key`
   - Enable ONLY: `Google Sheets API`
5. Click **Save**

---

## Step 2: Configure OAuth Client (2 minutes)

1. In the same Credentials page
2. Click on OAuth 2.0 Client: `506893960681-9nb4cq1jkgg7d5bvuf527ah0sh93j5ad`
3. Under **Authorized JavaScript origins**, add:
   ```
   https://yourdomain.com
   http://localhost
   ```
4. Under **Authorized redirect URIs**, add the same URLs
5. Click **Save**

---

## Step 3: Share Spreadsheets (1 minute)

Share each sheet with admin Google accounts (Editor access):

1. [Registrations](https://docs.google.com/spreadsheets/d/1q7vxkgof14p6OpHehTySIU6c0qNpbencA6E09agYJTg/edit) → Share → Add admin emails
2. [Volunteers](https://docs.google.com/spreadsheets/d/1T45QcAsY7m5SO8gSQKTvHI_PFFa4qx1x6dwW3iwG0s0/edit) → Share → Add admin emails
3. [Vendors](https://docs.google.com/spreadsheets/d/1V6G2KN1vvTB5Ng249rg9K6ijbUT7tou_jaE9ygALxeM/edit) → Share → Add admin emails

---

## Test It

1. Open your admin dashboard
2. Click "📊 Sync to Google Sheets"
3. Sign in with Google
4. Verify data syncs successfully

---

## What This Does

✅ **API Key**: Only works from your website
✅ **OAuth**: Only admins with sheet access can sync
✅ **Secure**: No one can abuse your API key from other sites

---

## Full Details

See: [SECURITY_SETUP_CHECKLIST.md](./SECURITY_SETUP_CHECKLIST.md) for complete guide

---

**Replace `yourdomain.com` with your actual domain!**
