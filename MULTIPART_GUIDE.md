# Multi-Part Score Guide

Complete guide for creating, processing, and exporting multi-part orchestral and band arrangements.

## Table of Contents

1. [Overview](#overview)
2. [Supported Instruments](#supported-instruments)
3. [Quick Start](#quick-start)
4. [Creating Multi-Part Scores](#creating-multi-part-scores)
5. [Processing Part Images](#processing-part-images)
6. [Transposition](#transposition)
7. [Export Formats](#export-formats)
8. [Advanced Usage](#advanced-usage)
9. [Examples](#examples)

## Overview

The multi-part system allows you to:
- Process individual instrument parts from handwritten scores
- Automatically handle transpositions (Bb, Eb, F instruments)
- Assemble complete band/orchestral scores
- Export to MusicXML with proper part layout
- Generate both transposed and concert pitch versions
- Export individual parts separately

## Supported Instruments

### Your Custom Ensemble

The system supports your specific instrumentation:

```python
from music_recognition import BandInstruments

# Flutes
BandInstruments.C_FLUTE

# Bb Clarinets/Trumpets
BandInstruments.Bb_CLARINET_1  # or Bb_TRUMPET_1
BandInstruments.Bb_CLARINET_2  # or Bb_TRUMPET_2
BandInstruments.Bb_CLARINET_3  # or Bb_TRUMPET_3

# Eb Alto Saxophones
BandInstruments.Eb_ALTO_SAX_1
BandInstruments.Eb_ALTO_SAX_2
BandInstruments.Eb_ALTO_SAX_3

# F French Horn
BandInstruments.F_FRENCH_HORN_1

# Bb Bass Clarinet/Baritone T.C.
BandInstruments.Bb_BASS_CLARINET  # or Bb_BARITONE_TC

# Euphonium/Baritone B.C.
BandInstruments.C_EUPHONIUM_BC

# C Trombones
BandInstruments.C_TROMBONE_1
BandInstruments.C_TROMBONE_2

# Bb Tenor Sax (listed as alternative for 3rd part)
BandInstruments.Bb_TENOR_SAX
```

### All Available Instruments

View all instruments:
```bash
python multipart_demo.py --list-instruments
```

Or in Python:
```python
from music_recognition import list_all_instruments

instruments = list_all_instruments()
for name, config in instruments.items():
    print(f"{name}: {config.short_name}, {config.clef.value} clef")
```

## Quick Start

### 1. List Instruments

```bash
python multipart_demo.py --list-instruments
```

### 2. Show Your Ensemble Configuration

```bash
python multipart_demo.py --show-ensemble
```

### 3. Process Multiple Parts

```bash
# Process part images and create a score
python multipart_demo.py --process-parts ./part_images --output my_score.xml
```

### 4. View Transposition Examples

```bash
python multipart_demo.py --transposition
```

## Creating Multi-Part Scores

### Method 1: From Individual Part Images

```python
from music_recognition import (
    MusicRecognitionSystem,
    ScoreAssembler,
    BandInstruments
)

# Initialize recognition system
system = MusicRecognitionSystem(model_path='checkpoints/best_model.pth')
assembler = ScoreAssembler(recognition_system=system)

# Define your parts and their images
part_images = {
    'C Flute': 'images/flute.jpg',
    '1st Bb Clarinet': 'images/clarinet1.jpg',
    '2nd Bb Clarinet': 'images/clarinet2.jpg',
    '1st Eb Alto Sax': 'images/alto_sax1.jpg',
    'F French Horn': 'images/horn.jpg',
    'Euphonium': 'images/euphonium.jpg',
    '1st Trombone': 'images/trombone1.jpg',
}

# Map parts to instruments
instruments = {
    'C Flute': BandInstruments.C_FLUTE,
    '1st Bb Clarinet': BandInstruments.Bb_CLARINET_1,
    '2nd Bb Clarinet': BandInstruments.Bb_CLARINET_2,
    '1st Eb Alto Sax': BandInstruments.Eb_ALTO_SAX_1,
    'F French Horn': BandInstruments.F_FRENCH_HORN_1,
    'Euphonium': BandInstruments.C_EUPHONIUM_BC,
    '1st Trombone': BandInstruments.C_TROMBONE_1,
}

# Process and assemble
score = assembler.create_score_from_parts(
    part_images=part_images,
    instruments=instruments,
    title="My Band Piece",
    composer="Composer Name"
)

# Export
score.export_musicxml('output.xml')
```

### Method 2: Manually Construct Score

```python
from music_recognition import MultiPartScore, BandInstruments
from music_recognition.postprocessing import MusicScore

# Create multi-part score
score = MultiPartScore(title="My Piece", composer="John Doe")

# Create individual parts
flute_part = MusicScore()
flute_part.measures = [
    # Add measure data...
]

# Add to score
score.add_part('C Flute', flute_part, BandInstruments.C_FLUTE)

# Export
score.export_musicxml('output.xml')
```

### Method 3: Pre-configured Ensemble

```python
from music_recognition import ScoreAssembler

# Create empty score for standard ensemble
score = ScoreAssembler.create_standard_ensemble_score(
    ensemble_type="concert_band",  # or "brass_ensemble", etc.
    title="Concert March",
    composer="Composer"
)

# Now populate with recognized music or manual entry
```

## Processing Part Images

### File Naming Convention

Organize your part images with clear names:

```
part_images/
├── flute.jpg
├── clarinet1.jpg
├── clarinet2.jpg
├── clarinet3.jpg
├── alto_sax1.jpg
├── alto_sax2.jpg
├── alto_sax3.jpg
├── horn.jpg
├── bass_clarinet.jpg
├── baritone.jpg
├── euphonium.jpg
├── trombone1.jpg
├── trombone2.jpg
└── tenor_sax.jpg
```

### Process Multiple Parts

```bash
python multipart_demo.py \
    --process-parts ./part_images \
    --output my_score.xml \
    --model checkpoints/best_model.pth
```

This will:
1. Recognize all parts from images
2. Create a complete score with proper transpositions
3. Export to MusicXML (`my_score.xml`)
4. Export concert pitch version (`my_score_concert.xml`)
5. Export individual parts to `parts/` directory

## Transposition

### Understanding Transposition

Different instruments transpose differently:

- **Bb instruments** (Clarinet, Trumpet, Tenor Sax): Written C sounds Bb (down major 2nd)
- **Eb instruments** (Alto Sax): Written C sounds Eb (down major 6th)
- **F instruments** (French Horn): Written C sounds F (down perfect 5th)
- **C instruments** (Flute, Trombone): No transposition (concert pitch)

### Transposition Examples

```python
from music_recognition import Transposer, BandInstruments

# Bb Clarinet
clarinet_transposer = Transposer(BandInstruments.Bb_CLARINET_1)

# Written C sounds as Bb (concert pitch)
concert = clarinet_transposer.written_to_concert("C5")  # Returns "Bb4"

# To write concert C, clarinet must play D
written = clarinet_transposer.concert_to_written("C4")  # Returns "D4"

# Eb Alto Sax
sax_transposer = Transposer(BandInstruments.Eb_ALTO_SAX_1)

# Written C sounds as Eb (concert pitch)
concert = sax_transposer.written_to_concert("C5")  # Returns "Eb4"

# F Horn
horn_transposer = Transposer(BandInstruments.F_FRENCH_HORN_1)

# Written C sounds as F (concert pitch)
concert = horn_transposer.written_to_concert("C5")  # Returns "F4"
```

### Convert Entire Score to Concert Pitch

```python
# Create transposed parts score
score = assembler.create_score_from_parts(...)

# Convert to concert pitch
concert_score = score.to_concert_pitch()

# Export concert version
concert_score.export_musicxml('concert_score.xml')
```

### Transpose Individual Notes

```python
from music_recognition import Note

# Create a note
note = Note.from_string("C4")

# Transpose by semitones
note_up = note.transpose_semitones(2)  # D4
note_down = note.transpose_semitones(-2)  # Bb3

# Convert to MIDI
midi_num = note.to_midi_number()  # 60 (middle C)
```

## Export Formats

### MusicXML (Full Score)

```python
# Standard export (transposed parts)
score.export_musicxml('score.xml')

# Concert pitch export
score.export_musicxml('score_concert.xml', concert_pitch=True)
```

### MusicXML (Individual Parts)

```python
# Export each part as a separate file
score.export_parts_separately(
    output_dir='parts/',
    format='musicxml'
)
```

### MIDI (Individual Parts)

```python
# Export parts as MIDI files
score.export_parts_separately(
    output_dir='midi_parts/',
    format='midi'
)
```

### ABC Notation (Individual Parts)

```python
# Export parts as ABC notation
score.export_parts_separately(
    output_dir='abc_parts/',
    format='abc'
)
```

## Advanced Usage

### Custom Part Order

```python
# Reorder parts in the score
score.reorder_parts([
    'C Flute',
    '1st Bb Clarinet',
    '2nd Bb Clarinet',
    'F French Horn',
    '1st Trombone'
])
```

### Add/Remove Parts

```python
# Remove a part
score.remove_part('3rd Bb Clarinet')

# Add a new part
from music_recognition.postprocessing import MusicScore

new_part = MusicScore()
# ... populate new_part ...

score.add_part('Bb Tenor Sax', new_part, BandInstruments.Bb_TENOR_SAX)
```

### Access Part Data

```python
# Get number of measures
num_measures = score.get_num_measures()

# Access individual parts
flute_score = score.parts['C Flute']
print(f"Flute has {len(flute_score.measures)} measures")

# Convert to dictionary
score_dict = score.to_dict()
```

### Create Custom Instrument

```python
from music_recognition.instruments import InstrumentConfig, ClefType, TransposeInterval

# Define custom instrument
custom_instrument = InstrumentConfig(
    name="Custom Bb Instrument",
    short_name="Cust.",
    clef=ClefType.TREBLE,
    transposition=TransposeInterval.Bb_DOWN,
    range_low="C3",
    range_high="C6"
)

# Use in score
score.add_part('Custom', part_score, custom_instrument)
```

## Examples

### Example 1: Process Your Band Parts

```python
"""
Process a complete band arrangement with all your specified parts.
"""
from music_recognition import (
    MusicRecognitionSystem,
    ScoreAssembler,
    BandInstruments
)

# Initialize
system = MusicRecognitionSystem(model_path='checkpoints/best_model.pth')
assembler = ScoreAssembler(recognition_system=system)

# Define all your parts
part_images = {
    'C Flute': 'parts/flute.jpg',
    '1st Bb Clarinet': 'parts/clarinet1.jpg',
    '2nd Bb Clarinet': 'parts/clarinet2.jpg',
    '3rd Bb Clarinet': 'parts/clarinet3.jpg',
    '1st Eb Alto Sax': 'parts/alto_sax1.jpg',
    '2nd Eb Alto Sax': 'parts/alto_sax2.jpg',
    '3rd Eb Alto Sax': 'parts/alto_sax3.jpg',
    'F French Horn': 'parts/horn.jpg',
    'Bb Bass Clarinet': 'parts/bass_clarinet.jpg',
    'Bb Baritone T.C.': 'parts/baritone.jpg',
    'Euphonium B.C.': 'parts/euphonium.jpg',
    '1st Trombone': 'parts/trombone1.jpg',
    '2nd Trombone': 'parts/trombone2.jpg',
    'Bb Tenor Sax': 'parts/tenor_sax.jpg',
}

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

# Process
score = assembler.create_score_from_parts(
    part_images=part_images,
    instruments=instruments,
    title="Band Arrangement",
    composer="Your Name"
)

# Export transposed version (as written for each instrument)
score.export_musicxml('band_score_transposed.xml')

# Export concert pitch version (for conductor/analysis)
score.export_musicxml('band_score_concert.xml', concert_pitch=True)

# Export individual parts
score.export_parts_separately('individual_parts/', format='musicxml')
score.export_parts_separately('midi_parts/', format='midi')
```

### Example 2: Transpose a Melody for All Instruments

```python
"""
Take a melody in concert pitch and create parts for all instruments.
"""
from music_recognition import ScoreTransposer, BandInstruments
from music_recognition.postprocessing import MusicScore

# Create concert pitch melody
concert_melody = MusicScore()
concert_melody.measures = [
    [
        {'type': 'note', 'pitch': 'C4', 'duration': 1.0},
        {'type': 'note', 'pitch': 'D4', 'duration': 1.0},
        {'type': 'note', 'pitch': 'E4', 'duration': 1.0},
        {'type': 'note', 'pitch': 'F4', 'duration': 1.0},
    ]
]

# Create parts for all instruments
instruments = [
    BandInstruments.C_FLUTE,
    BandInstruments.Bb_CLARINET_1,
    BandInstruments.Eb_ALTO_SAX_1,
    BandInstruments.F_FRENCH_HORN_1,
]

transposed_parts = ScoreTransposer.concert_to_transposed_parts(
    concert_melody,
    instruments
)

# Check transpositions
for inst_name, part_score in transposed_parts.items():
    print(f"\n{inst_name}:")
    print(f"  First note: {part_score.measures[0][0]['pitch']}")
```

### Example 3: Working with Mixed Ensembles

```python
"""
Create a score with both concert pitch and transposing instruments.
"""
from music_recognition import MultiPartScore, BandInstruments
from music_recognition.postprocessing import MusicScore

score = MultiPartScore(title="Mixed Ensemble", composer="Composer")

# Concert pitch instruments
for instrument in [BandInstruments.C_FLUTE, BandInstruments.C_TROMBONE_1]:
    part = MusicScore()
    part.clef = instrument.clef.value
    # ... populate part ...
    score.add_part(instrument.name, part, instrument)

# Transposing instruments
for instrument in [BandInstruments.Bb_CLARINET_1, BandInstruments.Eb_ALTO_SAX_1]:
    part = MusicScore()
    part.clef = instrument.clef.value
    # ... populate part ...
    score.add_part(instrument.name, part, instrument)

# Export - transpositions handled automatically
score.export_musicxml('mixed_ensemble.xml')
```

## Command Line Usage

### Basic Commands

```bash
# View all instruments
python multipart_demo.py --list-instruments

# Show your ensemble configuration
python multipart_demo.py --show-ensemble

# Learn about transpositions
python multipart_demo.py --transposition

# Process parts
python multipart_demo.py --process-parts ./parts --output score.xml

# With custom model
python multipart_demo.py --process-parts ./parts --output score.xml --model model.pth
```

## Tips and Best Practices

1. **Image Quality**: Ensure part images are clear and well-lit
2. **Consistent Formatting**: Keep all parts in the same key/time signature
3. **File Organization**: Use clear, consistent filenames for parts
4. **Concert Pitch**: Always keep a concert pitch version for analysis
5. **Part Layout**: Order parts from high to low (standard score order)
6. **Transposition Check**: Verify transpositions sound correct
7. **Individual Parts**: Export individual parts for performers
8. **Backup**: Keep original images and intermediate files

## Troubleshooting

### Parts Not Aligning

- Ensure all parts have the same number of measures
- Check time signatures match across parts
- Verify barlines are detected correctly

### Transposition Issues

- Confirm correct instrument selection
- Check that written pitches are correct before transposing
- Use concert pitch export to verify

### Missing Parts

- Check file naming matches expected patterns
- Verify image files are readable
- Ensure all instruments are defined in mapping

## Next Steps

- Process your band arrangements
- Experiment with different ensembles
- Create custom instrument configurations
- Build a complete score library
- Integrate with notation software

For more information, see:
- `README.md` - General overview
- `USAGE_GUIDE.md` - Single-part usage
- `multipart_demo.py` - Example code
