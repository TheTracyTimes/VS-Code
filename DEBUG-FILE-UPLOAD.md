# Debugging 11-File Upload Limit

## Steps to Debug

### Step 1: Check python-multipart Version

```bash
bash check-multipart-version.sh
```

**What you should see:**
```
✅ python-multipart is installed
   Version: 0.0.9 (or higher)
✅ Version is good (0.0.9+)
```

**If you see version 0.0.6 or lower:**
```bash
bash upgrade-multipart.sh
bash restart-server.sh
```

---

### Step 2: Check Browser Console

1. Open browser: `http://localhost:8000`
2. Press `F12` or right-click → "Inspect"
3. Click "Console" tab
4. Create a project and select your 12 files
5. Look for console messages:

**What you should see:**
```
Browser selected 12 files
After filtering for PDFs: 12 files
Files: [... list of 12 file names ...]
```

**If you see "Browser selected 11 files":**
- Your **browser** is limiting file selection (not the server)
- Try a different browser (Chrome, Firefox instead of Safari)
- Try selecting files differently (drag-drop vs click-to-browse)

**If you see "Browser selected 12 files" but only 11 upload:**
- The server is rejecting one file
- Check file sizes (one might be too large)
- Check server terminal for error messages

---

### Step 3: Check Server Terminal

When you click "Upload All Files", look at the server terminal window.

**What to look for:**
```
INFO:     127.0.0.1:12345 - "POST /api/projects/abc123/upload HTTP/1.1" 200 OK
```

**If you see errors:**
```
ERROR: Something about "multipart"
ERROR: Something about "file size"
ERROR: Something about "limit"
```

Copy the exact error message - it will tell us what's wrong!

---

### Step 4: Check File Sizes

```bash
ls -lh /path/to/your/pdfs/*.pdf
```

**Each file must be:**
- Under 100 MB
- A valid PDF file
- Not corrupt

**All files together must be:**
- Under 500 MB total

---

## Common Causes & Fixes

### Cause 1: Old python-multipart (0.0.6)
**Symptom:** Browser selects 12, but only 11 show in file list
**Fix:**
```bash
bash upgrade-multipart.sh
bash restart-server.sh
```

### Cause 2: Safari Browser Limitation
**Symptom:** Browser console shows "Browser selected 11 files"
**Fix:** Use Chrome or Firefox instead of Safari

### Cause 3: One File Is Too Large
**Symptom:** Browser selects 12, server receives 11
**Fix:** Check file sizes, compress large PDFs

### Cause 4: Server Not Restarted
**Symptom:** Upgraded multipart but still 11 files
**Fix:**
```bash
bash restart-server.sh
```
Make sure the old server is fully stopped first!

### Cause 5: Wrong Python Version Running Server
**Symptom:** Upgrade seemed to work but server still limited
**Fix:**
```bash
# Make sure you're using python3.11
cd web_app
python3.11 server.py

# Or use restart script which uses python3.11
bash restart-server.sh
```

---

## Testing the Fix

### Manual Test:

1. Stop server: `Ctrl + C`
2. Check version: `bash check-multipart-version.sh`
3. Start server: `bash restart-server.sh`
4. Open browser with console: `http://localhost:8000` + `F12`
5. Create project
6. Select 12 files
7. Check console: Should say "Browser selected 12 files"
8. Check file list: Should show all 12 files
9. Upload: Should upload all 12 files

### What Success Looks Like:

**Browser Console:**
```
Browser selected 12 files
After filtering for PDFs: 12 files
Files: ["file1.pdf", "file2.pdf", ..., "file12.pdf"]
```

**File List on Page:**
```
12 files shown:
✓ file1.pdf (2.5 MB) [Remove]
✓ file2.pdf (3.1 MB) [Remove]
...
✓ file12.pdf (1.8 MB) [Remove]
```

**Server Terminal:**
```
INFO: Uploaded 12 files
```

---

## Still Not Working?

### Try Different Browser

Safari has known issues with multiple file uploads.

**Try Chrome:**
```
1. Open Chrome
2. Go to localhost:8000
3. Select files
4. Check if all 12 appear
```

**Try Firefox:**
```
1. Open Firefox
2. Go to localhost:8000
3. Select files
4. Check if all 12 appear
```

### Try Drag & Drop

Instead of clicking "browse":
```
1. Open Finder window with your 12 PDFs
2. Select all 12 files
3. Drag them into the purple upload box
4. Drop them
5. Check if all 12 appear
```

### Check Server Is Using Python 3.11

```bash
# Stop server
Ctrl + C

# Check which python is running
which python3.11

# Explicitly start with python3.11
cd web_app
python3.11 server.py
```

### Nuclear Option: Full Reinstall

```bash
# Stop server
Ctrl + C

# Reinstall python-multipart
pip3.11 uninstall -y python-multipart
pip3.11 install "python-multipart>=0.0.9"

# Reinstall all requirements
pip3.11 install -r requirements.txt

# Restart server
bash restart-server.sh
```

---

## Report Back

If still not working, tell me:

1. **python-multipart version:**
   ```bash
   python3.11 -c "import multipart; print(multipart.__version__)"
   ```

2. **Browser console output:**
   - What does "Browser selected X files" say?

3. **How many files appear in the file list?**
   - 11, 12, or something else?

4. **What browser are you using?**
   - Chrome, Firefox, Safari, etc.

5. **Any errors in server terminal?**
   - Copy exact error messages

This info will help me figure out exactly what's blocking the 12th file!
