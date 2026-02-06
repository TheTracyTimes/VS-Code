// ===== GOOGLE SHEETS API CONFIGURATION =====
// This file handles syncing Firebase data to Google Sheets
// Similar to Google Forms, data will be automatically added to spreadsheets

// ===== CONFIGURATION =====
// IMPORTANT: You need to set up Google Sheets API credentials
// See GOOGLE-SHEETS-SETUP.md for detailed instructions

const GOOGLE_SHEETS_CONFIG = {
    // Your Google Cloud Project API Key (for client-side access)
    // Get this from: https://console.cloud.google.com/apis/credentials
    apiKey: 'REDACTED_GOOGLE_SHEETS_API_KEY',

    // Your Google Cloud Project Client ID (for OAuth)
    // Get this from: https://console.cloud.google.com/apis/credentials
    clientId: 'REDACTED_GOOGLE_CLIENT_ID'',

    // Google Sheets IDs for each form type
    // After creating spreadsheets, paste their IDs here
    // The ID is the long string in the URL: docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit
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

// Initialize Google Identity Services
function initGoogleIdentityServices() {
    tokenClient = google.accounts.oauth2.initTokenClient({
        client_id: GOOGLE_SHEETS_CONFIG.clientId,
        scope: GOOGLE_SHEETS_CONFIG.scopes,
        callback: '', // Will be set per-request
    });
    gisInited = true;
    console.log('Google Identity Services initialized');
}

// ===== AUTHENTICATION =====

// Request authentication token (only needed for admin dashboard)
function requestGoogleSheetsAuth(callback) {
    tokenClient.callback = async (response) => {
        if (response.error !== undefined) {
            console.error('Auth error:', response);
            throw response;
        }
        if (callback) callback(response);
    };

    if (gapi.client.getToken() === null) {
        // Prompt user to select a Google Account and consent
        tokenClient.requestAccessToken({ prompt: 'consent' });
    } else {
        // Skip display of account chooser and consent dialog
        tokenClient.requestAccessToken({ prompt: '' });
    }
}

// ===== SPREADSHEET SETUP =====

// Define column headers for each form type
const SHEET_HEADERS = {
    registrations: [
        'Timestamp',
        'Document ID',
        'First Name',
        'Last Name',
        'Phone',
        'Email',
        'Pastor Name',
        'Assembly Name',
        'Services Attending',
        'Airport Transport',
        'Arrival Date',
        'Arrival Time',
        'Departure Date',
        'Departure Time',
        'Local Transport',
        'Pickup Location',
        'Has Children',
        'Number of Children',
        'Number in VBS',
        'Number in Nursery',
        'Status'
    ],
    volunteers: [
        'Timestamp',
        'Document ID',
        'First Name',
        'Last Name',
        'Phone',
        'Email',
        'Committees',
        'Availability',
        'Committee Assignments',
        'Status'
    ],
    vendors: [
        'Timestamp',
        'Document ID',
        'Business Name',
        'Website',
        'First Name',
        'Last Name',
        'Phone',
        'Email',
        'Pastor Name',
        'Assembly Name',
        'Selling',
        'Goods Type',
        'Table Staffed',
        'Availability',
        'Approved',
        'Approval Notes',
        'Status'
    ]
};

// Create or verify spreadsheet headers
async function ensureSheetHeaders(spreadsheetId, sheetName, headers) {
    try {
        // Check if sheet exists
        const spreadsheet = await gapi.client.sheets.spreadsheets.get({
            spreadsheetId: spreadsheetId
        });

        const sheet = spreadsheet.result.sheets.find(s => s.properties.title === sheetName);

        if (!sheet) {
            // Create new sheet
            await gapi.client.sheets.spreadsheets.batchUpdate({
                spreadsheetId: spreadsheetId,
                resource: {
                    requests: [{
                        addSheet: {
                            properties: {
                                title: sheetName
                            }
                        }
                    }]
                }
            });
        }

        // Check if headers exist
        const response = await gapi.client.sheets.spreadsheets.values.get({
            spreadsheetId: spreadsheetId,
            range: `${sheetName}!A1:Z1`
        });

        if (!response.result.values || response.result.values.length === 0) {
            // Add headers
            await gapi.client.sheets.spreadsheets.values.update({
                spreadsheetId: spreadsheetId,
                range: `${sheetName}!A1`,
                valueInputOption: 'RAW',
                resource: {
                    values: [headers]
                }
            });

            // Format headers (bold, frozen row)
            await gapi.client.sheets.spreadsheets.batchUpdate({
                spreadsheetId: spreadsheetId,
                resource: {
                    requests: [
                        {
                            repeatCell: {
                                range: {
                                    sheetId: sheet ? sheet.properties.sheetId : 0,
                                    startRowIndex: 0,
                                    endRowIndex: 1
                                },
                                cell: {
                                    userEnteredFormat: {
                                        textFormat: { bold: true },
                                        backgroundColor: { red: 0.9, green: 0.9, blue: 0.9 }
                                    }
                                },
                                fields: 'userEnteredFormat(textFormat,backgroundColor)'
                            }
                        },
                        {
                            updateSheetProperties: {
                                properties: {
                                    sheetId: sheet ? sheet.properties.sheetId : 0,
                                    gridProperties: { frozenRowCount: 1 }
                                },
                                fields: 'gridProperties.frozenRowCount'
                            }
                        }
                    ]
                }
            });
        }

        return true;
    } catch (error) {
        console.error('Error ensuring sheet headers:', error);
        throw error;
    }
}

// ===== DATA FORMATTING =====

// Format Firebase data for Google Sheets row
function formatRegistrationData(data) {
    return [
        data.createdAt ? new Date(data.createdAt.toDate()).toLocaleString() : new Date().toLocaleString(),
        data.id || '',
        data.firstName || '',
        data.lastName || '',
        data.phone || '',
        data.email || '',
        data.pastorName || '',
        data.assemblyName || '',
        Array.isArray(data.services) ? data.services.join('; ') : data.services || '',
        data.airportTransport || '',
        data.arrivalDate || '',
        data.arrivalTime || '',
        data.departureDate || '',
        data.departureTime || '',
        data.localTransport || '',
        data.pickupLocation || '',
        data.hasChildren || '',
        data.numChildren || '',
        data.numVBS || '',
        data.numNursery || '',
        data.status || 'pending'
    ];
}

function formatVolunteerData(data) {
    return [
        data.createdAt ? new Date(data.createdAt.toDate()).toLocaleString() : new Date().toLocaleString(),
        data.id || '',
        data.firstName || '',
        data.lastName || '',
        data.phone || '',
        data.email || '',
        Array.isArray(data.committees) ? data.committees.join('; ') : data.committees || '',
        Array.isArray(data.availability) ? data.availability.join('; ') : data.availability || '',
        data.committeeAssignments ? JSON.stringify(data.committeeAssignments) : '',
        data.status || 'pending'
    ];
}

function formatVendorData(data) {
    return [
        data.createdAt ? new Date(data.createdAt.toDate()).toLocaleString() : new Date().toLocaleString(),
        data.id || '',
        data.businessName || '',
        data.website || '',
        data.firstName || '',
        data.lastName || '',
        data.phone || '',
        data.email || '',
        data.pastorName || '',
        data.assemblyName || '',
        data.selling || '',
        data.goodsType || '',
        data.tableStaffed || '',
        Array.isArray(data.availability) ? data.availability.join('; ') : data.availability || '',
        data.approved ? 'Yes' : 'No',
        data.approvalNotes || '',
        data.status || 'pending'
    ];
}

// ===== SYNC FUNCTIONS =====

// Add single row to Google Sheets
async function addRowToSheet(formType, data) {
    try {
        const spreadsheetId = GOOGLE_SHEETS_CONFIG.spreadsheetIds[formType];
        const sheetName = formType.charAt(0).toUpperCase() + formType.slice(1);

        if (!spreadsheetId || spreadsheetId === `YOUR_${formType.toUpperCase()}_SPREADSHEET_ID`) {
            console.warn(`Google Sheets not configured for ${formType}. Skipping sync.`);
            return false;
        }

        // Ensure headers exist
        await ensureSheetHeaders(spreadsheetId, sheetName, SHEET_HEADERS[formType]);

        // Format data based on form type
        let rowData;
        switch (formType) {
            case 'registrations':
                rowData = formatRegistrationData(data);
                break;
            case 'volunteers':
                rowData = formatVolunteerData(data);
                break;
            case 'vendors':
                rowData = formatVendorData(data);
                break;
            default:
                throw new Error(`Unknown form type: ${formType}`);
        }

        // Append row to sheet
        await gapi.client.sheets.spreadsheets.values.append({
            spreadsheetId: spreadsheetId,
            range: `${sheetName}!A:Z`,
            valueInputOption: 'RAW',
            insertDataOption: 'INSERT_ROWS',
            resource: {
                values: [rowData]
            }
        });

        console.log(`Row added to ${formType} Google Sheet`);
        return true;
    } catch (error) {
        console.error(`Error adding row to ${formType} sheet:`, error);
        // Don't throw - form submission should succeed even if Sheets sync fails
        return false;
    }
}

// Sync all data from Firebase to Google Sheets (for admin use)
async function syncAllDataToSheets(formType) {
    try {
        const spreadsheetId = GOOGLE_SHEETS_CONFIG.spreadsheetIds[formType];
        const sheetName = formType.charAt(0).toUpperCase() + formType.slice(1);

        if (!spreadsheetId || spreadsheetId === `YOUR_${formType.toUpperCase()}_SPREADSHEET_ID`) {
            throw new Error(`Google Sheets not configured for ${formType}`);
        }

        // Ensure headers exist
        await ensureSheetHeaders(spreadsheetId, sheetName, SHEET_HEADERS[formType]);

        // Get all data from Firebase
        let allData;
        switch (formType) {
            case 'registrations':
                allData = await getAllRegistrations();
                break;
            case 'volunteers':
                allData = await getAllVolunteers();
                break;
            case 'vendors':
                allData = await getAllVendors();
                break;
            default:
                throw new Error(`Unknown form type: ${formType}`);
        }

        // Format all data
        const formattedData = allData.map(data => {
            switch (formType) {
                case 'registrations':
                    return formatRegistrationData(data);
                case 'volunteers':
                    return formatVolunteerData(data);
                case 'vendors':
                    return formatVendorData(data);
            }
        });

        // Clear existing data (except headers) and add new data
        await gapi.client.sheets.spreadsheets.values.clear({
            spreadsheetId: spreadsheetId,
            range: `${sheetName}!A2:Z`
        });

        if (formattedData.length > 0) {
            await gapi.client.sheets.spreadsheets.values.append({
                spreadsheetId: spreadsheetId,
                range: `${sheetName}!A2`,
                valueInputOption: 'RAW',
                resource: {
                    values: formattedData
                }
            });
        }

        console.log(`Synced ${formattedData.length} rows to ${formType} Google Sheet`);
        return formattedData.length;
    } catch (error) {
        console.error(`Error syncing ${formType} to sheets:`, error);
        throw error;
    }
}

// ===== PUBLIC API =====

// Initialize on page load (if Google API scripts are loaded)
if (typeof gapi !== 'undefined') {
    initGoogleSheetsAPI();
}

if (typeof google !== 'undefined' && google.accounts) {
    initGoogleIdentityServices();
}

// Check if Google Sheets is configured
function isGoogleSheetsConfigured() {
    return GOOGLE_SHEETS_CONFIG.apiKey !== 'YOUR_GOOGLE_API_KEY' &&
           GOOGLE_SHEETS_CONFIG.clientId !== 'YOUR_CLIENT_ID.apps.googleusercontent.com';
}

// Export functions for use in other scripts
window.GoogleSheetsService = {
    addRowToSheet,
    syncAllDataToSheets,
    requestGoogleSheetsAuth,
    isGoogleSheetsConfigured,
    ensureSheetHeaders
};
