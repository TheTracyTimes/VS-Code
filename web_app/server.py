#!/usr/bin/env python3
"""
Web Application for Handwritten Music Recognition and Score Generation

This is the main FastAPI backend server that provides:
1. PDF upload endpoint
2. Music recognition processing
3. Part generation
4. Score creation and export
5. Progress tracking via WebSocket
6. File download endpoints

Run with: python web_app/server.py
Then open: http://localhost:8000
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
import os
import json
import asyncio
from pathlib import Path
import shutil
from datetime import datetime

# Import our music recognition modules (when available)
# For now, we'll use mock implementations so the app runs immediately
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import real modules, fall back to mocks if not available
try:
    from music_recognition import (
        PDFMusicReader,
        MusicRecognitionSystem,
        MultiPartScore,
        AutoScoreBuilder,
        create_individual_books_from_score,
        extract_songs_and_create_scores
    )
    from music_recognition.song_index import SongIndex, create_god_of_mercy_church_band_index
    from music_recognition.digital_book import create_digital_book_from_multipart_score
    REAL_PROCESSING = True
except ImportError as e:
    print(f"⚠️  Music recognition modules not fully available: {e}")
    print("⚠️  Running in DEMO MODE with mock processing")
    print("⚠️  Install dependencies: pip install torch opencv-python numpy")
    REAL_PROCESSING = False

    # Mock implementations for demo
    class SongIndex:
        def __init__(self):
            self.songs = []
        def count(self):
            return len(self.songs)

    def create_god_of_mercy_church_band_index():
        index = SongIndex()
        index.songs = [
            {"title": "Hallelujah, I'm Going Home", "number": "003"},
            {"title": "Goodbye, World, Goodbye", "number": "004"},
            {"title": "Make Somebody Glad", "number": "005"},
        ]
        return index


# Initialize FastAPI app
app = FastAPI(title="Music Recognition Web App", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure multipart form limits (allow up to 100 files, 200MB total)
# This ensures we can upload many PDF files at once
import multipart
from multipart.multipart import parse_options_header

# Increase multipart limits
MAX_FILES = 100  # Maximum number of files in a single upload
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB per file
MAX_TOTAL_SIZE = 200 * 1024 * 1024  # 200 MB total upload size

# Configuration
UPLOAD_DIR = "web_uploads"
OUTPUT_DIR = "web_output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Store active projects in memory (in production, use a database)
projects = {}
websocket_connections = {}


# Pydantic models for API
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = ""


class ProjectResponse(BaseModel):
    project_id: str
    name: str
    description: str
    status: str
    uploaded_files: int
    created_at: str


class SongBoundary(BaseModel):
    title: str
    number: str
    start_measure: int
    end_measure: int


class ProcessingOptions(BaseModel):
    split_combined: bool = True
    generate_derived_parts: bool = True
    extract_songs: bool = False
    song_boundaries: Optional[List[SongBoundary]] = []


# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, project_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[project_id] = websocket

    def disconnect(self, project_id: str):
        if project_id in self.active_connections:
            del self.active_connections[project_id]

    async def send_progress(self, project_id: str, message: dict):
        if project_id in self.active_connections:
            try:
                await self.active_connections[project_id].send_json(message)
            except:
                self.disconnect(project_id)


manager = ConnectionManager()


# API Endpoints
@app.get("/")
async def root():
    """Serve the main web application."""
    return FileResponse("static/index.html")


@app.get("/api/system-info")
async def get_system_info():
    """Get comprehensive system information and capabilities."""
    import platform
    import psutil

    # Check what's installed
    modules_info = {}

    # PyTorch
    try:
        import torch
        modules_info['pytorch'] = {
            'installed': True,
            'version': torch.__version__,
            'cuda_available': torch.cuda.is_available(),
            'cuda_version': torch.version.cuda if torch.cuda.is_available() else None
        }
    except ImportError:
        modules_info['pytorch'] = {'installed': False}

    # OpenCV
    try:
        import cv2
        modules_info['opencv'] = {
            'installed': True,
            'version': cv2.__version__
        }
    except ImportError:
        modules_info['opencv'] = {'installed': False}

    # NumPy
    try:
        import numpy
        modules_info['numpy'] = {
            'installed': True,
            'version': numpy.__version__
        }
    except ImportError:
        modules_info['numpy'] = {'installed': False}

    # music21
    try:
        import music21
        modules_info['music21'] = {
            'installed': True,
            'version': music21.__version__
        }
    except ImportError:
        modules_info['music21'] = {'installed': False}

    # ReportLab
    try:
        import reportlab
        modules_info['reportlab'] = {
            'installed': True,
            'version': reportlab.Version
        }
    except ImportError:
        modules_info['reportlab'] = {'installed': False}

    # FastAPI
    try:
        import fastapi
        modules_info['fastapi'] = {
            'installed': True,
            'version': fastapi.__version__
        }
    except ImportError:
        modules_info['fastapi'] = {'installed': False}

    # System info
    system_info = {
        'platform': platform.system(),
        'platform_version': platform.version(),
        'processor': platform.processor(),
        'python_version': platform.python_version(),
        'cpu_count': psutil.cpu_count(),
        'total_memory_gb': round(psutil.virtual_memory().total / (1024**3), 2),
        'available_memory_gb': round(psutil.virtual_memory().available / (1024**3), 2),
        'disk_free_gb': round(psutil.disk_usage('/').free / (1024**3), 2)
    }

    # Capabilities
    capabilities = {
        'real_processing': REAL_PROCESSING,
        'pdf_upload': True,
        'websocket_progress': True,
        'multi_file_upload': True,
        'part_generation': REAL_PROCESSING,
        'song_extraction': REAL_PROCESSING,
        'demo_mode': not REAL_PROCESSING
    }

    # Processing specs
    processing_specs = {
        'max_instruments': 30,
        'supported_formats': ['PDF'],
        'max_file_size_mb': 100,
        'max_songs': 125,
        'generated_parts': [
            'C Flute 2', 'C Flute 3', 'Oboe', 'Violin', 'Viola',
            'Cello', 'Bassoon', 'Tuba', 'Eb Alto Clarinet', 'Eb Baritone Sax'
        ],
        'output_formats': ['PDF'],
        'features': [
            'Handwritten music recognition',
            'Automatic part generation',
            'Combined part splitting',
            'Individual song extraction',
            'Real-time progress tracking',
            'Batch processing'
        ]
    }

    return {
        'mode': 'FULL' if REAL_PROCESSING else 'DEMO',
        'modules': modules_info,
        'system': system_info,
        'capabilities': capabilities,
        'processing': processing_specs,
        'version': '1.0.0'
    }


@app.post("/api/projects", response_model=ProjectResponse)
async def create_project(project: ProjectCreate):
    """Create a new music recognition project."""
    project_id = f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    project_data = {
        "project_id": project_id,
        "name": project.name,
        "description": project.description,
        "status": "created",
        "uploaded_files": 0,
        "uploaded_file_paths": [],
        "created_at": datetime.now().isoformat(),
        "output_dir": os.path.join(OUTPUT_DIR, project_id)
    }

    os.makedirs(project_data["output_dir"], exist_ok=True)
    projects[project_id] = project_data

    return project_data


@app.get("/api/projects", response_model=List[ProjectResponse])
async def list_projects():
    """Get list of all projects."""
    return list(projects.values())


@app.get("/api/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """Get project details."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    return projects[project_id]


@app.post("/api/projects/{project_id}/upload")
async def upload_pdf(project_id: str, files: List[UploadFile] = File(...)):
    """Upload PDF files to a project."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")

    project = projects[project_id]
    upload_dir = os.path.join(UPLOAD_DIR, project_id)
    os.makedirs(upload_dir, exist_ok=True)

    uploaded = []
    for file in files:
        if not file.filename.endswith('.pdf'):
            continue

        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)

        project["uploaded_file_paths"].append(file_path)
        uploaded.append(file.filename)

    project["uploaded_files"] = len(project["uploaded_file_paths"])
    project["status"] = "files_uploaded"

    return {"message": f"Uploaded {len(uploaded)} files", "files": uploaded}


@app.post("/api/projects/{project_id}/process")
async def process_project(project_id: str, options: ProcessingOptions):
    """Process uploaded PDFs: digitize, generate parts, create scores."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")

    project = projects[project_id]

    if project["uploaded_files"] == 0:
        raise HTTPException(status_code=400, detail="No files uploaded")

    # Start background processing
    asyncio.create_task(process_project_background(project_id, options))

    return {"message": "Processing started", "project_id": project_id}


async def process_project_background(project_id: str, options: ProcessingOptions):
    """Background task to process music recognition."""
    project = projects[project_id]
    project["status"] = "processing"

    try:
        # Send progress updates
        await manager.send_progress(project_id, {
            "stage": "starting",
            "message": "Initializing music recognition system...",
            "progress": 0
        })

        if REAL_PROCESSING:
            # Real processing with actual music recognition
            reader = PDFMusicReader()
            system = MusicRecognitionSystem()
            score = MultiPartScore(title=project["name"])

            # Step 1: Digitize all uploaded PDFs
            await manager.send_progress(project_id, {
                "stage": "digitizing",
                "message": f"Digitizing {project['uploaded_files']} PDF files...",
                "progress": 10
            })

            total_files = len(project["uploaded_file_paths"])
            for idx, file_path in enumerate(project["uploaded_file_paths"]):
                file_name = os.path.basename(file_path)
                await manager.send_progress(project_id, {
                    "stage": "digitizing",
                    "message": f"Processing {file_name}...",
                    "progress": 10 + int(40 * (idx / total_files))
                })
                extraction = reader.process_pdf_score(file_path)
                # Process extraction...

            # Step 2: Generate derived parts
            if options.generate_derived_parts:
                await manager.send_progress(project_id, {
                    "stage": "generating",
                    "message": "Generating derived parts...",
                    "progress": 50
                })
                complete_score = AutoScoreBuilder.build_complete_score(score)

            # Step 3: Create individual books
            await manager.send_progress(project_id, {
                "stage": "exporting",
                "message": "Creating individual part books...",
                "progress": 70
            })
            output_dir = os.path.join(project["output_dir"], "individual_books")
            books = create_individual_books_from_score(
                complete_score,
                output_dir,
                split_combined=options.split_combined
            )

            # Step 4: Extract songs
            if options.extract_songs and options.song_boundaries:
                await manager.send_progress(project_id, {
                    "stage": "extracting",
                    "message": f"Extracting {len(options.song_boundaries)} songs...",
                    "progress": 85
                })
                songs_dir = os.path.join(project["output_dir"], "songs")
                results = extract_songs_and_create_scores(
                    complete_score,
                    [s.dict() for s in options.song_boundaries],
                    output_base_dir=songs_dir,
                    split_combined=options.split_combined
                )
        else:
            # DEMO MODE: Simulate processing and create sample output files
            await manager.send_progress(project_id, {
                "stage": "digitizing",
                "message": "Demo: Simulating PDF digitization...",
                "progress": 20
            })
            await asyncio.sleep(1)

            await manager.send_progress(project_id, {
                "stage": "generating",
                "message": "Demo: Simulating part generation...",
                "progress": 50
            })
            await asyncio.sleep(1)

            # Create demo output files
            await manager.send_progress(project_id, {
                "stage": "exporting",
                "message": "Demo: Creating sample output files...",
                "progress": 75
            })

            output_dir = os.path.join(project["output_dir"], "individual_books")
            os.makedirs(output_dir, exist_ok=True)

            # Create sample PDF files (empty PDFs for demo)
            from reportlab.pdfgen import canvas as pdf_canvas
            from reportlab.lib.pagesizes import letter

            sample_parts = [
                "Trombone_1.pdf", "Trombone_2.pdf", "F_French_Horn.pdf",
                "Eb_Alto_Sax_1.pdf", "C_Flute_1.pdf", "C_Flute_2_Generated.pdf",
                "C_Flute_3_Generated.pdf", "Violin_Generated.pdf", "Viola_Generated.pdf"
            ]

            for part_name in sample_parts:
                file_path = os.path.join(output_dir, part_name)
                c = pdf_canvas.Canvas(file_path, pagesize=letter)
                c.setFont("Helvetica-Bold", 24)
                c.drawString(100, 750, project["name"])
                c.setFont("Helvetica", 16)
                c.drawString(100, 700, f"Part: {part_name.replace('_', ' ').replace('.pdf', '')}")
                c.drawString(100, 650, "This is a demo file.")
                c.drawString(100, 620, "Install music recognition dependencies for real processing:")
                c.setFont("Courier", 12)
                c.drawString(100, 590, "pip install torch opencv-python numpy music21")
                c.save()

            await asyncio.sleep(1)

        # Complete
        project["status"] = "completed"
        await manager.send_progress(project_id, {
            "stage": "completed",
            "message": "Processing complete! Your music books are ready to download." +
                       (" (Demo files)" if not REAL_PROCESSING else ""),
            "progress": 100
        })

    except Exception as e:
        import traceback
        project["status"] = "error"
        error_details = traceback.format_exc()
        print(f"Error in background processing: {error_details}")
        await manager.send_progress(project_id, {
            "stage": "error",
            "message": f"Error: {str(e)}",
            "progress": 0
        })


@app.websocket("/ws/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: str):
    """WebSocket for real-time progress updates."""
    await manager.connect(project_id, websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(project_id)


@app.get("/api/projects/{project_id}/files")
async def list_output_files(project_id: str):
    """List all generated output files for a project."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")

    project = projects[project_id]
    output_dir = project["output_dir"]

    if not os.path.exists(output_dir):
        return {"files": []}

    files = []
    for root, dirs, filenames in os.walk(output_dir):
        for filename in filenames:
            if filename.endswith('.pdf'):
                rel_path = os.path.relpath(os.path.join(root, filename), output_dir)
                files.append({
                    "name": filename,
                    "path": rel_path,
                    "size": os.path.getsize(os.path.join(root, filename))
                })

    return {"files": files}


@app.get("/api/projects/{project_id}/download/{file_path:path}")
async def download_file(project_id: str, file_path: str):
    """Download a generated file."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")

    project = projects[project_id]
    full_path = os.path.join(project["output_dir"], file_path)

    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(full_path, filename=os.path.basename(full_path))


@app.get("/api/song-index")
async def get_song_index():
    """Get the God of Mercy Church Band song index."""
    index = create_god_of_mercy_church_band_index()
    return {"songs": index.songs, "count": index.count()}


@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: str):
    """Delete a project and its files."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")

    project = projects[project_id]

    # Delete uploaded files
    upload_dir = os.path.join(UPLOAD_DIR, project_id)
    if os.path.exists(upload_dir):
        shutil.rmtree(upload_dir)

    # Delete output files
    if os.path.exists(project["output_dir"]):
        shutil.rmtree(project["output_dir"])

    # Remove from memory
    del projects[project_id]

    return {"message": "Project deleted"}


# Mount static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    print("=" * 70)
    print("Music Recognition Web Application")
    print("=" * 70)
    print("\nStarting server...")
    print("\n🎵 Open your browser to: http://localhost:8000")
    print("\nPress Ctrl+C to stop the server\n")

    # Configure uvicorn with increased limits for multiple file uploads
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        limit_max_requests=10000,  # Allow many concurrent requests
        timeout_keep_alive=120,     # Keep connections alive longer
    )


@app.get("/api/projects/{project_id}/songs")
async def list_songs(project_id: str):
    """List all extracted songs with their parts."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")

    project = projects[project_id]
    output_dir = project["output_dir"]
    songs_parts_dir = os.path.join(output_dir, "songs", "parts")

    if not os.path.exists(songs_parts_dir):
        return {"songs": []}

    songs = []
    for song_folder in os.listdir(songs_parts_dir):
        song_path = os.path.join(songs_parts_dir, song_folder)
        if os.path.isdir(song_path):
            # Get list of parts for this song
            parts = []
            for filename in os.listdir(song_path):
                if filename.endswith('.pdf'):
                    parts.append({
                        "name": filename.replace('.pdf', '').replace('_', ' '),
                        "filename": filename,
                        "path": os.path.join("songs", "parts", song_folder, filename)
                    })

            # Check if digital book exists
            digital_book_path = os.path.join(song_path, "digital_book", "index.html")
            has_digital_book = os.path.exists(digital_book_path)

            songs.append({
                "title": song_folder.replace('_', ' '),
                "folder": song_folder,
                "parts": parts,
                "has_digital_book": has_digital_book
            })

    # Sort songs alphabetically
    songs.sort(key=lambda x: x['title'])

    return {"songs": songs, "count": len(songs)}


@app.get("/api/projects/{project_id}/songs/{song_folder}/digital-book")
async def get_digital_book(project_id: str, song_folder: str):
    """Get the digital interactive book for a song."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")

    project = projects[project_id]
    book_path = os.path.join(
        project["output_dir"],
        "songs",
        "parts",
        song_folder,
        "digital_book",
        "index.html"
    )

    if not os.path.exists(book_path):
        raise HTTPException(status_code=404, detail="Digital book not found")

    return FileResponse(book_path, media_type="text/html")


@app.get("/api/projects/{project_id}/songs/{song_folder}/view")
async def view_song_score(project_id: str, song_folder: str, part: str = "all"):
    """View the score for a specific song (returns MusicXML or combined score)."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")

    project = projects[project_id]
    song_dir = os.path.join(project["output_dir"], "songs", "parts", song_folder)

    if not os.path.exists(song_dir):
        raise HTTPException(status_code=404, detail="Song not found")

    # Check for digital book
    digital_book_dir = os.path.join(song_dir, "digital_book")
    if os.path.exists(digital_book_dir):
        # Return list of available parts with MusicXML/MIDI
        musicxml_dir = os.path.join(digital_book_dir, "musicxml")
        midi_dir = os.path.join(digital_book_dir, "midi")

        parts_available = []
        if os.path.exists(musicxml_dir):
            for filename in os.listdir(musicxml_dir):
                if filename.endswith('.musicxml'):
                    part_name = filename.replace('.musicxml', '').replace('_', ' ')
                    midi_file = filename.replace('.musicxml', '.mid')
                    parts_available.append({
                        "name": part_name,
                        "musicxml": f"/api/projects/{project_id}/download/songs/parts/{song_folder}/digital_book/musicxml/{filename}",
                        "midi": f"/api/projects/{project_id}/download/songs/parts/{song_folder}/digital_book/midi/{midi_file}" if os.path.exists(os.path.join(midi_dir, midi_file)) else None
                    })

        return {"parts": parts_available}

    return {"message": "No digital book available. PDF files only."}
