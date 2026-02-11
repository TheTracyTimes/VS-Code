// ===== FIREBASE CONFIGURATION =====
// Auto-generated from .env file - DO NOT EDIT MANUALLY
// Run 'node setup-credentials.js' to regenerate

const firebaseConfig = {
    apiKey: "REDACTED_FIREBASE_API_KEY_1",
    authDomain: "sarasota-gospel-temple.firebaseapp.com",
    projectId: "sarasota-gospel-temple",
    storageBucket: "sarasota-gospel-temple.firebasestorage.app",
    messagingSenderId: "868460102497",
    appId: "1:868460102497:web:1b805b72d00801971c7b20",
    measurementId: "G-CEY9WE2C47"
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

const EMAILJS_SERVICE_ID = "REDACTED_EMAILJS_SERVICE_ID";
const EMAILJS_PUBLIC_KEY = "REDACTED_EMAILJS_PUBLIC_KEY";

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
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { firebaseConfig, db, auth, EMAILJS_SERVICE_ID, EMAILJS_PUBLIC_KEY };
}
