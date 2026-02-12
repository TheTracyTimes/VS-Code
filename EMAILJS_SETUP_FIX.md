# Fix Email Notifications and Google Sheets Sync

## Problem
Form submissions are saving to Firestore but:
- ❌ Confirmation emails are NOT being sent
- ❌ Data is NOT syncing to Google Sheets

## Root Causes

### 1. EmailJS Template IDs Not Configured
The EmailJS template IDs in your configuration are placeholders and need to be replaced with actual template IDs from your EmailJS dashboard.

### 2. Google Sheets API Not Fully Configured
Google Sheets API requires user authentication (OAuth) to write data, which is not currently implemented.

---

## Solution 1: Fix EmailJS (Required)

### Step 1: Check Your EmailJS Templates

1. Go to your EmailJS dashboard: https://dashboard.emailjs.com/admin/templates
2. You should have **3 templates** created:
   - One for Registration notifications
   - One for Vendor notifications
   - One for Volunteer notifications

3. For each template, copy the **Template ID** (looks like `template_abc123xyz`)

### Step 2: Update Your Environment Variables

1. Open your `.env` file (NOT `.env.example`)
2. Add these lines at the end:

```bash
# EmailJS Template IDs
EMAILJS_TEMPLATE_REGISTRATION=template_abc123xyz
EMAILJS_TEMPLATE_VENDOR=template_def456uvw
EMAILJS_TEMPLATE_VOLUNTEER=template_ghi789rst
```

**Replace** `template_abc123xyz`, etc. with your actual template IDs from Step 1.

### Step 3: Regenerate Configuration Files

Run the setup script to regenerate your config files with the new template IDs:

```bash
node setup-credentials.js
```

This will update `/config/firebase-config.js` with your actual template IDs.

### Step 4: Create Proper EmailJS Templates

If you haven't created the templates yet, here's what each should contain:

#### Registration Template

**Template Name:** `Registration Notification`

**To Email:** `sarasotagospel@gmail.com` (or your church email)

**Subject:**
```
New Registration - 2026 International Meeting
```

**Body:**
```
New registration received:

Name: {{firstName}} {{lastName}}
Phone: {{phone}}
Email: {{email}}
Pastor: {{pastorName}}
Assembly: {{assemblyName}}

Services Attending: {{services}}

Airport Transport: {{airportTransport}}
Local Transport: {{localTransport}}

Children Under 5: {{hasChildren}}

Submitted: {{timestamp}}

---
Sent from Sarasota Gospel Temple Website
```

#### Vendor Template

**Template Name:** `Vendor Application`

**To Email:** `sarasotagospel@gmail.com`

**Subject:**
```
New Vendor Application - {{businessName}}
```

**Body:**
```
New vendor application received:

Business Name: {{businessName}}
Contact: {{firstName}} {{lastName}}
Phone: {{phone}}
Email: {{email}}
Website: {{website}}

Pastor: {{pastorName}}
Assembly: {{assemblyName}}

Selling: {{selling}}
Table Staffed: {{tableStaffed}}
Availability: {{availability}}

Status: PENDING APPROVAL

Submitted: {{timestamp}}

---
Sent from Sarasota Gospel Temple Website
```

#### Volunteer Template

**Template Name:** `Volunteer Application`

**To Email:** `sarasotagospel@gmail.com`

**Subject:**
```
New Volunteer Sign-Up - {{firstName}} {{lastName}}
```

**Body:**
```
New volunteer application received:

Name: {{firstName}} {{lastName}}
Phone: {{phone}}
Email: {{email}}

Committees: {{committees}}
Availability: {{availability}}

Submitted: {{timestamp}}

---
Sent from Sarasota Gospel Temple Website
```

### Step 5: Test Your Forms

1. Open your website
2. Submit a test form
3. Check:
   - ✅ Email arrives at sarasotagospel@gmail.com
   - ✅ Data appears in Firestore
   - ✅ Success message shows on website

---

## Solution 2: Fix Google Sheets (Optional)

### Current Limitation

The current Google Sheets integration requires user authentication (OAuth login) to write data to sheets. This means users would need to click "Sign in with Google" before submitting forms.

### Recommended Approach: Use Firebase Functions (Server-Side)

Instead of client-side Google Sheets API, use Firebase Functions to write to Google Sheets server-side:

1. **Firebase Functions** receive the form submission
2. **Service Account** authenticates with Google Sheets
3. **Data is written** to your spreadsheet automatically
4. **No user authentication** required

This is already partially set up in your `functions/index.js` file.

### Quick Fix: Disable Google Sheets Sync

If you don't need Google Sheets sync immediately, it's already set up as non-blocking. The forms will work fine without it - they just won't sync to sheets.

The code already handles this gracefully:
```javascript
// Sync to Google Sheets (non-blocking - won't prevent form submission)
if (window.GoogleSheetsService && window.GoogleSheetsService.isGoogleSheetsConfigured()) {
    window.GoogleSheetsService.addRowToSheet('registrations', formData).catch(err => {
        console.warn('Google Sheets sync failed (form still submitted successfully)');
    });
}
```

---

## Testing Checklist

After completing the EmailJS setup:

- [ ] Submit a registration form
  - [ ] Firestore saves the data
  - [ ] Email arrives at sarasotagospel@gmail.com
  - [ ] Success message appears

- [ ] Submit a vendor application
  - [ ] Firestore saves the data
  - [ ] Email arrives at sarasotagospel@gmail.com
  - [ ] Success message appears

- [ ] Submit a volunteer form
  - [ ] Firestore saves the data
  - [ ] Email arrives at sarasotagospel@gmail.com
  - [ ] Success message appears

---

## Troubleshooting

### Emails Still Not Sending?

1. **Check Browser Console** (F12):
   - Look for EmailJS errors
   - Check if templates are being found

2. **Verify EmailJS Dashboard**:
   - Go to https://dashboard.emailjs.com/admin
   - Check "Logs" section for failed email attempts
   - Verify your service is connected (Gmail, etc.)

3. **Check Template IDs**:
   - Open `/config/firebase-config.js`
   - Verify the template IDs match your EmailJS dashboard

4. **EmailJS Quota**:
   - Free plan: 200 emails/month
   - Check if you've hit the limit

### Google Sheets Not Syncing?

This is expected with the current setup. See "Solution 2" above for details.

---

## Need Help?

If you're still experiencing issues:

1. Check the browser console (F12) for error messages
2. Check EmailJS dashboard logs
3. Verify all template IDs are correct
4. Ensure your EmailJS service is connected and active
