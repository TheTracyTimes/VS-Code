#!/usr/bin/env node

/**
 * Credential Setup Script for Sarasota Gospel Temple Website
 *
 * This script helps you configure credentials from .env file
 * and generates the necessary config files.
 *
 * Usage:
 *   node setup-credentials.js                    # Interactive setup
 *   node setup-credentials.js --from-env         # Load from .env file
 *   node setup-credentials.js --firebase-only    # Only set Firebase Functions config
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const readline = require('readline');

// Color output for terminal
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    red: '\x1b[31m',
    cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

function loadEnvFile() {
    const envPath = path.join(__dirname, '.env');

    if (!fs.existsSync(envPath)) {
        log('❌ .env file not found! Please create one from .env.example', 'red');
        log('Run: cp .env.example .env', 'yellow');
        process.exit(1);
    }

    const envContent = fs.readFileSync(envPath, 'utf-8');
    const env = {};

    envContent.split('\n').forEach(line => {
        line = line.trim();
        if (line && !line.startsWith('#')) {
            const [key, ...valueParts] = line.split('=');
            const value = valueParts.join('=').trim();
            if (key && value && !value.includes('your_') && !value.includes('your-')) {
                env[key] = value;
            }
        }
    });

    return env;
}

function validateCredentials(env) {
    const required = [
        'FIREBASE_API_KEY',
        'FIREBASE_AUTH_DOMAIN',
        'FIREBASE_PROJECT_ID',
        'EMAILJS_SERVICE_ID',
        'EMAILJS_PUBLIC_KEY',
        'GOOGLE_SHEETS_API_KEY',
        'GOOGLE_SHEETS_CLIENT_ID'
    ];

    const missing = required.filter(key => !env[key]);

    if (missing.length > 0) {
        log('❌ Missing required credentials in .env:', 'red');
        missing.forEach(key => log(`  - ${key}`, 'yellow'));
        log('\nPlease update your .env file with actual values', 'yellow');
        return false;
    }

    return true;
}

function generateFirebaseConfig(env) {
    return `// ===== FIREBASE CONFIGURATION =====
// Auto-generated from .env file - DO NOT EDIT MANUALLY
// Run 'node setup-credentials.js' to regenerate

const firebaseConfig = {
    apiKey: "${env.FIREBASE_API_KEY}",
    authDomain: "${env.FIREBASE_AUTH_DOMAIN}",
    projectId: "${env.FIREBASE_PROJECT_ID}",
    storageBucket: "${env.FIREBASE_STORAGE_BUCKET || env.FIREBASE_PROJECT_ID + '.firebasestorage.app'}",
    messagingSenderId: "${env.FIREBASE_MESSAGING_SENDER_ID}",
    appId: "${env.FIREBASE_APP_ID}",
    measurementId: "${env.FIREBASE_MEASUREMENT_ID || ''}"
};

// Initialize Firebase
let db, auth;

try {
    firebase.initializeApp(firebaseConfig);
    db = firebase.firestore();
    auth = firebase.auth();
    console.log('Firebase initialized successfully');
} catch (error) {
    console.error('Firebase initialization error:', error);
}

// ===== EMAILJS CONFIGURATION =====

const EMAILJS_SERVICE_ID = "${env.EMAILJS_SERVICE_ID}";
const EMAILJS_PUBLIC_KEY = "${env.EMAILJS_PUBLIC_KEY}";

// Initialize EmailJS
function initEmailJS() {
    if (typeof emailjs !== 'undefined') {
        emailjs.init(EMAILJS_PUBLIC_KEY);
        console.log('EmailJS initialized');
    }
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initEmailJS);
} else {
    initEmailJS();
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { firebaseConfig, db, auth, EMAILJS_SERVICE_ID, EMAILJS_PUBLIC_KEY };
}
`;
}

function generateGoogleSheetsConfig(env) {
    return `// ===== GOOGLE SHEETS API CONFIGURATION =====
// Auto-generated from .env file - DO NOT EDIT MANUALLY
// Run 'node setup-credentials.js' to regenerate

const GOOGLE_SHEETS_CONFIG = {
    // Your Google Cloud Project API Key (for client-side access)
    apiKey: '${env.GOOGLE_SHEETS_API_KEY}',

    // Your Google Cloud Project Client ID (for OAuth)
    clientId: '${env.GOOGLE_SHEETS_CLIENT_ID}',

    // Google Sheets IDs for each form type
    spreadsheetIds: {
        registrations: '${env.GOOGLE_SHEETS_REGISTRATIONS_ID || ''}',
        volunteers: '${env.GOOGLE_SHEETS_VOLUNTEERS_ID || ''}',
        vendors: '${env.GOOGLE_SHEETS_VENDORS_ID || ''}'
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
`;
}

function setFirebaseFunctionsConfig(env) {
    log('\n📋 Setting Firebase Functions configuration...', 'cyan');

    const commands = [
        `firebase functions:config:set emailjs.service_id="${env.EMAILJS_SERVICE_ID}"`,
        `firebase functions:config:set emailjs.private_key="${env.EMAILJS_PRIVATE_KEY}"`,
        `firebase functions:config:set google.credentials='${env.GOOGLE_SERVICE_ACCOUNT_JSON || '{}'}'`,
        `firebase functions:config:set sheets.registrations_id="${env.GOOGLE_SHEETS_REGISTRATIONS_ID || ''}"`,
        `firebase functions:config:set sheets.volunteers_id="${env.GOOGLE_SHEETS_VOLUNTEERS_ID || ''}"`,
        `firebase functions:config:set sheets.vendors_id="${env.GOOGLE_SHEETS_VENDORS_ID || ''}"`
    ];

    try {
        commands.forEach(cmd => {
            log(`  Running: ${cmd.split('=')[0]}=...`, 'yellow');
            execSync(cmd, { stdio: 'inherit', cwd: __dirname });
        });
        log('✅ Firebase Functions config updated successfully', 'green');
        log('\n💡 To deploy: firebase deploy --only functions', 'cyan');
    } catch (error) {
        log('❌ Error setting Firebase Functions config:', 'red');
        log('Make sure you are logged in: firebase login', 'yellow');
        log('And have selected a project: firebase use --add', 'yellow');
    }
}

function writeConfigFiles(env) {
    log('\n📝 Generating config files...', 'cyan');

    // Generate firebase-config.js
    const firebaseConfigPath = path.join(__dirname, 'config', 'firebase-config.js');
    const firebaseConfig = generateFirebaseConfig(env);
    fs.writeFileSync(firebaseConfigPath, firebaseConfig);
    log(`  ✅ Created ${firebaseConfigPath}`, 'green');

    // Generate google-sheets-config.js
    const sheetsConfigPath = path.join(__dirname, 'config', 'google-sheets-config.js');
    const sheetsConfig = generateGoogleSheetsConfig(env);
    fs.writeFileSync(sheetsConfigPath, sheetsConfig);
    log(`  ✅ Created ${sheetsConfigPath}`, 'green');
}

function main() {
    const args = process.argv.slice(2);
    const fromEnv = args.includes('--from-env');
    const firebaseOnly = args.includes('--firebase-only');

    log('╔════════════════════════════════════════════════════════╗', 'cyan');
    log('║   Sarasota Gospel Temple - Credential Setup Script    ║', 'cyan');
    log('╚════════════════════════════════════════════════════════╝', 'cyan');

    // Load environment variables
    log('\n📂 Loading credentials from .env file...', 'cyan');
    const env = loadEnvFile();

    if (Object.keys(env).length === 0) {
        log('⚠️  No credentials found in .env file', 'yellow');
        log('Please edit .env and add your actual credentials', 'yellow');
        log('See .env.example for the required format', 'yellow');
        process.exit(1);
    }

    log(`  Found ${Object.keys(env).length} credentials`, 'green');

    // Validate credentials
    if (!validateCredentials(env)) {
        process.exit(1);
    }

    log('✅ All required credentials found', 'green');

    // Generate config files
    if (!firebaseOnly) {
        writeConfigFiles(env);
    }

    // Set Firebase Functions config
    if (env.EMAILJS_PRIVATE_KEY || firebaseOnly) {
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });

        rl.question('\n🔧 Do you want to configure Firebase Functions? (y/n): ', (answer) => {
            if (answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes') {
                setFirebaseFunctionsConfig(env);
            } else {
                log('⏭️  Skipping Firebase Functions config', 'yellow');
                log('You can run this later with: node setup-credentials.js --firebase-only', 'cyan');
            }
            rl.close();

            log('\n╔════════════════════════════════════════════════════════╗', 'green');
            log('║              ✅ Setup Complete!                        ║', 'green');
            log('╚════════════════════════════════════════════════════════╝', 'green');
            log('\n📋 Next steps:', 'cyan');
            log('  1. Verify your config files were generated correctly', 'reset');
            log('  2. Test your forms locally', 'reset');
            log('  3. Deploy: firebase deploy --only hosting,functions', 'reset');
            log('\n💡 Tip: Never commit .env to git!', 'yellow');
        });
    } else {
        log('\n╔════════════════════════════════════════════════════════╗', 'green');
        log('║              ✅ Setup Complete!                        ║', 'green');
        log('╚════════════════════════════════════════════════════════╝', 'green');
        log('\n📋 Next steps:', 'cyan');
        log('  1. Verify your config files were generated correctly', 'reset');
        log('  2. Add EMAILJS_PRIVATE_KEY to .env for Firebase Functions', 'reset');
        log('  3. Run: node setup-credentials.js --firebase-only', 'reset');
        log('  4. Deploy: firebase deploy --only hosting,functions', 'reset');
        log('\n💡 Tip: Never commit .env to git!', 'yellow');
    }
}

// Run the script
if (require.main === module) {
    main();
}

module.exports = { loadEnvFile, generateFirebaseConfig, generateGoogleSheetsConfig };
