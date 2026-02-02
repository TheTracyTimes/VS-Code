// ===== VENDOR FORM - JAVASCRIPT =====
// Handles conditional logic, validation, and submission

// Form data object
let formData = {};

// ===== CONDITIONAL LOGIC =====

function toggleGoodsType(show) {
    const goodsTypeField = document.getElementById('goodsTypeField');
    const goodsTypeRadios = document.querySelectorAll('input[name="goodsType"]');

    if (show) {
        // Show goods type field
        goodsTypeField.classList.add('active');
        // Make required
        goodsTypeRadios.forEach(radio => {
            radio.setAttribute('required', 'required');
        });
    } else {
        // Hide goods type field
        goodsTypeField.classList.remove('active');
        // Remove required and clear selection
        goodsTypeRadios.forEach(radio => {
            radio.removeAttribute('required');
            radio.checked = false;
        });
        // Remove any error state
        goodsTypeField.classList.remove('has-error');
    }
}

// ===== VALIDATION =====

function validateForm() {
    let isValid = true;

    // Clear previous errors
    document.querySelectorAll('.error').forEach(el => el.classList.remove('error'));
    document.querySelectorAll('.has-error').forEach(el => el.classList.remove('has-error'));

    // Validate text inputs
    const textInputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="tel"]');
    textInputs.forEach(input => {
        if (input.hasAttribute('required') && !input.value.trim()) {
            input.classList.add('error');
            input.closest('.form-group').classList.add('has-error');
            isValid = false;
        }
    });

    // Validate email format
    const emailInput = document.getElementById('email');
    if (emailInput.value.trim() && !isValidEmail(emailInput.value)) {
        emailInput.classList.add('error');
        emailInput.closest('.form-group').classList.add('has-error');
        isValid = false;
    }

    // Validate phone format
    const phoneInput = document.getElementById('phone');
    if (phoneInput.value.trim() && !isValidPhone(phoneInput.value)) {
        phoneInput.classList.add('error');
        phoneInput.closest('.form-group').classList.add('has-error');
        isValid = false;
    }

    // Validate website (must be valid URL or "N/A")
    const websiteInput = document.getElementById('website');
    if (websiteInput.value.trim() && !isValidWebsite(websiteInput.value)) {
        websiteInput.classList.add('error');
        websiteInput.closest('.form-group').classList.add('has-error');
        isValid = false;
    }

    // Validate what are you selling (radio required)
    const sellingRadios = document.querySelectorAll('input[name="selling"]');
    const sellingChecked = Array.from(sellingRadios).some(r => r.checked);
    if (!sellingChecked) {
        document.querySelector('input[name="selling"]').closest('.form-group').classList.add('has-error');
        isValid = false;
    }

    // Validate goods type (if goods is selected)
    const goodsTypeField = document.getElementById('goodsTypeField');
    if (goodsTypeField.classList.contains('active')) {
        const goodsTypeRadios = document.querySelectorAll('input[name="goodsType"]');
        const goodsTypeChecked = Array.from(goodsTypeRadios).some(r => r.checked);
        if (!goodsTypeChecked) {
            goodsTypeField.classList.add('has-error');
            isValid = false;
        }
    }

    // Validate table staffed (radio required)
    const staffedRadios = document.querySelectorAll('input[name="tableStaffed"]');
    const staffedChecked = Array.from(staffedRadios).some(r => r.checked);
    if (!staffedChecked) {
        document.querySelector('input[name="tableStaffed"]').closest('.form-group').classList.add('has-error');
        isValid = false;
    }

    // Validate availability (at least one must be checked)
    const availabilityCheckboxes = document.querySelectorAll('input[name="availability"]:checked');
    if (availabilityCheckboxes.length === 0) {
        document.querySelector('input[name="availability"]').closest('.form-group').classList.add('has-error');
        isValid = false;
    }

    if (!isValid) {
        // Scroll to first error
        const firstError = document.querySelector('.has-error, .error');
        if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    return isValid;
}

function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function isValidPhone(phone) {
    // Accept various phone formats with country code
    const re = /^\+?[\d\s\-()]+$/;
    return re.test(phone) && phone.replace(/\D/g, '').length >= 10;
}

function isValidWebsite(website) {
    // Allow "N/A" or valid URL
    if (website.toLowerCase().trim() === 'n/a') {
        return true;
    }

    // Simple URL validation
    try {
        const url = new URL(website.startsWith('http') ? website : 'https://' + website);
        return true;
    } catch {
        return false;
    }
}

// ===== FORM SUBMISSION =====

document.getElementById('vendorForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    // Validate form
    if (!validateForm()) {
        return;
    }

    // Get selected selling type
    const sellingRadio = document.querySelector('input[name="selling"]:checked');
    const selling = sellingRadio ? sellingRadio.value : '';

    // Get goods type (if applicable)
    let goodsType = null;
    if (selling === 'Goods') {
        const goodsTypeRadio = document.querySelector('input[name="goodsType"]:checked');
        goodsType = goodsTypeRadio ? goodsTypeRadio.value : null;
    }

    // Get table staffed
    const staffedRadio = document.querySelector('input[name="tableStaffed"]:checked');
    const tableStaffed = staffedRadio ? staffedRadio.value : '';

    // Get availability
    const availabilityCheckboxes = document.querySelectorAll('input[name="availability"]:checked');
    const availability = Array.from(availabilityCheckboxes).map(cb => cb.value);

    // Collect form data
    formData = {
        firstName: document.getElementById('firstName').value.trim(),
        lastName: document.getElementById('lastName').value.trim(),
        businessName: document.getElementById('businessName').value.trim(),
        phone: document.getElementById('phone').value.trim(),
        email: document.getElementById('email').value.trim(),
        website: document.getElementById('website').value.trim(),
        pastorName: document.getElementById('pastorName').value.trim(),
        assemblyName: document.getElementById('assemblyName').value.trim(),
        selling: selling,
        goodsType: goodsType,
        tableStaffed: tableStaffed,
        availability: availability,
        timestamp: new Date().toISOString(),
        type: 'vendor',
        approved: false,
        status: 'pending'
    };

    // Show loading state
    const submitBtn = document.getElementById('submitBtn');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="loading-spinner"></span> Submitting...';

    try {
        // Submit to Firebase
        await submitVendor(formData);

        // Send email notifications
        await sendVendorEmails(formData);

        // Show success message
        document.getElementById('vendorForm').style.display = 'none';
        document.getElementById('successMessage').style.display = 'block';
        document.getElementById('confirmEmail').textContent = formData.email;
        document.getElementById('confirmBusiness').textContent = formData.businessName;
        document.getElementById('confirmName').textContent = `${formData.firstName} ${formData.lastName}`;

        // Scroll to success message
        document.getElementById('successMessage').scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (error) {
        console.error('Error submitting form:', error);
        alert('There was an error submitting your vendor application. Please try again or contact us at 941-800-5211.');
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
});

// ===== EMAIL NOTIFICATIONS =====

async function sendVendorEmails(data) {
    try {
        // Prepare goods details
        const goodsDetails = data.goodsType ? ` (${data.goodsType})` : '';
        const sellingText = `${data.selling}${goodsDetails}`;

        // Admin notification
        const adminTemplateParams = {
            to_email: 'sarasotagospel@gmail.com',
            from_name: data.businessName,
            reply_to: data.email,
            subject: 'New Vendor Application - 2026 International Meeting',
            message: `
New vendor application received:

BUSINESS INFORMATION:
Business Name: ${data.businessName}
Contact: ${data.firstName} ${data.lastName}
Phone: ${data.phone}
Email: ${data.email}
Website: ${data.website}

CHURCH INFORMATION:
Pastor: ${data.pastorName}
Assembly: ${data.assemblyName || 'Not provided'}

VENDOR DETAILS:
Selling: ${sellingText}
Table Staffed: ${data.tableStaffed}
Availability: ${data.availability.join(', ')}

Status: PENDING APPROVAL

Submitted: ${new Date().toLocaleString()}

Please review and approve/deny this application in the admin dashboard.
            `.trim()
        };

        // Confirmation email to vendor
        const confirmTemplateParams = {
            to_email: data.email,
            to_name: `${data.firstName} ${data.lastName}`,
            subject: 'Vendor Application Received - 2026 International Meeting',
            message: `
Dear ${data.firstName} ${data.lastName},

Thank you for your interest in being a vendor at the Sarasota Gospel Temple 2026 International Meeting!

YOUR APPLICATION:
Business: ${data.businessName}
Selling: ${sellingText}
Availability: ${data.availability.join(', ')}

Your application is currently under review. You'll receive an email within 3-5 business days regarding your application status.

If approved, we'll send you additional information including:
- Booth setup details
- Vendor guidelines
- Payment information (if applicable)
- Load-in times

Questions? Call us at 941-800-5211

Blessings,
Sarasota Gospel Temple
            `.trim()
        };

        // Send emails via EmailJS
        if (typeof emailjs !== 'undefined') {
            await emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, adminTemplateParams);
            await emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, confirmTemplateParams);
            console.log('Vendor notification emails sent');
        }
    } catch (error) {
        console.error('Error sending emails:', error);
        // Don't throw - form was still submitted successfully
    }
}

// ===== INITIALIZE =====

document.addEventListener('DOMContentLoaded', function() {
    console.log('Vendor form initialized');

    // Initialize EmailJS
    if (typeof emailjs !== 'undefined') {
        initEmailJS();
    }

    // Set focus on first input
    document.getElementById('firstName').focus();
});
