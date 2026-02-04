# Firebase + EmailJS Setup Guide
## Sarasota Gospel Temple Website Forms

This guide will walk you through setting up Firebase (for storing form data) and EmailJS (for email notifications) for your church website forms.

---

## Part 1: Firebase Setup

### Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Add project"** or **"Create a project"**
3. Enter project name: `sarasota-gospel-temple` (or your preferred name)
4. Disable Google Analytics (not needed for forms) or enable if you want analytics
5. Click **"Create project"**

### Step 2: Get Your Firebase Configuration

1. In the Firebase Console, click the **gear icon** (⚙️) next to "Project Overview"
2. Select **"Project settings"**
3. Scroll down to **"Your apps"** section
4. Click the **Web icon** (`</>`) to add a web app
5. Enter app nickname: `SGT Website`
6. **Do NOT check** "Also set up Firebase Hosting"
7. Click **"Register app"**
8. Copy the `firebaseConfig` object that appears

It will look like this:
```javascript
const firebaseConfig = {
  apiKey: "AIzaSyC...",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123"
};
```

### Step 3: Update Your Firebase Config File

1. Open the file: `/config/firebase-config.js`
2. Replace lines 14-22 with YOUR actual Firebase config values:

```javascript
const firebaseConfig = {
    apiKey: "YOUR_ACTUAL_API_KEY",
    authDomain: "your-actual-project.firebaseapp.com",
    projectId: "your-actual-project-id",
    storageBucket: "your-actual-project.appspot.com",
    messagingSenderId: "YOUR_ACTUAL_SENDER_ID",
    appId: "YOUR_ACTUAL_APP_ID",
    databaseURL: "https://your-actual-project.firebaseio.com"
};
```

### Step 4: Enable Firestore Database

1. In Firebase Console, click **"Firestore Database"** in the left sidebar
2. Click **"Create database"**
3. Select **"Start in production mode"** (we'll set rules next)
4. Choose location: **us-central** (or nearest to Florida)
5. Click **"Enable"**

### Step 5: Set Firestore Security Rules

1. In Firestore Database, click the **"Rules"** tab
2. Replace the default rules with these:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // Allow anyone to create (submit) forms
    match /registrations/{document} {
      allow create: if true;
      allow read, update, delete: if request.auth != null;
    }

    match /volunteers/{document} {
      allow create: if true;
      allow read, update, delete: if request.auth != null;
    }

    match /vendors/{document} {
      allow create: if true;
      allow read, update, delete: if request.auth != null;
    }
  }
}
```

3. Click **"Publish"**

**What these rules do:**
- Anyone can submit forms (create new documents)
- Only authenticated admins can read, update, or delete submissions
- This protects your data while allowing public form submissions

---

## Part 2: EmailJS Setup

EmailJS allows you to send emails directly from your website without a backend server. It's free for up to 200 emails/month.

### Step 1: Create EmailJS Account

1. Go to [EmailJS.com](https://www.emailjs.com/)
2. Click **"Sign Up Free"**
3. Create account with your church email or personal email
4. Verify your email address

### Step 2: Add an Email Service

1. In EmailJS dashboard, go to **"Email Services"**
2. Click **"Add New Service"**
3. Choose your email provider:
   - **Gmail** (recommended if using Gmail)
   - **Outlook/Office365** (if using Microsoft)
   - Or use their built-in service
4. Connect your email account (sarasotagospeltemple@gmail.com or your admin email)
5. Copy the **Service ID** (looks like `service_abc123`)

### Step 3: Create Email Templates

You need to create **THREE email templates** - one for each form type.

#### Template 1: Registration Notification

1. Go to **"Email Templates"** in EmailJS dashboard
2. Click **"Create New Template"**
3. Template Name: `Registration Notification`
4. Template Content:

**Subject:**
```
New Registration - {{from_name}}
```

**Body:**
```
New registration received for 2026 International Meeting:

Name: {{from_name}}
Phone: {{phone}}
Email: {{email}}
Pastor: {{pastor_name}}
Assembly: {{assembly_name}}

Services Attending: {{services}}

Airport Transport: {{airport_transport}}
Local Transport: {{local_transport}}

Children Under 5: {{has_children}}
Number of Children: {{num_children}}

VBS Attendance: {{vbs_attendance}}
Nursery: {{nursery_attendance}}

Submitted: {{submission_date}}

---
Sent from Sarasota Gospel Temple Website
```

5. Set **To Email:** `sarasotagospeltemple@gmail.com` (or your church email)
6. Save and copy the **Template ID** (looks like `template_abc123`)

#### Template 2: Volunteer Notification

1. Create another new template
2. Template Name: `Volunteer Application`
3. Template Content:

**Subject:**
```
New Volunteer Application - {{from_name}}
```

**Body:**
```
New volunteer application received:

Name: {{from_name}}
Email: {{email}}
Phone: {{phone}}

Areas of Interest:
{{areas_of_interest}}

Availability:
{{availability}}

Experience/Skills:
{{experience}}

Additional Comments:
{{comments}}

Submitted: {{submission_date}}

---
Sent from Sarasota Gospel Temple Website
```

4. Set **To Email:** `sarasotagospeltemple@gmail.com`
5. Save and copy the **Template ID**

#### Template 3: Vendor Application

1. Create another new template
2. Template Name: `Vendor Application`
3. Template Content:

**Subject:**
```
New Vendor Application - {{business_name}}
```

**Body:**
```
New vendor application received:

Business Name: {{business_name}}
Contact Name: {{contact_name}}
Email: {{email}}
Phone: {{phone}}
Website: {{website}}

Product/Service Type: {{product_type}}
Booth Size: {{booth_size}}
Setup Time: {{setup_time}}

Special Requirements:
{{special_requirements}}

Submitted: {{submission_date}}

---
Sent from Sarasota Gospel Temple Website
```

4. Set **To Email:** `sarasotagospeltemple@gmail.com`
5. Save and copy the **Template ID**

### Step 4: Get Your Public Key

1. Go to **"Account"** in EmailJS dashboard
2. Find **"API Keys"** section
3. Copy your **Public Key** (looks like `abc123xyz456`)

### Step 5: Update Your Firebase Config with EmailJS Credentials

1. Open `/config/firebase-config.js`
2. Find lines 265-267 and update with YOUR actual values:

```javascript
const EMAILJS_SERVICE_ID = 'service_abc123';  // From Step 2
const EMAILJS_TEMPLATE_ID = 'template_abc123'; // From Step 3 (Registration template)
const EMAILJS_PUBLIC_KEY = 'abc123xyz456';     // From Step 4
```

**Note:** You may want to create separate template IDs for each form. The current setup uses one template ID, but you can customize each form's JavaScript file to use different templates.

---

## Part 3: Update Form JavaScript Files (Optional)

If you want different email templates for each form type:

### For Registration Form (`js/registration-form.js`)
Update the EmailJS template ID to your registration template:
```javascript
const EMAILJS_TEMPLATE_ID = 'template_registration123';
```

### For Volunteer Form (`js/volunteer-form.js`)
Update to your volunteer template:
```javascript
const EMAILJS_TEMPLATE_ID = 'template_volunteer456';
```

### For Vendor Form (`js/vendor-form.js`)
Update to your vendor template:
```javascript
const EMAILJS_TEMPLATE_ID = 'template_vendor789';
```

---

## Part 4: Testing Your Forms

### Test Registration Form

1. Open your website in a browser
2. Navigate to the registration form
3. Fill out the form with test data
4. Submit the form
5. Check for:
   - ✅ Success message appears on the page
   - ✅ Email arrives at sarasotagospeltemple@gmail.com
   - ✅ Data appears in Firebase Console (Firestore Database)

### Check Firebase Data

1. Go to Firebase Console
2. Click **"Firestore Database"**
3. Look for collections: `registrations`, `volunteers`, `vendors`
4. Click on a collection to see submitted data
5. Each document should have all the form fields

### Check Email Notifications

1. Check the inbox for sarasotagospeltemple@gmail.com
2. Emails should arrive within 1-2 minutes
3. If no email arrives:
   - Check spam folder
   - Verify EmailJS service is connected
   - Check EmailJS dashboard for logs/errors

---

## Part 5: Deploy to Wix

### Option A: Upload to Wix as Custom Code

1. Log into Wix Editor
2. Go to **Settings** → **Custom Code**
3. Click **"Add Custom Code"**
4. Add Firebase SDK:
```html
<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore-compat.js"></script>
```
5. Add EmailJS SDK:
```html
<script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@3/dist/email.min.js"></script>
```
6. Upload your `firebase-config.js` file

### Option B: Embed as iFrame

1. Upload your entire website (HTML, CSS, JS files) to a hosting service like:
   - GitHub Pages (free)
   - Netlify (free)
   - Vercel (free)
2. In Wix, add an **iFrame** element
3. Set the iFrame source to your hosted form pages

### Option C: Use Wix's HTML Element (Recommended)

1. In Wix Editor, click **Add** (+)
2. Go to **Embed** → **HTML iframe**
3. Click **"Code"** mode
4. Paste your form HTML with embedded scripts
5. Make sure to include:
   - Firebase SDK scripts
   - EmailJS SDK script
   - Your firebase-config.js
   - Your form-specific JS file

---

## Part 6: Admin Dashboard (View Submissions)

Your site already has an admin dashboard setup. To access it:

1. Create the admin page on your Wix site
2. Upload `admin-dashboard.js` to your Wix site
3. Set up Firebase Authentication:
   - In Firebase Console, go to **Authentication**
   - Click **"Get Started"**
   - Enable **"Email/Password"** sign-in method
   - Go to **"Users"** tab
   - Click **"Add User"**
   - Create an admin account with your email and password

4. The admin dashboard will show:
   - All registrations
   - All volunteer applications
   - All vendor applications
   - Export to CSV functionality

---

## Security Best Practices

### 1. Protect Your Firebase Config
- Your Firebase API key is safe to be public (it's client-side)
- Security comes from Firestore rules, not hiding the config
- Never put admin passwords in client-side code

### 2. Firestore Rules
- Keep rules as shown above (create only for public, read/write for authenticated admins)
- Never use `allow read, write: if true;` in production

### 3. EmailJS Rate Limits
- Free tier: 200 emails/month
- If you exceed, upgrade to paid plan ($10/month for 1000 emails)
- Monitor usage in EmailJS dashboard

### 4. Spam Protection
- Consider adding Google reCAPTCHA to forms
- Monitor Firebase for spam submissions
- Set up email filters if needed

---

## Troubleshooting

### Forms Not Submitting

1. **Check browser console** (F12) for errors
2. **Verify Firebase config** is correct in `firebase-config.js`
3. **Check Firestore rules** allow create operations
4. **Verify internet connection** (Firebase requires online access)

### Emails Not Sending

1. **Check EmailJS dashboard** for error logs
2. **Verify service connection** is active
3. **Check template IDs** match in config file
4. **Verify email address** in template settings
5. **Check spam folder** for received emails

### Data Not Appearing in Firebase

1. **Check Firebase Console** → Firestore Database
2. **Verify rules** allow create operations
3. **Check browser console** for error messages
4. **Test with simple data** first

### CORS Errors on Wix

If you get CORS errors when hosting on Wix:
1. Upload files to a separate hosting service (Netlify, Vercel)
2. Use iFrame embedding in Wix
3. Or use Wix Velo (custom backend) instead

---

## Cost Summary

| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| **Firebase** | 50K reads/day, 20K writes/day | Pay as you go (~$0.18 per 100K) |
| **EmailJS** | 200 emails/month | $10/month for 1000 emails |
| **Total** | FREE for small church | ~$10/month if high volume |

For a church your size, the **free tier should be more than sufficient**.

---

## Support

If you need help:
- Firebase: https://firebase.google.com/support
- EmailJS: https://www.emailjs.com/docs
- Check browser console for error messages

**Your forms are already configured and ready to go!** Just add your Firebase and EmailJS credentials to `config/firebase-config.js` and you're all set.
