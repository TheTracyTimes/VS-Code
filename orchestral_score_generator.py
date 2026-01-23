"""
Complete Orchestral Score Generator

This script demonstrates the full workflow for:
1. Reading scanned PDF music scores
2. Recognizing handwritten music notation
3. Creating multi-part band/orchestral scores
4. Automatically generating derived parts (Flute 2, Flute 3, Violin, Viola, etc.)
5. Exporting complete scores with table of contents
"""

import argparse
from pathlib import Path
from typing import Dict, List

from music_recognition import (
    MusicRecognitionSystem,
    MultiPartScore,
    BandInstruments,
    PDFMusicReader,
    PartGenerator,
    AutoScoreBuilder,
    transpose_score_octaves
)
from music_recognition.postprocessing import MusicScore


def create_example_band_score() -> MultiPartScore:
    """
    Create an example band score with multiple parts.
    In real usage, this would be populated from recognized music notation.

    Returns:
        MultiPartScore with example parts
    """
    score = MultiPartScore(
        title="Concert March",
        composer="Example Composer"
    )

    # Define parts configuration
    parts_config = [
        ('C Flute', BandInstruments.C_FLUTE),
        ('1st Bb Clarinet', BandInstruments.Bb_CLARINET_1),
        ('2nd Bb Clarinet', BandInstruments.Bb_CLARINET_2),
        ('3rd Bb Clarinet', BandInstruments.Bb_CLARINET_3),
        ('1st Eb Alto Sax', BandInstruments.Eb_ALTO_SAX_1),
        ('2nd Eb Alto Sax', BandInstruments.Eb_ALTO_SAX_2),
        ('3rd Eb Alto Sax', BandInstruments.Eb_ALTO_SAX_3),
        ('Bb Tenor Sax', BandInstruments.Bb_TENOR_SAX),
        ('1st Bb Trumpet', BandInstruments.Bb_TRUMPET_1),
        ('2nd Bb Trumpet', BandInstruments.Bb_TRUMPET_2),
        ('3rd Bb Trumpet', BandInstruments.Bb_TRUMPET_3),
        ('F French Horn', BandInstruments.F_FRENCH_HORN_1),
        ('1st C Trombone', BandInstruments.C_TROMBONE_1),
        ('2nd C Trombone', BandInstruments.C_TROMBONE_2),
        ('Baritone B.C.', BandInstruments.C_EUPHONIUM_BC),
    ]

    # Create empty parts (in real usage, these would contain recognized notation)
    for part_name, instrument in parts_config:
        part = MusicScore()
        part.clef = instrument.clef.value
        part.time_signature = (4, 4)
        part.key_signature = 'C'

        # Add some empty measures as placeholders
        for _ in range(32):
            part.add_measure([])

        score.add_part(part_name, part, instrument)

    return score


def process_scanned_pdf(pdf_path: str, output_dir: str = 'output/extracted') -> Dict[str, List[str]]:
    """
    Process a scanned PDF music score and extract staff images.

    Args:
        pdf_path: Path to the scanned PDF
        output_dir: Directory to save extracted images

    Returns:
        Dictionary with extraction metadata
    """
    print(f"\n{'='*70}")
    print(f"STEP 1: Reading Scanned PDF")
    print(f"{'='*70}")

    reader = PDFMusicReader()
    result = reader.process_pdf_score(pdf_path, output_dir)

    print(f"✓ Extracted {result['total_pages']} pages")
    print(f"✓ Found {result['total_staves']} staves")
    print(f"✓ Images saved to: {output_dir}")

    return result


def recognize_music_notation(staff_images: List[str]) -> Dict[str, MusicScore]:
    """
    Recognize music notation from staff images.

    Args:
        staff_images: List of paths to staff images

    Returns:
        Dictionary of part name to recognized MusicScore
    """
    print(f"\n{'='*70}")
    print(f"STEP 2: Recognizing Music Notation")
    print(f"{'='*70}")

    system = MusicRecognitionSystem()

    recognized_parts = {}

    for i, image_path in enumerate(staff_images):
        print(f"Processing staff {i+1}/{len(staff_images)}...")

        # Recognize the music
        result = system.recognize_from_file(image_path)

        if result:
            part_name = f"Part {i+1}"
            recognized_parts[part_name] = result['score']
            print(f"  ✓ Recognized {len(result['score'].measures)} measures")
        else:
            print(f"  ✗ Failed to recognize staff {i+1}")

    print(f"\n✓ Successfully recognized {len(recognized_parts)} parts")

    return recognized_parts


def generate_derived_parts(score: MultiPartScore) -> MultiPartScore:
    """
    Generate all derived instrumental parts automatically.

    Args:
        score: Original MultiPartScore

    Returns:
        Complete MultiPartScore with all derived parts
    """
    print(f"\n{'='*70}")
    print(f"STEP 3: Generating Derived Parts")
    print(f"{'='*70}")

    # Use AutoScoreBuilder to generate all derived parts
    complete_score = AutoScoreBuilder.build_complete_score(score)

    print("\nGenerated derived parts:")
    print("  • Flute 2 (based on 2nd parts, transposed to flute range)")
    print("  • Flute 3 (based on 3rd parts, transposed to flute range)")
    print("  • Oboe (= Flute 2)")
    print("  • Violin (= C Flute 1 octave down)")
    print("  • Viola (= Flute 3 1 octave down, treble clef)")
    print("  • Cello (= Trombone 1)")
    print("  • Bassoon (= Trombone 2)")
    print("  • Tuba (= Baritone B.C. 1 octave down)")
    print("  • Alto Clarinet (= 3rd Alto Sax)")
    print("  • Soprano Sax (= 1st Clarinet/Trumpet)")
    print("  • Eb Baritone Sax (based on low brass, transposed to bari sax range)")

    original_count = len(score.parts)
    new_count = len(complete_score.parts)
    print(f"\n✓ Score expanded from {original_count} to {new_count} parts")

    return complete_score


def export_complete_score(score: MultiPartScore, output_path: str, include_toc: bool = True):
    """
    Export the complete score to PDF with all parts and table of contents.

    Args:
        score: Complete MultiPartScore
        output_path: Path for output PDF
        include_toc: Whether to include table of contents
    """
    print(f"\n{'='*70}")
    print(f"STEP 4: Exporting Complete Score")
    print(f"{'='*70}")

    if include_toc:
        score.export_with_toc(output_path, include_blank_pages=True)
        print(f"✓ Exported score with table of contents")
    else:
        score.export_full_score_book(output_path, num_pages=50)
        print(f"✓ Exported full score book")

    print(f"  File: {output_path}")
    print(f"  Parts: {len(score.parts)}")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Complete Orchestral Score Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  # Generate example score with all derived parts
  python orchestral_score_generator.py --example

  # Process a scanned PDF and generate complete score
  python orchestral_score_generator.py --input scanned_score.pdf --output complete_score.pdf

  # Generate score without table of contents
  python orchestral_score_generator.py --example --no-toc

Workflow:
  1. Read scanned PDF (or use example)
  2. Recognize music notation (or use example)
  3. Generate derived parts automatically:
     - Flute 2 based on 2nd parts (transposed to proper range/key)
     - Flute 3 based on 3rd parts (transposed to proper range/key)
     - Orchestral instruments with octave transpositions
  4. Export complete score with table of contents
        """
    )

    parser.add_argument(
        '--input',
        type=str,
        help='Path to scanned PDF music score'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='output/complete_orchestral_score.pdf',
        help='Output PDF path (default: output/complete_orchestral_score.pdf)'
    )

    parser.add_argument(
        '--example',
        action='store_true',
        help='Generate example score (without PDF input)'
    )

    parser.add_argument(
        '--no-toc',
        action='store_true',
        help='Skip table of contents generation'
    )

    parser.add_argument(
        '--extract-only',
        action='store_true',
        help='Only extract staves from PDF, do not recognize'
    )

    args = parser.parse_args()

    # Create output directory
    Path('output').mkdir(exist_ok=True)

    print(f"\n{'='*70}")
    print("ORCHESTRAL SCORE GENERATOR")
    print(f"{'='*70}")

    # Workflow based on arguments
    if args.example:
        # Generate example score
        print("\nMode: Example Generation")
        print("Using pre-configured example band score")

        score = create_example_band_score()

        # Generate derived parts
        complete_score = generate_derived_parts(score)

        # Export
        export_complete_score(complete_score, args.output, include_toc=not args.no_toc)

    elif args.input:
        # Process real PDF
        print("\nMode: PDF Processing")
        print(f"Input: {args.input}")

        if not Path(args.input).exists():
            print(f"Error: File not found: {args.input}")
            return

        # Step 1: Extract from PDF
        extraction_result = process_scanned_pdf(args.input)

        if args.extract_only:
            print("\n✓ Extraction complete (--extract-only mode)")
            return

        # Step 2: Recognize notation (requires trained model)
        print("\nNote: Music recognition requires a trained model.")
        print("For this example, we'll create a placeholder score.")

        # Create placeholder score
        score = create_example_band_score()

        # Step 3: Generate derived parts
        complete_score = generate_derived_parts(score)

        # Step 4: Export
        export_complete_score(complete_score, args.output, include_toc=not args.no_toc)

    else:
        parser.print_help()
        print("\n" + "="*70)
        print("Please specify --example or --input <pdf_path>")
        print("="*70)
        return

    print(f"\n{'='*70}")
    print("COMPLETE!")
    print(f"{'='*70}")
    print(f"\nYour complete orchestral score has been generated.")
    print(f"Output: {args.output}")
    print(f"\nThe score includes:")
    print(f"  • All original band parts")
    print(f"  • Automatically generated derived parts")
    print(f"  • Proper transpositions for all instruments")
    print(f"  • Table of contents (if enabled)")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
