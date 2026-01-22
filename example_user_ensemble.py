"""
Example script demonstrating multi-part score assembly with user's specific instrumentation:
- C Flute
- 1st, 2nd, 3rd Bb Clarinet/Trumpet
- 1st, 2nd, 3rd Eb Alto Sax
- F French Horn
- Bb Bass Clarinet/Baritone T.C.
- Baritone B.C./Euphonium
- 1st, 2nd C Trombone
- 3rd Bb Clarinet/Trumpet/Tenor Sax
"""

from music_recognition import (
    MusicRecognitionSystem,
    ScoreAssembler,
    BandInstruments,
    MultiPartScore,
    Transposer
)


def example_1_process_handwritten_parts():
    """
    Example 1: Process handwritten parts from images and assemble into a score.
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Process Handwritten Parts")
    print("="*70)

    # Initialize the recognition system
    print("\nInitializing recognition system...")
    system = MusicRecognitionSystem(
        model_path='checkpoints/best_model.pth',  # Use trained model
        device='cuda',  # or 'cpu'
        confidence_threshold=0.6
    )

    # Create score assembler
    assembler = ScoreAssembler(recognition_system=system)

    # Define your parts - map image files to instruments
    part_images = {
        'C Flute': 'part_images/flute.jpg',
        '1st Bb Clarinet': 'part_images/clarinet1.jpg',
        '2nd Bb Clarinet': 'part_images/clarinet2.jpg',
        '3rd Bb Clarinet': 'part_images/clarinet3.jpg',
        '1st Eb Alto Sax': 'part_images/alto_sax1.jpg',
        '2nd Eb Alto Sax': 'part_images/alto_sax2.jpg',
        '3rd Eb Alto Sax': 'part_images/alto_sax3.jpg',
        'F French Horn': 'part_images/horn.jpg',
        'Bb Bass Clarinet': 'part_images/bass_clarinet.jpg',
        'Bb Baritone T.C.': 'part_images/baritone_tc.jpg',
        'Euphonium B.C.': 'part_images/euphonium.jpg',
        '1st Trombone': 'part_images/trombone1.jpg',
        '2nd Trombone': 'part_images/trombone2.jpg',
        'Bb Tenor Sax': 'part_images/tenor_sax.jpg',
    }

    # Map parts to instrument configurations
    instruments = {
        'C Flute': BandInstruments.C_FLUTE,
        '1st Bb Clarinet': BandInstruments.Bb_CLARINET_1,
        '2nd Bb Clarinet': BandInstruments.Bb_CLARINET_2,
        '3rd Bb Clarinet': BandInstruments.Bb_CLARINET_3,
        '1st Eb Alto Sax': BandInstruments.Eb_ALTO_SAX_1,
        '2nd Eb Alto Sax': BandInstruments.Eb_ALTO_SAX_2,
        '3rd Eb Alto Sax': BandInstruments.Eb_ALTO_SAX_3,
        'F French Horn': BandInstruments.F_FRENCH_HORN_1,
        'Bb Bass Clarinet': BandInstruments.Bb_BASS_CLARINET,
        'Bb Baritone T.C.': BandInstruments.Bb_BARITONE_TC,
        'Euphonium B.C.': BandInstruments.C_EUPHONIUM_BC,
        '1st Trombone': BandInstruments.C_TROMBONE_1,
        '2nd Trombone': BandInstruments.C_TROMBONE_2,
        'Bb Tenor Sax': BandInstruments.Bb_TENOR_SAX,
    }

    print(f"\nProcessing {len(part_images)} parts...")

    # Process and assemble the score
    try:
        score = assembler.create_score_from_parts(
            part_images=part_images,
            instruments=instruments,
            title="Band Arrangement",
            composer="Your Name"
        )

        print("\n✓ Score assembled successfully!")

        # Export full score (transposed parts as written)
        print("\nExporting full score (transposed)...")
        score.export_musicxml('output/band_score_transposed.xml')

        # Export concert pitch version (for conductor)
        print("Exporting concert pitch score...")
        score.export_musicxml('output/band_score_concert.xml', concert_pitch=True)

        # Export individual parts
        print("Exporting individual parts...")
        score.export_parts_separately('output/parts/', format='musicxml')

        print("\n✓ All files exported to output/ directory!")

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have part images in the 'part_images/' directory")
        print("Expected files: flute.jpg, clarinet1.jpg, alto_sax1.jpg, etc.")


def example_2_create_empty_score():
    """
    Example 2: Create an empty multi-part score template for your ensemble.
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Create Empty Score Template")
    print("="*70)

    from music_recognition.postprocessing import MusicScore

    # Create the multi-part score
    score = MultiPartScore(
        title="New Band Piece",
        composer="Composer Name"
    )

    # Define all parts in score order (high to low)
    parts_list = [
        ('C Flute', BandInstruments.C_FLUTE),
        ('1st Bb Clarinet', BandInstruments.Bb_CLARINET_1),
        ('2nd Bb Clarinet', BandInstruments.Bb_CLARINET_2),
        ('3rd Bb Clarinet', BandInstruments.Bb_CLARINET_3),
        ('1st Eb Alto Sax', BandInstruments.Eb_ALTO_SAX_1),
        ('2nd Eb Alto Sax', BandInstruments.Eb_ALTO_SAX_2),
        ('3rd Eb Alto Sax', BandInstruments.Eb_ALTO_SAX_3),
        ('F French Horn', BandInstruments.F_FRENCH_HORN_1),
        ('Bb Bass Clarinet', BandInstruments.Bb_BASS_CLARINET),
        ('Bb Baritone T.C.', BandInstruments.Bb_BARITONE_TC),
        ('Euphonium B.C.', BandInstruments.C_EUPHONIUM_BC),
        ('1st Trombone', BandInstruments.C_TROMBONE_1),
        ('2nd Trombone', BandInstruments.C_TROMBONE_2),
        ('Bb Tenor Sax', BandInstruments.Bb_TENOR_SAX),
    ]

    print(f"\nCreating score with {len(parts_list)} parts:\n")

    # Add each part with empty measures
    for part_name, instrument in parts_list:
        # Create empty score for this part
        part_score = MusicScore()
        part_score.clef = instrument.clef.value
        part_score.time_signature = (4, 4)
        part_score.tempo = 120

        # Add to multi-part score
        score.add_part(part_name, part_score, instrument)

        # Show info
        trans_info = "Concert pitch" if instrument.transposition.name == "NONE" else f"Transposing ({instrument.transposition.name})"
        print(f"  ✓ {part_name:25} - {trans_info:30} - {instrument.clef.value} clef")

    # Export empty template
    print("\nExporting empty score template...")
    score.export_musicxml('output/empty_score_template.xml')

    print("✓ Empty template exported to output/empty_score_template.xml")
    print("  You can now edit this in your music notation software!")


def example_3_transposition_demo():
    """
    Example 3: Demonstrate transposition for your instruments.
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Transposition Examples")
    print("="*70)

    # Concert pitch note to transpose
    concert_note = "C4"

    print(f"\nConcert pitch: {concert_note}")
    print("\nWhat each instrument writes to play concert C4:\n")

    # Your instruments and their transpositions
    instruments = [
        ('C Flute', BandInstruments.C_FLUTE),
        ('Bb Clarinet', BandInstruments.Bb_CLARINET_1),
        ('Eb Alto Sax', BandInstruments.Eb_ALTO_SAX_1),
        ('F French Horn', BandInstruments.F_FRENCH_HORN_1),
        ('Bb Bass Clarinet', BandInstruments.Bb_BASS_CLARINET),
        ('Bb Baritone T.C.', BandInstruments.Bb_BARITONE_TC),
        ('Euphonium B.C.', BandInstruments.C_EUPHONIUM_BC),
        ('Trombone', BandInstruments.C_TROMBONE_1),
        ('Bb Tenor Sax', BandInstruments.Bb_TENOR_SAX),
    ]

    for name, instrument in instruments:
        transposer = Transposer(instrument)
        written_note = transposer.concert_to_written(concert_note)

        trans_type = "non-transposing" if instrument.transposition.name == "NONE" else "transposing"
        print(f"  {name:25} writes: {written_note:5} ({trans_type})")

    # Reverse example
    print("\n" + "-"*70)
    written_note = "C5"
    print(f"\nWhen written {written_note} is played, the concert pitch sounds:\n")

    for name, instrument in instruments:
        transposer = Transposer(instrument)
        sounding_note = transposer.written_to_concert(written_note)
        print(f"  {name:25} sounds: {sounding_note}")


def example_4_show_instrument_details():
    """
    Example 4: Show detailed information about your instruments.
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Your Ensemble Instrument Details")
    print("="*70)

    instruments = [
        BandInstruments.C_FLUTE,
        BandInstruments.Bb_CLARINET_1,
        BandInstruments.Bb_CLARINET_2,
        BandInstruments.Bb_CLARINET_3,
        BandInstruments.Eb_ALTO_SAX_1,
        BandInstruments.Eb_ALTO_SAX_2,
        BandInstruments.Eb_ALTO_SAX_3,
        BandInstruments.F_FRENCH_HORN_1,
        BandInstruments.Bb_BASS_CLARINET,
        BandInstruments.Bb_BARITONE_TC,
        BandInstruments.C_EUPHONIUM_BC,
        BandInstruments.C_TROMBONE_1,
        BandInstruments.C_TROMBONE_2,
        BandInstruments.Bb_TENOR_SAX,
    ]

    print("\nInstrument configurations:\n")

    for inst in instruments:
        print(f"• {inst.name}")
        print(f"  Short name:     {inst.short_name}")
        print(f"  Clef:           {inst.clef.value}")
        print(f"  Transposition:  {inst.transposition.name}")
        print(f"  Range:          {inst.range_low} - {inst.range_high}")
        print()


def main():
    """Run all examples."""
    import sys

    print("\n" + "="*70)
    print("USER ENSEMBLE EXAMPLES")
    print("Your instrumentation: Flute, 3 Clarinets, 3 Alto Saxes, Horn,")
    print("Bass Clarinet, Baritone, Euphonium, 2 Trombones, Tenor Sax")
    print("="*70)

    if len(sys.argv) > 1:
        example = sys.argv[1]

        if example == '1':
            example_1_process_handwritten_parts()
        elif example == '2':
            example_2_create_empty_score()
        elif example == '3':
            example_3_transposition_demo()
        elif example == '4':
            example_4_show_instrument_details()
        else:
            print(f"Unknown example: {example}")
            print("Usage: python example_user_ensemble.py [1|2|3|4]")
    else:
        # Run examples that don't require image files
        example_2_create_empty_score()
        example_3_transposition_demo()
        example_4_show_instrument_details()

        print("\n" + "="*70)
        print("To process handwritten parts:")
        print("  python example_user_ensemble.py 1")
        print("\nMake sure you have images in 'part_images/' directory first!")
        print("="*70 + "\n")


if __name__ == '__main__':
    main()
