# How to Add Elder Photos - Step by Step Guide

## 🔍 Can't Find the images/elders Folder?

Follow these steps on your Mac to get the folder and add photos:

### Step 1: Open Terminal on Your Mac

1. Press `Cmd + Space` to open Spotlight
2. Type "Terminal" and press Enter

### Step 2: Navigate to Your Repository

In Terminal, type these commands (press Enter after each):

```bash
cd /Users/liltrizzytreezy/GitHub/VS-Code
```

### Step 3: Check Your Current Branch

```bash
git branch
```

You should see a `*` next to `claude/analyze-photos-design-CqXcK`. If not, switch to it:

```bash
git checkout claude/analyze-photos-design-CqXcK
```

### Step 4: Pull the Latest Changes

```bash
git pull origin claude/analyze-photos-design-CqXcK
```

This will download the `images/elders` folder to your Mac.

### Step 5: Verify the Folder Exists

```bash
ls -la images/elders/
```

You should see:
```
README.md
```

### Step 6: Open the Folder in Finder

From Terminal, type:

```bash
open images/elders
```

This will open the `images/elders` folder in Finder on your Mac!

---

## 📸 Now Add Your Photos

Once the Finder window is open:

1. **Drag and drop** your photos into this folder
2. **Rename them** to exactly:
   - `achile.jpg` (for Brother & Sister Edwige Achile)
   - `eveillard.jpg` (for Brother & Sister Patrick Eveillard)

### Important Photo Requirements:
- **Exact filenames:** `achile.jpg` and `eveillard.jpg` (lowercase, no spaces)
- **Format:** JPG or PNG
- **Size:** At least 800x800 pixels recommended
- **File size:** Under 500KB for best website performance

---

## 🌐 View the Photos on Your Website

After saving the photos:

1. Open Terminal in your VS-Code directory
2. Start the local server:
   ```bash
   cd /Users/liltrizzytreezy/GitHub/VS-Code
   python3 -m http.server 8000
   ```
3. Open your browser to: http://localhost:8000
4. Click on "About" in the navigation
5. Scroll down to see the Elder photos!

If photos don't show immediately:
- Hard refresh: Press `Cmd + Shift + R`
- Check the exact filename spelling in Finder

---

## 💾 Commit the Photos to Git (Optional)

Once you're happy with how the photos look:

```bash
git add images/elders/achile.jpg images/elders/eveillard.jpg
git commit -m "Add elder photos for Achile and Eveillard"
git push origin claude/analyze-photos-design-CqXcK
```

---

## ❓ Troubleshooting

### "No such file or directory: /Users/liltrizzytreezy/GitHub/VS-Code"

Your repository might be in a different location. To find it:

```bash
cd ~
find . -name "VS-Code" -type d 2>/dev/null | grep GitHub
```

This will show you the actual path to your repository.

### "images/elders doesn't exist after git pull"

Check if you have uncommitted changes:

```bash
git status
```

If you see the images folder listed as untracked, that's expected - it exists but is empty except for the README.

Try this to see if the folder exists:
```bash
ls -la images/
```

If you see "No such file or directory", create it:
```bash
mkdir -p images/elders
```

Then you can add your photos directly!

---

## 📍 Quick Reference

**Repository Path:** `/Users/liltrizzytreezy/GitHub/VS-Code`
**Photos Go Here:** `/Users/liltrizzytreezy/GitHub/VS-Code/images/elders/`
**Required Files:**
- `achile.jpg`
- `eveillard.jpg`

**Open Folder Command:**
```bash
cd /Users/liltrizzytreezy/GitHub/VS-Code
open images/elders
```

**View Website Locally:**
```bash
cd /Users/liltrizzytreezy/GitHub/VS-Code
python3 -m http.server 8000
```
Then visit: http://localhost:8000/about.html
