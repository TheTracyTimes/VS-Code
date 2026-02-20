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
let lastManualInteraction = 0;
const AUTO_ROTATION_DELAY = 5000; // Pause auto-rotation for 5 seconds after manual interaction

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

    // If manual interaction, update timestamp to pause auto-rotation
    if (isManual) {
        lastManualInteraction = Date.now();
        console.log(`Manual navigation on ${galleryId}: slide ${gallery.currentSlide + 1}/${gallery.totalSlides}`);
    }
}

// Auto-rotate all galleries every 5 seconds
function autoRotateGalleries() {
    // Check if we should pause due to recent manual interaction
    const timeSinceManual = Date.now() - lastManualInteraction;
    if (timeSinceManual < AUTO_ROTATION_DELAY) {
        console.log(`Auto-rotation paused (${Math.ceil((AUTO_ROTATION_DELAY - timeSinceManual) / 1000)}s remaining)`);
        return;
    }

    // Rotate each gallery
    Object.keys(galleries).forEach(galleryId => {
        const container = document.getElementById(galleryId);
        if (container && galleries[galleryId].totalSlides > 0) {
            changeSlide(galleryId, 1, false);
        }
    });
}

// Attach event listeners to navigation buttons
function attachNavigationListeners() {
    Object.keys(galleries).forEach(galleryId => {
        const galleryContainer = document.getElementById(galleryId);
        if (!galleryContainer) return;

        // Find the parent ministry-gallery div
        const parentGallery = galleryContainer.closest('.ministry-gallery');
        if (!parentGallery) return;

        // Find prev and next buttons within this gallery
        const prevBtn = parentGallery.querySelector('.gallery-nav.prev');
        const nextBtn = parentGallery.querySelector('.gallery-nav.next');

        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                changeSlide(galleryId, -1, true);
            });
            console.log(`Attached prev button listener for ${galleryId}`);
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                changeSlide(galleryId, 1, true);
            });
            console.log(`Attached next button listener for ${galleryId}`);
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

            // Update counter
            const counter = document.getElementById(galleryId.replace('-gallery', '-counter'));
            if (counter) {
                counter.textContent = `1 / ${slides.length}`;
            }

            console.log(`Gallery ${galleryId}: ${slides.length} slides initialized`);
        } else {
            console.warn(`Gallery container not found: ${galleryId}`);
        }
    });

    // Attach navigation button listeners
    attachNavigationListeners();

    // Start auto-rotation (runs every 5 seconds)
    if (autoRotationInterval) {
        clearInterval(autoRotationInterval);
    }
    autoRotationInterval = setInterval(autoRotateGalleries, 5000);
    console.log('Gallery auto-rotation started (5 second interval)');
}

// ===== LIGHTBOX =====
let lightboxGalleryId = null;

function openLightbox(galleryId) {
    const gallery = galleries[galleryId];
    const container = document.getElementById(galleryId);
    if (!container || !gallery) return;

    const slides = container.querySelectorAll('.gallery-slide');
    const src = slides[gallery.currentSlide].querySelector('img').src;
    const alt = slides[gallery.currentSlide].querySelector('img').alt;

    lightboxGalleryId = galleryId;
    document.getElementById('lightboxImg').src = src;
    document.getElementById('lightboxImg').alt = alt;
    document.getElementById('lightbox').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    document.getElementById('lightbox').classList.remove('active');
    document.getElementById('lightboxImg').src = '';
    lightboxGalleryId = null;
    document.body.style.overflow = '';
}

function lightboxNav(direction) {
    if (!lightboxGalleryId) return;
    changeSlide(lightboxGalleryId, direction, true);

    const gallery = galleries[lightboxGalleryId];
    const container = document.getElementById(lightboxGalleryId);
    const slides = container.querySelectorAll('.gallery-slide');
    document.getElementById('lightboxImg').src = slides[gallery.currentSlide].querySelector('img').src;
    document.getElementById('lightboxImg').alt = slides[gallery.currentSlide].querySelector('img').alt;
}

function attachLightboxListeners() {
    Object.keys(galleries).forEach(galleryId => {
        const container = document.getElementById(galleryId);
        if (!container) return;
        container.querySelectorAll('.gallery-slide img').forEach(img => {
            img.addEventListener('click', () => openLightbox(galleryId));
        });
    });

    document.getElementById('lightboxClose').addEventListener('click', closeLightbox);
    document.getElementById('lightboxPrev').addEventListener('click', () => lightboxNav(-1));
    document.getElementById('lightboxNext').addEventListener('click', () => lightboxNav(1));

    document.getElementById('lightbox').addEventListener('click', function(e) {
        if (e.target === this) closeLightbox();
    });

    document.addEventListener('keydown', function(e) {
        if (!document.getElementById('lightbox').classList.contains('active')) return;
        if (e.key === 'Escape') closeLightbox();
        if (e.key === 'ArrowLeft') lightboxNav(-1);
        if (e.key === 'ArrowRight') lightboxNav(1);
    });
}

// Initialize when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        initializeGalleries();
        attachLightboxListeners();
    });
} else {
    initializeGalleries();
    attachLightboxListeners();
}

console.log('Gallery script loaded');
