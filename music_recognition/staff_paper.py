"""
Staff paper and music notation PDF generation with proper staff lines.
Creates professional-looking sheet music on US letter size paper.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from typing import Optional, List, Dict, Tuple
from pathlib import Path


class StaffPaperGenerator:
    """Generate blank staff paper and render music notation."""

    # US Letter dimensions
    PAGE_WIDTH = letter[0]  # 8.5 inches
    PAGE_HEIGHT = letter[1]  # 11 inches

    # Standard staff dimensions
    STAFF_LINE_SPACING = 0.15 * inch  # Space between staff lines (standard is about 0.15")
    STAFF_HEIGHT = 4 * STAFF_LINE_SPACING  # 5 lines = 4 spaces
    STAFF_LINE_THICKNESS = 0.5  # Points

    # Margins
    LEFT_MARGIN = 0.75 * inch
    RIGHT_MARGIN = 0.75 * inch
    TOP_MARGIN = 0.75 * inch
    BOTTOM_MARGIN = 0.75 * inch

    # Staff configuration for 12 staves
    NUM_STAVES_PER_PAGE = 12

    def __init__(self, staves_per_page: int = 12):
        """
        Initialize staff paper generator.

        Args:
            staves_per_page: Number of staves per page (default 12)
        """
        self.staves_per_page = staves_per_page

        # Calculate staff positions
        self.staff_positions = self._calculate_staff_positions()

    def _calculate_staff_positions(self) -> List[float]:
        """
        Calculate vertical positions for each staff.

        Returns:
            List of y-coordinates for top line of each staff
        """
        # Available vertical space
        usable_height = self.PAGE_HEIGHT - self.TOP_MARGIN - self.BOTTOM_MARGIN

        # Space between staves (including staff height)
        total_staff_height = self.staves_per_page * self.STAFF_HEIGHT
        remaining_space = usable_height - total_staff_height

        # Space between staves
        space_between = remaining_space / (self.staves_per_page + 1)

        # Calculate positions (from top)
        positions = []
        current_y = self.PAGE_HEIGHT - self.TOP_MARGIN - space_between

        for i in range(self.staves_per_page):
            positions.append(current_y)
            current_y -= (self.STAFF_HEIGHT + space_between)

        return positions

    def draw_staff_lines(
        self,
        c: canvas.Canvas,
        y_position: float,
        width: Optional[float] = None
    ):
        """
        Draw a single 5-line staff.

        Args:
            c: ReportLab canvas
            y_position: Y-coordinate of top line
            width: Staff width (defaults to page width minus margins)
        """
        if width is None:
            width = self.PAGE_WIDTH - self.LEFT_MARGIN - self.RIGHT_MARGIN

        c.setLineWidth(self.STAFF_LINE_THICKNESS)
        c.setStrokeColor(colors.black)

        # Draw 5 lines
        for i in range(5):
            y = y_position - (i * self.STAFF_LINE_SPACING)
            c.line(self.LEFT_MARGIN, y, self.LEFT_MARGIN + width, y)

    def draw_barline(
        self,
        c: canvas.Canvas,
        x_position: float,
        y_top: float,
        line_type: str = 'single'
    ):
        """
        Draw a barline.

        Args:
            c: ReportLab canvas
            x_position: X-coordinate of barline
            y_top: Y-coordinate of top of staff
            line_type: 'single', 'double', 'final'
        """
        y_bottom = y_top - self.STAFF_HEIGHT

        c.setLineWidth(1.0)

        if line_type == 'single':
            c.line(x_position, y_top, x_position, y_bottom)

        elif line_type == 'double':
            c.line(x_position, y_top, x_position, y_bottom)
            c.line(x_position + 3, y_top, x_position + 3, y_bottom)

        elif line_type == 'final':
            c.setLineWidth(0.5)
            c.line(x_position, y_top, x_position, y_bottom)
            c.setLineWidth(2.5)
            c.line(x_position + 4, y_top, x_position + 4, y_bottom)

    def draw_clef(
        self,
        c: canvas.Canvas,
        x_position: float,
        y_top: float,
        clef_type: str = 'treble'
    ):
        """
        Draw a clef symbol.

        Args:
            c: ReportLab canvas
            x_position: X-coordinate
            y_top: Y-coordinate of top of staff
            clef_type: 'treble', 'bass', 'alto'
        """
        # Simple text-based clef representation
        c.setFont("Helvetica-Bold", 36)

        if clef_type == 'treble':
            # Treble clef symbol (Unicode or text)
            y_pos = y_top - (2 * self.STAFF_LINE_SPACING)
            c.drawString(x_position, y_pos - 12, "𝄞")  # Or use "G"

        elif clef_type == 'bass':
            # Bass clef symbol
            y_pos = y_top - (3 * self.STAFF_LINE_SPACING)
            c.drawString(x_position, y_pos - 12, "𝄢")  # Or use "F"

        elif clef_type == 'alto':
            # Alto clef symbol
            y_pos = y_top - (2 * self.STAFF_LINE_SPACING)
            c.drawString(x_position, y_pos - 12, "𝄡")  # Or use "C"

    def draw_time_signature(
        self,
        c: canvas.Canvas,
        x_position: float,
        y_top: float,
        time_sig: Tuple[int, int]
    ):
        """
        Draw time signature.

        Args:
            c: ReportLab canvas
            x_position: X-coordinate
            y_top: Y-coordinate of top of staff
            time_sig: Tuple of (beats, beat_type) e.g., (4, 4)
        """
        c.setFont("Helvetica-Bold", 24)

        # Draw numerator
        y_numerator = y_top - self.STAFF_LINE_SPACING - 5
        c.drawCentredString(x_position, y_numerator, str(time_sig[0]))

        # Draw denominator
        y_denominator = y_top - (3 * self.STAFF_LINE_SPACING) - 5
        c.drawCentredString(x_position, y_denominator, str(time_sig[1]))

    def create_blank_staff_paper(
        self,
        output_path: str,
        num_pages: int = 1,
        title: Optional[str] = None,
        include_measures: bool = False,
        measures_per_staff: int = 4
    ):
        """
        Create blank staff paper PDF.

        Args:
            output_path: Path for output PDF
            num_pages: Number of pages to generate
            title: Optional title at top of page
            include_measures: Draw measure lines
            measures_per_staff: Number of measures per staff
        """
        c = canvas.Canvas(output_path, pagesize=letter)

        for page in range(num_pages):
            # Draw title if provided
            if title:
                c.setFont("Helvetica-Bold", 16)
                c.drawCentredString(
                    self.PAGE_WIDTH / 2,
                    self.PAGE_HEIGHT - 0.4 * inch,
                    title
                )

            # Draw page number
            c.setFont("Helvetica", 10)
            c.drawCentredString(
                self.PAGE_WIDTH / 2,
                0.4 * inch,
                f"Page {page + 1}"
            )

            # Draw all staves
            for staff_y in self.staff_positions:
                self.draw_staff_lines(c, staff_y)

                if include_measures:
                    # Draw initial barline
                    self.draw_barline(c, self.LEFT_MARGIN, staff_y, 'single')

                    # Calculate measure width
                    staff_width = self.PAGE_WIDTH - self.LEFT_MARGIN - self.RIGHT_MARGIN
                    measure_width = staff_width / measures_per_staff

                    # Draw measure barlines
                    for i in range(1, measures_per_staff + 1):
                        x_pos = self.LEFT_MARGIN + (i * measure_width)
                        line_type = 'final' if i == measures_per_staff else 'single'
                        self.draw_barline(c, x_pos, staff_y, line_type)

            # New page
            if page < num_pages - 1:
                c.showPage()

        c.save()
        print(f"✓ Created blank staff paper: {output_path}")
        print(f"  Pages: {num_pages}, Staves per page: {self.staves_per_page}")

    def create_score_template(
        self,
        output_path: str,
        instrument_name: str,
        clef: str = 'treble',
        time_signature: Tuple[int, int] = (4, 4),
        num_pages: int = 1,
        measures_per_staff: int = 4
    ):
        """
        Create a score template with clef and time signature.

        Args:
            output_path: Path for output PDF
            instrument_name: Name of instrument
            clef: Clef type ('treble', 'bass', 'alto')
            time_signature: Time signature tuple
            num_pages: Number of pages
            measures_per_staff: Measures per staff
        """
        c = canvas.Canvas(output_path, pagesize=letter)

        for page in range(num_pages):
            # Draw title
            c.setFont("Helvetica-Bold", 18)
            c.drawCentredString(
                self.PAGE_WIDTH / 2,
                self.PAGE_HEIGHT - 0.4 * inch,
                instrument_name
            )

            # Draw page number
            c.setFont("Helvetica", 10)
            c.drawCentredString(
                self.PAGE_WIDTH / 2,
                0.4 * inch,
                f"Page {page + 1}"
            )

            # Draw all staves
            for staff_idx, staff_y in enumerate(self.staff_positions):
                self.draw_staff_lines(c, staff_y)

                # Only draw clef and time sig on first staff or new systems
                if page == 0 and staff_idx == 0:
                    # Draw clef
                    clef_x = self.LEFT_MARGIN + 0.2 * inch
                    self.draw_clef(c, clef_x, staff_y, clef)

                    # Draw time signature
                    time_sig_x = self.LEFT_MARGIN + 0.7 * inch
                    self.draw_time_signature(c, time_sig_x, staff_y, time_signature)

                    # First measure starts after time signature
                    measure_start = self.LEFT_MARGIN + 1.1 * inch
                else:
                    measure_start = self.LEFT_MARGIN

                # Draw measures
                staff_width = self.PAGE_WIDTH - measure_start - self.RIGHT_MARGIN
                measure_width = staff_width / measures_per_staff

                # Initial barline
                self.draw_barline(c, measure_start, staff_y, 'single')

                # Measure barlines
                for i in range(1, measures_per_staff + 1):
                    x_pos = measure_start + (i * measure_width)
                    line_type = 'final' if i == measures_per_staff else 'single'
                    self.draw_barline(c, x_pos, staff_y, line_type)

            if page < num_pages - 1:
                c.showPage()

        c.save()
        print(f"✓ Created score template: {output_path}")
        print(f"  Instrument: {instrument_name}")
        print(f"  Clef: {clef}, Time: {time_signature[0]}/{time_signature[1]}")

    def create_multipart_score_paper(
        self,
        output_path: str,
        parts: List[Dict[str, str]],
        time_signature: Tuple[int, int] = (4, 4),
        staves_per_part: int = 1
    ):
        """
        Create multi-part score paper with different instruments.

        Args:
            output_path: Path for output PDF
            parts: List of part dictionaries with 'name' and 'clef'
            time_signature: Time signature
            staves_per_part: Number of staves per instrument
        """
        c = canvas.Canvas(output_path, pagesize=letter)

        # Title page
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(
            self.PAGE_WIDTH / 2,
            self.PAGE_HEIGHT - 2 * inch,
            "Multi-Part Score"
        )

        c.setFont("Helvetica", 14)
        y_pos = self.PAGE_HEIGHT - 3 * inch

        c.drawString(inch, y_pos, "Instrumentation:")
        y_pos -= 0.4 * inch

        c.setFont("Helvetica", 12)
        for part in parts:
            c.drawString(1.5 * inch, y_pos, f"• {part['name']} ({part['clef']} clef)")
            y_pos -= 0.3 * inch

        c.showPage()

        # Score pages - one page per part
        for part in parts:
            # Draw part name
            c.setFont("Helvetica-Bold", 18)
            c.drawCentredString(
                self.PAGE_WIDTH / 2,
                self.PAGE_HEIGHT - 0.4 * inch,
                part['name']
            )

            # Draw staves for this part
            staves_to_draw = min(staves_per_part * self.staves_per_page, self.staves_per_page)

            for staff_idx in range(staves_to_draw):
                staff_y = self.staff_positions[staff_idx]
                self.draw_staff_lines(c, staff_y)

                # Draw clef and time signature on first staff
                if staff_idx == 0:
                    clef_x = self.LEFT_MARGIN + 0.2 * inch
                    self.draw_clef(c, clef_x, staff_y, part['clef'])

                    time_sig_x = self.LEFT_MARGIN + 0.7 * inch
                    self.draw_time_signature(c, time_sig_x, staff_y, time_signature)

            c.showPage()

        c.save()
        print(f"✓ Created multi-part score paper: {output_path}")
        print(f"  Parts: {len(parts)}")


def create_blank_sheet(output_path: str, num_pages: int = 1):
    """
    Quick function to create blank staff paper with 12 staves.

    Args:
        output_path: Path for output PDF
        num_pages: Number of pages
    """
    generator = StaffPaperGenerator(staves_per_page=12)
    generator.create_blank_staff_paper(
        output_path=output_path,
        num_pages=num_pages,
        title="Music Manuscript Paper"
    )


def create_instrument_part(
    output_path: str,
    instrument_name: str,
    clef: str = 'treble',
    time_signature: Tuple[int, int] = (4, 4),
    num_pages: int = 1
):
    """
    Quick function to create an instrument part template.

    Args:
        output_path: Path for output PDF
        instrument_name: Instrument name
        clef: Clef type
        time_signature: Time signature
        num_pages: Number of pages
    """
    generator = StaffPaperGenerator(staves_per_page=12)
    generator.create_score_template(
        output_path=output_path,
        instrument_name=instrument_name,
        clef=clef,
        time_signature=time_signature,
        num_pages=num_pages
    )


if __name__ == '__main__':
    # Demo usage
    print("Generating sample staff paper...")

    # Blank paper
    create_blank_sheet('blank_staff_paper.pdf', num_pages=5)

    # Instrument part
    create_instrument_part(
        'clarinet_part.pdf',
        instrument_name='Bb Clarinet',
        clef='treble',
        time_signature=(4, 4),
        num_pages=3
    )

    print("\nDone!")
