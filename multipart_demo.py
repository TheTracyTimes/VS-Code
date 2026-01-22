"""
Demo script for multi-part music recognition and score assembly.
"""

import argparse
from pathlib import Path

from music_recognition import (
    MusicRecognitionSystem,
    MultiPartScore,
    ScoreAssembler,
    BandInstruments,
    StandardEnsembles,
    list_all_instruments
)


def demo_list_instruments():
    """Demonstrate listing all available instruments."""
    print("\n" + "="*70)
    print("AVAILABLE INSTRUMENTS")
    print("="*70)

    instruments = list_all_instruments()

    categories = {
        "Flutes": [],
        "Clarinets": [],
        "Saxophones": [],
        "Trumpets": [],
        "Horns": [],
        "Trombones": [],
        "Low Brass": [],
    }

    for name, config in instruments.items():
        if "Flute" in name or "Piccolo" in name:
            categories["Flutes"].append(config)
        elif "Clarinet" in name:
            categories["Clarinets"].append(config)
        elif "Saxophone" in name or "Sax" in name:
            categories["Saxophones"].append(config)
        elif "Trumpet" in name:
            categories["Trumpets"].append(config)
        elif "Horn" in name:
            categories["Horns"].append(config)
        elif "Trombone" in name:
            categories["Trombones"].append(config)
        elif "Baritone" in name or "Euphonium" in name or "Tuba" in name:
            categories["Low Brass"].append(config)

    for category, insts in categories.items():
        if insts:
            print(f"\n{category}:")
            for inst in insts:
                trans = "Concert pitch" if inst.transposition.name == "NONE" else f"Transposing: {inst.transposition.name}"
                print(f"  • {inst.name} ({inst.short_name})")
                print(f"    {trans}, Clef: {inst.clef.value}, Range: {inst.range_low}-{inst.range_high}")


def demo_create_user_ensemble():
    """
    Create an ensemble with the user's specified instrumentation:
    - C Flute
    - 1st, 2nd, 3rd Bb Clarinet/Trumpet
    - 1st, 2nd, 3rd Eb Alto Sax
    - F French Horn
    - Bb Bass Clarinet/Baritone T.C.
    - Baritone B.C./Euphonium
    - 1st, 2nd Trombone
    - 3rd Bb Clarinet/Trumpet/Tenor Sax
    """
    print("\n" + "="*70)
    print("CREATING USER-SPECIFIED ENSEMBLE")
    print("="*70)

    # Create the score with user's instrumentation
    score = MultiPartScore(
        title="My Band Arrangement",
        composer="Composer Name"
    )

    # Define the parts in score order (top to bottom)
    from music_recognition.postprocessing import MusicScore

    parts_config = [
        ("C Flute", BandInstruments.C_FLUTE),
        ("1st Bb Clarinet", BandInstruments.Bb_CLARINET_1),
        ("2nd Bb Clarinet", BandInstruments.Bb_CLARINET_2),
        ("3rd Bb Clarinet", BandInstruments.Bb_CLARINET_3),
        ("1st Eb Alto Sax", BandInstruments.Eb_ALTO_SAX_1),
        ("2nd Eb Alto Sax", BandInstruments.Eb_ALTO_SAX_2),
        ("3rd Eb Alto Sax", BandInstruments.Eb_ALTO_SAX_3),
        ("F French Horn", BandInstruments.F_FRENCH_HORN_1),
        ("Bb Bass Clarinet", BandInstruments.Bb_BASS_CLARINET),
        ("Bb Baritone T.C.", BandInstruments.Bb_BARITONE_TC),
        ("Euphonium B.C.", BandInstruments.C_EUPHONIUM_BC),
        ("1st Trombone", BandInstruments.C_TROMBONE_1),
        ("2nd Trombone", BandInstruments.C_TROMBONE_2),
        ("Bb Tenor Sax", BandInstruments.Bb_TENOR_SAX),
    ]

    print(f"\nAdding {len(parts_config)} parts to the score:\n")

    for part_name, instrument in parts_config:
        empty_score = MusicScore()
        empty_score.clef = instrument.clef.value
        score.add_part(part_name, empty_score, instrument)

        trans_info = "Non-transposing" if instrument.transposition.name == "NONE" else f"Transposing ({instrument.transposition.name})"
        print(f"  ✓ {part_name:30} - {trans_info:25} - Clef: {instrument.clef.value}")

    print(f"\n✓ Created ensemble with {len(score.parts)} parts")

    return score


def demo_process_parts(parts_dir: str, output_path: str, model_path: str = None):
    """
    Process multiple part images and create a complete score.

    Args:
        parts_dir: Directory containing part images
        output_path: Path to save the output MusicXML
        model_path: Optional path to trained model
    """
    print("\n" + "="*70)
    print("PROCESSING MULTI-PART SCORE FROM IMAGES")
    print("="*70)

    # Initialize recognition system
    system = MusicRecognitionSystem(model_path=model_path)

    # Create assembler
    assembler = ScoreAssembler(recognition_system=system)

    # Define which images correspond to which parts
    # Expecting files named like: flute.jpg, clarinet1.jpg, etc.
    parts_dir_path = Path(parts_dir)

    part_images = {}
    instruments = {}

    # Map filenames to instruments
    file_mappings = {
        'flute': ('C Flute', BandInstruments.C_FLUTE),
        'clarinet1': ('1st Bb Clarinet', BandInstruments.Bb_CLARINET_1),
        'clarinet2': ('2nd Bb Clarinet', BandInstruments.Bb_CLARINET_2),
        'clarinet3': ('3rd Bb Clarinet', BandInstruments.Bb_CLARINET_3),
        'alto_sax1': ('1st Eb Alto Sax', BandInstruments.Eb_ALTO_SAX_1),
        'alto_sax2': ('2nd Eb Alto Sax', BandInstruments.Eb_ALTO_SAX_2),
        'alto_sax3': ('3rd Eb Alto Sax', BandInstruments.Eb_ALTO_SAX_3),
        'horn': ('F French Horn', BandInstruments.F_FRENCH_HORN_1),
        'bass_clarinet': ('Bb Bass Clarinet', BandInstruments.Bb_BASS_CLARINET),
        'baritone': ('Bb Baritone T.C.', BandInstruments.Bb_BARITONE_TC),
        'euphonium': ('Euphonium B.C.', BandInstruments.C_EUPHONIUM_BC),
        'trombone1': ('1st Trombone', BandInstruments.C_TROMBONE_1),
        'trombone2': ('2nd Trombone', BandInstruments.C_TROMBONE_2),
        'tenor_sax': ('Bb Tenor Sax', BandInstruments.Bb_TENOR_SAX),
    }

    print(f"\nLooking for part images in: {parts_dir_path}")

    for file_key, (part_name, instrument) in file_mappings.items():
        # Look for image files with this key
        for ext in ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']:
            image_path = parts_dir_path / f"{file_key}{ext}"
            if image_path.exists():
                part_images[part_name] = str(image_path)
                instruments[part_name] = instrument
                print(f"  Found: {part_name} -> {image_path.name}")
                break

    if not part_images:
        print("\n❌ No part images found!")
        print("\nExpected filenames:")
        for key in file_mappings.keys():
            print(f"  - {key}.jpg (or .png)")
        return

    print(f"\n✓ Found {len(part_images)} parts")

    # Process all parts
    multi_score = assembler.create_score_from_parts(
        part_images=part_images,
        instruments=instruments,
        title="Band Arrangement",
        composer="Composer"
    )

    # Export to MusicXML
    print(f"\nExporting to: {output_path}")
    multi_score.export_musicxml(output_path)

    # Also export concert pitch version
    concert_path = output_path.replace('.xml', '_concert.xml')
    print(f"Exporting concert pitch score to: {concert_path}")
    multi_score.export_musicxml(concert_path, concert_pitch=True)

    # Export individual parts
    parts_output_dir = str(Path(output_path).parent / "parts")
    print(f"Exporting individual parts to: {parts_output_dir}/")
    multi_score.export_parts_separately(parts_output_dir, format='musicxml')

    print("\n✓ Processing complete!")


def demo_transposition_example():
    """Demonstrate transposition between concert pitch and written pitch."""
    print("\n" + "="*70)
    print("TRANSPOSITION DEMONSTRATION")
    print("="*70)

    from music_recognition import Transposer, Note

    # Example: Bb Clarinet
    print("\n--- Bb Clarinet Transposition ---")
    print("When a Bb clarinet plays a written C, it sounds a Bb (concert pitch)")

    clarinet_transposer = Transposer(BandInstruments.Bb_CLARINET_1)

    written_pitch = "C5"
    concert_pitch = clarinet_transposer.written_to_concert(written_pitch)
    print(f"Written pitch: {written_pitch} -> Concert pitch: {concert_pitch}")

    concert_pitch2 = "C4"
    written_pitch2 = clarinet_transposer.concert_to_written(concert_pitch2)
    print(f"Concert pitch: {concert_pitch2} -> Written pitch: {written_pitch2}")

    # Example: Eb Alto Sax
    print("\n--- Eb Alto Saxophone Transposition ---")
    print("When an Eb alto sax plays a written C, it sounds an Eb (concert pitch)")

    sax_transposer = Transposer(BandInstruments.Eb_ALTO_SAX_1)

    written_pitch = "C5"
    concert_pitch = sax_transposer.written_to_concert(written_pitch)
    print(f"Written pitch: {written_pitch} -> Concert pitch: {concert_pitch}")

    concert_pitch2 = "Eb4"
    written_pitch2 = sax_transposer.concert_to_written(concert_pitch2)
    print(f"Concert pitch: {concert_pitch2} -> Written pitch: {written_pitch2}")

    # Example: F French Horn
    print("\n--- F French Horn Transposition ---")
    print("When an F horn plays a written C, it sounds an F (concert pitch)")

    horn_transposer = Transposer(BandInstruments.F_FRENCH_HORN_1)

    written_pitch = "C5"
    concert_pitch = horn_transposer.written_to_concert(written_pitch)
    print(f"Written pitch: {written_pitch} -> Concert pitch: {concert_pitch}")

    concert_pitch2 = "F3"
    written_pitch2 = horn_transposer.concert_to_written(concert_pitch2)
    print(f"Concert pitch: {concert_pitch2} -> Written pitch: {written_pitch2}")


def main():
    """Main demo function."""
    parser = argparse.ArgumentParser(
        description='Multi-part music recognition demo',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all available instruments
  python multipart_demo.py --list-instruments

  # Show user ensemble configuration
  python multipart_demo.py --show-ensemble

  # Show transposition examples
  python multipart_demo.py --transposition

  # Process multiple part images into a score
  python multipart_demo.py --process-parts ./part_images --output score.xml

  # Process with a trained model
  python multipart_demo.py --process-parts ./part_images --output score.xml --model checkpoints/best_model.pth
        """
    )

    parser.add_argument('--list-instruments', action='store_true',
                        help='List all available instruments')
    parser.add_argument('--show-ensemble', action='store_true',
                        help='Show the user-specified ensemble configuration')
    parser.add_argument('--transposition', action='store_true',
                        help='Demonstrate transposition examples')
    parser.add_argument('--process-parts', type=str,
                        help='Directory containing part images to process')
    parser.add_argument('--output', type=str, default='output_score.xml',
                        help='Output MusicXML file path')
    parser.add_argument('--model', type=str,
                        help='Path to trained model weights')

    args = parser.parse_args()

    # Run appropriate demo
    if args.list_instruments:
        demo_list_instruments()

    elif args.show_ensemble:
        demo_create_user_ensemble()

    elif args.transposition:
        demo_transposition_example()

    elif args.process_parts:
        demo_process_parts(args.process_parts, args.output, args.model)

    else:
        # Run all demos
        print("\n" + "="*70)
        print("MULTI-PART MUSIC RECOGNITION - COMPLETE DEMO")
        print("="*70)

        demo_list_instruments()
        demo_create_user_ensemble()
        demo_transposition_example()

        print("\n" + "="*70)
        print("To process actual images, run with --process-parts flag")
        print("Example: python multipart_demo.py --process-parts ./part_images --output score.xml")
        print("="*70 + "\n")


if __name__ == '__main__':
    main()
