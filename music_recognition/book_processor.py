"""
Complete Instrument Book Processing

Handles the workflow for processing uploaded instrument books:
1. Digitize 18 uploaded handwritten books (preserving layout)
2. Generate 10 additional books from the 18
3. Output 28 clean digitized books with proper headers/footers
4. Extract 288 songs and create conductor scores

Each book contains all 288 songs for one instrument.
"""

from typing import Dict, List, Tuple, Optional
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import os

from .pdf_reader import PDFMusicReader
from .score_layout import add_headers_and_footers
from .part_generator import PartGenerator
from .multipart_score import MultiPartScore
from .instruments import BandInstruments


class InstrumentBookProcessor:
    """Process complete instrument books (each containing all 288 songs)."""

    def __init__(self):
        """Initialize book processor."""
        self.pdf_reader = PDFMusicReader()
        self.part_generator = PartGenerator()

        # Map of all 28 instruments in order
        self.all_instruments = [
            "Viola",
            "Violin",
            "Cello",
            "Oboe",
            "Bassoon",
            "C Flute 1",
            "C Flute 2",
            "C Flute 3",
            "Bb Soprano Saxophone",
            "Eb Alto Saxophone 1",
            "Eb Alto Saxophone 2",
            "Eb Alto Saxophone 3",
            "Bb Tenor Saxophone",
            "Eb Baritone Saxophone",
            "Bb Clarinet 1",
            "Bb Clarinet 2",
            "Bb Clarinet 3",
            "Eb Alto Clarinet",
            "Bb Bass Clarinet",
            "Bb Trumpet 1",
            "Bb Trumpet 2",
            "Bb Trumpet 3",
            "F French Horn",
            "Bb Baritone TC",
            "C Baritone BC",
            "C Trombone 1",
            "C Trombone 2",
            "Tuba"
        ]

    def process_uploaded_books(
        self,
        uploaded_book_paths: List[str],
        output_dir: str = 'output/digitized_books'
    ) -> Dict[str, str]:
        """
        Process uploaded handwritten books and generate all 28 digitized books.

        Args:
            uploaded_book_paths: List of paths to 18 uploaded PDF books
            output_dir: Directory to save digitized books

        Returns:
            Dictionary mapping instrument names to digitized book paths
        """
        os.makedirs(output_dir, exist_ok=True)

        print(f"\n{'='*70}")
        print("DIGITIZING INSTRUMENT BOOKS")
        print(f"{'='*70}")
        print(f"Processing {len(uploaded_book_paths)} uploaded books...")
        print(f"Will generate {28 - len(uploaded_book_paths)} additional books")
        print(f"Total output: 28 digitized books\n")

        digitized_books = {}

        # Step 1: Digitize the 18 uploaded books
        for idx, book_path in enumerate(uploaded_book_paths, 1):
            print(f"[{idx}/{len(uploaded_book_paths)}] Digitizing: {Path(book_path).name}")

            # Extract instrument name from filename or metadata
            instrument_name = self._extract_instrument_name(book_path)

            # Digitize this book (clean notation, preserve layout, add headers/footers)
            digitized_path = self._digitize_book(
                book_path,
                instrument_name,
                output_dir
            )

            digitized_books[instrument_name] = digitized_path
            print(f"  ✓ Created: {Path(digitized_path).name}\n")

        # Step 2: Generate 10 additional books from the 18
        print("\nGenerating additional instrument books...")
        generated_books = self._generate_additional_books(
            digitized_books,
            output_dir
        )

        digitized_books.update(generated_books)

        print(f"\n{'='*70}")
        print(f"COMPLETE: Created {len(digitized_books)} digitized books")
        print(f"{'='*70}\n")

        return digitized_books

    def _extract_instrument_name(self, book_path: str) -> str:
        """
        Extract instrument name from PDF filename or metadata.

        Args:
            book_path: Path to uploaded PDF

        Returns:
            Instrument name (e.g., "C Flute 1")
        """
        # Try to extract from filename
        filename = Path(book_path).stem

        # Look for instrument names in filename
        for instrument in self.all_instruments:
            # Simple matching - can be improved with fuzzy matching
            if instrument.lower().replace(' ', '_') in filename.lower().replace(' ', '_'):
                return instrument

        # If not found, return filename as-is
        return filename

    def _digitize_book(
        self,
        input_path: str,
        instrument_name: str,
        output_dir: str
    ) -> str:
        """
        Digitize one instrument book (clean notation, preserve layout, add headers).

        Args:
            input_path: Path to handwritten PDF
            instrument_name: Name of instrument (e.g., "C Flute 1")
            output_dir: Output directory

        Returns:
            Path to digitized PDF
        """
        # Output filename
        safe_name = instrument_name.replace(' ', '_')
        output_path = os.path.join(output_dir, f"{safe_name}.pdf")

        # Convert PDF to images for processing
        images = self.pdf_reader.pdf_to_images(input_path)

        # Create new PDF with clean notation
        c = canvas.Canvas(output_path, pagesize=letter)
        page_width, page_height = letter

        for page_num, image_path in enumerate(images, 1):
            # TODO: This is where music recognition would happen
            # For now, we'll create a placeholder with staff paper
            # In real implementation:
            # 1. Detect staves, measures, notes from image
            # 2. Clean up and redraw notation
            # 3. Preserve layout (same staves per page)

            # Add headers and footers
            add_headers_and_footers(
                c,
                part_name=instrument_name,
                page_number=page_num,
                page_width=page_width,
                page_height=page_height
            )

            # TODO: Draw digitized notation here
            # For now, add placeholder text
            c.setFont("Helvetica", 12)
            c.drawCentredString(
                page_width / 2,
                page_height / 2,
                f"Digitized notation for {instrument_name} - Page {page_num}"
            )
            c.drawCentredString(
                page_width / 2,
                page_height / 2 - 20,
                "(Awaiting music recognition implementation)"
            )

            c.showPage()

        c.save()
        return output_path

    def _generate_additional_books(
        self,
        existing_books: Dict[str, str],
        output_dir: str
    ) -> Dict[str, str]:
        """
        Generate 10 additional instrument books from the existing 18.

        Args:
            existing_books: Dictionary of already digitized books
            output_dir: Output directory

        Returns:
            Dictionary of newly generated books
        """
        generated_books = {}

        # Determine which books need to be generated
        existing_instruments = set(existing_books.keys())
        all_instruments = set(self.all_instruments)
        needed_instruments = all_instruments - existing_instruments

        print(f"Generating {len(needed_instruments)} books:")
        for instrument in sorted(needed_instruments):
            print(f"  - {instrument}")

        # TODO: Implement actual part generation
        # For now, create placeholder PDFs
        for instrument in needed_instruments:
            safe_name = instrument.replace(' ', '_')
            output_path = os.path.join(output_dir, f"{safe_name}.pdf")

            c = canvas.Canvas(output_path, pagesize=letter)
            page_width, page_height = letter

            # Create placeholder with headers/footers
            for page_num in range(1, 11):  # Placeholder: 10 pages
                add_headers_and_footers(
                    c,
                    part_name=instrument,
                    page_number=page_num,
                    page_width=page_width,
                    page_height=page_height
                )

                c.setFont("Helvetica", 12)
                c.drawCentredString(
                    page_width / 2,
                    page_height / 2,
                    f"Generated book: {instrument}"
                )
                c.drawCentredString(
                    page_width / 2,
                    page_height / 2 - 20,
                    "(Generated from source parts - awaiting implementation)"
                )

                c.showPage()

            c.save()
            generated_books[instrument] = output_path
            print(f"  ✓ Generated: {instrument}")

        return generated_books


# Example usage
if __name__ == '__main__':
    processor = InstrumentBookProcessor()

    # Example: Process uploaded books
    uploaded_books = [
        'uploads/C_Flute_1.pdf',
        'uploads/Bb_Clarinet_1.pdf',
        # ... (18 total)
    ]

    digitized = processor.process_uploaded_books(uploaded_books)
    print(f"\nCreated {len(digitized)} digitized books!")
