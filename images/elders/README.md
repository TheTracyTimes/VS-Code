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

The photos are displayed using CSS background-image:
```html
<div class="elder-photo" style="background-image: url('images/elders/achile.jpg'); background-size: cover; background-position: center;">
</div>
```

The CSS automatically:
- Centers the photo
- Scales it to fill the card (300px height)
- Adds the orange accent bar at the bottom
- Falls back to gradient background if photo not found

## ➕ Adding More Elder Photos (Optional)

For Brother & Sister Josue Oscar or Brother & Sister Elfils Jeune:

1. Save photo as `oscar.jpg` or `jeune.jpg` in this directory
2. Edit `/home/user/VS-Code/about.html`
3. Find their elder card section
4. Replace:
   ```html
   <div class="elder-photo">
       👨‍👩
   </div>
   ```
   With:
   ```html
   <div class="elder-photo" style="background-image: url('images/elders/oscar.jpg'); background-size: cover; background-position: center;">
   </div>
   ```

## ✅ Quick Checklist

- [ ] Navigate to `/Users/liltrizzytreezy/GitHub/VS-Code/images/elders/`
- [ ] Save `achile.jpg` (Brother & Sister Edwige Achile photo)
- [ ] Save `eveillard.jpg` (Brother & Sister Patrick Eveillard photo)
- [ ] Refresh the website to see the photos appear
- [ ] Optional: Add photos for the other two elders
