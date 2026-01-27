# Staff Detection Fix - Proper 5-Line Staff Recognition

## The Problem

The staff detector was incorrectly counting individual staff lines (the 5 horizontal lines) as separate staves instead of grouping them together into one staff.

**What was happening:**
- ❌ Each individual line counted as a "staff"
- ❌ A single musical staff (5 lines) was being split into 5 separate "staves"
- ❌ Line spacing wasn't consistent across staves
- ❌ The algorithm accepted any group of 4+ lines

**What should happen:**
- ✅ One musical staff = exactly 5 horizontal lines
- ✅ Lines should be evenly spaced within each staff
- ✅ Multiple staves should be detected separately

---

## The Fix

### What Changed

1. **Require exactly 5 lines per staff**
   - Old: Accepted 4+ lines (`if len(current_group) >= 4`)
   - New: Requires exactly 5 lines (`if len(current_group) == 5`)

2. **Validate line spacing**
   - New: Checks that all 5 lines are evenly spaced
   - New: Rejects groups with inconsistent spacing
   - New: Allows ±50% variance in spacing for real-world images

3. **Interpolation for missed lines**
   - New: If only 4 lines detected, calculates where 5th should be
   - New: Adds interpolated line at expected position

4. **Better grouping logic**
   - New: Maximum spacing threshold of 2.5× expected spacing
   - New: Prevents mixing lines from different staves

---

## How to Apply the Fix

### Step 1: Get the Fixed Code

```bash
cd ~/GitHub/VS-Code
git pull origin claude/handwritten-music-llm-qDHLY
```

### Step 2: Test the Fix (Optional but Recommended)

```bash
python3.11 test_staff_detection.py
```

You should see:
```
✅ ALL TESTS PASSED!
   - Detected correct number of staves
   - Each staff has exactly 5 lines
   - Line spacing is consistent
```

### Step 3: Restart Your Server

```bash
bash restart-server.sh
```

### Step 4: Process Your Files Again

1. Go to `http://localhost:8000`
2. Create a new project
3. Upload your 12 PDFs
4. Process them

Now each staff should be correctly recognized as 5 lines!

---

## Technical Details

### Staff Detection Algorithm (Improved)

```python
def find_staff_positions(self, image):
    """
    A musical staff consists of EXACTLY 5 horizontal lines.
    
    Steps:
    1. Detect all horizontal lines in the image
    2. Group lines that are close together (< 2.5× spacing)
    3. Validate groups have exactly 5 lines
    4. Verify consistent spacing within each group
    5. Return only validated staff groups
    """
```

### Spacing Validation

For each staff, the algorithm:
1. Calculates spacing between consecutive lines
2. Computes average spacing
3. Checks all spacings are within 50% of average
4. Rejects staves with inconsistent spacing

Example:
```
Staff with 5 lines at: [100, 120, 140, 160, 180]
Spacings: [20, 20, 20, 20]
Average: 20 pixels
Variance: 0 pixels
✅ Valid staff - consistent spacing
```

Bad example:
```
Staff with 5 lines at: [100, 105, 140, 145, 180]
Spacings: [5, 35, 5, 35]
Average: 20 pixels
Max variance: 15 pixels (75% of average)
❌ Invalid staff - inconsistent spacing
```

---

## What You'll See After the Fix

### Before (Broken):
```
Detected 60 staves
- Staff 1: 1 line at y=100
- Staff 2: 1 line at y=120
- Staff 3: 1 line at y=140
- Staff 4: 1 line at y=160
- Staff 5: 1 line at y=180
... (60 total individual lines counted as staves)
```

### After (Fixed):
```
Detected 12 staves
- Staff 1: 5 lines at [100, 120, 140, 160, 180]
- Staff 2: 5 lines at [300, 320, 340, 360, 380]
- Staff 3: 5 lines at [500, 520, 540, 560, 580]
... (12 actual musical staves)
```

---

## Configuration Options

If you need to adjust the detection (for unusual sheet music):

### Staff Line Thickness
```python
detector = StaffDetector(staff_line_thickness=3)  # For thicker lines
```

### Staff Space Height
```python
detector = StaffDetector(staff_space_height=15)  # For larger spacing
```

Default values:
- `staff_line_thickness = 2` pixels
- `staff_space_height = 10` pixels

---

## Testing Your Own Images

To test staff detection on your actual PDFs:

```python
from music_recognition.preprocessing import StaffDetector, ImagePreprocessor
import cv2

# Load your image
image = cv2.imread('your_sheet_music.jpg', cv2.IMREAD_GRAYSCALE)

# Preprocess
preprocessor = ImagePreprocessor()
processed = preprocessor.preprocess_array(image)

# Detect staves
detector = StaffDetector()
staves = detector.find_staff_positions(processed)

print(f"Detected {len(staves)} staves")
for i, staff in enumerate(staves, 1):
    print(f"Staff {i}: {len(staff)} lines at {staff}")
```

---

## Troubleshooting

### "Still detecting too many staves"

Your images might have very thin staff lines. Try:
```python
detector = StaffDetector(staff_line_thickness=1, staff_space_height=8)
```

### "Not detecting all staves"

Your images might have thicker lines or wider spacing. Try:
```python
detector = StaffDetector(staff_line_thickness=3, staff_space_height=15)
```

### "Some staves have wrong number of lines"

Check the image quality:
- Make sure the image is high resolution (300+ DPI)
- Ensure staff lines are clearly visible
- Check that lines aren't broken or faded

---

## Summary

✅ **Fixed Issues:**
- Individual staff lines no longer counted as separate staves
- Each staff now properly contains exactly 5 lines
- Line spacing is validated for consistency
- Better handling of imperfect line detection

✅ **Result:**
- Correct staff count for your sheet music
- Proper grouping of 5 lines per staff
- More reliable music recognition
- Consistent output across all instruments

---

Pull the latest code and restart your server to use the fix! 🎵
