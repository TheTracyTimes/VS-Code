#!/bin/bash
# Build script for Netlify - generates config files from environment variables

echo "Generating config files from environment variables..."

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
    auth = firebase.auth();
    console.log('Firebase initialized successfully');
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
    registration: '${EMAILJS_TEMPLATE_REGISTRATION:-registration_confirmation}',
    vendor: '${EMAILJS_TEMPLATE_VENDOR:-vendor_confirmation}',
    volunteer: '${EMAILJS_TEMPLATE_VOLUNTEER:-volunteer_confirmation}'
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
        vendors: '${GOOGLE_SHEETS_VENDORS_ID}'
    },

    // Discovery docs and scopes for Google Sheets API
    discoveryDocs: ['https://sheets.googleapis.com/\$discovery/rest?version=v4'],
    scopes: 'https://www.googleapis.com/auth/spreadsheets'
};

// ===== GOOGLE API CLIENT =====

let gapiInited = false;
let gisInited = false;
let tokenClient;

// Initialize Google API Client
function initGoogleSheetsAPI() {
    gapi.load('client', initializeGapiClient);
}

async function initializeGapiClient() {
    try {
        await gapi.client.init({
            apiKey: GOOGLE_SHEETS_CONFIG.apiKey,
            discoveryDocs: GOOGLE_SHEETS_CONFIG.discoveryDocs,
        });
        gapiInited = true;
        console.log('Google API Client initialized');
    } catch (error) {
        console.error('Error initializing Google API Client:', error);
    }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { GOOGLE_SHEETS_CONFIG };
}
SHEETS_EOF

echo "Config files generated successfully!"
echo "  - public/config/firebase-config.js"
echo "  - public/config/google-sheets-config.js"
