// ===== MAIN WEBSITE JAVASCRIPT =====
// Navigation, animations, and interactive elements

// ===== MOBILE NAVIGATION =====
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    const navToggle = document.querySelector('.nav-toggle');

    navMenu.classList.toggle('active');
    navToggle.classList.toggle('active');
}

// Close mobile menu when clicking on a link
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-menu a');

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            const navMenu = document.querySelector('.nav-menu');
            const navToggle = document.querySelector('.nav-toggle');

            if (navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            }
        });
    });
});

// ===== RAIN ANIMATION =====
function createRain() {
    const rainContainer = document.getElementById('rainContainer');

    if (!rainContainer) return;

    // Create 50 raindrops
    for (let i = 0; i < 50; i++) {
        const raindrop = document.createElement('div');
        raindrop.classList.add('raindrop');

        // Random position
        raindrop.style.left = Math.random() * 100 + '%';

        // Random animation duration (speed)
        raindrop.style.animationDuration = (Math.random() * 1 + 0.5) + 's';

        // Random delay
        raindrop.style.animationDelay = Math.random() * 2 + 's';

        rainContainer.appendChild(raindrop);
    }
}

// ===== LIGHTHOUSE BEAM ILLUMINATION =====
function initLighthouseIllumination() {
    const heroTitle = document.getElementById('heroTitle');
    const heroSubtitle = document.getElementById('heroSubtitle');

    if (!heroTitle || !heroSubtitle) return;

    let rotation = 0;
    const rotationSpeed = 360 / 12000; // 12 seconds per full rotation (matching CSS animation)

    function updateBeamPosition() {
        rotation = (rotation + rotationSpeed * 16.67) % 360; // 16.67ms = ~60fps

        // Lighthouse is centered below the text, beam rotates horizontally clockwise
        // The beam illuminates text when pointing straight up
        // 90 degrees = beam pointing up (12 o'clock position)
        // Illumination window: roughly 70-110 degrees

        const titleIlluminationStart = 70;
        const titleIlluminationEnd = 110;
        const subtitleIlluminationStart = 75;
        const subtitleIlluminationEnd = 105;

        // Check if title should be illuminated
        if (rotation >= titleIlluminationStart && rotation <= titleIlluminationEnd) {
            if (!heroTitle.classList.contains('illuminated')) {
                heroTitle.classList.add('illuminated');
            }
        } else {
            if (heroTitle.classList.contains('illuminated')) {
                heroTitle.classList.remove('illuminated');
            }
        }

        // Check if subtitle should be illuminated
        if (rotation >= subtitleIlluminationStart && rotation <= subtitleIlluminationEnd) {
            if (!heroSubtitle.classList.contains('illuminated')) {
                heroSubtitle.classList.add('illuminated');
            }
        } else {
            if (heroSubtitle.classList.contains('illuminated')) {
                heroSubtitle.classList.remove('illuminated');
            }
        }

        requestAnimationFrame(updateBeamPosition);
    }

    // Start the animation loop
    updateBeamPosition();
}

// ===== SMOOTH SCROLL =====
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Initialize rain animation and lighthouse illumination if on homepage
    createRain();
    initLighthouseIllumination();

    // Initialize Google Sheets API if available
    if (typeof initGoogleSheetsAPI !== 'undefined') {
        initGoogleSheetsAPI();
    }
});

// ===== STICKY NAVIGATION =====
let lastScroll = 0;
const nav = document.getElementById('mainNav');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 100) {
        nav.style.boxShadow = '0 4px 16px rgba(0,0,0,0.2)';
    } else {
        nav.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
    }

    lastScroll = currentScroll;
});

// ===== SCROLL REVEAL ANIMATIONS =====
function reveal() {
    const reveals = document.querySelectorAll('.ministry-card, .time-card, .detail-card, .schedule-day');

    reveals.forEach(element => {
        const windowHeight = window.innerHeight;
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;

        if (elementTop < windowHeight - elementVisible) {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }
    });
}

// Set initial state for reveal elements
document.addEventListener('DOMContentLoaded', function() {
    const reveals = document.querySelectorAll('.ministry-card, .time-card, .detail-card, .schedule-day');

    reveals.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    });

    reveal();
});

window.addEventListener('scroll', reveal);

// ===== FORM CARD ANIMATIONS =====
document.addEventListener('DOMContentLoaded', function() {
    const formCards = document.querySelectorAll('.form-card');

    formCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;

        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100);
    });
});

// ===== ACTIVE PAGE HIGHLIGHT IN NAVIGATION =====
document.addEventListener('DOMContentLoaded', function() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-menu a');

    navLinks.forEach(link => {
        const linkPage = link.getAttribute('href').split('/').pop();

        if (linkPage === currentPage) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});

// ===== LAZY LOADING FOR IMAGES =====
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
});

// ===== CONTACT FORM SUBMISSION (if contact form exists) =====
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');

    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            // Get form data
            const formData = {
                name: document.getElementById('contactName').value,
                email: document.getElementById('contactEmail').value,
                phone: document.getElementById('contactPhone').value,
                message: document.getElementById('contactMessage').value,
                timestamp: new Date().toISOString()
            };

            // Show loading state
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.textContent = 'Sending...';

            try {
                // Submit to Firebase
                const docId = await submitContact(formData);

                // Add document ID to form data for Google Sheets
                formData.id = docId;
                formData.createdAt = { toDate: () => new Date() };

                // Sync to Google Sheets (non-blocking - won't prevent form submission)
                if (window.GoogleSheetsService && window.GoogleSheetsService.isGoogleSheetsConfigured()) {
                    window.GoogleSheetsService.addRowToSheet('contacts', formData).catch(err => {
                        console.warn('Google Sheets sync failed (form still submitted successfully)');
                    });
                }

                // Show success message
                alert('Thank you for your message! We\'ll get back to you soon.');
                contactForm.reset();
            } catch (error) {
                console.error('Error submitting contact form:', error);
                alert('There was an error sending your message. Please try calling us at 941-800-5211.');
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            }
        });
    }
});

console.log('Sarasota Gospel Temple website loaded successfully');
