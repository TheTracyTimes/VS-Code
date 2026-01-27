# Clef and Key Signature Reference Guide

## Overview

This document explains how clefs and key signatures are properly handled for all generated instrument parts in the handwritten music recognition system.

---

## Generated Parts Clef Assignments

### Treble Clef (G Clef) - 7 Parts
| Instrument | Clef | Symbol | Reason |
|------------|------|--------|--------|
| **Viola** | G (Treble) | 𝄞 | Modern band arrangement standard (not alto clef) |
| **Violin** | G (Treble) | 𝄞 | Standard violin clef |
| **Flute 2** | G (Treble) | 𝄞 | Standard flute clef |
| **Flute 3** | G (Treble) | 𝄞 | Standard flute clef |
| **Oboe** | G (Treble) | 𝄞 | Standard oboe clef |
| **Alto Clarinet** | G (Treble) | 𝄞 | Standard clarinet clef (Eb transposing) |
| **Baritone Sax** | G (Treble) | 𝄞 | Standard sax clef (Eb transposing) |

### Bass Clef (F Clef) - 3 Parts
| Instrument | Clef | Symbol | Reason |
|------------|------|--------|--------|
| **Cello** | F (Bass) | 𝄢 | Standard cello clef (can use tenor for high passages) |
| **Bassoon** | F (Bass) | 𝄢 | Standard bassoon clef (can use tenor for high passages) |
| **Tuba** | F (Bass) | 𝄢 | Standard tuba clef |

---

## Key Signature Placement

Key signatures must be placed differently depending on the clef to ensure proper readability and standard notation practice.

### Sharp Order (Same for All Clefs)
F# - C# - G# - D# - A# - E# - B#

### Flat Order (Same for All Clefs)
Bb - Eb - Ab - Db - Gb - Cb - Fb

### Treble Clef (G) Sharp Positions

```
Key Signature: G Major (1 sharp - F#)
═════════════════════
          ♯
═════════════════════  (F line - 5th position)

═════════════════════

═════════════════════

Key Signature: D Major (2 sharps - F#, C#)
═════════════════════
          ♯           (F line - 5th position)
═════════════════════
             ♯        (C space - 3rd position)
═════════════════════

═════════════════════
```

**Treble Clef Sharp Positions:** [5, 3, 6, 4, 2, 5, 3]
- F# on line 5
- C# on space 3
- G# on line 6 (above staff)
- D# on space 4
- A# on space 2
- E# on line 5
- B# on space 3

### Bass Clef (F) Sharp Positions

```
Key Signature: G Major (1 sharp - F#)
═════════════════════

═════════════════════  (F space - 4th position)
          ♯
═════════════════════

═════════════════════

Key Signature: D Major (2 sharps - F#, C#)
═════════════════════

═════════════════════  (F space - 4th position)
          ♯
═════════════════════  (C space - 2nd position)
             ♯
═════════════════════
```

**Bass Clef Sharp Positions:** [4, 2, 5, 3, 1, 4, 2]
- F# on space 4
- C# on space 2
- G# on line 5 (top)
- D# on space 3
- A# on line 1 (bottom)
- E# on space 4
- B# on space 2

### Treble Clef (G) Flat Positions

```
Key Signature: F Major (1 flat - Bb)
═════════════════════

═════════════════════  (B line - 3rd position)
          ♭
═════════════════════

═════════════════════

Key Signature: Bb Major (2 flats - Bb, Eb)
═════════════════════

═════════════════════  (B line - 3rd position)
          ♭
═════════════════════

═════════════════════  (E line - 5th position)
             ♭
```

**Treble Clef Flat Positions:** [3, 5, 3, 6, 4, 2, 4]
- Bb on line 3
- Eb on line 5 (top)
- Ab on line 3
- Db on space 6 (above staff)
- Gb on space 4
- Cb on space 2
- Fb on space 4

### Bass Clef (F) Flat Positions

```
Key Signature: F Major (1 flat - Bb)
═════════════════════  (B space - 2nd position)
             ♭
═════════════════════

═════════════════════

═════════════════════

Key Signature: Bb Major (2 flats - Bb, Eb)
═════════════════════  (B space - 2nd position)
             ♭
═════════════════════

═════════════════════  (E space - 4th position)
          ♭
═════════════════════
```

**Bass Clef Flat Positions:** [2, 4, 1, 3, 1, 3, 1]
- Bb on space 2
- Eb on space 4
- Ab on line 1 (bottom)
- Db on space 3
- Gb on line 1
- Cb on space 3
- Fb on line 1

---

## Key Signature Transposition

When transposing music for different instruments, the key signature must be adjusted accordingly:

### Transposing Instruments:

| Instrument | Transposition | Example |
|------------|---------------|---------|
| **Baritone Sax (Eb)** | Up major 6th | Concert C → Written A |
| **Alto Clarinet (Eb)** | Up major 6th | Concert C → Written A |

### Concert Pitch Instruments:

| Instrument | Transposition | Example |
|------------|---------------|---------|
| Viola | None (C instrument) | Concert C → Written C |
| Violin | None (C instrument) | Concert C → Written C |
| Cello | None (C instrument) | Concert C → Written C |
| Bassoon | None (C instrument) | Concert C → Written C |
| Tuba | None (C instrument) | Concert C → Written C |
| Flute 2 | None (C instrument) | Concert C → Written C |
| Flute 3 | None (C instrument) | Concert C → Written C |
| Oboe | None (C instrument) | Concert C → Written C |

---

## Implementation Details

### ClefReference Class (music_recognition/clef_reference.py)

Provides:
- Clef information (symbol, middle C position, etc.)
- Key signature positions for each clef
- Note position calculation on staff
- Transposition helpers

### Key Methods:

```python
# Get clef information
clef_info = ClefReference.get_clef_info('G')  # Treble clef

# Get key signature positions
positions = ClefReference.get_key_signature_positions('G', '2#')  # D major in treble

# Calculate note position on staff
position = ClefReference.get_note_position_on_staff('C4', 'G')  # Middle C in treble
```

### Book Processor Integration (music_recognition/book_processor.py)

The book processor now:
1. Uses `ClefReference` for accurate clef drawing
2. Draws key signatures with proper vertical placement
3. Ensures clef and key signature appear at the start of each system
4. Accounts for key signature width when positioning measures

---

## Examples

### Example 1: D Major in Treble Clef

```
Clef: Treble (G)
Key: D Major (2 sharps: F#, C#)

═════════════════════
𝄞     ♯
═════════════════════
         ♯
═════════════════════

═════════════════════

═════════════════════
```

### Example 2: D Major in Bass Clef

```
Clef: Bass (F)
Key: D Major (2 sharps: F#, C#)

═════════════════════

═════════════════════
𝄢     ♯
═════════════════════
         ♯
═════════════════════

═════════════════════
```

### Example 3: Bb Major in Treble Clef

```
Clef: Treble (G)
Key: Bb Major (2 flats: Bb, Eb)

═════════════════════
𝄞             ♭    (Eb on top line)
═════════════════════
         ♭           (Bb on middle line)
═════════════════════

═════════════════════

═════════════════════
```

### Example 4: Bb Major in Bass Clef

```
Clef: Bass (F)
Key: Bb Major (2 flats: Bb, Eb)

═════════════════════
          ♭          (Eb on 4th space)
═════════════════════
𝄢
═════════════════════
         ♭           (Bb on 2nd space)
═════════════════════

═════════════════════
```

---

## Verification Checklist

When generating parts, verify:

- [ ] Correct clef assigned (G for treble, F for bass)
- [ ] Key signature sharps/flats in proper vertical positions
- [ ] Key signature order correct (F-C-G-D-A-E-B for sharps, B-E-A-D-G-C-F for flats)
- [ ] Transposing instruments have correct written key (Eb instruments)
- [ ] Clef and key signature appear at start of each system
- [ ] Notes positioned correctly relative to clef
- [ ] Accidentals (sharps/flats in notes) correctly placed

---

## References

- Standard Music Notation (Elaine Gould - "Behind Bars")
- Clef positioning standards (Boosey & Hawkes)
- Key signature conventions (music21 library documentation)

---

## Code Files

- `music_recognition/clef_reference.py` - Clef and key signature reference system
- `music_recognition/book_processor.py` - PDF generation with proper notation
- `music_recognition/part_generator.py` - Part generation with correct clefs assigned

---

**Last Updated:** January 2026
**Version:** 1.0
