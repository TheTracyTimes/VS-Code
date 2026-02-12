/**
 * Script to create an admin user in Firebase Authentication
 *
 * Usage:
 *   node create-admin.js <email> <password>
 *
 * Example:
 *   node create-admin.js admin@sarasota-gospel-temple.org MySecurePassword123!
 */

const admin = require('firebase-admin');
const dotenv = require('dotenv');

// Load environment variables
dotenv.config({ path: '../.env' });

// Initialize Firebase Admin SDK
try {
    // Parse the service account JSON from environment variable
    const serviceAccount = JSON.parse(process.env.GOOGLE_SERVICE_ACCOUNT_JSON || '{}');

    admin.initializeApp({
        credential: admin.credential.cert(serviceAccount),
        projectId: serviceAccount.project_id
    });

    console.log('✓ Firebase Admin SDK initialized successfully');
} catch (error) {
    console.error('✗ Error initializing Firebase Admin SDK:', error.message);
    console.error('\nMake sure GOOGLE_SERVICE_ACCOUNT_JSON is set in your .env file');
    process.exit(1);
}

async function createAdminUser(email, password) {
    try {
        // Validate input
        if (!email || !password) {
            throw new Error('Email and password are required');
        }

        if (password.length < 6) {
            throw new Error('Password must be at least 6 characters long');
        }

        // Check if user already exists
        try {
            const existingUser = await admin.auth().getUserByEmail(email);
            console.log(`\n⚠️  User with email ${email} already exists!`);
            console.log(`   UID: ${existingUser.uid}`);
            console.log(`   Created: ${existingUser.metadata.creationTime}`);

            // Ask if they want to update the password
            const readline = require('readline').createInterface({
                input: process.stdin,
                output: process.stdout
            });

            const answer = await new Promise((resolve) => {
                readline.question('\nDo you want to reset the password? (yes/no): ', (answer) => {
                    readline.close();
                    resolve(answer.toLowerCase());
                });
            });

            if (answer === 'yes' || answer === 'y') {
                await admin.auth().updateUser(existingUser.uid, {
                    password: password
                });
                console.log('\n✓ Password updated successfully!');
                console.log(`\nAdmin user details:`);
                console.log(`   Email: ${email}`);
                console.log(`   UID: ${existingUser.uid}`);
                return;
            } else {
                console.log('\n✗ Operation cancelled');
                process.exit(0);
            }
        } catch (error) {
            if (error.code !== 'auth/user-not-found') {
                throw error;
            }
            // User doesn't exist, continue with creation
        }

        // Create new admin user
        const userRecord = await admin.auth().createUser({
            email: email,
            password: password,
            emailVerified: true,
            disabled: false
        });

        console.log('\n✓ Admin user created successfully!');
        console.log(`\nAdmin user details:`);
        console.log(`   Email: ${email}`);
        console.log(`   UID: ${userRecord.uid}`);
        console.log(`   Created: ${userRecord.metadata.creationTime}`);
        console.log(`\n📝 Next steps:`);
        console.log(`   1. Save these credentials in a secure location`);
        console.log(`   2. Go to ${process.env.FIREBASE_AUTH_DOMAIN || 'your-app-url'}/admin/dashboard.html`);
        console.log(`   3. Login with the email and password you just created`);
        console.log(`\n⚠️  Security reminder:`);
        console.log(`   - Store the password securely`);
        console.log(`   - Use a strong, unique password`);
        console.log(`   - Enable 2FA if possible in Firebase Console`);

    } catch (error) {
        console.error('\n✗ Error creating admin user:', error.message);
        if (error.code) {
            console.error(`   Error code: ${error.code}`);
        }
        process.exit(1);
    }
}

// Get command line arguments
const args = process.argv.slice(2);

if (args.length < 2) {
    console.log('\n📋 Usage: node create-admin.js <email> <password>');
    console.log('\nExample:');
    console.log('   node create-admin.js admin@sarasota-gospel-temple.org MySecurePassword123!');
    console.log('\n⚠️  Password requirements:');
    console.log('   - At least 6 characters (8+ recommended)');
    console.log('   - Use a mix of letters, numbers, and symbols');
    process.exit(1);
}

const [email, password] = args;

// Run the script
createAdminUser(email, password)
    .then(() => {
        console.log('\n✓ Done!');
        process.exit(0);
    })
    .catch((error) => {
        console.error('\n✗ Fatal error:', error.message);
        process.exit(1);
    });
