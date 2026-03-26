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
        // Deduplicate array fields (e.g. services) corrupted by the back/forward glitch
        registrationsData.forEach(reg => {
            if (Array.isArray(reg.services)) {
                reg.services = [...new Set(reg.services)];
            }
        });
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

        const servicesCell = document.createElement('td');
        servicesCell.textContent = Array.isArray(reg.services) ? reg.services.length + ' services' : '—';
        row.appendChild(servicesCell);

        const transportCell = document.createElement('td');
        transportCell.textContent = reg.airportTransport;
        row.appendChild(transportCell);

        const pickupCell = document.createElement('td');
        pickupCell.textContent = reg.localTransport || '—';
        row.appendChild(pickupCell);

        const nurseryCell = document.createElement('td');
        nurseryCell.textContent = reg.nurseryAttendance || '—';
        row.appendChild(nurseryCell);

        const vbsCell = document.createElement('td');
        vbsCell.textContent = reg.vbsAttendance || '—';
        row.appendChild(vbsCell);

        const dateCell = document.createElement('td');
        dateCell.textContent = formatDate(reg.createdAt);
        row.appendChild(dateCell);

        // Create action links with event listeners (NO inline onclick)
        const actionsCell = document.createElement('td');
        actionsCell.className = 'action-links';

        const viewLink = document.createElement('a');
        viewLink.href = '#';
        viewLink.textContent = 'View';
        viewLink.addEventListener('click', (e) => { e.preventDefault(); viewDetails('registration', reg.id); });

        const editLink = document.createElement('a');
        editLink.href = '#';
        editLink.textContent = 'Edit';
        editLink.addEventListener('click', (e) => { e.preventDefault(); editRecord('registration', reg.id); });

        const deleteLink = document.createElement('a');
        deleteLink.href = '#';
        deleteLink.textContent = 'Delete';
        deleteLink.addEventListener('click', (e) => { e.preventDefault(); handleDelete('registrations', reg.id); });

        actionsCell.appendChild(viewLink);
        actionsCell.appendChild(document.createTextNode(' | '));
        actionsCell.appendChild(editLink);
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
        viewLink.addEventListener('click', (e) => { e.preventDefault(); viewDetails('volunteer', vol.id); });

        const editLink = document.createElement('a');
        editLink.href = '#';
        editLink.textContent = 'Edit';
        editLink.addEventListener('click', (e) => { e.preventDefault(); editRecord('volunteer', vol.id); });

        const deleteLink = document.createElement('a');
        deleteLink.href = '#';
        deleteLink.textContent = 'Delete';
        deleteLink.addEventListener('click', (e) => { e.preventDefault(); handleDelete('volunteers', vol.id); });

        actionsCell.appendChild(viewLink);
        actionsCell.appendChild(document.createTextNode(' | '));
        actionsCell.appendChild(editLink);
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
        viewLink.addEventListener('click', (e) => { e.preventDefault(); viewDetails('vendor', vendor.id); });

        const editLink = document.createElement('a');
        editLink.href = '#';
        editLink.textContent = 'Edit';
        editLink.addEventListener('click', (e) => { e.preventDefault(); editRecord('vendor', vendor.id); });

        actionsCell.appendChild(viewLink);
        actionsCell.appendChild(document.createTextNode(' | '));
        actionsCell.appendChild(editLink);

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
        viewLink.addEventListener('click', (e) => { e.preventDefault(); viewDetails('contact', contact.id); });

        const editLink = document.createElement('a');
        editLink.href = '#';
        editLink.textContent = 'Edit';
        editLink.addEventListener('click', (e) => { e.preventDefault(); editRecord('contact', contact.id); });

        const deleteLink = document.createElement('a');
        deleteLink.href = '#';
        deleteLink.textContent = 'Delete';
        deleteLink.addEventListener('click', (e) => { e.preventDefault(); handleDelete('contacts', contact.id); });

        actionsCell.appendChild(viewLink);
        actionsCell.appendChild(document.createTextNode(' | '));
        actionsCell.appendChild(editLink);
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

    const needsNursery = registrationsData.filter(r => r.nurseryAttendance === 'Yes').length;
    document.getElementById('needsNursery').textContent = needsNursery;

    const needsVBS = registrationsData.filter(r => r.vbsAttendance === 'Yes').length;
    document.getElementById('needsVBS').textContent = needsVBS;

    const needsPickup = registrationsData.filter(r => r.localTransport === 'Yes').length;
    document.getElementById('needsPickup').textContent = needsPickup;
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

// ===== EDIT RECORD =====

const EDITABLE_FIELDS = {
    registration: [
        'firstName', 'lastName', 'phone', 'email', 'pastorName', 'assemblyName',
        'services', 'airportTransport', 'travelingAlone', 'howManyPeople',
        'arrivalDate', 'arrivalTime', 'arrivalAirline', 'arrivalAirport', 'arrivalFlight',
        'departureDate', 'departureTime', 'departureAirline', 'departureAirport', 'departureFlight',
        'localTransport', 'pickupLocation', 'hasChildren',
        'vbsAttendance', 'vbsChildren', 'nurseryAttendance', 'nurseryChildren'
    ],
    volunteer: [
        'firstName', 'lastName', 'phone', 'email', 'pastorName', 'assemblyName',
        'committees', 'principalInstrument', 'availability'
    ],
    vendor: [
        'firstName', 'lastName', 'businessName', 'phone', 'email', 'website',
        'pastorName', 'assemblyName', 'selling', 'goodsType', 'tableStaffed', 'availability'
    ],
    contact: [
        'name', 'email', 'phone', 'message'
    ]
};

let editContext = { type: null, id: null, collection: null };

function editRecord(type, id) {
    let data, collection;
    if (type === 'registration') { data = registrationsData.find(r => r.id === id); collection = 'registrations'; }
    else if (type === 'volunteer')  { data = volunteersData.find(v => v.id === id);    collection = 'volunteers'; }
    else if (type === 'vendor')     { data = vendorsData.find(v => v.id === id);       collection = 'vendors'; }
    else if (type === 'contact')    { data = contactsData.find(c => c.id === id);      collection = 'contacts'; }

    if (!data) { alert('Record not found'); return; }

    editContext = { type, id, collection, data };

    document.getElementById('editModalTitle').textContent =
        'Edit ' + type.charAt(0).toUpperCase() + type.slice(1);

    const fieldsDiv = document.getElementById('editModalFields');
    fieldsDiv.innerHTML = '';

    (EDITABLE_FIELDS[type] || []).forEach(key => {
        const value = data[key];
        const group = document.createElement('div');
        group.className = 'form-group';

        const lbl = document.createElement('label');
        lbl.textContent = key.replace(/([A-Z])/g, ' $1').replace(/^./, s => s.toUpperCase());
        group.appendChild(lbl);

        let input;
        if (key === 'message' || key === 'pickupLocation') {
            input = document.createElement('textarea');
            input.rows = 3;
        } else {
            input = document.createElement('input');
            input.type = 'text';
        }
        input.id = `edit_${key}`;
        input.value = Array.isArray(value) ? value.join(', ') : (value != null ? value : '');
        group.appendChild(input);
        fieldsDiv.appendChild(group);
    });

    document.getElementById('editModal').style.display = 'flex';
}

async function saveEditRecord() {
    const { type, id, collection, data } = editContext;
    if (!type || !id) return;

    const updates = {};
    (EDITABLE_FIELDS[type] || []).forEach(key => {
        const input = document.getElementById(`edit_${key}`);
        if (!input) return;
        updates[key] = Array.isArray(data[key])
            ? input.value.split(',').map(s => s.trim()).filter(Boolean)
            : input.value;
    });

    const saveBtn = document.getElementById('editModalSave');
    saveBtn.disabled = true;
    saveBtn.textContent = 'Saving...';

    try {
        await updateRecord(collection, id, updates);
        document.getElementById('editModal').style.display = 'none';
        if (collection === 'registrations') await loadRegistrations();
        else if (collection === 'volunteers') await loadVolunteers();
        else if (collection === 'vendors')   await loadVendors();
        else if (collection === 'contacts')  await loadContacts();
        updateStatistics();
    } catch (error) {
        console.error('Error saving record:', error);
        alert('Error saving changes. Please try again.');
    } finally {
        saveBtn.disabled = false;
        saveBtn.textContent = 'Save Changes';
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

// ===== CHARTS =====

let serviceChartInstance           = null;
let committeeChartInstance         = null;
let registrationGroupChartInstance = null;
let volunteerGroupChartInstance    = null;

// Two-round duplicate detection (round 1 = pastor names, round 2 = assembly names)
let registrationRound = 'pastor'; // 'pastor' | 'assembly' | 'complete'
let volunteerRound    = 'pastor';
const dismissedRegPastor   = new Set();
const dismissedRegAssembly = new Set();
const dismissedVolPastor   = new Set();
const dismissedVolAssembly = new Set();

// Persisted dismissals loaded from Firestore (survive page refresh)
const savedDismissals = {
    registrationPastor:   new Set(),
    registrationAssembly: new Set(),
    volunteerPastor:      new Set(),
    volunteerAssembly:    new Set()
};

// Admin merge decisions — stored in Firestore adminSettings, never modifies user submissions
const savedMerges = {
    registrationPastor:   {},
    registrationAssembly: {},
    volunteerPastor:      {},
    volunteerAssembly:    {}
};

const CHART_PALETTE = [
    '#28478a','#c45508','#2a6496','#e07020','#1b6ca8',
    '#8b4513','#2e8b57','#8b008b','#b8860b','#4682b4',
    '#dc143c','#20b2aa','#ff8c00','#6a5acd','#3cb371',
    '#cd5c5c','#40e0d0','#daa520','#7b68ee','#32cd32'
];

function getPaletteColors(n) {
    const colors = [];
    for (let i = 0; i < n; i++) colors.push(CHART_PALETTE[i % CHART_PALETTE.length]);
    return colors;
}

function normalizePastorName(raw) {
    if (!raw) return '';
    return raw
        .normalize('NFD').replace(/[\u0300-\u036f]/g, '')   // é→e, è→e, à→a, etc.
        .replace(/\b(pastor|pasteur|past|pas|pst|bro|brother|rev|reverend|elder|eld|deacon|min|minister)\b\.?/gi, '')
        .replace(/[.,]/g, '')
        .replace(/\s+/g, ' ')
        .trim()
        .toLowerCase();
}

// Levenshtein distance for typo detection
function levenshtein(a, b) {
    const m = a.length, n = b.length;
    const dp = Array.from({ length: m + 1 }, (_, i) => [i]);
    for (let j = 1; j <= n; j++) dp[0][j] = j;
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            dp[i][j] = a[i-1] === b[j-1]
                ? dp[i-1][j-1]
                : 1 + Math.min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]);
        }
    }
    return dp[m][n];
}

function normalizeAssemblyName(raw) {
    if (!raw) return '';
    // Minimal normalization: lowercase and clean punctuation only
    // (do NOT strip church title words here — abbreviations like GOTK use them)
    return raw
        .normalize('NFD').replace(/[\u0300-\u036f]/g, '')   // é→e, è→e, à→a, etc.
        .replace(/[.,#&()']/g, '')
        .replace(/\s+/g, ' ')
        .trim()
        .toLowerCase();
}

function isSimilarPastorName(a, b) {
    if (!a || !b || a === b) return false;
    const wa = a.split(' ').filter(Boolean);
    const wb = b.split(' ').filter(Boolean);
    const [shorter, longer] = wa.length <= wb.length ? [wa, wb] : [wb, wa];
    // Exact word match: all words of shorter name appear in longer
    if (shorter.length > 0 && shorter.every(w => longer.includes(w))) return true;
    // Conjunction-stripped match: remove French/English conjunctions ("et"/"and") then retry.
    // Handles entries like "Exavier et Rosage" vs "Exavier Noël Rosage Beauzil"
    // where someone wrote two names joined by "et" instead of the full combined name.
    const conj = new Set(['et', 'and']);
    if (wa.some(w => conj.has(w)) || wb.some(w => conj.has(w))) {
        const wac = wa.filter(w => !conj.has(w));
        const wbc = wb.filter(w => !conj.has(w));
        const [shorterC, longerC] = wac.length <= wbc.length ? [wac, wbc] : [wbc, wac];
        if (shorterC.length > 0 && shorterC.every(w => longerC.includes(w))) return true;
    }
    // Different-surname guard: if both names have ≥2 words and their last names are
    // clearly different (beyond a typo), they are different people — don't flag.
    // e.g. "Theodate Desrivieres" vs "Theodore Smith" → different surnames → skip.
    // Same or near-identical surnames (e.g. "Jacque"/"Jacques") still proceed.
    if (wa.length >= 2 && wb.length >= 2) {
        const lastA = wa[wa.length - 1];
        const lastB = wb[wb.length - 1];
        const maxLastDist = Math.min(lastA.length, lastB.length) <= 5 ? 1 : 2;
        if (levenshtein(lastA, lastB) > maxLastDist) return false;
    }
    // Typo match: any word pair within edit distance 1-2 (min word length 4 to avoid false positives)
    for (const sw of shorter) {
        if (sw.length < 4) continue;
        for (const lw of longer) {
            if (lw.length < 4) continue;
            const dist = levenshtein(sw, lw);
            const maxDist = sw.length <= 5 ? 1 : 2;
            if (dist > 0 && dist <= maxDist) return true;
        }
    }
    // Nickname/prefix match: a word is the start of a longer word (e.g. "Theo" → "Theodate")
    for (const sw of shorter) {
        if (sw.length < 4) continue;
        for (const lw of longer) {
            if (lw.length > sw.length && lw.startsWith(sw)) return true;
        }
    }
    return false;
}

function isSimilarAssemblyName(a, b) {
    if (!a || !b || a === b) return false;

    // Abbreviation check: one entry is 2–6 lowercase letters that match the
    // first-letter initials of the other entry's words (exact order or anagram).
    // e.g. "cfga" matches "christian family gospel assembly" → c·f·g·a (exact)
    //      "gotk" matches "gospel tabernacle of kissimmee" → g·t·o·k (anagram {g,o,t,k})
    const checkAbbrev = (short, full) => {
        if (short.length < 2 || short.length > 6) return false;
        if (!/^[a-z]+$/.test(short)) return false;
        const words = full.split(' ').filter(Boolean);
        if (words.length < short.length) return false;
        const initials = words.map(w => w[0]).join('');
        // Exact-order match: "cfga" → "christian family gospel assembly"
        if (initials === short || initials.startsWith(short)) return true;
        // Anagram match (same letters, any order): "gotk" matches "gospel tabernacle of kissimmee" (g·t·o·k)
        if (initials.length === short.length) {
            const sorted = s => s.split('').sort().join('');
            if (sorted(initials) === sorted(short)) return true;
        }
        return false;
    };

    if (checkAbbrev(a, b) || checkAbbrev(b, a)) return true;

    // Significant-word overlap check (strip common church title words for comparison only)
    const stop = new Set([
        'assembly','gospel','temple','body','christ','church',
        'of','the','god','first','new','and','de','la','le','les',
        'des','du','en','et','christian','family'
    ]);
    const sig = str => str.split(' ').filter(w => w.length > 1 && !stop.has(w));
    const wa = sig(a);
    const wb = sig(b);
    if (!wa.length || !wb.length) return false;
    const [shorter, longer] = wa.length <= wb.length ? [wa, wb] : [wb, wa];
    return shorter.some(w => longer.includes(w));
}

function getCombinedLabel(pastorName, assemblyName) {
    const p = (pastorName || '').replace(/\b(pastor|pasteur)\b\.?/gi, '').replace(/\s+/g, ' ').trim();
    const a = (assemblyName || '').trim();
    if (p && a) return `${p} \u2014 ${a}`;
    return p || a || 'Unknown';
}

function findFlagsForField(data, fieldGetter, normFn, similarFn) {
    const groups = {};
    data.forEach(item => {
        const raw = fieldGetter(item);
        if (!raw) return;
        const norm = normFn(raw);
        if (!norm) return;
        if (!groups[norm]) groups[norm] = { display: raw, count: 0 };
        groups[norm].count++;
    });
    const keys = Object.keys(groups);
    const flags = [];
    for (let i = 0; i < keys.length; i++) {
        for (let j = i + 1; j < keys.length; j++) {
            if (similarFn(keys[i], keys[j])) {
                flags.push({
                    a: groups[keys[i]].display, countA: groups[keys[i]].count,
                    b: groups[keys[j]].display, countB: groups[keys[j]].count,
                    normA: keys[i], normB: keys[j]
                });
            }
        }
    }
    return flags;
}

// Return the display name after applying saved merges (never modifies original records)
function getEffectiveName(rawName, merges, normFn) {
    if (!rawName) return '';
    const norm = normFn(rawName);
    return merges[norm] || rawName;
}

// Load admin merge decisions and dismissals from Firestore (never touches user submissions)
async function loadMergeDecisions() {
    try {
        const [mergeDoc, dismissDoc] = await Promise.all([
            db.collection('adminSettings').doc('merges').get(),
            db.collection('adminSettings').doc('dismissals').get()
        ]);
        if (mergeDoc.exists) {
            const data = mergeDoc.data();
            Object.assign(savedMerges.registrationPastor,   data.registrationPastor   || {});
            Object.assign(savedMerges.registrationAssembly, data.registrationAssembly || {});
            Object.assign(savedMerges.volunteerPastor,      data.volunteerPastor      || {});
            Object.assign(savedMerges.volunteerAssembly,    data.volunteerAssembly    || {});
        }
        if (dismissDoc.exists) {
            const data = dismissDoc.data();
            (data.registrationPastor   || []).forEach(k => { savedDismissals.registrationPastor.add(k);   dismissedRegPastor.add(k);   });
            (data.registrationAssembly || []).forEach(k => { savedDismissals.registrationAssembly.add(k); dismissedRegAssembly.add(k); });
            (data.volunteerPastor      || []).forEach(k => { savedDismissals.volunteerPastor.add(k);      dismissedVolPastor.add(k);   });
            (data.volunteerAssembly    || []).forEach(k => { savedDismissals.volunteerAssembly.add(k);    dismissedVolAssembly.add(k); });
        }
    } catch (e) {
        console.error('Error loading admin settings:', e);
    }
}

// Save a dismissal decision to Firestore so it survives page refresh
async function saveDismissal(chartType, round, pairKey) {
    const key = chartType + round.charAt(0).toUpperCase() + round.slice(1);
    savedDismissals[key].add(pairKey);
    try {
        await db.collection('adminSettings').doc('dismissals').set(
            { [key]: [...savedDismissals[key]] }, { merge: true }
        );
    } catch (e) {
        console.error('Error saving dismissal:', e);
    }
}

// Save a merge decision to adminSettings (never touches registrations/volunteers/vendors records)
async function saveMerge(chartType, round, loserNorm, loserDisplay, winnerDisplay) {
    const key = chartType + round.charAt(0).toUpperCase() + round.slice(1); // e.g. 'registrationPastor'
    savedMerges[key][loserNorm] = winnerDisplay;
    const user = auth && auth.currentUser ? auth.currentUser.email : 'admin';
    try {
        await Promise.all([
            db.collection('adminSettings').doc('merges').set(
                { [key]: savedMerges[key] },
                { merge: true }
            ),
            db.collection('mergeLog').add({
                chartType,
                round,
                mergedFrom: loserDisplay,
                mergedInto: winnerDisplay,
                by: user,
                at: firebase.firestore.FieldValue.serverTimestamp()
            })
        ]);
    } catch (e) {
        console.error('Error saving merge decision:', e);
        alert('Error saving to database: ' + e.message);
    }
}

function renderGroupFlags(containerId, chartType) {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = '';

    const isReg     = chartType === 'registration';
    const data       = isReg ? registrationsData : volunteersData;
    const collection = isReg ? 'registrations'   : 'volunteers';
    const round      = isReg ? registrationRound  : volunteerRound;
    const rerender   = isReg ? renderRegistrationGroupChart : renderVolunteerGroupChart;

    function doReset() {
        // Keep dismissed pairs — only reset round progress to re-scan for new pairs
        if (isReg) {
            registrationRound = 'pastor';
        } else {
            volunteerRound = 'pastor';
        }
        rerender();
    }

    // All done
    if (round === 'complete') {
        const heading = document.createElement('p');
        heading.className = 'flag-heading';
        heading.style.cssText = 'background:#d4edda;border-color:#28a745;color:#155724;display:flex;align-items:center;justify-content:space-between;';
        const span = document.createElement('span');
        span.textContent = '\u2713 All duplicates reviewed (pastor names and assembly names).';
        heading.appendChild(span);
        const btn = document.createElement('button');
        btn.textContent = 'Check Again';
        btn.style.cssText = 'padding:2px 10px;font-size:12px;background:white;color:#155724;border:1px solid #155724;border-radius:4px;cursor:pointer;margin-left:12px;';
        btn.addEventListener('click', doReset);
        heading.appendChild(btn);
        container.appendChild(heading);
        return;
    }

    // Determine field config for current round
    let fieldGetter, normFn, similarFn, dismissed, roundLabel, mergeSet, round_key;
    if (round === 'pastor') {
        mergeSet   = isReg ? savedMerges.registrationPastor   : savedMerges.volunteerPastor;
        fieldGetter = r => getEffectiveName(r.pastorName, mergeSet, normalizePastorName);
        normFn     = normalizePastorName;
        similarFn  = isSimilarPastorName;
        dismissed  = isReg ? dismissedRegPastor   : dismissedVolPastor;
        roundLabel = 'Round 1 \u2014 Similar Pastor Names';
        round_key  = 'pastor';
    } else {
        mergeSet   = isReg ? savedMerges.registrationAssembly : savedMerges.volunteerAssembly;
        fieldGetter = r => getEffectiveName(r.assemblyName, mergeSet, normalizeAssemblyName);
        normFn     = normalizeAssemblyName;
        similarFn  = isSimilarAssemblyName;
        dismissed  = isReg ? dismissedRegAssembly : dismissedVolAssembly;
        roundLabel = 'Round 2 \u2014 Similar Assembly Names';
        round_key  = 'assembly';
    }

    const pairKey = (a, b) => [a, b].sort().join('|||');
    const flags  = findFlagsForField(data, fieldGetter, normFn, similarFn);
    const active = flags.filter(f => !dismissed.has(pairKey(f.normA, f.normB)));

    // Auto-advance if nothing left in this round
    if (!active.length) {
        if (round === 'pastor') {
            if (isReg) registrationRound = 'assembly'; else volunteerRound = 'assembly';
        } else {
            if (isReg) registrationRound = 'complete'; else volunteerRound = 'complete';
        }
        renderGroupFlags(containerId, chartType);
        return;
    }

    // Heading
    const heading = document.createElement('p');
    heading.className = 'flag-heading';
    heading.style.cssText = 'display:flex;align-items:center;justify-content:space-between;';
    const headingText = document.createElement('span');
    headingText.textContent = `\u26A0 ${roundLabel}: ${active.length} potential duplicate${active.length !== 1 ? 's' : ''} \u2014 please confirm:`;
    heading.appendChild(headingText);
    const resetBtn = document.createElement('button');
    resetBtn.textContent = 'Reset';
    resetBtn.style.cssText = 'padding:2px 10px;font-size:12px;background:white;color:#856404;border:1px solid #856404;border-radius:4px;cursor:pointer;margin-left:12px;';
    resetBtn.addEventListener('click', doReset);
    heading.appendChild(resetBtn);
    container.appendChild(heading);

    active.forEach(f => {
        const item = document.createElement('div');
        item.className = 'flag-item';
        item.style.cssText = 'display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap;';

        const text = document.createElement('span');
        text.textContent = `"${f.a}" (${f.countA}) and "${f.b}" (${f.countB}) \u2014 same?`;
        text.style.flex = '1';
        item.appendChild(text);

        const btnWrap = document.createElement('span');
        btnWrap.style.cssText = 'display:flex;gap:6px;flex-shrink:0;';

        const yesBtn = document.createElement('button');
        yesBtn.textContent = 'Yes';
        yesBtn.style.cssText = 'padding:2px 12px;font-size:12px;font-weight:600;background:#28478a;color:white;border:none;border-radius:4px;cursor:pointer;';
        yesBtn.addEventListener('click', () => {
            item.innerHTML = '';
            item.style.cssText = 'display:flex;flex-direction:column;align-items:flex-start;gap:6px;';
            const prompt = document.createElement('span');
            prompt.style.cssText = 'font-size:12px;font-weight:600;color:#856404;';
            prompt.textContent = 'Which name should they fall under?';
            item.appendChild(prompt);
            const btnRow = document.createElement('span');
            btnRow.style.cssText = 'display:flex;gap:6px;flex-wrap:wrap;';
            [{ display: f.a, norm: f.normA }, { display: f.b, norm: f.normB }].forEach(option => {
                const btn = document.createElement('button');
                btn.textContent = option.display;
                btn.style.cssText = 'padding:3px 12px;font-size:12px;font-weight:600;background:#28478a;color:white;border:none;border-radius:4px;cursor:pointer;';
                btn.addEventListener('click', async () => {
                    btn.disabled = true;
                    btn.textContent = 'Saving\u2026';
                    const loserNorm    = option.norm === f.normA ? f.normB : f.normA;
                    const loserDisplay = option.display === f.a ? f.b : f.a;
                    const pk = pairKey(f.normA, f.normB);
                    dismissed.add(pk);
                    await Promise.all([
                        saveMerge(chartType, round_key, loserNorm, loserDisplay, option.display),
                        saveDismissal(chartType, round_key, pk)
                    ]);
                    rerender();
                });
                btnRow.appendChild(btn);
            });
            item.appendChild(btnRow);
        });

        const noBtn = document.createElement('button');
        noBtn.textContent = 'No';
        noBtn.style.cssText = 'padding:2px 12px;font-size:12px;font-weight:600;background:white;color:#28478a;border:1px solid #28478a;border-radius:4px;cursor:pointer;';
        noBtn.addEventListener('click', () => {
            const pk = pairKey(f.normA, f.normB);
            dismissed.add(pk);
            saveDismissal(chartType, round_key, pk);
            rerender();
        });

        btnWrap.appendChild(yesBtn);
        btnWrap.appendChild(noBtn);
        item.appendChild(btnWrap);
        container.appendChild(item);
    });
}
function showChartDetail(panelId, titleId, bodyId, title, registrants, getNote) {
    const panel = document.getElementById(panelId);
    const titleEl = document.getElementById(titleId);
    const tbody = document.getElementById(bodyId);
    if (!panel || !titleEl || !tbody) return;

    titleEl.textContent = title;
    tbody.innerHTML = '';

    registrants.forEach(r => {
        const tr = document.createElement('tr');

        const nameCell = document.createElement('td');
        const fullName = `${r.firstName || ''} ${r.lastName || ''}`.trim() || r.name || '\u2014';
        nameCell.textContent = fullName;

        if (getNote) {
            const note = getNote(r);
            if (note) {
                const sub = document.createElement('div');
                sub.style.cssText = 'font-size:11px;color:#888;font-style:italic;margin-top:2px;';
                sub.textContent = note;
                nameCell.appendChild(sub);
            }
        }

        const emailCell = document.createElement('td');
        emailCell.textContent = r.email || '\u2014';
        const phoneCell = document.createElement('td');
        phoneCell.textContent = r.phone || '\u2014';
        tr.appendChild(nameCell);
        tr.appendChild(emailCell);
        tr.appendChild(phoneCell);
        tbody.appendChild(tr);
    });

    panel.classList.add('visible');
}

function renderServiceChart() {
    const serviceOrder = [
        { key: 'Thursday Morning Service, April 9th',  label: 'Thu Morning' },
        { key: 'Thursday Night Service, April 9th',    label: 'Thu Night' },
        { key: 'Friday Morning Service, April 10th',   label: 'Fri Morning' },
        { key: 'Friday Night Service, April 10th',     label: 'Fri Night' },
        { key: 'Saturday Morning Service, April 11th', label: 'Sat Morning' },
        { key: 'Saturday Youth Night, April 11th',     label: 'Sat Youth Night' }
    ];

    const counts = {};
    registrationsData.forEach(reg => {
        if (Array.isArray(reg.services)) {
            reg.services.forEach(s => { counts[s] = (counts[s] || 0) + 1; });
        }
    });

    const labels = serviceOrder.map(s => s.label);
    const data   = serviceOrder.map(s => counts[s.key] || 0);

    if (serviceChartInstance) serviceChartInstance.destroy();
    const ctx = document.getElementById('serviceChart');
    if (!ctx) return;
    serviceChartInstance = new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: 'Attendees',
                data,
                backgroundColor: getPaletteColors(labels.length),
                borderWidth: 0,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            onClick(e, elements) {
                if (!elements.length) return;
                const idx = elements[0].index;
                const serviceKey = serviceOrder[idx].key;
                const serviceLabel = serviceOrder[idx].label;
                const attendees = registrationsData.filter(r =>
                    Array.isArray(r.services) && r.services.includes(serviceKey)
                );
                showChartDetail('serviceDetail', 'serviceDetailTitle', 'serviceDetailBody',
                    `${serviceLabel} \u2014 ${attendees.length} attendee${attendees.length !== 1 ? 's' : ''}`,
                    attendees);
            },
            plugins: {
                legend: { display: false },
                tooltip: { mode: 'index', intersect: false }
            },
            scales: {
                y: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } }
            }
        }
    });
}

function renderCommitteeChart() {
    const committeeCounts = {};
    volunteersData.forEach(v => {
        const committees = Array.isArray(v.committees) ? v.committees : [];
        committees.forEach(c => { committeeCounts[c] = (committeeCounts[c] || 0) + 1; });
    });

    const sorted = Object.entries(committeeCounts).sort((a, b) => b[1] - a[1]);
    const labels = sorted.map(([k]) => k);
    const data   = sorted.map(([, v]) => v);

    if (committeeChartInstance) committeeChartInstance.destroy();
    const ctx = document.getElementById('committeeChart');
    if (!ctx) return;
    committeeChartInstance = new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: 'Volunteers',
                data,
                backgroundColor: getPaletteColors(labels.length),
                borderWidth: 0,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            onClick(e, elements) {
                if (!elements.length) return;
                const committee = labels[elements[0].index];
                const matches = volunteersData.filter(v =>
                    Array.isArray(v.committees) && v.committees.includes(committee)
                );
                showChartDetail('committeeDetail', 'committeeDetailTitle', 'committeeDetailBody',
                    `${committee} \u2014 ${matches.length} volunteer${matches.length !== 1 ? 's' : ''}`,
                    matches);
            },
            plugins: {
                legend: { display: false },
                tooltip: { mode: 'index', intersect: false }
            },
            scales: {
                y: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } }
            }
        }
    });
}

function renderRegistrationGroupChart() {
    // Group by normalized key so case-only variants (e.g. "new" vs "New") collapse into one slice
    const groups = {}; // normKey → { display, count }
    registrationsData.forEach(r => {
        const ep = getEffectiveName(r.pastorName,  savedMerges.registrationPastor,   normalizePastorName);
        const ea = getEffectiveName(r.assemblyName, savedMerges.registrationAssembly, normalizeAssemblyName);
        const normKey = getCombinedLabel(normalizePastorName(ep), normalizeAssemblyName(ea));
        if (!groups[normKey]) groups[normKey] = { display: getCombinedLabel(ep, ea), count: 0 };
        groups[normKey].count++;
    });
    const sorted = Object.entries(groups).sort((a, b) => b[1].count - a[1].count);

    const regFilter = normKey => registrationsData.filter(r => {
        const ep = getEffectiveName(r.pastorName,  savedMerges.registrationPastor,   normalizePastorName);
        const ea = getEffectiveName(r.assemblyName, savedMerges.registrationAssembly, normalizeAssemblyName);
        return getCombinedLabel(normalizePastorName(ep), normalizeAssemblyName(ea)) === normKey;
    });
    const regNote = r => {
        const notes = [];
        const ep = getEffectiveName(r.pastorName,   savedMerges.registrationPastor,   normalizePastorName);
        const ea = getEffectiveName(r.assemblyName, savedMerges.registrationAssembly, normalizeAssemblyName);
        if (r.pastorName   && ep !== r.pastorName)   notes.push(`Pastor also known as: \u201c${r.pastorName}\u201d`);
        if (r.assemblyName && ea !== r.assemblyName) notes.push(`Assembly also known as: \u201c${r.assemblyName}\u201d`);
        return notes.join(' \u2022 ');
    };

    if (registrationGroupChartInstance) registrationGroupChartInstance.destroy();
    const ctx = document.getElementById('registrationGroupChart');
    if (!ctx) return;
    registrationGroupChartInstance = new Chart(ctx.getContext('2d'), {
        type: 'pie',
        data: {
            labels: sorted.map(([, {display}]) => display),
            datasets: [{ data: sorted.map(([, {count}]) => count), backgroundColor: getPaletteColors(sorted.length), borderWidth: 1 }]
        },
        options: {
            responsive: true,
            onClick(e, elements) {
                if (!elements.length) return;
                const [normKey, {display}] = sorted[elements[0].index];
                const matches = regFilter(normKey);
                showChartDetail('registrationGroupDetail', 'registrationGroupDetailTitle', 'registrationGroupDetailBody',
                    `${display} \u2014 ${matches.length} registrant${matches.length !== 1 ? 's' : ''}`, matches, regNote);
            },
            plugins: {
                legend: { display: false },
                tooltip: { callbacks: { label: c => ` ${c.label}: ${c.raw}` } }
            }
        }
    });
    const regColors = getPaletteColors(sorted.length);
    renderScrollLegend('registrationGroupLegend', sorted.map(([, {display, count}]) => [display, count]), regColors, (_, idx) => {
        const [normKey, {display}] = sorted[idx];
        const matches = regFilter(normKey);
        showChartDetail('registrationGroupDetail', 'registrationGroupDetailTitle', 'registrationGroupDetailBody',
            `${display} \u2014 ${matches.length} registrant${matches.length !== 1 ? 's' : ''}`, matches, regNote);
    });
    renderGroupFlags('registrationGroupFlags', 'registration');
}

function renderVolunteerGroupChart() {
    // Group by normalized key so case-only variants collapse into one slice
    const groups = {}; // normKey → { display, count }
    volunteersData.forEach(v => {
        const ep = getEffectiveName(v.pastorName,  savedMerges.volunteerPastor,   normalizePastorName);
        const ea = getEffectiveName(v.assemblyName, savedMerges.volunteerAssembly, normalizeAssemblyName);
        const normKey = getCombinedLabel(normalizePastorName(ep), normalizeAssemblyName(ea));
        if (!groups[normKey]) groups[normKey] = { display: getCombinedLabel(ep, ea), count: 0 };
        groups[normKey].count++;
    });
    const sorted = Object.entries(groups).sort((a, b) => b[1].count - a[1].count);

    const volFilter = normKey => volunteersData.filter(v => {
        const ep = getEffectiveName(v.pastorName,  savedMerges.volunteerPastor,   normalizePastorName);
        const ea = getEffectiveName(v.assemblyName, savedMerges.volunteerAssembly, normalizeAssemblyName);
        return getCombinedLabel(normalizePastorName(ep), normalizeAssemblyName(ea)) === normKey;
    });
    const volNote = v => {
        const notes = [];
        const ep = getEffectiveName(v.pastorName,   savedMerges.volunteerPastor,   normalizePastorName);
        const ea = getEffectiveName(v.assemblyName, savedMerges.volunteerAssembly, normalizeAssemblyName);
        if (v.pastorName   && ep !== v.pastorName)   notes.push(`Pastor also known as: \u201c${v.pastorName}\u201d`);
        if (v.assemblyName && ea !== v.assemblyName) notes.push(`Assembly also known as: \u201c${v.assemblyName}\u201d`);
        return notes.join(' \u2022 ');
    };

    if (volunteerGroupChartInstance) volunteerGroupChartInstance.destroy();
    const ctx = document.getElementById('volunteerGroupChart');
    if (!ctx) return;
    volunteerGroupChartInstance = new Chart(ctx.getContext('2d'), {
        type: 'pie',
        data: {
            labels: sorted.map(([, {display}]) => display),
            datasets: [{ data: sorted.map(([, {count}]) => count), backgroundColor: getPaletteColors(sorted.length), borderWidth: 1 }]
        },
        options: {
            responsive: true,
            onClick(e, elements) {
                if (!elements.length) return;
                const [normKey, {display}] = sorted[elements[0].index];
                const matches = volFilter(normKey);
                showChartDetail('volunteerGroupDetail', 'volunteerGroupDetailTitle', 'volunteerGroupDetailBody',
                    `${display} \u2014 ${matches.length} volunteer${matches.length !== 1 ? 's' : ''}`, matches, volNote);
            },
            plugins: {
                legend: { display: false },
                tooltip: { callbacks: { label: c => ` ${c.label}: ${c.raw}` } }
            }
        }
    });
    const volColors = getPaletteColors(sorted.length);
    renderScrollLegend('volunteerGroupLegend', sorted.map(([, {display, count}]) => [display, count]), volColors, (_, idx) => {
        const [normKey, {display}] = sorted[idx];
        const matches = volFilter(normKey);
        showChartDetail('volunteerGroupDetail', 'volunteerGroupDetailTitle', 'volunteerGroupDetailBody',
            `${display} \u2014 ${matches.length} volunteer${matches.length !== 1 ? 's' : ''}`, matches, volNote);
    });
    renderGroupFlags('volunteerGroupFlags', 'volunteer');
}

function renderScrollLegend(legendId, sorted, colors, onClickFn) {
    const container = document.getElementById(legendId);
    if (!container) return;
    container.innerHTML = '';
    sorted.forEach(([lbl, count], idx) => {
        const item = document.createElement('div');
        item.className = 'legend-item';

        const swatch = document.createElement('span');
        swatch.className = 'legend-swatch';
        swatch.style.backgroundColor = colors[idx % colors.length];

        const label = document.createElement('span');
        label.className = 'legend-label';
        label.textContent = lbl;
        label.title = lbl;

        const countEl = document.createElement('span');
        countEl.className = 'legend-count';
        countEl.textContent = count;

        item.appendChild(swatch);
        item.appendChild(label);
        item.appendChild(countEl);
        item.addEventListener('click', () => onClickFn(lbl, idx));
        container.appendChild(item);
    });
}

async function renderCharts() {
    await loadMergeDecisions();
    renderServiceChart();
    renderCommitteeChart();
    renderRegistrationGroupChart();
    renderVolunteerGroupChart();
}

// ===== INITIALIZE =====

// Set up event listeners after DOM loads
document.addEventListener('DOMContentLoaded', () => {
    // Logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }

    // Restart duplicate review
    const restartBtn = document.getElementById('restartDuplicateReview');
    if (restartBtn) {
        restartBtn.addEventListener('click', async () => {
            restartBtn.disabled = true;
            restartBtn.textContent = 'Loading…';
            // Reload merges from Firestore so any merges confirmed this session
            // (or by another admin on another device) are included before re-scanning
            await loadMergeDecisions();
            // Keep dismissed pairs — just reset round progress to re-scan for new pairs
            registrationRound = 'pastor';
            volunteerRound    = 'pastor';
            renderRegistrationGroupChart();
            renderVolunteerGroupChart();
            restartBtn.disabled = false;
            restartBtn.textContent = '\u21BB Check for More Duplicates';
        });
    }

    // Clear dismissals button
    const clearDismissalsBtn = document.getElementById('clearDismissals');
    if (clearDismissalsBtn) {
        clearDismissalsBtn.addEventListener('click', async () => {
            if (!confirm('Clear all dismissed duplicate pairs? This will re-surface every pair you previously said "No" to, so you can review them again.')) return;
            clearDismissalsBtn.disabled = true;
            clearDismissalsBtn.textContent = 'Clearing…';
            try {
                await db.collection('adminSettings').doc('dismissals').set({
                    registrationPastor: [], registrationAssembly: [],
                    volunteerPastor: [],    volunteerAssembly: []
                });
                // Clear in-memory sets
                ['registrationPastor','registrationAssembly','volunteerPastor','volunteerAssembly'].forEach(k => {
                    savedDismissals[k].clear();
                });
                dismissedRegPastor.clear();
                dismissedRegAssembly.clear();
                dismissedVolPastor.clear();
                dismissedVolAssembly.clear();
                // Re-render both charts so cleared pairs reappear
                registrationRound = 'pastor';
                volunteerRound    = 'pastor';
                renderRegistrationGroupChart();
                renderVolunteerGroupChart();
            } catch (e) {
                console.error('Error clearing dismissals:', e);
                alert('Failed to clear dismissals. Please try again.');
            }
            clearDismissalsBtn.disabled = false;
            clearDismissalsBtn.textContent = '\u2715 Clear Dismissals';
        });
    }

    // Navigation buttons
    const navButtons = document.querySelectorAll('.dashboard-nav button');
    navButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const section = this.getAttribute('data-section');
            if (section) {
                showSection(section);
                if (section === 'charts') requestAnimationFrame(renderCharts);
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

    // Edit modal buttons
    document.getElementById('editModalSave').addEventListener('click', saveEditRecord);
    document.getElementById('editModalCancel').addEventListener('click', () => {
        document.getElementById('editModal').style.display = 'none';
    });
    document.getElementById('editModalClose').addEventListener('click', () => {
        document.getElementById('editModal').style.display = 'none';
    });
    document.getElementById('editModal').addEventListener('click', (e) => {
        if (e.target === document.getElementById('editModal')) {
            document.getElementById('editModal').style.display = 'none';
        }
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
