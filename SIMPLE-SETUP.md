# Super Simple Setup Guide

**No tech experience needed!** Just follow these steps exactly.

---

## What This Does

This program will:
- Let you upload scanned music sheets (PDFs)
- Turn handwritten music into digital files
- Create separate books for each instrument
- Give you professional PDFs you can print

---

## Before You Start

You need:
- A computer (Windows, Mac, or Linux)
- Internet connection
- 5 minutes of your time

---

## Step-by-Step Installation

### Step 1: Check if You Have Python

**What is Python?** It's like Microsoft Word for programmers. We need it to run our program.

**Windows:**
1. Click the Start menu (bottom left)
2. Type `cmd` and press Enter
3. A black window appears
4. Type: `python --version` and press Enter

**Mac:**
1. Press Command + Space
2. Type `terminal` and press Enter
3. A white/black window appears
4. Type: `python3 --version` and press Enter

**What you should see:**
```
Python 3.9.7
```
(or any version starting with 3.8, 3.9, 3.10, etc.)

**If you DON'T see this:**
- Go to: https://www.python.org/downloads/
- Click the big yellow "Download Python" button
- Run the file that downloads
- Follow the installation wizard (just click "Next" a bunch of times)
- ✅ Make sure to CHECK the box that says "Add Python to PATH"

---

### Step 2: Download the Music Recognition Files

**Option A: If you have the files already**
- Skip to Step 3!

**Option B: Download from GitHub**
1. Go to your GitHub repository
2. Click the green "Code" button
3. Click "Download ZIP"
4. Unzip the file to your Desktop or Documents folder

---

### Step 3: Open the Command Window in the Right Place

**Windows:**
1. Open the folder where you put the files
2. Hold `Shift` and right-click in an empty area
3. Click "Open PowerShell window here" or "Open command window here"

**Mac:**
1. Open Finder
2. Find the folder where you put the files
3. Right-click the folder
4. Click "Services" → "New Terminal at Folder"

**You should see something like:**
```
C:\Users\YourName\Desktop\VS-Code>
```
or
```
/Users/yourname/Desktop/VS-Code %
```

---

### Step 4: Install the Program (Lite Version - Fast & Easy)

**Copy and paste this command exactly:**

**Windows:**
```
install-lite.bat
```

**Mac/Linux:**
```
./install-lite.sh
```

**Press Enter.**

**What happens:**
- You'll see text scrolling by
- It says "Installing..."
- Takes about 1-2 minutes
- At the end, it says "✅ Installation complete!"

**If it asks for permission:**
- Click "Yes" or "Allow"

---

### Step 5: Start the Web App

**Copy and paste this command:**

**Windows:**
```
cd web_app
python server.py
```

**Mac/Linux:**
```
cd web_app
python3 server.py
```

**Press Enter.**

**What you should see:**
```
==============================
Music Recognition Web Application
==============================

🎵 Open your browser to: http://localhost:8000

Press Ctrl+C to stop the server
```

**DON'T CLOSE THIS WINDOW!** Keep it open while using the app.

---

### Step 6: Open Your Web Browser

1. Open your web browser (Chrome, Firefox, Safari, etc.)
2. In the address bar at the top, type exactly:
   ```
   localhost:8000
   ```
3. Press Enter

**You should see:**
- A beautiful purple website
- Title: "🎵 Handwritten Music Recognition"
- A "System Status" section showing your computer info

**Success!** 🎉 The app is running!

---

## How to Use It

### Upload Your Music Sheets:

1. **Create a Project:**
   - Type a name like "My Church Band Music"
   - Click "Create Project"

2. **Upload PDFs:**
   - You'll see a purple box that says "Drag & Drop"
   - Drag your PDF files from your desktop into this box
   - OR click the box and select files
   - Click "Upload All Files"

3. **Choose Options:**
   - Check the boxes for what you want:
     - ✅ Generate extra parts (like Flute 2, Violin, etc.)
     - ✅ Split combined parts (make separate books)
   - Click "Start Processing"

4. **Wait:**
   - You'll see a progress bar
   - It shows what's happening
   - **Note:** In lite mode, it creates sample files to show you how it works

5. **Download:**
   - When done, you'll see PDF files
   - Click any file to download it
   - Open with Adobe Reader or any PDF viewer

---

## Stopping the App

When you're done:
1. Go back to the black/white command window
2. Press `Ctrl + C` (hold Control and press C)
3. The program stops
4. You can close the window

---

## Starting Again Later

Want to use it again tomorrow?

1. Open command window in the VS-Code folder (see Step 3)
2. Type: `cd web_app` and press Enter
3. Type: `python server.py` (Windows) or `python3 server.py` (Mac)
4. Open browser to: `localhost:8000`

---

## Common Problems & Solutions

### "python: command not found"

**Problem:** Python isn't installed or not set up correctly

**Fix:**
- **Mac users:** Use `python3` instead of `python`
- **All users:** Reinstall Python from python.org
- Make sure to check "Add Python to PATH" during install

---

### "Address already in use"

**Problem:** Port 8000 is being used by another program

**Fix:** Someone else is using that address. Try:
```
localhost:8001
```
Or close other programs and try again.

---

### "Installation failed"

**Problem:** Internet connection issue or not enough disk space

**Fix:**
- Check your internet connection
- Make sure you have 1 GB free on your hard drive
- Try running the installer again

---

### Web page doesn't load

**Problem:** Server isn't running or wrong address

**Fix:**
1. Make sure the command window is still open
2. Make sure it says "Starting server..." in the window
3. Try typing the address exactly: `localhost:8000`
4. Try in a different browser

---

### "Demo Mode" message

**This is OK!** Demo mode means:
- The lite version is running
- It creates sample PDFs instead of real ones
- Perfect for testing and learning
- If you want real processing, run `install-full.bat` instead (downloads 2.5GB)

---

## What's the Difference?

### Lite Install (What You Just Did):
- ✅ 50 MB download
- ✅ 1-minute install
- ✅ Full web interface
- ✅ Upload PDFs
- ✅ See how it works
- ⚠️ Creates sample files (not real recognition)

### Full Install (For Real Use):
- ⚠️ 2.5 GB download
- ⚠️ 10-30 minute install
- ✅ Everything from Lite
- ✅ **PLUS** actual music recognition
- ✅ **PLUS** real digitization
- ✅ **PLUS** processes your handwritten music

**To upgrade later:**
```
install-full.bat    (Windows)
./install-full.sh   (Mac/Linux)
```

---

## Video Tutorial (If These Steps Don't Make Sense)

Think of it like:
1. **Installing Python** = Installing Microsoft Office
2. **Running install-lite** = Installing our app (like installing Zoom)
3. **Running server.py** = Starting the app (like opening Word)
4. **Opening localhost:8000** = Opening the app in your browser

---

## Still Confused? Quick Checklist

- [ ] I installed Python
- [ ] I downloaded the VS-Code folder
- [ ] I opened command window IN that folder
- [ ] I ran install-lite.bat (or .sh)
- [ ] I saw "Installation complete!"
- [ ] I typed: cd web_app
- [ ] I typed: python server.py (or python3 server.py)
- [ ] I saw "Open your browser to: http://localhost:8000"
- [ ] I opened my browser
- [ ] I typed: localhost:8000
- [ ] I see the purple website!

**If you got through all these, you're done!** 🎉

---

## Need More Help?

Take a screenshot of:
1. The command window (the black/white text window)
2. Your web browser

And share with someone who can help debug the issue.

---

## Summary

**3 commands to remember:**

**First time:**
```
./install-lite.sh    (Mac/Linux)
install-lite.bat     (Windows)
```

**Every time you use it:**
```
cd web_app
python3 server.py    (Mac/Linux)
python server.py     (Windows)
```

**In browser:**
```
localhost:8000
```

**That's it!** 🎵

---

**Made for musicians, not programmers.**
