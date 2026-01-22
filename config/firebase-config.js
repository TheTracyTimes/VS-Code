// ===== FIREBASE CONFIGURATION =====
// Initialize Firebase for the Sarasota Gospel Temple Website

// Firebase SDK imports (loaded from CDN in HTML)
// Make sure to include these scripts in your HTML:
/*
<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-auth-compat.js"></script>
*/

// Your Firebase configuration object
// REPLACE THESE VALUES with your actual Firebase project credentials
const firebaseConfig = {
    apiKey: "YOUR_API_KEY_HERE",
    authDomain: "your-project-id.firebaseapp.com",
    projectId: "your-project-id",
    storageBucket: "your-project-id.appspot.com",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID",
    databaseURL: "https://your-project-id.firebaseio.com"
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

// ===== DATABASE FUNCTIONS =====

// Submit registration to Firestore
async function submitRegistration(data) {
    try {
        const docRef = await db.collection('registrations').add({
            ...data,
            createdAt: firebase.firestore.FieldValue.serverTimestamp(),
            status: 'pending'
        });

        console.log('Registration submitted with ID:', docRef.id);
        return docRef.id;
    } catch (error) {
        console.error('Error adding registration:', error);
        throw error;
    }
}

// Submit volunteer application
async function submitVolunteer(data) {
    try {
        const docRef = await db.collection('volunteers').add({
            ...data,
            createdAt: firebase.firestore.FieldValue.serverTimestamp(),
            status: 'pending'
        });

        console.log('Volunteer application submitted with ID:', docRef.id);
        return docRef.id;
    } catch (error) {
        console.error('Error adding volunteer:', error);
        throw error;
    }
}

// Submit vendor application
async function submitVendor(data) {
    try {
        const docRef = await db.collection('vendors').add({
            ...data,
            createdAt: firebase.firestore.FieldValue.serverTimestamp(),
            status: 'pending',
            approved: false
        });

        console.log('Vendor application submitted with ID:', docRef.id);
        return docRef.id;
    } catch (error) {
        console.error('Error adding vendor:', error);
        throw error;
    }
}

// ===== ADMIN FUNCTIONS =====

// Get all registrations
async function getAllRegistrations() {
    try {
        const snapshot = await db.collection('registrations')
            .orderBy('createdAt', 'desc')
            .get();

        const registrations = [];
        snapshot.forEach(doc => {
            registrations.push({
                id: doc.id,
                ...doc.data()
            });
        });

        return registrations;
    } catch (error) {
        console.error('Error getting registrations:', error);
        throw error;
    }
}

// Get all volunteers
async function getAllVolunteers() {
    try {
        const snapshot = await db.collection('volunteers')
            .orderBy('createdAt', 'desc')
            .get();

        const volunteers = [];
        snapshot.forEach(doc => {
            volunteers.push({
                id: doc.id,
                ...doc.data()
            });
        });

        return volunteers;
    } catch (error) {
        console.error('Error getting volunteers:', error);
        throw error;
    }
}

// Get all vendors
async function getAllVendors() {
    try {
        const snapshot = await db.collection('vendors')
            .orderBy('createdAt', 'desc')
            .get();

        const vendors = [];
        snapshot.forEach(doc => {
            vendors.push({
                id: doc.id,
                ...doc.data()
            });
        });

        return vendors;
    } catch (error) {
        console.error('Error getting vendors:', error);
        throw error;
    }
}

// Update vendor approval status
async function updateVendorStatus(vendorId, approved, notes = '') {
    try {
        await db.collection('vendors').doc(vendorId).update({
            approved: approved,
            approvalNotes: notes,
            approvedAt: firebase.firestore.FieldValue.serverTimestamp()
        });

        console.log(`Vendor ${vendorId} ${approved ? 'approved' : 'denied'}`);
        return true;
    } catch (error) {
        console.error('Error updating vendor status:', error);
        throw error;
    }
}

// Delete a record (for admin use)
async function deleteRecord(collection, docId) {
    try {
        await db.collection(collection).doc(docId).delete();
        console.log(`Document ${docId} deleted from ${collection}`);
        return true;
    } catch (error) {
        console.error('Error deleting document:', error);
        throw error;
    }
}

// ===== AUTHENTICATION =====

// Sign in admin user
async function signInAdmin(email, password) {
    try {
        const userCredential = await auth.signInWithEmailAndPassword(email, password);
        console.log('Admin signed in:', userCredential.user.email);
        return userCredential.user;
    } catch (error) {
        console.error('Sign in error:', error);
        throw error;
    }
}

// Sign out
async function signOut() {
    try {
        await auth.signOut();
        console.log('User signed out');
    } catch (error) {
        console.error('Sign out error:', error);
        throw error;
    }
}

// Check authentication state
function onAuthStateChanged(callback) {
    auth.onAuthStateChanged(callback);
}

// ===== EXPORT FUNCTIONS =====

// Export data to CSV format
function exportToCSV(data, filename) {
    if (data.length === 0) {
        alert('No data to export');
        return;
    }

    // Get all unique keys from all objects
    const keys = [...new Set(data.flatMap(obj => Object.keys(obj)))];

    // Create CSV header
    const header = keys.join(',');

    // Create CSV rows
    const rows = data.map(obj => {
        return keys.map(key => {
            const value = obj[key];
            // Handle arrays, objects, and special characters
            if (Array.isArray(value)) {
                return `"${value.join('; ')}"`;
            } else if (typeof value === 'object' && value !== null) {
                return `"${JSON.stringify(value)}"`;
            } else if (typeof value === 'string' && value.includes(',')) {
                return `"${value}"`;
            }
            return value || '';
        }).join(',');
    });

    // Combine header and rows
    const csv = [header, ...rows].join('\n');

    // Create download link
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

// ===== EMAIL NOTIFICATIONS =====

// Configure EmailJS (free email service)
// Sign up at https://www.emailjs.com/
const EMAILJS_SERVICE_ID = 'YOUR_EMAILJS_SERVICE_ID';
const EMAILJS_TEMPLATE_ID = 'YOUR_EMAILJS_TEMPLATE_ID';
const EMAILJS_PUBLIC_KEY = 'YOUR_EMAILJS_PUBLIC_KEY';

// Initialize EmailJS
function initEmailJS() {
    if (typeof emailjs !== 'undefined') {
        emailjs.init(EMAILJS_PUBLIC_KEY);
        console.log('EmailJS initialized');
    }
}

// Send email notification for new registration
async function sendRegistrationEmail(data) {
    try {
        const templateParams = {
            to_email: 'tracykmussotte@gmail.com',
            from_name: `${data.firstName} ${data.lastName}`,
            reply_to: data.email || data.phone,
            subject: 'New Registration - 2026 International Meeting',
            message: `
New registration received:

Name: ${data.firstName} ${data.lastName}
Phone: ${data.phone}
Email: ${data.email || 'Not provided'}
Pastor: ${data.pastorName}
Assembly: ${data.assemblyName || 'Not provided'}

Services Attending: ${Array.isArray(data.services) ? data.services.join(', ') : data.services}

Airport Transportation: ${data.airportTransport}
Local Transportation: ${data.localTransport}

Children Under 5: ${data.hasChildren}
${data.hasChildren === 'Yes' ? `Number of Children: ${data.numChildren}` : ''}

Submitted: ${new Date().toLocaleString()}
            `.trim()
        };

        if (typeof emailjs !== 'undefined') {
            await emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, templateParams);
            console.log('Email notification sent');
        }
    } catch (error) {
        console.error('Error sending email:', error);
        // Don't throw - form was still submitted successfully
    }
}

// Send confirmation email to registrant
async function sendConfirmationEmail(data) {
    try {
        const templateParams = {
            to_email: data.email,
            to_name: `${data.firstName} ${data.lastName}`,
            subject: 'Registration Confirmed - 2026 International Meeting',
            message: `
Dear ${data.firstName} ${data.lastName},

Thank you for registering for the Sarasota Gospel Temple 2026 International Meeting!

EVENT DETAILS:
📅 Dates: April 9-11, 2026
📍 Location: 1900 Gandy Blvd N, St. Petersburg, FL 33702
📞 Contact: 941-667-0526

YOUR REGISTRATION:
Services Attending: ${Array.isArray(data.services) ? data.services.join(', ') : data.services}
Transportation Needed: ${data.airportTransport}

We look forward to seeing you at the meeting! If you need to update your registration, please contact us at 941-667-0526.

Blessings,
Sarasota Gospel Temple
            `.trim()
        };

        if (typeof emailjs !== 'undefined' && data.email) {
            await emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, templateParams);
            console.log('Confirmation email sent to registrant');
        }
    } catch (error) {
        console.error('Error sending confirmation email:', error);
    }
}
