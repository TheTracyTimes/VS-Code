// ===== FIREBASE CLOUD FUNCTIONS =====
// Secure backend endpoints for Sarasota Gospel Temple

// Load environment variables from .env file (for local development)
require('dotenv').config();

const functions = require('firebase-functions');
const admin = require('firebase-admin');
const emailjs = require('@emailjs/nodejs');
const { google } = require('googleapis');

admin.initializeApp();

// ===== ENVIRONMENT CONFIGURATION =====
// Helper function to get config from either .env or Firebase config
function getConfig(envKey, firebaseConfigPath) {
    // Try process.env first (local development with .env)
    if (process.env[envKey]) {
        return process.env[envKey];
    }

    // Try Firebase config (production)
    try {
        const configParts = firebaseConfigPath.split('.');
        let value = functions.config();
        for (const part of configParts) {
            value = value[part];
            if (!value) return null;
        }
        return value;
    } catch (error) {
        return null;
    }
}

// ===== VALIDATION UTILITIES =====

function validateEmail(email) {
    const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return re.test(email);
}

function validatePhone(phone) {
    const cleaned = phone.replace(/\D/g, '');
    return cleaned.length >= 10;
}

function validateName(name) {
    const cleaned = name.trim();
    return cleaned.length >= 2 && cleaned.length <= 50 && /^[a-zA-Z\s\-']+$/.test(cleaned);
}

function sanitizeText(text) {
    if (typeof text !== 'string') return '';
    return text.trim().substring(0, 500); // Limit length
}

// ===== RATE LIMITING =====

async function checkRateLimit(ip, formType) {
    const rateRef = admin.firestore().collection('rateLimits').doc(`${ip}_${formType}`);
    const rateDoc = await rateRef.get();
    const now = Date.now();
    const limit = 60000; // 1 minute

    if (rateDoc.exists) {
        const lastSubmit = rateDoc.data().lastSubmit;
        if (now - lastSubmit < limit) {
            const remaining = Math.ceil((limit - (now - lastSubmit)) / 1000);
            throw new functions.https.HttpsError(
                'resource-exhausted',
                `Too many requests. Please wait ${remaining} seconds before submitting again.`
            );
        }
    }

    await rateRef.set({ lastSubmit: now });
    return true;
}

// ===== REGISTRATION SUBMISSION =====

exports.submitRegistration = functions.https.onCall(async (data, context) => {
    try {
        // Get IP for rate limiting
        const ip = context.rawRequest.ip;
        await checkRateLimit(ip, 'registration');

        // Validate required fields
        if (!data.firstName || !data.lastName || !data.phone || !data.pastorName) {
            throw new functions.https.HttpsError('invalid-argument', 'Missing required fields');
        }

        // Validate data types and formats
        if (!validateName(data.firstName) || !validateName(data.lastName)) {
            throw new functions.https.HttpsError('invalid-argument', 'Invalid name format');
        }

        if (!validatePhone(data.phone)) {
            throw new functions.https.HttpsError('invalid-argument', 'Invalid phone number');
        }

        if (data.email && !validateEmail(data.email)) {
            throw new functions.https.HttpsError('invalid-argument', 'Invalid email format');
        }

        // Sanitize all text fields
        const sanitizedData = {
            firstName: sanitizeText(data.firstName),
            lastName: sanitizeText(data.lastName),
            phone: sanitizeText(data.phone),
            email: data.email ? sanitizeText(data.email) : null,
            pastorName: sanitizeText(data.pastorName),
            assemblyName: data.assemblyName ? sanitizeText(data.assemblyName) : null,
            services: Array.isArray(data.services) ? data.services : [],
            airportTransport: data.airportTransport || 'No',
            arrivalDate: data.arrivalDate ? sanitizeText(data.arrivalDate) : null,
            arrivalTime: data.arrivalTime ? sanitizeText(data.arrivalTime) : null,
            departureDate: data.departureDate ? sanitizeText(data.departureDate) : null,
            departureTime: data.departureTime ? sanitizeText(data.departureTime) : null,
            localTransport: data.localTransport || 'No',
            pickupLocation: data.pickupLocation ? sanitizeText(data.pickupLocation) : null,
            hasChildren: data.hasChildren || 'No',
            numChildren: data.numChildren ? parseInt(data.numChildren) : 0,
            numVBS: data.numVBS ? parseInt(data.numVBS) : 0,
            numNursery: data.numNursery ? parseInt(data.numNursery) : 0,
            createdAt: admin.firestore.FieldValue.serverTimestamp(),
            status: 'pending'
        };

        // Save to Firestore
        const docRef = await admin.firestore().collection('registrations').add(sanitizedData);

        return { success: true, id: docRef.id };
    } catch (error) {
        console.error('Error in submitRegistration:', error);
        throw error;
    }
});

// ===== VOLUNTEER SUBMISSION =====

exports.submitVolunteer = functions.https.onCall(async (data, context) => {
    try {
        const ip = context.rawRequest.ip;
        await checkRateLimit(ip, 'volunteer');

        // Validate required fields
        if (!data.firstName || !data.lastName || !data.phone) {
            throw new functions.https.HttpsError('invalid-argument', 'Missing required fields');
        }

        if (!validateName(data.firstName) || !validateName(data.lastName)) {
            throw new functions.https.HttpsError('invalid-argument', 'Invalid name format');
        }

        if (!validatePhone(data.phone)) {
            throw new functions.https.HttpsError('invalid-argument', 'Invalid phone number');
        }

        if (data.email && !validateEmail(data.email)) {
            throw new functions.https.HttpsError('invalid-argument', 'Invalid email format');
        }

        const sanitizedData = {
            firstName: sanitizeText(data.firstName),
            lastName: sanitizeText(data.lastName),
            phone: sanitizeText(data.phone),
            email: data.email ? sanitizeText(data.email) : null,
            committees: Array.isArray(data.committees) ? data.committees : [],
            availability: Array.isArray(data.availability) ? data.availability : [],
            createdAt: admin.firestore.FieldValue.serverTimestamp(),
            status: 'pending'
        };

        const docRef = await admin.firestore().collection('volunteers').add(sanitizedData);

        return { success: true, id: docRef.id };
    } catch (error) {
        console.error('Error in submitVolunteer:', error);
        throw error;
    }
});

// ===== VENDOR SUBMISSION =====

exports.submitVendor = functions.https.onCall(async (data, context) => {
    try {
        const ip = context.rawRequest.ip;
        await checkRateLimit(ip, 'vendor');

        // Validate required fields
        if (!data.businessName || !data.firstName || !data.lastName || !data.phone) {
            throw new functions.https.HttpsError('invalid-argument', 'Missing required fields');
        }

        if (!validateName(data.firstName) || !validateName(data.lastName)) {
            throw new functions.https.HttpsError('invalid-argument', 'Invalid name format');
        }

        if (!validatePhone(data.phone)) {
            throw new functions.https.HttpsError('invalid-argument', 'Invalid phone number');
        }

        if (data.email && !validateEmail(data.email)) {
            throw new functions.https.HttpsError('invalid-argument', 'Invalid email format');
        }

        const sanitizedData = {
            businessName: sanitizeText(data.businessName),
            website: data.website ? sanitizeText(data.website) : null,
            firstName: sanitizeText(data.firstName),
            lastName: sanitizeText(data.lastName),
            phone: sanitizeText(data.phone),
            email: data.email ? sanitizeText(data.email) : null,
            pastorName: data.pastorName ? sanitizeText(data.pastorName) : null,
            assemblyName: data.assemblyName ? sanitizeText(data.assemblyName) : null,
            selling: sanitizeText(data.selling),
            goodsType: data.goodsType || 'Books/Media',
            tableStaffed: data.tableStaffed || 'All Times',
            availability: Array.isArray(data.availability) ? data.availability : [],
            createdAt: admin.firestore.FieldValue.serverTimestamp(),
            status: 'pending',
            approved: false
        };

        const docRef = await admin.firestore().collection('vendors').add(sanitizedData);

        return { success: true, id: docRef.id };
    } catch (error) {
        console.error('Error in submitVendor:', error);
        throw error;
    }
});

// ===== SEND EMAIL VIA EMAILJS =====

exports.sendEmail = functions.https.onCall(async (data, context) => {
    try {
        // Validate request
        if (!data.templateId || !data.params) {
            throw new functions.https.HttpsError('invalid-argument', 'Missing template or parameters');
        }

        // Get EmailJS credentials from environment variables or Firebase config
        const serviceId = getConfig('EMAILJS_SERVICE_ID', 'emailjs.service_id');
        const publicKey = getConfig('EMAILJS_PUBLIC_KEY', 'emailjs.public_key');
        const privateKey = getConfig('EMAILJS_PRIVATE_KEY', 'emailjs.private_key');

        if (!serviceId || !publicKey || !privateKey) {
            throw new functions.https.HttpsError('failed-precondition', 'EmailJS not configured');
        }

        // Send email using EmailJS
        const response = await emailjs.send(
            serviceId,
            data.templateId,
            data.params,
            {
                publicKey: publicKey,
                privateKey: privateKey,
            }
        );

        return { success: true, response };
    } catch (error) {
        console.error('Error sending email:', error);
        throw new functions.https.HttpsError('internal', 'Failed to send email');
    }
});

// ===== GOOGLE SHEETS SYNC =====

exports.appendToSheet = functions.https.onCall(async (data, context) => {
    try {
        // Note: Authentication not required for public form submissions
        // Data validation will ensure integrity

        // Validate form type
        if (!data.formType || !['registrations', 'volunteers', 'vendors'].includes(data.formType)) {
            throw new functions.https.HttpsError('invalid-argument', 'Invalid form type');
        }

        // Get Google Sheets credentials from environment variables or Firebase config
        const credentials = getConfig('GOOGLE_SERVICE_ACCOUNT_JSON', 'google.service_account');
        if (!credentials) {
            console.warn('Google Sheets not configured - skipping sync');
            return { success: false, message: 'Google Sheets not configured' };
        }

        // Authenticate using service account
        const auth = new google.auth.GoogleAuth({
            credentials: typeof credentials === 'string' ? JSON.parse(credentials) : credentials,
            scopes: ['https://www.googleapis.com/auth/spreadsheets'],
        });

        const sheets = google.sheets({ version: 'v4', auth });

        // Get spreadsheet ID based on form type
        const spreadsheetIds = {
            registrations: getConfig('GOOGLE_SHEETS_REGISTRATIONS_ID', 'sheets.registrations_id'),
            volunteers: getConfig('GOOGLE_SHEETS_VOLUNTEERS_ID', 'sheets.volunteers_id'),
            vendors: getConfig('GOOGLE_SHEETS_VENDORS_ID', 'sheets.vendors_id')
        };

        const spreadsheetId = spreadsheetIds[data.formType];
        if (!spreadsheetId) {
            throw new functions.https.HttpsError('invalid-argument', 'Invalid form type');
        }

        // Format data as row values
        const values = [data.rowData];

        // Append to sheet
        const response = await sheets.spreadsheets.values.append({
            spreadsheetId: spreadsheetId,
            range: 'Sheet1!A:Z',
            valueInputOption: 'RAW',
            insertDataOption: 'INSERT_ROWS',
            resource: { values },
        });

        return { success: true, updatedRows: response.data.updates.updatedRows };
    } catch (error) {
        console.error('Error appending to sheet:', error);
        throw new functions.https.HttpsError('internal', 'Failed to append to sheet');
    }
});
