# Netlify Deployment Guide

## Quick Start Checklist

### ✅ Prerequisites
- [ ] GitHub repository with latest code
- [ ] Firebase project set up
- [ ] EmailJS account configured
- [ ] Google Sheets created and IDs noted
- [ ] Netlify account (free tier is fine)

### 🚀 Deployment Steps

## Step 1: Connect Repository to Netlify

1. Go to https://app.netlify.com/
2. Click **"Add new site"** → **"Import an existing project"**
3. Choose **GitHub** and authorize Netlify
4. Select repository: **TheTracyTimes/VS-Code**
5. Configure build settings:
   - **Branch to deploy:** `claude/analyze-photos-design-CqXcK` (or your main branch)
   - **Build command:** `bash build.sh` (already set in netlify.toml)
   - **Publish directory:** `public` (already set in netlify.toml)
6. Click **"Deploy site"**

## Step 2: Configure Environment Variables

Go to **Site settings** → **Environment variables** and add these:

### Firebase Configuration
```
FIREBASE_API_KEY=your_firebase_api_key
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project.firebasestorage.app
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_app_id
FIREBASE_MEASUREMENT_ID=your_measurement_id
```

### EmailJS Configuration
```
EMAILJS_SERVICE_ID=your_service_id
EMAILJS_PUBLIC_KEY=your_public_key
EMAILJS_TEMPLATE_REGISTRATION=registration_confirmation
EMAILJS_TEMPLATE_VENDOR=vendor_confirmation
EMAILJS_TEMPLATE_VOLUNTEER=volunteer_confirmation
```

### Google Sheets Configuration
```
GOOGLE_SHEETS_API_KEY=your_google_api_key
GOOGLE_SHEETS_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_SHEETS_REGISTRATIONS_ID=1q7vxkgof14p6OpHehTySIU6c0qNpbencA6E09agYJTg
GOOGLE_SHEETS_VOLUNTEERS_ID=1T45QcAsY7m5SO8gSQKTvHI_PFFa4qx1x6dwW3iwG0s0
GOOGLE_SHEETS_VENDORS_ID=1V6G2KN1vvTB5Ng249rg9K6ijbUT7tou_jaE9ygALxeM
```

### How to Add Each Variable

For each environment variable:
1. Click **"Add a variable"**
2. Select **"Add a single variable"**
3. Set:
   - **Key:** Variable name (e.g., `FIREBASE_API_KEY`)
   - **Values:** The actual value
   - **Scopes:** Select all (Production, Deploy previews, Branch deploys)
4. Click **"Create variable"**

## Step 3: Trigger Deployment

After adding all environment variables:
1. Go to **Deploys** tab
2. Click **"Trigger deploy"** → **"Deploy site"**
3. Wait for build to complete (usually 1-2 minutes)

## Step 4: Verify Deployment

Once deployed, test your site:

### Test Forms
1. Visit `https://your-site.netlify.app/forms/registration.html`
2. Open browser console (F12)
3. Check for these success messages:
   ```
   Firebase initialized successfully
   EmailJS initialized
   Google API Client initialized successfully
   ```

### Submit Test Form
1. Fill out and submit a form
2. Check that:
   - [ ] Form submits successfully
   - [ ] Confirmation email is received
   - [ ] Data appears in Firebase Firestore
   - [ ] Data appears in Google Sheet

## Step 5: Configure Custom Domain (Optional)

If you want to use your own domain:

1. Go to **Domain settings** → **Add custom domain**
2. Enter your domain name
3. Follow Netlify's DNS configuration instructions
4. Update your domain's DNS records:
   - Add **CNAME** record pointing to your Netlify subdomain
   - Or add **A** record pointing to Netlify's load balancer IP

## Troubleshooting

### Issue: "Config files not found"
**Solution:** Make sure `build.sh` has execute permissions and all environment variables are set in Netlify.

### Issue: "Firebase initialization error"
**Solution:** Check that all Firebase environment variables are correct in Netlify settings.

### Issue: "EmailJS not sending emails"
**Possible causes:**
1. Template IDs don't match those in EmailJS dashboard
2. EmailJS service is not configured correctly
3. Domain not authorized in EmailJS settings

**Solution:**
- Verify template IDs: `registration_confirmation`, `vendor_confirmation`, `volunteer_confirmation`
- Check EmailJS dashboard at https://dashboard.emailjs.com/

### Issue: "Google Sheets not syncing"
**Possible causes:**
1. Google Sheets API not enabled
2. API key restrictions too strict
3. OAuth consent screen not configured

**Solution:**
- Enable Google Sheets API in Google Cloud Console
- Configure API key restrictions (HTTP referrer: your Netlify domain)
- Set up OAuth consent screen

### Issue: Build fails with "Command not found: bash"
**Solution:** This shouldn't happen on Netlify, but if it does:
- Check netlify.toml is in root directory
- Verify build command is correct

## Continuous Deployment

Netlify automatically deploys when you push to your connected branch:

```bash
# Make changes
git add .
git commit -m "Update site"
git push origin claude/analyze-photos-design-CqXcK

# Netlify automatically builds and deploys
```

## Security Checklist

After deployment, verify security settings:

### Firebase Security
- [ ] Firestore security rules are configured (not wide-open)
- [ ] Authentication is properly configured
- [ ] Test that unauthorized access is blocked

### API Restrictions
- [ ] Firebase API key has domain restrictions (optional but recommended)
- [ ] Google Sheets API key restricted by HTTP referrer
- [ ] EmailJS has domain restrictions enabled

### Google Cloud Console
1. Go to **APIs & Services** → **Credentials**
2. Edit API key
3. Set **Application restrictions**:
   - HTTP referrers (web sites)
   - Add your Netlify URL: `https://your-site.netlify.app/*`
4. Set **API restrictions**:
   - Restrict key
   - Select only: Google Sheets API

### EmailJS Dashboard
1. Go to https://dashboard.emailjs.com/
2. Click on your service
3. Settings → **Allowed domains**
4. Add your Netlify domain

## Monitoring

### Set Up Alerts
1. **Firebase**: Console → Usage → Set up budget alerts
2. **Google Cloud**: Billing → Budget alerts
3. **EmailJS**: Check usage regularly (free tier: 200 emails/month)

### Monitor Logs
- **Netlify Logs**: Site → Functions → View logs
- **Firebase Logs**: Console → Firestore → Usage tab
- **Browser Console**: Check for JavaScript errors

## Environment Variables Reference

Copy these exact values from your local `.env` file:

```bash
# From your local .env file
cat .env | grep -v '^#' | grep -v '^$'
```

Then add each one to Netlify's environment variables section.

## Need Help?

- **Netlify Docs**: https://docs.netlify.com/
- **Firebase Docs**: https://firebase.google.com/docs
- **EmailJS Docs**: https://www.emailjs.com/docs/
- **Contact**: sarasotagospel@gmail.com or 941-800-5211
