// Global type declarations for external libraries loaded via CDN

// Firebase
declare var firebase: any;
declare var db: any;
declare var auth: any;

// EmailJS
declare var emailjs: any;
declare var EMAILJS_SERVICE_ID: string;
declare var EMAILJS_PUBLIC_KEY: string;
declare var EMAILJS_TEMPLATE_IDS: {
    registration: string;
    vendor: string;
    volunteer: string;
};
declare function initEmailJS(): void;

// Google APIs
declare var gapi: any;
declare var GOOGLE_SHEETS_CONFIG: any;
declare function requestGoogleAuth(): Promise<void>;

// Firebase service functions (from firebase-service.js)
declare function submitRegistration(data: any): Promise<string>;
declare function submitVendor(data: any): Promise<string>;
declare function submitVolunteer(data: any): Promise<string>;
declare function submitContact(data: any): Promise<string>;

// Admin auth functions (from admin-auth.js)
declare function signInAdmin(email: string, password: string): Promise<any>;
declare function signOut(): Promise<void>;
declare function onAuthStateChanged(callback: (user: any) => void): void;
declare function getAllRegistrations(): Promise<any[]>;
declare function getAllVolunteers(): Promise<any[]>;
declare function getAllVendors(): Promise<any[]>;
declare function updateVendorStatus(vendorId: string, approved: boolean): Promise<void>;

// CSV export utility
declare function exportToCSV(data: any[], filename: string): void;

// Extend Window interface for custom properties
interface Window {
    // Firebase service functions
    submitRegistration: (data: any) => Promise<string>;
    submitVendor: (data: any) => Promise<string>;
    submitVolunteer: (data: any) => Promise<string>;
    submitContact: (data: any) => Promise<string>;

    // Admin auth functions
    signInAdmin: (email: string, password: string) => Promise<any>;
    signOut: () => Promise<void>;
    onAuthStateChanged: (callback: (user: any) => void) => void;
    getAllRegistrations: () => Promise<any[]>;
    getAllVolunteers: () => Promise<any[]>;
    getAllVendors: () => Promise<any[]>;
    deleteRecord: (collection: string, docId: string) => Promise<void>;
    updateVendorStatus: (vendorId: string, approved: boolean) => Promise<void>;

    // EmailJS config
    EMAILJS_SERVICE_ID: string;
    EMAILJS_PUBLIC_KEY: string;
    EMAILJS_TEMPLATE_IDS: {
        registration: string;
        vendor: string;
        volunteer: string;
    };

    // Security utilities
    RateLimiter: any;
    CSRFProtection: any;
    FormValidator: any;
    DataMasking: any;
    XSSProtection: any;

    // Google Sheets service
    GoogleSheetsService: any;

    // Data stores (exposed from admin dashboard)
    registrationsData: any[];
    volunteersData: any[];
    vendorsData: any[];
    contactsData: any[];
}
