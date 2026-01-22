# Orchestral Score Generation Guide

Complete guide for generating orchestral and band scores with automatic part derivation.

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Instrument Library](#instrument-library)
4. [Automatic Part Generation](#automatic-part-generation)
5. [PDF Reading](#pdf-reading)
6. [Complete Workflow](#complete-workflow)
7. [Code Examples](#code-examples)
8. [Command Line Usage](#command-line-usage)

---

## Overview

This system provides comprehensive tools for creating complete orchestral and band scores from scanned handwritten music. It includes:

- **PDF Reading**: Extract music from scanned PDF scores
- **Music Recognition**: AI-powered handwritten music notation recognition
- **Multi-Part Scores**: Support for 40+ different instruments
- **Automatic Part Generation**: Generate derived parts automatically
- **Professional Export**: PDF export with table of contents

---

## Key Features

### 1. Expanded Instrument Library

**Band Instruments:**
- Flutes: C Flute, Flute 2, Flute 3, Piccolo
- Clarinets: Bb Clarinets (1st, 2nd, 3rd), Bass Clarinet, Alto Clarinet
- Saxophones: Soprano, Alto (1st, 2nd, 3rd), Tenor, Baritone
- Brass: Bb Trumpets (1st, 2nd, 3rd), F French Horns, Trombones (1st, 2nd, 3rd)
- Low Brass: Euphonium, Baritone, Tuba

**Orchestral Instruments:**
- Strings: Violin, Viola, Cello
- Woodwinds: Oboe, Bassoon

### 2. Automatic Part Generation

The system can automatically generate the following derived parts:

| Derived Part | Source | Method |
|--------------|--------|--------|
| **Flute 2** | All 2nd parts | Merge melodies from 2nd Clarinet, Trumpet, Alto Sax, Trombone |
| **Flute 3** | All 3rd parts | Merge melodies from 3rd Clarinet, Trumpet, Alto Sax, Tenor Sax |
| **Oboe** | Flute 2 | Direct copy (same part) |
| **Violin** | C Flute | Transpose 1 octave down |
| **Viola** | Flute 3 | Transpose 1 octave down (treble clef) |
| **Cello** | 1st Trombone | Direct copy |
| **Bassoon** | 2nd Trombone | Direct copy |
| **Tuba** | Baritone B.C. | Transpose 1 octave down |
| **Alto Clarinet** | 3rd Alto Sax | Direct copy (both Eb) |
| **Soprano Sax** | 1st Clarinet/Trumpet | Direct copy (both Bb) |

### 3. Octave Transposition Utilities

New utility functions for octave transposition:

```python
from music_recognition import transpose_octaves, transpose_score_octaves

# Transpose a single note
note = transpose_octaves('C4', -1)  # Returns 'C3'

# Transpose an entire score
violin_score = transpose_score_octaves(flute_score, -1)
```

### 4. PDF Reading

Extract music from scanned PDFs:

```python
from music_recognition import PDFMusicReader

reader = PDFMusicReader()
result = reader.process_pdf_score('scanned_score.pdf', 'output/extracted')

print(f"Extracted {result['total_pages']} pages")
print(f"Found {result['total_staves']} staves")
```

---

## Instrument Library

### All Available Instruments

```python
from music_recognition import BandInstruments, list_all_instruments

# List all instruments
instruments = list_all_instruments()
for name, config in instruments.items():
    print(f"{name}: {config.transposition.name}")

# Access specific instruments
flute = BandInstruments.C_FLUTE
violin = BandInstruments.VIOLIN
soprano_sax = BandInstruments.Bb_SOPRANO_SAX
```

### Transposing Instruments

The system handles transposition automatically:

| Instrument | Transposition | Written C sounds as |
|------------|---------------|---------------------|
| Bb Clarinet | Major 2nd down | Bb |
| Bb Trumpet | Major 2nd down | Bb |
| Bb Soprano Sax | Major 2nd down | Bb |
| Bb Tenor Sax | Major 2nd down (+ octave) | Bb (lower) |
| Eb Alto Sax | Major 6th down | Eb |
| Eb Alto Clarinet | Major 6th down | Eb |
| F French Horn | Perfect 5th down | F |

---

## Automatic Part Generation

### How It Works

The `PartGenerator` class analyzes multiple parts and selects the most active melody at each measure:

1. **Activity Analysis**: Counts notes vs. rests in each measure
2. **Best Selection**: Chooses the measure with the most musical activity
3. **Concert Pitch**: Converts all parts to concert pitch for comparison
4. **Intelligent Merging**: Creates coherent melodic lines

### Usage Example

```python
from music_recognition import MultiPartScore, PartGenerator, AutoScoreBuilder

# Create your original score
score = MultiPartScore(title="Concert March")

# Add parts (Flute, Clarinets, Saxes, Brass, etc.)
# ... add your parts ...

# Automatically generate all derived parts
complete_score = AutoScoreBuilder.build_complete_score(score)

# Export with all parts
complete_score.export_with_toc('complete_score.pdf')
```

### Manual Part Generation

For more control, use `PartGenerator` directly:

```python
from music_recognition import PartGenerator

generator = PartGenerator(score)

# Generate specific parts
flute_2 = generator.generate_flute_2()
flute_3 = generator.generate_flute_3()
violin = generator.copy_part_with_octave_shift('C Flute', -1)

# Get all derived parts
derived_parts = generator.generate_all_derived_parts()
```

---

## PDF Reading

### Extract Staves from PDF

```python
from music_recognition import PDFMusicReader

reader = PDFMusicReader(dpi=300)

# Convert PDF pages to images
images = reader.pdf_to_images('scanned_score.pdf')

# Extract individual staves
staves = reader.extract_staves_from_image(images[0])

# Process entire PDF
result = reader.process_pdf_score('scanned_score.pdf', 'output/extracted')
```

### Integration with Recognition

```python
from music_recognition import MusicRecognitionSystem, PDFMusicReader

# Step 1: Extract from PDF
reader = PDFMusicReader()
result = reader.process_pdf_score('scanned_score.pdf')

# Step 2: Recognize each staff
system = MusicRecognitionSystem()
recognized_parts = []

for staff_info in result['staves']:
    staff_image = staff_info['image_path']
    recognized = system.recognize_from_file(staff_image)
    recognized_parts.append(recognized['score'])
```

---

## Complete Workflow

### Full Pipeline Example

```python
from pathlib import Path
from music_recognition import (
    PDFMusicReader,
    MusicRecognitionSystem,
    MultiPartScore,
    BandInstruments,
    AutoScoreBuilder
)

# 1. Read scanned PDF
reader = PDFMusicReader()
extraction = reader.process_pdf_score('scanned_band_score.pdf')
print(f"Extracted {extraction['total_staves']} staves")

# 2. Recognize music notation
system = MusicRecognitionSystem()
score = MultiPartScore(title="Band Arrangement")

parts_config = [
    ('C Flute', BandInstruments.C_FLUTE),
    ('1st Bb Clarinet', BandInstruments.Bb_CLARINET_1),
    ('2nd Bb Clarinet', BandInstruments.Bb_CLARINET_2),
    ('3rd Bb Clarinet', BandInstruments.Bb_CLARINET_3),
    ('1st Eb Alto Sax', BandInstruments.Eb_ALTO_SAX_1),
    ('2nd Eb Alto Sax', BandInstruments.Eb_ALTO_SAX_2),
    ('3rd Eb Alto Sax', BandInstruments.Eb_ALTO_SAX_3),
    ('1st Bb Trumpet', BandInstruments.Bb_TRUMPET_1),
    ('2nd Bb Trumpet', BandInstruments.Bb_TRUMPET_2),
    ('1st C Trombone', BandInstruments.C_TROMBONE_1),
    ('2nd C Trombone', BandInstruments.C_TROMBONE_2),
    ('Baritone B.C.', BandInstruments.C_EUPHONIUM_BC),
]

for i, (part_name, instrument) in enumerate(parts_config):
    if i < len(extraction['staves']):
        staff_image = extraction['staves'][i]['image_path']
        recognized = system.recognize_from_file(staff_image)
        score.add_part(part_name, recognized['score'], instrument)

# 3. Generate all derived parts automatically
complete_score = AutoScoreBuilder.build_complete_score(score)

# 4. Export complete score with TOC
complete_score.export_with_toc('complete_orchestral_score.pdf')

print(f"Complete! Generated score with {len(complete_score.parts)} parts")
```

---

## Code Examples

### Example 1: Generate Flute 2 and Flute 3

```python
from music_recognition import MultiPartScore, PartGenerator, BandInstruments

# Create score with 2nd and 3rd parts
score = MultiPartScore(title="Band Score")

# Add parts (would come from recognition in real usage)
# ... add 2nd Clarinet, 2nd Trumpet, 2nd Alto Sax, etc. ...

# Generate derived parts
generator = PartGenerator(score)

flute_2 = generator.generate_flute_2()
flute_3 = generator.generate_flute_3()

# Add to score
score.add_part('Flute 2', flute_2, BandInstruments.C_FLUTE_2)
score.add_part('Flute 3', flute_3, BandInstruments.C_FLUTE_3)
```

### Example 2: Create String Parts

```python
from music_recognition import PartGenerator, BandInstruments

generator = PartGenerator(score)

# Violin = C Flute 1 octave down
violin = generator.copy_part_with_octave_shift('C Flute', -1)
score.add_part('Violin', violin, BandInstruments.VIOLIN)

# Viola = Flute 3 1 octave down (using treble clef)
flute_3 = generator.generate_flute_3()
from music_recognition import transpose_score_octaves
viola = transpose_score_octaves(flute_3, -1)
viola.clef = 'G'  # Treble clef
score.add_part('Viola', viola, BandInstruments.VIOLA)

# Cello = Trombone 1
cello = generator.copy_part_with_octave_shift('1st Trombone', 0)
score.add_part('Cello', cello, BandInstruments.CELLO)
```

### Example 3: Build Complete Score Automatically

```python
from music_recognition import MultiPartScore, AutoScoreBuilder

# Create your original band score
score = MultiPartScore(title="Concert March")
# ... add parts ...

# Automatically generate ALL derived parts
complete_score = AutoScoreBuilder.build_complete_score(score)

# The complete score now includes:
# - All original parts
# - Flute 2 (from 2nd parts)
# - Flute 3 (from 3rd parts)
# - Oboe (= Flute 2)
# - Violin (= Flute 1 octave down)
# - Viola (= Flute 3 1 octave down, treble clef)
# - Cello (= Trombone 1)
# - Bassoon (= Trombone 2)
# - Tuba (= Baritone 1 octave down)
# - Alto Clarinet (= 3rd Alto Sax)
# - Soprano Sax (= 1st Clarinet/Trumpet)

print(f"Generated {len(complete_score.parts)} total parts")
```

---

## Command Line Usage

### Using the Orchestral Score Generator Script

The `orchestral_score_generator.py` script provides a complete command-line interface:

```bash
# Generate example score with all derived parts
python orchestral_score_generator.py --example

# Process a scanned PDF
python orchestral_score_generator.py --input scanned_score.pdf --output complete_score.pdf

# Generate without table of contents
python orchestral_score_generator.py --example --no-toc

# Extract staves only (no recognition)
python orchestral_score_generator.py --input scanned_score.pdf --extract-only
```

### Help and Options

```bash
python orchestral_score_generator.py --help
```

Options:
- `--input <pdf>`: Path to scanned PDF music score
- `--output <pdf>`: Output PDF path (default: output/complete_orchestral_score.pdf)
- `--example`: Generate example score without PDF input
- `--no-toc`: Skip table of contents generation
- `--extract-only`: Only extract staves from PDF, do not recognize

---

## Advanced Usage

### Custom Part Merging

```python
from music_recognition import PartMerger

# Select best measure from multiple parts
measures = [part1.measures[0], part2.measures[0], part3.measures[0]]
best_measure = PartMerger.select_best_measure(measures)

# Merge entire parts by activity
parts_dict = {
    '2nd Clarinet': clarinet_2_score,
    '2nd Trumpet': trumpet_2_score,
    '2nd Alto Sax': alto_sax_2_score
}
merged_score = PartMerger.merge_parts_by_activity(parts_dict)
```

### Custom Instrument Mappings

```python
from music_recognition import InstrumentConfig, ClefType, TransposeInterval

# Define a custom instrument
custom_instrument = InstrumentConfig(
    name="Custom Instrument",
    short_name="Cust.",
    clef=ClefType.TREBLE,
    transposition=TransposeInterval.NONE,
    range_low="C3",
    range_high="C6"
)

# Use in your score
score.add_part("Custom Part", custom_score, custom_instrument)
```

---

## Requirements

### Python Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `torch` - Neural network for recognition
- `opencv-python` - Image processing
- `music21` - Music notation
- `reportlab` - PDF generation
- `pdf2image` - PDF reading
- `PyPDF2` - PDF manipulation
- `pillow` - Image handling
- `numpy` - Numerical operations

### System Dependencies

For PDF reading:
```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler

# Windows
# Download poppler from: https://github.com/oschwartz10612/poppler-windows
```

---

## Troubleshooting

### PDF Reading Issues

**Problem**: `pdf2image` fails to convert PDF
**Solution**: Install poppler-utils (see System Dependencies above)

**Problem**: Extracted images are too small/large
**Solution**: Adjust DPI setting:
```python
reader = PDFMusicReader(dpi=300)  # Default is 300
```

### Part Generation Issues

**Problem**: Flute 2/3 generation returns empty parts
**Solution**: Ensure your score has the required 2nd/3rd parts:
- For Flute 2: Need 2nd Clarinet, 2nd Trumpet, 2nd Alto Sax, or 2nd Trombone
- For Flute 3: Need 3rd Clarinet, 3rd Trumpet, 3rd Alto Sax, or Tenor Sax

**Problem**: Part names don't match
**Solution**: The system uses flexible name matching. Ensure part names contain keywords like "2nd", "3rd", "Clarinet", "Trumpet", etc.

### Export Issues

**Problem**: PDF export fails
**Solution**: Check that reportlab is installed and you have write permissions

---

## Next Steps

1. **Train the Recognition Model**: See `RECOGNITION_TRAINING.md` for details on training the CNN model
2. **Customize Instruments**: Add your own instrument configurations
3. **Extend Part Generation**: Create custom part derivation rules
4. **Batch Processing**: Process multiple scores in batch

---

## Support

For issues and questions:
- See `README.md` for general information
- See `PDF_EXPORT_GUIDE.md` for PDF export details
- Check the example scripts in the repository

---

## License

See LICENSE file for details.
