// ===== ADMIN DASHBOARD JAVASCRIPT =====
// Handles data loading, display, filtering, and export

// Current section
let currentSection = 'registrations';

// Data stores
let registrationsData = [];
let volunteersData = [];
let vendorsData = [];
let contactsData = [];

// ===== AUTHENTICATION =====

document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    try {
        await signInAdmin(email, password);
        document.getElementById('loginSection').style.display = 'none';
        document.getElementById('dashboardSection').style.display = 'block';
        loadAllData();
    } catch (error) {
        document.getElementById('loginError').style.display = 'block';
    }
});

// Check if user is already logged in
onAuthStateChanged(user => {
    if (user) {
        document.getElementById('loginSection').style.display = 'none';
        document.getElementById('dashboardSection').style.display = 'block';
        loadAllData();
    } else {
        document.getElementById('loginSection').style.display = 'block';
        document.getElementById('dashboardSection').style.display = 'none';
    }
});

async function handleLogout() {
    if (confirm('Are you sure you want to logout?')) {
        await signOut();
        location.reload();
    }
}

// ===== DATA LOADING =====

async function loadAllData() {
    await Promise.all([
        loadRegistrations(),
        loadVolunteers(),
        loadVendors(),
        loadContacts()
    ]);
    updateStatistics();
}

async function loadRegistrations() {
    try {
        document.getElementById('registrationsLoading').style.display = 'block';
        document.getElementById('registrationsTable').style.display = 'none';
        document.getElementById('registrationsEmpty').style.display = 'none';

        registrationsData = await getAllRegistrations();
        window.registrationsData = registrationsData; // Expose for Google Sheets sync

        if (registrationsData.length === 0) {
            document.getElementById('registrationsLoading').style.display = 'none';
            document.getElementById('registrationsEmpty').style.display = 'block';
            return;
        }

        displayRegistrations(registrationsData);

        document.getElementById('registrationsLoading').style.display = 'none';
        document.getElementById('registrationsTable').style.display = 'block';
    } catch (error) {
        console.error('Error loading registrations:', error);
        alert('Error loading registrations. Please refresh the page.');
    }
}

async function loadVolunteers() {
    try {
        document.getElementById('volunteersLoading').style.display = 'block';
        document.getElementById('volunteersTable').style.display = 'none';
        document.getElementById('volunteersEmpty').style.display = 'none';

        volunteersData = await getAllVolunteers();
        window.volunteersData = volunteersData; // Expose for Google Sheets sync

        if (volunteersData.length === 0) {
            document.getElementById('volunteersLoading').style.display = 'none';
            document.getElementById('volunteersEmpty').style.display = 'block';
            return;
        }

        displayVolunteers(volunteersData);

        document.getElementById('volunteersLoading').style.display = 'none';
        document.getElementById('volunteersTable').style.display = 'block';
    } catch (error) {
        console.error('Error loading volunteers:', error);
    }
}

async function loadContacts() {
    try {
        document.getElementById('contactsLoading').style.display = 'block';
        document.getElementById('contactsTable').style.display = 'none';
        document.getElementById('contactsEmpty').style.display = 'none';

        contactsData = await getAllContacts();
        window.contactsData = contactsData;

        if (contactsData.length === 0) {
            document.getElementById('contactsLoading').style.display = 'none';
            document.getElementById('contactsEmpty').style.display = 'block';
            return;
        }

        displayContacts(contactsData);

        document.getElementById('contactsLoading').style.display = 'none';
        document.getElementById('contactsTable').style.display = 'block';
    } catch (error) {
        console.error('Error loading contacts:', error);
    }
}

async function loadVendors() {
    try {
        document.getElementById('vendorsLoading').style.display = 'block';
        document.getElementById('vendorsTable').style.display = 'none';
        document.getElementById('vendorsEmpty').style.display = 'none';

        vendorsData = await getAllVendors();
        window.vendorsData = vendorsData; // Expose for Google Sheets sync

        if (vendorsData.length === 0) {
            document.getElementById('vendorsLoading').style.display = 'none';
            document.getElementById('vendorsEmpty').style.display = 'block';
            return;
        }

        displayVendors(vendorsData);

        document.getElementById('vendorsLoading').style.display = 'none';
        document.getElementById('vendorsTable').style.display = 'block';
    } catch (error) {
        console.error('Error loading vendors:', error);
    }
}

// ===== DATA DISPLAY =====

function displayRegistrations(data) {
    const tbody = document.getElementById('registrationsTableBody');
    tbody.innerHTML = '';

    data.forEach(reg => {
        const row = document.createElement('tr');

        // Create cells safely using textContent
        const nameCell = document.createElement('td');
        nameCell.textContent = `${reg.firstName} ${reg.lastName}`;
        row.appendChild(nameCell);

        const phoneCell = document.createElement('td');
        phoneCell.textContent = reg.phone;
        row.appendChild(phoneCell);

        const emailCell = document.createElement('td');
        emailCell.textContent = reg.email || '—';
        row.appendChild(emailCell);

        const pastorCell = document.createElement('td');
        pastorCell.textContent = reg.pastorName;
        row.appendChild(pastorCell);

        const servicesCell = document.createElement('td');
        servicesCell.textContent = Array.isArray(reg.services) ? reg.services.length + ' services' : '—';
        row.appendChild(servicesCell);

        const transportCell = document.createElement('td');
        transportCell.textContent = reg.airportTransport;
        row.appendChild(transportCell);

        const pickupCell = document.createElement('td');
        pickupCell.textContent = reg.pickupLocation || '—';
        row.appendChild(pickupCell);

        const childcareCell = document.createElement('td');
        childcareCell.textContent = reg.hasChildren || '—';
        row.appendChild(childcareCell);

        const dateCell = document.createElement('td');
        dateCell.textContent = formatDate(reg.createdAt);
        row.appendChild(dateCell);

        // Create action links with event listeners (NO inline onclick)
        const actionsCell = document.createElement('td');
        actionsCell.className = 'action-links';

        const viewLink = document.createElement('a');
        viewLink.href = '#';
        viewLink.textContent = 'View';
        viewLink.addEventListener('click', (e) => {
            e.preventDefault();
            viewDetails('registration', reg.id);
        });

        const deleteLink = document.createElement('a');
        deleteLink.href = '#';
        deleteLink.textContent = 'Delete';
        deleteLink.addEventListener('click', (e) => {
            e.preventDefault();
            handleDelete('registrations', reg.id);
        });

        actionsCell.appendChild(viewLink);
        actionsCell.appendChild(document.createTextNode(' | '));
        actionsCell.appendChild(deleteLink);
        row.appendChild(actionsCell);

        tbody.appendChild(row);
    });
}

function displayVolunteers(data) {
    const tbody = document.getElementById('volunteersTableBody');
    tbody.innerHTML = '';

    data.forEach(vol => {
        const row = document.createElement('tr');

        // Create cells safely using textContent
        const nameCell = document.createElement('td');
        nameCell.textContent = `${vol.firstName} ${vol.lastName}`;
        row.appendChild(nameCell);

        const phoneCell = document.createElement('td');
        phoneCell.textContent = vol.phone;
        row.appendChild(phoneCell);

        const emailCell = document.createElement('td');
        emailCell.textContent = vol.email;
        row.appendChild(emailCell);

        const committeesCell = document.createElement('td');
        committeesCell.textContent = Array.isArray(vol.committees) ? vol.committees.join(', ') : vol.committees;
        row.appendChild(committeesCell);

        const availCell = document.createElement('td');
        availCell.textContent = Array.isArray(vol.availability) ? vol.availability.length + ' slots' : '—';
        row.appendChild(availCell);

        const dateCell = document.createElement('td');
        dateCell.textContent = formatDate(vol.createdAt);
        row.appendChild(dateCell);

        // Create action links with event listeners
        const actionsCell = document.createElement('td');
        actionsCell.className = 'action-links';

        const viewLink = document.createElement('a');
        viewLink.href = '#';
        viewLink.textContent = 'View';
        viewLink.addEventListener('click', (e) => {
            e.preventDefault();
            viewDetails('volunteer', vol.id);
        });

        const deleteLink = document.createElement('a');
        deleteLink.href = '#';
        deleteLink.textContent = 'Delete';
        deleteLink.addEventListener('click', (e) => {
            e.preventDefault();
            handleDelete('volunteers', vol.id);
        });

        actionsCell.appendChild(viewLink);
        actionsCell.appendChild(document.createTextNode(' | '));
        actionsCell.appendChild(deleteLink);
        row.appendChild(actionsCell);

        tbody.appendChild(row);
    });
}

function displayVendors(data) {
    const tbody = document.getElementById('vendorsTableBody');
    tbody.innerHTML = '';

    data.forEach(vendor => {
        const statusClass = vendor.approved ? 'status-approved' : 'status-pending';
        const statusText = vendor.approved ? 'Approved' : 'Pending';

        const row = document.createElement('tr');

        // Create cells safely using textContent
        const businessCell = document.createElement('td');
        businessCell.textContent = vendor.businessName;
        row.appendChild(businessCell);

        const nameCell = document.createElement('td');
        nameCell.textContent = `${vendor.firstName} ${vendor.lastName}`;
        row.appendChild(nameCell);

        const phoneCell = document.createElement('td');
        phoneCell.textContent = vendor.phone;
        row.appendChild(phoneCell);

        const emailCell = document.createElement('td');
        emailCell.textContent = vendor.email;
        row.appendChild(emailCell);

        const sellingCell = document.createElement('td');
        sellingCell.textContent = vendor.selling || '—';
        row.appendChild(sellingCell);

        const statusCell = document.createElement('td');
        const statusBadge = document.createElement('span');
        statusBadge.className = `status-badge ${statusClass}`;
        statusBadge.textContent = statusText;
        statusCell.appendChild(statusBadge);
        row.appendChild(statusCell);

        const dateCell = document.createElement('td');
        dateCell.textContent = formatDate(vendor.createdAt);
        row.appendChild(dateCell);

        // Create action links with event listeners
        const actionsCell = document.createElement('td');
        actionsCell.className = 'action-links';

        const viewLink = document.createElement('a');
        viewLink.href = '#';
        viewLink.textContent = 'View';
        viewLink.addEventListener('click', (e) => {
            e.preventDefault();
            viewDetails('vendor', vendor.id);
        });

        actionsCell.appendChild(viewLink);

        if (!vendor.approved) {
            actionsCell.appendChild(document.createTextNode(' | '));
            const approveLink = document.createElement('a');
            approveLink.href = '#';
            approveLink.textContent = 'Approve';
            approveLink.addEventListener('click', (e) => {
                e.preventDefault();
                approveVendor(vendor.id);
            });
            actionsCell.appendChild(approveLink);
        }

        actionsCell.appendChild(document.createTextNode(' | '));
        const deleteLink = document.createElement('a');
        deleteLink.href = '#';
        deleteLink.textContent = 'Delete';
        deleteLink.addEventListener('click', (e) => {
            e.preventDefault();
            handleDelete('vendors', vendor.id);
        });

        actionsCell.appendChild(deleteLink);
        row.appendChild(actionsCell);

        tbody.appendChild(row);
    });
}

function displayContacts(data) {
    const tbody = document.getElementById('contactsTableBody');
    tbody.innerHTML = '';

    data.forEach(contact => {
        const row = document.createElement('tr');

        const nameCell = document.createElement('td');
        nameCell.textContent = contact.name || '—';
        row.appendChild(nameCell);

        const emailCell = document.createElement('td');
        emailCell.textContent = contact.email || '—';
        row.appendChild(emailCell);

        const phoneCell = document.createElement('td');
        phoneCell.textContent = contact.phone || '—';
        row.appendChild(phoneCell);

        const messageCell = document.createElement('td');
        const msg = contact.message || '—';
        messageCell.textContent = msg.length > 60 ? msg.substring(0, 60) + '…' : msg;
        row.appendChild(messageCell);

        const dateCell = document.createElement('td');
        dateCell.textContent = formatDate(contact.createdAt);
        row.appendChild(dateCell);

        const actionsCell = document.createElement('td');
        actionsCell.className = 'action-links';

        const viewLink = document.createElement('a');
        viewLink.href = '#';
        viewLink.textContent = 'View';
        viewLink.addEventListener('click', (e) => {
            e.preventDefault();
            viewDetails('contact', contact.id);
        });

        const deleteLink = document.createElement('a');
        deleteLink.href = '#';
        deleteLink.textContent = 'Delete';
        deleteLink.addEventListener('click', (e) => {
            e.preventDefault();
            handleDelete('contacts', contact.id);
        });

        actionsCell.appendChild(viewLink);
        actionsCell.appendChild(document.createTextNode(' | '));
        actionsCell.appendChild(deleteLink);
        row.appendChild(actionsCell);

        tbody.appendChild(row);
    });
}

// ===== STATISTICS =====

function updateStatistics() {
    document.getElementById('totalRegistrations').textContent = registrationsData.length;
    document.getElementById('totalVolunteers').textContent = volunteersData.length;
    document.getElementById('totalVendors').textContent = vendorsData.length;
    document.getElementById('totalContacts').textContent = contactsData.length;

    const needsTransport = registrationsData.filter(r => r.airportTransport === 'Yes').length;
    document.getElementById('needsTransport').textContent = needsTransport;

    const needsChildcare = registrationsData.filter(r => r.hasChildren === 'Yes').length;
    document.getElementById('needsChildcare').textContent = needsChildcare;
}

// ===== SECTION NAVIGATION =====

function showSection(section) {
    // Update active button
    document.querySelectorAll('.dashboard-nav button').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');

    // Hide all sections
    document.querySelectorAll('.section-content').forEach(sec => {
        sec.classList.remove('active');
    });

    // Show selected section
    document.getElementById(`${section}-section`).classList.add('active');

    currentSection = section;
}

// ===== SEARCH FUNCTIONALITY =====

function searchTable(tableId, searchTerm) {
    const tbody = document.querySelector(`#${tableId} tbody`);
    if (!tbody) return;

    const rows = tbody.getElementsByTagName('tr');
    const term = searchTerm.toLowerCase();

    Array.from(rows).forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(term) ? '' : 'none';
    });
}

// ===== REFRESH DATA =====

async function refreshData(section) {
    if (section === 'registrations') {
        await loadRegistrations();
    } else if (section === 'volunteers') {
        await loadVolunteers();
    } else if (section === 'vendors') {
        await loadVendors();
    } else if (section === 'contacts') {
        await loadContacts();
    }
    updateStatistics();
}

// ===== VIEW DETAILS =====

// Field order matching each form's input sequence
const FIELD_ORDER = {
    contact: [
        'name', 'email', 'phone', 'message', 'createdAt'
    ],
    registration: [
        'firstName', 'lastName', 'phone', 'email', 'pastorName', 'assemblyName',
        'services', 'airportTransport', 'travelingAlone', 'howManyPeople',
        'arrivalDate', 'arrivalTime', 'arrivalAirline', 'arrivalAirport', 'arrivalFlight',
        'departureDate', 'departureTime', 'departureAirline', 'departureAirport', 'departureFlight',
        'localTransport', 'pickupLocation', 'hasChildren',
        'vbsAttendance', 'vbsChildren', 'nurseryAttendance', 'nurseryChildren', 'createdAt'
    ],
    volunteer: [
        'firstName', 'lastName', 'phone', 'email', 'pastorName', 'assemblyName',
        'committees', 'principalInstrument', 'availability', 'committeeAssignments', 'createdAt'
    ],
    vendor: [
        'firstName', 'lastName', 'businessName', 'phone', 'email', 'website',
        'pastorName', 'assemblyName', 'selling', 'goodsType',
        'tableStaffed', 'availability', 'status', 'approved', 'createdAt'
    ]
};

function viewDetails(type, id) {
    let data;
    if (type === 'registration') {
        data = registrationsData.find(r => r.id === id);
    } else if (type === 'volunteer') {
        data = volunteersData.find(v => v.id === id);
    } else if (type === 'vendor') {
        data = vendorsData.find(v => v.id === id);
    } else if (type === 'contact') {
        data = contactsData.find(c => c.id === id);
    }

    if (!data) {
        alert('Record not found');
        return;
    }

    // Open new window first
    const modal = window.open('', 'Details', 'width=700,height=600');
    if (!modal) {
        alert('Please allow popups to view details');
        return;
    }

    // Create safe content structure
    const doc = modal.document;
    doc.open();
    doc.write(`
        <html>
        <head>
            <title>Details</title>
            <style>
                body { font-family: 'Source Serif Pro', Georgia, serif; padding: 20px; }
                h2 { color: #28478a; }
                p { margin: 8px 0; line-height: 1.6; }
                strong { color: #4d4d4d; }
            </style>
        </head>
        <body>
            <div id="content" style="max-width: 600px; max-height: 80vh; overflow-y: auto; padding: 20px;"></div>
        </body>
        </html>
    `);
    doc.close();

    // Build content safely using DOM methods
    const contentDiv = doc.getElementById('content');
    const title = doc.createElement('h2');
    title.textContent = 'Details';
    title.style.marginTop = '0';
    contentDiv.appendChild(title);

    // Use defined field order for this form type, then append any extra fields not in the list
    const orderedKeys = FIELD_ORDER[type] || [];
    const allKeys = Object.keys(data).filter(k => k !== 'id');
    const extraKeys = allKeys.filter(k => !orderedKeys.includes(k));
    const displayKeys = [...orderedKeys, ...extraKeys];

    for (const key of displayKeys) {
        if (!(key in data)) continue;
        const value = data[key];

        let displayValue = value;
        if (Array.isArray(value)) {
            displayValue = value.join(', ');
        } else if (typeof value === 'object' && value !== null) {
            if (value.toDate && typeof value.toDate === 'function') {
                displayValue = formatDate(value);
            } else {
                displayValue = JSON.stringify(value, null, 2);
            }
        } else if (key === 'createdAt') {
            displayValue = formatDate(value);
        }

        const label = key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase());

        const p = doc.createElement('p');
        const strong = doc.createElement('strong');
        strong.textContent = label + ': ';
        p.appendChild(strong);
        p.appendChild(doc.createTextNode(displayValue || '—'));
        contentDiv.appendChild(p);
    }
}

// ===== APPROVE VENDOR =====

async function approveVendor(vendorId) {
    if (!confirm('Approve this vendor?')) return;

    try {
        await updateVendorStatus(vendorId, true);
        alert('Vendor approved!');
        await loadVendors();
        updateStatistics();
    } catch (error) {
        console.error('Error approving vendor:', error);
        alert('Error approving vendor');
    }
}

// ===== DELETE RECORD =====

async function handleDelete(collection, docId) {
    if (!confirm('Are you sure you want to delete this record? This cannot be undone.')) {
        return;
    }

    try {
        await deleteRecord(collection, docId);
        alert('Record deleted successfully');

        // Reload appropriate section
        if (collection === 'registrations') {
            await loadRegistrations();
        } else if (collection === 'volunteers') {
            await loadVolunteers();
        } else if (collection === 'vendors') {
            await loadVendors();
        } else if (collection === 'contacts') {
            await loadContacts();
        }

        updateStatistics();
    } catch (error) {
        console.error('Error deleting record:', error);
        alert('Error deleting record');
    }
}

// ===== EXPORT TO EXCEL =====

function exportData(section) {
    let data, filename;

    if (section === 'registrations') {
        data = registrationsData;
        filename = `registrations-${getDateString()}.csv`;
    } else if (section === 'volunteers') {
        data = volunteersData;
        filename = `volunteers-${getDateString()}.csv`;
    } else if (section === 'vendors') {
        data = vendorsData;
        filename = `vendors-${getDateString()}.csv`;
    } else if (section === 'contacts') {
        data = contactsData;
        filename = `contacts-${getDateString()}.csv`;
    }

    if (!data || data.length === 0) {
        alert('No data to export');
        return;
    }

    // Flatten data for export
    const flattenedData = data.map(item => flattenObject(item));

    exportToCSV(flattenedData, filename);
}

// Helper function to flatten nested objects
function flattenObject(obj, prefix = '') {
    let result = {};

    for (const [key, value] of Object.entries(obj)) {
        const newKey = prefix ? `${prefix}_${key}` : key;

        if (Array.isArray(value)) {
            result[newKey] = value.join('; ');
        } else if (typeof value === 'object' && value !== null && !(value instanceof Date)) {
            // Handle Firestore timestamp
            if (value.toDate && typeof value.toDate === 'function') {
                result[newKey] = formatDate(value);
            } else {
                Object.assign(result, flattenObject(value, newKey));
            }
        } else if (key === 'createdAt') {
            result[newKey] = formatDate(value);
        } else {
            result[newKey] = value;
        }
    }

    return result;
}

// ===== UTILITY FUNCTIONS =====

function formatDate(timestamp) {
    if (!timestamp) return '—';

    let date;
    if (timestamp.toDate && typeof timestamp.toDate === 'function') {
        date = timestamp.toDate();
    } else if (timestamp instanceof Date) {
        date = timestamp;
    } else if (typeof timestamp === 'string') {
        date = new Date(timestamp);
    } else {
        return '—';
    }

    const month  = String(date.getMonth() + 1).padStart(2, '0');
    const day    = String(date.getDate()).padStart(2, '0');
    const year   = date.getFullYear();
    const raw    = date.getHours();
    const ampm   = raw >= 12 ? 'PM' : 'AM';
    const hours  = String(raw % 12 || 12).padStart(2, '0');
    const mins   = String(date.getMinutes()).padStart(2, '0');
    const secs   = String(date.getSeconds()).padStart(2, '0');

    return `${month}/${day}/${year} ${hours}:${mins}:${secs} ${ampm}`;
}

function getDateString() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// ===== GOOGLE SHEETS SYNC =====

async function syncToGoogleSheets(section, btn) {
    if (!window.GoogleSheetsService) {
        alert('Google Sheets integration is not loaded. Please check your configuration.');
        return;
    }

    if (!window.GoogleSheetsService.isGoogleSheetsConfigured()) {
        alert('Google Sheets API is not ready.\n\nPlease check:\n1. Google Sheets API key and Client ID are set\n2. The page has finished loading\n3. Try refreshing the page');
        return;
    }

    // Show loading state
    const originalText = btn ? btn.textContent : '';
    if (btn) {
        btn.disabled = true;
        btn.textContent = 'Syncing...';
    }

    try {
        // Sync all data for this section
        const count = await window.GoogleSheetsService.syncAllDataToSheets(section);

        alert(`Successfully synced ${count} ${section} to Google Sheets!`);

        if (btn) {
            btn.textContent = 'Synced!';
            setTimeout(() => {
                btn.textContent = originalText;
                btn.disabled = false;
            }, 2000);
        }
    } catch (error) {
        console.error('Sync error:', error);
        alert(`Error syncing to Google Sheets: ${error.message || 'Unknown error'}\n\nPlease check:\n1. Spreadsheet IDs are correct\n2. You have edit access to the spreadsheets`);
        if (btn) {
            btn.textContent = originalText;
            btn.disabled = false;
        }
    }
}

// ===== COLUMN SORTING =====

const sortState = {
    registrations: { key: null, dir: 'asc' },
    volunteers:    { key: null, dir: 'asc' },
    vendors:       { key: null, dir: 'asc' },
    contacts:      { key: null, dir: 'asc' }
};

function getSortValue(item, key) {
    switch (key) {
        case 'name':
            return (`${item.firstName || item.name || ''} ${item.lastName || ''}`).toLowerCase().trim();
        case 'services':
            return Array.isArray(item.services) ? item.services.length : 0;
        case 'committees':
            return Array.isArray(item.committees) ? item.committees.join(', ').toLowerCase() : String(item.committees || '').toLowerCase();
        case 'availability':
            return Array.isArray(item.availability) ? item.availability.length : 0;
        case 'approved':
            return item.approved ? 1 : 0;
        case 'createdAt': {
            const ts = item.createdAt;
            if (!ts) return 0;
            if (ts.toDate) return ts.toDate().getTime();
            if (ts instanceof Date) return ts.getTime();
            if (typeof ts === 'string') return new Date(ts).getTime();
            return 0;
        }
        default:
            return String(item[key] || '').toLowerCase();
    }
}

function sortTable(tableKey, sortKey) {
    const state = sortState[tableKey];
    if (state.key === sortKey) {
        state.dir = state.dir === 'asc' ? 'desc' : 'asc';
    } else {
        state.key = sortKey;
        state.dir = 'asc';
    }

    // Update arrow indicators
    document.querySelectorAll(`th[data-table="${tableKey}"]`).forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
        if (th.getAttribute('data-sort-key') === sortKey) {
            th.classList.add(state.dir === 'asc' ? 'sort-asc' : 'sort-desc');
        }
    });

    const dir = state.dir === 'asc' ? 1 : -1;
    const compare = (a, b) => {
        const av = getSortValue(a, sortKey);
        const bv = getSortValue(b, sortKey);
        if (av < bv) return -1 * dir;
        if (av > bv) return  1 * dir;
        return 0;
    };

    if (tableKey === 'registrations') {
        registrationsData.sort(compare);
        displayRegistrations(registrationsData);
    } else if (tableKey === 'volunteers') {
        volunteersData.sort(compare);
        displayVolunteers(volunteersData);
    } else if (tableKey === 'vendors') {
        vendorsData.sort(compare);
        displayVendors(vendorsData);
    } else if (tableKey === 'contacts') {
        contactsData.sort(compare);
        displayContacts(contactsData);
    }
}

// ===== INITIALIZE =====

// Set up event listeners after DOM loads
document.addEventListener('DOMContentLoaded', () => {
    // Logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }

    // Navigation buttons
    const navButtons = document.querySelectorAll('.dashboard-nav button');
    navButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const section = this.getAttribute('data-section');
            if (section) {
                showSection(section);
            }
        });
    });

    // Search boxes
    const searchInputs = document.querySelectorAll('input[data-table]');
    searchInputs.forEach(input => {
        input.addEventListener('keyup', function() {
            const tableId = this.getAttribute('data-table');
            searchTable(tableId, this.value);
        });
    });

    // Sortable column headers
    document.querySelectorAll('th[data-sort-key]').forEach(th => {
        th.addEventListener('click', function() {
            sortTable(this.getAttribute('data-table'), this.getAttribute('data-sort-key'));
        });
    });

    // Action buttons (export, sync, refresh)
    const actionButtons = document.querySelectorAll('button[data-action]');
    actionButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            const action = this.getAttribute('data-action');
            const section = this.getAttribute('data-section');

            if (action === 'export') {
                exportData(section);
            } else if (action === 'sync') {
                syncToGoogleSheets(section, this);
            } else if (action === 'refresh') {
                refreshData(section);
            }
        });
    });
});

console.log('Admin dashboard initialized');
