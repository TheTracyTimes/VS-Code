## PDF Export Guide

Complete guide for exporting music scores to PDF format with professional-looking staff paper.

## Table of Contents

1. [Overview](#overview)
2. [Export Methods](#export-methods)
3. [Blank Staff Paper](#blank-staff-paper)
4. [Score Templates](#score-templates)
5. [Exporting Recognized Scores](#exporting-recognized-scores)
6. [Multi-Part Scores](#multi-part-scores)
7. [Titles and Text](#titles-and-text)
8. [Table of Contents](#table-of-contents-1)
9. [Advanced Customization](#advanced-customization)
10. [Backend Configuration](#backend-configuration)

## Overview

The system provides comprehensive PDF export capabilities:

- **Blank Staff Paper**: 12 staves per page on US Letter size
- **Score Templates**: Pre-configured templates with clefs and time signatures
- **Recognized Scores**: Export AI-recognized music notation
- **Multi-Part Scores**: Export complete band/orchestral arrangements
- **Multiple Backends**: music21, verovio, or reportlab

### Page Specifications

- **Page Size**: US Letter (8.5" × 11")
- **Staves per Page**: 12 (configurable)
- **Staff Line Spacing**: 0.15" (standard)
- **Margins**: 0.75" on all sides

## Export Methods

### Method 1: music21 (Recommended)

Best for professional music notation rendering.

```bash
# Install
pip install music21

# Configure (first time)
python -c "import music21; music21.configure.run()"
```

### Method 2: Verovio

Web-based rendering engine for high-quality output.

```bash
# Install from https://www.verovio.org/
# Or use system package manager
```

### Method 3: reportlab (Always Available)

Basic PDF generation with staff lines, always included.

```python
# Already installed with the system
import reportlab
```

### Check Available Backends

```python
from music_recognition import check_pdf_backends

check_pdf_backends()
```

Or command line:

```bash
python pdf_examples.py --check-backends
```

## Blank Staff Paper

### Create Basic Blank Paper

```python
from music_recognition import create_blank_sheet

# Create 5 pages of blank staff paper
create_blank_sheet(
    output_path='blank_paper.pdf',
    num_pages=5
)
```

### With Measures

```python
from music_recognition import StaffPaperGenerator

generator = StaffPaperGenerator(staves_per_page=12)

generator.create_blank_staff_paper(
    output_path='staff_paper.pdf',
    num_pages=3,
    title="Music Manuscript Paper",
    include_measures=True,
    measures_per_staff=4
)
```

### Custom Configuration

```python
# Different number of staves
generator = StaffPaperGenerator(staves_per_page=10)

# Custom title
generator.create_blank_staff_paper(
    output_path='custom_paper.pdf',
    num_pages=1,
    title="My Music Paper"
)
```

## Score Templates

### Single Instrument Template

```python
from music_recognition import create_instrument_part

# Create a clarinet part template
create_instrument_part(
    output_path='clarinet_part.pdf',
    instrument_name='Bb Clarinet',
    clef='treble',
    time_signature=(4, 4),
    num_pages=3
)
```

### Multiple Instruments

```python
from music_recognition import StaffPaperGenerator

generator = StaffPaperGenerator(staves_per_page=12)

# Create templates for different instruments
instruments = [
    ('Bb Clarinet', 'treble', (4, 4)),
    ('Eb Alto Saxophone', 'treble', (3, 4)),
    ('Trombone', 'bass', (4, 4)),
    ('Euphonium', 'bass', (6, 8)),
]

for name, clef, time_sig in instruments:
    filename = name.replace(' ', '_').lower()
    generator.create_score_template(
        output_path=f'{filename}_template.pdf',
        instrument_name=name,
        clef=clef,
        time_signature=time_sig,
        num_pages=5,
        measures_per_staff=4
    )
```

### Score Template with Custom Settings

```python
generator = StaffPaperGenerator(staves_per_page=12)

generator.create_score_template(
    output_path='my_score.pdf',
    instrument_name='C Flute',
    clef='treble',
    time_signature=(3, 4),  # 3/4 time
    num_pages=10,
    measures_per_staff=6     # 6 measures per staff
)
```

## Exporting Recognized Scores

### Single Part Score

```python
from music_recognition import MusicRecognitionSystem

# Initialize system
system = MusicRecognitionSystem(
    model_path='checkpoints/best_model.pth'
)

# Recognize music
score = system.recognize('handwritten_music.jpg')

# Export to PDF
system.export_score(score, 'output.pdf', format='pdf')

# Or use the notation converter directly
from music_recognition.postprocessing import NotationConverter

converter = NotationConverter()
converter.current_score = score
converter.export_pdf(
    'output.pdf',
    method='auto',  # Try best method available
    title="My Music",
    composer="John Doe"
)
```

### Choose Export Method

```python
# Try specific method
converter.export_pdf('output.pdf', method='music21')  # Best quality

# Or
converter.export_pdf('output.pdf', method='verovio')  # Alternative

# Or
converter.export_pdf('output.pdf', method='basic')    # Always works
```

## Multi-Part Scores

### Export Full Score

```python
from music_recognition import MultiPartScore, ScoreAssembler, BandInstruments

# Create or load multi-part score
score = MultiPartScore(title="Band Piece", composer="Composer")

# ... add parts ...

# Export to PDF
score.export_pdf(
    'band_score.pdf',
    method='auto',
    concert_pitch=False  # Use transposed parts
)

# Export concert pitch version
score.export_pdf(
    'concert_score.pdf',
    method='auto',
    concert_pitch=True
)
```

### Export Individual Parts as PDFs

```python
# Export each part as a separate PDF file
score.export_parts_as_pdf(
    output_dir='pdf_parts/',
    method='auto'
)

# Creates:
# pdf_parts/C_Flute.pdf
# pdf_parts/Bb_Clarinet_1.pdf
# pdf_parts/Eb_Alto_Sax_1.pdf
# etc.
```

### Create Parts Book

```python
# Create a single PDF with all parts
# Includes title page and individual part pages
score.export_parts_book('parts_book.pdf')
```

### Complete Multi-Part Example

```python
from music_recognition import (
    MusicRecognitionSystem,
    ScoreAssembler,
    BandInstruments
)

# Initialize
system = MusicRecognitionSystem(model_path='checkpoints/best_model.pth')
assembler = ScoreAssembler(recognition_system=system)

# Process multiple parts
part_images = {
    'C Flute': 'parts/flute.jpg',
    'Bb Clarinet': 'parts/clarinet.jpg',
    'Trombone': 'parts/trombone.jpg',
}

instruments = {
    'C Flute': BandInstruments.C_FLUTE,
    'Bb Clarinet': BandInstruments.Bb_CLARINET_1,
    'Trombone': BandInstruments.C_TROMBONE_1,
}

# Assemble score
score = assembler.create_score_from_parts(
    part_images=part_images,
    instruments=instruments,
    title="My Band Arrangement",
    composer="Your Name"
)

# Export everything
score.export_pdf('full_score.pdf')                      # Full score
score.export_pdf('concert.pdf', concert_pitch=True)    # Concert pitch
score.export_parts_as_pdf('parts/')                    # Individual PDFs
score.export_parts_book('parts_book.pdf')              # Parts book
```

## Titles and Text

### Title Above First Staff

Add titles above the first staff of your score:

```python
from music_recognition import StaffPaperGenerator
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

generator = StaffPaperGenerator(staves_per_page=12)
c = canvas.Canvas('score.pdf', pagesize=letter)

# Draw staff
staff_y = generator.staff_positions[0]
generator.draw_staff_lines(c, staff_y)

# Add title above staff
generator.draw_title_above_staff(
    c,
    staff_y,
    "I. Allegro con brio",
    font_size=14,
    bold=True,
    centered=True
)

c.save()
```

### Song Titles Within Staves

Place song titles directly on staves (useful for song collections):

```python
# Draw staff
staff_y = generator.staff_positions[0]
generator.draw_staff_lines(c, staff_y)

# Add song title within the staff
generator.draw_title_in_staff(
    c,
    x_position=generator.LEFT_MARGIN,
    staff_y=staff_y,
    title="1. Amazing Grace",
    font_size=12,
    bold=True
)

# Add clef and time signature after title
clef_x = generator.LEFT_MARGIN + 2.5 * inch
generator.draw_clef(c, clef_x, staff_y, 'treble')
```

### Section Markers

Add rehearsal marks and section labels:

```python
# Draw section marker above staff
generator.draw_section_marker(
    c,
    x_position=generator.LEFT_MARGIN,
    staff_y=staff_y,
    text="A",
    style='box'  # 'box', 'circle', or 'plain'
)

# Common section labels
sections = ["Intro", "A", "B", "Bridge", "Chorus", "Verse", "Coda"]

# With different styles
generator.draw_section_marker(c, x, y, "A", style='box')     # Boxed
generator.draw_section_marker(c, x, y, "B", style='circle')  # Circled
generator.draw_section_marker(c, x, y, "Verse", style='plain')  # Plain text
```

### Complete Example with Titles

```python
from music_recognition import StaffPaperGenerator
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

generator = StaffPaperGenerator(staves_per_page=12)
c = canvas.Canvas('score_with_titles.pdf', pagesize=letter)

# Page title
c.setFont("Helvetica-Bold", 24)
c.drawCentredString(generator.PAGE_WIDTH / 2, generator.PAGE_HEIGHT - 0.5 * inch, "Symphony No. 1")

c.setFont("Helvetica", 14)
c.drawCentredString(generator.PAGE_WIDTH / 2, generator.PAGE_HEIGHT - 0.8 * inch, "by Ludwig van Beethoven")

# First staff with movement title
staff_y = generator.staff_positions[0]
generator.draw_staff_lines(c, staff_y)

generator.draw_title_above_staff(c, staff_y, "I. Allegro con brio", font_size=14, bold=True)

c.save()
```

## Table of Contents

### Create Table of Contents for Multi-Part Score

Generate a professional table of contents for your band/orchestral arrangements:

```python
from music_recognition import MultiPartScore, BandInstruments
from music_recognition.postprocessing import MusicScore

# Create multi-part score
score = MultiPartScore(title="Concert March", composer="John Composer")

# Add parts...
# (see Multi-Part Scores section)

# Export with table of contents
score.export_with_toc(
    'score_with_toc.pdf',
    include_blank_pages=True  # Include blank staff pages for each part
)
```

### Custom Table of Contents

Create custom TOC pages:

```python
from music_recognition import TableOfContentsGenerator
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas('custom_toc.pdf', pagesize=letter)
toc_gen = TableOfContentsGenerator()

# Parts for a band score
parts = [
    {
        'name': 'C Flute',
        'instrument': 'Non-transposing',
        'page': 3,
        'measures': 64
    },
    {
        'name': '1st Bb Clarinet',
        'instrument': 'Transposing (Bb)',
        'page': 4,
        'measures': 64
    },
    # ... more parts
]

toc_gen.create_parts_toc(
    c,
    score_title="Concert March in Eb",
    composer="Composer Name",
    parts=parts
)

c.save()
```

### Song Collection TOC

Create a table of contents for song books:

```python
songs = [
    {
        'title': 'Amazing Grace',
        'composer': 'Traditional',
        'page': 1,
        'key': 'G Major',
        'tempo': 'Andante'
    },
    {
        'title': 'Ode to Joy',
        'composer': 'L. van Beethoven',
        'page': 3,
        'key': 'D Major',
        'tempo': 'Allegro'
    },
    # ... more songs
]

toc_gen.create_song_list_toc(
    c,
    collection_title="Classic Piano Collection",
    songs=songs,
    include_keys=True,
    include_tempo=True
)
```

### Simple TOC with Chapters

```python
entries = [
    {'title': 'Introduction', 'page': 1},
    {'title': 'Chapter 1: Scales', 'page': 5},
    {'title': '  Major Scales', 'page': 6, 'indent': 1},
    {'title': '  Minor Scales', 'page': 10, 'indent': 1},
    {'title': 'Chapter 2: Arpeggios', 'page': 15},
    {'title': 'Appendix', 'page': 25},
]

toc_gen.create_toc_page(
    c,
    title="Music Theory Workbook",
    entries=entries,
    toc_title="Table of Contents"
)
```

### Complete Score with TOC and Blank Pages

```python
from music_recognition import create_score_with_toc

parts = [
    {
        'name': 'C Flute',
        'instrument': 'Flute',
        'clef': 'treble',
        'time_signature': (4, 4),
        'measures': 48
    },
    {
        'name': '1st Bb Clarinet',
        'instrument': 'Bb Clarinet',
        'clef': 'treble',
        'time_signature': (4, 4),
        'measures': 48
    },
    # ... more parts
]

# Creates title page, TOC, and blank staff pages for each part
create_score_with_toc(
    output_path='complete_score.pdf',
    score_title='Spring Festival Overture',
    composer='Composer Name',
    parts=parts,
    include_part_pages=True  # Include blank staff pages
)
```

### TOC Features

The table of contents generator supports:

- **Part listings** with instrument names and page numbers
- **Song collections** with composer, key, and tempo
- **Chapter structure** with indentation
- **Dotted lines** connecting titles to page numbers
- **Automatic pagination** for long lists
- **Section grouping** (Woodwinds, Brass, etc.)
- **Measure counts** for each part
- **Custom styling** and formatting

## Advanced Customization

### Custom Staff Configuration

```python
from music_recognition import StaffPaperGenerator

# Change number of staves per page
generator = StaffPaperGenerator(staves_per_page=8)

# Custom staff dimensions
generator.STAFF_LINE_SPACING = 0.2 * generator.inch  # Wider spacing
generator.LEFT_MARGIN = 1.0 * generator.inch          # Larger margins
```

### Multi-Part Score Paper

```python
generator = StaffPaperGenerator(staves_per_page=12)

# Create paper for entire ensemble
parts = [
    {'name': 'C Flute', 'clef': 'treble'},
    {'name': 'Bb Clarinet', 'clef': 'treble'},
    {'name': 'Eb Alto Sax', 'clef': 'treble'},
    {'name': 'Trombone', 'clef': 'bass'},
]

generator.create_multipart_score_paper(
    output_path='band_paper.pdf',
    parts=parts,
    time_signature=(4, 4),
    staves_per_part=1
)
```

### Custom Title Page

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas('custom_score.pdf', pagesize=letter)

# Custom title page
c.setFont("Helvetica-Bold", 36)
c.drawCentredString(4.25*72, 9*72, "My Amazing Score")

c.setFont("Helvetica", 24)
c.drawCentredString(4.25*72, 8*72, "by Composer Name")

c.showPage()

# Add staff pages using generator
generator = StaffPaperGenerator()
# ... add staff pages ...

c.save()
```

## Backend Configuration

### Configure music21

```python
import music21

# Interactive configuration
music21.configure.run()

# Or set paths manually
env = music21.environment.Environment()
env['musescoreDirectPNGPath'] = '/path/to/musescore'
env['lilypondPath'] = '/path/to/lilypond'
```

### Verovio Installation

```bash
# macOS
brew install verovio

# Ubuntu/Debian
sudo apt-get install verovio

# Or download from https://www.verovio.org/
```

### Test Backends

```python
from music_recognition import check_pdf_backends

# Prints status of all backends
check_pdf_backends()
```

## Command Line Examples

### Basic Usage

```bash
# Create blank paper
python -c "from music_recognition import create_blank_sheet; create_blank_sheet('paper.pdf', 10)"

# Create instrument template
python -c "from music_recognition import create_instrument_part; create_instrument_part('clarinet.pdf', 'Bb Clarinet')"

# Run all examples
python pdf_examples.py

# Run specific example
python pdf_examples.py --example 1

# Check backends
python pdf_examples.py --check-backends
```

### Batch Create Templates

```bash
# Create templates for all instruments in your ensemble
python << 'EOF'
from music_recognition import create_instrument_part, BandInstruments

instruments = [
    ('C Flute', 'treble'),
    ('Bb Clarinet', 'treble'),
    ('Eb Alto Sax', 'treble'),
    ('Trombone', 'bass'),
]

for name, clef in instruments:
    filename = name.replace(' ', '_').lower()
    create_instrument_part(f'{filename}.pdf', name, clef, num_pages=5)
    print(f"Created {filename}.pdf")
EOF
```

## Tips and Best Practices

1. **Quality**: Use music21 + MuseScore for best results
2. **Speed**: Use reportlab for quick blank paper generation
3. **Consistency**: Keep staff spacing consistent (0.15" standard)
4. **Measures**: 4-6 measures per staff is typical
5. **Page Numbers**: Always included automatically
6. **Margins**: 0.75" margins are standard for binding

## Troubleshooting

### PDF Export Fails

```python
# Check what's available
from music_recognition import check_pdf_backends
check_pdf_backends()

# Try specific method
score.export_pdf('output.pdf', method='basic')  # Always works
```

### music21 Not Working

```bash
# Reinstall
pip uninstall music21
pip install music21

# Configure
python -c "import music21; music21.configure.run()"
```

### Font Issues

```python
# reportlab uses built-in fonts
# For custom fonts, register them:
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('CustomFont', 'path/to/font.ttf'))
```

## Integration with Notation Software

### Export for MuseScore

```python
# Export as MusicXML (imports into MuseScore)
score.export_musicxml('score.xml')

# Then in MuseScore: File → Open → score.xml
# Or use music21 to export directly
```

### Export for Sibelius

```python
# Export as MusicXML
score.export_musicxml('score.xml')

# Import in Sibelius: File → Open
```

### Export for Finale

```python
# Export as MusicXML
score.export_musicxml('score.xml')

# Import in Finale: File → Import → MusicXML
```

## Export Modes: Full Score vs Song Collection

### Overview

The system provides two distinct export modes for different use cases:

1. **Full Score Book**: All parts together with vertically aligned barlines
2. **Song Collection**: Multiple songs per page for later extraction

### Mode 1: Full Score Book with Aligned Barlines

**Use this mode when:**
- Creating conductor scores
- All parts play together
- Barlines must align vertically
- Professional ensemble scores

**Features:**
- ✓ Vertically aligned barlines across all parts
- ✓ System brackets connecting staves
- ✓ Part labels on the left
- ✓ Professional score layout

**Example:**

```python
from music_recognition import MultiPartScore, BandInstruments
from music_recognition.postprocessing import MusicScore

# Create score
score = MultiPartScore(title="Concert March", composer="John Composer")

# Add parts
parts = [
    ('C Flute', BandInstruments.C_FLUTE),
    ('Bb Clarinet', BandInstruments.Bb_CLARINET_1),
    ('Alto Sax', BandInstruments.Eb_ALTO_SAX_1),
    ('Trombone', BandInstruments.C_TROMBONE_1),
]

for name, instrument in parts:
    part = MusicScore()
    part.clef = instrument.clef.value
    score.add_part(name, part, instrument)

# Export as full score book
score.export_full_score_book(
    'full_score.pdf',
    num_pages=10,               # Total pages
    measures_per_system=4,      # Measures in each system
    systems_per_page=2          # Systems on each page
)
```

**Result:**
- Each page contains multiple systems
- Each system shows all parts together
- Barlines are vertically aligned
- Perfect for conductor scores

### Mode 2: Song Collection (Multiple Songs per Page)

**Use this mode when:**
- Creating song books
- Each song is independent
- Songs will be extracted individually later
- Space efficiency is important

**Features:**
- ✓ Multiple independent songs per page
- ✓ Song titles clearly labeled
- ✓ Compact layout
- ✓ Easy to extract individual songs

**Example:**

```python
# Export as song collection
score.export_as_song_collection(
    'song_book.pdf',
    songs_per_page=4,    # Fit 4 songs on each page
    staves_per_song=3    # 3 staves for each song
)
```

**Result:**
- Each page contains multiple songs
- Each song has its own title
- Songs are vertically stacked
- Perfect for song books and collections

### Direct Creation (Without MultiPartScore)

#### Full Score Book

```python
from music_recognition import create_full_score_book

parts = [
    {'name': 'Flute', 'clef': 'treble', 'time_signature': (4, 4)},
    {'name': 'Clarinet', 'clef': 'treble', 'time_signature': (4, 4)},
    {'name': 'Trombone', 'clef': 'bass', 'time_signature': (4, 4)},
]

create_full_score_book(
    output_path='score.pdf',
    score_title='My Band Score',
    composer='Composer Name',
    parts=parts,
    num_pages=8,
    measures_per_system=4,
    systems_per_page=2
)
```

#### Song Collection

```python
from music_recognition import create_song_collection

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
    # ... more songs
]

create_song_collection(
    output_path='songs.pdf',
    collection_title='Classic Songs',
    songs=songs,
    songs_per_page=3,
    staves_per_song=4
)
```

### Comparison

| Feature | Full Score Book | Song Collection |
|---------|----------------|-----------------|
| **Layout** | All parts together | Songs stacked separately |
| **Barlines** | Vertically aligned | Independent per song |
| **Brackets** | System brackets | None |
| **Part Labels** | Yes, on left | Song titles above |
| **Density** | Lower (2-3 systems/page) | Higher (3-4 songs/page) |
| **Best For** | Conductor scores | Song books |
| **Extraction** | View all parts together | Extract individual songs |

### Advanced Customization

#### Custom System Layout

```python
from music_recognition import AlignedScoreLayout
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas('custom.pdf', pagesize=letter)
layout = AlignedScoreLayout()

parts = [
    {'name': 'Soprano', 'clef': 'treble', 'time_signature': (3, 4)},
    {'name': 'Alto', 'clef': 'treble', 'time_signature': (3, 4)},
    {'name': 'Tenor', 'clef': 'treble', 'time_signature': (3, 4)},
    {'name': 'Bass', 'clef': 'bass', 'time_signature': (3, 4)},
]

layout.create_full_score_page(
    c,
    parts=parts,
    page_title="Choral Score - Page 1",
    measures_per_system=3,
    systems_per_page=4
)

c.save()
```

#### Custom Song Page

```python
from music_recognition import SongCollectionLayout

c = canvas.Canvas('songs.pdf', pagesize=letter)
layout = SongCollectionLayout()

songs = [
    {'title': 'Song 1', 'clef': 'treble', 'time_signature': (4, 4)},
    {'title': 'Song 2', 'clef': 'treble', 'time_signature': (3, 4)},
]

layout.create_song_page(
    c,
    songs=songs,
    staves_per_song=4,
    page_title="My Songs - Page 1"
)

c.save()
```

### Extraction Workflow

For song collections, you can later extract individual songs:

```python
from music_recognition import SongCollectionLayout

# Get song regions (bounding boxes)
layout = SongCollectionLayout()
regions = layout.extract_song_regions(
    songs=songs,
    staves_per_song=3
)

# Each region contains:
# - song_index
# - title
# - y_top, y_bottom
# - x_left, x_right

# Use these coordinates to extract individual songs from the PDF
# (requires PDF manipulation library like PyPDF2 or pdfrw)
```

### Command Line Examples

```bash
# Run full score examples
python score_layout_examples.py --example 1

# Run song collection examples
python score_layout_examples.py --example 2

# Compare both modes
python score_layout_examples.py --example 6

# Show usage guide
python score_layout_examples.py --guide
```

### Best Practices

**For Full Score Books:**
- Use 2-3 systems per page for readability
- Keep measures per system to 3-5
- Include part labels on the first system
- Use system brackets to group instruments

**For Song Collections:**
- Allocate 3-4 staves per song
- Fit 3-4 songs per page
- Include clear song titles
- Leave space between songs

## Next Steps

- Experiment with different staff configurations
- Create templates for your ensemble
- Process handwritten parts and export to PDF
- Share parts with musicians

For more information:
- `README.md` - General overview
- `MULTIPART_GUIDE.md` - Multi-part score documentation
- `pdf_examples.py` - Example code
