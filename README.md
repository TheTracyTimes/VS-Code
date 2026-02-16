# Sarasota Gospel Temple Website

A complete custom website for Sarasota Gospel Temple featuring the 2026 International Meeting with integrated registration system.

![Brand Colors](https://img.shields.io/badge/Navy_Blue-%2328478a-28478a)
![Brand Colors](https://img.shields.io/badge/Beige-%23e4e3dd-e4e3dd)
![Brand Colors](https://img.shields.io/badge/Burnt_Orange-%23c45508-c45508)

## 🌟 Features

### Website Pages
- **Homepage** - Animated hero with rain effect, lighthouse beam, and featured 2026 Meeting banner
- **2026 Meeting** - Event details with prominent form access cards
- **About** - Church history, mission, and 4 elders
- **Ministries** - Youth, Prayer, Bible Study, Music, and Sunday School programs
- **Give** - Multiple giving options (PayPal, Zelle, GoFundMe)
- **Contact** - Service times, address, map, contact form, and social media links
- **Events** - Event calendar and 2026 Meeting information
- **Gallery** - Photo albums (placeholder for future content)

### Custom Forms System
- **Registration Form** - 3-phase attendee registration with transportation and child care
- **Volunteer Form** - Committee selection with intelligent availability matrix
- **Vendor Application** - Business application with approval workflow

### Backend Features
- **Firebase Firestore** - Complete data ownership and storage
- **Email Notifications** - Automated confirmations via EmailJS
- **Admin Dashboard** - View and manage all submissions
- **Data Export** - CSV/Excel export for analytics
- **Secure Authentication** - Firebase Auth for admin access

## 📁 Project Structure

```
VS-Code/
├── index.html                    # Homepage with animated hero
├── 2026-meeting.html             # Event page with form access
├── about.html                    # About page with elders
├── ministries.html               # Ministries overview
├── give.html                     # Giving options
├── contact.html                  # Contact information
├── events.html                   # Events calendar
├── gallery.html                  # Photo gallery
│
├── forms/
│   ├── registration.html         # 3-phase registration form
│   ├── volunteer.html            # Volunteer sign-up form
│   └── vendor.html               # Vendor application form
│
├── css/
│   ├── design-system.css         # Core design system & form styles
│   └── pages.css                 # Website page layouts
│
├── js/
│   ├── main.js                   # Website interactivity & animations
│   ├── registration-form.js      # Registration form logic
│   ├── volunteer-form.js         # Volunteer form with matrix
│   ├── vendor-form.js            # Vendor form logic
│   └── admin-dashboard.js        # Admin data management
│
├── config/
│   └── firebase-config.js        # Firebase & EmailJS configuration
│
├── admin/
│   └── dashboard.html            # Admin dashboard for data management
│
├── docs/
│   ├── DESIGN_ANALYSIS.md        # Complete brand guidelines
│   ├── REGISTRATION_FORM_SPEC.md # Registration form specifications
│   └── VOLUNTEER_VENDOR_FORMS_SPEC.md # Volunteer & vendor specs
│
├── DEPLOYMENT_GUIDE.md           # Complete deployment instructions
└── README.md                     # This file
```

## 🎨 Design System

### Brand Colors
```css
--navy-blue: #28478a;      /* Primary brand color */
--beige: #e4e3dd;          /* Secondary background */
--burnt-orange: #c45508;   /* Accent color */
--off-white: #f1f1f1;      /* Light backgrounds */
--dark-gray: #6e6a67;      /* Body text */
--charcoal: #4d4d4d;       /* Headings */
```

### Typography
- **Display:** The Seasons (Canva library)
- **Body:** Source Serif Pro, Alegreya
- **UI:** Lato, Canva Sans

### Design Elements
- Nautical theme with lighthouse and anchor motifs
- Gold accents and decorative borders
- Photo treatments with rounded corners and soft shadows
- Gradient backgrounds for visual depth

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/TheTracyTimes/VS-Code.git
cd VS-Code
```

### 2. Configure Backend Services

**Firebase Setup:**
1. Create Firebase project at [console.firebase.google.com](https://console.firebase.google.com/)
2. Enable Firestore Database
3. Enable Email/Password Authentication
4. Copy configuration to `config/firebase-config.js`

**EmailJS Setup:**
1. Create account at [emailjs.com](https://www.emailjs.com/)
2. Configure email service (Gmail recommended)
3. Create three email templates (registration, volunteer, vendor)
4. Copy credentials to `config/firebase-config.js`

**See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.**

### 3. Deploy to Netlify
```bash
# Push to GitHub
git add .
git commit -m "Configure backend services"
git push origin main

# Deploy via Netlify dashboard
# Connect GitHub repository
# Deploy from main branch
```

### 4. Test Everything
- Submit test forms
- Verify email notifications
- Check admin dashboard
- Test on mobile devices

## 📋 Form Specifications

### Registration Form (3 Phases)
**Phase 1: Basic Information**
- Personal details (name, church, pastor)
- Contact information (email, phone)
- Service attendance preferences (6 checkboxes)

**Phase 2: Transportation**
- Arrival/departure details
- Airport transportation needs (conditional)
- Local transportation preferences

**Phase 3: Child Care**
- VBS registration with age validation
- Nursery needs with age validation
- Child information forms

### Volunteer Form
**Features:**
- 11 committee options
- 6 availability time slots
- Intelligent committee-availability matrix
  - Only appears if multiple committees selected
  - Assigns specific committee to each time slot
- Skills and experience section

### Vendor Application
**Features:**
- Business information
- Goods/Services selection
- Conditional goods type (Perishable/Non-Perishable)
- Website validation (accepts URL or "N/A")
- Description and special requirements
- Approval workflow

## 🔐 Security

### Firestore Security Rules
```javascript
// Allow public form submissions
// Restrict admin access to authenticated users only
match /registrations/{document} {
  allow create: if true;
  allow read, update, delete: if request.auth != null;
}
```

### Admin Dashboard
- Firebase Authentication required
- Secure credential management
- Optional Netlify password protection

## 📊 Data Management

### Viewing Submissions
**Admin Dashboard:** `your-site.com/admin/dashboard.html`
- Real-time data viewing
- Search and filter capabilities
- Vendor approval workflow

**Firebase Console:** Direct database access
- Navigate to Firestore collections
- View raw submission data

### Exporting Data
- Click "Export to Excel" in admin dashboard
- Opens CSV file for analysis in Excel/Google Sheets
- Includes all submission fields and timestamps

## 📱 Mobile Responsive

All pages optimized for:
- iPhone (iOS Safari)
- Android phones (Chrome)
- Tablets (iPad)
- Desktop browsers

Features:
- Hamburger navigation menu
- Touch-friendly form controls
- Optimized images and animations
- Readable typography on small screens

## 🎯 Key User Flows

### Registering for 2026 Meeting
1. Visit homepage or events page
2. Click "2026 International Meeting" banner
3. Select "Attendee Registration" card
4. Complete 3-phase registration form
5. Receive email confirmation

### Volunteering
1. Navigate to 2026 Meeting page
2. Click "Volunteer Sign-Up" card
3. Select committees and availability
4. Assign committees to time slots (if applicable)
5. Submit and receive confirmation

### Vendor Application
1. Navigate to 2026 Meeting page
2. Click "Vendor Application" card
3. Complete business information
4. Select goods/services details
5. Await approval from admin

## 🔧 Customization

### Updating Content
**Church Information:**
- Edit `contact.html` for address, phone, email
- Update service times in `contact.html` and `index.html`
- Modify footer in all pages for universal changes

**Adding Photos:**
- Replace emoji placeholders in `about.html` (elder photos)
- Add images to `/images/gallery/` folders
- Update `gallery.html` with photo links

**Modifying Forms:**
- Edit HTML in `/forms/` directory
- Update JavaScript logic in `/js/` directory
- Adjust validation rules as needed

### Adding New Pages
1. Create new HTML file in root directory
2. Include design-system.css and pages.css
3. Copy navigation and footer from existing pages
4. Add link to navigation in all pages

## 📚 Documentation

- **[DESIGN_ANALYSIS.md](docs/DESIGN_ANALYSIS.md)** - Complete brand guidelines and design system
- **[REGISTRATION_FORM_SPEC.md](docs/REGISTRATION_FORM_SPEC.md)** - Detailed registration form specifications
- **[VOLUNTEER_VENDOR_FORMS_SPEC.md](docs/VOLUNTEER_VENDOR_FORMS_SPEC.md)** - Volunteer and vendor form specifications
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Complete deployment instructions

## 🌐 Social Media

- **Website:** [sarasotagospeltemple.org](https://www.sarasotagospeltemple.org)
- **Facebook:** [@sarasotagospeltemple](https://www.facebook.com/people/Sarasota-Gospel-Temple/61557296390196/)
- **Instagram:** [@sarasotagospeltemple](https://www.instagram.com/sarasotagospeltemple/)
- **YouTube:** [@sarasotagospeltemple](https://www.youtube.com/@sarasotagospeltemple)
- **Linktree:** [linktr.ee/sarasotagospeltemple](https://www.linktr.ee/sarasotagospeltemple)

## 📞 Contact

**Sarasota Gospel Temple**
- **Address:** 3629 Tallevast Road, Sarasota, FL 34243
- **Email:** sarasotagospel@gmail.com
- **Phone:** (941) 800-5211

**Service Times:**
- Sunday Morning: 10:00 AM
- Sunday Evening: 6:00 PM
- Wednesday: 7:00 PM

## ✨ Highlights

### Technical Excellence
- ✅ Vanilla JavaScript (no frameworks needed)
- ✅ Complete data ownership (your own database)
- ✅ Mobile-first responsive design
- ✅ Semantic HTML5 markup
- ✅ CSS custom properties for consistency
- ✅ Progressive form navigation
- ✅ Real-time validation
- ✅ Automated email notifications
- ✅ Secure admin authentication
- ✅ Data export for analytics

### Design Excellence
- ✅ Brand-consistent styling throughout
- ✅ Nautical theme with lighthouse/anchor motifs
- ✅ Smooth animations and transitions
- ✅ Professional photography treatments
- ✅ Accessibility considerations
- ✅ Print-friendly layouts

### User Experience
- ✅ Intuitive navigation
- ✅ Clear call-to-action buttons
- ✅ Multi-step forms with progress indicators
- ✅ Conditional logic for relevant fields only
- ✅ Helpful error messages
- ✅ Mobile-optimized touch targets

## 🎉 2026 International Meeting

**April 9-11, 2026**

Join us for three days of worship, fellowship, and spiritual renewal at Sarasota Gospel Temple's International Meeting!

### Event Schedule
- **Thursday, April 9th** - Welcome Service (7:00 PM)
- **Friday, April 10th** - All-day Conference
- **Saturday, April 11th** - Closing Celebration

### Registration Open
Forms are now live and accessible via the 2026 Meeting page. Register early for:
- VBS and Nursery spots (limited availability)
- Volunteer committee positions
- Vendor booth space

---

## 📝 License

This website was custom-built for Sarasota Gospel Temple. All rights reserved.

## 🙏 Acknowledgments

Built with care for the Sarasota Gospel Temple community, incorporating feedback and requirements for complete data ownership, brand consistency, and user-friendly functionality.

---

**Ready to launch your website?** Follow the [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) to go live!

*Last updated: January 2026*
