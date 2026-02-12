// ===== GOOGLE SHEETS SERVICE =====
// Handles syncing form submissions to Google Sheets

window.GoogleSheetsService = {
    /**
     * Check if Google Sheets is properly configured
     * With Firebase Functions approach, we only need Firebase to be initialized
     */
    isGoogleSheetsConfigured() {
        // Check if Firebase Functions is available
        if (typeof firebase === 'undefined' || !firebase.functions) {
            console.warn('Firebase Functions not available - Google Sheets sync disabled');
            return false;
        }

        // If old config exists with spreadsheet IDs, use it
        // Otherwise Firebase Functions will use the IDs from secrets
        return true;
    },

    /**
     * Add a row to the specified Google Sheet via Firebase Cloud Function
     * @param {string} formType - Type of form (registrations, vendors, volunteers)
     * @param {object} data - Form data to add
     */
    async addRowToSheet(formType, data) {
        if (!this.isGoogleSheetsConfigured()) {
            console.warn('Google Sheets not configured - skipping sync');
            return;
        }

        try {
            // Format data for Google Sheets based on form type
            const row = this.formatDataForSheet(formType, data);

            // Call Firebase Cloud Function to append to sheet
            // The function will use spreadsheet IDs from Firebase Secrets
            const appendToSheet = firebase.functions().httpsCallable('appendToSheet');
            const response = await appendToSheet({
                formType: formType,
                rowData: row
            });

            console.log('Successfully synced to Google Sheets:', response.data);
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
