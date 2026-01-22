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
        row.innerHTML = `
            <td>${reg.firstName} ${reg.lastName}</td>
            <td>${reg.phone}</td>
            <td>${reg.email || '—'}</td>
            <td>${reg.pastorName}</td>
            <td>${Array.isArray(reg.services) ? reg.services.length : '—'} services</td>
            <td>${reg.airportTransport}</td>
            <td>${formatDate(reg.createdAt)}</td>
            <td class="action-links">
                <a onclick="viewDetails('registration', '${reg.id}')">View</a>
                <a onclick="deleteRecord('registrations', '${reg.id}')">Delete</a>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function displayVolunteers(data) {
    const tbody = document.getElementById('volunteersTableBody');
    tbody.innerHTML = '';

    data.forEach(vol => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${vol.firstName} ${vol.lastName}</td>
            <td>${vol.phone}</td>
            <td>${vol.email}</td>
            <td>${Array.isArray(vol.committees) ? vol.committees.join(', ') : vol.committees}</td>
            <td>${Array.isArray(vol.availability) ? vol.availability.length : '—'} slots</td>
            <td>${formatDate(vol.createdAt)}</td>
            <td class="action-links">
                <a onclick="viewDetails('volunteer', '${vol.id}')">View</a>
                <a onclick="deleteRecord('volunteers', '${vol.id}')">Delete</a>
            </td>
        `;
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
        row.innerHTML = `
            <td>${vendor.businessName}</td>
            <td>${vendor.firstName} ${vendor.lastName}</td>
            <td>${vendor.phone}</td>
            <td>${vendor.email}</td>
            <td>${vendor.selling || '—'}</td>
            <td><span class="status-badge ${statusClass}">${statusText}</span></td>
            <td>${formatDate(vendor.createdAt)}</td>
            <td class="action-links">
                <a onclick="viewDetails('vendor', '${vendor.id}')">View</a>
                ${!vendor.approved ? `<a onclick="approveVendor('${vendor.id}')">Approve</a>` : ''}
                <a onclick="deleteRecord('vendors', '${vendor.id}')">Delete</a>
            </td>
        `;
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

    // Create modal content
    let content = '<div style="max-width: 600px; max-height: 80vh; overflow-y: auto; padding: 20px;">';
    content += `<h2 style="margin-top: 0;">Details</h2>`;

    for (const [key, value] of Object.entries(data)) {
        if (key === 'id') continue;

        let displayValue = value;
        if (Array.isArray(value)) {
            displayValue = value.join(', ');
        } else if (typeof value === 'object' && value !== null) {
            displayValue = JSON.stringify(value, null, 2);
        } else if (key === 'createdAt') {
            displayValue = formatDate(value);
        }

        const label = key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase());
        content += `<p><strong>${label}:</strong> ${displayValue || '—'}</p>`;
    }

    content += '</div>';

    // Show in alert (basic) - you can create a proper modal
    const modal = window.open('', 'Details', 'width=700,height=600');
    modal.document.write(`
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
        <body>${content}</body>
        </html>
    `);
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

// ===== INITIALIZE =====

console.log('Admin dashboard initialized');
