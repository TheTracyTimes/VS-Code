# 🚀 Quick Start Guide

Get your music recognition web app running in **2 minutes**!

---

## Step 1: Choose Your Installation

You have **two options**:

### Option A: Quick Demo (Recommended to Start)
- **Size**: ~100MB
- **Time**: 2 minutes
- **What you get**: Web interface with sample files
- **Best for**: Seeing how it works before full install

### Option B: Full Install (For Real Processing)
- **Size**: ~2.5GB
- **Time**: 5-15 minutes
- **What you get**: Complete AI-powered music recognition
- **Best for**: Actually processing your handwritten music

---

## Step 2: Run the Installer

**On Mac/Linux:**
```bash
./install.sh
```

**On Windows:**
```bash
install.bat
```

The installer will ask which option you want. Choose `1` for Quick Demo or `2` for Full Install.

---

## Step 3: Start the Web App

**On Mac/Linux:**
```bash
cd web_app
./start.sh
```

**On Windows:**
```bash
cd web_app
start.bat
```

---

## Step 4: Open Your Browser

Go to: **http://localhost:8000**

You'll see a beautiful purple web interface! 🎨

---

## Using the Web App

### 1. Create a Project
- Enter project name: "God of Mercy Church Band Hymnal"
- Click "Create Project"

### 2. Upload Your PDFs
- Drag and drop all 12 PDF files
- Or click to browse
- Click "Upload All Files"

### 3. Configure Options
- ✅ Generate derived parts (Flute 2, Violin, etc.)
- ✅ Split combined parts (separate books)
- Click "Start Processing"

### 4. Watch Progress
- Real-time progress bar
- See what's happening at each stage

### 5. Download Results
- Click any file to download
- Get 22-27 individual part books

---

## What Gets Created?

### Quick Demo Mode:
- Sample PDF files showing the workflow
- Each file says "This is a demo file"
- Shows you exactly how the interface works

### Full Install Mode:
- Real digitization of your handwritten music
- 22-27 professional part books generated
- All derived parts automatically created

---

## Upgrading from Demo to Full

Already installed Quick Demo? Want real processing?

Just run the installer again and choose option 2:

```bash
./install.sh    # or install.bat on Windows
# Choose: 2
```

The web app will automatically switch to real processing mode!

---

## Dependencies Explained

### What's in Quick Demo (~100MB):
- **FastAPI** - Web framework
- **Uvicorn** - Web server
- **WebSockets** - Real-time updates
- **ReportLab** - PDF creation

### What's added in Full Install (~2.5GB):
- **PyTorch** (~2GB) - AI/machine learning
- **OpenCV** - Image processing
- **NumPy** - Numerical operations
- **music21** - Music notation handling
- **Various AI models** - For recognition

---

## Troubleshooting

### "Port already in use"
Change port in `web_app/server.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8080)  # Changed from 8000
```

### "Module not found" errors
Make sure you ran the installer:
```bash
./install.sh    # or install.bat
```

### "Demo mode" in console
This means Quick Demo is installed. To get real processing:
```bash
./install.sh    # Choose option 2
```

### Web app won't start
Check if Python 3.8+ is installed:
```bash
python3 --version
```

---

## System Requirements

### Minimum (Quick Demo):
- **OS**: Windows 10+, macOS 10.14+, Linux
- **Python**: 3.8 or higher
- **RAM**: 4GB
- **Disk**: 500MB free

### Recommended (Full Install):
- **OS**: Windows 10+, macOS 10.14+, Linux
- **Python**: 3.9 or higher
- **RAM**: 8GB (16GB for large collections)
- **Disk**: 5GB free
- **GPU**: Optional (CUDA-capable for faster processing)

---

## Next Steps

Once the web app is running:

1. **Try the demo** - Upload sample PDFs
2. **Read the documentation** - See `web_app/README.md`
3. **Customize options** - Split/combine parts as needed
4. **Process your collection** - Upload your 12 PDFs
5. **Download results** - Get all generated books

---

## Getting Help

- **Web App Issues**: Check `web_app/README.md`
- **Architecture Details**: See `WEB_APPLICATION_ARCHITECTURE.md`
- **Music Recognition**: See main project documentation
- **Quick Reference**: See `WEB_APP_QUICK_START.md`

---

## One-Liners for Each Option

### Super Quick Start (Demo Mode):
```bash
./install.sh && cd web_app && ./start.sh
# Choose: 1 when asked
# Then open: http://localhost:8000
```

### Full Install (Real Processing):
```bash
./install.sh && cd web_app && ./start.sh
# Choose: 2 when asked (downloads 2.5GB)
# Then open: http://localhost:8000
```

---

## Summary

**Quick Demo:**
```bash
./install.sh    # Choose 1
cd web_app && ./start.sh
# Open: http://localhost:8000
```

**Full Install:**
```bash
./install.sh    # Choose 2
cd web_app && ./start.sh
# Open: http://localhost:8000
```

That's it! Start digitizing music! 🎵🎶🎼
