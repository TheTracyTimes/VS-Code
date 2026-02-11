# 🚀 Quick Start - Credential Setup

## Your Problem: Terminal Not Reading Credentials

**SOLVED!** ✅

### What Was Wrong:
1. ❌ Firebase CLI was not installed
2. ❌ No way to configure Firebase Functions from terminal

### What's Fixed:
1. ✅ Firebase CLI installed globally
2. ✅ `.env` file created for Firebase Functions configuration
3. ✅ Setup script created for future credential management
4. ✅ Package.json with helpful npm commands

**Note:** Your client-side credentials are already configured in `config/firebase-config.js` and `config/google-sheets-config.js`. The `.env` file and setup script are for Firebase Functions (backend) configuration.

---

## 🎯 How To Use Firebase CLI (3 Simple Steps)

### Step 1: Login to Firebase

Your terminal can now use Firebase commands:

```bash
firebase login
```

### Step 2: Select Your Project

```bash
firebase use --add
```

Select `sarasota-gospel-temple` from the list.

### Step 3: Configure Firebase Functions Backend

To configure Firebase Functions (backend) with environment variables:

```bash
# First, add your EmailJS private key and service account JSON to .env
nano .env

# Then configure Firebase Functions
firebase functions:config:set emailjs.service_id="your_service_id"
firebase functions:config:set emailjs.private_key="your_private_key"

# Or use the helper script
npm run setup:firebase
```

---

## 📋 Available Commands

```bash
# Firebase CLI Commands (Now Working!)
firebase login                    # Login to Firebase
firebase use --add                # Select Firebase project
firebase deploy                   # Deploy everything
firebase functions:config:set     # Set backend config
firebase functions:config:get     # View backend config

# Helper Scripts
npm run firebase:login            # Login to Firebase
npm run firebase:deploy           # Deploy everything
npm run setup:firebase            # Configure Functions from .env
npm run help                      # Show all commands
```

---

## 🔍 Understanding Your Credentials

Your project uses credentials in two places:

### 1. **Client-Side (Already Configured)** ✅
- Location: `config/firebase-config.js` and `config/google-sheets-config.js`
- Purpose: Frontend JavaScript that runs in the browser
- Status: Already working with your current credentials
- Update: Edit the files directly or manually update from `.env`

### 2. **Backend (Firebase Functions)**
- Location: Firebase Functions environment config
- Purpose: Server-side code that runs on Firebase
- Status: Needs configuration via `firebase functions:config:set`
- Update: Use `firebase functions:config:set` commands

---

## 🎬 Full Example Workflow

```bash
# 1. Check your .env file (already populated!)
cat .env

# 2. Run setup to generate config files
npm run setup

# 3. Test locally (optional)
npm run firebase:serve

# 4. Login to Firebase
npm run firebase:login

# 5. Select project
npm run firebase:init

# 6. Configure backend
npm run setup:firebase

# 7. Deploy
npm run firebase:deploy
```

---

## 📚 Need More Details?

See the comprehensive guide:

```bash
cat CREDENTIAL_SETUP_GUIDE.md
```

Or open it in your editor for detailed instructions, troubleshooting, and security best practices.

---

## ⚡ Common Issues & Quick Fixes

### "firebase: command not found"
**Fix:** Restart your terminal. Firebase CLI was just installed.

### "No credentials found in .env"
**Fix:** This shouldn't happen - your .env is already populated! But if it does, edit `.env` and replace any `your_` placeholders.

### "Permission denied"
**Fix:** Run with node directly:
```bash
node setup-credentials.js
```

### Config files not updating
**Fix:** Make sure you're running `npm run setup` after changing `.env`

---

## ✅ What's Different Now?

### Before (The Problem):
```bash
# Terminal commands didn't work
$ firebase login
bash: firebase: command not found

$ firebase functions:config:set emailjs.service_id="..."
bash: firebase: command not found
```

### After (The Solution):
```bash
# Firebase CLI is now installed and working!
$ firebase login
✔ Success! Logged in as ...

$ firebase functions:config:set emailjs.service_id="..."
✔ Functions config updated

$ firebase deploy
✔ Deploy complete!
```

**Now you can:**
- ✅ Use all `firebase` terminal commands
- ✅ Configure Firebase Functions from the command line
- ✅ Deploy your site and functions
- ✅ Manage backend configuration with environment variables

---

## 🎉 You're All Set!

Your terminal can now use Firebase CLI commands. The core issue is resolved!

**Next steps:**
1. Login to Firebase: `firebase login`
2. Select your project: `firebase use --add`
3. Configure Functions: Add private keys to `.env`, then use `firebase functions:config:set`
4. Deploy when ready: `firebase deploy`

**Questions?** Check `CREDENTIAL_SETUP_GUIDE.md` for detailed help.
