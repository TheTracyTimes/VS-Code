// ===== REGISTRATION FORM - JAVASCRIPT =====
// Handles form navigation, validation, and Firebase submission

// Current step tracker
let currentStep = 1;

// Form data object
let formData = {};

// ===== STEP NAVIGATION =====

function nextStep(step) {
    // Validate current section before proceeding
    if (!validateSection(currentStep)) {
        return;
    }

    // Save current section data
    saveCurrentSectionData();

    // Hide current section
    document.querySelector(`.form-section[data-section="${currentStep}"]`).classList.remove('active');

    // Show next section
    document.querySelector(`.form-section[data-section="${step}"]`).classList.add('active');

    // Update progress indicator
    updateProgressIndicator(step);

    // Update current step
    currentStep = step;

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function previousStep(step) {
    // Hide current section
    document.querySelector(`.form-section[data-section="${currentStep}"]`).classList.remove('active');

    // Show previous section
    document.querySelector(`.form-section[data-section="${step}"]`).classList.add('active');

    // Update progress indicator
    updateProgressIndicator(step);

    // Update current step
    currentStep = step;

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function updateProgressIndicator(step) {
    // Remove all active/completed classes
    document.querySelectorAll('.progress-step').forEach(el => {
        el.classList.remove('active', 'completed');
    });

    // Mark previous steps as completed
    for (let i = 1; i < step; i++) {
        document.querySelector(`.progress-step[data-step="${i}"]`).classList.add('completed');
    }

    // Mark current step as active
    document.querySelector(`.progress-step[data-step="${step}"]`).classList.add('active');
}

// ===== CONDITIONAL FIELD TOGGLES =====

function toggleAirportFields(show) {
    const fields = document.getElementById('airportFields');
    const inputs = fields.querySelectorAll('input');

    if (show) {
        fields.style.display = 'block';
        // Make fields required
        inputs.forEach(input => {
            input.setAttribute('required', 'required');
        });
    } else {
        fields.style.display = 'none';
        // Remove required attribute and set to N/A
        inputs.forEach(input => {
            input.removeAttribute('required');
            input.value = 'N/A';
            // Remove error state
            input.classList.remove('error');
            input.closest('.form-group').classList.remove('has-error');
        });
    }
}

function toggleLocalTransport(show) {
    const field = document.getElementById('localTransportField');
    const textarea = document.getElementById('pickupLocation');

    if (show) {
        field.style.display = 'block';
        textarea.setAttribute('required', 'required');
    } else {
        field.style.display = 'none';
        textarea.removeAttribute('required');
        textarea.value = '';
        // Remove error state
        textarea.classList.remove('error');
        field.classList.remove('has-error');
    }
}

function toggleChildrenFields(show) {
    const fields = document.getElementById('childrenFields');
    const input = document.getElementById('numChildren');

    if (show) {
        fields.style.display = 'block';
        input.setAttribute('required', 'required');
    } else {
        fields.style.display = 'none';
        input.removeAttribute('required');
        input.value = '';
        // Also hide VBS and nursery fields
        document.getElementById('vbsNo').checked = true;
        toggleVBSField(false);
        document.getElementById('nurseryNo').checked = true;
        toggleNurseryField(false);
    }
}

function toggleVBSField(show) {
    const field = document.getElementById('vbsField');
    const input = document.getElementById('numVBS');

    if (show) {
        field.style.display = 'block';
        input.setAttribute('required', 'required');
    } else {
        field.style.display = 'none';
        input.removeAttribute('required');
        input.value = '';
        // Remove error state
        input.classList.remove('error');
        field.classList.remove('has-error');
    }
}

function toggleNurseryField(show) {
    const field = document.getElementById('nurseryField');
    const input = document.getElementById('numNursery');

    if (show) {
        field.style.display = 'block';
        input.setAttribute('required', 'required');
    } else {
        field.style.display = 'none';
        input.removeAttribute('required');
        input.value = '';
        // Remove error state
        input.classList.remove('error');
        field.classList.remove('has-error');
    }
}

// ===== VALIDATION =====

function validateSection(section) {
    const sectionEl = document.querySelector(`.form-section[data-section="${section}"]`);
    let isValid = true;

    // Clear previous errors
    sectionEl.querySelectorAll('.error').forEach(el => el.classList.remove('error'));
    sectionEl.querySelectorAll('.has-error').forEach(el => el.classList.remove('has-error'));

    // Validate text inputs
    const textInputs = sectionEl.querySelectorAll('input[type="text"]:not([type="hidden"]), input[type="email"], input[type="tel"], input[type="number"], textarea');
    textInputs.forEach(input => {
        // Skip if field is not visible or not required
        if (input.offsetParent === null || !input.hasAttribute('required')) {
            return;
        }

        if (!input.value.trim()) {
            input.classList.add('error');
            input.closest('.form-group').classList.add('has-error');
            isValid = false;
        }
    });

    // Validate email format (if provided)
    const emailInput = sectionEl.querySelector('input[type="email"]');
    if (emailInput && emailInput.value.trim() && !isValidEmail(emailInput.value)) {
        emailInput.classList.add('error');
        emailInput.closest('.form-group').classList.add('has-error');
        isValid = false;
    }

    // Validate phone format
    const phoneInput = sectionEl.querySelector('input[type="tel"]');
    if (phoneInput && phoneInput.hasAttribute('required') && !isValidPhone(phoneInput.value)) {
        phoneInput.classList.add('error');
        phoneInput.closest('.form-group').classList.add('has-error');
        isValid = false;
    }

    // Validate checkboxes (at least one must be checked)
    const checkboxGroups = sectionEl.querySelectorAll('.checkbox-group');
    checkboxGroups.forEach(group => {
        const checkboxes = group.querySelectorAll('input[type="checkbox"]');
        const checked = Array.from(checkboxes).some(cb => cb.checked);

        if (!checked) {
            group.closest('.form-group').classList.add('has-error');
            isValid = false;
        }
    });

    // Validate radio buttons
    const radioGroups = sectionEl.querySelectorAll('.radio-group');
    radioGroups.forEach(group => {
        const radios = group.querySelectorAll('input[type="radio"]');
        const checked = Array.from(radios).some(r => r.checked);

        if (!checked && radios[0].hasAttribute('required')) {
            group.closest('.form-group').classList.add('has-error');
            isValid = false;
        }
    });

    // Section-specific validation
    if (section === 3) {
        // Validate child care logic
        const hasChildren = document.querySelector('input[name="hasChildren"]:checked');
        if (hasChildren && hasChildren.value === 'Yes') {
            const numChildren = parseInt(document.getElementById('numChildren').value) || 0;
            const numVBS = parseInt(document.getElementById('numVBS').value) || 0;
            const numNursery = parseInt(document.getElementById('numNursery').value) || 0;

            // Check if VBS + Nursery doesn't exceed total children
            if (numVBS + numNursery > numChildren) {
                alert('The total number of children in VBS and nursery cannot exceed the total number of children under 5.');
                isValid = false;
            }
        }
    }

    if (!isValid) {
        // Scroll to first error
        const firstError = sectionEl.querySelector('.has-error');
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

// ===== SAVE FORM DATA =====

function saveCurrentSectionData() {
    const section = document.querySelector(`.form-section[data-section="${currentStep}"]`);

    // Save all input values
    section.querySelectorAll('input, textarea, select').forEach(input => {
        if (input.type === 'checkbox') {
            if (!formData[input.name]) {
                formData[input.name] = [];
            }
            if (input.checked) {
                formData[input.name].push(input.value);
            }
        } else if (input.type === 'radio') {
            if (input.checked) {
                formData[input.name] = input.value;
            }
        } else {
            formData[input.name] = input.value;
        }
    });
}

// ===== FORM SUBMISSION =====

document.getElementById('registrationForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    // Validate final section
    if (!validateSection(currentStep)) {
        return;
    }

    // Save final section data
    saveCurrentSectionData();

    // Add timestamp
    formData.timestamp = new Date().toISOString();
    formData.type = 'registration';

    // Show loading state
    const submitBtn = document.getElementById('submitBtn');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="loading-spinner"></span> Submitting...';

    try {
        // Submit to Firebase
        await submitRegistration(formData);

        // Send email notification
        await sendEmailNotification(formData);

        // Show success message
        document.getElementById('registrationForm').style.display = 'none';
        document.getElementById('successMessage').style.display = 'block';
        document.getElementById('confirmEmail').textContent = formData.email || formData.phone;

        // Scroll to success message
        document.getElementById('successMessage').scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (error) {
        console.error('Error submitting form:', error);
        alert('There was an error submitting your registration. Please try again or contact us at 941-800-5211.');
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
});

// ===== EMAIL NOTIFICATION =====

async function sendEmailNotification(data) {
    try {
        // Admin notification
        const adminTemplateParams = {
            to_email: 'sarasotagospel@gmail.com',
            from_name: `${data.firstName} ${data.lastName}`,
            reply_to: data.email || data.phone,
            subject: 'New Registration - 2026 International Meeting',
            message: `
New registration received:

Name: ${data.firstName} ${data.lastName}
Phone: ${data.phone}
Email: ${data.email || 'Not provided'}
Pastor: ${data.pastorName}
Assembly: ${data.assemblyName || 'Not provided'}

Services Attending: ${Array.isArray(data.services) ? data.services.join(', ') : data.services}

Airport Transportation: ${data.airportTransport}
Local Transportation: ${data.localTransport}

Children Under 5: ${data.hasChildren}
${data.hasChildren === 'Yes' ? `Number of Children: ${data.numChildren}` : ''}

Submitted: ${new Date().toLocaleString()}
            `.trim()
        };

        // Confirmation email to registrant (if email provided)
        if (data.email) {
            const confirmTemplateParams = {
                to_email: data.email,
                to_name: `${data.firstName} ${data.lastName}`,
                subject: 'Registration Confirmed - 2026 International Meeting',
                message: `
Dear ${data.firstName} ${data.lastName},

Thank you for registering for the Sarasota Gospel Temple 2026 International Meeting!

EVENT DETAILS:
📅 Dates: April 9-11, 2026
📍 Location: 1900 Gandy Blvd N, St. Petersburg, FL 33702
📞 Contact: 941-800-5211

YOUR REGISTRATION:
Services Attending: ${Array.isArray(data.services) ? data.services.join(', ') : data.services}
Transportation Needed: ${data.airportTransport}

We look forward to seeing you at the meeting! If you need to update your registration, please contact us at 941-800-5211.

Blessings,
Sarasota Gospel Temple
                `.trim()
            };

            // Send both emails
            if (typeof emailjs !== 'undefined') {
                await emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, adminTemplateParams);
                await emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, confirmTemplateParams);
                console.log('Registration notification emails sent');
            }
        } else {
            // Send only admin notification if no email provided
            if (typeof emailjs !== 'undefined') {
                await emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, adminTemplateParams);
                console.log('Registration notification email sent to admin');
            }
        }
    } catch (error) {
        console.error('Email error:', error);
        // Don't throw - form was still submitted successfully
    }
}

// ===== INITIALIZE =====

document.addEventListener('DOMContentLoaded', function() {
    console.log('Registration form initialized');

    // Initialize EmailJS
    if (typeof emailjs !== 'undefined') {
        initEmailJS();
    }

    // Set focus on first input
    document.getElementById('firstName').focus();
});
