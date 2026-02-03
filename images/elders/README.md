# Elder Photos Directory

## 📍 Where to Save Photos

This directory is located at:
```
/Users/liltrizzytreezy/GitHub/VS-Code/images/elders/
```

To add elder photos to your website, save the image files directly in this folder.

## 📸 Required Photos

### 1. Brother & Sister Edwige Achile
- **Filename:** `achile.jpg`
- **Full path:** `/Users/liltrizzytreezy/GitHub/VS-Code/images/elders/achile.jpg`
- **Status:** ⚠️ Ready to upload (website is configured, just save the file here)

### 2. Brother & Sister Patrick Eveillard
- **Filename:** `eveillard.jpg`
- **Full path:** `/Users/liltrizzytreezy/GitHub/VS-Code/images/elders/eveillard.jpg`
- **Status:** ⚠️ Ready to upload (website is configured, just save the file here)

### 3. Brother & Sister Josue Oscar
- **Filename:** `oscar.jpg`
- **Full path:** `/Users/liltrizzytreezy/GitHub/VS-Code/images/elders/oscar.jpg`
- **Status:** ⚠️ Ready to upload (website is configured, just save the file here)

### 4. Brother & Sister Elfils Jeune
- **Filename:** `jeune.jpg`
- **Full path:** `/Users/liltrizzytreezy/GitHub/VS-Code/images/elders/jeune.jpg`
- **Status:** ⚠️ Ready to upload (website is configured, just save the file here)

## 📝 How to Add Photos

**Step 1:** Save your photo files to this directory
- Navigate to: `/Users/liltrizzytreezy/GitHub/VS-Code/images/elders/`
- Save photos with the exact filenames shown above
- Supported formats: `.jpg`, `.jpeg`, `.png`

**Step 2:** The website will automatically display them
- The HTML is already configured to show these photos
- No code changes needed - just save the files!
- If photos don't appear immediately, hard refresh your browser (Cmd+Shift+R on Mac)

## 🎨 Photo Guidelines

For best results:
- **Aspect ratio:** Square or portrait orientation works best
- **Resolution:** At least 800x800 pixels
- **File size:** Keep under 500KB for fast loading
- **Format:** JPG preferred (PNG also works)
- **Content:** Professional photo showing both the Elder and their spouse

## 🔧 Technical Details

The photos are displayed using HTML img tags with custom sizing:
```html
<div class="elder-photo achile-photo">
    <img src="images/elders/achile.jpg" alt="Brother & Sister Edwige Achile">
</div>
```

**Custom Photo Sizing:**
Each elder has their own photo container class that can be adjusted:
- `.achile-photo` - Min height: 350px
- `.eveillard-photo` - Min height: 350px
- `.oscar-photo` - Min height: 300px
- `.jeune-photo` - Min height: 300px

The CSS automatically:
- Centers the photo
- Uses object-fit to maintain aspect ratio
- Scales to fill the container without distortion
- Adds the orange accent bar at the bottom
- Falls back to gradient background with emoji if photo not found

## ➕ All Elder Photos Configured

All four elder photos are now configured and ready to use:
- **Achile:** `achile.jpg`
- **Eveillard:** `eveillard.jpg`
- **Oscar:** `oscar.jpg`
- **Jeune:** `jeune.jpg`

Simply save the photos to this directory with the correct filenames and they will automatically appear on the website!

## 🎛️ Adjusting Photo Sizes

If a photo doesn't fit well in its container, you can adjust the min-height in the CSS:

1. Open `about.html` in a text editor
2. Find the style section with `.elder-photo.achile-photo` (around line 90)
3. Change the `min-height` value for the specific elder:
   ```css
   .elder-photo.achile-photo {
       min-height: 400px;  /* Adjust this value */
   }
   ```
4. Save and refresh your browser to see the changes

Recommended heights based on photo orientation:
- **Portrait photos:** 350-400px
- **Square photos:** 300-350px
- **Landscape photos:** 250-300px

## ✅ Quick Checklist

- [ ] Navigate to `/Users/liltrizzytreezy/GitHub/VS-Code/images/elders/`
- [ ] Save `achile.jpg` (Brother & Sister Edwige Achile photo)
- [ ] Save `eveillard.jpg` (Brother & Sister Patrick Eveillard photo)
- [ ] Save `oscar.jpg` (Brother & Sister Josue Oscar photo)
- [ ] Save `jeune.jpg` (Brother & Sister Elfils Jeune photo)
- [ ] Refresh the website to see the photos appear
