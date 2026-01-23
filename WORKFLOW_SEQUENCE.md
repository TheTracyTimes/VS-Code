# Music Book Generator - Complete Workflow Sequence

Detailed step-by-step workflow for processing music books from upload to download.

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    WORKFLOW SEQUENCE                         │
└─────────────────────────────────────────────────────────────┘

Step 1: UPLOAD (Drag & Drop)
    ↓
    Upload all 12 PDF books
    Wait for all uploads to complete
    Validate all files

Step 2: DIGITIZE (Recognition)
    ↓
    Process all 12 PDFs in parallel
    Extract staff images
    Recognize music notation
    Store digitized music data

Step 3: GENERATE (Derived Parts) ← DEPENDS ON STEP 2 DATA
    ↓
    Use digitized data from Step 2
    Generate Flute 2 (from 2nd parts)
    Generate Flute 3 (from 3rd parts)
    Generate Violin, Viola, Cello, etc.
    Generate Eb Baritone Sax (from low brass)
    Total: 10+ new parts created

Step 4: SPLIT (Individual Books)
    ↓
    Split combined parts into individual books
    Example: "Bb Clarinet/Trumpet 1/Soprano Sax" → 3 books
    Total: 22-27 individual books

Step 5: EXTRACT (Songs)
    ↓
    User defines song boundaries
    Extract each song from all parts

Step 6: EXPORT (Generate PDFs)
    ↓
    Create individual part books (all songs)
    Create conductor scores (per song)
    Create individual parts (per song)

Step 7: DOWNLOAD
    ↓
    Download all generated PDFs
    Preview before downloading
    Download as ZIP
```

---

## Detailed Workflow Steps

### STEP 1: UPLOAD (User Action)

**User Interface:**
```
┌───────────────────────────────────────────────────────┐
│  Upload Your 12 Music Books                           │
│                                                        │
│  ┌──────────────────────────────────────────────┐    │
│  │  Drag & Drop PDFs here                       │    │
│  │  or click to browse                          │    │
│  │                                               │    │
│  │  📄 Supported: PDF files only                │    │
│  │  📊 Progress: 0/12 files uploaded            │    │
│  └──────────────────────────────────────────────┘    │
│                                                        │
│  Uploaded Files (0/12):                               │
│  [Empty - waiting for files]                          │
│                                                        │
│  [Continue to Digitize] (disabled until 12 uploaded)  │
└───────────────────────────────────────────────────────┘
```

**After Upload:**
```
┌───────────────────────────────────────────────────────┐
│  Upload Complete! ✓                                   │
│                                                        │
│  Uploaded Files (12/12): ✓                           │
│  ✓ Trombone_1.pdf                     2.3 MB         │
│  ✓ Trombone_2.pdf                     2.1 MB         │
│  ✓ French_Horn.pdf                    2.0 MB         │
│  ✓ Eb_Alto_Sax_1.pdf                 1.9 MB         │
│  ✓ Eb_Alto_Sax_2.pdf                 1.8 MB         │
│  ✓ Eb_Alto_Sax_3.pdf                 2.0 MB         │
│  ✓ Bb_Tenor_Sax.pdf                  1.7 MB         │
│  ✓ Bb_Clarinet_Trumpet_1.pdf         2.2 MB         │
│  ✓ Bb_Clarinet_Trumpet_2.pdf         2.0 MB         │
│  ✓ Baritone_BC.pdf                   1.9 MB         │
│  ✓ Baritone_TC.pdf                   2.1 MB         │
│  ✓ C_Flute_1.pdf                     1.8 MB         │
│                                                        │
│  Total: 24.8 MB                                       │
│                                                        │
│  [Start Digitizing] ← NOW ENABLED                    │
└───────────────────────────────────────────────────────┘
```

**Backend Processing:**
```python
@app.post("/api/projects/{project_id}/upload")
async def upload_files(
    project_id: int,
    files: List[UploadFile],
    db: Session = Depends(get_db)
):
    """Upload all PDF files (wait for all 12)."""

    # Validate file count
    if len(files) != 12:
        raise HTTPException(
            status_code=400,
            detail=f"Expected 12 files, got {len(files)}"
        )

    # Save all files
    uploaded_files = []
    for file in files:
        # Validate PDF
        if not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail=f"File {file.filename} is not a PDF"
            )

        # Save to storage
        file_path = await save_file(file, project_id)

        # Create DB record
        db_file = File(
            project_id=project_id,
            filename=file.filename,
            file_path=file_path,
            status='uploaded'
        )
        db.add(db_file)
        uploaded_files.append(db_file)

    db.commit()

    return {
        "message": "All 12 files uploaded successfully",
        "files": uploaded_files,
        "ready_for_digitization": True
    }
```

---

### STEP 2: DIGITIZE (Automatic Processing)

**IMPORTANT:** This step must complete BEFORE Step 3 can start!

**User Interface:**
```
┌───────────────────────────────────────────────────────┐
│  Digitizing Your Music Books...                       │
│                                                        │
│  Overall Progress: ████████░░░░ 67% (8/12 complete)  │
│                                                        │
│  Currently Processing: Bb_Clarinet_Trumpet_2.pdf      │
│                                                        │
│  Completed:                                           │
│  ✓ Trombone_1.pdf           (45 measures recognized) │
│  ✓ Trombone_2.pdf           (42 measures recognized) │
│  ✓ French_Horn.pdf          (48 measures recognized) │
│  ✓ Eb_Alto_Sax_1.pdf       (46 measures recognized) │
│  ✓ Eb_Alto_Sax_2.pdf       (44 measures recognized) │
│  ✓ Eb_Alto_Sax_3.pdf       (43 measures recognized) │
│  ✓ Bb_Tenor_Sax.pdf        (41 measures recognized) │
│  ✓ Bb_Clarinet_Trumpet_1.pdf (47 measures)          │
│                                                        │
│  Processing:                                          │
│  ⏳ Bb_Clarinet_Trumpet_2.pdf (Page 2/3)             │
│                                                        │
│  Pending:                                             │
│  ⏸ Baritone_BC.pdf                                   │
│  ⏸ Baritone_TC.pdf                                   │
│  ⏸ C_Flute_1.pdf                                     │
│                                                        │
│  Estimated time remaining: 3 minutes                  │
└───────────────────────────────────────────────────────┘
```

**Backend Processing:**
```python
@app.post("/api/projects/{project_id}/digitize")
async def start_digitization(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Start digitizing all uploaded files."""

    # Verify all 12 files uploaded
    files = db.query(File).filter(
        File.project_id == project_id,
        File.status == 'uploaded'
    ).all()

    if len(files) != 12:
        raise HTTPException(
            status_code=400,
            detail=f"Need 12 files uploaded, found {len(files)}"
        )

    # Queue digitization task
    task = digitize_all_books.delay(project_id)

    # Update project status
    project = db.query(Project).get(project_id)
    project.status = 'digitizing'
    db.commit()

    return {
        "task_id": task.id,
        "status": "digitizing",
        "message": "Digitization started for all 12 books"
    }


# Celery task for digitization
@celery_app.task(bind=True)
def digitize_all_books(self, project_id: int):
    """
    Digitize all 12 books in parallel.
    MUST complete before derived parts can be generated.
    """
    from music_recognition import (
        PDFMusicReader,
        MusicRecognitionSystem,
        MultiPartScore,
        BandInstruments
    )

    db = get_db()
    files = db.query(File).filter(
        File.project_id == project_id
    ).order_by(File.filename).all()

    reader = PDFMusicReader()
    system = MusicRecognitionSystem()

    # Create multipart score
    score = MultiPartScore(title="Band Collection")

    # Instrument mapping
    instrument_map = {
        'trombone_1': BandInstruments.C_TROMBONE_1,
        'trombone_2': BandInstruments.C_TROMBONE_2,
        'french_horn': BandInstruments.F_FRENCH_HORN_1,
        'eb_alto_sax_1': BandInstruments.Eb_ALTO_SAX_1,
        'eb_alto_sax_2': BandInstruments.Eb_ALTO_SAX_2,
        'eb_alto_sax_3': BandInstruments.Eb_ALTO_SAX_3,
        'bb_tenor_sax': BandInstruments.Bb_TENOR_SAX,
        'bb_clarinet_trumpet_1': BandInstruments.Bb_CLARINET_1,
        'bb_clarinet_trumpet_2': BandInstruments.Bb_CLARINET_2,
        'baritone_bc': BandInstruments.C_EUPHONIUM_BC,
        'baritone_tc': BandInstruments.Bb_BARITONE_TC,
        'c_flute_1': BandInstruments.C_FLUTE,
    }

    total_files = len(files)

    for i, file in enumerate(files):
        # Update progress
        percent = int((i / total_files) * 100)
        self.update_state(
            state='PROGRESS',
            meta={
                'current': i + 1,
                'total': total_files,
                'percent': percent,
                'current_file': file.filename
            }
        )

        # Extract from PDF
        extraction = reader.process_pdf_score(file.file_path)

        # Recognize notation
        recognized_measures = []
        for staff_info in extraction['staves']:
            result = system.recognize_from_file(staff_info['image_path'])
            if result:
                recognized_measures.extend(result['score'].measures)

        # Get instrument
        file_key = file.filename.lower().replace('.pdf', '').replace('_', '_')
        instrument = instrument_map.get(file_key, BandInstruments.C_FLUTE)

        # Create score
        part_score = MusicScore()
        part_score.measures = recognized_measures

        # Add to multipart score
        score.add_part(file.filename.replace('.pdf', ''), part_score, instrument)

        # Update file status
        file.status = 'digitized'
        file.measures_recognized = len(recognized_measures)
        db.commit()

    # Save digitized score to database
    save_digitized_score(project_id, score)

    # Update project status
    project = db.query(Project).get(project_id)
    project.status = 'digitized'
    project.digitization_complete = True
    db.commit()

    return {
        'status': 'complete',
        'books_digitized': total_files,
        'ready_for_generation': True
    }
```

**Completion Notification:**
```
┌───────────────────────────────────────────────────────┐
│  ✓ Digitization Complete!                             │
│                                                        │
│  Successfully digitized all 12 books:                 │
│  • Total measures recognized: 534                     │
│  • Average confidence: 94.2%                          │
│  • Processing time: 4 min 23 sec                      │
│                                                        │
│  Ready to generate derived parts!                     │
│                                                        │
│  [Continue to Part Generation] →                     │
└───────────────────────────────────────────────────────┘
```

---

### STEP 3: GENERATE DERIVED PARTS (Uses Step 2 Data)

**CRITICAL:** This step REQUIRES digitized data from Step 2!

**User Interface:**
```
┌───────────────────────────────────────────────────────┐
│  Generate Derived Parts                               │
│                                                        │
│  Using digitized data from your 12 uploaded books,    │
│  we can automatically generate 10 additional parts:   │
│                                                        │
│  ☑ Flute 2                                            │
│     Source: 2nd Clarinet, 2nd Trumpet, 2nd Alto Sax  │
│     Method: Concert pitch + flute range               │
│                                                        │
│  ☑ Flute 3                                            │
│     Source: 3rd Clarinet, 3rd Trumpet, 3rd Alto Sax, │
│            Tenor Sax                                  │
│     Method: Concert pitch + flute range               │
│                                                        │
│  ☑ Oboe (= Flute 2)                                  │
│  ☑ Violin (= Flute 1 octave down)                   │
│  ☑ Viola (= Flute 3 octave down, treble clef)       │
│  ☑ Cello (= Trombone 1)                              │
│  ☑ Bassoon (= Trombone 2)                            │
│  ☑ Tuba (= Baritone B.C. octave down)                │
│  ☑ Alto Clarinet (= 3rd Alto Sax)                    │
│  ☑ Eb Baritone Sax                                    │
│     Source: Baritone B.C., Baritone T.C., Tuba       │
│     Method: Concert pitch + bari sax range            │
│                                                        │
│  [Generate All Parts] ← Starts generation             │
└───────────────────────────────────────────────────────┘
```

**During Generation:**
```
┌───────────────────────────────────────────────────────┐
│  Generating Derived Parts...                          │
│                                                        │
│  Progress: ████████████░░ 80% (8/10 complete)        │
│                                                        │
│  ✓ Flute 2 generated (48 measures)                   │
│  ✓ Flute 3 generated (47 measures)                   │
│  ✓ Oboe created (copy of Flute 2)                    │
│  ✓ Violin generated (48 measures)                    │
│  ✓ Viola generated (47 measures)                     │
│  ✓ Cello created (copy of Trombone 1)                │
│  ✓ Bassoon created (copy of Trombone 2)              │
│  ✓ Tuba generated (43 measures)                      │
│  ⏳ Generating Alto Clarinet...                       │
│  ⏸ Pending: Eb Baritone Sax                          │
│                                                        │
│  Estimated time remaining: 30 seconds                 │
└───────────────────────────────────────────────────────┘
```

**Backend Processing:**
```python
@app.post("/api/projects/{project_id}/generate-parts")
async def generate_derived_parts(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    Generate derived parts using digitized data.
    REQUIRES: Project status = 'digitized'
    """

    # Verify digitization complete
    project = db.query(Project).get(project_id)

    if not project.digitization_complete:
        raise HTTPException(
            status_code=400,
            detail="Cannot generate parts: digitization not complete"
        )

    # Queue generation task
    task = generate_all_derived_parts.delay(project_id)

    # Update status
    project.status = 'generating'
    db.commit()

    return {
        "task_id": task.id,
        "status": "generating",
        "message": "Generating 10 derived parts from digitized data"
    }


# Celery task
@celery_app.task(bind=True)
def generate_all_derived_parts(self, project_id: int):
    """
    Generate all derived parts.
    Uses digitized data from Step 2.
    """
    from music_recognition import AutoScoreBuilder

    db = get_db()

    # Load digitized score from database
    digitized_score = load_digitized_score(project_id)

    # Update progress
    self.update_state(
        state='PROGRESS',
        meta={'step': 'loading', 'percent': 0}
    )

    # Generate ALL derived parts automatically
    # This uses the digitized data:
    # - Flute 2: from 2nd Clarinet, 2nd Trumpet, 2nd Alto Sax
    # - Flute 3: from 3rd Clarinet, 3rd Trumpet, 3rd Alto Sax, Tenor Sax
    # - Eb Bari Sax: from Baritone B.C., Baritone T.C., Tuba
    # - Violin: from Flute 1
    # - Viola: from generated Flute 3
    # - Cello: from Trombone 1
    # - Bassoon: from Trombone 2
    # - Tuba: from Baritone B.C.
    # - Alto Clarinet: from 3rd Alto Sax
    # - Oboe: from generated Flute 2

    complete_score = AutoScoreBuilder.build_complete_score(digitized_score)

    # Save generated parts
    save_complete_score(project_id, complete_score)

    # Update project
    project = db.query(Project).get(project_id)
    project.status = 'parts_generated'
    project.parts_generated = len(complete_score.parts)
    db.commit()

    return {
        'status': 'complete',
        'original_parts': len(digitized_score.parts),
        'generated_parts': len(complete_score.parts),
        'new_parts_created': len(complete_score.parts) - len(digitized_score.parts)
    }
```

**Completion:**
```
┌───────────────────────────────────────────────────────┐
│  ✓ Part Generation Complete!                          │
│                                                        │
│  Created 10 new derived parts:                        │
│  ✓ Flute 2 (48 measures)                             │
│  ✓ Flute 3 (47 measures)                             │
│  ✓ Oboe (48 measures)                                │
│  ✓ Violin (48 measures)                              │
│  ✓ Viola (47 measures)                               │
│  ✓ Cello (45 measures)                               │
│  ✓ Bassoon (42 measures)                             │
│  ✓ Tuba (43 measures)                                │
│  ✓ Alto Clarinet (43 measures)                       │
│  ✓ Eb Baritone Sax (42 measures)                     │
│                                                        │
│  Total parts: 22 (12 original + 10 generated)         │
│                                                        │
│  [Continue to Song Extraction] →                     │
└───────────────────────────────────────────────────────┘
```

---

## API Workflow Sequence

```javascript
// Frontend React workflow

const uploadAndProcess = async () => {
  // STEP 1: Upload all 12 files
  const files = [/* 12 PDF files */];

  const uploadResponse = await api.post(
    `/projects/${projectId}/upload`,
    { files }
  );

  if (uploadResponse.ready_for_digitization) {
    // STEP 2: Start digitization
    const digitizeResponse = await api.post(
      `/projects/${projectId}/digitize`
    );

    // Monitor progress via WebSocket
    socket.on('digitization_progress', (progress) => {
      updateProgress(progress);
    });

    // Wait for completion
    socket.on('digitization_complete', async (data) => {
      if (data.ready_for_generation) {
        // STEP 3: Generate derived parts
        const generateResponse = await api.post(
          `/projects/${projectId}/generate-parts`
        );

        // Monitor generation
        socket.on('generation_progress', (progress) => {
          updateProgress(progress);
        });

        socket.on('generation_complete', (data) => {
          // Now ready for song extraction, export, etc.
          navigateTo('/project/' + projectId + '/songs');
        });
      }
    });
  }
};
```

---

## Summary: Why This Sequence Matters

### ❌ WRONG (Won't Work):
```
Upload PDF 1 → Digitize → Generate parts → Upload PDF 2 → ...
```
**Problem:** Can't generate Flute 2 without all 2nd parts digitized!

### ✅ CORRECT (Will Work):
```
Upload ALL 12 PDFs
    ↓
Digitize ALL 12 PDFs (get all music data)
    ↓
Generate parts (using ALL digitized data)
    ↓
Split, extract, export
```

### Key Dependencies:

1. **Flute 2** needs:
   - 2nd Bb Clarinet (digitized)
   - 2nd Bb Trumpet (digitized)
   - 2nd Eb Alto Sax (digitized)
   - 2nd Trombone (digitized)

2. **Flute 3** needs:
   - 3rd Bb Clarinet (digitized)
   - 3rd Bb Trumpet (digitized)
   - 3rd Eb Alto Sax (digitized)
   - Bb Tenor Sax (digitized)

3. **Eb Baritone Sax** needs:
   - Baritone B.C. (digitized)
   - Baritone T.C. (digitized)
   - Tuba part if available (digitized)

4. **Violin** needs:
   - C Flute 1 (digitized)

5. **Viola** needs:
   - Flute 3 (which needs 3rd parts digitized first!)

**Therefore:** ALL uploads → ALL digitization → THEN generation!

---

## User Experience Flow

```
User uploads 12 PDFs → "Start Digitizing" button appears
    ↓
User clicks "Start Digitizing"
    ↓
Progress bar shows: "Digitizing 8/12 books..."
    ↓
When complete: "✓ Ready to generate parts!"
    ↓
User clicks "Generate Parts"
    ↓
Progress bar shows: "Generating 7/10 parts..."
    ↓
When complete: "✓ All parts ready! Extract songs or download now"
    ↓
User can now:
  - Define songs
  - Download individual books
  - Download conductor scores
  - Download song-specific parts
```

---

This ensures the system has ALL the necessary data before attempting to create derived parts!
