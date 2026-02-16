# Sarasota Gospel Temple Website - Deployment Guide

This guide will walk you through deploying your complete custom website with forms to production.

## 📋 Prerequisites

Before deploying, you'll need:
- A Firebase account (free tier is sufficient)
- An EmailJS account (free tier allows 200 emails/month)
- A Wix account with your domain connected
- Google Maps API key (for the map on contact page - already configured)

---

## 🔥 Step 1: Firebase Setup (Database & Authentication)

### 1.1 Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Add project"**
3. Name it: `sarasota-gospel-temple` (or your preferred name)
4. Disable Google Analytics (not needed for this project)
5. Click **"Create project"**

### 1.2 Enable Firestore Database

1. In your Firebase project, click **"Firestore Database"** in the left menu
2. Click **"Create database"**
3. Select **"Start in production mode"**
4. Choose a location (select `us-east1` for East Coast)
5. Click **"Enable"**

### 1.3 Configure Firestore Security Rules

1. In Firestore, click the **"Rules"** tab
2. Replace the default rules with:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow anyone to submit forms (create)
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

**What this does:** Allows anyone to submit forms, but only authenticated admins can view/manage submissions.

### 1.4 Enable Authentication

1. Click **"Authentication"** in the left menu
2. Click **"Get started"**
3. Click on **"Email/Password"** provider
4. Enable it and click **"Save"**

### 1.5 Create Admin User

1. Go to **Authentication > Users** tab
2. Click **"Add user"**
3. Enter your admin email: `sarasotagospel@gmail.com` (or preferred admin email)
4. Create a secure password (save it somewhere safe!)
5. Click **"Add user"**

### 1.6 Get Firebase Configuration

1. Click the **gear icon** ⚙️ next to "Project Overview"
2. Click **"Project settings"**
3. Scroll down to **"Your apps"**
4. Click the **web icon** `</>`
5. Register app name: `Sarasota Gospel Temple Website`
6. Don't check "Firebase Hosting" (we'll use Netlify)
7. Click **"Register app"**
8. Copy the `firebaseConfig` object - you'll need this next!

---

## ✉️ Step 2: EmailJS Setup (Form Notifications)

### 2.1 Create EmailJS Account

1. Go to [EmailJS](https://www.emailjs.com/)
2. Sign up for free account
3. Verify your email address

### 2.2 Add Email Service

1. Go to **"Email Services"** in dashboard
2. Click **"Add New Service"**
3. Select **Gmail** (or your preferred email provider)
4. Connect your email account: `sarasotagospel@gmail.com`
5. Note the **Service ID** (e.g., `service_abc123`)

### 2.3 Create Email Templates

Create THREE templates for each form type:

#### Template 1: Registration Confirmation
1. Go to **"Email Templates"**
2. Click **"Create New Template"**
3. Name: `registration_confirmation`
4. Subject: `Registration Confirmed - 2026 International Meeting`
5. Content:

```
Hello {{firstName}} {{lastName}},

Thank you for registering for the 2026 International Meeting at Sarasota Gospel Temple!

Registration Details:
- Name: {{firstName}} {{lastName}}
- Church: {{churchName}}
- Pastor: {{pastorName}}
- Email: {{email}}
- Phone: {{phone}}

We'll send you more information as the event approaches.

Blessings,
Sarasota Gospel Temple
```

6. Note the **Template ID** (e.g., `template_xyz789`)

#### Template 2: Volunteer Confirmation
1. Create another template
2. Name: `volunteer_confirmation`
3. Subject: `Volunteer Application Received - 2026 International Meeting`
4. Content:

```
Hello {{firstName}} {{lastName}},

Thank you for volunteering for the 2026 International Meeting!

Your application has been received. We'll contact you soon regarding your committee assignments.

Selected Committees: {{committees}}

Blessings,
Sarasota Gospel Temple
```

5. Note the **Template ID**

#### Template 3: Vendor Confirmation
1. Create another template
2. Name: `vendor_confirmation`
3. Subject: `Vendor Application Received - 2026 International Meeting`
4. Content:

```
Hello {{businessName}},

Thank you for applying to be a vendor at the 2026 International Meeting!

Application Details:
- Business: {{businessName}}
- Contact: {{contactName}}
- Type: {{sellingType}}

Your application is under review. We'll contact you within 5-7 business days.

Blessings,
Sarasota Gospel Temple
```

5. Note the **Template ID**

### 2.4 Get EmailJS Public Key

1. Go to **"Account"** in EmailJS dashboard
2. Find your **Public Key** (e.g., `user_abc123xyz`)
3. Save this - you'll need it next!

---

## 🔧 Step 3: Configure Your Website

### 3.1 Update Firebase Configuration

Open `config/firebase-config.js` and replace the placeholder values:

```javascript
const firebaseConfig = {
  apiKey: "AIza...", // From Firebase Console
  authDomain: "sarasota-gospel-temple.firebaseapp.com",
  projectId: "sarasota-gospel-temple",
  storageBucket: "sarasota-gospel-temple.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123"
};
```

### 3.2 Update EmailJS Configuration

In the same `firebase-config.js` file, find the EmailJS section:

```javascript
// EmailJS Configuration
const EMAILJS_PUBLIC_KEY = 'YOUR_PUBLIC_KEY_HERE'; // Replace with your EmailJS public key
const EMAILJS_SERVICE_ID = 'YOUR_SERVICE_ID'; // Replace with your service ID
const EMAILJS_TEMPLATE_IDS = {
  registration: 'YOUR_REGISTRATION_TEMPLATE_ID',
  volunteer: 'YOUR_VOLUNTEER_TEMPLATE_ID',
  vendor: 'YOUR_VENDOR_TEMPLATE_ID'
};
```

Replace with your actual values from EmailJS.

### 3.3 Update Google Maps

Open `contact.html` and find the Google Maps iframe:

```html
<iframe src="https://www.google.com/maps/embed?pb=..."></iframe>
```

**To get your embed URL:**
1. Go to [Google Maps](https://www.google.com/maps)
2. Search for: `3629 Tallevast Road, Sarasota, FL 34243`
3. Click **"Share"** → **"Embed a map"**
4. Copy the iframe code
5. Replace the existing iframe in `contact.html`

---

## 🚀 Step 4: Deploy to Wix

Since your domain is already on Wix, you have two deployment options:

### Option A: Wix Custom Code (Recommended for Full Control)

#### 4.1 Prepare Your Files

1. **Download all website files** from your repository:
   - All HTML pages (index.html, about.html, etc.)
   - `/css` folder (design-system.css, pages.css)
   - `/js` folder (all JavaScript files)
   - `/forms` folder (all three forms)
   - `/config` folder (firebase-config.js)
   - `/admin` folder (dashboard.html)
   - `/images` folder (all logos and photos)

2. **Create a ZIP file** of all folders and files

#### 4.2 Set Up Wix Custom Code

1. Log in to your **Wix Dashboard**
2. Go to **Settings** → **Custom Code**
3. Click **"+ Add Custom Code"**

**IMPORTANT:** Wix doesn't support uploading complete HTML sites directly. You have two better options:

### Option B: Deploy to Netlify and Point Your Domain (RECOMMENDED)

This gives you full control and is easier to manage:

#### 4.1 Deploy to Netlify

1. Go to [Netlify](https://www.netlify.com/) and create a free account
2. Click **"Add new site"** → **"Import an existing project"**
3. Connect your GitHub account
4. Select your repository: `VS-Code`
5. Configure build settings:
   - **Branch to deploy:** `claude/analyze-photos-design-CqXcK` (or main)
   - **Build command:** (leave empty - this is a static site)
   - **Publish directory:** `/` (root)
6. Click **"Deploy site"**
7. Wait 2-3 minutes for deployment to complete

Netlify will give you a URL like: `https://your-site-name.netlify.app`

#### 4.2 Point Your Wix Domain to Netlify

1. In Netlify, go to **"Domain settings"**
2. Click **"Add custom domain"**
3. Enter your domain (e.g., `sarasotagospeltemple.com`)
4. Netlify will provide DNS records to add

5. In your **Wix Dashboard**:
   - Go to **Domains** → **Your Domain**
   - Click **"Manage DNS Records"**
   - Click **"+ Add Record"**

6. Add these DNS records from Netlify:
   - **A Record:** Name: `@`, Value: Netlify IP address
   - **CNAME Record:** Name: `www`, Value: `your-site.netlify.app`

7. Back in Netlify, click **"Verify DNS configuration"**
8. Wait 24-48 hours for DNS propagation
9. Netlify will automatically enable HTTPS

### Option C: Host on External Server and Redirect from Wix

If you want to use another hosting provider:

#### 4.1 Alternative Hosting Options

**GitHub Pages (Free):**
1. Push your code to GitHub
2. Go to repository **Settings** → **Pages**
3. Select branch and `/root` folder
4. Click **"Save"**
5. Your site will be at `username.github.io/repository-name`

**Vercel (Free, Fast):**
1. Go to [Vercel](https://vercel.com/)
2. Import your GitHub repository
3. Deploy with one click
4. Connect your domain

**Firebase Hosting (Free):**
1. Install Firebase CLI: `npm install -g firebase-tools`
2. Run `firebase init hosting`
3. Select your Firebase project
4. Set public directory to `/`
5. Configure as single-page app: No
6. Run `firebase deploy`

#### 4.2 Redirect Wix Domain

Once hosted elsewhere:

1. In **Wix Dashboard** → **Domains**
2. Click your domain name
3. Click **"Redirect Domain"**
4. Enter your new hosting URL
5. Choose **301 Permanent Redirect**
6. Save changes

---

## 🎯 Recommended Deployment Path

**For your situation (domain on Wix, custom website):**

1. ✅ **Deploy to Netlify** (Step 4, Option B)
   - Free tier is perfect
   - Automatic HTTPS
   - Fast global CDN
   - Easy updates via GitHub
   - Professional and reliable

2. ✅ **Point Wix domain to Netlify**
   - Keep your domain registration on Wix
   - Update DNS records to point to Netlify
   - Visitors see your custom domain
   - You get full control over your website

3. ✅ **Alternative: Keep on GitHub Pages**
   - Also free and reliable
   - Slightly different DNS setup
   - Works just as well

**Why not use Wix directly?**
- Wix is designed for their drag-and-drop builder
- Your custom coded site won't work properly in Wix
- Netlify/GitHub Pages are built for custom code
- You still keep your domain name on Wix, just point it elsewhere

---

## ✅ Step 5: Testing Checklist

Before announcing the website, test everything:

### 5.1 Form Submissions

- [ ] Submit a test registration form
- [ ] Check Firestore for the submission
- [ ] Verify email confirmation was sent
- [ ] Submit a test volunteer form
- [ ] Submit a test vendor form

### 5.2 Admin Dashboard

- [ ] Navigate to `your-site.com/admin/dashboard.html`
- [ ] Log in with your admin credentials
- [ ] View all test submissions
- [ ] Export data to CSV
- [ ] Open CSV in Excel to verify format

### 5.3 Navigation

- [ ] Click through all 8 pages
- [ ] Test mobile menu on phone
- [ ] Verify 2026 Meeting banner links work
- [ ] Test all social media links
- [ ] Verify external links open in new tabs

### 5.4 Forms Accessibility

- [ ] Click 2026 Meeting banner on homepage → verify it goes to 2026-meeting.html
- [ ] Click 2026 Meeting banner on events page → verify same
- [ ] On 2026-meeting.html, click all three form cards
- [ ] Verify forms open correctly

### 5.5 Mobile Responsiveness

- [ ] Test on iPhone (Safari)
- [ ] Test on Android phone (Chrome)
- [ ] Test on tablet (iPad)
- [ ] Verify navigation menu works
- [ ] Verify forms are usable on mobile

### 5.6 Contact Page

- [ ] Verify Google Map loads correctly
- [ ] Test contact form submission
- [ ] Verify all social media links work
- [ ] Check phone number is clickable on mobile

---

## 📊 Step 6: Data Management

### 6.1 Accessing Form Submissions

**Option 1: Admin Dashboard**
- Go to `your-site.com/admin/dashboard.html`
- Log in with admin credentials
- View and export data

**Option 2: Firebase Console**
- Go to Firebase Console → Firestore
- Navigate to collections: `registrations`, `volunteers`, `vendors`
- View submissions directly

### 6.2 Exporting Data for Analytics

1. Use admin dashboard **"Export to Excel"** buttons
2. Open CSV files in Excel or Google Sheets
3. Analyze data:
   - Registration counts by church
   - Volunteer committee preferences
   - Vendor applications by type

### 6.3 Email Notifications

All form submissions automatically send:
- Confirmation email to submitter
- Notification email to admin (`sarasotagospel@gmail.com`)

**To change notification email:**
- Edit EmailJS templates
- Add admin email in CC/BCC field

---

## 🔒 Security Best Practices

### 6.1 Protect Admin Dashboard

The admin dashboard is at `/admin/dashboard.html`. To add extra security:

**Option 1: Netlify Password Protection** (Easiest - if using Netlify)
1. In Netlify, go to **"Site settings"** → **"Access control"**
2. Enable **"Password protection"**
3. Set a password for `/admin/*` path

**Option 2: Vercel Password Protection** (if using Vercel)
1. Create a `vercel.json` file with basic auth configuration
2. Set environment variables for username/password

**Option 3: Move Admin to Separate Subdomain**
1. Deploy admin dashboard to `admin.sarasotagospeltemple.com`
2. Apply password protection only to admin subdomain

**Note:** Firebase Authentication already protects the dashboard - only logged-in admins can view data

### 6.2 Firebase Security

Your current Firestore rules are secure:
- Anyone can submit forms (create only)
- Only authenticated admins can read/update/delete

**To add admin emails as environment variable:**
1. In Firebase Console → Authentication
2. Only add trusted admin emails as users
3. Never share admin credentials

### 6.3 API Key Security

Your Firebase API key in `firebase-config.js` is safe to expose publicly because:
- Firestore security rules protect your data
- API key is restricted to your domain in Firebase Console

**To restrict API key** (recommended):
1. Go to Google Cloud Console
2. Find your API key
3. Add **"HTTP referrers"** restriction:
   - `https://your-domain.com/*`
   - `https://your-netlify-subdomain.netlify.app/*`

---

## 🎨 Content Updates

### 7.1 Adding Photos to Gallery

1. Create folders in `/images/gallery/`:
   - `sunday-services/`
   - `youth-ministry/`
   - `special-events/`
   - `community-outreach/`
   - `music-ministry/`
   - `2026-meeting/`

2. Add photos to each folder

3. Update `gallery.html`:

```html
<div class="album-card" onclick="window.location.href='gallery/sunday-services.html'">
  <div class="album-cover" style="background-image: url('images/gallery/sunday-services/cover.jpg')"></div>
  <h3>Sunday Services</h3>
  <p>📷 24 Photos</p>
</div>
```

4. Create individual gallery pages for each album

**Recommendation:** Use [Netlify CMS](https://www.netlifycms.org/) for easy photo uploads without coding.

### 7.2 Updating Church Information

All church info is in these files:
- **Service times:** `contact.html`, `index.html`
- **Address:** `contact.html`, footer in all pages
- **Social links:** Footer in all pages, `events.html`
- **Elder photos:** `about.html` (replace 👨‍👩 emoji with actual photos)

### 7.3 Adding Events to Calendar

Edit `events.html` and add event cards:

```html
<div class="event-card">
  <div class="event-date">
    <div class="event-month">MAR</div>
    <div class="event-day">15</div>
  </div>
  <div class="event-info">
    <h4>Youth Conference</h4>
    <p>📍 Sarasota Gospel Temple</p>
    <p>⏰ 6:00 PM - 9:00 PM</p>
  </div>
</div>
```

---

## 📈 Analytics (Optional)

### 8.1 Add Google Analytics

1. Create Google Analytics 4 property
2. Get measurement ID (e.g., `G-XXXXXXXXXX`)
3. Add to every HTML page in `<head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### 8.2 Track Form Submissions

Add event tracking to form submissions:

```javascript
// After successful submission
gtag('event', 'form_submission', {
  'event_category': 'Forms',
  'event_label': 'Registration Form',
  'value': 1
});
```

---

## 🐛 Troubleshooting

### Form Not Submitting

**Problem:** Form shows error on submission

**Solutions:**
1. Check browser console for errors (F12 → Console tab)
2. Verify Firebase configuration is correct
3. Check Firestore security rules
4. Ensure Firebase scripts are loading (check Network tab)

### Email Not Sending

**Problem:** Form submits but no email received

**Solutions:**
1. Check EmailJS dashboard for usage limits (200/month on free tier)
2. Verify template IDs are correct
3. Check spam folder
4. Test email template in EmailJS dashboard

### Admin Dashboard Login Fails

**Problem:** Cannot log into admin dashboard

**Solutions:**
1. Verify email/password in Firebase Authentication
2. Check browser console for errors
3. Clear browser cache and cookies
4. Try incognito/private browsing mode

### Map Not Loading

**Problem:** Google Map on contact page shows error

**Solutions:**
1. Verify iframe embed code is correct
2. Check Google Maps API restrictions
3. Try regenerating embed code from Google Maps

---

## 🚀 Go-Live Checklist

Before announcing the website publicly:

- [ ] All Firebase credentials configured
- [ ] All EmailJS templates tested
- [ ] Forms tested with real submissions
- [ ] Admin dashboard accessible and working
- [ ] Data export to CSV tested
- [ ] All 8 pages live and accessible
- [ ] 2026 Meeting banner links to forms
- [ ] Mobile responsive on multiple devices
- [ ] All social media links verified
- [ ] Google Map loading correctly and fills frame properly
- [ ] Custom domain configured (DNS records updated)
- [ ] HTTPS enabled (automatic with most hosting providers)
- [ ] Browser testing (Chrome, Safari, Firefox)
- [ ] Test email confirmations received
- [ ] Admin login credentials saved securely
- [ ] Backup plan for form data established
- [ ] DNS propagation complete (can take 24-48 hours)

---

## 📞 Support Resources

### Firebase
- [Firebase Documentation](https://firebase.google.com/docs)
- [Firestore Security Rules](https://firebase.google.com/docs/firestore/security/get-started)

### EmailJS
- [EmailJS Documentation](https://www.emailjs.com/docs/)
- [Template Guide](https://www.emailjs.com/docs/user-guide/creating-email-template/)

### Hosting Platforms
- [Netlify Documentation](https://docs.netlify.com/)
- [Netlify Custom Domains](https://docs.netlify.com/domains-https/custom-domains/)
- [GitHub Pages Guide](https://docs.github.com/en/pages)
- [Vercel Documentation](https://vercel.com/docs)
- [Firebase Hosting](https://firebase.google.com/docs/hosting)

### Wix Domain Management
- [Wix DNS Records](https://support.wix.com/en/article/managing-dns-records-in-your-wix-account)
- [Wix Domain Redirect](https://support.wix.com/en/article/redirecting-your-domain)

### Additional Help
- Email: sarasotagospel@gmail.com
- Repository: [Your GitHub Repository]

---

## 🎉 Your Deployment Roadmap

Your complete custom website is ready for launch! You now have:

✅ Professional website with 8 pages
✅ Custom forms with your own database
✅ Complete data ownership and analytics
✅ Mobile responsive design
✅ Email notifications
✅ Admin dashboard with export capability
✅ Brand-consistent styling throughout
✅ Google Maps properly fitted in frame

---

## 📝 Step-by-Step Launch Plan for Wix Domain Owners

### Phase 1: Configure Services (30-45 minutes)

**Step 1: Firebase Setup**
1. Create Firebase project at https://console.firebase.google.com/
2. Enable Firestore Database (production mode)
3. Add security rules from Section 1.3
4. Enable Email/Password authentication
5. Create admin user account
6. Copy Firebase configuration values

**Step 2: EmailJS Setup**
1. Create account at https://www.emailjs.com/
2. Connect your Gmail account
3. Create three email templates:
   - Registration confirmation
   - Volunteer confirmation
   - Vendor confirmation
4. Save Service ID and Template IDs

**Step 3: Update Configuration Files**
1. Open `config/firebase-config.js`
2. Replace Firebase values with your actual credentials
3. Replace EmailJS values with your actual IDs
4. Save the file
5. Commit and push changes to GitHub

---

### Phase 2: Deploy Your Website (15-30 minutes)

**Recommended: Netlify Deployment**

1. **Sign up for Netlify**
   - Go to https://www.netlify.com/
   - Create free account with GitHub

2. **Import Your Repository**
   - Click "Add new site" → "Import an existing project"
   - Connect GitHub
   - Select your `VS-Code` repository
   - Branch: `claude/analyze-photos-design-CqXcK` (or main)
   - Build command: (leave empty)
   - Publish directory: `/`
   - Click "Deploy site"

3. **Wait for Deployment**
   - Takes 2-3 minutes
   - Netlify gives you a URL like: `https://random-name-123.netlify.app`
   - Test this URL to make sure everything works!

---

### Phase 3: Connect Your Wix Domain (24-48 hours)

**Step 1: Add Custom Domain in Netlify**
1. In Netlify, go to "Domain settings"
2. Click "Add custom domain"
3. Enter your domain: `yourdomain.com` (replace with your actual domain)
4. Netlify will show you DNS records to add

**Step 2: Update DNS in Wix**
1. Log in to **Wix Dashboard**
2. Go to **Domains** → Click your domain name
3. Click **"Manage DNS Records"**
4. Click **"+ Add Record"**

5. **Add A Record** (for root domain):
   - Type: `A`
   - Name: `@`
   - Value: `75.2.60.5` (Netlify's IP - verify current IP in Netlify)
   - TTL: `3600` (1 hour)

6. **Add CNAME Record** (for www):
   - Type: `CNAME`
   - Name: `www`
   - Value: `your-site-name.netlify.app` (from Netlify)
   - TTL: `3600`

7. **Save changes**

**Step 3: Verify in Netlify**
1. Back in Netlify, click "Verify DNS configuration"
2. Wait for verification (can take up to 48 hours)
3. Once verified, Netlify enables automatic HTTPS

**Important:** DNS changes take 24-48 hours to fully propagate worldwide. Your old Wix site will show until then.

---

### Phase 4: Testing (1 hour)

Once DNS propagates and your domain shows the new site:

**Test Forms:**
- [ ] Submit registration form → Check Firestore + Email
- [ ] Submit volunteer form → Check Firestore + Email
- [ ] Submit vendor form → Check Firestore + Email
- [ ] Test contact form

**Test Admin Dashboard:**
- [ ] Go to `yourdomain.com/admin/dashboard.html`
- [ ] Log in with Firebase admin credentials
- [ ] View submissions
- [ ] Export to CSV and open in Excel

**Test Navigation:**
- [ ] Click through all 8 pages
- [ ] Test mobile menu on phone
- [ ] Verify 2026 Meeting banner links
- [ ] Click all social media links
- [ ] Test on iPhone, Android, tablet

**Test Contact Page:**
- [ ] Verify Google Map loads and fills frame properly
- [ ] Click phone number on mobile
- [ ] Test social links

---

### Phase 5: Go Live! 🎉

1. **Announce to Congregation**
   - Share website URL
   - Promote 2026 Meeting registration
   - Encourage volunteer signups

2. **Monitor Submissions**
   - Check admin dashboard daily
   - Respond to form submissions
   - Export data for planning

3. **Future Updates**
   - Push changes to GitHub
   - Netlify auto-deploys in 2-3 minutes
   - No manual upload needed!

---

## ⏱️ Total Time Estimate

- Firebase Setup: 20 minutes
- EmailJS Setup: 15 minutes
- Config File Updates: 10 minutes
- Netlify Deployment: 15 minutes
- Wix DNS Update: 10 minutes
- **Total Active Work: ~70 minutes**
- DNS Propagation Wait: 24-48 hours (automatic)
- Testing: 1 hour

**You can complete all setup in one afternoon, then wait for DNS to propagate!**

---

## 🆘 Quick Troubleshooting

**"My domain still shows old Wix site"**
- DNS takes 24-48 hours to propagate
- Check if you added both A and CNAME records correctly
- Clear browser cache

**"Forms don't submit"**
- Check browser console (F12) for errors
- Verify Firebase config values are correct
- Check Firestore security rules

**"No emails received"**
- Check EmailJS dashboard for errors
- Verify you're under 200 emails/month limit (free tier)
- Check spam folder

**"Can't log into admin dashboard"**
- Verify email/password in Firebase Authentication
- Clear browser cache/cookies
- Try incognito mode

---

## 📞 Need Help?

If you get stuck:
1. Check the detailed sections above
2. Review error messages in browser console (F12)
3. Check Firebase Console for issues
4. Email: sarasotagospel@gmail.com

---

*This guide was created for Sarasota Gospel Temple - 2026 International Meeting Website*
*Last updated: February 2026*
*Deployment Platform: Netlify (recommended) | Domain Management: Wix*
