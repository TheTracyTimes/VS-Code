// ===== GALLERY ROTATION =====
// Handles photo gallery rotation for ministry pages

// Gallery data
const galleries = {
    'music-gallery': {
        currentSlide: 0,
        totalSlides: 0
    },
    'prayer-gallery': {
        currentSlide: 0,
        totalSlides: 0
    },
    'youth-gallery': {
        currentSlide: 0,
        totalSlides: 0
    }
};

let autoRotationInterval = null;
let lastInteractionTime = Date.now();
const AUTO_ROTATION_DELAY = 5000; // Resume auto-rotation after 5 seconds of no interaction

// Change slide function
function changeSlide(galleryId, direction, isManual = false) {
    const gallery = galleries[galleryId];
    const container = document.getElementById(galleryId);
    const counter = document.getElementById(galleryId.replace('-gallery', '-counter'));

    if (!container || !gallery) {
        console.error('Gallery elements not found:', galleryId);
        return;
    }

    const slides = container.querySelectorAll('.gallery-slide');

    if (slides.length === 0) {
        console.error('No slides found in gallery:', galleryId);
        return;
    }

    // Update total slides count if not set
    if (gallery.totalSlides === 0) {
        gallery.totalSlides = slides.length;
    }

    // Hide current slide
    slides[gallery.currentSlide].classList.remove('active');

    // Calculate new slide index
    gallery.currentSlide += direction;

    // Wrap around if needed
    if (gallery.currentSlide >= gallery.totalSlides) {
        gallery.currentSlide = 0;
    } else if (gallery.currentSlide < 0) {
        gallery.currentSlide = gallery.totalSlides - 1;
    }

    // Show new slide
    slides[gallery.currentSlide].classList.add('active');

    // Update counter if it exists
    if (counter) {
        counter.textContent = `${gallery.currentSlide + 1} / ${gallery.totalSlides}`;
    }

    // If manual interaction, update last interaction time
    if (isManual) {
        lastInteractionTime = Date.now();
        console.log(`Manual navigation on ${galleryId}: slide ${gallery.currentSlide + 1}/${gallery.totalSlides}`);
    }
}

// Auto-rotate galleries every 5 seconds
function autoRotateGalleries() {
    // Only auto-rotate if enough time has passed since last manual interaction
    const timeSinceLastInteraction = Date.now() - lastInteractionTime;
    if (timeSinceLastInteraction < AUTO_ROTATION_DELAY) {
        return;
    }

    Object.keys(galleries).forEach(galleryId => {
        const container = document.getElementById(galleryId);
        if (container && galleries[galleryId].totalSlides > 0) {
            changeSlide(galleryId, 1, false);
        }
    });
}

// Initialize galleries
function initializeGalleries() {
    console.log('Initializing gallery rotation...');

    // Initialize each gallery
    Object.keys(galleries).forEach(galleryId => {
        const container = document.getElementById(galleryId);
        if (container) {
            const slides = container.querySelectorAll('.gallery-slide');
            galleries[galleryId].totalSlides = slides.length;
            galleries[galleryId].currentSlide = 0;

            // Ensure first slide is active
            if (slides.length > 0) {
                slides[0].classList.add('active');
            }

            console.log(`Gallery ${galleryId}: ${slides.length} slides initialized`);
        } else {
            console.warn(`Gallery container not found: ${galleryId}`);
        }
    });

    // Start auto-rotation
    if (autoRotationInterval) {
        clearInterval(autoRotationInterval);
    }
    autoRotationInterval = setInterval(autoRotateGalleries, 5000);
    console.log('Gallery auto-rotation started (5 second interval)');
}

// Global function for button clicks (needs to be accessible from HTML onclick)
window.changeSlide = function(galleryId, direction) {
    changeSlide(galleryId, direction, true);
};

// Initialize when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeGalleries);
} else {
    // DOM is already loaded
    initializeGalleries();
}

console.log('Gallery script loaded');
