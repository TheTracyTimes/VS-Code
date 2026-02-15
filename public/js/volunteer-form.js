// ===== VOLUNTEER FORM - JAVASCRIPT =====
// Handles committee selection, availability matrix, validation, and submission

// Form data object
let formData = {};

// Track selected committees and availability
let selectedCommittees = [];
let selectedAvailability = [];

// ===== COMMITTEE SELECTION =====

function updateCommitteeSelection() {
    // Get all checked committees
    const checkboxes = document.querySelectorAll('input[name="committees"]:checked');
    selectedCommittees = Array.from(checkboxes).map(cb => cb.value);

    // Toggle committee notes
    const medicalCheckbox = document.getElementById('comm10');
    const medicalNote = document.getElementById('medicalNote');

    if (medicalCheckbox && medicalNote) {
        medicalNote.style.display = medicalCheckbox.checked ? 'block' : 'none';
    }

    // Update matrix visibility and content
    updateMatrix();
}

// ===== AVAILABILITY SELECTION =====

function updateAvailabilitySelection() {
    // Get all checked availability slots
    const checkboxes = document.querySelectorAll('input[name="availability"]:checked');
    selectedAvailability = Array.from(checkboxes).map(cb => cb.value);

    // Update matrix visibility and content
    updateMatrix();
}

// ===== COMMITTEE-AVAILABILITY MATRIX =====

function updateMatrix() {
    const matrixSection = document.getElementById('matrixSection');
    const matrixRows = document.getElementById('matrixRows');

    // Show matrix only if:
    // 1. More than one committee is selected AND
    // 2. At least one availability slot is selected
    if (selectedCommittees.length > 1 && selectedAvailability.length > 0) {
        matrixSection.classList.add('active');
        buildMatrix();
    } else {
        matrixSection.classList.remove('active');
        matrixRows.innerHTML = '';
    }
}

function buildMatrix() {
    const matrixRows = document.getElementById('matrixRows');
    matrixRows.innerHTML = '';

    // Create a row for each selected availability slot
    selectedAvailability.forEach((slot, index) => {
        const row = document.createElement('div');
        row.className = 'matrix-row';

        // Time slot label
        const label = document.createElement('div');
        label.className = 'matrix-label';
        label.textContent = slot;

        // Committee dropdown
        const selectWrapper = document.createElement('div');
        selectWrapper.className = 'matrix-select';

        const select = document.createElement('select');
        select.name = `matrix-${index}`;
        select.id = `matrix-${index}`;
        select.setAttribute('data-slot', slot);
        select.required = true;

        // Add placeholder option
        const placeholderOption = document.createElement('option');
        placeholderOption.value = '';
        placeholderOption.textContent = 'Select committee for this time slot';
        select.appendChild(placeholderOption);

        // Add options for each selected committee
        selectedCommittees.forEach(committee => {
            const option = document.createElement('option');
            option.value = committee;
            option.textContent = committee;
            select.appendChild(option);
        });

        selectWrapper.appendChild(select);

        row.appendChild(label);
        row.appendChild(selectWrapper);
        matrixRows.appendChild(row);
    });
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

    // Validate committees (at least one must be checked)
    const committeeCheckboxes = document.querySelectorAll('input[name="committees"]:checked');
    if (committeeCheckboxes.length === 0) {
        document.querySelector('input[name="committees"]').closest('.form-group').classList.add('has-error');
        isValid = false;
    }

    // Validate availability (at least one must be checked)
    const availabilityCheckboxes = document.querySelectorAll('input[name="availability"]:checked');
    if (availabilityCheckboxes.length === 0) {
        document.querySelector('input[name="availability"]').closest('.form-group').classList.add('has-error');
        isValid = false;
    }

    // Validate matrix (if visible, all dropdowns must have selection)
    const matrixSection = document.getElementById('matrixSection');
    if (matrixSection.classList.contains('active')) {
        const matrixSelects = matrixSection.querySelectorAll('select');
        matrixSelects.forEach(select => {
            if (!select.value) {
                select.classList.add('error');
                isValid = false;
            }
        });

        if (!isValid) {
            alert('Please assign a committee for each time slot in the matrix below.');
        }
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

// ===== FORM SUBMISSION =====

document.getElementById('volunteerForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    // Validate form
    if (!validateForm()) {
        return;
    }

    // Collect form data
    formData = {
        firstName: document.getElementById('firstName').value.trim(),
        lastName: document.getElementById('lastName').value.trim(),
        phone: document.getElementById('phone').value.trim(),
        email: document.getElementById('email').value.trim(),
        committees: selectedCommittees,
        availability: selectedAvailability,
        timestamp: new Date().toISOString(),
        type: 'volunteer'
    };

    // If matrix is active, collect committee assignments for each time slot
    const matrixSection = document.getElementById('matrixSection');
    if (matrixSection.classList.contains('active')) {
        const matrixSelects = matrixSection.querySelectorAll('select');
        const assignments = {};

        matrixSelects.forEach(select => {
            const slot = select.getAttribute('data-slot');
            assignments[slot] = select.value;
        });

        formData.committeeAssignments = assignments;
    }

    // Check rate limiting
    if (window.RateLimiter) {
        const rateLimitCheck = window.RateLimiter.canSubmit('volunteer');
        if (!rateLimitCheck.allowed) {
            alert(rateLimitCheck.message);
            return;
        }
    }

    // Validate CSRF token
    if (window.CSRFProtection) {
        if (!window.CSRFProtection.validateForm(document.getElementById('volunteerForm'))) {
            alert('Security validation failed. Please refresh the page and try again.');
            return;
        }
    }

    // Validate and sanitize form data
    if (window.FormValidator) {
        const validation = window.FormValidator.validateFormData(formData, [
            'firstName', 'lastName', 'phone', 'email'
        ]);

        if (!validation.valid) {
            alert('Please fix the following errors:\n' + validation.errors.join('\n'));
            return;
        }

        formData = { ...formData, ...validation.sanitized };
    }

    // Show loading state
    const submitBtn = document.getElementById('submitBtn');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="loading-spinner"></span> Submitting...';

    try {
        // Submit to Firebase
        const docId = await submitVolunteer(formData);

        // Record submission for rate limiting
        if (window.RateLimiter) {
            window.RateLimiter.recordSubmission('volunteer');
        }

        // Add document ID to form data for Google Sheets
        formData.id = docId;
        formData.createdAt = { toDate: () => new Date() };

        // Send email notifications
        await sendVolunteerEmails(formData);

        // Sync to Google Sheets (non-blocking - won't prevent form submission)
        if (window.GoogleSheetsService && window.GoogleSheetsService.isGoogleSheetsConfigured()) {
            window.GoogleSheetsService.addRowToSheet('volunteers', formData).catch(err => {
                console.warn('Google Sheets sync failed (form still submitted successfully)');
            });
        }

        // Show success message with masked email
        document.getElementById('volunteerForm').style.display = 'none';
        document.getElementById('successMessage').style.display = 'block';
        document.getElementById('confirmEmail').textContent = window.DataMasking ?
            window.DataMasking.maskEmail(formData.email) : formData.email;
        document.getElementById('confirmCommittees').textContent = formData.committees.join(', ');
        document.getElementById('confirmAvailability').textContent = formData.availability.length + ' time slot(s)';

        // Scroll to success message
        document.getElementById('successMessage').scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (error) {
        console.error('Error submitting form:', error.message || 'Unknown error');
        alert('There was an error submitting your volunteer application. Please try again or contact us at 941-800-5211.');
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
});

// ===== EMAIL NOTIFICATIONS =====

async function sendVolunteerEmails(data) {
    try {
        // Prepare assignment details for email
        let assignmentText = '';
        if (data.committeeAssignments) {
            assignmentText = '\n\nCommittee Assignments:\n';
            for (const [slot, committee] of Object.entries(data.committeeAssignments)) {
                assignmentText += `${slot}: ${committee}\n`;
            }
        }

        // Admin notification
        const adminTemplateParams = {
            to_email: 'sarasotagospel@gmail.com',
            from_name: `${data.firstName} ${data.lastName}`,
            reply_to: data.email,
            subject: 'New Volunteer Sign-Up - 2026 International Meeting',
            message: `
New volunteer application received:

Name: ${data.firstName} ${data.lastName}
Phone: ${data.phone}
Email: ${data.email}

Committees: ${data.committees.join(', ')}
Availability: ${data.availability.join(', ')}
${assignmentText}

Submitted: ${new Date().toLocaleString()}
            `.trim()
        };

        // Confirmation email to volunteer
        const confirmTemplateParams = {
            to_email: data.email,
            firstName: data.firstName || '',
            lastName: data.lastName || '',
            committees: data.committees.join(', ')
        };

        // Send emails via EmailJS
        if (typeof emailjs !== 'undefined') {
            await emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_IDS.volunteer, adminTemplateParams);
            await emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_IDS.volunteer, confirmTemplateParams);
            console.log('Volunteer notification emails sent');
        }
    } catch (error) {
        console.error('Error sending emails:', error);
        // Don't throw - form was still submitted successfully
    }
}

// ===== INITIALIZE =====

document.addEventListener('DOMContentLoaded', function() {
    console.log('Volunteer form initialized');

    // Initialize CSRF protection
    if (window.CSRFProtection) {
        const form = document.getElementById('volunteerForm');
        window.CSRFProtection.addToForm(form);
    }

    // Initialize EmailJS
    if (typeof emailjs !== 'undefined') {
        initEmailJS();
    }

    // Set focus on first input
    document.getElementById('firstName').focus();
});
