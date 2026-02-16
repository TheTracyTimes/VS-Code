// ===== GALLERY ROTATION =====
// Handles photo gallery rotation for ministry pages

// Gallery data
const galleries = {
    'music-gallery': {
        currentSlide: 0
    },
    'prayer-gallery': {
        currentSlide: 0
    },
    'youth-gallery': {
        currentSlide: 0
    }
};

// Change slide function
function changeSlide(galleryId, direction) {
    const gallery = galleries[galleryId];
    const container = document.getElementById(galleryId);
    const counter = document.getElementById(galleryId.replace('-gallery', '-counter'));

    if (!container || !gallery || !counter) {
        console.error('Gallery elements not found:', galleryId);
        return;
    }

    const slides = container.querySelectorAll('.gallery-slide');

    if (slides.length === 0) {
        console.error('No slides found in gallery:', galleryId);
        return;
    }

    // Hide current slide
    slides[gallery.currentSlide].classList.remove('active');

    // Calculate new slide index
    gallery.currentSlide += direction;

    // Wrap around if needed (use actual slide count from DOM)
    if (gallery.currentSlide >= slides.length) {
        gallery.currentSlide = 0;
    } else if (gallery.currentSlide < 0) {
        gallery.currentSlide = slides.length - 1;
    }

    // Show new slide
    slides[gallery.currentSlide].classList.add('active');

    // Update counter
    counter.textContent = `${gallery.currentSlide + 1} / ${slides.length}`;
}

// Auto-rotate galleries every 5 seconds
function autoRotateGalleries() {
    Object.keys(galleries).forEach(galleryId => {
        changeSlide(galleryId, 1);
    });
}

// Initialize gallery rotation when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing gallery rotation...');

    // Verify galleries exist
    Object.keys(galleries).forEach(galleryId => {
        const container = document.getElementById(galleryId);
        if (container) {
            const slides = container.querySelectorAll('.gallery-slide');
            console.log(`Gallery ${galleryId}: ${slides.length} slides found`);
        } else {
            console.warn(`Gallery container not found: ${galleryId}`);
        }
    });

    // Start auto-rotation immediately, then every 5 seconds
    setInterval(autoRotateGalleries, 5000);
    console.log('Gallery auto-rotation started (5 second interval)');
});

console.log('Gallery script loaded');
