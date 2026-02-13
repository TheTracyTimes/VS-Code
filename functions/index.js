// ===== FIREBASE CLOUD FUNCTIONS =====
// Secure backend endpoints for Sarasota Gospel Temple

// Load environment variables from .env file (for local development)
require('dotenv').config();

const functions = require('firebase-functions');
const { defineSecret } = require('firebase-functions/params');
const admin = require('firebase-admin');
const emailjs = require('@emailjs/nodejs');
const { google } = require('googleapis');

admin.initializeApp();

// ===== SECRETS CONFIGURATION =====
// Define secrets for production use (automatically uses process.env in local dev)
const EMAILJS_SERVICE_ID = defineSecret('EMAILJS_SERVICE_ID');
const EMAILJS_PUBLIC_KEY = defineSecret('EMAILJS_PUBLIC_KEY');
const EMAILJS_PRIVATE_KEY = defineSecret('EMAILJS_PRIVATE_KEY');
const GOOGLE_SERVICE_ACCOUNT_JSON = defineSecret('GOOGLE_SERVICE_ACCOUNT_JSON');
const GOOGLE_SHEETS_REGISTRATIONS_ID = defineSecret('GOOGLE_SHEETS_REGISTRATIONS_ID');
const GOOGLE_SHEETS_VOLUNTEERS_ID = defineSecret('GOOGLE_SHEETS_VOLUNTEERS_ID');
const GOOGLE_SHEETS_VENDORS_ID = defineSecret('GOOGLE_SHEETS_VENDORS_ID');

// ===== HELPER FUNCTIONS =====

/**
 * Gets a secret value with fallback to environment variable
 * @param {Object} secret - The secret object from defineSecret
 * @param {string} envKey - The environment variable key to use as fallback
 * @returns {string|null} The secret value or null if not found
 */
function getSecretValue(secret, envKey) {
    try {
        // Try to get value from Firebase Secrets first
        const value = secret.value();
        if (value) return value;
    } catch (error) {
        // Secret not available, will try environment variable
        console.log(`Secret not available for ${envKey}, trying environment variable`);
    }

    // Fallback to environment variable
    const envValue = process.env[envKey];
    if (envValue) {
        console.log(`Using environment variable for ${envKey}`);
        return envValue;
    }

    console.warn(`Neither secret nor environment variable found for ${envKey}`);
    return null;
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

exports.sendEmail = functions
    .runWith({ secrets: [EMAILJS_SERVICE_ID, EMAILJS_PUBLIC_KEY, EMAILJS_PRIVATE_KEY] })
    .https.onCall(async (data, context) => {
        try {
            // Validate request
            if (!data.templateId || !data.params) {
                throw new functions.https.HttpsError('invalid-argument', 'Missing template or parameters');
            }

            // Get EmailJS credentials from secrets
            const serviceId = EMAILJS_SERVICE_ID.value();
            const publicKey = EMAILJS_PUBLIC_KEY.value();
            const privateKey = EMAILJS_PRIVATE_KEY.value();

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

exports.appendToSheet = functions
    .runWith({
        secrets: [
            GOOGLE_SERVICE_ACCOUNT_JSON,
            GOOGLE_SHEETS_REGISTRATIONS_ID,
            GOOGLE_SHEETS_VOLUNTEERS_ID,
            GOOGLE_SHEETS_VENDORS_ID
        ]
    })
    .https.onCall(async (data, context) => {
        try {
            // Note: Authentication not required for public form submissions
            // Data validation will ensure integrity

            // Validate form type
            if (!data.formType || !['registrations', 'volunteers', 'vendors'].includes(data.formType)) {
                throw new functions.https.HttpsError('invalid-argument', 'Invalid form type');
            }

            // Get Google Sheets credentials from secrets
            const credentials = GOOGLE_SERVICE_ACCOUNT_JSON.value();
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
                registrations: GOOGLE_SHEETS_REGISTRATIONS_ID.value(),
                volunteers: GOOGLE_SHEETS_VOLUNTEERS_ID.value(),
                vendors: GOOGLE_SHEETS_VENDORS_ID.value()
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

// Bulk sync all data to Google Sheets
exports.syncAllToSheet = functions
    .runWith({
        secrets: [
            GOOGLE_SERVICE_ACCOUNT_JSON,
            GOOGLE_SHEETS_REGISTRATIONS_ID,
            GOOGLE_SHEETS_VOLUNTEERS_ID,
            GOOGLE_SHEETS_VENDORS_ID
        ]
    })
    .https.onCall(async (data, context) => {
        try {
            // Validate form type
            if (!data.formType || !['registrations', 'volunteers', 'vendors'].includes(data.formType)) {
                throw new functions.https.HttpsError('invalid-argument', 'Invalid form type');
            }

            // Validate that we have data to sync
            if (!data.rows || !Array.isArray(data.rows)) {
                throw new functions.https.HttpsError('invalid-argument', 'Invalid data: rows must be an array');
            }

            // Get Google Sheets credentials from secrets or environment
            console.log('Attempting to retrieve Google Sheets credentials...');
            const credentials = getSecretValue(GOOGLE_SERVICE_ACCOUNT_JSON, 'GOOGLE_SERVICE_ACCOUNT_JSON');
            if (!credentials) {
                console.error('Google Sheets credentials not configured');
                throw new functions.https.HttpsError(
                    'failed-precondition',
                    'Google Sheets not configured. Please set GOOGLE_SERVICE_ACCOUNT_JSON secret or environment variable.'
                );
            }
            console.log('Credentials retrieved successfully');

            // Authenticate using service account
            console.log('Authenticating with Google Sheets API...');
            let parsedCredentials;
            try {
                parsedCredentials = typeof credentials === 'string' ? JSON.parse(credentials) : credentials;
            } catch (parseError) {
                console.error('Failed to parse service account credentials:', parseError);
                throw new functions.https.HttpsError(
                    'failed-precondition',
                    'Invalid Google service account credentials format. Please check the GOOGLE_SERVICE_ACCOUNT_JSON secret.'
                );
            }

            const auth = new google.auth.GoogleAuth({
                credentials: parsedCredentials,
                scopes: ['https://www.googleapis.com/auth/spreadsheets'],
            });

            const sheets = google.sheets({ version: 'v4', auth });
            console.log('Google Sheets API client initialized');

            // Get spreadsheet ID based on form type using getSecretValue for better error handling
            console.log(`Retrieving spreadsheet ID for ${data.formType}...`);
            const spreadsheetIds = {
                registrations: getSecretValue(GOOGLE_SHEETS_REGISTRATIONS_ID, 'GOOGLE_SHEETS_REGISTRATIONS_ID'),
                volunteers: getSecretValue(GOOGLE_SHEETS_VOLUNTEERS_ID, 'GOOGLE_SHEETS_VOLUNTEERS_ID'),
                vendors: getSecretValue(GOOGLE_SHEETS_VENDORS_ID, 'GOOGLE_SHEETS_VENDORS_ID')
            };

            const spreadsheetId = spreadsheetIds[data.formType];
            console.log(`Spreadsheet ID for ${data.formType}:`, spreadsheetId ? 'Found' : 'NOT FOUND');
            if (!spreadsheetId) {
                const secretName = `GOOGLE_SHEETS_${data.formType.toUpperCase()}_ID`;
                throw new functions.https.HttpsError(
                    'failed-precondition',
                    `Missing spreadsheet ID for ${data.formType}. Please configure the ${secretName} secret in Firebase.`
                );
            }

            // Define headers based on form type
            const headers = {
                registrations: [
                    'Timestamp', 'ID', 'First Name', 'Last Name', 'Phone', 'Email',
                    'Pastor Name', 'Assembly Name', 'Services', 'Airport Transport',
                    'Local Transport', 'Has Children', 'Number of Children',
                    'VBS Attendance', 'Nursery Attendance'
                ],
                volunteers: [
                    'Timestamp', 'ID', 'First Name', 'Last Name', 'Phone', 'Email',
                    'Committees', 'Availability', 'Committee Assignments'
                ],
                vendors: [
                    'Timestamp', 'ID', 'Business Name', 'First Name', 'Last Name',
                    'Phone', 'Email', 'Website', 'Pastor Name', 'Assembly Name',
                    'Selling', 'Goods Type', 'Table Staffed', 'Availability',
                    'Status', 'Approved'
                ]
            };

            // Clear existing data (except headers) and write new data
            // First, clear all data
            console.log(`Clearing existing data from spreadsheet ${spreadsheetId}...`);
            try {
                await sheets.spreadsheets.values.clear({
                    spreadsheetId: spreadsheetId,
                    range: 'Sheet1!A:Z'
                });
                console.log('Existing data cleared successfully');
            } catch (clearError) {
                console.error('Error clearing spreadsheet:', clearError);
                if (clearError.code === 404) {
                    throw new functions.https.HttpsError(
                        'failed-precondition',
                        `Spreadsheet not found (ID: ${spreadsheetId}). Please verify the spreadsheet ID is correct.`
                    );
                } else if (clearError.code === 403) {
                    throw new functions.https.HttpsError(
                        'failed-precondition',
                        `Service account does not have access to spreadsheet (ID: ${spreadsheetId}). Please share the spreadsheet with the service account email.`
                    );
                }
                throw clearError;
            }

            // Prepare data with headers
            const allRows = [
                headers[data.formType],
                ...data.rows
            ];
            console.log(`Preparing to write ${allRows.length} rows (including header) to spreadsheet...`);

            // Write all data at once
            try {
                const response = await sheets.spreadsheets.values.update({
                    spreadsheetId: spreadsheetId,
                    range: 'Sheet1!A1',
                    valueInputOption: 'RAW',
                    resource: { values: allRows }
                });
                console.log(`Successfully wrote ${response.data.updatedRows} rows to spreadsheet`);

                return {
                    success: true,
                    updatedRows: response.data.updatedRows,
                    syncedCount: data.rows.length
                };
            } catch (writeError) {
                console.error('Error writing to spreadsheet:', writeError);
                if (writeError.code === 403) {
                    throw new functions.https.HttpsError(
                        'failed-precondition',
                        `Service account does not have write permission to spreadsheet (ID: ${spreadsheetId}). Please ensure the service account has Editor access.`
                    );
                }
                throw writeError;
            }
        } catch (error) {
            console.error('Error syncing all to sheet:', {
                message: error.message,
                stack: error.stack,
                code: error.code,
                details: error.details,
                response: error.response?.data
            });

            // Provide detailed error message
            const errorMessage = error.message || error.toString() || 'Unknown error occurred';
            throw new functions.https.HttpsError(
                'internal',
                `Failed to sync to sheet: ${errorMessage}`,
                { originalError: error.code, stack: error.stack }
            );
        }
    });
