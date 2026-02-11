// ===== FIREBASE CONFIGURATION =====
// Auto-generated from .env file - DO NOT EDIT MANUALLY
// Run 'node setup-credentials.js' to regenerate

const firebaseConfig = {
    apiKey: "AIzaSyBZVYB04dtsa9AL7e5xw1W5ZVOrqds6Akk",
    authDomain: "sarasota-gospel-temple.firebaseapp.com",
    projectId: "sarasota-gospel-temple",
    storageBucket: "sarasota-gospel-temple.firebasestorage.app",
    messagingSenderId: "868460102497",
    appId: "1:868460102497:web:d36ace1f5fd535b21c7b20",
    measurementId: "G-BQG0SYFGQ9"
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

const EMAILJS_SERVICE_ID = "service_vdrrcls";
const EMAILJS_PUBLIC_KEY = "T35UiRys7umDsRZw8";

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
