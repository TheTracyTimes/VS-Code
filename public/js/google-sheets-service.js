// ===== GOOGLE SHEETS SERVICE =====
// Handles syncing form submissions to Google Sheets using fetch API

const SHEETS_API_BASE = 'https://sheets.googleapis.com/v4/spreadsheets';

// Map section names to actual sheet tab names
const SHEET_TAB_NAMES = {
    registrations: 'Registrations',
    volunteers: 'Volunteers',
    vendors: 'Vendors',
    contacts: 'Contacts'
};

// Helper: check if user has a valid Google OAuth token
function isGoogleAuthenticated() {
    return googleAccessToken !== null;
}

// Helper: request Google OAuth authentication
function requestGoogleAuth() {
    return new Promise((resolve, reject) => {
        if (typeof tokenClient === 'undefined' || !tokenClient) {
            reject(new Error('Google Identity Services not initialized'));
            return;
        }
        tokenClient.callback = (response) => {
            if (response.error) {
                reject(response);
            } else {
                googleAccessToken = response.access_token;
                console.log('Google OAuth token set successfully');
                resolve(response);
            }
        };
        tokenClient.requestAccessToken({ prompt: 'consent' });
    });
}

window.GoogleSheetsService = {
    /**
     * Check if Google Sheets is properly configured
     */
    isGoogleSheetsConfigured() {
        if (typeof GOOGLE_SHEETS_CONFIG === 'undefined') {
            console.warn('Google Sheets configuration not found');
            return false;
        }
        if (!GOOGLE_SHEETS_CONFIG.clientId) {
            console.warn('Google Sheets Client ID not configured');
            return false;
        }
        if (typeof tokenClient === 'undefined' || !tokenClient) {
            console.warn('Google Identity Services not initialized');
            return false;
        }
        return true;
    },

    /**
     * Make an authenticated request to the Google Sheets API
     */
    async sheetsRequest(url, method, body) {
        const headers = {
            'Authorization': `Bearer ${googleAccessToken}`,
            'Content-Type': 'application/json'
        };

        const options = { method, headers };
        if (body) {
            options.body = JSON.stringify(body);
        }

        const response = await fetch(url, options);
        if (!response.ok) {
            const error = await response.json();
            throw { status: response.status, message: error.error?.message || response.statusText };
        }
        return response.json();
    },

    /**
     * Add a row to the specified Google Sheet
     */
    async addRowToSheet(formType, data) {
        if (!this.isGoogleSheetsConfigured()) {
            console.warn('Google Sheets not configured - skipping sync');
            return;
        }

        try {
            if (!isGoogleAuthenticated()) {
                console.log('Not authenticated, skipping Google Sheets sync for form submission');
                return;
            }

            const row = this.formatDataForSheet(formType, data);
            const spreadsheetId = GOOGLE_SHEETS_CONFIG.spreadsheetIds[formType];
            if (!spreadsheetId) {
                throw new Error(`No spreadsheet ID configured for ${formType}`);
            }

            const tabName = SHEET_TAB_NAMES[formType] || 'Sheet1';
            const url = `${SHEETS_API_BASE}/${spreadsheetId}/values/${tabName}!A:Z:append?valueInputOption=RAW&insertDataOption=INSERT_ROWS`;
            const response = await this.sheetsRequest(url, 'POST', { values: [row] });

            console.log('Successfully synced to Google Sheets:', response);
            return response;
        } catch (error) {
            console.error('Google Sheets sync error:', error);
        }
    },

    /**
     * Sync all data for a section to Google Sheets
     */
    async syncAllDataToSheets(section) {
        if (!this.isGoogleSheetsConfigured()) {
            throw new Error('Google Sheets not configured. Please check Client ID.');
        }

        // Request OAuth authentication
        try {
            await requestGoogleAuth();
        } catch (error) {
            throw new Error('Failed to authenticate with Google. Please try again.');
        }

        // Get data from global variables
        let data;
        switch (section) {
            case 'registrations':
                data = window.registrationsData || [];
                break;
            case 'volunteers':
                data = window.volunteersData || [];
                break;
            case 'vendors':
                data = window.vendorsData || [];
                break;
            case 'contacts':
                data = window.contactsData || [];
                break;
            default:
                throw new Error(`Unknown section: ${section}`);
        }

        if (data.length === 0) {
            throw new Error(`No ${section} data to sync`);
        }

        const spreadsheetId = GOOGLE_SHEETS_CONFIG.spreadsheetIds[section];
        if (!spreadsheetId) {
            throw new Error(`No spreadsheet ID configured for ${section}`);
        }

        const tabName = SHEET_TAB_NAMES[section] || 'Sheet1';

        // Ensure the sheet tab exists, create it if not
        await this.ensureSheetTabExists(spreadsheetId, tabName);

        // Format all data rows
        const formattedRows = data.map(record => this.formatDataForSheet(section, record));

        // Define headers
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
            ],
            contacts: [
                'Timestamp', 'ID', 'Name', 'Phone', 'Email', 'Message'
            ]
        };

        try {
            console.log(`Syncing ${formattedRows.length} ${section} records to Google Sheets...`);

            // Clear existing data
            console.log('Clearing existing data...');
            const clearUrl = `${SHEETS_API_BASE}/${spreadsheetId}/values/${tabName}!A:Z:clear`;
            await this.sheetsRequest(clearUrl, 'POST', {});

            // Prepare data with headers
            const allRows = [
                headers[section],
                ...formattedRows
            ];

            // Write all data at once
            console.log(`Writing ${allRows.length} rows (including header)...`);
            const updateUrl = `${SHEETS_API_BASE}/${spreadsheetId}/values/${tabName}!A1?valueInputOption=RAW`;
            await this.sheetsRequest(updateUrl, 'PUT', { values: allRows });

            console.log(`Successfully synced ${formattedRows.length} records to Google Sheets`);
            return formattedRows.length;
        } catch (error) {
            console.error('Google Sheets bulk sync error:', error);

            const status = error.status;
            if (status === 404) {
                throw new Error('Spreadsheet not found. Please verify the spreadsheet ID is correct.');
            } else if (status === 403) {
                throw new Error('Permission denied. Please ensure you have edit access to the spreadsheet.');
            } else if (status === 401) {
                throw new Error('Authentication failed. Please sign in again.');
            } else if (status === 429) {
                throw new Error('Google Sheets API quota exceeded. Please try again later.');
            } else {
                throw new Error(error.message || 'Failed to sync to Google Sheets');
            }
        }
    },

    /**
     * Ensure a sheet tab exists, creating it if it doesn't
     */
    async ensureSheetTabExists(spreadsheetId, tabName) {
        try {
            const metaUrl = `${SHEETS_API_BASE}/${spreadsheetId}?fields=sheets.properties.title`;
            const meta = await this.sheetsRequest(metaUrl, 'GET');
            const exists = meta.sheets && meta.sheets.some(s => s.properties.title === tabName);
            if (!exists) {
                const batchUrl = `${SHEETS_API_BASE}/${spreadsheetId}:batchUpdate`;
                await this.sheetsRequest(batchUrl, 'POST', {
                    requests: [{ addSheet: { properties: { title: tabName } } }]
                });
                console.log(`Created sheet tab: ${tabName}`);
            }
        } catch (error) {
            console.warn('Could not verify/create sheet tab:', error);
        }
    },

    /**
     * Format form data for Google Sheets
     */
    formatDataForSheet(formType, data) {
        const timestamp = data.createdAt && data.createdAt.toDate ?
                         data.createdAt.toDate().toLocaleString() :
                         new Date().toLocaleString();

        switch (formType) {
            case 'registrations':
                return [
                    timestamp, data.id || '',
                    data.firstName || '', data.lastName || '',
                    data.phone || '', data.email || '',
                    data.pastorName || '', data.assemblyName || '',
                    Array.isArray(data.services) ? data.services.join(', ') : data.services || '',
                    data.airportTransport || '', data.localTransport || '',
                    data.hasChildren || '', data.numChildren || '',
                    data.vbsAttendance || '', data.nurseryAttendance || ''
                ];
            case 'vendors':
                return [
                    timestamp, data.id || '',
                    data.businessName || '', data.firstName || '', data.lastName || '',
                    data.phone || '', data.email || '', data.website || '',
                    data.pastorName || '', data.assemblyName || '',
                    data.selling || '', data.goodsType || '',
                    data.tableStaffed || '',
                    Array.isArray(data.availability) ? data.availability.join(', ') : data.availability || '',
                    data.status || 'pending', data.approved ? 'Yes' : 'No'
                ];
            case 'volunteers':
                return [
                    timestamp, data.id || '',
                    data.firstName || '', data.lastName || '',
                    data.phone || '', data.email || '',
                    Array.isArray(data.committees) ? data.committees.join(', ') : data.committees || '',
                    Array.isArray(data.availability) ? data.availability.join(', ') : data.availability || '',
                    data.committeeAssignments && typeof data.committeeAssignments === 'object'
                        ? Object.entries(data.committeeAssignments).map(([slot, comm]) => `${slot}: ${comm}`).join('; ')
                        : data.committeeAssignments || ''
                ];
            case 'contacts':
                return [
                    timestamp, data.id || '',
                    data.name || '', data.phone || '',
                    data.email || '', data.message || ''
                ];
            default:
                return [];
        }
    }
};

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { GoogleSheetsService: window.GoogleSheetsService };
}
