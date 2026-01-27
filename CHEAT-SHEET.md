# Music Recognition - Quick Reference Card

**Print this page and keep it handy!**

---

## 🚀 First Time Setup (Do Once)

### 1. Install Python
- Go to: **python.org/downloads**
- Click "Download Python"
- Run installer
- ✅ **Check "Add Python to PATH"**

### 2. Install the App

**Windows:**
```
install-lite.bat
```

**Mac:**
```
./install-lite.sh
```

---

## 🎵 Every Time You Use It

### 1. Start the Server

**Easy way (recommended):**
```
bash restart-server.sh
```

**Manual way:**

**Windows:**
```
cd web_app
python server.py
```

**Mac:**
```
cd web_app
python3.11 server.py
```

### 2. Open Browser

Type in address bar:
```
localhost:8000
```

### 3. When Done
Press `Ctrl + C` in the terminal (or run `bash kill-server.sh`)

---

## 📝 Quick Workflow

1. **Create Project** → Enter name
2. **Drag PDFs** → Into purple box
3. **Upload** → Click button
4. **Choose Options** → Check boxes
5. **Process** → Click "Start Processing"
6. **Download** → Click files when done

---

## ⚡ Common Commands

| What You Want | Command |
|---------------|---------|
| **First install** | `install-lite.bat` (Win) or `bash install-lite.sh` (Mac) |
| **Start app** | `cd web_app` then `python3.11 server.py` |
| **Restart app** | `bash restart-server.sh` |
| **Stop app** | `Ctrl + C` or `bash kill-server.sh` |
| **Open app** | Browser: `localhost:8000` |
| **Full install** | `install-full.bat` (Win) or `bash install-full.sh` (Mac) |
| **PDF support** | `bash install-pdf-support.sh` |
| **Check files** | `python3 verify_installation.py` |
| **Fix missing files** | `bash restore_files.sh` |
| **Test staff detection** | `python3.11 test_staff_detection.py` |
| **Upgrade multipart** | `bash upgrade-multipart.sh` |

---

## 🆘 Quick Fixes

| Problem | Solution |
|---------|----------|
| **"command not found"** | Mac: Use `python3.11` instead of `python` |
| **Won't install** | Check internet, try again |
| **Port 8000 in use** | Run `bash restart-server.sh` |
| **Page won't load** | Make sure terminal is still open |
| **Missing files** | Run `bash restore_files.sh` |
| **PDF not working** | Run `bash install-pdf-support.sh` |
| **Still DEMO mode** | Use `python3.11 server.py` not `python3` |

---

## 📁 Folder Structure

```
VS-Code/
  ├── install-lite.sh      ← Run this first time
  ├── web_app/
  │   └── server.py        ← Run this every time
  └── web_output/          ← Your files appear here
```

---

## 🎯 Remember These 3 Things

1. **Install once:** `install-lite.bat` or `./install-lite.sh`
2. **Run every time:** `cd web_app` then `python server.py`
3. **Open browser:** `localhost:8000`

---

**That's all you need to know!** 🎵
