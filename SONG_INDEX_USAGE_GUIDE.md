# Song Index Usage Guide

Your **God of Mercy Church Band Hymnal** table of contents is **extremely valuable** for organizing and generating music books! This guide shows how the table of contents integrates with the workflow.

---

## What the Table of Contents Provides

From your table of contents, we have:
- **125+ Songs** in your collection
- **Song Titles**: "Hallelujah, I'm Going Home", "Goodbye, World, Goodbye", etc.
- **Song Numbers**: 001, 002, 003, ... 125
- **Alphabetical Organization**: Quick lookup by song name

---

## How This Helps Your Workflow

### 1. **Organized Song Extraction**

When you upload your 12 PDFs, you'll need to tell the system where each song starts and ends. The table of contents gives you the complete song list:

```python
from music_recognition import SongIndex, extract_songs_and_create_scores

# Load your song index
index = SongIndex()
index.load_from_json('god_of_mercy_songs.json')

# Define measure boundaries (you'll do this once after digitizing)
index.update_measure_boundaries({
    '003': {'start': 0, 'end': 32},      # Hallelujah, I'm Going Home
    '004': {'start': 33, 'end': 64},     # Goodbye, World, Goodbye
    '005': {'start': 65, 'end': 96},     # Make Somebody Glad
    # ... continue for all 125 songs
})

# Get songs ready for extraction
songs = index.get_songs_for_extraction()

# Extract all 125 songs automatically!
results = extract_songs_and_create_scores(complete_score, songs)
```

---

### 2. **Consistent File Naming**

All your exported song scores and part books will use the official song titles:

**Without Index:**
```
output/songs/scores/
    Song_001.pdf
    Song_002.pdf
```

**With Index:**
```
output/songs/scores/
    Hallelujah_Im_Going_Home.pdf
    Goodbye_World_Goodbye.pdf
    Make_Somebody_Glad.pdf
```

Much more organized and searchable!

---

### 3. **Generate Professional Table of Contents**

The system can create a professional table of contents in your PDF exports:

```python
from music_recognition.table_of_contents import TableOfContentsGenerator
from music_recognition.song_index import create_god_of_mercy_church_band_index

# Get song data
index = create_god_of_mercy_church_band_index()

# Format for TOC
toc_entries = []
for song in index.songs:
    toc_entries.append({
        'title': f"{song['number']}. {song['title']}",
        'page': song.get('page', None)  # Will be calculated during export
    })

# Add TOC to your PDF exports
# (This happens automatically in the complete_workflow)
```

**Result:** Your PDF will have a beautiful table of contents at the front, just like a professional hymnal!

---

## Complete Workflow with Song Index

Here's how the table of contents integrates into the complete workflow:

### Step 1: Create Song Index (One-Time Setup)

```python
from music_recognition.song_index import create_god_of_mercy_church_band_index

# Create index from your table of contents
index = create_god_of_mercy_church_band_index()

print(f"Loaded {index.count()} songs")  # Shows: Loaded 125+ songs

# Save for later use
index.save_to_json('my_song_index.json')
```

### Step 2: Upload and Digitize (As Before)

```python
from music_recognition import (
    PDFMusicReader,
    MusicRecognitionSystem,
    MultiPartScore,
    AutoScoreBuilder
)

# Upload your 12 PDFs
physical_books = [
    ('Trombone 1', 'scans/trombone_1.pdf'),
    ('Trombone 2', 'scans/trombone_2.pdf'),
    # ... all 12 books
]

# Digitize ALL books
reader = PDFMusicReader()
system = MusicRecognitionSystem()
score = MultiPartScore(title="God of Mercy Church Band Hymnal")

for book_name, pdf_file in physical_books:
    extraction = reader.process_pdf_score(pdf_file)
    for staff_info in extraction['staves']:
        recognized = system.recognize_from_file(staff_info['image_path'])
        score.add_part(book_name, recognized['score'], instrument)

# Generate derived parts
complete_score = AutoScoreBuilder.build_complete_score(score)
```

### Step 3: Define Song Boundaries Using Index

After digitizing, you'll examine the score and define where each song starts:

```python
# Load your song index
from music_recognition.song_index import SongIndex
index = SongIndex()
index.load_from_json('my_song_index.json')

# Define measure boundaries for each song
# (You'll identify these by looking at the digitized score)
measure_boundaries = {
    '001': {'start': 0, 'end': 16},       # Make me an Instrument
    '002': {'start': 17, 'end': 32},      # Thanks To Him
    '003': {'start': 33, 'end': 48},      # Hallelujah, I'm Going Home
    '004': {'start': 49, 'end': 64},      # Goodbye, World, Goodbye
    '005': {'start': 65, 'end': 80},      # Make Somebody Glad
    # ... continue for all 125 songs
}

# Update index with boundaries
index.update_measure_boundaries(measure_boundaries)

# Save updated index
index.save_to_json('my_song_index.json')
```

### Step 4: Extract All 125 Songs Automatically!

```python
from music_recognition import extract_songs_and_create_scores

# Get songs ready for extraction
songs = index.get_songs_for_extraction()
print(f"Extracting {len(songs)} songs...")

# Extract all songs at once!
results = extract_songs_and_create_scores(
    complete_score,
    songs,
    output_base_dir='output/god_of_mercy_songs',
    split_combined=True  # Each instrument gets separate book per song
)

print(f"""
✓ Created {len(results['scores'])} full conductor scores
✓ Created {len(results['parts'])} song folders with individual parts
✓ Total individual part PDFs: {sum(len(parts) for parts in results['parts'].values())}
""")
```

**Output Structure:**
```
output/god_of_mercy_songs/
    scores/
        Make_me_an_Instrument.pdf
        Thanks_To_Him.pdf
        Hallelujah_Im_Going_Home.pdf
        Goodbye_World_Goodbye.pdf
        ... (125 scores total)
    parts/
        Make_me_an_Instrument/
            Trombone_1.pdf
            Flute_2.pdf
            Violin.pdf
            ... (22-27 parts per song)
        Thanks_To_Him/
            Trombone_1.pdf
            Flute_2.pdf
            ...
        ... (125 song folders)
```

---

## Benefits of Using the Table of Contents

| Benefit | Description |
|---------|-------------|
| **Organization** | Songs are named properly instead of "Song_001.pdf" |
| **Searchability** | Easy to find "Hallelujah, I'm Going Home" instead of "Song_003.pdf" |
| **Professional Output** | Generated PDFs include proper table of contents |
| **Scalability** | Handles all 125 songs without manual entry |
| **Metadata** | Preserves song numbers and titles from your hymnal |
| **Automation** | Process all songs at once instead of one-by-one |

---

## Quick Reference Commands

### Load Song Index
```python
from music_recognition.song_index import SongIndex, create_god_of_mercy_church_band_index

# From built-in data
index = create_god_of_mercy_church_band_index()

# From saved JSON
index = SongIndex()
index.load_from_json('my_song_index.json')
```

### Look Up a Song
```python
# By title
song = index.get_song_by_title("Hallelujah, I'm Going Home")
print(f"{song['title']} is song #{song['number']}")

# By number
song = index.get_song_by_number('003')
print(f"Song #003 is: {song['title']}")
```

### Generate Indexes
```python
# Alphabetical index
print(index.generate_alphabetical_index())

# Numerical index
print(index.generate_numerical_index())
```

### Update Measure Boundaries
```python
# Add measure data
index.update_measure_boundaries({
    '003': {'start': 0, 'end': 32},
    '004': {'start': 33, 'end': 64},
})

# Save updated
index.save_to_json('updated_index.json')
```

---

## Summary

Your table of contents **significantly improves** the workflow by providing:

✅ **Complete song catalog** (125+ songs)
✅ **Organized metadata** (titles, numbers)
✅ **Automated extraction** (process all songs at once)
✅ **Professional naming** (proper song titles in filenames)
✅ **Easy lookup** (find songs by title or number)
✅ **Integration ready** (works with web application)

This makes the entire process of digitizing, organizing, and distributing your hymnal much more efficient and professional! 🎵
