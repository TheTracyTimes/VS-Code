"""
Examples demonstrating PDF export functionality.
"""

import argparse
from pathlib import Path

from music_recognition import (
    MusicRecognitionSystem,
    MultiPartScore,
    ScoreAssembler,
    BandInstruments,
    StaffPaperGenerator,
    create_blank_sheet,
    create_instrument_part,
    check_pdf_backends
)


def example_1_blank_staff_paper():
    """Create blank staff paper with 12 staves per page."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Create Blank Staff Paper (12 staves/page)")
    print("="*70)

    # Create blank sheets
    create_blank_sheet(
        output_path='output/blank_staff_paper.pdf',
        num_pages=5
    )

    print("\n✓ Created 5 pages of blank staff paper")
    print("  File: output/blank_staff_paper.pdf")


def example_2_instrument_templates():
    """Create instrument part templates."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Create Instrument Part Templates")
    print("="*70)

    # Create templates for different instruments
    instruments = [
        ('Bb Clarinet', 'treble', (4, 4)),
        ('Eb Alto Saxophone', 'treble', (4, 4)),
        ('F French Horn', 'treble', (4, 4)),
        ('Trombone', 'bass', (4, 4)),
        ('Euphonium', 'bass', (3, 4)),
    ]

    Path('output/templates').mkdir(exist_ok=True, parents=True)

    for name, clef, time_sig in instruments:
        filename = name.replace(' ', '_').lower()
        create_instrument_part(
            output_path=f'output/templates/{filename}_template.pdf',
            instrument_name=name,
            clef=clef,
            time_signature=time_sig,
            num_pages=3
        )

    print(f"\n✓ Created {len(instruments)} instrument templates")
    print("  Directory: output/templates/")


def example_3_custom_staff_paper():
    """Create custom staff paper with specific settings."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Create Custom Staff Paper")
    print("="*70)

    generator = StaffPaperGenerator(staves_per_page=12)

    # Blank paper with measures
    generator.create_blank_staff_paper(
        output_path='output/staff_paper_with_measures.pdf',
        num_pages=3,
        title="Music Manuscript Paper",
        include_measures=True,
        measures_per_staff=4
    )

    print("\n✓ Created staff paper with 4 measures per staff")
    print("  File: output/staff_paper_with_measures.pdf")


def example_4_score_template():
    """Create a complete score template for a specific instrument."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Create Score Template with Clef and Time Signature")
    print("="*70)

    generator = StaffPaperGenerator(staves_per_page=12)

    generator.create_score_template(
        output_path='output/clarinet_score.pdf',
        instrument_name='Bb Clarinet',
        clef='treble',
        time_signature=(4, 4),
        num_pages=5,
        measures_per_staff=4
    )

    print("\n✓ Created clarinet score template")
    print("  File: output/clarinet_score.pdf")
    print("  12 staves/page, 4 measures/staff, 5 pages")


def example_5_multipart_template():
    """Create templates for a band arrangement."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Create Multi-Part Score Templates")
    print("="*70)

    generator = StaffPaperGenerator(staves_per_page=12)

    # Define the parts
    parts = [
        {'name': 'C Flute', 'clef': 'treble'},
        {'name': '1st Bb Clarinet', 'clef': 'treble'},
        {'name': '2nd Bb Clarinet', 'clef': 'treble'},
        {'name': '1st Eb Alto Sax', 'clef': 'treble'},
        {'name': 'F French Horn', 'clef': 'treble'},
        {'name': 'Euphonium', 'clef': 'bass'},
        {'name': '1st Trombone', 'clef': 'bass'},
        {'name': '2nd Trombone', 'clef': 'bass'},
    ]

    generator.create_multipart_score_paper(
        output_path='output/band_arrangement_template.pdf',
        parts=parts,
        time_signature=(4, 4),
        staves_per_part=1
    )

    print(f"\n✓ Created multi-part template with {len(parts)} parts")
    print("  File: output/band_arrangement_template.pdf")


def example_6_export_recognized_score():
    """Export a recognized score to PDF."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Export Recognized Score to PDF")
    print("="*70)

    try:
        # Initialize recognition system
        system = MusicRecognitionSystem(
            model_path='checkpoints/best_model.pth'
        )

        # Recognize a score
        print("\nRecognizing music from image...")
        score = system.recognize('sample_music.jpg')

        # Export to PDF (tries multiple methods)
        print("\nExporting to PDF...")
        success = system.export_score(
            score,
            'output/recognized_score.pdf',
            format='pdf'
        )

        if success:
            print("\n✓ PDF exported successfully")
            print("  File: output/recognized_score.pdf")
        else:
            print("\n❌ PDF export failed - check PDF backends")

    except FileNotFoundError:
        print("\n⚠ Sample image not found")
        print("  To run this example, place a music score image at 'sample_music.jpg'")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def example_7_multipart_pdf():
    """Export a multi-part score to PDF."""
    print("\n" + "="*70)
    print("EXAMPLE 7: Export Multi-Part Score to PDF")
    print("="*70)

    try:
        # Create a sample multi-part score
        from music_recognition.postprocessing import MusicScore

        score = MultiPartScore(
            title="Band Arrangement",
            composer="Composer Name"
        )

        # Add some parts (normally these would be recognized from images)
        parts_config = [
            ('C Flute', BandInstruments.C_FLUTE),
            ('Bb Clarinet', BandInstruments.Bb_CLARINET_1),
            ('Eb Alto Sax', BandInstruments.Eb_ALTO_SAX_1),
            ('Trombone', BandInstruments.C_TROMBONE_1),
        ]

        for part_name, instrument in parts_config:
            part = MusicScore()
            part.clef = instrument.clef.value
            score.add_part(part_name, part, instrument)

        # Export full score to PDF
        print("\nExporting full score to PDF...")
        score.export_pdf('output/full_band_score.pdf', method='auto')

        # Export individual parts as PDFs
        print("\nExporting individual parts as PDFs...")
        score.export_parts_as_pdf('output/pdf_parts/', method='auto')

        # Create parts book
        print("\nCreating parts book...")
        score.export_parts_book('output/parts_book.pdf')

        print("\n✓ All PDF exports completed")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nNote: For best PDF output, install music21:")
        print("  pip install music21")


def example_8_check_backends():
    """Check available PDF export backends."""
    print("\n" + "="*70)
    print("EXAMPLE 8: Check PDF Export Backends")
    print("="*70)

    check_pdf_backends()

    print("\nRecommendations:")
    print("  - For professional notation: Install music21 + MuseScore")
    print("  - For basic output: reportlab (already installed)")
    print("  - For web-based: Install verovio")


def main():
    """Run examples."""
    parser = argparse.ArgumentParser(
        description='PDF export examples',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all examples
  python pdf_examples.py

  # Run specific example
  python pdf_examples.py --example 1

  # Check PDF backends
  python pdf_examples.py --check-backends

Available Examples:
  1. Create blank staff paper (12 staves/page)
  2. Create instrument part templates
  3. Create custom staff paper with measures
  4. Create score template with clef and time signature
  5. Create multi-part score templates
  6. Export recognized score to PDF
  7. Export multi-part score to PDF
  8. Check PDF export backends
        """
    )

    parser.add_argument(
        '--example',
        type=int,
        choices=range(1, 9),
        help='Run a specific example (1-8)'
    )

    parser.add_argument(
        '--check-backends',
        action='store_true',
        help='Check available PDF backends'
    )

    args = parser.parse_args()

    # Create output directory
    Path('output').mkdir(exist_ok=True)

    print("\n" + "="*70)
    print("PDF EXPORT EXAMPLES")
    print("="*70)

    if args.check_backends:
        example_8_check_backends()

    elif args.example:
        # Run specific example
        examples = {
            1: example_1_blank_staff_paper,
            2: example_2_instrument_templates,
            3: example_3_custom_staff_paper,
            4: example_4_score_template,
            5: example_5_multipart_template,
            6: example_6_export_recognized_score,
            7: example_7_multipart_pdf,
            8: example_8_check_backends,
        }

        examples[args.example]()

    else:
        # Run examples that don't require input files
        example_1_blank_staff_paper()
        example_2_instrument_templates()
        example_3_custom_staff_paper()
        example_4_score_template()
        example_5_multipart_template()
        example_8_check_backends()

        print("\n" + "="*70)
        print("To run examples 6-7, you need:")
        print("  - A trained model (for example 6)")
        print("  - Part images (for example 7)")
        print("\nRun specific examples with: python pdf_examples.py --example N")
        print("="*70 + "\n")


if __name__ == '__main__':
    main()
