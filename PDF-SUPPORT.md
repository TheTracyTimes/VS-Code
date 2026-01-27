# PDF Support Installation

## Quick Fix

If you're seeing this error:
```
ImportError: pdf2image not installed. Install with: pip install pdf2image
```

Run this command:

```bash
bash install-pdf-support.sh
```

This automated script will:
1. ✅ Check if Poppler is installed
2. ✅ Install pdf2image and PyPDF2 Python packages
3. ✅ Verify everything works

---

## Manual Installation

### Step 1: Install Poppler (System Dependency)

pdf2image needs a system library called **Poppler** to convert PDFs to images.

**Mac:**
```bash
brew install poppler
```

**Ubuntu/Debian Linux:**
```bash
sudo apt-get update
sudo apt-get install poppler-utils
```

**Fedora/RedHat Linux:**
```bash
sudo dnf install poppler-utils
```

**Windows:**
1. Download from: https://github.com/oschwartz10612/poppler-windows/releases/
2. Extract to `C:\Program Files\poppler`
3. Add `C:\Program Files\poppler\Library\bin` to PATH

### Step 2: Install Python Packages

```bash
pip3.11 install pdf2image PyPDF2
```

Or use the standard pip if python3.11 is your default:
```bash
pip install pdf2image PyPDF2
```

### Step 3: Verify Installation

Test if it works:

```bash
python3.11 -c "from pdf2image import convert_from_path; print('✅ pdf2image works!')"
```

You should see: `✅ pdf2image works!`

---

## What These Packages Do

### pdf2image
- Converts PDF pages to images
- Needed for processing scanned sheet music PDFs
- Uses Poppler under the hood

### PyPDF2
- Reads PDF metadata
- Extracts page information
- Works with pdf2image for complete PDF handling

### Poppler
- System-level PDF rendering library
- Required by pdf2image
- Not a Python package - installed separately

---

## Troubleshooting

### "pdftoppm not found" Error

This means Poppler isn't installed or isn't in PATH.

**Mac:**
```bash
# Check if installed
which pdftoppm

# If not found, install
brew install poppler
```

**Linux:**
```bash
# Check if installed
which pdftoppm

# If not found, install
sudo apt-get install poppler-utils  # Ubuntu/Debian
```

### "command not found: brew" (Mac Only)

You need to install Homebrew first:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then install poppler:
```bash
brew install poppler
```

### Permission Denied

On Linux, you might need sudo:

```bash
sudo pip3.11 install pdf2image PyPDF2
```

Or use a virtual environment (recommended).

---

## Do I Really Need This?

**Yes, if you want to:**
- ✅ Upload PDF files to the web app
- ✅ Process scanned sheet music from PDF
- ✅ Extract individual pages from PDF books

**No, if you:**
- ❌ Only work with image files (PNG, JPG, etc.)
- ❌ Don't plan to upload PDFs

The system will work fine without PDF support - you just can't upload PDF files.

---

## After Installation

Once installed, restart your server:

```bash
cd web_app
python3.11 server.py
```

The PDF upload feature will now work in the web interface!

---

## Still Having Issues?

Check the diagnostic:

```bash
python3.11 diagnostic_advanced.py
```

Look for this section:
```
✅ pdf2image: <version>
✅ PyPDF2: <version>
```

If you see ❌ for either, the installation didn't work. Try the manual steps above.
