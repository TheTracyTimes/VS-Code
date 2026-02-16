// ===== GALLERY ROTATION =====
// Handles photo gallery rotation for ministry pages

// Gallery data - will be populated once photos are uploaded
const galleries = {
    'music-gallery': {
        currentSlide: 0,
        totalSlides: 22,
        photos: [] // Will contain photo paths once uploaded
    },
    'prayer-gallery': {
        currentSlide: 0,
        totalSlides: 29,
        photos: []
    },
    'youth-gallery': {
        currentSlide: 0,
        totalSlides: 7,
        photos: []
    }
};

// Change slide function
function changeSlide(galleryId, direction) {
    const gallery = galleries[galleryId];
    const container = document.getElementById(galleryId);
    const counter = document.getElementById(galleryId.replace('-gallery', '-counter'));

    if (!container || !gallery || !counter) return;

    const slides = container.querySelectorAll('.gallery-slide');

    if (slides.length === 0) return;

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

    // Update counter
    counter.textContent = `${gallery.currentSlide + 1} / ${gallery.totalSlides}`;
}

// Auto-rotate galleries every 5 seconds
function autoRotateGalleries() {
    Object.keys(galleries).forEach(galleryId => {
        changeSlide(galleryId, 1);
    });
}

// Initialize gallery rotation when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Start auto-rotation after a brief delay
    setTimeout(() => {
        setInterval(autoRotateGalleries, 5000);
    }, 1000);
});

console.log('Gallery rotation initialized');
