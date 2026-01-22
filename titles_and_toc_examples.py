"""
Examples demonstrating titles and table of contents functionality.
"""

import argparse
from pathlib import Path

from music_recognition import (
    StaffPaperGenerator,
    TableOfContentsGenerator,
    create_score_with_toc,
    MultiPartScore,
    BandInstruments
)
from music_recognition.postprocessing import MusicScore
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def example_1_title_above_staff():
    """Create score with title above first staff."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Title Above First Staff")
    print("="*70)

    generator = StaffPaperGenerator(staves_per_page=12)
    c = canvas.Canvas('output/score_with_title_above.pdf', pagesize=letter)

    # Page title at top
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(generator.PAGE_WIDTH / 2, generator.PAGE_HEIGHT - 0.5 * inch, "Symphony No. 1")

    c.setFont("Helvetica", 14)
    c.drawCentredString(generator.PAGE_WIDTH / 2, generator.PAGE_HEIGHT - 0.8 * inch, "by Ludwig van Beethoven")

    # Draw staves
    for staff_idx, staff_y in enumerate(generator.staff_positions):
        generator.draw_staff_lines(c, staff_y)

        # Add title above first staff
        if staff_idx == 0:
            generator.draw_title_above_staff(
                c,
                staff_y,
                "I. Allegro con brio",
                font_size=14,
                bold=True,
                centered=True
            )

        # Add clef to first staff
        if staff_idx == 0:
            clef_x = generator.LEFT_MARGIN + 0.2 * inch
            generator.draw_clef(c, clef_x, staff_y, 'treble')

            time_sig_x = generator.LEFT_MARGIN + 0.7 * inch
            generator.draw_time_signature(c, time_sig_x, staff_y, (3, 4))

    c.save()
    print("✓ Created score with title above staff")
    print("  File: output/score_with_title_above.pdf")


def example_2_titles_in_staff():
    """Create score with song titles within staves."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Song Titles Within Staves")
    print("="*70)

    generator = StaffPaperGenerator(staves_per_page=12)
    c = canvas.Canvas('output/score_with_song_titles.pdf', pagesize=letter)

    # Page title
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(generator.PAGE_WIDTH / 2, generator.PAGE_HEIGHT - 0.5 * inch, "Song Collection")

    # Define songs to place on staves
    songs = [
        ("1. Amazing Grace", 0),
        ("2. Ode to Joy", 3),
        ("3. Twinkle Twinkle", 6),
        ("4. Mary Had a Little Lamb", 9),
    ]

    # Draw all staves
    for staff_idx, staff_y in enumerate(generator.staff_positions):
        generator.draw_staff_lines(c, staff_y)

        # Check if this staff has a song title
        for song_title, song_staff_idx in songs:
            if staff_idx == song_staff_idx:
                # Draw title within the staff
                generator.draw_title_in_staff(
                    c,
                    generator.LEFT_MARGIN,
                    staff_y,
                    song_title,
                    font_size=12,
                    bold=True
                )

                # Add clef and time signature after title
                clef_x = generator.LEFT_MARGIN + 2.5 * inch
                generator.draw_clef(c, clef_x, staff_y, 'treble')

                time_sig_x = clef_x + 0.5 * inch
                generator.draw_time_signature(c, time_sig_x, staff_y, (4, 4))

    c.save()
    print("✓ Created score with song titles in staves")
    print("  File: output/score_with_song_titles.pdf")


def example_3_section_markers():
    """Create score with section markers (A, B, C, Verse, Chorus, etc.)."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Section Markers and Rehearsal Marks")
    print("="*70)

    generator = StaffPaperGenerator(staves_per_page=12)
    c = canvas.Canvas('output/score_with_sections.pdf', pagesize=letter)

    # Page title
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(generator.PAGE_WIDTH / 2, generator.PAGE_HEIGHT - 0.5 * inch, "March with Sections")

    # Define sections
    sections = [
        ("Intro", 0, 'box'),
        ("A", 2, 'box'),
        ("B", 4, 'box'),
        ("Bridge", 6, 'box'),
        ("A", 8, 'box'),
        ("Coda", 10, 'box'),
    ]

    # Draw staves
    for staff_idx, staff_y in enumerate(generator.staff_positions):
        generator.draw_staff_lines(c, staff_y)

        # Add section markers
        for section_name, section_staff_idx, style in sections:
            if staff_idx == section_staff_idx:
                generator.draw_section_marker(
                    c,
                    generator.LEFT_MARGIN,
                    staff_y,
                    section_name,
                    style=style
                )

        # Add clef to first staff
        if staff_idx == 0:
            clef_x = generator.LEFT_MARGIN + 1.2 * inch
            generator.draw_clef(c, clef_x, staff_y, 'treble')

            time_sig_x = generator.LEFT_MARGIN + 1.7 * inch
            generator.draw_time_signature(c, time_sig_x, staff_y, (2, 4))

    c.save()
    print("✓ Created score with section markers")
    print("  File: output/score_with_sections.pdf")


def example_4_simple_toc():
    """Create a simple table of contents."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Simple Table of Contents")
    print("="*70)

    c = canvas.Canvas('output/simple_toc.pdf', pagesize=letter)
    toc_gen = TableOfContentsGenerator()

    # Create TOC entries
    entries = [
        {'title': 'Introduction', 'page': 1},
        {'title': 'Chapter 1: Scales', 'page': 5},
        {'title': '  Major Scales', 'page': 6, 'indent': 1},
        {'title': '  Minor Scales', 'page': 10, 'indent': 1},
        {'title': 'Chapter 2: Arpeggios', 'page': 15},
        {'title': '  Major Arpeggios', 'page': 16, 'indent': 1},
        {'title': '  Minor Arpeggios', 'page': 20, 'indent': 1},
        {'title': 'Appendix', 'page': 25},
    ]

    toc_gen.create_toc_page(
        c,
        title="Music Theory Workbook",
        entries=entries
    )

    c.save()
    print("✓ Created simple table of contents")
    print("  File: output/simple_toc.pdf")


def example_5_parts_toc():
    """Create table of contents for multi-part score."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Multi-Part Score Table of Contents")
    print("="*70)

    c = canvas.Canvas('output/parts_toc.pdf', pagesize=letter)
    toc_gen = TableOfContentsGenerator()

    # Define parts
    parts = [
        {'name': 'C Flute', 'instrument': 'Non-transposing', 'page': 3, 'measures': 64},
        {'name': '1st Bb Clarinet', 'instrument': 'Transposing (Bb)', 'page': 4, 'measures': 64},
        {'name': '2nd Bb Clarinet', 'instrument': 'Transposing (Bb)', 'page': 5, 'measures': 64},
        {'name': '3rd Bb Clarinet', 'instrument': 'Transposing (Bb)', 'page': 6, 'measures': 64},
        {'name': '1st Eb Alto Sax', 'instrument': 'Transposing (Eb)', 'page': 7, 'measures': 64},
        {'name': '2nd Eb Alto Sax', 'instrument': 'Transposing (Eb)', 'page': 8, 'measures': 64},
        {'name': 'F French Horn', 'instrument': 'Transposing (F)', 'page': 9, 'measures': 64},
        {'name': '1st Trombone', 'instrument': 'Non-transposing', 'page': 10, 'measures': 64},
        {'name': '2nd Trombone', 'instrument': 'Non-transposing', 'page': 11, 'measures': 64},
        {'name': 'Euphonium', 'instrument': 'Non-transposing', 'page': 12, 'measures': 64},
    ]

    toc_gen.create_parts_toc(
        c,
        score_title="Concert March in Eb",
        composer="John Philip Sousa",
        parts=parts
    )

    c.save()
    print("✓ Created multi-part table of contents")
    print("  File: output/parts_toc.pdf")


def example_6_song_collection_toc():
    """Create table of contents for song collection."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Song Collection Table of Contents")
    print("="*70)

    c = canvas.Canvas('output/song_collection_toc.pdf', pagesize=letter)
    toc_gen = TableOfContentsGenerator()

    # Define songs
    songs = [
        {'title': 'Amazing Grace', 'composer': 'Traditional', 'page': 1, 'key': 'G Major', 'tempo': 'Andante'},
        {'title': 'Ode to Joy', 'composer': 'L. van Beethoven', 'page': 3, 'key': 'D Major', 'tempo': 'Allegro'},
        {'title': 'Canon in D', 'composer': 'J. Pachelbel', 'page': 5, 'key': 'D Major', 'tempo': 'Andante'},
        {'title': 'Für Elise', 'composer': 'L. van Beethoven', 'page': 8, 'key': 'A Minor', 'tempo': 'Poco moto'},
        {'title': 'Clair de Lune', 'composer': 'C. Debussy', 'page': 12, 'key': 'Db Major', 'tempo': 'Andante'},
        {'title': 'The Entertainer', 'composer': 'S. Joplin', 'page': 16, 'key': 'C Major', 'tempo': 'Not fast'},
        {'title': 'Moonlight Sonata', 'composer': 'L. van Beethoven', 'page': 20, 'key': 'C# Minor', 'tempo': 'Adagio'},
    ]

    toc_gen.create_song_list_toc(
        c,
        collection_title="Classic Piano Collection",
        songs=songs,
        include_keys=True,
        include_tempo=True
    )

    c.save()
    print("✓ Created song collection table of contents")
    print("  File: output/song_collection_toc.pdf")


def example_7_complete_score_with_toc():
    """Create complete score with TOC and blank pages."""
    print("\n" + "="*70)
    print("EXAMPLE 7: Complete Score with TOC and Blank Pages")
    print("="*70)

    parts = [
        {'name': 'C Flute', 'instrument': 'Flute', 'clef': 'treble', 'time_signature': (4, 4), 'measures': 48},
        {'name': '1st Bb Clarinet', 'instrument': 'Bb Clarinet', 'clef': 'treble', 'time_signature': (4, 4), 'measures': 48},
        {'name': '2nd Bb Clarinet', 'instrument': 'Bb Clarinet', 'clef': 'treble', 'time_signature': (4, 4), 'measures': 48},
        {'name': '1st Eb Alto Sax', 'instrument': 'Eb Alto Saxophone', 'clef': 'treble', 'time_signature': (4, 4), 'measures': 48},
        {'name': 'F French Horn', 'instrument': 'F French Horn', 'clef': 'treble', 'time_signature': (4, 4), 'measures': 48},
        {'name': '1st Trombone', 'instrument': 'Trombone', 'clef': 'bass', 'time_signature': (4, 4), 'measures': 48},
        {'name': 'Euphonium', 'instrument': 'Euphonium', 'clef': 'bass', 'time_signature': (4, 4), 'measures': 48},
    ]

    create_score_with_toc(
        output_path='output/complete_score_with_toc.pdf',
        score_title='Spring Festival Overture',
        composer='Composer Name',
        parts=parts,
        include_part_pages=True
    )

    print("✓ Created complete score with TOC")
    print("  File: output/complete_score_with_toc.pdf")


def example_8_multipart_score_with_toc():
    """Export MultiPartScore with table of contents."""
    print("\n" + "="*70)
    print("EXAMPLE 8: MultiPartScore with TOC Export")
    print("="*70)

    # Create a multi-part score
    score = MultiPartScore(
        title="Band Arrangement",
        composer="Composer Name"
    )

    # Add parts
    parts_config = [
        ('C Flute', BandInstruments.C_FLUTE),
        ('1st Bb Clarinet', BandInstruments.Bb_CLARINET_1),
        ('2nd Bb Clarinet', BandInstruments.Bb_CLARINET_2),
        ('1st Eb Alto Sax', BandInstruments.Eb_ALTO_SAX_1),
        ('F French Horn', BandInstruments.F_FRENCH_HORN_1),
        ('1st Trombone', BandInstruments.C_TROMBONE_1),
        ('Euphonium', BandInstruments.C_EUPHONIUM_BC),
    ]

    for part_name, instrument in parts_config:
        part = MusicScore()
        part.clef = instrument.clef.value
        part.time_signature = (4, 4)
        # Add some empty measures
        for _ in range(48):
            part.add_measure([])
        score.add_part(part_name, part, instrument)

    # Export with TOC
    score.export_with_toc('output/multipart_with_toc.pdf', include_blank_pages=True)

    print("✓ Exported MultiPartScore with TOC")
    print("  File: output/multipart_with_toc.pdf")


def main():
    """Run examples."""
    parser = argparse.ArgumentParser(
        description='Titles and Table of Contents examples',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all examples
  python titles_and_toc_examples.py

  # Run specific example
  python titles_and_toc_examples.py --example 1

Available Examples:
  1. Title above first staff
  2. Song titles within staves
  3. Section markers (A, B, C, Verse, Chorus)
  4. Simple table of contents
  5. Multi-part score table of contents
  6. Song collection table of contents
  7. Complete score with TOC and blank pages
  8. MultiPartScore with TOC export
        """
    )

    parser.add_argument(
        '--example',
        type=int,
        choices=range(1, 9),
        help='Run a specific example (1-8)'
    )

    args = parser.parse_args()

    # Create output directory
    Path('output').mkdir(exist_ok=True)

    print("\n" + "="*70)
    print("TITLES AND TABLE OF CONTENTS EXAMPLES")
    print("="*70)

    if args.example:
        # Run specific example
        examples = {
            1: example_1_title_above_staff,
            2: example_2_titles_in_staff,
            3: example_3_section_markers,
            4: example_4_simple_toc,
            5: example_5_parts_toc,
            6: example_6_song_collection_toc,
            7: example_7_complete_score_with_toc,
            8: example_8_multipart_score_with_toc,
        }

        examples[args.example]()

    else:
        # Run all examples
        example_1_title_above_staff()
        example_2_titles_in_staff()
        example_3_section_markers()
        example_4_simple_toc()
        example_5_parts_toc()
        example_6_song_collection_toc()
        example_7_complete_score_with_toc()
        example_8_multipart_score_with_toc()

        print("\n" + "="*70)
        print("All examples completed!")
        print("Check the output/ directory for generated PDFs")
        print("="*70 + "\n")


if __name__ == '__main__':
    main()
