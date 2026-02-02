# Setup Guide - Sarasota Gospel Temple Website
## Custom Forms with Firebase Backend

This guide will walk you through setting up your custom forms with Firebase database, admin dashboard, and email notifications.

---

## Overview of What You're Getting

✅ **Custom Forms** (matching your brand design):
- Registration Form (3 phases)
- Volunteer Sign-up Form
- Vendor Application Form

✅ **Firebase Backend**:
- YOUR own database (you own all data)
- Real-time data sync
- Secure authentication

✅ **Admin Dashboard**:
- View all submissions in real-time
- Export to Excel/CSV
- Search and filter data
- Approve/deny vendors
- Delete records

✅ **Email Notifications**:
- Instant notification when someone submits
- Confirmation emails to registrants

✅ **Cost**: **100% FREE** (Firebase free tier)

---

## Part 1: Firebase Setup (15 minutes)

### Step 1: Create Firebase Account

1. Go to [https://firebase.google.com/](https://firebase.google.com/)
2. Click "Get Started"
3. Sign in with your Google account (or create one)

### Step 2: Create a New Project

1. Click "Add Project"
2. Project name: `sarasota-gospel-temple` (or your preferred name)
3. Click "Continue"
4. **Disable Google Analytics** (not needed for this) - Toggle OFF
5. Click "Create Project"
6. Wait for project to be created (30 seconds)
7. Click "Continue"

### Step 3: Set Up Firestore Database

1. In the left sidebar, click "Build" → "Firestore Database"
2. Click "Create database"
3. Select "Start in **production mode**"
4. Click "Next"
5. Choose location: **nam5 (us-central)** (closest to Florida)
6. Click "Enable"
7. Wait for database to be created (1 minute)

### Step 4: Configure Firestore Rules

1. Click on the "Rules" tab
2. Replace the default rules with this:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow public to write to forms (submissions)
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

3. Click "Publish"

**What this does**: Anyone can submit forms (create), but only authenticated admins can view/edit/delete data.

### Step 5: Get Your Firebase Configuration

1. Click the gear icon ⚙️ (Settings) next to "Project Overview"
2. Click "Project settings"
3. Scroll down to "Your apps"
4. Click the **Web** icon (`</>`)
5. App nickname: `SGT Website`
6. **DO NOT** check "Firebase Hosting" (we'll host elsewhere)
7. Click "Register app"
8. You'll see a `firebaseConfig` object that looks like this:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXX",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:xxxxxxxxxxxxx",
  databaseURL: "https://your-project.firebaseio.com"
};
```

9. **COPY THIS ENTIRE OBJECT** - you'll need it shortly
10. Click "Continue to console"

### Step 6: Enable Authentication

1. In the left sidebar, click "Build" → "Authentication"
2. Click "Get started"
3. Click on "Email/Password" provider
4. Toggle "Enable" to ON
5. Click "Save"

### Step 7: Create Admin User

1. Still in Authentication, click "Users" tab
2. Click "Add user"
3. Email: `your-admin-email@example.com` (YOUR email)
4. Password: Create a secure password (save it somewhere safe!)
5. Click "Add user"

**IMPORTANT**: Save your admin email and password - you'll use this to login to the dashboard.

### Step 8: Update Your Website Code

1. Open the file: `config/firebase-config.js`
2. Find this section:

```javascript
const firebaseConfig = {
    apiKey: "YOUR_API_KEY_HERE",
    authDomain: "your-project-id.firebaseapp.com",
    ...
};
```

3. **REPLACE** it with the configuration you copied in Step 5
4. Save the file

**You're done with Firebase!** 🎉

---

## Part 2: Email Notifications Setup (10 minutes)

We'll use EmailJS - a free service that sends emails directly from JavaScript.

### Step 1: Create EmailJS Account

1. Go to [https://www.emailjs.com/](https://www.emailjs.com/)
2. Click "Sign Up Free"
3. Create account with your email
4. Verify your email address

### Step 2: Add Email Service

1. In EmailJS dashboard, click "Email Services"
2. Click "Add New Service"
3. Choose your email provider:
   - **Gmail** (if you use Gmail) - RECOMMENDED
   - Or "Outlook", "Yahoo", etc.
4. Click "Connect Account"
5. Follow prompts to authorize EmailJS to send emails on your behalf
6. Service Name: `SGT Notifications`
7. Click "Create Service"
8. **COPY the Service ID** (looks like `service_xxxxxxx`)

### Step 3: Create Email Template

1. Click "Email Templates" in sidebar
2. Click "Create New Template"
3. Template Name: `Registration Notification`
4. In the template editor, paste this:

```
Subject: New Registration - 2026 International Meeting

{{from_name}} has registered for the International Meeting

Name: {{from_name}}
Email: {{reply_to}}
Phone: {{phone}}
Pastor: {{pastor}}

Services Attending: {{services}}

Airport Transportation: {{airport_transport}}
Local Transportation: {{local_transport}}

Children Under 5: {{has_children}}

Submitted: {{timestamp}}

---
View all registrations in admin dashboard
```

5. Click "Save"
6. **COPY the Template ID** (looks like `template_xxxxxxx`)

### Step 4: Get Your Public Key

1. Click "Account" (top right)
2. Find "API Keys" section
3. **COPY the Public Key** (looks like a long string)

### Step 5: Update Your Website Code

1. Open the file: `config/firebase-config.js`
2. Find this section:

```javascript
const EMAILJS_SERVICE_ID = 'YOUR_EMAILJS_SERVICE_ID';
const EMAILJS_TEMPLATE_ID = 'YOUR_EMAILJS_TEMPLATE_ID';
const EMAILJS_PUBLIC_KEY = 'YOUR_EMAILJS_PUBLIC_KEY';
```

3. Replace with YOUR values:
   - Service ID from Step 2
   - Template ID from Step 3
   - Public Key from Step 4

4. Save the file

### Step 6: Update Email Recipients

1. Open `config/firebase-config.js`
2. Find:

```javascript
to_email: 'sarasotagospel@gmail.com',
```

3. Change to YOUR email address where you want notifications
4. Save

**Email setup complete!** 📧

---

## Part 3: Website Deployment (20 minutes)

You have several options for hosting. I recommend **Netlify** (free and easy).

### Option A: Netlify (RECOMMENDED - Free)

#### Step 1: Create Netlify Account

1. Go to [https://www.netlify.com/](https://www.netlify.com/)
2. Click "Sign up"
3. Sign up with GitHub (or email)

#### Step 2: Deploy Your Site

**Method 1: Drag and Drop (Easiest)**

1. In Netlify dashboard, look for the big box that says "Want to deploy a new site without connecting to Git? Drag and drop your site folder here"
2. Open your `VS-Code` folder on your computer
3. Drag the ENTIRE folder into that box
4. Wait for upload (1-2 minutes)
5. You'll get a random URL like `random-name-123456.netlify.app`

**Method 2: GitHub (Better for updates)**

1. Push your code to GitHub repository
2. In Netlify, click "Add new site" → "Import an existing project"
3. Choose "GitHub"
4. Select your repository
5. Build settings: Leave blank (it's just HTML/CSS/JS)
6. Click "Deploy site"
7. Wait for deployment (2 minutes)

#### Step 3: Custom Domain (Optional)

If you own a domain (like `sarasotagospeltemple.org`):

1. In Netlify site settings, click "Domain settings"
2. Click "Add custom domain"
3. Enter your domain
4. Follow DNS instructions to point domain to Netlify

### Option B: Firebase Hosting (Also Free)

1. Install Firebase CLI: Open terminal and run:
   ```bash
   npm install -g firebase-tools
   ```

2. Login to Firebase:
   ```bash
   firebase login
   ```

3. Initialize hosting in your project folder:
   ```bash
   cd /path/to/VS-Code
   firebase init hosting
   ```
   - Select your Firebase project
   - Public directory: `.` (current folder)
   - Single page app: No
   - Don't overwrite files

4. Deploy:
   ```bash
   firebase deploy --only hosting
   ```

5. You'll get a URL like `your-project.web.app`

### Option C: Traditional Web Hosting

If you have traditional hosting (GoDaddy, Bluehost, etc.):

1. Connect via FTP (FileZilla or similar)
2. Upload all files to `public_html` or `www` folder
3. Make sure `index.html` is in the root
4. Forms will work immediately

---

## Part 4: Testing Everything (15 minutes)

### Test 1: Submit a Registration

1. Go to your website URL
2. Navigate to the registration form
3. Fill out all 3 phases with test data
4. Submit
5. You should see success message

### Test 2: Check Firebase Database

1. Go to Firebase Console
2. Click "Firestore Database"
3. You should see a new document in `registrations` collection
4. Click on it to see all the form data

### Test 3: Check Email Notification

1. Check your email (the one you set in EmailJS)
2. You should have received a notification email
3. If not, check spam folder

### Test 4: Access Admin Dashboard

1. Go to `your-website-url/admin/dashboard.html`
2. Login with the admin email/password you created in Firebase
3. You should see the test registration in the table
4. Click "Export to Excel" to test CSV download

### Test 5: Form Validation

1. Try submitting form with empty fields → Should show errors
2. Try proceeding to next phase without filling required fields → Should block
3. Test phone number format validation
4. Test email format validation

---

## Part 5: Customization & Branding

### Update Contact Information

**In registration.html** (lines 50-54):
```html
<p><strong>Dates:</strong> April 9-11, 2026</p>
<p><strong>Location:</strong> 1900 Gandy Blvd N, St. Petersburg, FL 33702</p>
<p><strong>Contact:</strong> 941-800-5211</p>
```

Change to your actual info.

### Update Colors (if needed)

**In css/design-system.css** (lines 9-16):
```css
--navy-blue: #28478a;
--beige: #e4e3dd;
--burnt-orange: #c45508;
```

These are your official brand colors - don't change unless needed.

### Add Your Logo

1. Save your logo as `logo.png` in `assets/images/`
2. In forms/registration.html, add at top:
```html
<img src="../assets/images/logo.png" alt="SGT Logo" style="max-width: 200px;">
```

### Add Lighthouse Background

1. Save lighthouse illustration as `lighthouse.png` in `assets/images/`
2. Uncomment the lighthouse watermark section in registration.html

---

## Part 6: Daily Operations

### Viewing New Registrations

1. Go to `your-website-url/admin/dashboard.html`
2. Login with admin credentials
3. See all registrations in real-time
4. Click "Refresh" to get latest data

### Exporting Data to Excel

1. In admin dashboard, click section (Registrations/Volunteers/Vendors)
2. Click "📥 Export to Excel" button
3. CSV file downloads automatically
4. Open in Excel or Google Sheets

### Approving Vendors

1. Go to Vendors section in dashboard
2. Click "View" on any vendor
3. Review their application
4. Click "Approve" if accepted
5. Vendor status updates to "Approved"

### Searching & Filtering

1. Use search box at top of each section
2. Type name, email, phone, etc.
3. Table filters in real-time

### Backing Up Data

**Automatic**: Firebase backs up automatically daily

**Manual Export**:
1. Export each section to CSV regularly
2. Save CSV files to your computer
3. Recommended: Weekly backups

---

## Part 7: Troubleshooting

### Problem: Forms Don't Submit

**Solution**:
1. Check browser console (F12) for errors
2. Verify Firebase config is correct in `firebase-config.js`
3. Check Firestore rules allow public `create`
4. Try in incognito mode (rules out extensions)

### Problem: Can't Login to Admin Dashboard

**Solutions**:
- Verify email/password is correct
- Check if user exists in Firebase Authentication
- Clear browser cache and cookies
- Try different browser

### Problem: Emails Not Sending

**Solutions**:
- Verify EmailJS Service ID, Template ID, and Public Key are correct
- Check if EmailJS service is connected to your email
- Check spam folder
- Verify email address in code is correct
- Check EmailJS dashboard for error logs

### Problem: "Permission Denied" in Firestore

**Solutions**:
- Check Firestore Rules allow public `create`
- For admin operations, ensure you're logged in
- Verify authentication is working

### Problem: Export Not Working

**Solutions**:
- Check if there's data to export
- Try different browser
- Check browser's download settings
- Look for popup blocker

---

## Part 8: Security & Privacy

### Data Security

✅ **Encrypted**: All data transmitted over HTTPS
✅ **Access Control**: Only admins can view data
✅ **Authentication**: Secure login required for admin
✅ **Firestore Rules**: Protects against unauthorized access

### Privacy Compliance

Add this to your forms (above submit button):

```html
<p style="font-size: 14px; color: #6e6a67;">
By submitting this form, you agree to our
<a href="/privacy-policy">Privacy Policy</a>.
Your information will only be used for event planning and will not be shared with third parties.
</p>
```

### Admin Access

**Best Practices**:
- Use a strong password (12+ characters)
- Don't share admin credentials
- Log out when done
- Change password periodically
- Consider enabling 2-factor authentication in Firebase

---

## Part 9: Cost Breakdown

### Firebase (Database & Hosting)
- **Free tier**: Up to 1GB storage, 10GB bandwidth/month
- **Cost for this project**: $0/month
- Easily handles 1000+ registrations

### EmailJS (Email notifications)
- **Free tier**: 200 emails/month
- **Cost**: $0/month
- If you need more: $7/month for 1000 emails

### Domain Name (Optional)
- **Cost**: ~$12-15/year
- Examples: GoDaddy, Namecheap, Google Domains

### **Total Ongoing Cost: $0-2/month** 🎉

---

## Part 10: Next Steps & Enhancements

### Immediate Next Steps

1. ✅ Set up Firebase (Part 1)
2. ✅ Set up EmailJS (Part 2)
3. ✅ Deploy website (Part 3)
4. ✅ Test everything (Part 4)
5. 📢 Share registration link with congregation

### Future Enhancements

**Phase 2 (Optional)**:
- Add volunteer and vendor forms
- Create QR codes for check-in
- Add calendar integration
- SMS notifications via Twilio
- Payment integration (if charging registration fee)
- Multi-language support (Haitian Creole, Spanish)

**Phase 3 (Optional)**:
- Event check-in system with QR codes
- Attendance tracking
- Automated reminder emails
- Reports and analytics dashboard
- Mobile app for admins

---

## Support & Help

### Need Help?

**Firebase Documentation**: [https://firebase.google.com/docs](https://firebase.google.com/docs)
**EmailJS Documentation**: [https://www.emailjs.com/docs/](https://www.emailjs.com/docs/)

### Common Questions

**Q: Can multiple people access the admin dashboard?**
A: Yes! Create additional users in Firebase Authentication. Each gets their own login.

**Q: Can I edit a registration after it's submitted?**
A: Yes, but you'll need to do it in Firebase Console directly, or add an edit feature to the dashboard.

**Q: What happens if I exceed the free tier limits?**
A: Firebase will notify you. For 1000-2000 registrations, you'll stay well within free limits.

**Q: Can I use my own email server instead of EmailJS?**
A: Yes! You can set up SendGrid, Mailgun, or use your server's SMTP.

**Q: Is my data secure?**
A: Yes! Firebase uses enterprise-grade security. Data is encrypted, and only admins can access it.

---

## Quick Reference

### Important URLs

- **Firebase Console**: [https://console.firebase.google.com/](https://console.firebase.google.com/)
- **EmailJS Dashboard**: [https://dashboard.emailjs.com/](https://dashboard.emailjs.com/)
- **Your Website**: (your deployed URL)
- **Admin Dashboard**: `your-website-url/admin/dashboard.html`

### Admin Credentials

- **Email**: (the one you created in Firebase)
- **Password**: (save this securely!)

### File Locations

- **Registration Form**: `forms/registration.html`
- **Admin Dashboard**: `admin/dashboard.html`
- **Firebase Config**: `config/firebase-config.js`
- **Design System**: `css/design-system.css`

---

## Success Checklist

Before going live, verify:

- [ ] Firebase project created and configured
- [ ] Firestore rules published
- [ ] Admin user created in Authentication
- [ ] Firebase config updated in code
- [ ] EmailJS account created and configured
- [ ] Email template created in EmailJS
- [ ] EmailJS IDs updated in code
- [ ] Website deployed and accessible
- [ ] Test registration submitted successfully
- [ ] Registration appears in Firestore
- [ ] Email notification received
- [ ] Admin dashboard accessible and working
- [ ] Export to Excel working
- [ ] Contact information updated in forms
- [ ] Privacy policy added (if required)

---

**Congratulations!** Your custom form system is ready! 🎉

You now have a professional, fully-branded registration system that you completely own and control, with zero monthly fees.

---

**Questions?** Review the troubleshooting section or reach out for support.

**Last Updated**: January 22, 2026
**Version**: 1.0
