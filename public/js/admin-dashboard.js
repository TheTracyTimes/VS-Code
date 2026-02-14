// ===== ADMIN DASHBOARD JAVASCRIPT =====
// Handles data loading, display, filtering, and export

// Current section
let currentSection = 'registrations';

// Data stores
let registrationsData = [];
let volunteersData = [];
let vendorsData = [];

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
        loadVendors()
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
            deleteRecord('registrations', reg.id);
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
            deleteRecord('volunteers', vol.id);
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
            deleteRecord('vendors', vendor.id);
        });

        actionsCell.appendChild(deleteLink);
        row.appendChild(actionsCell);

        tbody.appendChild(row);
    });
}

// ===== STATISTICS =====

function updateStatistics() {
    // Total registrations
    document.getElementById('totalRegistrations').textContent = registrationsData.length;

    // Total volunteers
    document.getElementById('totalVolunteers').textContent = volunteersData.length;

    // Total vendors
    document.getElementById('totalVendors').textContent = vendorsData.length;

    // Need airport transport
    const needsTransport = registrationsData.filter(r => r.airportTransport === 'Yes').length;
    document.getElementById('needsTransport').textContent = needsTransport;
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
    }
    updateStatistics();
}

// ===== VIEW DETAILS =====

function viewDetails(type, id) {
    let data;
    if (type === 'registration') {
        data = registrationsData.find(r => r.id === id);
    } else if (type === 'volunteer') {
        data = volunteersData.find(v => v.id === id);
    } else if (type === 'vendor') {
        data = vendorsData.find(v => v.id === id);
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

    for (const [key, value] of Object.entries(data)) {
        if (key === 'id') continue;

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

async function deleteRecord(collection, docId) {
    if (!confirm('Are you sure you want to delete this record? This cannot be undone.')) {
        return;
    }

    try {
        await window.deleteRecord(collection, docId);
        alert('Record deleted successfully');

        // Reload appropriate section
        if (collection === 'registrations') {
            await loadRegistrations();
        } else if (collection === 'volunteers') {
            await loadVolunteers();
        } else if (collection === 'vendors') {
            await loadVendors();
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
    // Handle Firestore timestamp
    if (timestamp.toDate && typeof timestamp.toDate === 'function') {
        date = timestamp.toDate();
    } else if (timestamp instanceof Date) {
        date = timestamp;
    } else if (typeof timestamp === 'string') {
        date = new Date(timestamp);
    } else {
        return '—';
    }

    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

function getDateString() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// ===== GOOGLE SHEETS SYNC =====

async function syncToGoogleSheets(section) {
    if (!window.GoogleSheetsService) {
        alert('Google Sheets integration is not loaded. Please check your configuration.');
        return;
    }

    if (!window.GoogleSheetsService.isGoogleSheetsConfigured()) {
        alert('Google Sheets is not configured yet.\n\nPlease configure Firebase Secrets for Google Sheets integration.');
        return;
    }

    // Show loading state
    const originalText = event.target.textContent;
    event.target.disabled = true;
    event.target.textContent = '⏳ Syncing...';

    try {
        // Sync all data for this section
        const count = await window.GoogleSheetsService.syncAllDataToSheets(section);

        alert(`✅ Successfully synced ${count} ${section} to Google Sheets!`);

        event.target.textContent = '✓ Synced!';
        setTimeout(() => {
            event.target.textContent = originalText;
            event.target.disabled = false;
        }, 2000);
    } catch (error) {
        console.error('Sync error:', error);
        alert(`Error syncing to Google Sheets: ${error.message || 'Unknown error'}\n\nPlease check:\n1. Firebase Secrets are configured\n2. Spreadsheet IDs are correct\n3. Service account has access to spreadsheets`);
        event.target.textContent = originalText;
        event.target.disabled = false;
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

    // Action buttons (export, sync, refresh)
    const actionButtons = document.querySelectorAll('button[data-action]');
    actionButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            const action = this.getAttribute('data-action');
            const section = this.getAttribute('data-section');

            if (action === 'export') {
                exportData(section);
            } else if (action === 'sync') {
                syncToGoogleSheets(section);
            } else if (action === 'refresh') {
                refreshData(section);
            }
        });
    });
});

console.log('Admin dashboard initialized');
