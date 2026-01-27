#!/usr/bin/env python3
"""
Verification script to check if all necessary files are present.
Run this to see what files are missing from your installation.
"""

import os
import sys
from pathlib import Path

# Get the VS-Code directory
vs_code_dir = Path(__file__).parent.absolute()

print("=" * 70)
print("INSTALLATION VERIFICATION")
print("=" * 70)
print(f"\nChecking directory: {vs_code_dir}")
print()

# Define all required files
required_files = {
    "Core Python Scripts": [
        "diagnostic.py",
        "diagnostic_advanced.py",
        "demo.py",
        "dataset.py",
        "evaluate.py",
        "example.py",
    ],
    "Installation Scripts": [
        "install-lite.sh",
        "install-lite.bat",
        "install-full.sh",
        "install-full.bat",
    ],
    "Documentation": [
        "SIMPLE-SETUP.md",
        "CHEAT-SHEET.md",
        "FULL-INSTALLATION.md",
        "README.md",
    ],
    "Requirements": [
        "requirements.txt",
        "requirements-lite.txt",
    ],
    "Music Recognition - Core Files": [
        "music_recognition/__init__.py",
        "music_recognition/system.py",
        "music_recognition/instruments.py",
        "music_recognition/transposition.py",
        "music_recognition/part_generator.py",
        "music_recognition/multipart_score.py",
        "music_recognition/pdf_export.py",
        "music_recognition/pdf_reader.py",
        "music_recognition/score_layout.py",
        "music_recognition/staff_paper.py",
        "music_recognition/table_of_contents.py",
        "music_recognition/title_extraction.py",
        "music_recognition/individual_books.py",
        "music_recognition/song_extraction.py",
        "music_recognition/song_index.py",
        "music_recognition/part_grouping.py",
    ],
    "Music Recognition - Preprocessing": [
        "music_recognition/preprocessing/__init__.py",
        "music_recognition/preprocessing/image_processor.py",
        "music_recognition/preprocessing/staff_detector.py",
    ],
    "Music Recognition - Models": [
        "music_recognition/models/__init__.py",
        "music_recognition/models/cnn_classifier.py",
        "music_recognition/models/symbol_detector.py",
    ],
    "Music Recognition - Postprocessing": [
        "music_recognition/postprocessing/__init__.py",
        "music_recognition/postprocessing/notation_converter.py",
    ],
    "Web Application": [
        "web_app/server.py",
        "web_app/static/index.html",
        "web_app/static/styles.css",
        "web_app/static/app.js",
    ],
}

# Check each category
total_files = 0
missing_files = 0
missing_list = []

for category, files in required_files.items():
    print(f"\n{category}:")
    print("-" * 70)

    category_missing = []
    for file_path in files:
        total_files += 1
        full_path = vs_code_dir / file_path

        if full_path.exists():
            size = full_path.stat().st_size
            print(f"  ✅ {file_path} ({size:,} bytes)")
        else:
            print(f"  ❌ {file_path} - MISSING!")
            missing_files += 1
            category_missing.append(file_path)

    if category_missing:
        missing_list.extend(category_missing)

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Total files checked: {total_files}")
print(f"Files present: {total_files - missing_files}")
print(f"Files missing: {missing_files}")

if missing_files > 0:
    print("\n" + "=" * 70)
    print("⚠️  MISSING FILES DETECTED")
    print("=" * 70)
    print(f"\nYou are missing {missing_files} critical files!")
    print("\nMissing files:")
    for file_path in missing_list:
        print(f"  - {file_path}")

    print("\n" + "=" * 70)
    print("HOW TO FIX")
    print("=" * 70)
    print("""
The files are in the Git repository but not on your computer.
Here's how to get them:

1. Make sure you're on the right branch:
   git branch

   You should see: * claude/handwritten-music-llm-qDHLY

2. If you're on a different branch, switch to it:
   git checkout claude/handwritten-music-llm-qDHLY

3. Pull the latest changes:
   git pull origin claude/handwritten-music-llm-qDHLY

4. If that doesn't work, try a hard reset (WARNING: loses local changes):
   git fetch origin
   git reset --hard origin/claude/handwritten-music-llm-qDHLY

5. Run this script again to verify:
   python3 verify_installation.py

If you're still having issues, the files might have been deleted locally.
Check your git status:
   git status

If files show as "deleted", restore them:
   git restore music_recognition/
""")

else:
    print("\n✅ All files are present!")
    print("\nYou can now:")
    print("  1. Run the lite installation: bash install-lite.sh")
    print("  2. Or run the full installation: bash install-full.sh")
    print("  3. Then start the server: cd web_app && python3.11 server.py")

print("\n" + "=" * 70)
