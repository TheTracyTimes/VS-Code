# Content Management System Specification
## Sarasota Gospel Temple Website - Editable Content

---

## Overview

**Goal**: Enable non-technical users to update website text and images without coding knowledge
**Primary User**: Church administrators, ministry leaders
**Key Requirement**: Simple, intuitive interface for content updates

---

## Content Management Approach Options

### Option 1: Simple CMS (Recommended for Ease)

**Platforms**:
- **WordPress** - Most popular, extensive plugins
- **Wix** - Drag-and-drop, very user-friendly
- **Squarespace** - Beautiful templates, easy to use
- **Webflow** - More design control, visual editor

**Pros**:
- No coding required
- Built-in image management
- WYSIWYG (What You See Is What You Get) editors
- Mobile apps available
- Automatic backups
- User roles/permissions

**Cons**:
- Monthly fees ($12-40/month)
- Less customization
- May not match exact design
- Template limitations

**Recommended**: **WordPress** with custom theme
- Free and open-source
- Huge plugin ecosystem
- Can be customized to match exact design
- Easy image/text editing
- Hosting: ~$10-15/month

---

### Option 2: Headless CMS (Modern, Flexible)

**Platforms**:
- **Contentful** - Developer-friendly
- **Sanity** - Real-time collaboration
- **Strapi** - Open-source, self-hosted
- **Prismic** - Good for churches/nonprofits

**How it works**:
- Content stored in CMS
- Website pulls content via API
- Separate content from design

**Pros**:
- Complete design control
- Modern, fast performance
- Multi-platform (website, app, etc.)
- Structured content

**Cons**:
- Requires developer setup
- More complex for non-technical users
- API knowledge needed for changes

---

### Option 3: Static Site with CMS (Best Balance - RECOMMENDED)

**Platform**: **Netlify CMS** or **Decap CMS** (formerly Netlify CMS)
**Framework**: HTML/CSS/JS with CMS interface

**How it works**:
1. Website built with HTML/CSS/JavaScript
2. CMS interface overlays on top
3. Content stored in simple files (Markdown/JSON)
4. Easy admin panel for editing
5. Hosted on Netlify/Vercel (free tier available)

**Pros**:
- ✅ Complete design control (matches exact aesthetic)
- ✅ Free hosting (Netlify/Vercel)
- ✅ Fast performance (static site)
- ✅ Easy editing interface
- ✅ Git-based (version control, backups)
- ✅ No monthly CMS fees

**Cons**:
- Initial setup requires developer
- Less features than full CMS
- Image optimization manual

**This is the RECOMMENDED approach** - Perfect balance of customization, cost, and ease of use.

---

## Editable Content Areas

### Homepage Editable Sections

| Section | Editable Elements | Type |
|---------|-------------------|------|
| **Hero** | Headline, Tagline, Background Image | Text + Image |
| **Welcome Message** | Title, Body Text, Pastor Photo | Text + Image |
| **Service Times** | Days, Times, Address | Text |
| **Ministries Grid** | Ministry Names, Descriptions, Icons | Text + Images |
| **Upcoming Events** | Event Cards (Title, Date, Image, Link) | Text + Images |
| **Give Section** | Headline, Description, Button Text | Text |
| **Footer** | Contact Info, Social Links, Hours | Text |

### About Page Editable Sections

| Section | Editable Elements | Type |
|---------|-------------------|------|
| **History** | Title, Body Text, Historical Photos | Text + Images |
| **Mission Statement** | Text Block | Text |
| **Elders Section** | Names, Titles, Photos, Bios | Text + Images |

### Ministries Page Editable Sections

| Section | Editable Elements | Type |
|---------|-------------------|------|
| **Each Ministry** | Name, Description, Leader, Photo, Schedule | Text + Images |

### Events Page Editable Sections

| Section | Editable Elements | Type |
|---------|-------------------|------|
| **Featured Event** | Banner Image, Title, Date, Description | Text + Image |
| **Calendar Events** | Date, Time, Title, Description, Location | Text |
| **Event Photos** | Gallery Images, Captions | Images |

### Gallery Page Editable Sections

| Section | Editable Elements | Type |
|---------|-------------------|------|
| **Photo Galleries** | Album Name, Photos, Captions, Date | Text + Images |

### 2026 Meeting Page Editable Sections

| Section | Editable Elements | Type |
|---------|-------------------|------|
| **Event Info** | Dates, Times, Schedule, Speakers | Text |
| **Hero Banner** | Event Image, Logo | Image |
| **Registration Info** | Deadlines, Fees, Instructions | Text |

---

## Admin Interface Design

### Login Page
```
[Lighthouse Logo]

SARASOTA GOSPEL TEMPLE
Admin Login

Email: [__________________]
Password: [__________________]

[Login Button]

Forgot password?
```

**URL**: yourwebsite.com/admin
**Security**: Password protected, HTTPS only

---

### Dashboard After Login
```
╔════════════════════════════════════════════════╗
║  SARASOTA GOSPEL TEMPLE - Content Manager      ║
╠════════════════════════════════════════════════╣
║                                                ║
║  Welcome, [Admin Name]                         ║
║                                                ║
║  Quick Actions:                                ║
║  [Edit Homepage] [Add Event] [Update Gallery] ║
║                                                ║
║  ┌─────────────┐ ┌─────────────┐             ║
║  │   PAGES     │ │   MEDIA     │             ║
║  │             │ │             │             ║
║  │ • Home      │ │ • Images    │             ║
║  │ • About     │ │ • Documents │             ║
║  │ • Ministries│ │             │             ║
║  │ • Events    │ │             │             ║
║  │ • Gallery   │ │             │             ║
║  │ • Give      │ │             │             ║
║  │ • 2026 Mtg  │ │             │             ║
║  └─────────────┘ └─────────────┘             ║
║                                                ║
║  Recent Activity:                              ║
║  • Event added: Youth Night - Jan 20           ║
║  • Photo uploaded: Service Photos - Jan 18     ║
║                                                ║
║  [Logout]                                      ║
╚════════════════════════════════════════════════╝
```

---

### Page Editor Interface

**Example: Editing Homepage Welcome Section**

```
╔════════════════════════════════════════════════╗
║  Edit Page: Homepage > Welcome Section         ║
╠════════════════════════════════════════════════╣
║                                                ║
║  Section Title:                                ║
║  [Welcome to Sarasota Gospel Temple_________]  ║
║                                                ║
║  Section Text:                                 ║
║  ┌────────────────────────────────────────┐  ║
║  │ We are a community of believers        │  ║
║  │ seeking to dwell in God's presence...  │  ║
║  │                                        │  ║
║  │ [Bold] [Italic] [Link] [List]         │  ║
║  └────────────────────────────────────────┘  ║
║                                                ║
║  Pastor Photo:                                 ║
║  ┌─────────┐                                  ║
║  │  [IMG]  │  [Change Photo] [Remove]         ║
║  └─────────┘                                  ║
║                                                ║
║  ┌──────────────────────────────────────────┐ ║
║  │           PREVIEW                         │ ║
║  │  [Shows how it will look on website]     │ ║
║  └──────────────────────────────────────────┘ ║
║                                                ║
║  [Cancel]  [Save Draft]  [Publish Changes]   ║
╚════════════════════════════════════════════════╝
```

---

### Image Upload Interface

```
╔════════════════════════════════════════════════╗
║  Upload Image                                  ║
╠════════════════════════════════════════════════╣
║                                                ║
║  ┌────────────────────────────────────────┐  ║
║  │                                        │  ║
║  │   Drag and drop image here             │  ║
║  │   or                                   │  ║
║  │   [Browse Files]                       │  ║
║  │                                        │  ║
║  │   Accepted: JPG, PNG, WebP             │  ║
║  │   Max size: 5MB                        │  ║
║  └────────────────────────────────────────┘  ║
║                                                ║
║  Image Title:                                  ║
║  [________________________________]            ║
║                                                ║
║  Alt Text (for accessibility):                ║
║  [________________________________]            ║
║                                                ║
║  ☑ Optimize for web (recommended)             ║
║  ☑ Create thumbnail                           ║
║                                                ║
║  [Cancel]  [Upload Image]                     ║
╚════════════════════════════════════════════════╝
```

---

## Content Types & Fields

### Event Content Type
```yaml
Event:
  - Title (text, required)
  - Date (date picker, required)
  - Time (time picker, required)
  - Location (text)
  - Description (rich text)
  - Featured Image (image upload)
  - Registration Link (URL)
  - Categories (dropdown: Service, Meeting, Youth, etc.)
  - Status (dropdown: Upcoming, Past, Cancelled)
```

### Ministry Content Type
```yaml
Ministry:
  - Name (text, required)
  - Description (rich text)
  - Leader Name (text)
  - Leader Photo (image upload)
  - Meeting Schedule (text)
  - Contact Email (email)
  - Icon (image upload)
  - Status (checkbox: Active/Inactive)
```

### Elder Content Type
```yaml
Elder:
  - Full Name (text, required)
  - Title (text: "Brother & Sister")
  - Photo (image upload)
  - Bio (rich text)
  - Email (email)
  - Phone (phone)
  - Display Order (number)
```

### Gallery Album Content Type
```yaml
Gallery Album:
  - Album Name (text, required)
  - Date (date picker)
  - Description (textarea)
  - Cover Image (image upload)
  - Photos (multiple image upload)
    - Each photo can have:
      - Caption (text)
      - Photographer (text)
```

### Announcement/Slideshow Content Type
```yaml
Slideshow Item:
  - Title (text)
  - Description (text)
  - Background Image (image upload)
  - Link (URL)
  - Button Text (text)
  - Active (checkbox)
  - Display Order (number)
```

---

## Text Editor Features

### Rich Text Editor (WYSIWYG)

**Formatting Options**:
- **Bold**, *Italic*, Underline
- Headings (H2, H3, H4)
- Bullet lists, Numbered lists
- Links (internal and external)
- Alignment (left, center, right)
- Scripture quotes (special formatting)
- Undo/Redo

**What You Get**:
```
Toolbar:
[B] [I] [U] | [H2] [H3] | [•] [1.] | [🔗] [📷] | [←] [→]

Content Area:
┌─────────────────────────────────────────┐
│ Type your content here...               │
│                                         │
│ Use the toolbar above to format text    │
└─────────────────────────────────────────┘

Character count: 156
```

**Special Features**:
- Bible verse formatter (adds proper styling)
- Scripture reference auto-link
- Paste from Word (cleans formatting)
- Auto-save drafts

---

## Image Management

### Image Library

**Organization**:
```
Media Library
├── Events
│   ├── 2026-International-Meeting
│   ├── Youth-Events
│   └── Services
├── Ministries
│   ├── Youth
│   ├── Music
│   └── Prayer
├── People
│   ├── Elders
│   └── Leaders
├── Building
└── Graphics
    ├── Logos
    ├── Icons
    └── Backgrounds
```

**Features**:
- Folder organization
- Search by filename/date
- Filter by type/size
- Bulk upload
- Bulk edit (alt text, tags)
- Image preview
- Copy image URL
- Edit image (crop, resize)
- Replace image (keeps same URL)

### Image Optimization

**Automatic Processing**:
1. Resize large images (max 2000px wide)
2. Compress for web (80-90% quality)
3. Generate responsive sizes:
   - Large (1200px)
   - Medium (800px)
   - Small (400px)
   - Thumbnail (200px)
4. Convert to WebP (modern format)
5. Keep original as backup

**User Controls**:
- Upload original high-res image
- System handles optimization
- Option to disable optimization for specific images
- Preview before saving

---

## Editing Workflow

### Typical Edit Process

**Step 1**: Log in to admin panel
**Step 2**: Navigate to page/content to edit
**Step 3**: Click "Edit" button
**Step 4**: Make changes in editor
**Step 5**: Preview changes
**Step 6**: Save as draft OR publish immediately
**Step 7**: View on live website

### Save Options

**Save as Draft**:
- Changes NOT visible on public website
- Can be reviewed later
- Multiple drafts can exist

**Publish**:
- Changes go live immediately
- Previous version archived
- Can be reverted if needed

**Schedule**:
- Set future publish date/time
- Automatically publishes at scheduled time
- Useful for announcements

---

## User Roles & Permissions

### Role Levels

**Super Admin** (Tech person/developer):
- Full access to everything
- Can add/remove users
- Can modify design/code
- Access to settings

**Admin** (Lead pastor/administrator):
- Edit all content
- Upload/manage images
- Add/edit/delete events
- Cannot modify design/settings

**Editor** (Ministry leaders):
- Edit specific pages (their ministry)
- Upload images to specific folders
- Add events (pending approval)
- Cannot delete

**Contributor** (Limited access):
- Create content (pending approval)
- Cannot publish
- Cannot upload images

### Permission Matrix

| Action | Super Admin | Admin | Editor | Contributor |
|--------|-------------|-------|--------|-------------|
| Edit Homepage | ✅ | ✅ | ❌ | ❌ |
| Edit About | ✅ | ✅ | ❌ | ❌ |
| Edit Ministries | ✅ | ✅ | ✅ Own only | ❌ |
| Add Events | ✅ | ✅ | ✅ Approval needed | ✅ Approval needed |
| Upload Images | ✅ | ✅ | ✅ Limited | ❌ |
| Delete Content | ✅ | ✅ | ❌ | ❌ |
| Manage Users | ✅ | ❌ | ❌ | ❌ |
| Site Settings | ✅ | ❌ | ❌ | ❌ |

---

## Mobile Admin App

### Features

**Ideal for**:
- Quick text updates
- Publishing photos from events
- Posting urgent announcements

**Capabilities**:
- Edit text content
- Upload photos (from camera or gallery)
- Publish/unpublish content
- Respond to form submissions
- View website analytics

**Platform Options**:
- WordPress mobile app (if using WordPress)
- Custom web app (responsive admin panel)
- PWA (Progressive Web App) - works like app, no download

---

## Training & Documentation

### For Content Editors

**Video Tutorials**:
1. How to log in (2 min)
2. How to edit text (5 min)
3. How to upload images (5 min)
4. How to add an event (7 min)
5. How to update the gallery (5 min)
6. How to manage the slideshow (5 min)

**Written Guide**:
- PDF manual with screenshots
- Step-by-step instructions
- Common tasks checklist
- Troubleshooting section

**Quick Reference Card**:
- 1-page printable guide
- Common tasks
- Support contact info

---

## Content Backup & Safety

### Automatic Backups

**Frequency**:
- Daily full backup
- Instant backup before any change
- Keep backups for 30 days

**What's backed up**:
- All content (text)
- All images
- All settings
- All forms/submissions

**Restore Options**:
- Restore entire site
- Restore single page
- Restore specific version
- Restore deleted image

### Version History

**Track Changes**:
- Who made the change
- When it was made
- What was changed
- Previous version saved

**Revert Capability**:
- Roll back to any previous version
- Compare versions side-by-side
- Restore deleted content

---

## Technical Implementation

### Recommended Tech Stack

**Frontend** (What users see):
- HTML5, CSS3, JavaScript
- Custom design matching brand guidelines
- Responsive/mobile-friendly
- Fast loading (optimized)

**Backend** (Content management):
- **Netlify CMS** (free, open-source)
  - Simple admin interface
  - Git-based (automatic version control)
  - Markdown or JSON for content
  - Image handling built-in

**Hosting**:
- **Netlify** or **Vercel** (free tier)
  - Automatic deployments
  - Free SSL certificate
  - Fast CDN
  - Forms built-in (for contact form)

**Alternative** (if prefer traditional):
- **WordPress** with custom theme
  - Widely supported
  - Tons of plugins
  - More features out of box
  - Hosting ~$10-15/month

---

## Content Structure (For Netlify CMS)

### File Organization
```
/content
  /pages
    homepage.md
    about.md
    contact.md
  /ministries
    youth.md
    prayer.md
    music.md
  /events
    2026-international-meeting.md
    youth-night-jan.md
  /gallery
    albums.json
  /elders
    achile.md
    eveillard.md
    oscar.md
    jeune.md

/public/images
  /events
  /ministries
  /people
  /graphics
```

### Example Content File (homepage.md)
```yaml
---
title: "Sarasota Gospel Temple"
tagline: "A City of Refuge"
hero_image: "/images/lighthouse-hero.png"
---

# Welcome to Sarasota Gospel Temple

We are a community of believers seeking to dwell in God's presence...

## Service Times
- Sunday Morning: 10:00 AM
- Sunday Evening: 6:00 PM
- Wednesday Bible Study: 7:00 PM
```

**Editing Experience**:
- Admin opens "Homepage" in CMS
- Sees form fields for title, tagline, hero image, content
- Makes changes in simple interface
- Clicks "Publish"
- Changes appear on website immediately

---

## Security Considerations

### Access Control
- Strong password requirements
- Two-factor authentication (optional)
- Auto-logout after inactivity
- Login attempt limits
- IP whitelist option (optional)

### Content Security
- Input validation (prevent malicious code)
- File type restrictions (only images, PDFs, etc.)
- File size limits
- Malware scanning on uploads
- HTTPS only (encrypted)

### Backup Security
- Encrypted backups
- Off-site storage
- Regular backup testing
- Access logs

---

## Support & Maintenance

### Ongoing Support

**For Admins**:
- Email support for questions
- Phone support for urgent issues
- Screen share sessions for training
- Regular check-ins (monthly)

**For Technical Issues**:
- Bug fixes
- Security updates
- Performance optimization
- New feature requests

### Maintenance Schedule

**Weekly**:
- Check for broken links
- Review form submissions
- Monitor site performance

**Monthly**:
- Update plugins/software
- Review analytics
- Content audit

**Quarterly**:
- Full backup test
- Security review
- Performance audit
- Training refresher

---

## Cost Breakdown

### Netlify CMS Option (RECOMMENDED)
- **Setup**: One-time developer fee
- **Hosting**: FREE (Netlify/Vercel free tier)
- **Domain**: ~$12-15/year
- **Maintenance**: Optional support package
- **Total ongoing**: ~$1-2/month

### WordPress Option
- **Setup**: One-time developer fee
- **Hosting**: $10-15/month
- **Domain**: ~$12-15/year
- **Premium plugins**: $0-50/year (optional)
- **Total ongoing**: ~$12-20/month

---

**Last Updated**: 2026-01-22
**Version**: 1.0
**Status**: Specification Complete
