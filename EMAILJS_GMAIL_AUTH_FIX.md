# Fix EmailJS Gmail Authentication Error (412)

## Problem
EmailJS is showing **412 errors** with the message:
```
Gmail_API: Request had insufficient authentication scopes.
```

This means the Gmail account connected to EmailJS doesn't have permission to send emails through the Gmail API.

---

## Root Cause

When you connect Gmail to EmailJS, you must grant it permission to "Send email on your behalf". If this permission wasn't granted during the initial setup, or if the token expired, EmailJS cannot send emails.

---

## Solution: Reconnect Gmail with Proper Permissions

### Step 1: Go to EmailJS Email Services

1. Log into your EmailJS dashboard: https://dashboard.emailjs.com/
2. Click on **"Email Services"** in the left sidebar
3. Find your Gmail service in the list

### Step 2: Disconnect the Gmail Account

1. Click on your Gmail service to open it
2. Look for a **"Disconnect"** or **"Remove"** button
3. Click it to disconnect the Gmail account
4. Confirm the disconnection

### Step 3: Reconnect Gmail with Full Permissions

1. Click **"Add New Service"** (or reconnect the existing one)
2. Select **"Gmail"**
3. Click **"Connect Account"**
4. You'll be redirected to Google's OAuth consent screen
5. **IMPORTANT:** Make sure to grant ALL requested permissions, especially:
   - ✅ **"Send email on your behalf"**
   - ✅ **"View your email address"**
   - ✅ **"See your personal info"**

### Step 4: Verify the Connection

1. After reconnecting, you should see a green checkmark or "Connected" status
2. Your Service ID should still be the same (e.g., `service_abc123`)
3. Make note of the Service ID - you'll need it for your configuration

### Step 5: Test Email Sending

1. In the EmailJS dashboard, go to your Gmail service
2. Look for a **"Send Test Email"** button
3. Send a test email to verify it works
4. Check your inbox to confirm the test email arrived

---

## Alternative: Use EmailJS's Built-in Email Service

If you continue having issues with Gmail, you can use EmailJS's built-in email service instead:

### Option A: Use EmailJS Email Service (Recommended for Simplicity)

1. In EmailJS dashboard, go to **"Email Services"**
2. Click **"Add New Service"**
3. Select **"EmailJS"** (their built-in service)
4. Configure the "From" email address (can be your Gmail)
5. Configure the "From" name
6. Save the service

**Advantages:**
- No OAuth issues
- Simpler setup
- Works immediately
- Still sends emails reliably

**Limitations:**
- Emails come from EmailJS servers (may go to spam more often)
- Free tier: 200 emails/month
- "From" address will show as `noreply@emailjs.com` with reply-to set to your email

### Option B: Use a Different Gmail Account

Sometimes the issue is with the specific Gmail account's security settings:

1. Create a new Gmail account specifically for EmailJS (e.g., `sarasotagospel.notifications@gmail.com`)
2. Connect this new account to EmailJS
3. During OAuth, grant all permissions
4. Update your EmailJS service to use this new account

---

## Common Issues and Solutions

### Issue 1: "This app isn't verified" Warning

When connecting Gmail, you might see a warning that says "This app isn't verified by Google":

1. Click **"Advanced"**
2. Click **"Go to EmailJS (unsafe)"**
3. This is safe - Google shows this for any third-party app using Gmail API
4. Grant the requested permissions

### Issue 2: Permissions Not Sticking

If you granted permissions but still see 412 errors:

1. Go to your Google Account settings: https://myaccount.google.com/permissions
2. Look for **"EmailJS"** in the list of connected apps
3. Click on it and **"Remove Access"**
4. Go back to EmailJS and reconnect from scratch
5. Make sure to grant all permissions this time

### Issue 3: Gmail Security Settings Blocking Access

Some Gmail accounts have strict security settings:

1. Go to your Gmail account settings: https://myaccount.google.com/security
2. Check if **"Less secure app access"** is turned OFF (this is outdated but might be an issue)
3. Check if **"2-Step Verification"** is enabled (might interfere with OAuth)
4. Try using an **App Password** instead (see below)

### Using App Passwords (Alternative Method)

If OAuth continues to fail, you can use an App Password:

**⚠️ NOTE:** This only works if you have 2-Step Verification enabled on your Gmail account.

1. Go to your Google Account: https://myaccount.google.com/
2. Click **"Security"** in the left sidebar
3. Under "Signing in to Google", click **"App passwords"**
4. Click **"Select app"** → Choose **"Mail"**
5. Click **"Select device"** → Choose **"Other"** and type "EmailJS"
6. Click **"Generate"**
7. Copy the 16-character password that appears
8. In EmailJS, instead of using OAuth, configure SMTP settings:
   - SMTP Server: `smtp.gmail.com`
   - Port: `587` (TLS) or `465` (SSL)
   - Username: Your full Gmail address
   - Password: The app password you just generated

---

## Verify Your EmailJS Configuration

After fixing the authentication issue, verify your environment variables are correct:

### In Your `.env` File

Make sure these values match your EmailJS dashboard:

```bash
# EmailJS Configuration
EMAILJS_SERVICE_ID=service_abc123xyz    # Your Gmail service ID
EMAILJS_PUBLIC_KEY=your_public_key_here
EMAILJS_TEMPLATE_REGISTRATION=registration_confirmatio
EMAILJS_TEMPLATE_VENDOR=vendor_confirmation
EMAILJS_TEMPLATE_VOLUNTEER=volunteer_confirmation
```

### Regenerate Config Files

After updating `.env`, run:

```bash
node setup-credentials.js
```

This will update `/config/firebase-config.js` with your EmailJS credentials.

---

## Test Your Forms

After fixing the Gmail authentication:

1. **Clear your browser cache** (important!)
2. Open your website
3. Submit a test registration form
4. Check:
   - ✅ Browser console shows no EmailJS errors
   - ✅ EmailJS dashboard "Logs" section shows successful send
   - ✅ Email arrives at `sarasotagospel@gmail.com`
   - ✅ No 412 errors in EmailJS logs

---

## Monitoring EmailJS Logs

To check if emails are sending successfully:

1. Go to EmailJS dashboard: https://dashboard.emailjs.com/
2. Click **"Logs"** in the left sidebar
3. You should see:
   - **Green checkmarks** = Successful sends
   - **Red X marks** = Failed sends
4. Click on any failed send to see error details

---

## Rate Limits

Remember EmailJS free tier limits:
- **200 emails per month**
- If you hit the limit, upgrade to paid plan ($10/month for 1000 emails)

---

## Quick Checklist

- [ ] Disconnected old Gmail connection from EmailJS
- [ ] Reconnected Gmail with all permissions granted
- [ ] Verified "Send email on your behalf" permission was granted
- [ ] Sent test email from EmailJS dashboard (successful)
- [ ] Updated `.env` file with correct EmailJS credentials
- [ ] Ran `node setup-credentials.js` to regenerate config
- [ ] Cleared browser cache
- [ ] Tested form submission (successful)
- [ ] Verified email arrived at destination
- [ ] Checked EmailJS logs (no 412 errors)

---

## Still Having Issues?

If you're still seeing 412 errors after following this guide:

1. **Check the exact error message** in EmailJS dashboard logs
2. **Verify Gmail account permissions**: https://myaccount.google.com/permissions
3. **Try using EmailJS's built-in email service** instead of Gmail (see above)
4. **Contact EmailJS support**: https://www.emailjs.com/docs

---

## Contact Information

For urgent issues, you can:
- Check EmailJS documentation: https://www.emailjs.com/docs/
- Contact EmailJS support through their dashboard
- Check Google OAuth troubleshooting: https://support.google.com/

---

**Last Updated:** February 12, 2026
