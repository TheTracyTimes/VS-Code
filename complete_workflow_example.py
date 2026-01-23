"""
Complete Workflow Example: From Scanned PDFs to Individual Song Scores

This script demonstrates the complete workflow:
1. Scan 12 physical books (combined parts)
2. Digitize all music notation
3. Generate 10 derived parts automatically
4. Split combined parts into individual books (22-27 total instruments)
5. Extract individual songs
6. Create separate full scores for each song
7. Create individual part books for each song

OUTPUT STRUCTURE:
    output/
        individual_books/           # All instruments, all songs
            Trombone_1.pdf
            Flute_2.pdf
            Violin.pdf
            ...
        songs/
            parts/                  # Individual parts per song
                March_No_1/
                    Trombone_1.pdf
                    Flute_2.pdf
                    ...
                Beautiful_Waltz/
                    Trombone_1.pdf
                    ...
            scores/                 # Full scores per song
                March_No_1_Score.pdf
                Beautiful_Waltz_Score.pdf
                Grand_Finale_Score.pdf
"""

from music_recognition import (
    PDFMusicReader,
    MusicRecognitionSystem,
    MultiPartScore,
    BandInstruments,
    AutoScoreBuilder,
    create_individual_books_from_score,
    extract_songs_and_create_scores
)
from pathlib import Path


def main():
    """Complete workflow from scanning to individual song scores."""

    print("="*70)
    print("COMPLETE MUSIC BOOK GENERATION WORKFLOW")
    print("="*70)

    # ========================================================================
    # STEP 1: Define your 12 physical books
    # ========================================================================
    print("\nSTEP 1: Processing 12 Physical Books")
    print("-" * 70)

    physical_books = [
        ('Trombone 1', BandInstruments.C_TROMBONE_1),
        ('Trombone 2', BandInstruments.C_TROMBONE_2),
        ('F French Horn', BandInstruments.F_FRENCH_HORN_1),
        ('Eb Alto Sax 1', BandInstruments.Eb_ALTO_SAX_1),
        ('Eb Alto Sax 2', BandInstruments.Eb_ALTO_SAX_2),
        ('Eb Alto Sax 3', BandInstruments.Eb_ALTO_SAX_3),
        # Combined parts:
        ('Bb Tenor Sax', BandInstruments.Bb_TENOR_SAX),  # Also has 3rd Clarinet/Trumpet
        ('Bb Clarinet 1', BandInstruments.Bb_CLARINET_1),  # Also has 1st Trumpet, Soprano Sax
        ('Bb Clarinet 2', BandInstruments.Bb_CLARINET_2),  # Also has 2nd Trumpet
        ('Baritone B.C.', BandInstruments.C_EUPHONIUM_BC),
        ('Baritone T.C.', BandInstruments.Bb_BARITONE_TC),  # Also has Bass Clarinet
        ('C Flute 1', BandInstruments.C_FLUTE),
    ]

    # ========================================================================
    # STEP 2: Scan and digitize (simulated here with placeholder)
    # ========================================================================
    print("\nSTEP 2: Scanning and Digitizing")
    print("-" * 70)
    print("In real usage, you would:")
    print("  1. Scan each physical book to PDF")
    print("  2. Use PDFMusicReader to extract staff images")
    print("  3. Use MusicRecognitionSystem to recognize notation")
    print("\nFor this example, we'll create a placeholder score...")

    # Create placeholder multipart score
    score = MultiPartScore(title="Band Collection", composer="Various")

    # In real usage, you would do:
    # reader = PDFMusicReader()
    # system = MusicRecognitionSystem()
    # for book_name, instrument in physical_books:
    #     pdf_file = f"scanned/{book_name}.pdf"
    #     extraction = reader.process_pdf_score(pdf_file)
    #     for staff_info in extraction['staves']:
    #         recognized = system.recognize_from_file(staff_info['image_path'])
    #         score.add_part(book_name, recognized['score'], instrument)

    print("✓ All 12 books digitized")

    # ========================================================================
    # STEP 3: Generate derived parts automatically
    # ========================================================================
    print("\nSTEP 3: Generating Derived Parts")
    print("-" * 70)

    complete_score = AutoScoreBuilder.build_complete_score(score)

    print("✓ Generated parts:")
    print("  • Flute 2 (from 2nd parts, adjusted to flute range)")
    print("  • Flute 3 (from 3rd parts, adjusted to flute range)")
    print("  • Oboe (= Flute 2)")
    print("  • Violin (= Flute 1 octave down)")
    print("  • Viola (= Flute 3 octave down, treble clef)")
    print("  • Cello (= Trombone 1)")
    print("  • Bassoon (= Trombone 2)")
    print("  • Tuba (= Baritone B.C. octave down)")
    print("  • Alto Clarinet (= 3rd Alto Sax)")
    print("  • Eb Baritone Sax (from low brass, adjusted to bari range)")

    # ========================================================================
    # STEP 4: Create individual books for each instrument
    # ========================================================================
    print("\nSTEP 4: Creating Individual Part Books")
    print("-" * 70)

    individual_books = create_individual_books_from_score(
        complete_score,
        'output/individual_books'
    )

    print(f"\n✓ Created {len(individual_books)} individual part books")
    print("  Each book contains ALL songs for that instrument")

    # ========================================================================
    # STEP 5: Define song boundaries
    # ========================================================================
    print("\nSTEP 5: Defining Song Boundaries")
    print("-" * 70)

    # Define where each song starts and ends (measure numbers)
    songs = [
        {
            'title': 'March No. 1',
            'start_measure': 0,
            'end_measure': 32
        },
        {
            'title': 'Beautiful Waltz',
            'start_measure': 33,
            'end_measure': 64
        },
        {
            'title': 'Grand Finale',
            'start_measure': 65,
            'end_measure': 96
        }
    ]

    print(f"✓ Defined {len(songs)} songs:")
    for song in songs:
        print(f"  • {song['title']} (measures {song['start_measure']}-{song['end_measure']})")

    # ========================================================================
    # STEP 6: Extract songs and create individual scores
    # ========================================================================
    print("\nSTEP 6: Creating Individual Song Scores")
    print("-" * 70)

    song_results = extract_songs_and_create_scores(
        complete_score,
        songs,
        output_base_dir='output/songs'
    )

    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    print("\n" + "="*70)
    print("COMPLETE!")
    print("="*70)

    print("\nYou now have:")
    print(f"\n1. INDIVIDUAL PART BOOKS (all songs): {len(individual_books)} books")
    print("   Location: output/individual_books/")
    print("   Each musician gets ONE book with ALL songs")

    print(f"\n2. SONG SCORES (all parts): {len(songs)} scores")
    print("   Location: output/songs/scores/")
    print("   Each song has a full conductor score with ALL instruments")

    print(f"\n3. INDIVIDUAL PARTS PER SONG: {len(songs)} song folders")
    print("   Location: output/songs/parts/")
    print("   For each song, each musician has their own part")

    print("\nExample file structure:")
    print("""
    output/
        individual_books/           (22-27 books, each with all songs)
            Trombone_1.pdf
            Trombone_2.pdf
            Flute_2.pdf             (generated)
            Violin.pdf              (generated)
            Eb_Baritone_Sax.pdf     (generated)
            ...

        songs/
            parts/                  (individual parts per song)
                March_No_1/
                    Trombone_1.pdf  (just March No. 1)
                    Flute_2.pdf
                    Violin.pdf
                    ...
                Beautiful_Waltz/
                    Trombone_1.pdf  (just Beautiful Waltz)
                    Flute_2.pdf
                    ...
                Grand_Finale/
                    Trombone_1.pdf  (just Grand Finale)
                    ...

            scores/                 (full conductor scores)
                March_No_1_Score.pdf        (all instruments)
                Beautiful_Waltz_Score.pdf   (all instruments)
                Grand_Finale_Score.pdf      (all instruments)
    """)

    print("="*70)
    print("\nWorkflow complete! Ready for rehearsal and performance!")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
