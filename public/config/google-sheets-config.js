// ===== GOOGLE SHEETS API CONFIGURATION =====
// Auto-generated from .env file - DO NOT EDIT MANUALLY
// Run 'node setup-credentials.js' to regenerate

const GOOGLE_SHEETS_CONFIG = {
    // Your Google Cloud Project API Key (for client-side access)
    apiKey: 'REDACTED_GOOGLE_SHEETS_API_KEY',

    // Your Google Cloud Project Client ID (for OAuth)
    clientId: 'REDACTED_GOOGLE_CLIENT_ID',

    // Google Sheets IDs for each form type
    spreadsheetIds: {
        registrations: '1q7vxkgof14p6OpHehTySIU6c0qNpbencA6E09agYJTg',
        volunteers: '1T45QcAsY7m5SO8gSQKTvHI_PFFa4qx1x6dwW3iwG0s0',
        vendors: '1V6G2KN1vvTB5Ng249rg9K6ijbUT7tou_jaE9ygALxeM'
    },

    // Discovery docs and scopes for Google Sheets API
    discoveryDocs: ['https://sheets.googleapis.com/$discovery/rest?version=v4'],
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
