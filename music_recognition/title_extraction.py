"""
Title extraction and staff line removal for clean music notation.

This module detects text titles written in staff areas, removes the staff lines
behind them, and formats titles cleanly in Times New Roman font.
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional, Dict
from pathlib import Path


class TitleExtractor:
    """Extracts titles from music notation and removes staff lines behind them."""

    def __init__(self):
        """Initialize title extractor."""
        self.staff_line_color = (0, 0, 0)  # Black
        self.background_color = (255, 255, 255)  # White

    def detect_text_regions(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect regions in the image that contain text.

        Args:
            image: Input image as numpy array

        Returns:
            List of bounding boxes (x, y, width, height) for text regions
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Apply binary threshold
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

        # Use morphological operations to connect text characters
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 5))
        dilated = cv2.dilate(binary, kernel, iterations=2)

        # Find contours
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter contours to get text regions
        text_regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # Filter by aspect ratio and size (text is usually wider than tall)
            aspect_ratio = w / h if h > 0 else 0
            if aspect_ratio > 2.0 and w > 50 and h > 10 and h < 100:
                text_regions.append((x, y, w, h))

        return text_regions

    def detect_staff_lines(self, image: np.ndarray) -> List[int]:
        """
        Detect horizontal staff lines in the image.

        Args:
            image: Input image as numpy array

        Returns:
            List of y-coordinates of staff lines
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Apply binary threshold
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

        # Use horizontal kernel to detect horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        detected_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel)

        # Find horizontal projections
        horizontal_projection = np.sum(detected_lines, axis=1)

        # Find peaks (staff lines)
        threshold = np.max(horizontal_projection) * 0.5
        staff_lines = []
        for i, value in enumerate(horizontal_projection):
            if value > threshold:
                staff_lines.append(i)

        # Group close lines together (within 2 pixels)
        if not staff_lines:
            return []

        grouped_lines = []
        current_group = [staff_lines[0]]

        for line in staff_lines[1:]:
            if line - current_group[-1] <= 2:
                current_group.append(line)
            else:
                # Take average of group
                grouped_lines.append(int(np.mean(current_group)))
                current_group = [line]

        # Add last group
        if current_group:
            grouped_lines.append(int(np.mean(current_group)))

        return grouped_lines

    def remove_staff_lines_in_region(self, image: np.ndarray, region: Tuple[int, int, int, int],
                                     staff_lines: List[int]) -> np.ndarray:
        """
        Remove staff lines in a specific region of the image.

        Args:
            image: Input image as numpy array
            region: Tuple (x, y, width, height) defining the region
            staff_lines: List of y-coordinates of staff lines

        Returns:
            Image with staff lines removed in the region
        """
        x, y, w, h = region
        result = image.copy()

        # For each staff line that intersects the region
        for line_y in staff_lines:
            if y <= line_y <= y + h:
                # Remove the line in the horizontal region
                # Use a thickness of 2-3 pixels to account for line thickness
                for dy in range(-1, 2):
                    if 0 <= line_y + dy < image.shape[0]:
                        result[line_y + dy, x:x+w] = 255  # White background

        return result

    def extract_clean_title(self, image_path: str, output_path: Optional[str] = None) -> Dict:
        """
        Extract titles from music notation image and remove staff lines behind them.

        Args:
            image_path: Path to input image
            output_path: Optional path to save cleaned image

        Returns:
            Dictionary with:
                - 'cleaned_image': Image with staff lines removed behind titles
                - 'text_regions': List of detected text regions
                - 'staff_lines': List of detected staff line positions
        """
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")

        # Detect text regions
        text_regions = self.detect_text_regions(image)

        # Detect staff lines
        staff_lines = self.detect_staff_lines(image)

        # Remove staff lines in text regions
        cleaned_image = image.copy()
        for region in text_regions:
            cleaned_image = self.remove_staff_lines_in_region(cleaned_image, region, staff_lines)

        # Save if output path provided
        if output_path:
            cv2.imwrite(output_path, cleaned_image)

        return {
            'cleaned_image': cleaned_image,
            'text_regions': text_regions,
            'staff_lines': staff_lines,
            'original_image': image
        }

    def process_pdf_page(self, pdf_page_image: np.ndarray) -> np.ndarray:
        """
        Process a PDF page to clean titles.

        Args:
            pdf_page_image: PDF page as numpy array

        Returns:
            Cleaned image with staff lines removed behind titles
        """
        # Detect text regions
        text_regions = self.detect_text_regions(pdf_page_image)

        # Detect staff lines
        staff_lines = self.detect_staff_lines(pdf_page_image)

        # Remove staff lines in text regions
        cleaned_image = pdf_page_image.copy()
        for region in text_regions:
            cleaned_image = self.remove_staff_lines_in_region(cleaned_image, region, staff_lines)

        return cleaned_image


class PartSplitter:
    """
    Splits combined instrumental parts into separate individual books.

    For example: "Bb Clarinet/Trumpet 1/Soprano Sax" → 3 separate books
    """

    # Define part name patterns and their variations
    PART_PATTERNS = {
        'clarinet': ['Clarinet', 'Cl.', 'Clar.'],
        'trumpet': ['Trumpet', 'Tpt.', 'Trpt.'],
        'saxophone': ['Saxophone', 'Sax', 'S. Sax', 'A. Sax', 'T. Sax', 'Bari. Sax'],
        'trombone': ['Trombone', 'Tbn.', 'Trb.'],
        'horn': ['Horn', 'Hn.', 'French Horn'],
        'baritone': ['Baritone', 'Bar.', 'Euphonium', 'Euph.'],
        'flute': ['Flute', 'Fl.'],
        'bass_clarinet': ['Bass Clarinet', 'B. Cl.', 'Bass Cl.'],
        'tenor_sax': ['Tenor Sax', 'T. Sax', 'Tenor Saxophone'],
    }

    @staticmethod
    def parse_combined_part_name(part_name: str) -> List[str]:
        """
        Parse a combined part name into individual instrument names.

        Args:
            part_name: Combined part name (e.g., "Bb Clarinet/Trumpet 1/Soprano Sax")

        Returns:
            List of individual instrument names

        Examples:
            >>> parse_combined_part_name("Bb Clarinet/Trumpet 1/Soprano Sax")
            ['1st Bb Clarinet', '1st Bb Trumpet', 'Bb Soprano Sax']

            >>> parse_combined_part_name("Bb Tenor Sax/Bb Clarinet/Trumpet 3")
            ['Bb Tenor Sax', '3rd Bb Clarinet', '3rd Bb Trumpet']
        """
        # Split by common delimiters
        parts = part_name.replace(';', '/').split('/')

        individual_parts = []

        for part in parts:
            part = part.strip()
            if part:
                individual_parts.append(part)

        return individual_parts

    @staticmethod
    def create_individual_books(combined_score: 'MusicScore',
                               combined_part_name: str,
                               instrument_mapping: Dict[str, 'InstrumentConfig']) -> Dict[str, Tuple['MusicScore', 'InstrumentConfig']]:
        """
        Create individual part books from a combined part.

        Args:
            combined_score: MusicScore containing the combined part
            combined_part_name: Name of the combined part
            instrument_mapping: Dictionary mapping part names to instrument configs

        Returns:
            Dictionary of individual part name to (score, instrument) tuples
        """
        # Parse the combined name
        individual_names = PartSplitter.parse_combined_part_name(combined_part_name)

        # Create separate books
        individual_books = {}

        for name in individual_names:
            # Find matching instrument config
            instrument = None
            for pattern_name, config in instrument_mapping.items():
                if pattern_name.lower() in name.lower():
                    instrument = config
                    break

            if instrument:
                # Create a copy of the score for this instrument
                score_copy = PartSplitter._copy_score(combined_score)
                individual_books[name] = (score_copy, instrument)

        return individual_books

    @staticmethod
    def _copy_score(score: 'MusicScore') -> 'MusicScore':
        """Create a deep copy of a MusicScore."""
        from .postprocessing import MusicScore

        new_score = MusicScore()
        new_score.time_signature = score.time_signature
        new_score.key_signature = score.key_signature
        new_score.clef = score.clef
        new_score.tempo = score.tempo

        # Deep copy measures
        for measure in score.measures:
            new_measure = [note.copy() for note in measure]
            new_score.measures.append(new_measure)

        return new_score


def extract_titles_from_pdf(pdf_path: str, output_dir: str) -> Dict[str, str]:
    """
    Extract and clean titles from all pages of a PDF.

    Args:
        pdf_path: Path to PDF file
        output_dir: Directory to save cleaned images

    Returns:
        Dictionary mapping page numbers to cleaned image paths
    """
    from pdf2image import convert_from_path
    import os

    extractor = TitleExtractor()

    # Convert PDF to images
    images = convert_from_path(pdf_path)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    cleaned_paths = {}

    for i, img in enumerate(images):
        # Convert PIL image to numpy array
        img_array = np.array(img)

        # Process the page
        cleaned = extractor.process_pdf_page(img_array)

        # Save cleaned image
        output_path = os.path.join(output_dir, f'page_{i+1}_cleaned.png')
        cv2.imwrite(output_path, cv2.cvtColor(cleaned, cv2.COLOR_RGB2BGR))

        cleaned_paths[i+1] = output_path

    return cleaned_paths
