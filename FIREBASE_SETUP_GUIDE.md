# Firebase Functions Configuration Guide

This guide will help you configure Firebase Functions with Google Sheets integration and EmailJS for the Sarasota Gospel Temple website.

## Prerequisites

Before starting, ensure you have:
- A Firebase project created at [console.firebase.google.com](https://console.firebase.google.com/)
- Admin access to your Firebase project
- Node.js installed on your machine

## Step 1: Install Firebase CLI

```bash
# Install Firebase CLI globally
npm install -g firebase-tools

# Login to Firebase
firebase login

# Initialize Firebase in your project (if not already done)
cd /Users/liltrizzytreezy/GitHub/VS-Code
firebase use --add
```

## Step 2: Create Google Service Account

Your Firebase Functions need a service account to access Google Sheets API.

### 2.1 Create Service Account in Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your Firebase project (it should be listed there)
3. Navigate to **IAM & Admin** → **Service Accounts**
4. Click **Create Service Account**
5. Enter details:
   - **Name:** `firebase-sheets-sync`
   - **Description:** `Service account for syncing Firebase data to Google Sheets`
6. Click **Create and Continue**
7. Grant these roles:
   - **Editor** (for Sheets access)
8. Click **Continue**, then **Done**

### 2.2 Create and Download Service Account Key

1. Find your newly created service account in the list
2. Click on the service account email
3. Go to **Keys** tab
4. Click **Add Key** → **Create new key**
5. Choose **JSON** format
6. Click **Create**
7. The JSON file will download automatically

### 2.3 Save the Service Account Key

```bash
# Move the downloaded file to a secure location (NOT in your repo!)
# Example: Save it in your home directory
mv ~/Downloads/your-project-name-*.json ~/firebase-service-account.json

# IMPORTANT: Never commit this file to Git!
# It's already in your .gitignore as *service-account*.json
```

## Step 3: Enable Google Sheets API

1. In [Google Cloud Console](https://console.cloud.google.com/)
2. Go to **APIs & Services** → **Library**
3. Search for **Google Sheets API**
4. Click on it and press **Enable**

## Step 4: Share Google Sheets with Service Account

You need to share your Google Sheets with the service account email.

1. Open each of your three Google Sheets:
   - [Registrations Sheet](https://docs.google.com/spreadsheets/d/1q7vxkgof14p6OpHehTySIU6c0qNpbencA6E09agYJTg)
   - [Volunteers Sheet](https://docs.google.com/spreadsheets/d/1T45QcAsY7m5SO8gSQKTvHI_PFFa4qx1x6dwW3iwG0s0)
   - [Vendors Sheet](https://docs.google.com/spreadsheets/d/1V6G2KN1vvTB5Ng249rg9K6ijbUT7tou_jaE9ygALxeM)

2. For each sheet:
   - Click **Share** button
   - Add the service account email (looks like: `firebase-sheets-sync@your-project.iam.gserviceaccount.com`)
   - Give it **Editor** permissions
   - Click **Done**

## Step 5: Configure Firebase Functions

Now set all the configuration values at once:

```bash
# Navigate to your project
cd /Users/liltrizzytreezy/GitHub/VS-Code

# Set all configurations (replace the path with your actual service account file location)
firebase functions:config:set \
  google.credentials="$(cat ~/firebase-service-account.json)" \
  sheets.registrations_id="1q7vxkgof14p6OpHehTySIU6c0qNpbencA6E09agYJTg" \
  sheets.volunteers_id="1T45QcAsY7m5SO8gSQKTvHI_PFFa4qx1x6dwW3iwG0s0" \
  sheets.vendors_id="1V6G2KN1vvTB5Ng249rg9K6ijbUT7tou_jaE9ygALxeM"
```

## Step 6: Configure EmailJS (if not already done)

Your functions also need EmailJS configuration for sending email notifications:

```bash
# Get these values from your EmailJS dashboard at emailjs.com
firebase functions:config:set \
  emailjs.service_id="YOUR_EMAILJS_SERVICE_ID" \
  emailjs.public_key="YOUR_EMAILJS_PUBLIC_KEY" \
  emailjs.private_key="YOUR_EMAILJS_PRIVATE_KEY"
```

### How to Get EmailJS Credentials:

1. Go to [EmailJS Dashboard](https://dashboard.emailjs.com/)
2. **Service ID:** Go to Email Services → Your service → Copy the Service ID
3. **Public Key:** Go to Account → Copy the Public Key
4. **Private Key:** Go to Account → Copy the Private Key (also called API Key)

## Step 7: Verify Configuration

Check that all configurations are set correctly:

```bash
firebase functions:config:get
```

You should see output like:
```json
{
  "google": {
    "credentials": "{\"type\":\"service_account\"...}"
  },
  "sheets": {
    "registrations_id": "1q7vxkgof14p6OpHehTySIU6c0qNpbencA6E09agYJTg",
    "volunteers_id": "1T45QcAsY7m5SO8gSQKTvHI_PFFa4qx1x6dwW3iwG0s0",
    "vendors_id": "1V6G2KN1vvTB5Ng249rg9K6ijbUT7tou_jaE9ygALxeM"
  },
  "emailjs": {
    "service_id": "...",
    "public_key": "...",
    "private_key": "..."
  }
}
```

## Step 8: Install Dependencies and Deploy

```bash
# Navigate to functions directory
cd functions

# Install dependencies
npm install

# Go back to root
cd ..

# Deploy functions to Firebase
firebase deploy --only functions
```

## Step 9: Test the Integration

1. Visit your website
2. Submit a test form (registration, volunteer, or vendor)
3. Check that:
   - Data appears in Firebase Firestore
   - Email confirmation is sent
   - Data is synced to the appropriate Google Sheet

## Troubleshooting

### Error: "firebase: command not found"
```bash
# Install Firebase CLI globally
npm install -g firebase-tools
```

### Error: "Failed to get Firebase project"
```bash
# Make sure you're logged in
firebase login

# Select your project
firebase use --add
```

### Error: "Permission denied" when accessing Sheets
- Make sure you shared each Google Sheet with the service account email
- Verify the service account has Editor permissions
- Check that Google Sheets API is enabled in Google Cloud Console

### Error: "EmailJS not configured"
- Run `firebase functions:config:get` to verify EmailJS settings are present
- Re-run the EmailJS configuration command if needed
- Deploy functions again after setting config

## Local Development

For local testing with Firebase emulator:

```bash
# Download the config to local file
firebase functions:config:get > functions/.runtimeconfig.json

# Start emulator
npm run serve

# IMPORTANT: Never commit .runtimeconfig.json to Git!
# It's already gitignored
```

## Security Best Practices

✅ **DO:**
- Keep service account JSON file outside your Git repository
- Use environment variables for sensitive data
- Regularly rotate service account keys
- Limit service account permissions to minimum required

❌ **DON'T:**
- Commit service account JSON to Git
- Share service account credentials publicly
- Use overly permissive IAM roles
- Hardcode credentials in source code

## Summary of Required Configurations

| Config Key | Description | Where to Get It |
|------------|-------------|-----------------|
| `google.credentials` | Service account JSON | Google Cloud Console → IAM → Service Accounts |
| `sheets.registrations_id` | Registrations sheet ID | Already set (from URL) |
| `sheets.volunteers_id` | Volunteers sheet ID | Already set (from URL) |
| `sheets.vendors_id` | Vendors sheet ID | Already set (from URL) |
| `emailjs.service_id` | EmailJS service | EmailJS Dashboard → Email Services |
| `emailjs.public_key` | EmailJS public key | EmailJS Dashboard → Account |
| `emailjs.private_key` | EmailJS private key | EmailJS Dashboard → Account |

---

**Need help?** Check the [Firebase documentation](https://firebase.google.com/docs/functions/config-env) for more details on environment configuration.

*Last updated: February 2026*
