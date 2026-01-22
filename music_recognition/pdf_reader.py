"""
PDF reading and image extraction for scanned music scores.
Processes PDF files to extract music notation images for recognition.
"""

import tempfile
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional
import os

try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

import cv2
import numpy as np


class PDFMusicReader:
    """Read and extract music notation from scanned PDF files."""

    def __init__(self, dpi: int = 300):
        """
        Initialize PDF music reader.

        Args:
            dpi: Resolution for PDF to image conversion (default 300)
        """
        self.dpi = dpi

    def check_dependencies(self) -> dict:
        """
        Check which PDF reading methods are available.

        Returns:
            Dictionary with availability status
        """
        return {
            'pdf2image': PDF2IMAGE_AVAILABLE,
            'PyPDF2': PYPDF2_AVAILABLE,
            'poppler': self._check_poppler()
        }

    def _check_poppler(self) -> bool:
        """Check if poppler-utils is installed."""
        try:
            result = subprocess.run(
                ['pdftoppm', '-v'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def pdf_to_images(
        self,
        pdf_path: str,
        output_folder: Optional[str] = None
    ) -> List[str]:
        """
        Convert PDF pages to images.

        Args:
            pdf_path: Path to PDF file
            output_folder: Folder to save images (optional)

        Returns:
            List of image file paths
        """
        if not PDF2IMAGE_AVAILABLE:
            raise ImportError(
                "pdf2image not installed. Install with: pip install pdf2image"
            )

        pdf_path = Path(pdf_path)

        if output_folder is None:
            output_folder = tempfile.mkdtemp(prefix='music_pdf_')

        output_dir = Path(output_folder)
        output_dir.mkdir(exist_ok=True, parents=True)

        print(f"Converting PDF to images (DPI={self.dpi})...")

        # Convert PDF to images
        images = convert_from_path(
            str(pdf_path),
            dpi=self.dpi,
            output_folder=str(output_dir),
            fmt='png'
        )

        # Save images
        image_paths = []
        for i, image in enumerate(images):
            image_path = output_dir / f"page_{i+1:03d}.png"
            image.save(str(image_path), 'PNG')
            image_paths.append(str(image_path))
            print(f"  Saved page {i+1}: {image_path}")

        print(f"✓ Converted {len(image_paths)} pages")
        return image_paths

    def extract_staves_from_image(
        self,
        image_path: str,
        num_staves_expected: int = None
    ) -> List[Tuple[np.ndarray, Tuple[int, int, int, int]]]:
        """
        Extract individual staves from a page image.

        Args:
            image_path: Path to image file
            num_staves_expected: Expected number of staves (optional)

        Returns:
            List of (staff_image, bbox) tuples
        """
        # Read image
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect horizontal lines (staff lines)
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (100, 1))
        detected_lines = cv2.morphologyEx(gray, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

        # Find horizontal projection
        horizontal_proj = np.sum(detected_lines, axis=1)

        # Find staff groups
        threshold = np.max(horizontal_proj) * 0.3
        in_staff = False
        staff_regions = []
        start_y = 0

        for i, val in enumerate(horizontal_proj):
            if val > threshold and not in_staff:
                in_staff = True
                start_y = i
            elif val <= threshold and in_staff:
                in_staff = False
                # Add some padding
                padding = 20
                staff_regions.append((
                    max(0, start_y - padding),
                    min(image.shape[0], i + padding)
                ))

        # Extract staff images
        staves = []
        for idx, (y_start, y_end) in enumerate(staff_regions):
            staff_img = image[y_start:y_end, :]
            bbox = (0, y_start, image.shape[1], y_end - y_start)
            staves.append((staff_img, bbox))

        print(f"  Extracted {len(staves)} staves from {Path(image_path).name}")
        return staves

    def process_pdf_score(
        self,
        pdf_path: str,
        output_dir: str = None
    ) -> dict:
        """
        Process a complete PDF score and extract all parts.

        Args:
            pdf_path: Path to PDF file
            output_dir: Directory for output

        Returns:
            Dictionary with extracted parts information
        """
        if output_dir is None:
            output_dir = Path(pdf_path).stem + "_extracted"

        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True, parents=True)

        # Convert PDF to images
        page_images = self.pdf_to_images(pdf_path, str(output_path / "pages"))

        # Extract staves from each page
        all_staves = []
        for page_num, page_path in enumerate(page_images, 1):
            print(f"\nProcessing page {page_num}...")
            staves = self.extract_staves_from_image(page_path)

            for staff_num, (staff_img, bbox) in enumerate(staves, 1):
                staff_path = output_path / f"page{page_num:03d}_staff{staff_num:02d}.png"
                cv2.imwrite(str(staff_path), staff_img)

                all_staves.append({
                    'page': page_num,
                    'staff_number': staff_num,
                    'image_path': str(staff_path),
                    'bbox': bbox
                })

        # Save metadata
        import json
        metadata = {
            'source_pdf': str(pdf_path),
            'total_pages': len(page_images),
            'total_staves': len(all_staves),
            'staves': all_staves
        }

        metadata_path = output_path / 'metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        print(f"\n✓ Extracted {len(all_staves)} staves from {len(page_images)} pages")
        print(f"  Output directory: {output_path}")
        print(f"  Metadata: {metadata_path}")

        return metadata


def read_pdf_score(
    pdf_path: str,
    recognition_system=None,
    output_dir: str = None
) -> dict:
    """
    Read and recognize music from a scanned PDF score.

    Args:
        pdf_path: Path to PDF file
        recognition_system: MusicRecognitionSystem instance
        output_dir: Output directory

    Returns:
        Dictionary with recognized parts
    """
    reader = PDFMusicReader(dpi=300)

    # Extract images from PDF
    metadata = reader.process_pdf_score(pdf_path, output_dir)

    if recognition_system is None:
        print("No recognition system provided - images extracted only")
        return metadata

    # Recognize each staff
    print("\nRecognizing music notation...")
    recognized_parts = []

    for staff_info in metadata['staves']:
        print(f"  Recognizing page {staff_info['page']}, staff {staff_info['staff_number']}...")

        try:
            score = recognition_system.recognize(staff_info['image_path'])
            recognized_parts.append({
                'staff_info': staff_info,
                'score': score
            })
        except Exception as e:
            print(f"    Error: {e}")

    print(f"\n✓ Recognized {len(recognized_parts)} parts")

    return {
        'metadata': metadata,
        'recognized_parts': recognized_parts
    }


def install_pdf_dependencies():
    """Print instructions for installing PDF dependencies."""
    print("\n" + "="*70)
    print("PDF READING DEPENDENCIES")
    print("="*70)

    print("\nRequired:")
    print("  1. pdf2image (Python package)")
    print("     pip install pdf2image")

    print("\n  2. poppler-utils (System package)")
    print("     macOS:    brew install poppler")
    print("     Ubuntu:   sudo apt-get install poppler-utils")
    print("     Windows:  Download from http://blog.alivate.com.au/poppler-windows/")

    print("\nOptional:")
    print("  PyPDF2 (for PDF manipulation)")
    print("     pip install PyPDF2")

    print("\n" + "="*70)


def check_pdf_setup():
    """Check PDF reading setup and show status."""
    reader = PDFMusicReader()
    status = reader.check_dependencies()

    print("\n" + "="*70)
    print("PDF READING SETUP STATUS")
    print("="*70)

    print("\nPython Packages:")
    print(f"  pdf2image: {'✓ Installed' if status['pdf2image'] else '✗ Not installed'}")
    print(f"  PyPDF2:    {'✓ Installed' if status['PyPDF2'] else '✗ Not installed'}")

    print("\nSystem Tools:")
    print(f"  poppler:   {'✓ Installed' if status['poppler'] else '✗ Not installed'}")

    if all(status.values()):
        print("\n✓ All dependencies installed - PDF reading ready!")
    else:
        print("\n⚠ Some dependencies missing")
        print("\nRun install_pdf_dependencies() for installation instructions")

    print("="*70 + "\n")

    return status


if __name__ == '__main__':
    # Check setup
    check_pdf_setup()
