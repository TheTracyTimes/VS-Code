# 🌐 DNS Setup Guide - Complete Step-by-Step Instructions

**IMPORTANT:** Read this entire guide before making any changes!

---

## 📋 BEFORE YOU START - CHECKLIST

- [ ] You have access to your Wix account (where your domain is)
- [ ] You know your exact domain name (e.g., sarasotagospeltemple.com)
- [ ] You have 30-45 minutes to complete this without interruption
- [ ] You've deployed your site to Firebase or Netlify (we'll do this together)

---

## ⚠️ IMPORTANT WARNINGS

1. **DO NOT delete all your existing DNS records!** Only modify what we tell you to modify.
2. **DO keep:** MX records (email), TXT records (email verification), any records you don't recognize
3. **DNS changes take time:** Changes can take 5 minutes to 48 hours to work worldwide
4. **Your email won't break:** We're only changing website hosting, not email
5. **You can reverse changes:** DNS changes are reversible if something goes wrong

---

## 🔥 OPTION 1: FIREBASE HOSTING (RECOMMENDED)

### Why Firebase?
- ✅ Your backend is already on Firebase
- ✅ Everything in one place (easier to manage)
- ✅ Free tier: 10 GB storage, 10 GB/month bandwidth
- ✅ Automatic SSL certificate
- ✅ Global CDN for fast loading

---

### STEP 1: Deploy Your Site to Firebase

**On your local computer**, open Terminal/Command Prompt and navigate to your project folder:

```bash
# 1. Make sure you're in the project directory
cd /path/to/VS-Code

# 2. Login to Firebase (browser will open)
firebase login

# 3. Check which project you're using
firebase projects:list

# 4. Make sure you're using the right project
firebase use sarasota-gospel-temple

# 5. Deploy everything
firebase deploy

# Or deploy just hosting:
firebase deploy --only hosting
```

**What you'll see:**
```
✔  Deploy complete!

Project Console: https://console.firebase.google.com/project/sarasota-gospel-temple/overview
Hosting URL: https://sarasota-gospel-temple.web.app
```

**✅ Success Check:** Visit the Hosting URL. If your site loads, you're ready for Step 2!

---

### STEP 2: Add Your Custom Domain in Firebase Console

1. **Go to Firebase Console:**
   - Visit: https://console.firebase.google.com/
   - Click on your project: **sarasota-gospel-temple**

2. **Navigate to Hosting:**
   - Click **Hosting** in the left sidebar
   - Click the **Add custom domain** button

3. **Enter Your Domain:**
   - Type your domain name (e.g., `sarasotagospeltemple.com`)
   - Click **Continue**

4. **Choose Domain Type:**
   - Select **"I own this domain"**
   - Click **Continue**

5. **Firebase will show you DNS records:**

   You'll see a screen like this:

   ```
   Add these DNS records to your domain provider:

   Type    Name/Host    Value/Points To
   ────────────────────────────────────────
   A       @            151.101.1.195
   A       @            151.101.65.195
   TXT     @            firebase=sarasota-gospel-temple-abc123def456
   ```

   **📝 COPY THESE RECORDS** - You'll need them for Step 3!

---

### STEP 3: Update DNS in Wix (The Critical Part!)

Now we'll add these records in Wix. **Follow these instructions EXACTLY:**

#### 3A. Login to Wix and Find DNS Settings

1. **Go to Wix.com and login**
2. **Click on "Domains"** (top menu or dashboard)
3. **Find your domain** in the list (e.g., sarasotagospeltemple.com)
4. **Click the three dots (⋮) next to the domain**
5. **Select "Manage DNS Records"** or **"Advanced DNS"**

You should see a page titled "DNS Records" or "Edit DNS"

---

#### 3B. Identify What DNS Records to Modify

**LOOK at your current DNS records. You'll see various types:**

**KEEP THESE (Don't touch!):**
- ✅ **MX records** (for email - usually say "Google", "Microsoft", etc.)
- ✅ **TXT records for email** (SPF, DKIM, etc.)
- ✅ **NS records** (nameservers)

**CHANGE/DELETE THESE:**
- ❌ **A records pointing to Wix** (usually 23.236.62.147 or similar)
- ❌ **CNAME record for "www"** pointing to Wix
- ❌ **CNAME record for "@"** or your root domain

---

#### 3C. Remove Old Wix Hosting Records

**Find these and DELETE them:**

1. Look for **A record** with:
   - Name: `@` or `(empty)` or `yourdomain.com`
   - Points to: Wix IP (like `23.236.62.147`)
   - **Action:** Click delete/trash icon ❌

2. Look for **CNAME record** with:
   - Name: `www`
   - Points to: Something like `wix.com` or Wix redirect
   - **Action:** Click delete/trash icon ❌

---

#### 3D. Add New Firebase DNS Records

Now add the THREE records Firebase gave you:

**Record 1 - First A Record:**
1. Click **"Add Record"** or **"+ Add"**
2. Select **Type:** `A`
3. **Name/Host:** `@` (this means root domain)
4. **Value/Points To:** `151.101.1.195` (first IP from Firebase)
5. **TTL:** `3600` (or leave default)
6. Click **Save**

**Record 2 - Second A Record:**
1. Click **"Add Record"** again
2. Select **Type:** `A`
3. **Name/Host:** `@`
4. **Value/Points To:** `151.101.65.195` (second IP from Firebase)
5. **TTL:** `3600` (or leave default)
6. Click **Save**

**Record 3 - TXT Record (Verification):**
1. Click **"Add Record"** again
2. Select **Type:** `TXT`
3. **Name/Host:** `@`
4. **Value:** `firebase=sarasota-gospel-temple-abc123def456` (copy EXACTLY from Firebase)
5. **TTL:** `3600` (or leave default)
6. Click **Save**

---

#### 3E. Add "www" Subdomain (Optional but Recommended)

This makes `www.yourdomain.com` work too:

1. Click **"Add Record"**
2. Select **Type:** `CNAME`
3. **Name/Host:** `www`
4. **Value/Points To:** `sarasota-gospel-temple.web.app` (your Firebase hosting URL)
5. **TTL:** `3600`
6. Click **Save**

---

#### 3F. DOUBLE CHECK Before Saving!

Your DNS records should now look like this:

```
Type    Name    Value
────────────────────────────────────────────────────
A       @       151.101.1.195                          ✅
A       @       151.101.65.195                         ✅
TXT     @       firebase=sarasota-gospel-temple...     ✅
CNAME   www     sarasota-gospel-temple.web.app         ✅
MX      @       (your email provider)                  ✅ (existing)
TXT     @       (SPF/email records)                    ✅ (existing)
```

**CRITICAL:** Make sure you still see your MX and email TXT records!

Click **"Save Changes"** or **"Update DNS"**

---

### STEP 4: Verify Domain in Firebase

1. **Go back to Firebase Console** (the tab with DNS instructions)
2. Click **"Verify"** button
3. Firebase will check if the DNS records are correct

**Three possible outcomes:**

**✅ SUCCESS:** "Domain verified! Your site will be available soon."
- Great! Move to Step 5

**⏳ PENDING:** "DNS records not found yet. This can take up to 48 hours."
- Wait 15-30 minutes and click "Refresh" or "Verify" again
- DNS usually updates in 5-60 minutes, rarely takes 48 hours

**❌ ERROR:** "DNS records incorrect or not found"
- Go back to Wix DNS settings
- Double-check you entered the EXACT values Firebase provided
- Make sure you used `@` for the Name/Host
- Wait 10 minutes and try verifying again

---

### STEP 5: Wait for SSL Certificate (HTTPS)

After verification:
- Firebase automatically creates an SSL certificate
- This takes **5-30 minutes**
- Your site might show "Not Secure" briefly - this is normal

**Check status:**
1. In Firebase Console → Hosting → Domains
2. Look for your domain - status should say:
   - **"Pending"** → Wait (SSL certificate being created)
   - **"Connected"** → ✅ Done! Your site is live!

---

### STEP 6: Test Your Site

Once status shows "Connected":

1. **Clear your browser cache** (important!)
2. Visit: `https://yourdomain.com` (use HTTPS!)
3. Visit: `https://www.yourdomain.com` (check www too)

**✅ Working if:**
- Site loads
- Shows green padlock 🔒 in browser (HTTPS)
- Forms work
- No errors in console (F12)

**❌ Not working?** See Troubleshooting section below

---

## 🚀 OPTION 2: NETLIFY HOSTING (ALTERNATIVE)

### Why Netlify?
- ✅ Very user-friendly interface
- ✅ Generous free tier (100 GB/month bandwidth)
- ✅ Simple deployment
- ✅ Great for static sites

### STEP 1: Deploy to Netlify

**Method A: Drag & Drop (Easiest)**

1. **Visit:** https://app.netlify.com/drop
2. **Drag your `public` folder** from your VS-Code project
3. **Wait for upload** (1-2 minutes)
4. **Netlify gives you a URL** like: `https://random-name-12345.netlify.app`
5. **Test it:** Click the URL - your site should load

**Method B: Git Connection (Better for updates)**

1. **Push your code to GitHub** (if not already)
2. **Go to:** https://app.netlify.com/
3. Click **"Add new site"** → **"Import an existing project"**
4. Connect **GitHub**, select your repository
5. **Build settings:**
   - Build command: `(leave empty)`
   - Publish directory: `public`
6. Click **"Deploy site"**

**✅ Success Check:** Visit the Netlify URL. If site loads, continue!

---

### STEP 2: Add Custom Domain in Netlify

1. **In Netlify dashboard**, click your site
2. Go to **"Domain settings"** (top menu or left sidebar)
3. Click **"Add custom domain"**
4. Enter your domain: `sarasotagospeltemple.com`
5. Click **"Verify"**
6. Click **"Yes, add domain"** when prompted

Netlify will show DNS configuration instructions.

---

### STEP 3: Get DNS Records from Netlify

Netlify will show you ONE of these options:

**Option A: A Record (Recommended)**
```
Type    Name    Value
─────────────────────────
A       @       75.2.60.5
```

**Option B: CNAME (Alternative)**
```
Type     Name    Value
───────────────────────────────────
CNAME    @       random-name-12345.netlify.app
```

**Use Option A (A Record)** if Wix allows it. If Wix doesn't allow CNAME for root domain, use A record.

📝 **Copy these values** - you'll need them for Wix!

---

### STEP 4: Update DNS in Wix for Netlify

#### 4A. Login to Wix DNS Settings

1. Go to **Wix.com** and login
2. Click **"Domains"**
3. Find your domain → Click **three dots (⋮)**
4. Select **"Manage DNS Records"**

---

#### 4B. Remove Old Wix Records

**DELETE these:**
- ❌ A record with `@` pointing to Wix IP
- ❌ CNAME with `www` pointing to Wix

**KEEP these:**
- ✅ MX records (email)
- ✅ TXT records (email)
- ✅ NS records

---

#### 4C. Add Netlify DNS Records

**For Root Domain:**

1. Click **"Add Record"**
2. **Type:** `A`
3. **Name:** `@`
4. **Value:** `75.2.60.5` (the IP Netlify gave you)
5. **TTL:** `3600`
6. Click **Save**

**For WWW Subdomain:**

1. Click **"Add Record"**
2. **Type:** `CNAME`
3. **Name:** `www`
4. **Value:** `random-name-12345.netlify.app` (your Netlify subdomain)
5. **TTL:** `3600`
6. Click **Save**

**Final DNS should look like:**
```
Type    Name    Value
──────────────────────────────────────────────────
A       @       75.2.60.5                         ✅
CNAME   www     random-name-12345.netlify.app     ✅
MX      @       (your email provider)             ✅ (existing)
```

Click **"Save Changes"**

---

### STEP 5: Verify in Netlify

1. Go back to **Netlify** → **Domain settings**
2. Under your domain, click **"Verify DNS configuration"**
3. Wait for verification (5-60 minutes usually)

**Status indicators:**
- **"DNS configured correctly"** ✅ Perfect!
- **"Waiting for DNS propagation"** ⏳ Wait 15-30 mins, refresh
- **"DNS not configured"** ❌ Check your Wix DNS settings

---

### STEP 6: Enable HTTPS in Netlify

1. In Netlify → **Domain settings**
2. Scroll to **"HTTPS"** section
3. Click **"Verify DNS configuration"** (if not already verified)
4. Click **"Provision certificate"** (might be automatic)
5. Wait 5-10 minutes for SSL certificate

---

### STEP 7: Test Your Netlify Site

1. Clear browser cache
2. Visit: `https://yourdomain.com`
3. Visit: `https://www.yourdomain.com`

**✅ Working if:** Site loads with green padlock 🔒

---

## 🔧 TROUBLESHOOTING

### Problem: "DNS_PROBE_FINISHED_NXDOMAIN" Error

**Cause:** DNS records haven't propagated yet

**Solution:**
1. Wait 15-30 minutes
2. Clear browser cache (Ctrl+Shift+Delete)
3. Try incognito/private window
4. Check DNS propagation: https://www.whatsmydns.net/

---

### Problem: "Your connection is not private" (SSL Error)

**Cause:** SSL certificate not ready yet

**Solution:**
1. Wait 10-30 minutes for certificate provisioning
2. Check Firebase/Netlify dashboard for SSL status
3. Try forcing refresh: Ctrl+Shift+R

---

### Problem: Site shows old Wix content

**Cause:** Browser or DNS cache

**Solution:**
1. Clear browser cache completely
2. Wait 1-2 hours for DNS to propagate
3. Try different device/network
4. Use: https://www.whatsmydns.net/ to check global DNS

---

### Problem: Email stopped working

**Cause:** Deleted MX records by mistake

**Solution:**
1. Go back to Wix DNS
2. Re-add MX records for your email provider
3. Contact Wix support for original MX record values

---

### Problem: DNS verification fails in Firebase/Netlify

**Checklist:**
- [ ] Used `@` for root domain (not your domain name)
- [ ] Copied EXACT values (no extra spaces)
- [ ] Saved changes in Wix
- [ ] Waited at least 15 minutes
- [ ] Only deleted Wix website records, not email records

---

## 📞 NEED HELP?

If you get stuck:

1. **Check DNS propagation:** https://www.whatsmydns.net/
   - Enter your domain
   - Check if new records are visible worldwide

2. **Firebase Support:** https://firebase.google.com/support
3. **Netlify Support:** https://www.netlify.com/support/
4. **Wix Support:** https://www.wix.com/contact

---

## ✅ FINAL CHECKLIST

After completing setup:

- [ ] Site loads at: https://yourdomain.com
- [ ] Site loads at: https://www.yourdomain.com
- [ ] HTTPS works (green padlock 🔒)
- [ ] All forms work (test registration, volunteer, vendor)
- [ ] Email still works (if you use email with this domain)
- [ ] Admin dashboard accessible
- [ ] Mobile version works

---

## 🎉 SUCCESS!

Once everything is checked, your site is LIVE!

**What to do next:**
1. Test all forms thoroughly
2. Share the new URL with your team
3. Monitor for any issues in first 24 hours
4. Set up monitoring (Firebase Analytics, etc.)

---

## 📋 QUICK REFERENCE - DNS RECORD TYPES

| Type | What It Does | Example |
|------|-------------|---------|
| **A** | Points domain to IP address | `@ → 151.101.1.195` |
| **CNAME** | Points domain to another domain | `www → yoursite.web.app` |
| **MX** | Email routing | For your email provider |
| **TXT** | Verification & email security | Firebase verification, SPF |
| **NS** | Nameservers | Usually don't touch these |

**Name/Host field meanings:**
- `@` = Root domain (yourdomain.com)
- `www` = www subdomain (www.yourdomain.com)
- `*` = Wildcard (any subdomain)

---

**Remember:** DNS changes are reversible. If something breaks, you can always put the old records back!

Good luck! 🚀
