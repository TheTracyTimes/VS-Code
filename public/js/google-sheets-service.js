// ===== GOOGLE SHEETS SERVICE =====
// Handles syncing form submissions to Google Sheets

window.GoogleSheetsService = {
    /**
     * Check if Google Sheets is properly configured
     */
    isGoogleSheetsConfigured() {
        return typeof GOOGLE_SHEETS_CONFIG !== 'undefined' &&
               GOOGLE_SHEETS_CONFIG.apiKey &&
               GOOGLE_SHEETS_CONFIG.clientId &&
               GOOGLE_SHEETS_CONFIG.apiKey !== 'your_google_api_key' &&
               GOOGLE_SHEETS_CONFIG.clientId !== 'your_client_id.apps.googleusercontent.com';
    },

    /**
     * Add a row to the specified Google Sheet
     * @param {string} formType - Type of form (registrations, vendors, volunteers)
     * @param {object} data - Form data to add
     */
    async addRowToSheet(formType, data) {
        if (!this.isGoogleSheetsConfigured()) {
            console.warn('Google Sheets not configured - skipping sync');
            return;
        }

        try {
            const spreadsheetId = GOOGLE_SHEETS_CONFIG.spreadsheetIds[formType];
            if (!spreadsheetId) {
                console.warn(`No spreadsheet ID configured for ${formType}`);
                return;
            }

            // Ensure Google API is loaded
            if (typeof gapi === 'undefined' || !gapi.client) {
                console.warn('Google API client not loaded - skipping Google Sheets sync');
                return;
            }

            // Format data for Google Sheets based on form type
            const row = this.formatDataForSheet(formType, data);

            // Append to sheet
            const response = await gapi.client.sheets.spreadsheets.values.append({
                spreadsheetId: spreadsheetId,
                range: 'Sheet1!A:Z', // Adjust range as needed
                valueInputOption: 'USER_ENTERED',
                resource: {
                    values: [row]
                }
            });

            console.log('Successfully synced to Google Sheets:', response);
            return response;
        } catch (error) {
            console.error('Google Sheets sync error:', error);
            // Don't throw - form was already submitted successfully
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
