# Part Name Recognition and Mapping

This document shows how part names in your uploaded PDFs are recognized and mapped to standardized output names.

---

## 🎺 How It Works

When you upload PDFs, the system:
1. **Detects** the part name from the PDF (e.g., "C Trombone 1", "Bb Clarinet 2")
2. **Recognizes** the instrument using fuzzy matching (ignores case, handles variations)
3. **Maps** to standardized output name (e.g., "1st Trombone", "2nd Clarinet")
4. **Generates** the part book with the clean, simplified name

---

## 📋 Your PDF Naming → Output Names

### Trombones
| Your PDF File Name | System Recognizes | Output File Name |
|-------------------|-------------------|------------------|
| C Trombone 1 | Trombone + "1" | **1st_Trombone.pdf** |
| C Trombone 2 | Trombone + "2" | **2nd_Trombone.pdf** |
| 1st C Trombone | Trombone + "1st" | **1st_Trombone.pdf** |
| Trombone 1 | Trombone + "1" | **1st_Trombone.pdf** |
| Tbn. 1 | Trombone + "1" | **1st_Trombone.pdf** |

### Clarinets
| Your PDF File Name | System Recognizes | Output File Name |
|-------------------|-------------------|------------------|
| Bb Clarinet 1 | Clarinet + "1" | **1st_Clarinet.pdf** |
| Bb Clarinet 2 | Clarinet + "2" | **2nd_Clarinet.pdf** |
| 1st Bb Clarinet | Clarinet + "1st" | **1st_Clarinet.pdf** |
| Clarinet 1 | Clarinet + "1" | **1st_Clarinet.pdf** |
| Cl. 1 | Clarinet + "1" | **1st_Clarinet.pdf** |

### Baritones
| Your PDF File Name | System Recognizes | Output File Name |
|-------------------|-------------------|------------------|
| Baritone | Baritone (no T.C.) | **Euphonium_Bass_Clef.pdf** |
| Baritone B.C. | Baritone + "B.C." | **Euphonium_Bass_Clef.pdf** |
| Baritone T.C. | Baritone + "T.C." | **Baritone_Treble_Clef.pdf** |
| Baritone (Treble Clef) | Baritone + "Treble" | **Baritone_Treble_Clef.pdf** |
| Euphonium | Euphonium | **Euphonium_Bass_Clef.pdf** |

---

## 🎵 Complete Instrument Recognition Table

### Woodwinds

**Flutes:**
- "Flute", "Flute 1", "1st Flute" → **C_Flute.pdf**
- "Flute 2", "2nd Flute" → **C_Flute_2.pdf** (generated)
- "Flute 3", "3rd Flute" → **C_Flute_3.pdf** (generated)

**Clarinets:**
- "Clarinet 1", "Bb Clarinet 1", "1st Clarinet" → **1st_Clarinet.pdf**
- "Clarinet 2", "Bb Clarinet 2", "2nd Clarinet" → **2nd_Clarinet.pdf**
- "Clarinet 3", "Bb Clarinet 3", "3rd Clarinet" → **3rd_Clarinet.pdf**
- "Bass Clarinet", "Bb Bass Clarinet" → **Bb_Bass_Clarinet.pdf**

**Saxophones:**
- "Alto Sax 1", "Eb Alto Sax 1", "1st Alto Sax" → **1st_Eb_Alto_Saxophone.pdf**
- "Alto Sax 2", "Eb Alto Sax 2", "2nd Alto Sax" → **2nd_Eb_Alto_Saxophone.pdf**
- "Tenor Sax", "Bb Tenor Sax" → **Bb_Tenor_Saxophone.pdf**
- "Bari Sax", "Baritone Sax", "Eb Bari Sax" → **Eb_Baritone_Saxophone.pdf**

### Brass

**Trumpets:**
- "Trumpet 1", "Bb Trumpet 1", "1st Trumpet" → **1st_Bb_Trumpet.pdf**
- "Trumpet 2", "Bb Trumpet 2", "2nd Trumpet" → **2nd_Bb_Trumpet.pdf**

**French Horn:**
- "French Horn", "F Horn", "Horn" → **F_French_Horn.pdf**

**Trombones:**
- "Trombone 1", "C Trombone 1", "1st Trombone" → **1st_Trombone.pdf**
- "Trombone 2", "C Trombone 2", "2nd Trombone" → **2nd_Trombone.pdf**

**Low Brass:**
- "Baritone", "Euphonium", "Baritone B.C." → **Euphonium_Bass_Clef.pdf**
- "Baritone T.C.", "Baritone (Treble Clef)" → **Baritone_Treble_Clef.pdf**
- "Tuba" → **C_Tuba.pdf**

---

## 🔍 Recognition Rules

The system uses **fuzzy matching** with these rules:

### Rule 1: Case Insensitive
- "TROMBONE 1" = "trombone 1" = "Trombone 1" = "TrOmBoNe 1"

### Rule 2: Ignores Key/Pitch Prefixes
- "C Trombone" = "Trombone"
- "Bb Clarinet" = "Clarinet"
- "Eb Alto Sax" = "Alto Sax"
- "F Horn" = "Horn"

### Rule 3: Number Recognition
Recognizes multiple formats:
- **Digits:** "1", "2", "3"
- **Ordinals:** "1st", "2nd", "3rd"
- **Words:** "first", "second", "third"

### Rule 4: Abbreviation Recognition
- "Tbn." = "Trombone"
- "Cl." = "Clarinet"
- "Tpt." = "Trumpet"
- "Sax" = "Saxophone"

### Rule 5: Special Cases

**Baritone Clef Detection:**
- Contains "T.C." or "Treble" → Baritone (Treble Clef)
- Otherwise → Euphonium (Bass Clef)

**Clarinet Type:**
- Contains "Bass" → Bass Clarinet
- Contains "Alto" → Alto Clarinet
- Otherwise → Regular Clarinet

---

## 💡 Examples from Your Church Band

Based on typical church band notation, here's how your parts will map:

### Uploaded File Names → Output Names

```
Your PDFs:                  Output Part Books:
--------------              ------------------
C Trombone 1.pdf      →     1st_Trombone.pdf
C Trombone 2.pdf      →     2nd_Trombone.pdf
Bb Clarinet 1.pdf     →     1st_Clarinet.pdf
Bb Clarinet 2.pdf     →     2nd_Clarinet.pdf
Eb Alto Sax 1.pdf     →     1st_Eb_Alto_Saxophone.pdf
Bb Trumpet 1.pdf      →     1st_Bb_Trumpet.pdf
F French Horn.pdf     →     F_French_Horn.pdf
Baritone.pdf          →     Euphonium_Bass_Clef.pdf
                            + Baritone_Treble_Clef.pdf (generated)
```

---

## 🎯 Low Brass Section Output

Your Low Brass section will generate **4 part books:**

1. **1st_Trombone.pdf** - From your "C Trombone 1" PDF
2. **2nd_Trombone.pdf** - From your "C Trombone 2" PDF
3. **Euphonium_Bass_Clef.pdf** - From your "Baritone" PDF (bass clef)
4. **Baritone_Treble_Clef.pdf** - Generated from Euphonium (treble clef, transposed)

Both baritone versions contain the **same musical content**, just in different clefs for different readers.

---

## 🔧 What If My Part Isn't Recognized?

If the system doesn't recognize a part name:

1. **Check the spelling** - Make sure it contains the instrument name
2. **Use common names** - "Clarinet 1" instead of "Cl. #1"
3. **Add numbers clearly** - "Trumpet 1" not "Trumpet-One"
4. **Avoid special characters** - "Trombone 2" not "Trombone #2"

**Recognized keywords:**
- Flute, Clarinet, Saxophone (Sax), Trumpet, Horn, Trombone, Baritone, Euphonium, Tuba

**Recognized numbers:**
- 1, 2, 3, 1st, 2nd, 3rd, first, second, third

---

## ✅ Your Configuration Is Ready!

The system will correctly recognize:
- ✅ "C Trombone 1" → "1st Trombone"
- ✅ "C Trombone 2" → "2nd Trombone"
- ✅ "Bb Clarinet 1" → "1st Clarinet"
- ✅ "Bb Clarinet 2" → "2nd Clarinet"
- ✅ "Baritone B.C." → "Euphonium (Bass Clef)"
- ✅ "Baritone T.C." → "Baritone (Treble Clef)"

Upload your 12 files and the system will handle the rest! 🎵
