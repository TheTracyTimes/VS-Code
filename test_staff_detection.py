#!/usr/bin/env python3.11
"""
Test script to verify staff detection is working correctly.
This will show how many staves are detected and verify each has 5 lines.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from music_recognition.preprocessing import StaffDetector, ImagePreprocessor
    import cv2
    import numpy as np
    
    print("=" * 70)
    print("STAFF DETECTION TEST")
    print("=" * 70)
    print()
    
    # Test with default parameters
    detector = StaffDetector(staff_line_thickness=2, staff_space_height=10)
    print("✅ StaffDetector initialized")
    print(f"   - Staff line thickness: {detector.staff_line_thickness} pixels")
    print(f"   - Staff space height: {detector.staff_space_height} pixels")
    print()
    
    # Create a test image with multiple staves
    print("Creating test image with 3 staves (15 lines total)...")
    height = 800
    width = 1000
    test_image = np.zeros((height, width), dtype=np.uint8)
    
    # Staff 1: Lines at y=100, 120, 140, 160, 180
    # Staff 2: Lines at y=300, 320, 340, 360, 380
    # Staff 3: Lines at y=500, 520, 540, 560, 580
    
    staff_positions = [
        [100, 120, 140, 160, 180],  # Staff 1
        [300, 320, 340, 360, 380],  # Staff 2
        [500, 520, 540, 560, 580],  # Staff 3
    ]
    
    for staff in staff_positions:
        for line_y in staff:
            cv2.line(test_image, (0, line_y), (width, line_y), 255, 2)
    
    print("✅ Test image created with 3 staves")
    print()
    
    # Detect staves
    print("Running staff detection...")
    detected_staves = detector.find_staff_positions(test_image)
    
    print()
    print("=" * 70)
    print("DETECTION RESULTS")
    print("=" * 70)
    print()
    print(f"Number of staves detected: {len(detected_staves)}")
    print()
    
    if len(detected_staves) == 3:
        print("✅ CORRECT: Detected 3 staves (expected 3)")
    else:
        print(f"❌ ERROR: Expected 3 staves, but detected {len(detected_staves)}")
    
    print()
    print("Staff details:")
    print("-" * 70)
    
    all_correct = True
    for i, staff in enumerate(detected_staves, 1):
        print(f"\nStaff {i}:")
        print(f"  Number of lines: {len(staff)}")
        
        if len(staff) == 5:
            print(f"  ✅ Correct: Has exactly 5 lines")
        else:
            print(f"  ❌ ERROR: Has {len(staff)} lines (should be 5)")
            all_correct = False
        
        print(f"  Line positions: {staff}")
        
        if len(staff) >= 2:
            spacings = [staff[i+1] - staff[i] for i in range(len(staff)-1)]
            avg_spacing = sum(spacings) / len(spacings)
            print(f"  Line spacings: {spacings}")
            print(f"  Average spacing: {avg_spacing:.1f} pixels")
            
            # Check consistency
            spacing_variance = max(abs(s - avg_spacing) for s in spacings)
            if spacing_variance < avg_spacing * 0.2:
                print(f"  ✅ Spacing is consistent (max variance: {spacing_variance:.1f}px)")
            else:
                print(f"  ⚠️  Spacing varies (max variance: {spacing_variance:.1f}px)")
    
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    
    if len(detected_staves) == 3 and all_correct and all(len(s) == 5 for s in detected_staves):
        print("✅ ALL TESTS PASSED!")
        print("   - Detected correct number of staves")
        print("   - Each staff has exactly 5 lines")
        print("   - Line spacing is consistent")
        print()
        print("The staff detection is working correctly!")
    else:
        print("❌ SOME TESTS FAILED")
        print()
        print("Issues found:")
        if len(detected_staves) != 3:
            print(f"  - Expected 3 staves, got {len(detected_staves)}")
        for i, staff in enumerate(detected_staves, 1):
            if len(staff) != 5:
                print(f"  - Staff {i} has {len(staff)} lines (should be 5)")
    
    print()
    print("=" * 70)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print()
    print("Make sure you have the required dependencies installed:")
    print("  pip3.11 install opencv-python numpy")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
