# Full Installation Guide - Real Music Recognition

Complete installation for **actual handwritten music digitization** with AI-powered recognition.

---

## What You're Installing

### Core AI/ML Components:
- **PyTorch** (~2.0 GB) - Deep learning framework
- **TorchVision** (~200 MB) - Computer vision models
- **OpenCV** (~50 MB) - Image processing
- **NumPy** - Numerical computing

### Music Processing:
- **music21** - Music notation library
- **ReportLab** - PDF generation
- **SciPy** - Scientific computing

### Web Application:
- **FastAPI** - Modern web framework
- **Uvicorn** - High-performance server
- **WebSockets** - Real-time updates
- **psutil** - System information

---

## Installation Steps

### Step 1: Check Requirements

**Minimum:**
- Python 3.8 or higher
- 8 GB RAM
- 5 GB free disk space
- Internet connection

**Recommended:**
- Python 3.9+
- 16 GB RAM
- 10 GB free disk space
- GPU with CUDA support (for faster processing)

**Check your Python version:**
```bash
python --version
# or
python3 --version
```

### Step 1.5: Install System Dependencies (For PDF Support)

To process PDF files, you need **Poppler** installed on your system:

**Mac:**
```bash
brew install poppler
```

**Ubuntu/Debian:**
```bash
sudo apt-get install poppler-utils
```

**Fedora:**
```bash
sudo dnf install poppler-utils
```

**Windows:**
- Download from: https://github.com/oschwartz10612/poppler-windows/releases/
- Extract and add to PATH

**Don't have Homebrew on Mac?**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

⚠️ **Can skip this step** if you don't plan to upload PDFs (images will still work).

### Step 2: Run the Full Installer

**On Mac/Linux:**
```bash
./install-full.sh
```

**On Windows:**
```bash
install-full.bat
```

**What happens:**
1. Upgrades pip to latest version
2. Downloads PyTorch (~2 GB)
3. Installs all dependencies from requirements.txt
4. Verifies installation
5. Shows success message

**Time required:** 5-30 minutes depending on:
- Internet speed
- Computer performance
- Whether PyTorch is cached

### Step 3: Wait for Installation

You'll see progress like this:
```
Installing all dependencies from requirements.txt...
   (This will take several minutes...)

Downloading torch-2.0.0-cp39-cp39-linux_x86_64.whl (2.1 GB)
████████████████████ 100%

Installing collected packages: torch, torchvision, opencv-python...
```

**Don't close the terminal!** This is normal and can take 10-20 minutes.

### Step 4: Verify Installation

When complete, you'll see:
```
============================================================
  ✅ INSTALLATION SUCCESSFUL!
============================================================

Installed components:
  ✓ PyTorch 2.0.0
  ✓ OpenCV
  ✓ FastAPI Web Framework
  ✓ Music21 Notation Library
  ✓ All music recognition modules

============================================================
  🚀 READY TO USE!
============================================================
```

### Step 5: Start the Web App

```bash
cd web_app
python server.py
```

You'll see:
```
==============================
Music Recognition Web Application
==============================

Starting server...

🎵 Open your browser to: http://localhost:8000

Press Ctrl+C to stop the server
```

### Step 6: Open Your Browser

Go to: **http://localhost:8000**

You'll see the web interface with **System Status** showing:

```
System Status                    FULL MODE ✅

Processing Mode: ✅ Real Music Recognition
Python Version: 3.9.7
CPU Cores: 8
Memory: 12 GB available / 16 GB total
Disk Space: 45 GB free
Platform: Linux
PyTorch: ✅ v2.0.0
OpenCV: ✅ v4.8.0
```

Click "Show Detailed Specifications" to see:
- All installed modules
- Full system capabilities
- Generated parts list (10 automatic parts)
- Processing specifications

---

## What Each Component Does

### PyTorch (2 GB)
- **Purpose:** AI/Machine Learning framework
- **Used for:** Handwritten music recognition CNN model
- **Why needed:** Core of the recognition system
- **Alternative:** None - required for real processing

### OpenCV (50 MB)
- **Purpose:** Image processing library
- **Used for:** PDF page extraction, staff line detection
- **Why needed:** Processes scanned images
- **Alternative:** None - required for PDF processing

### music21 (30 MB)
- **Purpose:** Music notation toolkit
- **Used for:** Music theory, transposition, score manipulation
- **Why needed:** Handles musical transformations
- **Alternative:** None - required for proper notation

### FastAPI + Uvicorn (20 MB)
- **Purpose:** Web framework and server
- **Used for:** Running the web application
- **Why needed:** Provides the browser interface
- **Alternative:** Could use command line, but web is easier

---

## Troubleshooting

### Installation Fails

**Problem:** `ERROR: Could not find a version that satisfies the requirement torch`

**Solution:** Upgrade pip and try again:
```bash
python -m pip install --upgrade pip
./install-full.sh
```

---

**Problem:** `No space left on device`

**Solution:** Free up disk space (need 5GB+):
```bash
# Check available space
df -h

# Clean pip cache if needed
pip cache purge
```

---

**Problem:** Installation hangs at "Downloading torch"

**Solution:** This is normal! PyTorch is 2GB. Wait 10-30 minutes depending on internet speed.

---

**Problem:** `ModuleNotFoundError: No module named 'torch'`

**Solution:** Installation didn't complete. Run installer again:
```bash
./install-full.sh
```

---

### Web App Won't Start

**Problem:** `Address already in use`

**Solution:** Port 8000 is busy. Change port in `web_app/server.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8080)  # Changed from 8000
```

---

**Problem:** Web page shows "DEMO MODE" even though PyTorch installed

**Solution:** Restart the server:
```bash
# Stop server: Ctrl+C
# Start again:
cd web_app
python server.py
```

---

### GPU Support (Optional)

**To use GPU (if you have NVIDIA card):**

1. Check if CUDA is available:
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

2. If False, install CUDA-enabled PyTorch:
```bash
# Visit: https://pytorch.org/get-started/locally/
# Select your OS, CUDA version, and install command
```

3. Restart web app - it will show "CUDA enabled" in specs

---

## What You Can Do Now

With full installation, you can:

✅ **Upload real PDFs** - Your scanned handwritten music
✅ **Digitize notation** - CNN recognizes actual notes
✅ **Generate 10 parts** - Automatic Flute 2, Violin, Viola, etc.
✅ **Split combined parts** - Separate "Clarinet/Trumpet" into 2 books
✅ **Extract 125 songs** - Individual songs from full collection
✅ **Download PDFs** - Professional part books ready to print

---

## File Structure After Installation

```
VS-Code/
├── requirements.txt          # All dependencies (installed)
├── install-full.sh          # Installer you just ran
├── web_app/
│   ├── server.py            # Web server (running)
│   └── static/
│       └── index.html       # Web interface (open in browser)
├── music_recognition/       # AI recognition system
│   ├── system.py           # CNN model (now working!)
│   ├── part_generator.py   # Auto-generation (now working!)
│   └── ...
└── web_output/             # Your generated files go here
    └── project_*/
        └── individual_books/
            ├── Trombone_1.pdf
            ├── C_Flute_2.pdf  ← Auto-generated!
            └── ...
```

---

## Testing the Installation

### Quick Test:

1. **Open browser:** http://localhost:8000

2. **Check System Status panel:**
   - Should show "FULL MODE ✅"
   - PyTorch should show "✅ v2.0.0"
   - OpenCV should show "✅ v4.8.0"

3. **Click "Show Detailed Specifications":**
   - All modules should show green dots ●
   - "Real Music Recognition" should be ✅
   - Should list 10 generated parts

### Full Test:

1. Create a project: "Test Project"
2. Upload a sample PDF (or use demo PDF)
3. Choose options (all checked)
4. Click "Start Processing"
5. Watch progress bar (should show real processing stages)
6. Download generated files

---

## Upgrading Later

Already have an older version installed?

```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Or specific package
pip install --upgrade torch
```

---

## Uninstalling

To remove everything:

```bash
# Uninstall packages
pip uninstall -r requirements.txt -y

# Remove generated files
rm -rf web_output/
rm -rf web_uploads/
```

---

## Performance Tips

### For Faster Processing:

1. **Use GPU** (if available):
   - Install CUDA-enabled PyTorch
   - 10-100x faster recognition

2. **Increase RAM** (if possible):
   - 16GB+ recommended for large collections
   - Enables parallel processing

3. **Use SSD** (vs HDD):
   - Faster file I/O
   - Quicker PDF reading

### For Lower Memory:

1. **Process fewer files at once**
2. **Disable song extraction** (if not needed)
3. **Close other applications**

---

## Getting Help

**Installation Issues:**
- Check Python version: `python --version`
- Check disk space: `df -h`
- Check pip version: `pip --version`

**Runtime Issues:**
- Check web console (F12 in browser)
- Check server logs (terminal output)
- Verify system specs (in web interface)

**Recognition Issues:**
- Check CUDA status (if using GPU)
- Verify PyTorch installed: `python -c "import torch"`
- Check memory usage

---

## Summary

**What you installed:**
- ✅ PyTorch 2.0+ (AI framework)
- ✅ Full music recognition system
- ✅ Complete web application
- ✅ All 10 auto-generation capabilities

**Total download:** ~2.5 GB
**Total disk space:** ~4 GB
**Installation time:** 5-30 minutes

**Result:**
Fully functional music recognition system with beautiful web interface!

---

## Next Steps

1. **Start the web app:**
   ```bash
   cd web_app && python server.py
   ```

2. **Open browser:** http://localhost:8000

3. **Upload your music:** Drag and drop 12 PDFs

4. **Process:** Click "Start Processing"

5. **Download:** Get 22-27 generated part books!

---

**Welcome to real music recognition!** 🎵🎶🎼

You're now ready to digitize your handwritten music collection!
