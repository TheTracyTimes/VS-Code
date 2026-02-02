# Volunteer & Vendor Forms Specification
## 2026 International Meeting - Sarasota Gospel Temple

---

## Volunteer Sign-Up Form

### Form Overview
**Purpose**: Recruit and organize volunteers for the 2026 International Meeting
**Type**: Single-page form with conditional logic
**Submission**: Email + Google Sheets

---

### Volunteer Form Fields

| Field | Type | Required | Validation | Notes |
|-------|------|----------|------------|-------|
| First and Last Name | Text | Yes* | Min 2 chars | Single or split field |
| Phone Number (with country code) | Tel | Yes* | International format | Country code dropdown |
| Email Address | Email | Yes* | Valid email | Required for confirmation |
| Committee Selection | Checkbox (Multiple) | Yes* | Min 1 selection | See options below |
| Availability | Checkbox (Multiple) | Yes* | Min 1 selection | See time slots below |
| Committee-Availability Matrix | Dynamic Table | Conditional | Required if multiple committees | Assign committee to each time slot |

**Committee Options**:
- [ ] Dining Room
- [ ] Nursery
- [ ] Usher
- [ ] Transportation
- [ ] Cleaning
- [ ] Interpretation
- [ ] Media
- [ ] Singers
- [ ] Musician
- [ ] Medical
- [ ] Floater (Wherever Needed)

**Availability Time Slots**:
- [ ] Thursday Morning, April 9th
- [ ] Thursday Afternoon, April 9th
- [ ] Friday Morning, April 10th
- [ ] Friday Afternoon, April 10th
- [ ] Saturday Morning, April 11th
- [ ] Saturday Afternoon, April 11th

### Conditional Logic: Committee-Availability Matrix

**Trigger**: If user selects MORE than one committee
**Action**: Show additional field

**Matrix Format**:
```
For each time slot selected, specify which committee:

Thursday Morning, April 9th: [Dropdown: Select Committee]
Thursday Afternoon, April 9th: [Dropdown: Select Committee]
Friday Morning, April 10th: [Dropdown: Select Committee]
...
```

**Dropdown Options**: Only show committees the user selected in Question 4

**Example**:
- User selects: Usher, Media, Floater
- User selects availability: Thursday Morning, Friday Morning
- Matrix shows:
  ```
  Thursday Morning: [Dropdown: Usher, Media, or Floater]
  Friday Morning: [Dropdown: Usher, Media, or Floater]
  ```

**Validation**:
- Required if more than one committee selected
- Each time slot must have a committee assigned
- Cannot leave any dropdown empty

---

## Vendor Application Form

### Form Overview
**Purpose**: Manage vendor applications for the meeting marketplace
**Type**: Single-page form with conditional fields
**Submission**: Email + Google Sheets (requires approval workflow)

---

### Vendor Form Fields

| Field | Type | Required | Validation | Notes |
|-------|------|----------|------------|-------|
| First and Last Name | Text | Yes* | Min 2 chars | Contact person |
| Business Name | Text | Yes* | Min 2 chars | |
| Phone Number | Tel | Yes* | Valid format | |
| Email Address | Email | Yes* | Valid email | |
| Website | URL | Yes* | Valid URL or "N/A" | Accept "N/A" as valid |
| Name of your Pastor | Text | Yes* | Min 2 chars | |
| Name of your Assembly | Text | No | | Optional field |
| What are you selling? | Radio | Yes* | Single selection | Goods or Services |
| If goods, what kind? | Radio | Conditional | Required if "Goods" | Perishable/Non-perishable |
| Will you have someone at the table? | Radio | Yes* | Single selection | Yes/No |
| Availability | Checkbox (Multiple) | Yes* | Min 1 selection | See time slots below |

**Selling Type Options**:
- ( ) Goods
- ( ) Services

**Goods Type Options** (shown only if "Goods" selected):
- ( ) Perishable
- ( ) Non-Perishable

**Table Staffing**:
- ( ) Yes - I will have someone at my table
- ( ) No - My table will be unattended

**Availability Time Slots**:
- [ ] Thursday Morning, April 9th
- [ ] Thursday Afternoon, April 9th
- [ ] Friday Morning, April 10th
- [ ] Friday Afternoon, April 10th
- [ ] Saturday Morning, April 11th
- [ ] Saturday Afternoon, April 11th

### Conditional Logic

**Question 8 → Question 9**:
- IF "What are you selling?" = "Goods"
  - THEN show "If goods, what kind?"
- IF "What are you selling?" = "Services"
  - THEN hide/skip Question 9

### Vendor Approval Workflow

**Step 1**: Vendor submits application
**Step 2**: Admin receives notification email
**Step 3**: Admin reviews application
**Step 4**: Admin approves/denies vendor
**Step 5**: Vendor receives approval email with next steps

**Approval Email Template**:
```
Subject: Vendor Application Approved - 2026 International Meeting

Dear [Business Name],

Your vendor application has been approved for the Sarasota Gospel Temple 2026 International Meeting!

NEXT STEPS:
1. Review vendor guidelines (attached)
2. Confirm your setup time
3. Submit booth fee payment (if applicable)
4. Provide liability insurance (if applicable)

YOUR APPLICATION:
Business: [Business Name]
Contact: [Name]
Selling: [Goods/Services]
Availability: [Selected times]

Please contact us at 941-800-5211 with any questions.

Blessings,
Sarasota Gospel Temple Vendor Coordination Team
```

---

## Form Design & Styling

### Visual Design (Applies to Both Forms)

**Form Header**:
- Navy Blue background (#28478a)
- White text
- Form title in The Seasons font
- Brief description in Source Serif Pro
- Decorative lighthouse watermark (faded)

**Form Container**:
- Max width: 900px
- Background: White or Off-White (#f1f1f1)
- Padding: 40px desktop, 20px mobile
- Border-radius: 8px
- Subtle shadow: 0 2px 8px rgba(0,0,0,0.1)

**Section Dividers**:
- Thin line: 1px solid #6e6a67
- Section headers in Alegreya, 20px
- Optional: Anchor icon before section name

**Input Styling**:
- Border: 1px solid #6e6a67
- Border-radius: 4px
- Padding: 12px 16px
- Font: Source Serif Pro, 16px
- Focus: Navy Blue border (#28478a), subtle glow
- Placeholder: Dark Gray (#6e6a67), italic

**Checkboxes & Radio Buttons**:
- Custom styled with Navy Blue (#28478a)
- Larger touch targets (minimum 44px x 44px)
- Label clickable
- Checked state: Navy Blue fill

**Submit Button**:
- Background: Burnt Orange (#c45508)
- Text: White (#f1f1f1)
- Font: Canva Sans, semi-bold, 16px
- Padding: 16px 32px
- Border-radius: 4px
- Width: Full width on mobile, auto on desktop
- Hover: Darken 10%, slight scale (1.02)
- Cursor: pointer

**Required Field Indicator**:
- Burnt Orange asterisk (#c45508)
- Positioned after label
- Font-size: 18px

**Helper Text**:
- Font: Source Serif Pro, 14px, italic
- Color: Dark Gray (#6e6a67)
- Margin-top: 4px

---

## Form Validation

### Volunteer Form Validation
- [ ] Name: Not empty, min 2 characters
- [ ] Phone: Valid international format
- [ ] Email: Valid email format
- [ ] Committees: At least one selected
- [ ] Availability: At least one time slot selected
- [ ] Matrix: If multiple committees, all time slots must have committee assigned

### Vendor Form Validation
- [ ] Name: Not empty, min 2 characters
- [ ] Business Name: Not empty, min 2 characters
- [ ] Phone: Valid format
- [ ] Email: Valid email format
- [ ] Website: Valid URL or exactly "N/A" (case insensitive)
- [ ] Pastor Name: Not empty, min 2 characters
- [ ] Assembly: No validation (optional)
- [ ] Selling Type: Must select one option
- [ ] Goods Type: Required only if "Goods" selected
- [ ] Table Staffing: Must select one option
- [ ] Availability: At least one time slot selected

### Error Messages

**Empty Required Field**:
"This field is required."

**Invalid Email**:
"Please enter a valid email address."

**Invalid Phone**:
"Please enter a valid phone number with country code."

**Invalid Website**:
"Please enter a valid URL or 'N/A' if you don't have a website."

**No Selection**:
"Please select at least one option."

**Matrix Incomplete**:
"Please assign a committee for each time slot you selected."

---

## Confirmation Messages

### Volunteer Form Success
```
✓ Thank you for volunteering!

Your volunteer registration has been received. We'll contact you at [email] with more details about your role.

Committee(s): [List]
Availability: [List]

Blessings,
Sarasota Gospel Temple
```

### Vendor Form Success
```
✓ Vendor application submitted!

Thank you for your interest in being a vendor at the 2026 International Meeting.

Your application is under review. You'll receive an email at [email] within 3-5 business days regarding your application status.

Business: [Business Name]
Contact: [Name]

Questions? Call 941-800-5211

Blessings,
Sarasota Gospel Temple
```

---

## Data Management

### Export Format (Google Sheets)

**Volunteer Sheet Columns**:
| Timestamp | Name | Phone | Email | Committees | Availability | Matrix | Status |
|-----------|------|-------|-------|------------|--------------|--------|--------|

**Vendor Sheet Columns**:
| Timestamp | Name | Business | Phone | Email | Website | Pastor | Assembly | Type | Goods Type | Staffed | Availability | Status | Approved By | Notes |
|-----------|------|----------|-------|-------|---------|--------|----------|------|------------|---------|--------------|--------|-------------|-------|

### Admin Dashboard Needs

**Volunteer Management**:
- Filter by committee
- Filter by availability
- Export to CSV
- Print roster
- Send group emails

**Vendor Management**:
- Approve/Deny applications
- Filter by type (goods/services)
- Filter by availability
- Assign booth numbers
- Track payment status
- Send vendor communications

---

## Mobile Responsiveness

### Key Mobile Optimizations:

**Checkboxes/Radio Lists**:
- Stack vertically
- Full width
- Larger touch targets (min 44px)
- More spacing between options

**Phone Number Input**:
- Trigger numeric keyboard
- Country code selector easily accessible

**Availability Grid**:
- Consider accordion on mobile
- Or single column layout with clear labels

**Committee-Availability Matrix**:
- Stack dropdowns vertically
- Clear labels for each time slot
- Group by day for easier scanning

**Submit Button**:
- Fixed to bottom on mobile (optional)
- Full width
- Always visible/accessible

---

## Accessibility Requirements

### WCAG 2.1 AA Compliance:

**Keyboard Navigation**:
- All fields accessible via Tab
- Checkboxes/radios via Space
- Submit via Enter

**Screen Readers**:
- Proper labels for all inputs
- ARIA labels for complex fields
- Error announcements
- Success message announced

**Color Contrast**:
- Text: 4.5:1 minimum
- UI elements: 3:1 minimum
- Don't rely on color alone

**Focus Indicators**:
- Visible focus outline
- Navy Blue outline (#28478a)
- 2px solid, offset

**Labels & Instructions**:
- Clear, concise labels
- Instructions before fields
- Error messages associated with fields

---

## Advanced Features (Optional)

### Volunteer Form Enhancements:
1. **Skills Matrix**: Add skills/experience checkboxes
2. **Shift Preferences**: Morning person vs night owl
3. **T-Shirt Size**: For volunteer shirts
4. **Emergency Contact**: Name and phone
5. **Special Accommodations**: Wheelchair, interpreter needs
6. **Previous Experience**: Volunteer history

### Vendor Form Enhancements:
1. **Photo Upload**: Product photos (max 3)
2. **Booth Size**: Table size preference
3. **Power Needs**: Electricity required (yes/no)
4. **Setup Requirements**: Special needs
5. **Insurance Upload**: Liability insurance certificate
6. **References**: Previous events
7. **Product Description**: Textarea for details
8. **Pricing Range**: $ - $$$ indicator
9. **Social Media**: Instagram, Facebook handles

---

## Integration with Main Website

### Navigation Path:
```
Home > 2026 International Meeting > Get Involved

[Registration] [Volunteer] [Vendor]
    ↓             ↓          ↓
  Forms        Forms      Forms
```

### Page Layout:
```
[Hero: "Join Us - 2026 International Meeting"]
[Navy Blue Section]

[Three Cards: Attend | Volunteer | Sell]
    Each card links to respective form

[Info Section: What to Expect]
[Contact Section: Questions?]
```

---

## Testing Scenarios

### Volunteer Form Tests:
1. Submit with single committee → should NOT show matrix
2. Submit with multiple committees → SHOULD show matrix
3. Try submitting matrix incomplete → should show error
4. Select all committees → verify all appear in matrix dropdowns
5. Change committee selection → verify matrix updates
6. Submit valid form → check data in spreadsheet
7. Verify confirmation email sends

### Vendor Form Tests:
1. Select "Services" → goods type should hide
2. Select "Goods" → goods type should show and be required
3. Submit with "Goods" but no type → should error
4. Enter invalid website → should error
5. Enter "N/A" for website → should accept
6. Enter "n/a" for website → should accept (case insensitive)
7. Submit valid form → check data in spreadsheet
8. Verify admin notification email

---

## Support Documentation

### For Volunteers:
- Volunteer handbook
- Committee descriptions
- What to expect
- Dress code
- Parking information
- Meal information

### For Vendors:
- Vendor guidelines PDF
- Booth setup instructions
- Load-in times
- Prohibited items list
- Payment information
- Booth dimensions/layout
- Power availability
- Insurance requirements

---

**Last Updated**: 2026-01-22
**Version**: 1.0
**Status**: Specification Complete
