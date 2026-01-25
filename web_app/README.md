# Music Recognition Web Application

A beautiful, easy-to-use web interface for digitizing handwritten music sheets and generating professional part books.

## Features

✨ **Drag & Drop Upload** - Simply drag your 12 PDF files into the browser
🎵 **Automatic Processing** - Digitize all sheets and generate derived parts automatically
📊 **Real-time Progress** - Watch the progress as your music is being processed
📥 **Easy Downloads** - Download all generated part books with one click
🎼 **125 Songs** - Built-in song index for God of Mercy Church Band Hymnal
⚙️ **Flexible Options** - Choose to split or combine parts, extract individual songs

---

## Quick Start

### 1. Install Dependencies

```bash
cd web_app
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python server.py
```

### 3. Open Your Browser

Navigate to: **http://localhost:8000**

That's it! You're ready to start digitizing music!

---

## How to Use

### Step 1: Create a Project

1. Enter your project name (e.g., "God of Mercy Church Band Hymnal")
2. Optionally add a description
3. Click "Create Project"

### Step 2: Upload Your PDF Files

1. Drag and drop all 12 PDF files into the upload zone
2. Or click to browse and select files
3. Review the file list
4. Click "Upload All Files"

### Step 3: Configure Processing Options

Choose your processing options:

- ✅ **Generate derived parts** - Create Flute 2, Flute 3, Violin, Viola, Cello, Bassoon, Tuba, etc.
- ✅ **Split combined parts** - Separate "Bb Clarinet/Trumpet 1/Soprano Sax" into 3 individual books
- ⬜ **Extract individual songs** - Create separate scores for each of the 125 songs

Click "Start Processing" to begin!

### Step 4: Watch the Progress

Watch in real-time as the system:
1. Digitizes all 12 PDF files
2. Recognizes handwritten music notation
3. Generates derived instrumental parts
4. Creates individual part books
5. Exports professional PDFs

### Step 5: Download Your Music Books

Once complete, you'll see all generated PDFs:
- Individual part books (22-27 books depending on options)
- Full conductor scores
- Individual song extracts (if enabled)

Click any file to download it instantly!

---

## What Gets Generated

### With Default Options (Split Combined = True)

From your 12 uploaded PDFs, the system creates **22-27 individual part books**:

**Original Parts (12 physical sheets → 20 books):**
1. Trombone 1
2. Trombone 2
3. F French Horn
4. Eb Alto Saxophone 1
5. Eb Alto Saxophone 2
6. Eb Alto Saxophone 3
7. Bb Tenor Sax
8. Bb Clarinet 3
9. Bb Trumpet 3
10. Bb Clarinet 1 *(split from combined)*
11. Bb Trumpet 1 *(split from combined)*
12. Bb Soprano Sax *(split from combined)*
13. Bb Clarinet 2 *(split from combined)*
14. Bb Trumpet 2 *(split from combined)*
15. Baritone B.C.
16. Baritone T.C. *(split from combined)*
17. Bb Bass Clarinet *(split from combined)*
18. C Flute 1

**Auto-Generated Parts (10 new books):**
19. **C Flute 2** - Based on 2nd parts, adjusted to flute range
20. **C Flute 3** - Based on 3rd parts, adjusted to flute range
21. **Oboe** - Copy of Flute 2
22. **Violin** - Flute 1 one octave down
23. **Viola** - Flute 3 one octave down (treble clef)
24. **Cello** - Copy of Trombone 1
25. **Bassoon** - Copy of Trombone 2
26. **Tuba** - Baritone B.C. one octave down
27. **Eb Alto Clarinet** - Copy of 3rd Alto Sax
28. **Eb Baritone Sax** - Generated from low brass parts

### File Structure

```
web_output/
└── project_20260125_143022/
    ├── individual_books/
    │   ├── Trombone_1.pdf
    │   ├── Trombone_2.pdf
    │   ├── C_Flute_1.pdf
    │   ├── C_Flute_2.pdf  (generated)
    │   ├── C_Flute_3.pdf  (generated)
    │   ├── Violin.pdf     (generated)
    │   ├── Viola.pdf      (generated)
    │   ├── Cello.pdf      (generated)
    │   └── ... (all 22-27 books)
    │
    └── songs/  (if song extraction enabled)
        ├── scores/
        │   ├── Hallelujah_Im_Going_Home.pdf
        │   ├── Goodbye_World_Goodbye.pdf
        │   └── ... (125 songs)
        └── parts/
            ├── Hallelujah_Im_Going_Home/
            │   ├── Trombone_1.pdf
            │   ├── Flute_2.pdf
            │   └── ... (all parts for this song)
            └── ... (125 song folders)
```

---

## API Endpoints

The backend provides a full REST API:

### Projects

- `POST /api/projects` - Create a new project
- `GET /api/projects` - List all projects
- `GET /api/projects/{id}` - Get project details
- `DELETE /api/projects/{id}` - Delete a project

### File Operations

- `POST /api/projects/{id}/upload` - Upload PDF files
- `POST /api/projects/{id}/process` - Start processing
- `GET /api/projects/{id}/files` - List output files
- `GET /api/projects/{id}/download/{path}` - Download file

### Real-time Updates

- `WebSocket /ws/{project_id}` - Real-time progress updates

### Song Index

- `GET /api/song-index` - Get the 125-song index

---

## Architecture

```
┌─────────────────┐
│   Web Browser   │  ← User Interface (HTML/CSS/JavaScript)
│  (Your Device)  │
└────────┬────────┘
         │ HTTP/WebSocket
         │
┌────────▼────────┐
│   FastAPI       │  ← Backend Server (Python)
│   Server        │
│  (port 8000)    │
└────────┬────────┘
         │
    ┌────┴────┬───────────┬─────────────┐
    │         │           │             │
┌───▼───┐ ┌──▼──┐  ┌─────▼─────┐ ┌────▼────┐
│ PDF   │ │Music│  │   Part    │ │  Song   │
│Reader │ │ AI  │  │ Generator │ │Extractor│
└───────┘ └─────┘  └───────────┘ └─────────┘
```

### Technology Stack

**Backend:**
- **FastAPI** - Modern Python web framework
- **Uvicorn** - Lightning-fast ASGI server
- **WebSockets** - Real-time progress updates

**Frontend:**
- **Vanilla JavaScript** - No frameworks needed!
- **Modern CSS** - Beautiful gradient design
- **Responsive** - Works on desktop and mobile

**Processing:**
- **OpenCV** - Image processing
- **NumPy** - Numerical operations
- **music21** - Music notation handling
- **ReportLab** - PDF generation

---

## Configuration

Edit `server.py` to customize:

```python
# Upload directory
UPLOAD_DIR = "web_uploads"

# Output directory
OUTPUT_DIR = "web_output"

# Server port
# Change in the uvicorn.run() call at bottom of server.py
port = 8000
```

---

## Development

### Run in Development Mode

```bash
# With auto-reload
uvicorn web_app.server:app --reload --host 0.0.0.0 --port 8000
```

### Access from Other Devices

To access the web app from other devices on your network:

1. Find your computer's IP address:
   ```bash
   # On Windows
   ipconfig

   # On Mac/Linux
   ifconfig
   ```

2. Open browser on other device to:
   ```
   http://YOUR_IP_ADDRESS:8000
   ```

---

## Troubleshooting

### Port Already in Use

If port 8000 is already in use, change it in `server.py`:

```python
uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
```

### File Upload Fails

- Check file size limits (default is usually 100MB)
- Ensure PDFs are valid and not corrupted
- Check disk space in `web_uploads/` directory

### Processing Takes Too Long

- Processing 12 PDFs with 125 songs can take several minutes
- Watch the progress bar for updates
- Check console output for detailed logs

### Downloads Not Working

- Check `web_output/` directory exists and has permissions
- Ensure project wasn't deleted
- Try refreshing the browser

---

## Production Deployment

For production use, consider:

1. **Use a production ASGI server**:
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker web_app.server:app
   ```

2. **Add authentication** - Protect the upload endpoint

3. **Use a database** - PostgreSQL instead of in-memory storage

4. **Add file storage** - S3 or similar for uploads/outputs

5. **Enable HTTPS** - Use nginx as reverse proxy with SSL

6. **Set up Celery** - For background task processing

See `WEB_APPLICATION_ARCHITECTURE.md` for full production architecture.

---

## Features Coming Soon

🔄 **Batch Processing** - Process multiple projects simultaneously
👥 **User Accounts** - Save and manage your projects
☁️ **Cloud Storage** - Store files in the cloud
📧 **Email Notifications** - Get notified when processing completes
🎨 **Preview** - Preview scores before downloading
✏️ **Editor** - Edit recognized notes and fix errors
📱 **Mobile App** - Native iOS and Android apps

---

## Support

For issues or questions:
1. Check the main documentation in project root
2. Review `WEB_APPLICATION_ARCHITECTURE.md` for technical details
3. Check server console output for error messages

---

## License

This web application is part of the Music Recognition project.

---

**Made with ❤️ for musicians everywhere**

Start digitizing your handwritten music sheets today! 🎵
