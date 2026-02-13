// ===== GOOGLE SHEETS SERVICE =====
// Handles syncing form submissions to Google Sheets using client-side API

window.GoogleSheetsService = {
    /**
     * Check if Google Sheets is properly configured
     * For client-side approach, we need API key, client ID, and initialized gapi
     */
    isGoogleSheetsConfigured() {
        // Check if Google Sheets config exists
        if (typeof GOOGLE_SHEETS_CONFIG === 'undefined') {
            console.warn('Google Sheets configuration not found');
            return false;
        }

        // Check if API key and client ID are configured
        if (!GOOGLE_SHEETS_CONFIG.apiKey || !GOOGLE_SHEETS_CONFIG.clientId) {
            console.warn('Google Sheets API key or Client ID not configured');
            return false;
        }

        // Check if gapi is loaded
        if (typeof gapi === 'undefined' || !gapi.client) {
            console.warn('Google API client not loaded');
            return false;
        }

        return true;
    },

    /**
     * Add a row to the specified Google Sheet via client-side API
     * @param {string} formType - Type of form (registrations, vendors, volunteers)
     * @param {object} data - Form data to add
     */
    async addRowToSheet(formType, data) {
        if (!this.isGoogleSheetsConfigured()) {
            console.warn('Google Sheets not configured - skipping sync');
            return;
        }

        try {
            // Ensure user is authenticated (silent if already authenticated)
            if (!isGoogleAuthenticated()) {
                console.log('Not authenticated, skipping Google Sheets sync for form submission');
                return;
            }

            // Format data for Google Sheets based on form type
            const row = this.formatDataForSheet(formType, data);

            // Get spreadsheet ID for the form type
            const spreadsheetId = GOOGLE_SHEETS_CONFIG.spreadsheetIds[formType];
            if (!spreadsheetId) {
                throw new Error(`No spreadsheet ID configured for ${formType}`);
            }

            // Append row to sheet using Google Sheets API
            const response = await gapi.client.sheets.spreadsheets.values.append({
                spreadsheetId: spreadsheetId,
                range: 'Sheet1!A:Z',
                valueInputOption: 'RAW',
                insertDataOption: 'INSERT_ROWS',
                resource: {
                    values: [row]
                }
            });

            console.log('✅ Successfully synced to Google Sheets:', response.result);
            return response;
        } catch (error) {
            console.error('❌ Google Sheets sync error:', error);
            // Don't throw - form was already submitted successfully
        }
    },

    /**
     * Sync all data for a section to Google Sheets
     * @param {string} section - Section name (registrations, volunteers, vendors)
     * @returns {number} - Number of records synced
     */
    async syncAllDataToSheets(section) {
        if (!this.isGoogleSheetsConfigured()) {
            throw new Error('Google Sheets not configured. Please check API key and Client ID.');
        }

        // Request OAuth authentication (requires user interaction)
        try {
            await requestGoogleAuth();
        } catch (error) {
            throw new Error('Failed to authenticate with Google. Please try again.');
        }

        // Get data from global variables based on section
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
            default:
                throw new Error(`Unknown section: ${section}`);
        }

        if (data.length === 0) {
            throw new Error(`No ${section} data to sync`);
        }

        // Get spreadsheet ID for the section
        const spreadsheetId = GOOGLE_SHEETS_CONFIG.spreadsheetIds[section];
        if (!spreadsheetId) {
            throw new Error(`No spreadsheet ID configured for ${section}`);
        }

        // Format all data rows
        const formattedRows = data.map(record => this.formatDataForSheet(section, record));

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

        try {
            console.log(`🔄 Syncing ${formattedRows.length} ${section} records to Google Sheets...`);

            // Clear existing data
            console.log('🗑️ Clearing existing data...');
            await gapi.client.sheets.spreadsheets.values.clear({
                spreadsheetId: spreadsheetId,
                range: 'Sheet1!A:Z'
            });

            // Prepare data with headers
            const allRows = [
                headers[section],
                ...formattedRows
            ];

            // Write all data at once
            console.log(`📝 Writing ${allRows.length} rows (including header)...`);
            const response = await gapi.client.sheets.spreadsheets.values.update({
                spreadsheetId: spreadsheetId,
                range: 'Sheet1!A1',
                valueInputOption: 'RAW',
                resource: {
                    values: allRows
                }
            });

            console.log(`✅ Successfully synced ${formattedRows.length} records to Google Sheets`);
            console.log(`📊 Spreadsheet URL: https://docs.google.com/spreadsheets/d/${spreadsheetId}/edit`);

            return formattedRows.length;
        } catch (error) {
            console.error('❌ Google Sheets bulk sync error:', error);

            // Provide more specific error messages based on error status
            const status = error.status || error.code;

            if (status === 404) {
                throw new Error(`Spreadsheet not found. Please verify the spreadsheet ID is correct.`);
            } else if (status === 403) {
                throw new Error(`Permission denied. Please ensure you have edit access to the spreadsheet.`);
            } else if (status === 401) {
                throw new Error(`Authentication failed. Please sign in again.`);
            } else if (status === 400) {
                throw new Error(`Invalid request: ${error.message}`);
            } else if (status === 429) {
                throw new Error(`Google Sheets API quota exceeded. Please try again later.`);
            } else {
                throw new Error(error.message || 'Failed to sync to Google Sheets');
            }
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
                    timestamp,
                    data.id || '',
                    data.firstName || '',
                    data.lastName || '',
                    data.phone || '',
                    data.email || '',
                    data.pastorName || '',
                    data.assemblyName || '',
                    Array.isArray(data.services) ? data.services.join(', ') : data.services || '',
                    data.airportTransport || '',
                    data.localTransport || '',
                    data.hasChildren || '',
                    data.numChildren || '',
                    data.vbsAttendance || '',
                    data.nurseryAttendance || ''
                ];

            case 'vendors':
                return [
                    timestamp,
                    data.id || '',
                    data.businessName || '',
                    data.firstName || '',
                    data.lastName || '',
                    data.phone || '',
                    data.email || '',
                    data.website || '',
                    data.pastorName || '',
                    data.assemblyName || '',
                    data.selling || '',
                    data.goodsType || '',
                    data.tableStaffed || '',
                    Array.isArray(data.availability) ? data.availability.join(', ') : data.availability || '',
                    data.status || 'pending',
                    data.approved ? 'Yes' : 'No'
                ];

            case 'volunteers':
                return [
                    timestamp,
                    data.id || '',
                    data.firstName || '',
                    data.lastName || '',
                    data.phone || '',
                    data.email || '',
                    Array.isArray(data.committees) ? data.committees.join(', ') : data.committees || '',
                    Array.isArray(data.availability) ? data.availability.join(', ') : data.availability || '',
                    data.committeeAssignments || ''
                ];

            default:
                console.warn('Unknown form type:', formType);
                return [];
        }
    }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { GoogleSheetsService: window.GoogleSheetsService };
}
