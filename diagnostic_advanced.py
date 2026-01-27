#!/usr/bin/env python3.11
"""
Advanced diagnostic to find the exact import issue
"""

import sys
import os

# Add VS-Code to path
vs_code_path = os.path.dirname(os.path.abspath(__file__))
if vs_code_path not in sys.path:
    sys.path.insert(0, vs_code_path)

print("=" * 60)
print("Advanced Import Diagnostic")
print("=" * 60)

print("\nStep 1: Test PyTorch directly")
print("-" * 60)
try:
    import torch
    print(f"✅ PyTorch: {torch.__version__}")
except Exception as e:
    print(f"❌ PyTorch failed: {e}")
    sys.exit(1)

print("\nStep 2: Test system.py imports directly")
print("-" * 60)

# Test if system.py can be imported bypassing __init__.py
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "system_test",
        "music_recognition/system.py"
    )
    system_module = importlib.util.module_from_spec(spec)

    print("Attempting to load system.py...")
    spec.loader.exec_module(system_module)
    print("✅ system.py loaded successfully!")
    print(f"✅ MusicRecognitionSystem class found: {hasattr(system_module, 'MusicRecognitionSystem')}")

except Exception as e:
    print(f"❌ system.py failed to load: {e}")
    import traceback
    traceback.print_exc()

print("\nStep 3: Check if system.py file exists")
print("-" * 60)
system_path = os.path.join(vs_code_path, "music_recognition", "system.py")
print(f"Looking for: {system_path}")
print(f"File exists: {os.path.exists(system_path)}")
if os.path.exists(system_path):
    print(f"File size: {os.path.getsize(system_path)} bytes")

print("\nStep 4: List all files in music_recognition/")
print("-" * 60)
music_rec_dir = os.path.join(vs_code_path, "music_recognition")
files = os.listdir(music_rec_dir)
print("Files found:")
for f in sorted(files):
    full_path = os.path.join(music_rec_dir, f)
    if os.path.isfile(full_path):
        print(f"  📄 {f}")
    else:
        print(f"  📁 {f}/")

print("\nStep 5: Try importing music_recognition package")
print("-" * 60)
try:
    import music_recognition
    print("✅ music_recognition package imported!")
    print(f"Package location: {music_recognition.__file__}")
    print(f"Package contents: {dir(music_recognition)}")
except Exception as e:
    print(f"❌ music_recognition package failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("DIAGNOSIS COMPLETE")
print("=" * 60)
