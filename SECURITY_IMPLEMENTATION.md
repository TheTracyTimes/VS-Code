# Security Implementation Guide

## Overview

This document describes the comprehensive security measures implemented for the Sarasota Gospel Temple website, including how to rotate credentials and maintain security best practices.

## Implemented Security Features

### 1. Backend Security with Firebase Functions

All sensitive operations have been moved to Firebase Cloud Functions to protect API keys and credentials.

**Location:** `/functions/index.js`

**Features:**
- Server-side validation of all form submissions
- Rate limiting per IP address (1 minute cooldown)
- Input sanitization and validation
- Secure credential storage via Firebase environment config

### 2. Client-Side Security

**Location:** `/js/security-utils.js`

**Features:**
- **XSS Protection:** DOMPurify integration prevents cross-site scripting attacks
- **Input Validation:** Comprehensive form validation with sanitization
- **CSRF Protection:** Token-based CSRF protection on all forms
- **Rate Limiting:** Client-side rate limiting (1 minute between submissions)
- **Data Masking:** Sensitive data (emails, phone numbers) are masked in UI

### 3. Content Security Policy (CSP)

**Location:** `/firebase.json`

Headers implemented:
- `Content-Security-Policy`: Restricts resource loading to trusted sources
- `X-Frame-Options`: Prevents clickjacking attacks
- `X-Content-Type-Options`: Prevents MIME-type sniffing
- `Referrer-Policy`: Controls referrer information
- `X-XSS-Protection`: Browser XSS protection

### 4. Firestore Security Rules

**Location:** `/firestore.rules`

Features:
- Server-side validation of all data fields
- Email and phone number format validation
- Name validation (letters, spaces, hyphens, apostrophes only)
- Only authenticated users can read/update/delete records
- Public can only create records (for form submissions)

### 5. Fixed Vulnerabilities

#### Fixed XSS Vulnerabilities
- **Admin Dashboard:** Replaced `innerHTML` with safe DOM manipulation methods
- **View Details Modal:** Replaced `document.write()` with safe DOM methods
- **All Forms:** Implemented DOMPurify sanitization

#### Removed Inline Event Handlers
- All `onclick` attributes replaced with event listeners
- Navigation buttons now use data attributes
- Action buttons use event delegation

#### Secure Logging
- Removed logging of sensitive data (emails, passwords)
- Implemented secure logging with data masking

## Credential Rotation Guide

### CRITICAL: Rotate ALL Exposed Credentials

Since credentials were previously exposed in client-side JavaScript, you must rotate them immediately.

### 1. Firebase Credentials

**Steps:**
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project: `sarasota-gospel-temple`
3. Click the gear icon → Project settings
4. Under "Your apps", click "Add app" → Web
5. Register a new web app with a new name
6. Copy the new credentials
7. **Do NOT commit these to the repository**

**Store securely:**
- For local development: Create `.env` file (already in `.gitignore`)
- For Firebase Functions: Use Firebase environment config

```bash
# Set Firebase Functions environment variables
firebase functions:config:set \
  firebase.api_key="NEW_API_KEY" \
  firebase.auth_domain="NEW_AUTH_DOMAIN"
```

### 2. EmailJS Credentials

**Steps:**
1. Go to [EmailJS Dashboard](https://dashboard.emailjs.com/)
2. Create a new service or regenerate keys
3. Update environment variables

```bash
# Set EmailJS credentials for Firebase Functions
firebase functions:config:set \
  emailjs.service_id="NEW_SERVICE_ID" \
  emailjs.public_key="NEW_PUBLIC_KEY" \
  emailjs.private_key="NEW_PRIVATE_KEY"
```

### 3. Google Sheets & API Credentials

**Steps:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to APIs & Services → Credentials
3. Delete old API keys and OAuth clients
4. Create new credentials:
   - Create new API key (restrict to Sheets API)
   - Create new OAuth 2.0 Client ID
   - Download service account JSON for Firebase Functions

```bash
# Set Google credentials for Firebase Functions
firebase functions:config:set \
  google.credentials="$(cat path/to/service-account.json)" \
  sheets.registrations_id="SPREADSHEET_ID" \
  sheets.volunteers_id="SPREADSHEET_ID" \
  sheets.vendors_id="SPREADSHEET_ID"
```

### 4. Verify Old Credentials Are Revoked

**Firebase:**
- In Firebase Console → Project settings → Your apps
- Delete the old web app configuration

**Google Cloud:**
- Delete old API keys from Google Cloud Console
- Revoke old OAuth clients

**EmailJS:**
- Delete or disable old API keys in EmailJS dashboard

## Environment Configuration

### Local Development Setup

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Fill in your new credentials in `.env`:
```env
FIREBASE_API_KEY=your_new_firebase_api_key
EMAILJS_SERVICE_ID=your_new_emailjs_service_id
# ... etc
```

3. **Never commit `.env` to git** (already in `.gitignore`)

### Production Deployment

For Firebase Functions production:

```bash
# Deploy with new environment config
firebase deploy --only functions
```

For Firebase Hosting:

```bash
# Deploy updated code
firebase deploy --only hosting
```

## Security Best Practices

### 1. Regular Security Audits

Run security checks monthly:
```bash
# Check for exposed secrets
git secrets --scan

# Audit npm packages
npm audit

# Check for outdated dependencies
npm outdated
```

### 2. Monitor Firebase Usage

- Check Firebase Console → Usage tab for unusual activity
- Review Firestore security rules regularly
- Monitor Cloud Functions logs for errors

### 3. Form Submission Monitoring

- Review rate limiting logs in Firestore `rateLimits` collection
- Monitor for unusual submission patterns
- Check admin dashboard regularly

### 4. Keep Dependencies Updated

```bash
# Update Firebase Functions dependencies
cd functions
npm update

# Check for security vulnerabilities
npm audit fix
```

### 5. Review Access Controls

- Regularly audit Firebase Authentication users
- Review Firestore security rules
- Check Google Cloud IAM permissions

## Testing Security Features

### 1. Test XSS Protection

Try submitting forms with malicious input:
```
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
```

Expected result: Input should be sanitized and displayed as plain text.

### 2. Test CSRF Protection

1. Open browser console on form page
2. Try: `sessionStorage.removeItem('csrf_token')`
3. Submit form

Expected result: "Security validation failed" error.

### 3. Test Rate Limiting

1. Submit a form
2. Try to submit again within 60 seconds

Expected result: "Please wait X seconds before submitting again" error.

### 4. Test Input Validation

Try submitting:
- Invalid email formats
- Phone numbers with < 10 digits
- Names with special characters

Expected result: Validation errors displayed.

## Incident Response Plan

If credentials are exposed again:

1. **Immediately** rotate all affected credentials
2. Review Firebase/Google Cloud logs for unauthorized access
3. Check Firestore for suspicious data
4. Notify users if data breach occurred
5. Update `.gitignore` to prevent future exposure
6. Run `git filter-branch` to remove secrets from git history

## Support

For security concerns, contact:
- Email: sarasotagospel@gmail.com
- Phone: 941-800-5211

## File Manifest

### Security Files
- `/js/security-utils.js` - Client-side security utilities
- `/functions/index.js` - Backend security and validation
- `/firestore.rules` - Database security rules
- `/firebase.json` - Security headers configuration
- `/.gitignore` - Prevents committing sensitive files
- `/.env.example` - Template for environment variables

### Configuration Files (DO NOT COMMIT)
- `/.env` - Local environment variables
- `/config/firebase-config.js` - Should use environment variables
- `/config/google-sheets-config.js` - Should use environment variables

### Updated Files
- `/js/admin-dashboard.js` - XSS fixes, secure event handlers
- `/js/registration-form.js` - CSRF protection, validation, rate limiting
- `/js/volunteer-form.js` - CSRF protection, validation, rate limiting
- `/js/vendor-form.js` - CSRF protection, validation, rate limiting
- `/admin/dashboard.html` - Security scripts, removed inline handlers
- `/forms/*.html` - Added security scripts

## Version History

- **v2.0.0** (2024) - Comprehensive security overhaul
  - Implemented Firebase Functions backend
  - Added XSS protection with DOMPurify
  - Implemented CSRF protection
  - Added rate limiting
  - Implemented input validation and sanitization
  - Added Content Security Policy
  - Updated Firestore security rules
  - Removed inline event handlers
  - Implemented secure logging with data masking

---

**Last Updated:** February 2024
**Security Audit:** Recommended quarterly
