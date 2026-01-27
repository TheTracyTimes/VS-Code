# 🔧 Fix Missing Files

## The Problem

Your Mac is missing most of the `music_recognition/` files!

You currently have only these files:
- `music_recognition/__init__.py`
- `music_recognition/individual_books.py`
- `music_recognition/part_grouping.py`
- `music_recognition/song_extraction.py`
- `music_recognition/song_index.py`

But you should have **24 files total**, including the critical `system.py` that enables FULL MODE.

---

## Quick Fix (Recommended)

Run this command in your VS-Code directory:

```bash
python3 verify_installation.py
```

This will:
1. ✅ Check which files you're missing
2. ✅ Show you exactly what's wrong
3. ✅ Tell you how to fix it

---

## Manual Fix

If the verification script doesn't help, try these steps:

### Step 1: Check Your Branch
```bash
git branch
```

You should see: `* claude/handwritten-music-llm-qDHLY`

### Step 2: Pull Latest Changes
```bash
git pull origin claude/handwritten-music-llm-qDHLY
```

### Step 3: Check Git Status
```bash
git status
```

If you see files listed as "deleted", restore them:
```bash
git restore music_recognition/
```

### Step 4: Nuclear Option (If Nothing Else Works)

⚠️ **WARNING**: This will delete any local changes you haven't committed!

```bash
git fetch origin
git reset --hard origin/claude/handwritten-music-llm-qDHLY
```

---

## Verify It Worked

After trying the fix, run the verification script:

```bash
python3 verify_installation.py
```

You should see ✅ for all files!

Then run the diagnostic again:

```bash
python3.11 diagnostic_advanced.py
```

You should see:
- ✅ system.py loaded successfully!
- ✅ MusicRecognitionSystem class found: True

---

## What These Files Do

The missing files are CRITICAL for full music recognition:

- **system.py** - Main recognition system (needed for FULL MODE)
- **instruments.py** - Instrument configurations
- **transposition.py** - Music transposition
- **part_generator.py** - Automatic part generation
- **preprocessing/** - Image processing
- **models/** - AI/CNN models
- **postprocessing/** - Notation conversion

Without these, you can only run in DEMO MODE!

---

## Still Having Issues?

Run this to see what git thinks about your files:

```bash
git ls-files music_recognition/ | wc -l
```

Should show: **24 files**

If it shows less, something is wrong with your git checkout.

Try:
```bash
git checkout -- music_recognition/
```

---

## After Getting All Files

Once all files are present:

1. **Run full installation:**
   ```bash
   bash install-full.sh
   ```

2. **Start server with Python 3.11:**
   ```bash
   cd web_app
   python3.11 server.py
   ```

3. **Open browser:**
   ```
   localhost:8000
   ```

4. **You should see:**
   - ✅ **FULL MODE** badge
   - ✅ Real Music Recognition
   - ✅ Automatic Part Generation (10 parts)
   - ✅ Individual Song Extraction

---

**Good luck! 🎵**
