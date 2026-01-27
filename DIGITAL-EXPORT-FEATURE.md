# Digital Music Export Feature

## 🎵 Overview

The system digitizes handwritten music sheets into **clean, professional notation files**:
1. **MusicXML Format** - Open in MuseScore, Finale, Sibelius, Dorico
2. **MIDI Format** - Play back in any music software or DAW
3. **Full Conductor Scores** - Complete scores with all parts for each song
4. **Individual Part Files** - Separate MusicXML and MIDI for each instrument

---

## 📚 What Gets Created

For each of the 288 songs in your hymnal, the system generates:

### PDF Output (Printable):
- **1 digitized multi-part book** - Clean version preserving original layout (10-12 staves/page)
- **1 full conductor score** - All 28 parts combined in traditional score format

### Digital Export Files:
- **28 MusicXML files** - Industry-standard notation format (one per instrument)
- **28 MIDI files** - Audio playback files (one per instrument)
- **index.json** - Metadata listing all parts

### Layout Preservation:
- Songs stay on the **same pages** as uploaded handwritten PDFs
- **10-12 staves per page** (matches original handwritten layout)
- **Variable measure widths** - Not all measures are the same size
- **Consistent notation** - Clef, time signature, and key signature stay the same throughout
- **Song names in staves** - Preserve any song titles or text written in the staves

---

## 🎯 Output Structure

```
web_output/
  └── [Your Project Name]/
      ├── individual_books/          # Traditional PDF books
      │   ├── C_Flute_1.pdf
      │   ├── Bb_Clarinet_1.pdf
      │   └── ...
      │
      └── songs/                      # Individual songs (288 songs)
          ├── books/                  # Digitized multi-part books
          │   ├── 001_Hallelujah_Im_Going_Home.pdf        # Clean digitized book (10-12 staves/page)
          │   ├── 002_Make_Somebody_Glad.pdf
          │   └── ... (288 digitized books)
          │
          ├── scores/                 # Full conductor scores
          │   ├── 001_Hallelujah_Im_Going_Home_Score.pdf  # All 28 parts combined
          │   ├── 002_Make_Somebody_Glad_Score.pdf
          │   └── ... (288 scores)
          │
          └── digital_export/         # MusicXML and MIDI exports
              ├── 001_Hallelujah_Im_Going_Home/
              │   ├── index.json
              │   ├── musicxml/
              │   │   ├── C_Flute_1.musicxml
              │   │   ├── Bb_Clarinet_1.musicxml
              │   │   └── ... (28 MusicXML files)
              │   └── midi/
              │       ├── C_Flute_1.mid
              │       ├── Bb_Clarinet_1.mid
              │       └── ... (28 MIDI files)
              │
              ├── 002_Make_Somebody_Glad/
              │   └── ... (same structure)
              │
              └── ... (288 song folders)
```

---

## 🖥️ How to Use the Digital Exports

### Step 1: Complete Processing
Upload your 18 handwritten PDFs and process them in the web interface

### Step 2: Download Files
After processing completes, download the generated files:
- **288 digitized PDF books** - Clean multi-part books (10-12 staves/page)
- **288 conductor score PDFs** - Full scores with all parts
- **288 folders with MusicXML/MIDI** - 28 files each for individual instrument playback

### Step 3: Open in Music Software

**For Notation Viewing/Editing (MusicXML):**
- Open `.musicxml` files in MuseScore (Free!)
- Or use Finale, Sibelius, Dorico, Notion

**For Audio Playback (MIDI):**
- Open `.mid` files in any MIDI player
- Or import into DAWs (Logic, Ableton, FL Studio)
- Or open in notation software for playback

### Step 4: Use the Files
- **Edit notation** - Fix any recognition errors
- **Transpose** - Change keys as needed
- **Print** - Export to PDF from notation software
- **Record** - Use MIDI for audio production
- **Share** - Send MusicXML/MIDI to other musicians

---

## 📋 File Formats Explained

### MusicXML (.musicxml)
- **What it is:** Industry-standard notation format
- **Use with:** MuseScore, Finale, Sibelius, Dorico, Notion
- **Contains:** Complete musical notation, clefs, key signatures, notes, rhythms
- **Editable:** Yes - you can edit in notation software
- **Playback:** Most notation software can play MusicXML files

### MIDI (.mid)
- **What it is:** Musical Instrument Digital Interface audio format
- **Use with:** Any MIDI player, DAWs (Logic, FL Studio, Ableton), notation software
- **Contains:** Note events, timing, velocity (volume), tempo
- **Editable:** Yes - in DAWs or notation software
- **Playback:** All music software supports MIDI playback

### PDF (.pdf)
- **What it is:** Printable sheet music
- **Use for:** Printing physical copies for musicians
- **Contains:** Visual representation of the score
- **Editable:** No (read-only)
- **Playback:** No audio capability

---

## 🎹 Using with Professional Software

### MuseScore (Free!)
1. Open MuseScore
2. File → Open
3. Select the .musicxml file
4. Press Play to hear it
5. Edit notation as needed
6. Export to PDF, MP3, or other formats

### Finale / Sibelius / Dorico
1. Import the .musicxml file
2. Edit and arrange as needed
3. Professional engraving and layout tools
4. Export to various formats

### DAWs (Logic Pro, Ableton, FL Studio)
1. Import the .mid file
2. Assign instruments/sounds
3. Mix and produce
4. Export as audio (MP3, WAV)

---

## 🎼 All 28 Instrument Parts

The system generates clean notation for:

### Woodwinds (16 parts):
C Flute 1, C Flute 2, C Flute 3, Bb Clarinet 1, Bb Clarinet 2, Bb Clarinet 3, Eb Alto Clarinet, Bb Bass Clarinet, Bb Soprano Saxophone, Eb Alto Saxophone 1, Eb Alto Saxophone 2, Eb Alto Saxophone 3, Bb Tenor Saxophone, Eb Baritone Saxophone, Oboe, Bassoon

### Brass (9 parts):
Bb Trumpet 1, Bb Trumpet 2, Bb Trumpet 3, F French Horn, C Trombone 1, C Trombone 2, C Baritone BC, Bb Baritone TC, Tuba

### Strings (3 parts):
Violin, Viola, Cello

**Total: 28 professional part books** for each of the 288 songs!

### Score Organization:
Conductor scores can be arranged in two ways:
- **By Instrument Group**: Woodwinds → Brass → Strings (traditional orchestral order)
- **By Part Number**: All 1st parts, then 2nd parts, then 3rd parts, etc.

---

## 🔧 What You Can Do with the Files

### In MuseScore (Free!):
- **View and Edit** - See clean notation, make corrections
- **Play back** - Hear each part or full score
- **Transpose** - Change keys easily
- **Print** - Export high-quality PDFs
- **Share** - Send files to other musicians

### In Finale/Sibelius/Dorico:
- **Professional Engraving** - Perfect layout and formatting
- **Advanced Editing** - Full notation control
- **Custom Arrangements** - Modify and adapt scores
- **Publishing** - Prepare for performance or recording

### In DAWs (Logic, Ableton, FL Studio):
- **MIDI Import** - Bring melodies into your productions
- **Instrument Assignment** - Use virtual instruments
- **Mix and Master** - Create polished recordings
- **Audio Export** - Generate MP3, WAV files

---

## 💡 Use Cases

### For Musicians
- **Practice at home** - Listen to your part
- **Learn new music** - Follow notation while listening
- **Check notes** - Verify correct pitches
- **Slow down** - Practice difficult passages

### For Directors/Teachers
- **Prepare rehearsals** - Review all parts
- **Create practice tracks** - Export audio for students
- **Edit scores** - Fix errors in notation software
- **Distribute parts** - Email MusicXML/MIDI files

### For Arrangers
- **Import and edit** - Modify arrangements
- **Transpose** - Change keys easily
- **Add parts** - Create new instrumental parts
- **Export** - Share in multiple formats

### For Churches/Ensembles
- **Digital library** - Organize your music
- **Easy access** - View scores on tablets/laptops
- **No paper** - Reduce printing costs
- **Backup** - Never lose your music

---

## 📊 Output Format Comparison

| Feature | Handwritten PDF | Digitized PDF | MusicXML | MIDI |
|---------|----------------|---------------|----------|------|
| **Printable** | ✅ Yes | ✅ Yes | ✅ Yes* | ❌ No |
| **Clean notation** | ❌ Handwritten | ✅ Professional | ✅ Professional | ❌ N/A |
| **Audio playback** | ❌ No | ❌ No | ✅ Yes** | ✅ Yes |
| **Editable** | ❌ No | ❌ No | ✅ Yes | ✅ Yes |
| **Transposable** | ❌ No | ❌ No | ✅ Yes | ✅ Yes |
| **Software compatible** | Limited | Limited | ✅ All notation software | ✅ All music software |
| **File size** | Large | Large | Small | Very small |

\* Export to PDF from notation software
\*\* Play in notation software

---

## 🚀 Getting Started

### Processing Workflow

When processing your 18 handwritten multi-part PDFs, the system automatically:
1. **Digitizes** each page → Clean notation preserving layout (10-12 staves/page, same pages)
2. **Extracts** 288 individual songs with proper page boundaries
3. **Creates** for each song:
   - 1 digitized PDF book (preserving multi-part layout, song names in staves)
   - 1 full conductor score PDF (all 28 parts combined)
   - 28 MusicXML files (one per instrument - editable)
   - 28 MIDI files (one per instrument - playback)

**Important**: Clef, time signature, and key signature stay consistent throughout each song.

All generated automatically!

### Using Your Digital Files

1. **Complete processing** in the web interface
2. **Download files** - Get all songs and parts
3. **Open in software** - MuseScore (free!), Finale, Sibelius, or any MIDI player
4. **Edit and play** - Fix errors, transpose, hear the music
5. **Print or share** - Create PDFs, send to musicians

---

## 📥 Downloading Individual Songs

Each song provides multiple download options:

### From Web Interface:
- Click on a song
- Select "Download" for the part you want
- Choose format: MusicXML, MIDI, or PDF

### From File System:
Navigate to: `web_output/[Project]/songs/digital_export/[Song Name]/`
- **musicxml/** folder - All 28 notation files
- **midi/** folder - All 28 audio files
- **index.json** - Metadata for all parts

---

## ✅ Summary

With the digital export feature, you get:

- ✅ **288 songs** extracted and digitized from handwritten hymnal
- ✅ **Layout preserved** - Songs stay on same pages, 10-12 staves/page
- ✅ **Song names in staves** - Preserves titles and text from original
- ✅ **Consistent notation** - Clef, time, and key signatures stay the same
- ✅ **28 parts per song** - Complete instrumentation for each song
- ✅ **288 digitized PDF books** - Clean multi-part books matching original layout
- ✅ **288 full conductor scores** - All parts combined in score format
- ✅ **8,064 MusicXML files** - Editable in MuseScore, Finale, Sibelius, Dorico
- ✅ **8,064 MIDI files** - Audio playback in any music software
- ✅ **Complete instrumentation** - Woodwinds (16), Brass (9), Strings (3)
- ✅ **Ready to use** - Open files directly in professional software

**Total Files Generated:**
- **576 PDF files** (288 digitized books + 288 conductor scores)
- **8,064 MusicXML files** (28 parts × 288 songs - editable notation)
- **8,064 MIDI files** (28 parts × 288 songs - audio playback)
- **288 index.json files** (metadata)
- **16,992 total files!**

---

🎵 **Your complete digitized music library - from handwritten sheets to professional notation!**
