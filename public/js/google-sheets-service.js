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
     * Sync all data for a section to Google Sheets
     * @param {string} section - Section name (registrations, volunteers, vendors)
     * @returns {number} - Number of records synced
     */
    async syncAllDataToSheets(section) {
        if (!this.isGoogleSheetsConfigured()) {
            throw new Error('Google Sheets not configured');
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

        // Format all data rows
        const formattedRows = data.map(record => this.formatDataForSheet(section, record));

        try {
            // Call Firebase Cloud Function to sync all data
            console.log(`Syncing ${formattedRows.length} ${section} records to Google Sheets...`);
            const syncAllToSheet = firebase.functions().httpsCallable('syncAllToSheet');
            const response = await syncAllToSheet({
                formType: section,
                rows: formattedRows
            });

            console.log('Successfully synced all data to Google Sheets:', response.data);
            console.log(`Spreadsheet URL: https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit`);
            return response.data.syncedCount || data.length;
        } catch (error) {
            console.error('Google Sheets bulk sync error details:', {
                message: error.message,
                code: error.code,
                details: error.details,
                fullError: error
            });

            // Provide more specific error messages based on error code
            if (error.code === 'functions/not-found') {
                throw new Error('Firebase Function not deployed. Please deploy functions first.');
            } else if (error.code === 'functions/permission-denied') {
                throw new Error('Permission denied. Check Firebase Secrets configuration.');
            } else if (error.code === 'functions/failed-precondition') {
                // This error includes detailed message about what's missing
                throw new Error(error.message || 'Google Sheets configuration incomplete.');
            } else if (error.code === 'functions/invalid-argument') {
                // Invalid data or request format
                throw new Error(error.message || 'Invalid data format for Google Sheets.');
            } else if (error.code === 'functions/resource-exhausted') {
                // API quota exceeded
                throw new Error(error.message || 'Google Sheets API quota exceeded. Please try again later.');
            } else if (error.code === 'functions/internal') {
                // For internal errors, use the detailed message from the function
                throw new Error(error.message || 'Internal server error. Check Firebase Functions logs.');
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
