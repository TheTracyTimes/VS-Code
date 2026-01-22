# 2026 International Meeting - Registration Form Specification

## Overview
Multi-phase registration form for the Sarasota Gospel Temple 2026 International Meeting (April 9-11, 2026).

**Form Type**: Multi-step (3 phases)
**Event**: 2026 International Meeting
**Dates**: April 9-11, 2026
**Location**: 1900 Gandy Blvd N, St. Petersburg, FL 33702

---

## Form Structure

### Phase 1: Basic Information

| Field | Type | Required | Validation | Notes |
|-------|------|----------|------------|-------|
| First and Last Name | Text | Yes* | Min 2 chars | Single field or split into two |
| Phone Number (with country code) | Tel | Yes* | International format | Include country code dropdown |
| Email Address | Email | No | Valid email format | Optional for accessibility |
| Name of your Pastor | Text | Yes* | Min 2 chars | |
| Name of your Assembly | Text | No | | Church/congregation name |
| Services of Attendance | Checkbox (Multiple) | Yes* | Min 1 selection | See options below |

**Services of Attendance Options**:
- [ ] Thursday Morning Service, April 9th
- [ ] Thursday Night Service, April 9th
- [ ] Friday Morning Service, April 10th
- [ ] Friday Night Service, April 10th
- [ ] Saturday Morning Service, April 11th
- [ ] Saturday Youth Night, April 11th

---

### Phase 2: Transportation

| Field | Type | Required | Validation | Notes |
|-------|------|----------|------------|-------|
| Do you need transportation from the airport? | Radio | Yes* | Single selection | Yes/No |
| **ARRIVAL INFORMATION** | | | | |
| Arrival Time | Text/DateTime | Yes* | Time format | "N/A" if not applicable |
| Airline (Arrival) | Text | Yes* | | "N/A" if not applicable |
| Airport (Arrival) | Text | Yes* | | "N/A" if not applicable |
| Flight Number (Arrival) | Text | Yes* | Alphanumeric | "N/A" if not applicable |
| Number of people with you | Number | Yes* | >= 0 | "N/A" if not applicable |
| **DEPARTURE INFORMATION** | | | | |
| Departure Time | Text/DateTime | Yes* | Time format | "N/A" if not applicable |
| Airline (Departure) | Text | Yes* | | "N/A" if not applicable |
| Airport (Departure) | Text | Yes* | | "N/A" if not applicable |
| Flight Number (Departure) | Text | Yes* | Alphanumeric | "N/A" if not applicable |
| **LOCAL TRANSPORTATION** | | | | |
| Will you need transportation during the meeting? | Radio | Yes* | Single selection | Yes/No |
| If yes, pickup location | Textarea | Conditional | Required if "Yes" above | Hotel name/address |

**Smart Form Logic**:
- If "Do you need transportation from airport" = "No", pre-fill all flight fields with "N/A"
- If "Will you need transportation during meeting" = "No", hide pickup location field
- Show helper text: "Please enter N/A if not applicable" for conditional fields

---

### Phase 3: Child Care

| Field | Type | Required | Validation | Notes |
|-------|------|----------|------------|-------|
| Will you have children under 5? | Radio | Yes* | Single selection | Yes/No |
| If yes, how many? | Number | Conditional | > 0 if "Yes" | Only show if "Yes" above |
| Will your child/children attend VBS (Vacation Bible School)? | Radio | Yes* | Single selection | Yes/No |
| If yes, how many will attend VBS? | Number | Conditional | > 0 if "Yes" | Only show if "Yes" above |
| Will your child/children be in the nursery during service? | Radio | Yes* | Single selection | Yes/No |
| If yes, how many children in the nursery? | Number | Conditional | > 0 if "Yes" | Only show if "Yes" above |

**Smart Form Logic**:
- If "Will you have children under 5?" = "No", auto-set VBS and nursery to "No"
- Show child count fields only when relevant "Yes" is selected
- Validate that child counts are logical (nursery + VBS ≤ total children)

---

## Technical Implementation

### Form Technology Stack Options

**Option 1: HTML5 + JavaScript** (Recommended for simplicity)
- Native form validation
- Custom JavaScript for multi-step progression
- Local storage for draft saving

**Option 2: Form Builder Service**
- Google Forms (free, easy integration)
- Typeform (beautiful UI, paid)
- JotForm (good features, freemium)
- FormStack (enterprise, paid)

**Option 3: Custom React/Vue Form**
- Full control over UX
- Better validation and conditional logic
- Requires more development time

### Form Submission

**Recommended Backend Options**:
1. **Google Sheets** (Free, easy setup)
   - Use Google Forms or FormSubmit.co
   - Auto-populate spreadsheet
   - Easy to export and manage

2. **Email Notification** (Simple)
   - FormSubmit, FormSpree, or custom PHP
   - Send formatted email with responses
   - Requires email backup/organization

3. **Database** (Most robust)
   - Firebase, Airtable, or custom backend
   - Structured data storage
   - Query and reporting capabilities

**Recommended**: Google Forms → Google Sheets for easy management and no cost

### Data Collection & Storage

**Required Data Handling**:
- Store submissions securely
- Export to Excel/CSV for review
- Email confirmations to registrants
- Admin notification on new registration

**Data Privacy**:
- GDPR/privacy policy notice
- Secure transmission (HTTPS)
- Data retention policy
- Option to delete/update registration

---

## User Experience Design

### Progress Indicator
```
[●●●○] Phase 1: Basic Info → Phase 2: Transportation → Phase 3: Child Care → Submit
```

**Visual Design**:
- Show current phase highlighted (Navy Blue #28478a)
- Completed phases with checkmark
- Upcoming phases in light gray

### Phase Navigation

**Phase 1 → Phase 2**:
- "Continue to Transportation" button (Navy Blue background)
- Validate all required fields before proceeding

**Phase 2 → Phase 3**:
- "Continue to Child Care" button
- "Back to Basic Info" link (light gray)

**Phase 3 → Submit**:
- "Submit Registration" button (Burnt Orange #c45508)
- "Back to Transportation" link
- Review summary before submit (optional)

### Field Layout

**Desktop (2-column)**:
```
[ First Name          ] [ Last Name           ]
[ Phone Number        ] [ Email               ]
```

**Mobile (1-column)**:
```
[ First Name                              ]
[ Last Name                               ]
[ Phone Number                            ]
```

### Styling Guidelines

**Form Container**:
- Max width: 800px
- Background: White or Off-White (#f1f1f1)
- Padding: 40px
- Border-radius: 8px
- Box shadow: subtle

**Input Fields**:
- Border: 1px solid Dark Gray (#6e6a67)
- Border-radius: 4px
- Padding: 12px 16px
- Font: Canva Sans or Source Serif Pro
- Focus state: Navy Blue border (#28478a)

**Labels**:
- Font: Source Serif Pro or Canva Sans
- Color: Charcoal (#4d4d4d)
- Required indicator: Burnt Orange asterisk (#c45508)
- Font-size: 14-16px

**Buttons**:
- Primary (Submit): Burnt Orange background (#c45508), white text
- Secondary (Continue): Navy Blue background (#28478a), white text
- Padding: 14px 28px
- Border-radius: 4px
- Font: Canva Sans, semi-bold
- Hover: Darken by 10%

**Helper Text**:
- Font-size: 12-14px
- Color: Dark Gray (#6e6a67)
- Italic style
- Below relevant fields

**Error Messages**:
- Color: Red (#d32f2f)
- Font-size: 13px
- Icon: ⚠️ or ✕
- Below field with error

**Success Message** (after submission):
- Checkmark icon ✓
- Navy Blue background (#28478a)
- White text
- Confirmation number
- Next steps information

---

## Form Validation Rules

### Phase 1 Validation
- [ ] First and Last Name: Not empty, min 2 characters
- [ ] Phone Number: Valid international format (regex)
- [ ] Email: Valid email format or empty
- [ ] Pastor Name: Not empty, min 2 characters
- [ ] Services: At least one checkbox selected

### Phase 2 Validation
- [ ] Airport transportation: Must select Yes or No
- [ ] If transportation needed:
  - All arrival fields must be filled (or N/A)
  - All departure fields must be filled (or N/A)
  - Number of people must be >= 0
- [ ] Local transportation: Must select Yes or No
- [ ] If local transportation needed: Pickup location required

### Phase 3 Validation
- [ ] Children under 5: Must select Yes or No
- [ ] If yes: Child count must be > 0
- [ ] VBS attendance: Must select Yes or No
- [ ] If VBS yes: VBS count must be > 0
- [ ] Nursery attendance: Must select Yes or No
- [ ] If nursery yes: Nursery count must be > 0
- [ ] Logic check: VBS + Nursery ≤ Total children under 5

---

## Confirmation & Follow-up

### Confirmation Email Template

**Subject**: Registration Confirmed - 2026 International Meeting

**Body**:
```
Dear [First Name] [Last Name],

Thank you for registering for the Sarasota Gospel Temple 2026 International Meeting!

EVENT DETAILS:
📅 Dates: April 9-11, 2026
📍 Location: 1900 Gandy Blvd N, St. Petersburg, FL 33702
📞 Contact: 941-667-0526

YOUR REGISTRATION:
Services Attending: [List of selected services]
Transportation Needed: [Yes/No]
Children Attending: [Yes/No - count if applicable]

We look forward to seeing you at the meeting! If you need to update your registration, please contact us at [email].

Blessings,
Sarasota Gospel Temple

---
This is an automated confirmation. Please do not reply to this email.
```

### Admin Notification

**Send to**: Church admin email
**Include**: All form responses in structured format
**Trigger**: Immediately upon form submission

---

## Additional Features (Optional Enhancements)

### Nice-to-Have Features:
1. **Draft Saving**: Auto-save progress to browser localStorage
2. **Edit Registration**: Allow users to update their registration via unique link
3. **QR Code**: Generate QR code for registration confirmation
4. **Calendar Integration**: Add events to Google/Apple Calendar
5. **Payment Integration**: If registration fee required (future)
6. **Waitlist**: If capacity limits reached
7. **Attendance Tracking**: QR code check-in system at event
8. **SMS Notifications**: Text reminders before event
9. **Multi-language**: Haitian Creole, Spanish options
10. **Export to PDF**: Printable registration summary

---

## Testing Checklist

### Functionality Testing:
- [ ] All required fields validate correctly
- [ ] Conditional logic shows/hides fields properly
- [ ] Phone number accepts international formats
- [ ] Email validation works correctly
- [ ] Multi-select checkboxes allow multiple selections
- [ ] Phase progression works in both directions
- [ ] Form submits successfully
- [ ] Confirmation email sends correctly
- [ ] Admin notification receives all data
- [ ] Data stores in database/spreadsheet correctly

### Browser Testing:
- [ ] Chrome (desktop & mobile)
- [ ] Firefox
- [ ] Safari (desktop & mobile)
- [ ] Edge
- [ ] Samsung Internet (mobile)

### Responsive Testing:
- [ ] Mobile portrait (320px - 480px)
- [ ] Mobile landscape (481px - 767px)
- [ ] Tablet (768px - 1024px)
- [ ] Desktop (1025px+)

### Accessibility Testing:
- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] ARIA labels present
- [ ] Color contrast meets WCAG AA
- [ ] Focus indicators visible
- [ ] Error messages announced

---

## Implementation Timeline

**Phase 1**: Design & Setup (Week 1)
- Create form mockup/wireframe
- Set up Google Form or custom HTML
- Design visual styling

**Phase 2**: Development (Week 2)
- Build multi-step form logic
- Implement validation
- Create confirmation emails
- Set up data collection

**Phase 3**: Testing (Week 3)
- Test all functionality
- Cross-browser testing
- Mobile responsiveness
- User acceptance testing

**Phase 4**: Launch (Week 4)
- Deploy to website
- Test in production
- Monitor submissions
- Gather feedback

---

## Support & Maintenance

**Pre-Event**:
- Monitor registrations weekly
- Export data for planning
- Send reminder emails
- Update capacity if needed

**During Event**:
- Have registration desk for on-site registration
- Print registration list for check-in
- Handle last-minute changes

**Post-Event**:
- Send thank you emails
- Archive registration data
- Review process for improvements
- Plan for next year

---

## Contact Information for Form Support

**Technical Issues**: [website admin email]
**Registration Questions**: 941-667-0526
**General Inquiries**: tracykmussotte@gmail.com

---

## Notes for Developers

- Use semantic HTML5 form elements
- Ensure HTTPS for form submission
- Implement CSRF protection
- Sanitize all inputs server-side
- Use progressive enhancement (works without JavaScript)
- Consider rate limiting to prevent spam
- Add honeypot field for bot detection
- Store timestamps for each submission
- Log IP addresses (optional, for security)
- Regular backup of registration data

---

**Last Updated**: 2026-01-22
**Version**: 1.0
**Status**: Specification Complete - Ready for Development
