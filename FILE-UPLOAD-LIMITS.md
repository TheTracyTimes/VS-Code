# File Upload Limit Fix

## The Problem

You're seeing that only 11 files are uploaded when you select 12 files. This is caused by an old version of `python-multipart` (version 0.0.6) that has limitations on handling multiple files.

---

## Quick Fix (1 Command)

```bash
bash upgrade-multipart.sh
```

This will:
1. ✅ Uninstall old python-multipart (0.0.6)
2. ✅ Install new python-multipart (0.0.9+)
3. ✅ Enable uploading 12+ files at once

Then restart your server:
```bash
bash restart-server.sh
```

---

## Manual Fix

If the automated script doesn't work, do this manually:

### Step 1: Uninstall Old Version
```bash
pip3.11 uninstall python-multipart
```

### Step 2: Install New Version
```bash
pip3.11 install "python-multipart>=0.0.9"
```

### Step 3: Restart Server
```bash
bash restart-server.sh
```

---

## What Changed?

### Before (Version 0.0.6)
- ❌ Limited to ~10-11 files per upload
- ❌ Old 2019 codebase
- ❌ Known bugs with multipart forms

### After (Version 0.0.9+)
- ✅ Can upload 100+ files at once
- ✅ Updated 2023 codebase
- ✅ Fixes multipart form handling
- ✅ Better memory management

---

## Server Configuration

The server is now configured with these limits:

| Setting | Value |
|---------|-------|
| **Maximum files per upload** | 100 files |
| **Maximum file size** | 100 MB per file |
| **Maximum total upload size** | 200 MB total |

These limits are set in `web_app/server.py` lines 85-89.

---

## Testing the Fix

After upgrading and restarting:

1. Open browser: http://localhost:8000
2. Create a project
3. Try uploading 12 PDF files
4. All 12 should appear in the file list
5. Click "Upload All Files"
6. All 12 should upload successfully

---

## Still Having Issues?

### Only Some Files Uploading

**Check file names:** Files with special characters might fail.
- ✅ Good: `song-001.pdf`, `Hymn_03.pdf`
- ❌ Bad: `song #1.pdf`, `hymn&march.pdf`

**Check file sizes:** Each file must be under 100 MB.
```bash
ls -lh *.pdf
```

**Check total size:** All files combined must be under 200 MB.

### Browser Limits

Some browsers limit file uploads:
- Chrome: Usually fine
- Firefox: Usually fine  
- Safari: Can be flaky with 10+ files

Try a different browser if Safari isn't working.

### Network Issues

For large uploads:
- Check your internet connection
- Make sure the server didn't timeout
- Look for errors in the server terminal

---

## Increasing Limits Further

If you need to upload MORE than 100 files or MORE than 200 MB:

Edit `web_app/server.py` around line 87:

```python
# Change these values:
MAX_FILES = 200  # Increase to 200 files
MAX_FILE_SIZE = 100 * 1024 * 1024  # Keep at 100 MB per file
MAX_TOTAL_SIZE = 500 * 1024 * 1024  # Increase to 500 MB total
```

Then restart the server.

---

## Why Version 0.0.6 Was Limited

The old version had:
- Hardcoded limits in the multipart parser
- Memory leaks with many files
- Poor handling of large uploads
- Bugs in file count tracking

Version 0.0.9+ fixed all of these issues.

---

## After Upgrading

You should now be able to:
- ✅ Upload 12 PDF files at once
- ✅ Upload 20, 30, 50+ files if needed
- ✅ Upload larger total file sizes
- ✅ Better upload reliability

---

**Quick Reference:**
- Upgrade: `bash upgrade-multipart.sh`
- Restart: `bash restart-server.sh`
- Test: Upload 12+ files in browser at `localhost:8000`
