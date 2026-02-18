// ===== REGISTRATION FORM - JAVASCRIPT =====
// Handles form navigation, validation, and Firebase submission
// NOTE: EMAILJS_TEMPLATE_IDS and submitRegistration are defined in
// firebase-config.js and firebase-service.js (loaded before this script)

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
        // Reset the "Will you be traveling alone?" and "How many?" fields
        toggleHowManyField(false);
        document.getElementById('travelAloneYes').checked = false;
        document.getElementById('travelAloneNo').checked = false;
    }
}

function toggleHowManyField(show) {
    const field = document.getElementById('howManyField');
    const input = document.getElementById('howManyPeople');

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
    if (!show) {
        // If no children under 10, also set VBS and nursery to No
        document.getElementById('vbsNo').checked = true;
        toggleVBSField(false);
        document.getElementById('nurseryNo').checked = true;
        toggleNurseryField(false);
    }
}

function toggleVBSField(show) {
    const field = document.getElementById('vbsField');
    const input = document.getElementById('numVBS');
    const detailsContainer = document.getElementById('vbsChildrenDetails');

    if (show) {
        field.style.display = 'block';
        input.setAttribute('required', 'required');
    } else {
        field.style.display = 'none';
        input.removeAttribute('required');
        input.value = '';
        // Clear dynamic child fields
        if (detailsContainer) {
            detailsContainer.innerHTML = '';
        }
        // Remove error state
        input.classList.remove('error');
        field.classList.remove('has-error');
    }
}

function toggleNurseryField(show) {
    const field = document.getElementById('nurseryField');
    const input = document.getElementById('numNursery');
    const detailsContainer = document.getElementById('nurseryChildrenDetails');

    if (show) {
        field.style.display = 'block';
        input.setAttribute('required', 'required');
    } else {
        field.style.display = 'none';
        input.removeAttribute('required');
        input.value = '';
        // Clear dynamic child fields
        if (detailsContainer) {
            detailsContainer.innerHTML = '';
        }
        // Remove error state
        input.classList.remove('error');
        field.classList.remove('has-error');
    }
}

// Generate dynamic fields for nursery children
function generateNurseryChildFields() {
    const numChildren = parseInt(document.getElementById('numNursery').value) || 0;
    const container = document.getElementById('nurseryChildrenDetails');

    if (!container) return;

    // Clear existing fields
    container.innerHTML = '';

    if (numChildren < 1) return;

    // Create fields for each child
    for (let i = 1; i <= numChildren; i++) {
        const childSection = document.createElement('div');
        childSection.style.marginTop = '24px';
        childSection.style.padding = '16px';
        childSection.style.backgroundColor = '#f8f9fa';
        childSection.style.borderRadius = '8px';
        childSection.style.border = '1px solid #dee2e6';

        childSection.innerHTML = `
            <h4 style="margin-top: 0; margin-bottom: 16px; font-size: 16px; color: var(--navy-blue);">Nursery Child ${i}</h4>

            <div class="form-group">
                <label for="nurseryChild${i}Name">Full Name <span class="required">*</span></label>
                <input type="text" id="nurseryChild${i}Name" name="nurseryChild${i}Name" required>
                <span class="error-message">Please enter child's full name</span>
            </div>

            <div class="form-group">
                <label for="nurseryChild${i}Age">Age <span class="required">*</span></label>
                <input type="number" id="nurseryChild${i}Age" name="nurseryChild${i}Age" min="1" max="3" required>
                <span class="error-message">Please enter child's age (1-3)</span>
            </div>

            <div class="form-group">
                <label for="nurseryChild${i}Allergies">Allergies</label>
                <textarea id="nurseryChild${i}Allergies" name="nurseryChild${i}Allergies" placeholder="List any allergies or dietary restrictions, or write 'None'"></textarea>
            </div>

            <div class="form-group">
                <label for="nurseryChild${i}Medical">Medical Conditions</label>
                <textarea id="nurseryChild${i}Medical" name="nurseryChild${i}Medical" placeholder="List any medical conditions, or write 'None'"></textarea>
            </div>

            <div class="form-group">
                <label for="nurseryChild${i}Behavioral">Behavioral/Sensory Needs</label>
                <textarea id="nurseryChild${i}Behavioral" name="nurseryChild${i}Behavioral" placeholder="List any behavioral or sensory needs, or write 'None'"></textarea>
            </div>
        `;

        container.appendChild(childSection);
    }
}

// Generate dynamic fields for VBS children
function generateVBSChildFields() {
    const numChildren = parseInt(document.getElementById('numVBS').value) || 0;
    const container = document.getElementById('vbsChildrenDetails');

    if (!container) return;

    // Clear existing fields
    container.innerHTML = '';

    if (numChildren < 1) return;

    // Create fields for each child
    for (let i = 1; i <= numChildren; i++) {
        const childSection = document.createElement('div');
        childSection.style.marginTop = '24px';
        childSection.style.padding = '16px';
        childSection.style.backgroundColor = '#f8f9fa';
        childSection.style.borderRadius = '8px';
        childSection.style.border = '1px solid #dee2e6';

        childSection.innerHTML = `
            <h4 style="margin-top: 0; margin-bottom: 16px; font-size: 16px; color: var(--navy-blue);">VBS Child ${i}</h4>

            <div class="form-group">
                <label for="vbsChild${i}Name">Full Name <span class="required">*</span></label>
                <input type="text" id="vbsChild${i}Name" name="vbsChild${i}Name" required>
                <span class="error-message">Please enter child's full name</span>
            </div>

            <div class="form-group">
                <label for="vbsChild${i}Age">Age <span class="required">*</span></label>
                <input type="number" id="vbsChild${i}Age" name="vbsChild${i}Age" min="4" max="10" required>
                <span class="error-message">Please enter child's age (4-10)</span>
            </div>

            <div class="form-group">
                <label for="vbsChild${i}Allergies">Allergies</label>
                <textarea id="vbsChild${i}Allergies" name="vbsChild${i}Allergies" placeholder="List any allergies or dietary restrictions, or write 'None'"></textarea>
            </div>

            <div class="form-group">
                <label for="vbsChild${i}Medical">Medical Conditions</label>
                <textarea id="vbsChild${i}Medical" name="vbsChild${i}Medical" placeholder="List any medical conditions, or write 'None'"></textarea>
            </div>

            <div class="form-group">
                <label for="vbsChild${i}Behavioral">Behavioral/Sensory Needs</label>
                <textarea id="vbsChild${i}Behavioral" name="vbsChild${i}Behavioral" placeholder="List any behavioral or sensory needs, or write 'None'"></textarea>
            </div>
        `;

        container.appendChild(childSection);
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
        // Child care section - no additional validation needed
        // Individual child fields are validated through standard required field validation
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

    // If on child care section, collect structured child data
    if (currentStep === 3) {
        collectChildData();
    }
}

// Collect and structure child data
function collectChildData() {
    // Collect nursery children data
    const numNursery = parseInt(document.getElementById('numNursery').value) || 0;
    if (numNursery > 0) {
        formData.nurseryChildren = [];
        for (let i = 1; i <= numNursery; i++) {
            const name = document.getElementById(`nurseryChild${i}Name`)?.value || '';
            const age = document.getElementById(`nurseryChild${i}Age`)?.value || '';
            const allergies = document.getElementById(`nurseryChild${i}Allergies`)?.value || 'None';
            const medical = document.getElementById(`nurseryChild${i}Medical`)?.value || 'None';
            const behavioral = document.getElementById(`nurseryChild${i}Behavioral`)?.value || 'None';

            formData.nurseryChildren.push({
                name: name,
                age: age,
                allergies: allergies,
                medicalConditions: medical,
                behavioralNeeds: behavioral
            });
        }
    }

    // Collect VBS children data
    const numVBS = parseInt(document.getElementById('numVBS').value) || 0;
    if (numVBS > 0) {
        formData.vbsChildren = [];
        for (let i = 1; i <= numVBS; i++) {
            const name = document.getElementById(`vbsChild${i}Name`)?.value || '';
            const age = document.getElementById(`vbsChild${i}Age`)?.value || '';
            const allergies = document.getElementById(`vbsChild${i}Allergies`)?.value || 'None';
            const medical = document.getElementById(`vbsChild${i}Medical`)?.value || 'None';
            const behavioral = document.getElementById(`vbsChild${i}Behavioral`)?.value || 'None';

            formData.vbsChildren.push({
                name: name,
                age: age,
                allergies: allergies,
                medicalConditions: medical,
                behavioralNeeds: behavioral
            });
        }
    }
}

// ===== FORM SUBMISSION =====

document.getElementById('registrationForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    // Check rate limiting
    if (window.RateLimiter) {
        const rateLimitCheck = window.RateLimiter.canSubmit('registration');
        if (!rateLimitCheck.allowed) {
            alert(rateLimitCheck.message);
            return;
        }
    }

    // Validate CSRF token if available
    if (window.CSRFProtection) {
        if (!window.CSRFProtection.validateForm(this)) {
            alert('Security validation failed. Please refresh the page and try again.');
            return;
        }
    }

    // Validate final section
    if (!validateSection(currentStep)) {
        return;
    }

    // Save final section data
    saveCurrentSectionData();

    // Validate and sanitize form data if FormValidator is available
    if (window.FormValidator) {
        const validation = window.FormValidator.validateFormData(formData, [
            'firstName', 'lastName', 'phone', 'email', 'pastorName', 'assemblyName'
        ]);

        if (!validation.valid) {
            alert('Please fix the following errors:\n' + validation.errors.join('\n'));
            return;
        }

        // Use sanitized data
        formData = { ...formData, ...validation.sanitized };
    }

    // Add timestamp and status (required by Firestore rules)
    formData.timestamp = new Date().toISOString();
    formData.type = 'registration';
    formData.status = 'pending';

    // Show loading state
    const submitBtn = document.getElementById('submitBtn');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="loading-spinner"></span> Submitting...';

    try {
        // Submit to Firebase
        const docId = await submitRegistration(formData);

        // Record submission for rate limiting
        if (window.RateLimiter) {
            window.RateLimiter.recordSubmission('registration');
        }

        // Add document ID to form data for Google Sheets
        formData.id = docId;
        formData.createdAt = { toDate: () => new Date() };

        // Send email notification
        await sendEmailNotification(formData);

        // Sync to Google Sheets (non-blocking - won't prevent form submission)
        if (window.GoogleSheetsService && window.GoogleSheetsService.isGoogleSheetsConfigured()) {
            window.GoogleSheetsService.addRowToSheet('registrations', formData).catch(err => {
                console.warn('Google Sheets sync failed (form still submitted successfully)');
            });
        }

        // Show success message with masked email
        document.getElementById('registrationForm').style.display = 'none';
        document.getElementById('successMessage').style.display = 'block';
        const confirmEmail = formData.email || formData.phone;
        document.getElementById('confirmEmail').textContent = window.DataMasking ?
            window.DataMasking.maskEmail(confirmEmail) : confirmEmail;

        // Scroll to success message
        document.getElementById('successMessage').scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (error) {
        console.error('Error submitting form:', error.message || 'Unknown error');
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

Children Under 10: ${data.hasChildren}

Nursery (Ages 1-3): ${data.nurseryAttendance}
${data.nurseryAttendance === 'Yes' && data.nurseryChildren ? `
Nursery Children (${data.nurseryChildren.length}):
${data.nurseryChildren.map((child, idx) => `
  ${idx + 1}. ${child.name}, Age ${child.age}
     Allergies: ${child.allergies}
     Medical Conditions: ${child.medicalConditions || 'None'}
     Behavioral/Sensory Needs: ${child.behavioralNeeds || 'None'}`).join('\n')}` : ''}

VBS (Ages 4-10): ${data.vbsAttendance}
${data.vbsAttendance === 'Yes' && data.vbsChildren ? `
VBS Children (${data.vbsChildren.length}):
${data.vbsChildren.map((child, idx) => `
  ${idx + 1}. ${child.name}, Age ${child.age}
     Allergies: ${child.allergies}
     Medical Conditions: ${child.medicalConditions || 'None'}
     Behavioral/Sensory Needs: ${child.behavioralNeeds || 'None'}`).join('\n')}` : ''}

Submitted: ${new Date().toLocaleString()}
            `.trim()
        };

        // Confirmation email to registrant (if email provided)
        if (data.email) {
            const confirmTemplateParams = {
                to_email: data.email,
                firstName: data.firstName || '',
                lastName: data.lastName || '',
                churchName: data.assemblyName || 'N/A',
                pastorName: data.pastorName || '',
                email: data.email || '',
                phone: data.phone || ''
            };

            // Send both emails (independently so one failure doesn't block the other)
            if (typeof emailjs !== 'undefined') {
                try {
                    await emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_IDS.registration, adminTemplateParams, EMAILJS_PUBLIC_KEY);
                    console.log('Registration admin notification email sent');
                } catch (adminErr) {
                    console.error('Admin email failed:', adminErr);
                }
                try {
                    await emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_IDS.registration, confirmTemplateParams, EMAILJS_PUBLIC_KEY);
                    console.log('Registration confirmation email sent');
                } catch (confirmErr) {
                    console.error('Confirmation email failed:', confirmErr);
                }
            } else {
                console.error('EmailJS is not loaded!');
            }
        } else {
            // Send only admin notification if no email provided
            if (typeof emailjs !== 'undefined') {
                console.log('EmailJS sending admin-only with:', { serviceId: EMAILJS_SERVICE_ID, templateId: EMAILJS_TEMPLATE_IDS.registration, publicKey: EMAILJS_PUBLIC_KEY });
                try {
                    await emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_IDS.registration, adminTemplateParams, EMAILJS_PUBLIC_KEY);
                    console.log('Registration admin notification email sent');
                } catch (adminErr) {
                    console.error('Admin email failed:', adminErr);
                }
            } else {
                console.error('EmailJS is not loaded!');
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

    // Initialize CSRF protection
    if (window.CSRFProtection) {
        const form = document.getElementById('registrationForm');
        window.CSRFProtection.addToForm(form);
    }

    // Initialize EmailJS
    if (typeof emailjs !== 'undefined') {
        initEmailJS();
    }

    // ===== NAVIGATION BUTTONS =====
    document.getElementById('btnToStep2').addEventListener('click', function() { nextStep(2); });
    document.getElementById('btnToStep3').addEventListener('click', function() { nextStep(3); });
    document.getElementById('btnBackToStep1').addEventListener('click', function() { previousStep(1); });
    document.getElementById('btnBackToStep2').addEventListener('click', function() { previousStep(2); });

    // ===== TRANSPORTATION SECTION =====
    document.getElementById('airportYes').addEventListener('change', function() { toggleAirportFields(true); });
    document.getElementById('airportNo').addEventListener('change', function() { toggleAirportFields(false); });
    document.getElementById('travelAloneYes').addEventListener('change', function() { toggleHowManyField(false); });
    document.getElementById('travelAloneNo').addEventListener('change', function() { toggleHowManyField(true); });
    document.getElementById('localTransportYes').addEventListener('change', function() { toggleLocalTransport(true); });
    document.getElementById('localTransportNo').addEventListener('change', function() { toggleLocalTransport(false); });

    // ===== CHILD CARE SECTION =====
    document.getElementById('childrenYes').addEventListener('change', function() { toggleChildrenFields(true); });
    document.getElementById('childrenNo').addEventListener('change', function() { toggleChildrenFields(false); });
    document.getElementById('vbsYes').addEventListener('change', function() { toggleVBSField(true); });
    document.getElementById('vbsNo').addEventListener('change', function() { toggleVBSField(false); });
    document.getElementById('nurseryYes').addEventListener('change', function() { toggleNurseryField(true); });
    document.getElementById('nurseryNo').addEventListener('change', function() { toggleNurseryField(false); });
    document.getElementById('numVBS').addEventListener('change', generateVBSChildFields);
    document.getElementById('numNursery').addEventListener('change', generateNurseryChildFields);

    // Set focus on first input
    document.getElementById('firstName').focus();
});
