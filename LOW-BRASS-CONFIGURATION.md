# Low Brass Section - Complete Configuration

## 🎺 Your Low Brass Instrumentation

Your Low Brass section consists of **4 parts:**

1. **C Trombone 1** → Maps to **1st Trombone**
2. **C Trombone 2** → Maps to **2nd Trombone**
3. **C Baritone BC** → Maps to **C Baritone BC (Bass Clef)**
4. **Bb Baritone TC** → Maps to **Bb Baritone TC (Treble Clef)**

---

## 🎵 Critical Understanding: Baritone Instruments

### Two Different Instruments, Not Two Versions!

**Important:** The two baritone parts are **DIFFERENT instruments** with **DIFFERENT transpositions:**

#### C Baritone BC (Bass Clef)
- **Key:** C instrument (non-transposing)
- **Clef:** Bass clef
- **Reads:** Concert pitch
- **Transposition:** NONE
- **Example:** Written C sounds as C

#### Bb Baritone TC (Treble Clef)
- **Key:** Bb instrument (transposing)
- **Clef:** Treble clef
- **Reads:** Transposed notation
- **Transposition:** Down a major 2nd (whole step)
- **Example:** Written C sounds as Bb

### Why This Matters

These are **NOT** the same part in different clefs! They are:
- **Different instruments** with different transpositions
- **Played differently** - one reads concert pitch, one reads transposed
- **Separate parts** that should be generated independently

---

## 📋 File Upload Recognition

When you upload your PDFs, the system will recognize these names:

### Trombones
| Your Upload Name | Recognized As | Output File |
|-----------------|---------------|-------------|
| C Trombone 1 | 1st Trombone | 1st_Trombone.pdf |
| C Trombone 2 | 2nd Trombone | 2nd_Trombone.pdf |
| 1st C Trombone | 1st Trombone | 1st_Trombone.pdf |
| Trombone 1 | 1st Trombone | 1st_Trombone.pdf |

### Baritones
| Your Upload Name | Recognized As | Output File |
|-----------------|---------------|-------------|
| C Baritone BC | C Baritone BC (Bass Clef) | C_Baritone_BC.pdf |
| Baritone B.C. | C Baritone BC (Bass Clef) | C_Baritone_BC.pdf |
| Baritone (Bass Clef) | C Baritone BC (Bass Clef) | C_Baritone_BC.pdf |
| Bb Baritone TC | Bb Baritone TC (Treble Clef) | Bb_Baritone_TC.pdf |
| Baritone T.C. | Bb Baritone TC (Treble Clef) | Bb_Baritone_TC.pdf |
| Baritone (Treble Clef) | Bb Baritone TC (Treble Clef) | Bb_Baritone_TC.pdf |

---

## 🎼 Musical Relationship

### If Both Parts Play the Same Melody:

**C Baritone BC (Bass Clef):**
```
Written:  C  D  E  F  G  A  B  C
Sounds:   C  D  E  F  G  A  B  C  (concert pitch)
```

**Bb Baritone TC (Treble Clef):**
```
Written:  D  E  F# G  A  B  C# D
Sounds:   C  D  E  F  G  A  B  C  (concert pitch)
```

Notice:
- C Baritone BC writes what it sounds (concert pitch)
- Bb Baritone TC writes a whole step higher than it sounds
- Both sound the same pitch when playing together

---

## 🔧 System Configuration

### Trombone Settings
```
1st Trombone:
  - Clef: Bass
  - Transposition: None (C instrument)
  - Range: E2 to F5

2nd Trombone:
  - Clef: Bass
  - Transposition: None (C instrument)
  - Range: E2 to F5
```

### Baritone Settings
```
C Baritone BC (Bass Clef):
  - Clef: Bass
  - Transposition: None (C instrument)
  - Range: E2 to B4
  - Short Name: Bar. BC

Bb Baritone TC (Treble Clef):
  - Clef: Treble
  - Transposition: Down major 2nd (Bb instrument)
  - Range: E2 to B4
  - Short Name: Bar. TC
```

---

## 📊 Complete Low Brass Output

When you process your 12 files, the Low Brass section will generate:

### 4 Individual Part Books:

1. **1st_Trombone.pdf**
   - Bass clef
   - Concert pitch (C instrument)
   - From your "C Trombone 1" upload

2. **2nd_Trombone.pdf**
   - Bass clef
   - Concert pitch (C instrument)
   - From your "C Trombone 2" upload

3. **C_Baritone_BC.pdf**
   - Bass clef
   - Concert pitch (C instrument)
   - From your "C Baritone BC" upload

4. **Bb_Baritone_TC.pdf**
   - Treble clef
   - Transposed (Bb instrument)
   - From your "Bb Baritone TC" upload

---

## ⚠️ Important Notes

### These Are NOT Auto-Generated
Unlike Flute 2/3 or Violin parts which are automatically generated:
- **C Baritone BC** comes from your uploaded PDF
- **Bb Baritone TC** comes from your uploaded PDF
- They are **separate, independent parts**

### Different Notation
- C Baritone BC reads concert pitch in bass clef
- Bb Baritone TC reads transposed notation in treble clef
- They are NOT the same music in different clefs
- They are different transpositions of the underlying melody

### Why Two Versions?
Some baritone/euphonium players are trained to read:
- **Bass clef at concert pitch** (like trombones) → Use C Baritone BC
- **Treble clef transposed** (like trumpets) → Use Bb Baritone TC

Both versions can play the same melody, but the written notation is different.

---

## ✅ Summary

**Your Low Brass section:**
- ✅ 1st Trombone (C instrument, bass clef, concert pitch)
- ✅ 2nd Trombone (C instrument, bass clef, concert pitch)
- ✅ C Baritone BC (C instrument, bass clef, concert pitch)
- ✅ Bb Baritone TC (Bb instrument, treble clef, transposed)

**All 4 parts are independent and will be generated from your uploaded PDFs.**

🎵 Ready to process!
