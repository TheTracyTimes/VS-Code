// ===== SECURITY UTILITIES =====
// Client-side security helpers for forms and data protection

// ===== INPUT VALIDATION =====

const FormValidator = {
    // Sanitize text by stripping HTML tags
    sanitizeText(input) {
        if (!input) return '';
        // Use DOMPurify if available, otherwise basic escaping
        if (typeof DOMPurify !== 'undefined') {
            return DOMPurify.sanitize(input, { ALLOWED_TAGS: [] });
        }
        // Fallback: escape HTML entities
        const div = document.createElement('div');
        div.textContent = input;
        return div.innerHTML;
    },

    // Validate email format
    validateEmail(email) {
        if (!email) return { valid: false, message: 'Email is required' };
        const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!re.test(email)) {
            return { valid: false, message: 'Invalid email format' };
        }
        return { valid: true, sanitized: this.sanitizeText(email) };
    },

    // Validate phone number
    validatePhone(phone) {
        if (!phone) return { valid: false, message: 'Phone is required' };
        const cleaned = phone.replace(/\D/g, '');
        if (cleaned.length < 10) {
            return { valid: false, message: 'Phone must be at least 10 digits' };
        }
        return { valid: true, sanitized: cleaned };
    },

    // Validate name (letters, spaces, hyphens, apostrophes only)
    validateName(name) {
        if (!name) return { valid: false, message: 'Name is required' };
        const sanitized = this.sanitizeText(name);
        if (!/^[a-zA-Z\s\-']+$/.test(sanitized)) {
            return { valid: false, message: 'Name contains invalid characters' };
        }
        if (sanitized.length < 2 || sanitized.length > 50) {
            return { valid: false, message: 'Name must be 2-50 characters' };
        }
        return { valid: true, sanitized };
    },

    // Validate all form data
    validateFormData(formData, requiredFields) {
        const errors = [];
        const sanitized = {};

        for (const field of requiredFields) {
            const value = formData[field];

            if (field.toLowerCase().includes('email')) {
                const result = this.validateEmail(value);
                if (!result.valid) errors.push(`${field}: ${result.message}`);
                else sanitized[field] = result.sanitized;
            }
            else if (field.toLowerCase().includes('phone')) {
                const result = this.validatePhone(value);
                if (!result.valid) errors.push(`${field}: ${result.message}`);
                else sanitized[field] = result.sanitized;
            }
            else if (field.toLowerCase().includes('name')) {
                const result = this.validateName(value);
                if (!result.valid) errors.push(`${field}: ${result.message}`);
                else sanitized[field] = result.sanitized;
            }
            else {
                // Generic text field
                sanitized[field] = this.sanitizeText(value);
            }
        }

        // Copy non-required fields
        for (const [key, value] of Object.entries(formData)) {
            if (!requiredFields.includes(key)) {
                if (typeof value === 'string') {
                    sanitized[key] = this.sanitizeText(value);
                } else {
                    sanitized[key] = value;
                }
            }
        }

        return { valid: errors.length === 0, errors, sanitized };
    }
};

// ===== CSRF PROTECTION =====

const CSRFProtection = {
    // Generate random token
    generateToken() {
        const array = new Uint8Array(32);
        crypto.getRandomValues(array);
        return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
    },

    // Set new token in session storage
    setToken() {
        const token = this.generateToken();
        sessionStorage.setItem('csrf_token', token);
        return token;
    },

    // Get current token (create if doesn't exist)
    getToken() {
        let token = sessionStorage.getItem('csrf_token');
        if (!token) {
            token = this.setToken();
        }
        return token;
    },

    // Validate token matches session
    validateToken(token) {
        return token === sessionStorage.getItem('csrf_token');
    },

    // Add hidden input to form
    addToForm(form) {
        let input = form.querySelector('input[name="csrf_token"]');
        if (!input) {
            input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'csrf_token';
            form.appendChild(input);
        }
        input.value = this.getToken();
    },

    // Validate form has valid CSRF token
    validateForm(form) {
        const formData = new FormData(form);
        const token = formData.get('csrf_token');
        return this.validateToken(token);
    }
};

// ===== RATE LIMITING =====

const RateLimiter = {
    // Check if user can submit form
    canSubmit(formType) {
        const key = `${formType}_lastSubmit`;
        const lastSubmit = localStorage.getItem(key);

        if (lastSubmit) {
            const elapsed = Date.now() - parseInt(lastSubmit);
            const minInterval = 60000; // 1 minute

            if (elapsed < minInterval) {
                const remaining = Math.ceil((minInterval - elapsed) / 1000);
                return {
                    allowed: false,
                    message: `Please wait ${remaining} seconds before submitting again`
                };
            }
        }

        return { allowed: true };
    },

    // Record submission time
    recordSubmission(formType) {
        const key = `${formType}_lastSubmit`;
        localStorage.setItem(key, Date.now().toString());
    }
};

// ===== SENSITIVE DATA MASKING =====

const DataMasking = {
    // Mask email address
    maskEmail(email) {
        if (!email || !email.includes('@')) return '***';
        const [local, domain] = email.split('@');
        if (local.length <= 2) return '***@' + domain;
        const maskedLocal = local.charAt(0) + '***' + local.charAt(local.length - 1);
        return `${maskedLocal}@${domain}`;
    },

    // Mask phone number
    maskPhone(phone) {
        if (!phone) return '***';
        const cleaned = phone.replace(/\D/g, '');
        if (cleaned.length < 4) return '***';
        return '***-***-' + cleaned.slice(-4);
    },

    // Mask name (show first and last initial only)
    maskName(name) {
        if (!name || name.length < 2) return '***';
        return name.charAt(0) + '***';
    },

    // Safely display user data without exposing sensitive info
    safeDisplay(value, type) {
        if (!value) return '—';

        switch (type) {
            case 'email':
                return this.maskEmail(value);
            case 'phone':
                return this.maskPhone(value);
            case 'name':
                return this.maskName(value);
            default:
                return value;
        }
    }
};

// ===== XSS PREVENTION =====

const XSSProtection = {
    // Safely set text content (never use innerHTML with user data)
    setTextContent(element, text) {
        element.textContent = text || '—';
    },

    // Sanitize HTML before inserting
    sanitizeHTML(html) {
        if (!html) return '';
        if (typeof DOMPurify !== 'undefined') {
            return DOMPurify.sanitize(html, {
                ALLOWED_TAGS: [], // Strip all HTML by default
                KEEP_CONTENT: true
            });
        }
        // Fallback: escape HTML
        const div = document.createElement('div');
        div.textContent = html;
        return div.innerHTML;
    },

    // Create safe table cell
    createTableCell(content, tagName = 'td') {
        const cell = document.createElement(tagName);
        this.setTextContent(cell, content);
        return cell;
    },

    // Create link element safely
    createLink(text, clickHandler) {
        const link = document.createElement('a');
        link.href = '#';
        link.textContent = text;
        link.addEventListener('click', (e) => {
            e.preventDefault();
            clickHandler(e);
        });
        return link;
    }
};

// ===== SECURE CONSOLE LOGGING =====

const SecureLogger = {
    // Log without exposing sensitive data
    log(message, data = null) {
        if (data && typeof data === 'object') {
            // Create sanitized copy
            const sanitized = {};
            for (const [key, value] of Object.entries(data)) {
                if (key.toLowerCase().includes('email')) {
                    sanitized[key] = DataMasking.maskEmail(value);
                } else if (key.toLowerCase().includes('phone')) {
                    sanitized[key] = DataMasking.maskPhone(value);
                } else if (key.toLowerCase().includes('password') || key.toLowerCase().includes('token')) {
                    sanitized[key] = '***';
                } else {
                    sanitized[key] = value;
                }
            }
            console.log(message, sanitized);
        } else {
            console.log(message);
        }
    },

    error(message, error = null) {
        if (error) {
            console.error(message, error.message || error);
        } else {
            console.error(message);
        }
    }
};

// ===== EXPORT FOR USE IN OTHER SCRIPTS =====

if (typeof window !== 'undefined') {
    window.FormValidator = FormValidator;
    window.CSRFProtection = CSRFProtection;
    window.RateLimiter = RateLimiter;
    window.DataMasking = DataMasking;
    window.XSSProtection = XSSProtection;
    window.SecureLogger = SecureLogger;
}
