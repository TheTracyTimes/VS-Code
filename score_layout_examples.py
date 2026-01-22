"""
Examples demonstrating aligned barlines and song collection layouts.

Two main modes:
1. Full Score Book: All parts together with vertically aligned barlines
2. Song Collection: Multiple songs per page that can be extracted later
"""

import argparse
from pathlib import Path

from music_recognition import (
    MultiPartScore,
    BandInstruments,
    create_full_score_book,
    create_song_collection,
    AlignedScoreLayout,
    SongCollectionLayout
)
from music_recognition.postprocessing import MusicScore
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def example_1_full_score_aligned_barlines():
    """Create a full score with all parts and aligned barlines."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Full Score Book with Aligned Barlines")
    print("="*70)
    print("\nThis mode is ideal for:")
    print("  - Complete ensemble scores")
    print("  - Parts that play together")
    print("  - Synchronized barlines across all staves")
    print("  - Professional conductor scores")

    parts = [
        {'name': 'C Flute', 'clef': 'treble', 'time_signature': (4, 4)},
        {'name': '1st Bb Clarinet', 'clef': 'treble', 'time_signature': (4, 4)},
        {'name': '2nd Bb Clarinet', 'clef': 'treble', 'time_signature': (4, 4)},
        {'name': '1st Eb Alto Sax', 'clef': 'treble', 'time_signature': (4, 4)},
        {'name': 'F French Horn', 'clef': 'treble', 'time_signature': (4, 4)},
        {'name': '1st Trombone', 'clef': 'bass', 'time_signature': (4, 4)},
        {'name': 'Euphonium', 'clef': 'bass', 'time_signature': (4, 4)},
    ]

    create_full_score_book(
        output_path='output/full_score_aligned.pdf',
        score_title='Concert March in Eb',
        composer='John Philip Sousa',
        parts=parts,
        num_pages=8,
        measures_per_system=4,
        systems_per_page=2  # 2 systems per page (each system has all parts)
    )

    print("\n✓ Created full score book")
    print("  File: output/full_score_aligned.pdf")
    print("  Features:")
    print("    - Barlines are vertically aligned across all parts")
    print("    - System brackets connect all staves")
    print("    - Part labels on the left")
    print("    - 4 measures per system, 2 systems per page")


def example_2_song_collection():
    """Create a song collection with multiple songs per page."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Song Collection (Multiple Songs per Page)")
    print("="*70)
    print("\nThis mode is ideal for:")
    print("  - Song books and collections")
    print("  - Individual songs that can be extracted later")
    print("  - Educational materials")
    print("  - Hymn books and songsters")

    songs = [
        {
            'title': '1. Amazing Grace',
            'clef': 'treble',
            'time_signature': (3, 4),
            'measures_per_staff': 4
        },
        {
            'title': '2. Ode to Joy',
            'clef': 'treble',
            'time_signature': (4, 4),
            'measures_per_staff': 4
        },
        {
            'title': '3. Twinkle Twinkle Little Star',
            'clef': 'treble',
            'time_signature': (4, 4),
            'measures_per_staff': 4
        },
        {
            'title': '4. Mary Had a Little Lamb',
            'clef': 'treble',
            'time_signature': (4, 4),
            'measures_per_staff': 4
        },
        {
            'title': '5. Happy Birthday',
            'clef': 'treble',
            'time_signature': (3, 4),
            'measures_per_staff': 4
        },
        {
            'title': '6. Jingle Bells',
            'clef': 'treble',
            'time_signature': (4, 4),
            'measures_per_staff': 4
        },
    ]

    create_song_collection(
        output_path='output/song_collection.pdf',
        collection_title='Classic Songs for Piano',
        songs=songs,
        songs_per_page=3,  # 3 songs per page
        staves_per_song=4   # 4 staves for each song
    )

    print("\n✓ Created song collection")
    print("  File: output/song_collection.pdf")
    print("  Features:")
    print("    - 6 songs total, 3 songs per page")
    print("    - 4 staves allocated to each song")
    print("    - Each song can be extracted separately later")
    print("    - Song titles clearly labeled")


def example_3_multipart_score_full_book():
    """Export a MultiPartScore as a full score book."""
    print("\n" + "="*70)
    print("EXAMPLE 3: MultiPartScore → Full Score Book")
    print("="*70)

    # Create multi-part score
    score = MultiPartScore(
        title="Spring Festival March",
        composer="Composer Name"
    )

    # Add parts
    parts_config = [
        ('C Flute', BandInstruments.C_FLUTE),
        ('1st Bb Clarinet', BandInstruments.Bb_CLARINET_1),
        ('2nd Bb Clarinet', BandInstruments.Bb_CLARINET_2),
        ('1st Eb Alto Sax', BandInstruments.Eb_ALTO_SAX_1),
        ('2nd Eb Alto Sax', BandInstruments.Eb_ALTO_SAX_2),
        ('F French Horn', BandInstruments.F_FRENCH_HORN_1),
        ('1st Trombone', BandInstruments.C_TROMBONE_1),
        ('2nd Trombone', BandInstruments.C_TROMBONE_2),
        ('Euphonium', BandInstruments.C_EUPHONIUM_BC),
    ]

    for part_name, instrument in parts_config:
        part = MusicScore()
        part.clef = instrument.clef.value
        part.time_signature = (4, 4)
        score.add_part(part_name, part, instrument)

    # Export as full score book
    score.export_full_score_book(
        'output/multipart_full_score.pdf',
        num_pages=10,
        measures_per_system=4,
        systems_per_page=2
    )

    print("\n✓ Exported MultiPartScore as full score book")
    print("  File: output/multipart_full_score.pdf")
    print("  9 parts, vertically aligned barlines")


def example_4_multipart_score_song_collection():
    """Export a MultiPartScore as a song collection."""
    print("\n" + "="*70)
    print("EXAMPLE 4: MultiPartScore → Song Collection")
    print("="*70)

    # Create multi-part score (treating each part as a separate song)
    score = MultiPartScore(
        title="Clarinet Method Book",
        composer="Various"
    )

    # Add "songs" (exercises or pieces)
    songs = [
        ('Exercise 1: Long Tones', BandInstruments.Bb_CLARINET_1),
        ('Exercise 2: Scales', BandInstruments.Bb_CLARINET_1),
        ('Exercise 3: Arpeggios', BandInstruments.Bb_CLARINET_1),
        ('Piece 1: Simple Melody', BandInstruments.Bb_CLARINET_1),
        ('Piece 2: March', BandInstruments.Bb_CLARINET_1),
        ('Piece 3: Waltz', BandInstruments.Bb_CLARINET_1),
    ]

    for song_name, instrument in songs:
        part = MusicScore()
        part.clef = instrument.clef.value
        part.time_signature = (4, 4)
        score.add_part(song_name, part, instrument)

    # Export as song collection
    score.export_as_song_collection(
        'output/clarinet_method_book.pdf',
        songs_per_page=3,
        staves_per_song=3
    )

    print("\n✓ Exported MultiPartScore as song collection")
    print("  File: output/clarinet_method_book.pdf")
    print("  6 exercises/pieces, 3 per page")


def example_5_custom_system_layout():
    """Create custom system layout with specific spacing."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Custom System Layout")
    print("="*70)

    c = canvas.Canvas('output/custom_layout.pdf', pagesize=letter)
    layout = AlignedScoreLayout()

    parts = [
        {'name': 'Soprano', 'clef': 'treble', 'time_signature': (3, 4)},
        {'name': 'Alto', 'clef': 'treble', 'time_signature': (3, 4)},
        {'name': 'Tenor', 'clef': 'treble', 'time_signature': (3, 4)},
        {'name': 'Bass', 'clef': 'bass', 'time_signature': (3, 4)},
    ]

    # Create page with specific layout
    layout.create_full_score_page(
        c,
        parts=parts,
        page_title="Choral Arrangement - Page 1",
        measures_per_system=3,  # 3 measures per system
        systems_per_page=4      # 4 systems on the page
    )

    c.save()

    print("\n✓ Created custom layout")
    print("  File: output/custom_layout.pdf")
    print("  4-part choral score, 3 measures per system")


def example_6_comparison():
    """Create both versions side-by-side for comparison."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Comparison of Both Modes")
    print("="*70)

    parts = [
        {'name': 'Flute', 'clef': 'treble', 'time_signature': (4, 4)},
        {'name': 'Clarinet', 'clef': 'treble', 'time_signature': (4, 4)},
        {'name': 'Alto Sax', 'clef': 'treble', 'time_signature': (4, 4)},
        {'name': 'Trombone', 'clef': 'bass', 'time_signature': (4, 4)},
    ]

    # Mode 1: Full score book
    create_full_score_book(
        output_path='output/comparison_full_score.pdf',
        score_title='Comparison - Full Score Mode',
        composer='Demo',
        parts=parts,
        num_pages=3,
        measures_per_system=4,
        systems_per_page=2
    )

    # Mode 2: Song collection (treating parts as songs)
    songs = [
        {'title': part['name'], 'clef': part['clef'], 'time_signature': part['time_signature'], 'measures_per_staff': 4}
        for part in parts
    ]

    create_song_collection(
        output_path='output/comparison_song_collection.pdf',
        collection_title='Comparison - Song Collection Mode',
        songs=songs,
        songs_per_page=4,
        staves_per_song=3
    )

    print("\n✓ Created both versions for comparison")
    print("  Full Score:      output/comparison_full_score.pdf")
    print("    - All parts together with aligned barlines")
    print("  Song Collection: output/comparison_song_collection.pdf")
    print("    - Each part separate, can be extracted later")


def print_usage_guide():
    """Print guide on when to use each mode."""
    print("\n" + "="*70)
    print("USAGE GUIDE: Which Mode to Use?")
    print("="*70)

    print("\n🎼 USE FULL SCORE BOOK MODE WHEN:")
    print("  ✓ Creating conductor scores")
    print("  ✓ All parts need to play together")
    print("  ✓ Barlines must align vertically across all parts")
    print("  ✓ You need to see all parts simultaneously")
    print("  ✓ Creating orchestral or band scores")
    print("\n  Example:")
    print("    score.export_full_score_book('score.pdf', num_pages=10)")

    print("\n📚 USE SONG COLLECTION MODE WHEN:")
    print("  ✓ Creating song books with multiple songs")
    print("  ✓ Each song is independent")
    print("  ✓ Songs will be extracted individually later")
    print("  ✓ Creating educational materials (exercises)")
    print("  ✓ Space efficiency is important (more per page)")
    print("\n  Example:")
    print("    score.export_as_song_collection('book.pdf', songs_per_page=4)")

    print("\n💡 KEY DIFFERENCES:")
    print("  Full Score:       Song Collection:")
    print("  - Aligned barlines  - Independent songs")
    print("  - System brackets   - Song titles")
    print("  - Part labels       - Compact layout")
    print("  - Fewer items/page  - More items/page")
    print("  - Conductor view    - Song book view")

    print("\n" + "="*70)


def main():
    """Run examples."""
    parser = argparse.ArgumentParser(
        description='Score layout and barline alignment examples',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all examples
  python score_layout_examples.py

  # Run specific example
  python score_layout_examples.py --example 1

  # Show usage guide
  python score_layout_examples.py --guide

Available Examples:
  1. Full score book with aligned barlines
  2. Song collection (multiple songs per page)
  3. MultiPartScore → Full score book
  4. MultiPartScore → Song collection
  5. Custom system layout
  6. Comparison of both modes
        """
    )

    parser.add_argument(
        '--example',
        type=int,
        choices=range(1, 7),
        help='Run a specific example (1-6)'
    )

    parser.add_argument(
        '--guide',
        action='store_true',
        help='Show usage guide'
    )

    args = parser.parse_args()

    # Create output directory
    Path('output').mkdir(exist_ok=True)

    print("\n" + "="*70)
    print("SCORE LAYOUT EXAMPLES - Aligned Barlines & Song Collections")
    print("="*70)

    if args.guide:
        print_usage_guide()
        return

    if args.example:
        # Run specific example
        examples = {
            1: example_1_full_score_aligned_barlines,
            2: example_2_song_collection,
            3: example_3_multipart_score_full_book,
            4: example_4_multipart_score_song_collection,
            5: example_5_custom_system_layout,
            6: example_6_comparison,
        }

        examples[args.example]()

    else:
        # Run all examples
        example_1_full_score_aligned_barlines()
        example_2_song_collection()
        example_3_multipart_score_full_book()
        example_4_multipart_score_song_collection()
        example_5_custom_system_layout()
        example_6_comparison()

        print("\n" + "="*70)
        print("All examples completed!")
        print("\nCheck the output/ directory for:")
        print("  - full_score_aligned.pdf")
        print("  - song_collection.pdf")
        print("  - multipart_full_score.pdf")
        print("  - clarinet_method_book.pdf")
        print("  - custom_layout.pdf")
        print("  - comparison_*.pdf")
        print("\nRun with --guide to see usage recommendations")
        print("="*70 + "\n")


if __name__ == '__main__':
    main()
