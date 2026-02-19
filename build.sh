#!/bin/bash
# ===== NETLIFY BUILD SCRIPT =====
# Generates config files from environment variables
#
# SECURITY NOTE:
# This script ONLY includes CLIENT-SIDE credentials that are safe to expose publicly.
# The following credentials are EXCLUDED and should NEVER be in client-side code:
#   - EMAILJS_PRIVATE_KEY (server-side only, for Firebase Functions)
#   - GOOGLE_SERVICE_ACCOUNT_JSON (server-side only, for Firebase Functions)
#
# All credentials generated here are designed to be public and are secured through:
#   - Firebase Security Rules (not hiding the API key)
#   - Google OAuth authorized domains
#   - Google Cloud API restrictions (HTTP referrers)
#   - EmailJS domain restrictions

echo "========================================="
echo "Netlify Build: Generating Config Files"
echo "========================================="
echo ""
echo "⚠️  SECURITY CHECK:"
echo "✅ Only public client-side credentials will be included"
echo "❌ Private keys (EMAILJS_PRIVATE_KEY, SERVICE_ACCOUNT) excluded"
echo ""

# Create public/config directory
mkdir -p public/config

# Generate firebase-config.js
cat > public/config/firebase-config.js << FIREBASE_EOF
// ===== FIREBASE CONFIGURATION =====
// Auto-generated at build time from environment variables

const firebaseConfig = {
    apiKey: "${FIREBASE_API_KEY}",
    authDomain: "${FIREBASE_AUTH_DOMAIN}",
    projectId: "${FIREBASE_PROJECT_ID}",
    storageBucket: "${FIREBASE_STORAGE_BUCKET}",
    messagingSenderId: "${FIREBASE_MESSAGING_SENDER_ID}",
    appId: "${FIREBASE_APP_ID}",
    measurementId: "${FIREBASE_MEASUREMENT_ID}"
};

// Initialize Firebase
let db, auth;

try {
    firebase.initializeApp(firebaseConfig);
    db = firebase.firestore();
    console.log('Firebase initialized successfully');

    // Initialize Auth only if the Auth SDK is loaded
    if (typeof firebase.auth === 'function') {
        auth = firebase.auth();
        console.log('Firebase Auth initialized');
    }
} catch (error) {
    console.error('Firebase initialization error:', error);
}

// ===== EMAILJS CONFIGURATION =====

const EMAILJS_SERVICE_ID = "${EMAILJS_SERVICE_ID}";
const EMAILJS_PUBLIC_KEY = "${EMAILJS_PUBLIC_KEY}";

// EmailJS Template IDs
// IMPORTANT: These must match the template IDs in your EmailJS dashboard
// If emails are not sending, verify these IDs in https://dashboard.emailjs.com/admin/templates
const EMAILJS_TEMPLATE_IDS = {
    registration: '${EMAILJS_TEMPLATE_REGISTRATION:-registration_confirmatio}',
    vendor: '${EMAILJS_TEMPLATE_VENDOR:-vendor_confirmation}',
    volunteer: '${EMAILJS_TEMPLATE_VOLUNTEER:-volunteer_confirmation}',
    contact: '${EMAILJS_TEMPLATE_CONTACT:-contact_confirmation}'
};

// Initialize EmailJS
function initEmailJS() {
    if (typeof emailjs !== 'undefined') {
        emailjs.init(EMAILJS_PUBLIC_KEY);
        console.log('EmailJS initialized');
    }
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initEmailJS);
} else {
    initEmailJS();
}

// Export for use in other scripts
if (typeof window !== 'undefined') {
    window.EMAILJS_SERVICE_ID = EMAILJS_SERVICE_ID;
    window.EMAILJS_PUBLIC_KEY = EMAILJS_PUBLIC_KEY;
    window.EMAILJS_TEMPLATE_IDS = EMAILJS_TEMPLATE_IDS;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { firebaseConfig, db, auth, EMAILJS_SERVICE_ID, EMAILJS_PUBLIC_KEY, EMAILJS_TEMPLATE_IDS };
}
FIREBASE_EOF

# Generate google-sheets-config.js
cat > public/config/google-sheets-config.js << SHEETS_EOF
// ===== GOOGLE SHEETS API CONFIGURATION =====
// Auto-generated at build time from environment variables

const GOOGLE_SHEETS_CONFIG = {
    // Your Google Cloud Project API Key (for client-side access)
    apiKey: '${GOOGLE_SHEETS_API_KEY}',

    // Your Google Cloud Project Client ID (for OAuth)
    clientId: '${GOOGLE_SHEETS_CLIENT_ID}',

    // Google Sheets IDs for each form type
    spreadsheetIds: {
        registrations: '${GOOGLE_SHEETS_REGISTRATIONS_ID}',
        volunteers: '${GOOGLE_SHEETS_VOLUNTEERS_ID}',
        vendors: '${GOOGLE_SHEETS_VENDORS_ID}',
        contacts: '${GOOGLE_SHEETS_CONTACTS_ID:-${GOOGLE_SHEETS_REGISTRATIONS_ID}}'
    },
    scopes: 'https://www.googleapis.com/auth/spreadsheets'
};

// ===== GOOGLE IDENTITY SERVICES =====

let tokenClient;
let googleAccessToken = null;

// Initialize Google Identity Services token client for OAuth
function initGISClient() {
    if (typeof google === 'undefined' || !google.accounts) {
        console.warn('Google Identity Services not loaded');
        return;
    }
    tokenClient = google.accounts.oauth2.initTokenClient({
        client_id: GOOGLE_SHEETS_CONFIG.clientId,
        scope: GOOGLE_SHEETS_CONFIG.scopes,
        callback: '',
    });
    console.log('Google Identity Services initialized');
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    if (GOOGLE_SHEETS_CONFIG.clientId) {
        initGISClient();
    }
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { GOOGLE_SHEETS_CONFIG };
}
SHEETS_EOF

echo ""
echo "========================================="
echo "✅ Config files generated successfully!"
echo "========================================="
echo "  - public/config/firebase-config.js"
echo "  - public/config/google-sheets-config.js"
echo ""

# ===== SECURITY VALIDATION =====
echo "🔒 Running security validation..."

# Check that private keys are NOT in generated files
SECURITY_ERROR=0

if grep -r "EMAILJS_PRIVATE_KEY\|emailjs.private\|private_key.*BEGIN PRIVATE KEY" public/config/ 2>/dev/null; then
    echo "❌ ERROR: Private key detected in generated config files!"
    SECURITY_ERROR=1
fi

if grep -r "GOOGLE_SERVICE_ACCOUNT_JSON\|service_account.*private_key" public/config/ 2>/dev/null; then
    echo "❌ ERROR: Service account credentials detected in generated config files!"
    SECURITY_ERROR=1
fi

if [ $SECURITY_ERROR -eq 1 ]; then
    echo ""
    echo "❌ BUILD FAILED: Security validation error"
    echo "   Private credentials were found in client-side config files."
    echo "   This is a critical security issue."
    exit 1
fi

echo "✅ Security validation passed - no private keys in client-side code"
echo ""
echo "========================================="
echo "🚀 Build completed successfully!"
echo "========================================="
