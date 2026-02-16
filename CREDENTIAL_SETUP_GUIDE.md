# Credential Setup Guide

This guide will help you configure all the credentials needed for the Sarasota Gospel Temple website to work properly.

## 🚨 IMPORTANT: The Problem

Your terminal wasn't reading credential commands because:
1. **Firebase CLI was not installed** - Now fixed! ✅
2. **No `.env` file existed** - Now created! ✅
3. **Credentials were hardcoded** - Now we use environment variables! ✅

---

## 📋 Prerequisites

Before starting, make sure you have:
- ✅ Node.js installed (already present)
- ✅ Firebase CLI installed (just installed)
- ✅ Access to your Firebase, EmailJS, and Google Cloud accounts

---

## 🎯 Quick Start (Recommended)

### Step 1: Edit Your `.env` File

Open the `.env` file in the root directory and replace the placeholder values with your actual credentials:

```bash
# Open in your editor
nano .env
# or
vim .env
# or use any text editor
```

Replace values like `your_firebase_api_key_here` with your actual credentials.

### Step 2: Run the Setup Script

```bash
npm run setup
```

This will:
- ✅ Read your credentials from `.env`
- ✅ Generate `config/firebase-config.js` with your Firebase credentials
- ✅ Generate `config/google-sheets-config.js` with your Google Sheets credentials
- ✅ Optionally configure Firebase Functions

### Step 3: Login to Firebase (if needed)

```bash
npm run firebase:login
```

### Step 4: Select Your Firebase Project

```bash
npm run firebase:init
```

Select `sarasota-gospel-temple` from the list.

### Step 5: Configure Firebase Functions

```bash
npm run setup:firebase
```

This sets up the backend credentials for Firebase Functions.

---

## 📚 Detailed Instructions

### Where to Get Your Credentials

#### 🔥 Firebase Credentials

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project: `sarasota-gospel-temple`
3. Click the gear icon ⚙️ → Project Settings
4. Scroll down to "Your apps" → Select your web app
5. Copy the configuration values:
   - `FIREBASE_API_KEY`
   - `FIREBASE_AUTH_DOMAIN`
   - `FIREBASE_PROJECT_ID`
   - `FIREBASE_STORAGE_BUCKET`
   - `FIREBASE_MESSAGING_SENDER_ID`
   - `FIREBASE_APP_ID`
   - `FIREBASE_MEASUREMENT_ID`

#### 📧 EmailJS Credentials

1. Go to [EmailJS Dashboard](https://dashboard.emailjs.com/)
2. Navigate to "Email Services"
3. Copy your `EMAILJS_SERVICE_ID`
4. Go to "Account" → "API Keys"
5. Copy your `EMAILJS_PUBLIC_KEY`
6. For backend: Copy your `EMAILJS_PRIVATE_KEY` (different from public key!)

#### 📊 Google Sheets API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Navigate to "APIs & Services" → "Credentials"
4. Copy your `GOOGLE_SHEETS_API_KEY`
5. Copy your OAuth 2.0 `GOOGLE_SHEETS_CLIENT_ID`
6. Get your spreadsheet IDs from the URLs:
   - Registration sheet URL: `https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit`
   - Copy the ID for `GOOGLE_SHEETS_REGISTRATIONS_ID`
   - Repeat for volunteers and vendors sheets

#### 🔑 Service Account (for Firebase Functions)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to "IAM & Admin" → "Service Accounts"
3. Create or select a service account
4. Click "Keys" → "Add Key" → "Create new key"
5. Choose JSON format
6. Download the JSON file
7. Copy the ENTIRE contents and paste into `GOOGLE_SERVICE_ACCOUNT_JSON` in `.env`

---

## 🛠️ Available Commands

After setup, you can use these npm commands:

```bash
# Credential Setup
npm run setup              # Setup from .env file (recommended)
npm run setup:interactive  # Interactive setup (asks questions)
npm run setup:firebase     # Only configure Firebase Functions

# Firebase Commands
npm run firebase:login     # Login to Firebase
npm run firebase:init      # Select Firebase project
npm run firebase:deploy    # Deploy everything
npm run firebase:deploy:hosting    # Deploy website only
npm run firebase:deploy:functions  # Deploy functions only
npm run firebase:config:get        # View current Firebase config
npm run firebase:serve     # Test locally

# Help
npm run help              # Show all commands
```

---

## 🔍 Manual Firebase Functions Configuration

If you prefer to set Firebase Functions config manually:

```bash
# EmailJS Configuration
firebase functions:config:set emailjs.service_id="your_service_id"
firebase functions:config:set emailjs.private_key="your_private_key"

# Google Sheets Configuration
firebase functions:config:set sheets.registrations_id="your_registrations_id"
firebase functions:config:set sheets.volunteers_id="your_volunteers_id"
firebase functions:config:set sheets.vendors_id="your_vendors_id"

# Google Service Account (paste JSON as single line)
firebase functions:config:set google.credentials='{"type":"service_account",...}'

# View current configuration
firebase functions:config:get
```

---

## 🚨 Troubleshooting

### "firebase: command not found"

**Solution:** Firebase CLI is now installed globally. Restart your terminal.

```bash
# Verify installation
firebase --version
```

### "Error: No credentials found in .env file"

**Solution:** Edit `.env` and replace placeholder values with real credentials.

```bash
nano .env
```

Make sure there are no lines with `your_` or `your-` in the values.

### "Permission denied when running setup script"

**Solution:** The script is already executable, but you can run it with node:

```bash
node setup-credentials.js
```

### "Firebase login required"

**Solution:** Login to Firebase:

```bash
firebase login
```

### "No Firebase project selected"

**Solution:** Select your project:

```bash
firebase use --add
```

Then choose `sarasota-gospel-temple` from the list.

### Config files not updating

**Solution:** The setup script overwrites the config files. If you made manual changes, they will be lost. Always edit `.env` instead.

---

## 🔒 Security Best Practices

### ✅ DO:
- ✅ Keep `.env` file private (it's in `.gitignore`)
- ✅ Use the setup script to generate config files
- ✅ Rotate credentials if they're exposed
- ✅ Use Firebase Security Rules to protect data

### ❌ DON'T:
- ❌ Commit `.env` to git
- ❌ Share credentials in chat or email
- ❌ Hardcode credentials in JavaScript files
- ❌ Push service account JSON to git

---

## 📖 Example `.env` File

Here's what your `.env` file should look like (with real values):

```env
# Firebase Configuration
FIREBASE_API_KEY=REDACTED_FIREBASE_API_KEY_1
FIREBASE_AUTH_DOMAIN=sarasota-gospel-temple.firebaseapp.com
FIREBASE_PROJECT_ID=sarasota-gospel-temple
FIREBASE_STORAGE_BUCKET=sarasota-gospel-temple.firebasestorage.app
FIREBASE_MESSAGING_SENDER_ID=868460102497
FIREBASE_APP_ID=1:868460102497:web:1b805b72d00801971c7b20
FIREBASE_MEASUREMENT_ID=G-CEY9WE2C47

# EmailJS Configuration
EMAILJS_SERVICE_ID=REDACTED_EMAILJS_SERVICE_ID
EMAILJS_PUBLIC_KEY=REDACTED_EMAILJS_PUBLIC_KEY
EMAILJS_PRIVATE_KEY=your_private_key_here

# Google Sheets Configuration
GOOGLE_SHEETS_API_KEY=REDACTED_GOOGLE_SHEETS_API_KEY
GOOGLE_SHEETS_CLIENT_ID=REDACTED_GOOGLE_CLIENT_ID
GOOGLE_SHEETS_REGISTRATIONS_ID=1q7vxkgof14p6OpHehTySIU6c0qNpbencA6E09agYJTg
GOOGLE_SHEETS_VOLUNTEERS_ID=1T45QcAsY7m5SO8gSQKTvHI_PFFa4qx1x6dwW3iwG0s0
GOOGLE_SHEETS_VENDORS_ID=1V6G2KN1vvTB5Ng249rg9K6ijbUT7tou_jaE9ygALxeM

# Google Service Account (for Firebase Functions)
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account","project_id":"sarasota-gospel-temple",...}
```

---

## 🎬 Complete Setup Workflow

Here's the complete workflow from start to finish:

```bash
# 1. Edit your credentials
nano .env

# 2. Run setup script
npm run setup

# 3. Login to Firebase (if not already logged in)
npm run firebase:login

# 4. Select your project
npm run firebase:init

# 5. Configure Firebase Functions
npm run setup:firebase

# 6. Test locally
npm run firebase:serve

# 7. Deploy to production
npm run firebase:deploy
```

---

## 📞 Need Help?

If you're still having issues:

1. Check that `.env` has real values (not placeholders)
2. Verify Firebase CLI is installed: `firebase --version`
3. Make sure you're logged in: `firebase login`
4. Check your Firebase project: `firebase projects:list`
5. View current config: `npm run firebase:config:get`

---

## ✅ Verification Checklist

Before deploying, verify:

- [ ] `.env` file exists with real credentials
- [ ] `config/firebase-config.js` was generated
- [ ] `config/google-sheets-config.js` was generated
- [ ] Firebase CLI is installed
- [ ] Logged into Firebase
- [ ] Correct Firebase project selected
- [ ] Firebase Functions config is set
- [ ] Tested forms locally
- [ ] No credentials in git history

---

**Last Updated:** February 11, 2026
**Script Version:** 1.0.0
