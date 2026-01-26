#!/usr/bin/env python3.11
"""
Diagnostic script to check Python environment
"""

import sys
print("=" * 60)
print("Python Environment Diagnostic")
print("=" * 60)
print(f"\nPython version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Python path: {sys.path}")

print("\n" + "=" * 60)
print("Checking PyTorch...")
print("=" * 60)
try:
    import torch
    print(f"✅ PyTorch installed: {torch.__version__}")
    print(f"✅ CUDA available: {torch.cuda.is_available()}")
except ImportError as e:
    print(f"❌ PyTorch NOT found: {e}")

print("\n" + "=" * 60)
print("Checking other dependencies...")
print("=" * 60)

modules = {
    'opencv-python': 'cv2',
    'numpy': 'numpy',
    'fastapi': 'fastapi',
    'reportlab': 'reportlab',
    'music21': 'music21',
    'psutil': 'psutil'
}

for name, import_name in modules.items():
    try:
        mod = __import__(import_name)
        version = getattr(mod, '__version__', 'unknown')
        print(f"✅ {name}: {version}")
    except ImportError:
        print(f"❌ {name}: NOT FOUND")

print("\n" + "=" * 60)
print("Checking music_recognition module...")
print("=" * 60)

# Add VS-Code to path
import os
vs_code_path = os.path.dirname(os.path.abspath(__file__))
if vs_code_path not in sys.path:
    sys.path.insert(0, vs_code_path)

try:
    from music_recognition import preprocessing
    print("✅ music_recognition.preprocessing imports OK")
except ImportError as e:
    print(f"❌ music_recognition.preprocessing failed: {e}")

try:
    from music_recognition import models
    print("✅ music_recognition.models imports OK")
except ImportError as e:
    print(f"❌ music_recognition.models failed: {e}")

try:
    from music_recognition import postprocessing
    print("✅ music_recognition.postprocessing imports OK")
except ImportError as e:
    print(f"❌ music_recognition.postprocessing failed: {e}")

try:
    from music_recognition import system
    print("✅ music_recognition.system imports OK")
except ImportError as e:
    print(f"❌ music_recognition.system failed: {e}")

try:
    from music_recognition import MusicRecognitionSystem
    print("✅ MusicRecognitionSystem can be imported!")
    print("\n🎉 FULL MODE SHOULD WORK!")
except ImportError as e:
    print(f"❌ MusicRecognitionSystem failed: {e}")
    print("\n⚠️  WILL RUN IN DEMO MODE")

print("\n" + "=" * 60)
