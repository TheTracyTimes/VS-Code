# Part Generation Specification

This document specifies exactly which parts are handwritten (uploaded) and which parts are automatically generated.

---

## 📤 Parts Already Made (Handwritten) - 18 Parts

These parts will be **uploaded** as PDFs:

### Woodwinds (9 parts):
1. **C Flute 1**
2. **Bb Clarinet 1**
3. **Bb Clarinet 2**
4. **Bb Clarinet 3**
5. **Bb Bass Clarinet**
6. **Eb Alto Saxophone 1**
7. **Eb Alto Saxophone 2**
8. **Eb Alto Saxophone 3**
9. **Bb Tenor Saxophone**
10. **Bb Soprano Saxophone**

### Brass (7 parts):
11. **Bb Trumpet 1**
12. **Bb Trumpet 2**
13. **Bb Trumpet 3**
14. **F French Horn**

### Low Brass (4 parts):
15. **C Trombone 1**
16. **C Trombone 2**
17. **C Baritone BC** (Bass Clef)
18. **Bb Baritone TC** (Treble Clef)

**Total: 18 handwritten parts to upload**

---

## 🤖 Parts to be Generated - 10 Parts

These parts will be **automatically created** by the system:

### 1. Eb Alto Clarinet
**Source:** Eb Alto Saxophone 3
**Method:** Copy and adjust to Alto Clarinet range
**Why:** Both are Eb instruments, so transposition is the same
**Range:** Eb Alto Clarinet range

### 2. C Flute 2
**Sources:** 
- Bb Clarinet 2
- Bb Trumpet 2
- Eb Alto Saxophone 2

**Method:** 
1. Transpose all sources to concert pitch (C)
2. Merge by selecting most active measures
3. Adjust to C Flute range (C4-C7)

**Note:** Does NOT include Trombone 2

### 3. C Flute 3
**Sources:**
- Bb Clarinet 3
- Bb Trumpet 3
- Eb Alto Saxophone 3

**Method:**
1. Transpose all sources to concert pitch (C)
2. Merge by selecting most active measures
3. Adjust to C Flute range (C4-C7)

### 4. Viola
**Source:** C Flute 3 (generated part)
**Method:** Copy and shift down one octave
**Clef:** Treble clef
**Range:** One octave below Flute 3

### 5. Violin
**Source:** C Flute 1 (handwritten part)
**Method:** Copy and shift down one octave
**Clef:** Treble clef
**Range:** One octave below Flute 1

### 6. Cello
**Source:** C Trombone 1 (handwritten part)
**Method:** Copy directly (same range)
**Clef:** Bass clef
**Why:** Trombone 1 and Cello have similar range and role

### 7. Oboe
**Source:** C Flute 2 (generated part)
**Method:** Copy directly (same as Flute 2)
**Clef:** Treble clef
**Why:** Oboe and Flute 2 play similar melodic lines

### 8. Bassoon
**Source:** C Trombone 2 (handwritten part)
**Method:** Copy directly (same range)
**Clef:** Bass clef
**Why:** Bassoon and Trombone 2 have similar range and role

### 9. Tuba
**Source:** C Baritone BC (handwritten part)
**Method:** Copy and shift down one octave
**Clef:** Bass clef
**Range:** One octave below Baritone

### 10. Eb Baritone Saxophone
**Sources:**
- Bb Baritone TC (handwritten)
- C Baritone BC (handwritten)
- C Trombone 1 (handwritten)
- C Trombone 2 (handwritten)

**Method:**
1. Transpose all sources to concert pitch
2. Merge by selecting most active measures
3. Adjust to Baritone Sax range (D2-A4)
4. Set treble clef

**Total: 10 automatically generated parts**

---

## 📊 Complete Final Part List

When processing is complete, you will have **28 total parts**:

### Woodwinds (13):
- C Flute 1 *(uploaded)*
- C Flute 2 *(generated)*
- C Flute 3 *(generated)*
- Oboe *(generated)*
- Bb Soprano Saxophone *(uploaded)*
- Eb Alto Saxophone 1 *(uploaded)*
- Eb Alto Saxophone 2 *(uploaded)*
- Eb Alto Saxophone 3 *(uploaded)*
- Bb Tenor Saxophone *(uploaded)*
- Eb Baritone Saxophone *(generated)*
- Bb Clarinet 1 *(uploaded)*
- Bb Clarinet 2 *(uploaded)*
- Bb Clarinet 3 *(uploaded)*
- Eb Alto Clarinet *(generated)*
- Bb Bass Clarinet *(uploaded)*

### Brass (7):
- Bb Trumpet 1 *(uploaded)*
- Bb Trumpet 2 *(uploaded)*
- Bb Trumpet 3 *(uploaded)*
- F French Horn *(uploaded)*
- C Trombone 1 *(uploaded)*
- C Trombone 2 *(uploaded)*
- C Baritone BC *(uploaded)*
- Bb Baritone TC *(uploaded)*
- Tuba *(generated)*

### Strings (3):
- Violin *(generated)*
- Viola *(generated)*
- Cello *(generated)*

### Woodwind Doubles (1):
- Bassoon *(generated)*

**Grand Total: 28 parts** (18 uploaded + 10 generated)

---

## 🎵 Generation Flow Chart

```
Uploaded Parts (18)
    ↓
    ├─→ Eb Alto Sax 3 ────────→ Eb Alto Clarinet
    │
    ├─→ Clarinet 2 + Trumpet 2 + Alto Sax 2 ─→ C Flute 2 ─→ Oboe
    │
    ├─→ Clarinet 3 + Trumpet 3 + Alto Sax 3 ─→ C Flute 3 ─→ Viola (octave down)
    │
    ├─→ C Flute 1 ─────────────→ Violin (octave down)
    │
    ├─→ C Trombone 1 ───────────→ Cello (copy)
    │
    ├─→ C Trombone 2 ───────────→ Bassoon (copy)
    │
    ├─→ C Baritone BC ──────────→ Tuba (octave down)
    │
    └─→ Bb Baritone TC + C Baritone BC + 
        C Trombone 1 + C Trombone 2 ─→ Eb Baritone Sax
```

---

## ⚙️ Technical Details

### Transposition Process

**For Bb instruments (Clarinet, Trumpet, Tenor Sax, Baritone TC):**
- Written pitch transposes down a major 2nd to concert pitch
- Example: Written C = Concert Bb

**For Eb instruments (Alto Sax, Baritone Sax, Alto Clarinet):**
- Written pitch transposes down a major 6th to concert pitch
- Example: Written C = Concert Eb

**For C instruments (Flute, Trombone, Baritone BC, Tuba):**
- No transposition needed
- Written pitch = Concert pitch

### Merging Algorithm

When multiple parts are merged (Flute 2, Flute 3, Baritone Sax):

1. **Convert to concert pitch** - All sources transposed to C
2. **Analyze each measure** - Find which part is most active
3. **Select best melody** - Choose most melodically interesting line
4. **Adjust range** - Transpose octaves to fit target instrument
5. **Set clef** - Assign appropriate clef for instrument

### Range Adjustment

Each instrument has a specific playable range:
- **C Flute:** C4 to C7
- **Eb Alto Clarinet:** G3 to E6
- **Eb Baritone Sax:** D2 to A4
- **Viola:** C3 to E6
- **Violin:** G3 to E7
- **Cello:** C2 to C5
- **Tuba:** E1 to F4

Notes outside the range are automatically transposed by octaves.

---

## ✅ Verification Checklist

After processing, verify you have:

- [ ] 18 uploaded parts recognized correctly
- [ ] 10 generated parts created successfully
- [ ] 28 total individual part PDFs
- [ ] Each part has proper clef and key signature
- [ ] Transpositions are correct for each instrument
- [ ] All parts are in playable range

---

## 🎯 Summary

**Upload:** 18 handwritten parts
**Generate:** 10 derived parts automatically
**Result:** 28 complete instrumental parts ready for your church band

All generation happens automatically during processing - no manual work needed! 🎵
