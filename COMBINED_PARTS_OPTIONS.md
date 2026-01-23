# Combined Parts Options

This document explains how to handle combined instrument parts in your music books.

## What are Combined Parts?

Combined parts are when multiple instruments share the same music on one physical sheet. Examples:
- **"Bb Clarinet 1/Bb Trumpet 1/Bb Soprano Sax"** - Three Bb instruments playing the same music
- **"Bb Clarinet 2/Bb Trumpet 2"** - Two instruments sharing one part
- **"Baritone T.C./Bb Bass Clarinet"** - Two instruments on one sheet

## Options for Handling Combined Parts

You have **two options** for how to export combined parts:

### Option 1: Split Into Separate Books (Default)

Each instrument gets its own individual book, even though they play the same music.

**Use Case**: You have multiple musicians who each need their own part book.

**Example**:
```python
from music_recognition import create_individual_books_from_score

# Split combined parts into separate books (default behavior)
books = create_individual_books_from_score(
    complete_score,
    output_dir='output/individual_books',
    split_combined=True  # This is the default
)

# From "Bb Clarinet 1/Bb Trumpet 1/Bb Soprano Sax", creates 3 separate PDFs:
#   ✓ 1st_Bb_Clarinet.pdf
#   ✓ 1st_Bb_Trumpet.pdf
#   ✓ Bb_Soprano_Sax.pdf
```

**Result**:
- Each musician has their own dedicated book
- 3 musicians = 3 separate PDF files
- Good for rehearsals where each player needs their own part

---

### Option 2: Keep Combined Parts Together

All instruments in the combined part share one book.

**Use Case**: You want to save paper/printing, or musicians are comfortable sharing.

**Example**:
```python
from music_recognition import create_individual_books_from_score

# Keep combined parts together in one book
books = create_individual_books_from_score(
    complete_score,
    output_dir='output/individual_books',
    split_combined=False  # Keep them together
)

# From "Bb Clarinet 1/Bb Trumpet 1/Bb Soprano Sax", creates 1 combined PDF:
#   ✓ Bb_Clarinet_1_Bb_Trumpet_1_Bb_Soprano_Sax.pdf
```

**Result**:
- One PDF for all three instruments
- The book cover shows all instruments: "Bb Clarinet 1/Bb Trumpet 1/Bb Soprano Sax"
- 3 musicians share 1 PDF file
- Good for saving printing costs or when instruments play together

---

## When to Use Each Option

| Scenario | Recommended Option | Why |
|----------|-------------------|-----|
| **Formal performances** | Split (`split_combined=True`) | Each musician has their own professional-looking part |
| **Rehearsals with multiple players per part** | Split | Each player can mark their own music independently |
| **Budget-conscious printing** | Keep together (`split_combined=False`) | Fewer pages to print |
| **Small ensembles** | Keep together | Easier to manage fewer files |
| **Digital distribution** | Split | Musicians only download what they need |
| **Archival purposes** | Keep together | Maintains the original combined structure |

---

## Complete Workflow Example

### Example: Creating Books for All 12 Physical Sheets

```python
from music_recognition import (
    MultiPartScore,
    AutoScoreBuilder,
    create_individual_books_from_score,
    extract_songs_and_create_scores
)

# Step 1: Process your 12 physical sheets
# (digitization and part generation happens here)
score = MultiPartScore(title="Band Collection")
# ... add all 12 parts ...

# Step 2: Generate derived parts
complete_score = AutoScoreBuilder.build_complete_score(score)

# Step 3a: Create individual books - SPLIT VERSION
split_books = create_individual_books_from_score(
    complete_score,
    output_dir='output/books_split',
    split_combined=True
)
print(f"Created {len(split_books)} separate books")
# Result: ~22-27 individual PDFs

# Step 3b: Create individual books - COMBINED VERSION
combined_books = create_individual_books_from_score(
    complete_score,
    output_dir='output/books_combined',
    split_combined=False
)
print(f"Created {len(combined_books)} books (some combined)")
# Result: Fewer PDFs (~15-20), some contain multiple instruments
```

---

## Song Extraction with Combined Parts Option

When extracting individual songs, you can also control whether to split combined parts:

```python
# Define your songs
songs = [
    {'title': 'March No. 1', 'start_measure': 0, 'end_measure': 32},
    {'title': 'Beautiful Waltz', 'start_measure': 33, 'end_measure': 64},
]

# Option A: Extract songs with SPLIT parts
results_split = extract_songs_and_create_scores(
    complete_score,
    songs,
    output_base_dir='output/songs_split',
    split_combined=True  # Each instrument gets separate book per song
)

# Option B: Extract songs with COMBINED parts
results_combined = extract_songs_and_create_scores(
    complete_score,
    songs,
    output_base_dir='output/songs_combined',
    split_combined=False  # Combined instruments share one book per song
)
```

**Output Structure** (split_combined=True):
```
output/songs_split/
    parts/
        March_No_1/
            1st_Bb_Clarinet.pdf         ← Individual book
            1st_Bb_Trumpet.pdf          ← Individual book
            Bb_Soprano_Sax.pdf          ← Individual book
            ...
```

**Output Structure** (split_combined=False):
```
output/songs_combined/
    parts/
        March_No_1/
            Bb_Clarinet_1_Bb_Trumpet_1_Bb_Soprano_Sax.pdf  ← Combined book
            ...
```

---

## Implementation Details

The system automatically handles combined parts by:

1. **Detecting combined parts**: Any part name with "/" is considered combined
2. **Parsing instrument names**: Extracts individual instrument names from combined labels
3. **Creating copies**: When splitting, creates identical copies of the music for each instrument
4. **Mapping instruments**: Assigns correct transposition and clef to each instrument
5. **Generating filenames**: Creates safe, descriptive filenames for each book

### Automatic Instrument Mapping

When splitting combined parts, the system automatically maps each instrument to its correct configuration:

- **"1st Bb Clarinet"** → Bb transposition, treble clef
- **"1st Bb Trumpet"** → Bb transposition, treble clef
- **"Bb Soprano Sax"** → Bb transposition, treble clef
- **"Baritone T.C."** → Bb transposition, treble clef
- **"Bb Bass Clarinet"** → Bb transposition, treble clef (sounds octave + major 2nd lower)

Each gets the same music data, but with proper metadata for that instrument.

---

## Web Application Support

When the web application is implemented, users will have a simple toggle:

```
┌─────────────────────────────────────────────┐
│  Export Settings                             │
├─────────────────────────────────────────────┤
│                                              │
│  Combined Parts Handling:                   │
│                                              │
│  ○ Split into separate books                │
│     Each instrument gets its own book        │
│                                              │
│  ○ Keep combined parts together             │
│     Instruments share one book               │
│                                              │
│  [Generate Books]                           │
└─────────────────────────────────────────────┘
```

This gives users complete flexibility to choose what works best for their needs!

---

## Summary

✅ **Default behavior**: Combined parts are split into separate books (`split_combined=True`)
✅ **Option available**: Keep combined parts together (`split_combined=False`)
✅ **Complete flexibility**: Choose per-export what works best for your needs
✅ **Automatic handling**: System properly maps instruments and creates correct transpositions

Whether you need 27 individual books or prefer to keep combined parts together to save printing costs, the system supports both workflows!
