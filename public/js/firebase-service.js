// ===== FIREBASE SERVICE FUNCTIONS =====
// Handles all Firebase Firestore operations for form submissions

// ===== REGISTRATION SUBMISSIONS =====

async function submitRegistration(data) {
    try {
        // Check if Firebase is initialized
        if (typeof db === 'undefined' || !db) {
            throw new Error('Firebase is not initialized. Please check your configuration.');
        }

        // Add to Firestore
        const docRef = await db.collection('registrations').add({
            ...data,
            createdAt: firebase.firestore.FieldValue.serverTimestamp(),
            updatedAt: firebase.firestore.FieldValue.serverTimestamp()
        });

        console.log('Registration submitted successfully:', docRef.id);
        return docRef.id;
    } catch (error) {
        console.error('Firebase submission error:', error);
        throw new Error('Failed to submit registration: ' + error.message);
    }
}

// ===== VENDOR SUBMISSIONS =====

async function submitVendor(data) {
    try {
        // Check if Firebase is initialized
        if (typeof db === 'undefined' || !db) {
            throw new Error('Firebase is not initialized. Please check your configuration.');
        }

        // Add to Firestore
        const docRef = await db.collection('vendors').add({
            ...data,
            createdAt: firebase.firestore.FieldValue.serverTimestamp(),
            updatedAt: firebase.firestore.FieldValue.serverTimestamp()
        });

        console.log('Vendor application submitted successfully:', docRef.id);
        return docRef.id;
    } catch (error) {
        console.error('Firebase submission error:', error);
        throw new Error('Failed to submit vendor application: ' + error.message);
    }
}

// ===== VOLUNTEER SUBMISSIONS =====

async function submitVolunteer(data) {
    try {
        // Check if Firebase is initialized
        if (typeof db === 'undefined' || !db) {
            throw new Error('Firebase is not initialized. Please check your configuration.');
        }

        // Add to Firestore
        const docRef = await db.collection('volunteers').add({
            ...data,
            createdAt: firebase.firestore.FieldValue.serverTimestamp(),
            updatedAt: firebase.firestore.FieldValue.serverTimestamp()
        });

        console.log('Volunteer registration submitted successfully:', docRef.id);
        return docRef.id;
    } catch (error) {
        console.error('Firebase submission error:', error);
        throw new Error('Failed to submit volunteer registration: ' + error.message);
    }
}

// ===== CONTACT SUBMISSIONS =====

async function submitContact(data) {
    try {
        // Check if Firebase is initialized
        if (typeof db === 'undefined' || !db) {
            throw new Error('Firebase is not initialized. Please check your configuration.');
        }

        // Add to Firestore
        const docRef = await db.collection('contacts').add({
            ...data,
            createdAt: firebase.firestore.FieldValue.serverTimestamp(),
            updatedAt: firebase.firestore.FieldValue.serverTimestamp()
        });

        console.log('Contact form submitted successfully:', docRef.id);
        return docRef.id;
    } catch (error) {
        console.error('Firebase submission error:', error);
        throw new Error('Failed to submit contact form: ' + error.message);
    }
}

// ===== DELETE RECORD =====

async function deleteFirestoreRecord(collection, docId) {
    try {
        if (typeof db === 'undefined' || !db) {
            throw new Error('Firebase is not initialized.');
        }
        await db.collection(collection).doc(docId).delete();
        console.log('Record deleted:', docId);
    } catch (error) {
        console.error('Firebase delete error:', error);
        throw new Error('Failed to delete record: ' + error.message);
    }
}

// Export for use in other scripts
if (typeof window !== 'undefined') {
    window.submitRegistration = submitRegistration;
    window.submitVendor = submitVendor;
    window.submitVolunteer = submitVolunteer;
    window.submitContact = submitContact;
    window.deleteFirestoreRecord = deleteFirestoreRecord;
}
