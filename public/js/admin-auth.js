// ===== ADMIN AUTHENTICATION & DATA ACCESS =====
// Provides authentication and Firestore data access functions for admin dashboard

// ===== AUTHENTICATION FUNCTIONS =====

/**
 * Sign in admin user with email and password
 * @param {string} email - Admin email
 * @param {string} password - Admin password
 * @returns {Promise<firebase.User>}
 */
async function signInAdmin(email, password) {
    try {
        const userCredential = await auth.signInWithEmailAndPassword(email, password);
        return userCredential.user;
    } catch (error) {
        console.error('Error signing in:', error);
        throw error;
    }
}

/**
 * Sign out current admin user
 * @returns {Promise<void>}
 */
async function signOut() {
    try {
        await auth.signOut();
    } catch (error) {
        console.error('Error signing out:', error);
        throw error;
    }
}

/**
 * Listen to authentication state changes
 * @param {function} callback - Callback function to receive user object
 */
function onAuthStateChanged(callback) {
    auth.onAuthStateChanged(callback);
}

// ===== DATA RETRIEVAL FUNCTIONS =====

/**
 * Get all registrations from Firestore
 * @returns {Promise<Array>}
 */
async function getAllRegistrations() {
    try {
        const snapshot = await db.collection('registrations').orderBy('createdAt', 'desc').get();
        const registrations = [];

        snapshot.forEach(doc => {
            registrations.push({
                id: doc.id,
                ...doc.data()
            });
        });

        return registrations;
    } catch (error) {
        console.error('Error fetching registrations:', error);
        throw error;
    }
}

/**
 * Get all volunteers from Firestore
 * @returns {Promise<Array>}
 */
async function getAllVolunteers() {
    try {
        const snapshot = await db.collection('volunteers').orderBy('createdAt', 'desc').get();
        const volunteers = [];

        snapshot.forEach(doc => {
            volunteers.push({
                id: doc.id,
                ...doc.data()
            });
        });

        return volunteers;
    } catch (error) {
        console.error('Error fetching volunteers:', error);
        throw error;
    }
}

/**
 * Get all vendors from Firestore
 * @returns {Promise<Array>}
 */
async function getAllVendors() {
    try {
        const snapshot = await db.collection('vendors').orderBy('createdAt', 'desc').get();
        const vendors = [];

        snapshot.forEach(doc => {
            vendors.push({
                id: doc.id,
                ...doc.data()
            });
        });

        return vendors;
    } catch (error) {
        console.error('Error fetching vendors:', error);
        throw error;
    }
}

/**
 * Get all contacts from Firestore
 * @returns {Promise<Array>}
 */
async function getAllContacts() {
    try {
        const snapshot = await db.collection('contacts').orderBy('createdAt', 'desc').get();
        const contacts = [];

        snapshot.forEach(doc => {
            contacts.push({
                id: doc.id,
                ...doc.data()
            });
        });

        return contacts;
    } catch (error) {
        console.error('Error fetching contacts:', error);
        throw error;
    }
}

// ===== DATA MODIFICATION FUNCTIONS =====

/**
 * Delete a record from Firestore
 * @param {string} collection - Collection name (registrations, volunteers, vendors)
 * @param {string} docId - Document ID to delete
 * @returns {Promise<void>}
 */
async function deleteRecord(collection, docId) {
    try {
        // Check if user is authenticated
        const user = auth.currentUser;
        if (!user) {
            throw new Error('User not authenticated');
        }

        await db.collection(collection).doc(docId).delete();
    } catch (error) {
        console.error('Error deleting record:', error);
        throw error;
    }
}

/**
 * Update vendor approval status
 * @param {string} vendorId - Vendor document ID
 * @param {boolean} approved - Approval status
 * @returns {Promise<void>}
 */
async function updateVendorStatus(vendorId, approved) {
    try {
        // Check if user is authenticated
        const user = auth.currentUser;
        if (!user) {
            throw new Error('User not authenticated');
        }

        await db.collection('vendors').doc(vendorId).update({
            approved: approved,
            approvedAt: firebase.firestore.FieldValue.serverTimestamp(),
            approvedBy: user.email
        });
    } catch (error) {
        console.error('Error updating vendor status:', error);
        throw error;
    }
}

// Make functions available globally (for compatibility with existing code)
window.signInAdmin = signInAdmin;
window.signOut = signOut;
window.onAuthStateChanged = onAuthStateChanged;
window.getAllRegistrations = getAllRegistrations;
window.getAllVolunteers = getAllVolunteers;
window.getAllVendors = getAllVendors;
window.getAllContacts = getAllContacts;
window.deleteRecord = deleteRecord;
window.updateVendorStatus = updateVendorStatus;

console.log('Admin authentication and data access initialized');
