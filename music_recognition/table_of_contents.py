"""
Table of contents generation for multi-part scores and music books.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from typing import List, Dict, Tuple, Optional
from pathlib import Path


class TableOfContentsGenerator:
    """Generate table of contents pages for music scores."""

    PAGE_WIDTH = letter[0]
    PAGE_HEIGHT = letter[1]

    def __init__(self):
        """Initialize TOC generator."""
        pass

    def create_toc_page(
        self,
        c: canvas.Canvas,
        title: str,
        entries: List[Dict[str, any]],
        toc_title: str = "Table of Contents"
    ):
        """
        Create a table of contents page.

        Args:
            c: ReportLab canvas
            title: Main document title
            entries: List of TOC entries, each with 'title', 'page' (optional), 'indent' (optional)
            toc_title: Title for TOC section
        """
        # Main title
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(self.PAGE_WIDTH / 2, self.PAGE_HEIGHT - 1.5 * inch, title)

        # TOC title
        c.setFont("Helvetica-Bold", 18)
        c.drawString(inch, self.PAGE_HEIGHT - 2.5 * inch, toc_title)

        # Draw line under TOC title
        c.setLineWidth(1)
        c.line(inch, self.PAGE_HEIGHT - 2.6 * inch, self.PAGE_WIDTH - inch, self.PAGE_HEIGHT - 2.6 * inch)

        # TOC entries
        y_position = self.PAGE_HEIGHT - 3 * inch
        line_height = 0.25 * inch

        for entry in entries:
            entry_title = entry.get('title', '')
            page_num = entry.get('page', None)
            indent_level = entry.get('indent', 0)
            description = entry.get('description', '')

            # Calculate indent
            x_indent = inch + (0.3 * inch * indent_level)

            # Draw entry title
            if indent_level == 0:
                c.setFont("Helvetica-Bold", 12)
            else:
                c.setFont("Helvetica", 11)

            c.drawString(x_indent, y_position, entry_title)

            # Draw description if provided
            if description:
                c.setFont("Helvetica-Oblique", 10)
                c.drawString(x_indent + 0.2 * inch, y_position - 12, description)
                y_position -= 12

            # Draw page number if provided
            if page_num is not None:
                c.setFont("Helvetica", 11)
                page_text = str(page_num)
                page_x = self.PAGE_WIDTH - inch - c.stringWidth(page_text, "Helvetica", 11)

                # Draw dots between title and page number
                dots_start = x_indent + c.stringWidth(entry_title, c._fontname, c._fontsize) + 10
                dots_end = page_x - 10

                c.setFont("Helvetica", 8)
                dot_spacing = 8
                dot_x = dots_start
                while dot_x < dots_end:
                    c.drawString(dot_x, y_position + 2, ".")
                    dot_x += dot_spacing

                c.setFont("Helvetica", 11)
                c.drawString(page_x, y_position, page_text)

            y_position -= line_height

            # Check if we need a new page
            if y_position < 1.5 * inch:
                c.showPage()
                y_position = self.PAGE_HEIGHT - 1.5 * inch
                c.setFont("Helvetica-Bold", 14)
                c.drawString(inch, y_position + 0.3 * inch, f"{toc_title} (continued)")
                y_position -= 0.3 * inch

    def create_parts_toc(
        self,
        c: canvas.Canvas,
        score_title: str,
        composer: str,
        parts: List[Dict[str, any]]
    ):
        """
        Create a table of contents for a multi-part score.

        Args:
            c: ReportLab canvas
            score_title: Score title
            composer: Composer name
            parts: List of parts with 'name', 'instrument', 'page', 'measures' (optional)
        """
        # Title page
        c.setFont("Helvetica-Bold", 32)
        c.drawCentredString(self.PAGE_WIDTH / 2, self.PAGE_HEIGHT - 2 * inch, score_title)

        c.setFont("Helvetica", 20)
        c.drawCentredString(self.PAGE_WIDTH / 2, self.PAGE_HEIGHT - 2.7 * inch, f"by {composer}")

        # TOC section
        c.setFont("Helvetica-Bold", 18)
        c.drawString(inch, self.PAGE_HEIGHT - 4 * inch, "Instrumentation")

        # Draw line
        c.setLineWidth(1)
        c.line(inch, self.PAGE_HEIGHT - 4.1 * inch, self.PAGE_WIDTH - inch, self.PAGE_HEIGHT - 4.1 * inch)

        y_position = self.PAGE_HEIGHT - 4.5 * inch
        line_height = 0.3 * inch

        # Group parts by section if provided
        current_section = None

        for idx, part in enumerate(parts, 1):
            part_name = part.get('name', f'Part {idx}')
            instrument = part.get('instrument', '')
            page_num = part.get('page', None)
            measures = part.get('measures', None)
            section = part.get('section', None)

            # Draw section header if new section
            if section and section != current_section:
                if current_section is not None:
                    y_position -= 0.15 * inch

                c.setFont("Helvetica-Bold", 13)
                c.drawString(inch, y_position, section)
                y_position -= 0.25 * inch
                current_section = section

            # Draw part entry
            c.setFont("Helvetica-Bold", 12)
            c.drawString(inch + 0.2 * inch, y_position, f"{idx}. {part_name}")

            # Draw instrument and measures info
            info_parts = []
            if instrument:
                info_parts.append(instrument)
            if measures:
                info_parts.append(f"{measures} measures")

            if info_parts:
                c.setFont("Helvetica", 10)
                info_text = " • ".join(info_parts)
                c.drawString(inch + 0.4 * inch, y_position - 12, info_text)

            # Draw page number
            if page_num is not None:
                c.setFont("Helvetica", 11)
                page_text = f"p. {page_num}"
                page_x = self.PAGE_WIDTH - inch - c.stringWidth(page_text, "Helvetica", 11)
                c.drawString(page_x, y_position, page_text)

            y_position -= line_height

            # New page if needed
            if y_position < 1.5 * inch:
                c.showPage()
                y_position = self.PAGE_HEIGHT - 1.5 * inch
                c.setFont("Helvetica-Bold", 14)
                c.drawString(inch, y_position + 0.3 * inch, "Instrumentation (continued)")
                y_position -= 0.5 * inch

    def create_song_list_toc(
        self,
        c: canvas.Canvas,
        collection_title: str,
        songs: List[Dict[str, any]],
        include_keys: bool = True,
        include_tempo: bool = True
    ):
        """
        Create a table of contents for a song collection.

        Args:
            c: ReportLab canvas
            collection_title: Collection title
            songs: List of songs with 'title', 'composer', 'page', 'key', 'tempo' (optional)
            include_keys: Include key signatures in listing
            include_tempo: Include tempo markings in listing
        """
        # Title
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(self.PAGE_WIDTH / 2, self.PAGE_HEIGHT - 1.5 * inch, collection_title)

        # TOC title
        c.setFont("Helvetica-Bold", 18)
        c.drawString(inch, self.PAGE_HEIGHT - 2.5 * inch, "Contents")

        # Draw line
        c.setLineWidth(1)
        c.line(inch, self.PAGE_HEIGHT - 2.6 * inch, self.PAGE_WIDTH - inch, self.PAGE_HEIGHT - 2.6 * inch)

        y_position = self.PAGE_HEIGHT - 3 * inch
        line_height = 0.4 * inch

        for idx, song in enumerate(songs, 1):
            song_title = song.get('title', f'Song {idx}')
            composer = song.get('composer', '')
            page_num = song.get('page', None)
            key = song.get('key', '')
            tempo = song.get('tempo', '')

            # Song number and title
            c.setFont("Helvetica-Bold", 12)
            c.drawString(inch, y_position, f"{idx}. {song_title}")

            # Composer
            if composer:
                c.setFont("Helvetica-Oblique", 10)
                c.drawString(inch + 0.3 * inch, y_position - 13, composer)

            # Key and tempo on same line
            info_parts = []
            if include_keys and key:
                info_parts.append(f"Key: {key}")
            if include_tempo and tempo:
                info_parts.append(f"Tempo: {tempo}")

            if info_parts:
                c.setFont("Helvetica", 9)
                info_text = " • ".join(info_parts)
                c.drawString(inch + 0.3 * inch, y_position - 25, info_text)

            # Page number
            if page_num is not None:
                c.setFont("Helvetica", 11)
                page_text = str(page_num)
                page_x = self.PAGE_WIDTH - inch - c.stringWidth(page_text, "Helvetica", 11)

                # Draw dots
                title_width = c.stringWidth(f"{idx}. {song_title}", "Helvetica-Bold", 12)
                dots_start = inch + title_width + 10
                dots_end = page_x - 10

                c.setFont("Helvetica", 8)
                dot_x = dots_start
                while dot_x < dots_end:
                    c.drawString(dot_x, y_position + 2, ".")
                    dot_x += 8

                c.setFont("Helvetica", 11)
                c.drawString(page_x, y_position, page_text)

            y_position -= line_height

            # New page if needed
            if y_position < 1.5 * inch:
                c.showPage()
                y_position = self.PAGE_HEIGHT - 1.5 * inch
                c.setFont("Helvetica-Bold", 14)
                c.drawString(inch, y_position + 0.3 * inch, "Contents (continued)")
                y_position -= 0.5 * inch


def create_score_with_toc(
    output_path: str,
    score_title: str,
    composer: str,
    parts: List[Dict[str, any]],
    include_part_pages: bool = True
):
    """
    Create a complete score PDF with table of contents.

    Args:
        output_path: Path for output PDF
        score_title: Score title
        composer: Composer name
        parts: List of parts with metadata
        include_part_pages: Include blank part pages after TOC
    """
    from .staff_paper import StaffPaperGenerator

    c = canvas.Canvas(output_path, pagesize=letter)

    # Create TOC
    toc_gen = TableOfContentsGenerator()
    toc_gen.create_parts_toc(c, score_title, composer, parts)

    c.showPage()

    # Create part pages if requested
    if include_part_pages:
        generator = StaffPaperGenerator(staves_per_page=12)

        for part in parts:
            part_name = part.get('name', 'Part')
            instrument = part.get('instrument', '')
            clef = part.get('clef', 'treble')
            time_sig = part.get('time_signature', (4, 4))

            # Part title page or first staff page
            c.setFont("Helvetica-Bold", 18)
            c.drawCentredString(
                generator.PAGE_WIDTH / 2,
                generator.PAGE_HEIGHT - 0.5 * inch,
                part_name
            )

            if instrument:
                c.setFont("Helvetica", 12)
                c.drawCentredString(
                    generator.PAGE_WIDTH / 2,
                    generator.PAGE_HEIGHT - 0.75 * inch,
                    instrument
                )

            # Draw staves
            for staff_idx, staff_y in enumerate(generator.staff_positions):
                generator.draw_staff_lines(c, staff_y)

                # Add clef and time signature to first staff
                if staff_idx == 0:
                    clef_x = generator.LEFT_MARGIN + 0.2 * inch
                    generator.draw_clef(c, clef_x, staff_y, clef)

                    time_sig_x = generator.LEFT_MARGIN + 0.7 * inch
                    generator.draw_time_signature(c, time_sig_x, staff_y, time_sig)

            c.showPage()

    c.save()
    print(f"✓ Created score with table of contents: {output_path}")


if __name__ == '__main__':
    # Demo
    parts = [
        {'name': 'C Flute', 'instrument': 'Non-transposing', 'page': 3, 'measures': 64},
        {'name': '1st Bb Clarinet', 'instrument': 'Transposing (Bb)', 'page': 4, 'measures': 64},
        {'name': '2nd Bb Clarinet', 'instrument': 'Transposing (Bb)', 'page': 5, 'measures': 64},
        {'name': '1st Eb Alto Sax', 'instrument': 'Transposing (Eb)', 'page': 6, 'measures': 64},
        {'name': 'F French Horn', 'instrument': 'Transposing (F)', 'page': 7, 'measures': 64},
        {'name': '1st Trombone', 'instrument': 'Non-transposing', 'page': 8, 'measures': 64},
        {'name': 'Euphonium', 'instrument': 'Non-transposing', 'page': 9, 'measures': 64},
    ]

    create_score_with_toc(
        'demo_score_with_toc.pdf',
        'Concert March',
        'Composer Name',
        parts
    )

    print("Demo created: demo_score_with_toc.pdf")
