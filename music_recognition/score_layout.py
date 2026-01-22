"""
Advanced score layout with barline alignment and song collections.
Handles both full score books and individual song extraction.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from typing import List, Dict, Tuple, Optional
from pathlib import Path
from .staff_paper import StaffPaperGenerator


class AlignedScoreLayout:
    """Layout multi-part scores with synchronized barlines."""

    def __init__(self, staves_per_system: int = None):
        """
        Initialize aligned score layout.

        Args:
            staves_per_system: Number of staves per system (one for each part)
        """
        self.generator = StaffPaperGenerator()
        self.staves_per_system = staves_per_system
        self.system_spacing = 0.8 * inch  # Space between systems

    def calculate_system_positions(
        self,
        num_systems: int,
        staves_per_system: int
    ) -> List[List[float]]:
        """
        Calculate positions for multi-staff systems with proper spacing.

        Args:
            num_systems: Number of systems on the page
            staves_per_system: Number of staves in each system

        Returns:
            List of systems, each containing staff positions
        """
        page_height = self.generator.PAGE_HEIGHT
        top_margin = 1.5 * inch  # Extra space for title
        bottom_margin = self.generator.BOTTOM_MARGIN

        # Calculate total height needed
        staff_height = self.generator.STAFF_HEIGHT
        staff_spacing = 0.15 * inch  # Small gap between staves in a system

        # Height of one system
        system_height = (staves_per_system * staff_height) + ((staves_per_system - 1) * staff_spacing)

        # Available space
        available_height = page_height - top_margin - bottom_margin

        # Calculate spacing between systems
        total_system_height = num_systems * system_height
        remaining_space = available_height - total_system_height
        system_gap = remaining_space / (num_systems + 1) if num_systems > 0 else 0

        # Calculate positions
        systems = []
        current_y = page_height - top_margin - system_gap

        for _ in range(num_systems):
            system_staves = []
            y_pos = current_y

            for _ in range(staves_per_system):
                system_staves.append(y_pos)
                y_pos -= (staff_height + staff_spacing)

            systems.append(system_staves)
            current_y = y_pos - system_gap

        return systems

    def draw_aligned_barlines(
        self,
        c: canvas.Canvas,
        staff_positions: List[float],
        measure_x_positions: List[float],
        connect_staves: bool = True
    ):
        """
        Draw vertically aligned barlines across multiple staves.

        Args:
            c: ReportLab canvas
            staff_positions: Y-positions of staff top lines
            measure_x_positions: X-positions where barlines should be drawn
            connect_staves: Draw lines connecting staves (for full scores)
        """
        if not staff_positions or not measure_x_positions:
            return

        staff_height = self.generator.STAFF_HEIGHT

        for x_pos in measure_x_positions:
            c.setLineWidth(1.0)
            c.setStrokeColor(colors.black)

            if connect_staves:
                # Draw single line from top of first staff to bottom of last staff
                top_y = staff_positions[0]
                bottom_y = staff_positions[-1] - staff_height
                c.line(x_pos, top_y, x_pos, bottom_y)
            else:
                # Draw separate barlines for each staff
                for staff_y in staff_positions:
                    c.line(x_pos, staff_y, x_pos, staff_y - staff_height)

    def draw_system_bracket(
        self,
        c: canvas.Canvas,
        x_position: float,
        staff_positions: List[float],
        bracket_type: str = 'brace'
    ):
        """
        Draw a bracket or brace connecting staves in a system.

        Args:
            c: ReportLab canvas
            x_position: X-position for the bracket
            staff_positions: Y-positions of staves to connect
            bracket_type: 'brace', 'bracket', or 'line'
        """
        if not staff_positions:
            return

        top_y = staff_positions[0]
        bottom_y = staff_positions[-1] - self.generator.STAFF_HEIGHT

        c.setLineWidth(2.0)
        c.setStrokeColor(colors.black)

        if bracket_type == 'line':
            # Simple vertical line
            c.line(x_position, top_y, x_position, bottom_y)

        elif bracket_type == 'bracket':
            # Square bracket
            width = 8
            c.line(x_position, top_y, x_position, bottom_y)
            c.line(x_position, top_y, x_position + width, top_y)
            c.line(x_position, bottom_y, x_position + width, bottom_y)

        elif bracket_type == 'brace':
            # Simplified brace (using curves)
            middle_y = (top_y + bottom_y) / 2
            c.setLineWidth(1.5)

            # Top half
            c.bezier(
                x_position + 5, top_y,
                x_position - 3, (top_y + middle_y) / 2,
                x_position - 8, middle_y - 5,
                x_position - 10, middle_y
            )

            # Bottom half
            c.bezier(
                x_position - 10, middle_y,
                x_position - 8, middle_y + 5,
                x_position - 3, (middle_y + bottom_y) / 2,
                x_position + 5, bottom_y
            )

    def create_full_score_page(
        self,
        c: canvas.Canvas,
        parts: List[Dict],
        page_title: str = "",
        measures_per_system: int = 4,
        systems_per_page: int = 3
    ):
        """
        Create a full score page with multiple parts and aligned barlines.

        Args:
            c: ReportLab canvas
            parts: List of part dictionaries with 'name', 'clef', 'time_signature'
            page_title: Title for the page
            measures_per_system: Number of measures per system
            systems_per_page: Number of systems on the page
        """
        num_parts = len(parts)

        # Page title
        if page_title:
            c.setFont("Helvetica-Bold", 16)
            c.drawCentredString(
                self.generator.PAGE_WIDTH / 2,
                self.generator.PAGE_HEIGHT - 0.7 * inch,
                page_title
            )

        # Calculate system positions
        systems = self.calculate_system_positions(systems_per_page, num_parts)

        for system_idx, staff_positions in enumerate(systems):
            # Draw bracket connecting all staves
            bracket_x = self.generator.LEFT_MARGIN - 0.3 * inch
            self.draw_system_bracket(c, bracket_x, staff_positions, bracket_type='brace')

            # Draw part labels for first system
            if system_idx == 0:
                for part_idx, (staff_y, part) in enumerate(zip(staff_positions, parts)):
                    c.setFont("Helvetica", 9)
                    label_y = staff_y - (self.generator.STAFF_HEIGHT / 2)
                    c.drawRightString(
                        self.generator.LEFT_MARGIN - 0.5 * inch,
                        label_y,
                        part['name']
                    )

            # Draw staves
            for part_idx, (staff_y, part) in enumerate(zip(staff_positions, parts)):
                self.generator.draw_staff_lines(c, staff_y)

                # Add clef and time signature on first system
                if system_idx == 0:
                    clef_x = self.generator.LEFT_MARGIN + 0.1 * inch
                    self.generator.draw_clef(c, clef_x, staff_y, part.get('clef', 'treble'))

                    time_sig_x = self.generator.LEFT_MARGIN + 0.6 * inch
                    time_sig = part.get('time_signature', (4, 4))
                    self.generator.draw_time_signature(c, time_sig_x, staff_y, time_sig)

            # Calculate measure positions
            staff_width = self.generator.PAGE_WIDTH - self.generator.LEFT_MARGIN - self.generator.RIGHT_MARGIN
            measure_start = self.generator.LEFT_MARGIN + (1.0 * inch if system_idx == 0 else 0.2 * inch)
            usable_width = self.generator.PAGE_WIDTH - measure_start - self.generator.RIGHT_MARGIN
            measure_width = usable_width / measures_per_system

            # Draw aligned barlines
            barline_positions = [measure_start]
            for i in range(1, measures_per_system + 1):
                barline_positions.append(measure_start + (i * measure_width))

            self.draw_aligned_barlines(c, staff_positions, barline_positions, connect_staves=True)

            # Draw final barline as double
            final_x = barline_positions[-1]
            c.setLineWidth(0.5)
            c.line(final_x - 3, staff_positions[0], final_x - 3, staff_positions[-1] - self.generator.STAFF_HEIGHT)
            c.setLineWidth(2.5)
            c.line(final_x, staff_positions[0], final_x, staff_positions[-1] - self.generator.STAFF_HEIGHT)


class SongCollectionLayout:
    """Layout for song collections with multiple songs per page."""

    def __init__(self):
        """Initialize song collection layout."""
        self.generator = StaffPaperGenerator()

    def create_song_page(
        self,
        c: canvas.Canvas,
        songs: List[Dict],
        staves_per_song: int = 3,
        page_title: Optional[str] = None
    ):
        """
        Create a page with multiple songs.

        Args:
            c: ReportLab canvas
            songs: List of song dictionaries with 'title', 'clef', 'time_signature', 'measures'
            staves_per_song: Number of staves allocated to each song
            page_title: Optional page title
        """
        # Page title
        y_position = self.generator.PAGE_HEIGHT - 0.5 * inch

        if page_title:
            c.setFont("Helvetica-Bold", 16)
            c.drawCentredString(self.generator.PAGE_WIDTH / 2, y_position, page_title)
            y_position -= 0.5 * inch

        # Calculate spacing
        available_height = y_position - self.generator.BOTTOM_MARGIN
        total_staves_needed = len(songs) * staves_per_song
        space_between_songs = 0.3 * inch

        staff_spacing = (available_height - (len(songs) - 1) * space_between_songs) / total_staves_needed
        staff_spacing = min(staff_spacing, self.generator.STAFF_LINE_SPACING * 5)  # Cap spacing

        current_y = y_position

        for song_idx, song in enumerate(songs):
            song_title = song.get('title', f'Song {song_idx + 1}')
            clef = song.get('clef', 'treble')
            time_sig = song.get('time_signature', (4, 4))
            measures_per_staff = song.get('measures_per_staff', 4)

            # Draw song title above first staff
            c.setFont("Helvetica-Bold", 12)
            c.drawString(self.generator.LEFT_MARGIN, current_y, song_title)
            current_y -= 0.25 * inch

            # Draw staves for this song
            for staff_idx in range(staves_per_song):
                staff_y = current_y
                self.generator.draw_staff_lines(c, staff_y)

                # Add clef and time signature to first staff
                if staff_idx == 0:
                    clef_x = self.generator.LEFT_MARGIN + 0.2 * inch
                    self.generator.draw_clef(c, clef_x, staff_y, clef)

                    time_sig_x = self.generator.LEFT_MARGIN + 0.7 * inch
                    self.generator.draw_time_signature(c, time_sig_x, staff_y, time_sig)

                    # Barlines start after clef/time sig
                    measure_start = self.generator.LEFT_MARGIN + 1.1 * inch
                else:
                    measure_start = self.generator.LEFT_MARGIN

                # Draw measures
                usable_width = self.generator.PAGE_WIDTH - measure_start - self.generator.RIGHT_MARGIN
                measure_width = usable_width / measures_per_staff

                # Draw barlines
                for i in range(measures_per_staff + 1):
                    x_pos = measure_start + (i * measure_width)
                    line_type = 'final' if i == measures_per_staff else 'single'

                    if line_type == 'final':
                        # Double barline at end
                        c.setLineWidth(0.5)
                        c.line(x_pos - 3, staff_y, x_pos - 3, staff_y - self.generator.STAFF_HEIGHT)
                        c.setLineWidth(2.5)
                        c.line(x_pos, staff_y, x_pos, staff_y - self.generator.STAFF_HEIGHT)
                    else:
                        # Single barline
                        c.setLineWidth(1.0)
                        c.line(x_pos, staff_y, x_pos, staff_y - self.generator.STAFF_HEIGHT)

                current_y -= (self.generator.STAFF_HEIGHT + staff_spacing)

            # Space between songs
            current_y -= space_between_songs

    def extract_song_regions(
        self,
        songs: List[Dict],
        staves_per_song: int = 3
    ) -> List[Dict]:
        """
        Calculate bounding boxes for each song on the page.

        Args:
            songs: List of songs
            staves_per_song: Staves per song

        Returns:
            List of dictionaries with song metadata and region bounds
        """
        # This would be used to extract individual songs later
        regions = []

        y_position = self.generator.PAGE_HEIGHT - 1.0 * inch
        staff_spacing = 0.15 * inch
        space_between_songs = 0.3 * inch

        for song_idx, song in enumerate(songs):
            song_height = staves_per_song * (self.generator.STAFF_HEIGHT + staff_spacing) + 0.5 * inch

            regions.append({
                'song_index': song_idx,
                'title': song.get('title', f'Song {song_idx + 1}'),
                'y_top': y_position,
                'y_bottom': y_position - song_height,
                'x_left': self.generator.LEFT_MARGIN,
                'x_right': self.generator.PAGE_WIDTH - self.generator.RIGHT_MARGIN
            })

            y_position -= (song_height + space_between_songs)

        return regions


def create_full_score_book(
    output_path: str,
    score_title: str,
    composer: str,
    parts: List[Dict],
    num_pages: int = 10,
    measures_per_system: int = 4,
    systems_per_page: int = 3
):
    """
    Create a full score book with all parts together and aligned barlines.

    Args:
        output_path: Path for output PDF
        score_title: Title of the score
        composer: Composer name
        parts: List of parts with 'name', 'clef', 'time_signature'
        num_pages: Number of pages to create
        measures_per_system: Measures per system
        systems_per_page: Systems per page
    """
    c = canvas.Canvas(output_path, pagesize=letter)
    layout = AlignedScoreLayout()

    # Title page
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(layout.generator.PAGE_WIDTH / 2, layout.generator.PAGE_HEIGHT - 2 * inch, score_title)

    c.setFont("Helvetica", 18)
    c.drawCentredString(layout.generator.PAGE_WIDTH / 2, layout.generator.PAGE_HEIGHT - 2.7 * inch, f"by {composer}")

    c.showPage()

    # Score pages
    for page_num in range(1, num_pages + 1):
        layout.create_full_score_page(
            c,
            parts=parts,
            page_title=f"{score_title} - Page {page_num}",
            measures_per_system=measures_per_system,
            systems_per_page=systems_per_page
        )

        # Page number
        c.setFont("Helvetica", 10)
        c.drawCentredString(layout.generator.PAGE_WIDTH / 2, 0.5 * inch, str(page_num + 1))

        c.showPage()

    c.save()
    print(f"✓ Created full score book: {output_path}")
    print(f"  {num_pages} pages with {len(parts)} parts")
    print(f"  Barlines are vertically aligned across all parts")


def create_song_collection(
    output_path: str,
    collection_title: str,
    songs: List[Dict],
    songs_per_page: int = 4,
    staves_per_song: int = 3
):
    """
    Create a song collection with multiple songs per page.

    Args:
        output_path: Path for output PDF
        collection_title: Title of the collection
        songs: List of songs with 'title', 'clef', 'time_signature', 'measures_per_staff'
        songs_per_page: Number of songs per page
        staves_per_song: Number of staves for each song
    """
    c = canvas.Canvas(output_path, pagesize=letter)
    layout = SongCollectionLayout()

    # Title page
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(layout.generator.PAGE_WIDTH / 2, layout.generator.PAGE_HEIGHT - 2 * inch, collection_title)

    c.setFont("Helvetica", 12)
    c.drawCentredString(layout.generator.PAGE_WIDTH / 2, layout.generator.PAGE_HEIGHT - 2.5 * inch, f"{len(songs)} Songs")

    c.showPage()

    # Create pages with songs
    page_num = 1
    for i in range(0, len(songs), songs_per_page):
        songs_on_page = songs[i:i + songs_per_page]

        layout.create_song_page(
            c,
            songs=songs_on_page,
            staves_per_song=staves_per_song,
            page_title=f"{collection_title} - Page {page_num}"
        )

        # Page number
        c.setFont("Helvetica", 10)
        c.drawCentredString(layout.generator.PAGE_WIDTH / 2, 0.5 * inch, str(page_num + 1))

        c.showPage()
        page_num += 1

    c.save()
    print(f"✓ Created song collection: {output_path}")
    print(f"  {len(songs)} songs across {page_num} pages")
    print(f"  {songs_per_page} songs per page, {staves_per_song} staves per song")


if __name__ == '__main__':
    # Demo: Full score
    parts = [
        {'name': 'Flute', 'clef': 'treble', 'time_signature': (4, 4)},
        {'name': 'Bb Clarinet', 'clef': 'treble', 'time_signature': (4, 4)},
        {'name': 'Alto Sax', 'clef': 'treble', 'time_signature': (4, 4)},
        {'name': 'Trombone', 'clef': 'bass', 'time_signature': (4, 4)},
    ]

    create_full_score_book(
        'demo_full_score.pdf',
        'Concert March',
        'Composer Name',
        parts,
        num_pages=5
    )

    # Demo: Song collection
    songs = [
        {'title': '1. Amazing Grace', 'clef': 'treble', 'time_signature': (3, 4), 'measures_per_staff': 4},
        {'title': '2. Ode to Joy', 'clef': 'treble', 'time_signature': (4, 4), 'measures_per_staff': 4},
        {'title': '3. Twinkle Twinkle', 'clef': 'treble', 'time_signature': (4, 4), 'measures_per_staff': 4},
        {'title': '4. Mary Had a Little Lamb', 'clef': 'treble', 'time_signature': (4, 4), 'measures_per_staff': 4},
    ]

    create_song_collection(
        'demo_song_collection.pdf',
        'Classic Songs Collection',
        songs,
        songs_per_page=4,
        staves_per_song=3
    )
