# Security Guidelines

## Credential Management

### Environment Variables (.env file)

**NEVER commit the `.env` file to git!** This file contains sensitive credentials:
- Firebase API keys and project IDs
- EmailJS service IDs and keys
- Google Sheets API keys and spreadsheet IDs
- Google Service Account JSON

The `.env` file is in `.gitignore` and should remain there.

### Config File Generation

Config files in `config/` and `public/config/` directories contain API keys and are generated at build time:

```
config/
├── firebase-config.js      ❌ Contains API keys - in .gitignore
└── google-sheets-config.js ❌ Contains API keys - in .gitignore

public/config/
├── firebase-config.js      ❌ Contains API keys - in .gitignore
└── google-sheets-config.js ❌ Contains API keys - in .gitignore
```

**These files should NEVER be committed to git.**

### How Config Files Are Generated

#### Production (Netlify)
1. Environment variables are set in Netlify dashboard
2. Build command runs: `bash build.sh`
3. Script generates config files in `public/config/` from environment variables
4. Files are served to users but never committed to git

#### Local Development
1. Create `.env` from `.env.example`
2. Add your credentials to `.env`
3. Run development server: `npm run dev`
4. Script generates config files locally (not committed)

## Security Best Practices

### ✅ DO

- Keep `.env` file in `.gitignore`
- Use environment variables for all credentials
- Generate config files at build time
- Use the provided `dev-server.sh` script for local development
- Keep Firebase security rules properly configured
- Regularly rotate API keys and credentials

### ❌ DON'T

- **DON'T** commit `.env` files
- **DON'T** commit config files with real credentials
- **DON'T** manually copy credentials to `public/config/`
- **DON'T** share credentials in chat, email, or documentation
- **DON'T** use production credentials for local testing (when possible)
- **DON'T** disable `.gitignore` entries for credential files

## API Key Security Levels

### Client-Side Keys (Public)
These keys are meant to be exposed in the browser but should still be protected:

- **Firebase API Key**: Can be public but enable Firebase security rules
- **EmailJS Public Key**: Meant for client-side use
- **Google Sheets API Key**: Use API restrictions in Google Cloud Console
- **Google OAuth Client ID**: Public, but restrict to authorized domains

**Protection measures:**
- Enable Firebase security rules to restrict database access
- Use EmailJS reCAPTCHA and domain restrictions
- Restrict Google API keys by HTTP referrer and API scope
- Monitor API usage for abuse

### Server-Side Keys (Private)
These keys should NEVER be exposed to the client:

- **EmailJS Private Key**: Keep in Firebase Functions only
- **Google Service Account JSON**: Keep in Firebase Functions only
- **Firebase Admin SDK credentials**: Server-side only

## File Structure for Security

```
.
├── .env                          ❌ Never commit (contains all secrets)
├── .env.example                  ✅ Commit (template only, no real values)
├── .gitignore                    ✅ Commit (ignores all credential files)
├── build.sh                      ✅ Commit (generates configs from env vars)
├── dev-server.sh                 ✅ Commit (secure local dev workflow)
├── setup-credentials.js          ✅ Commit (helps generate configs)
│
├── config/                       ❌ Directory for root-level configs
│   ├── firebase-config.js        ❌ Never commit (has API keys)
│   └── google-sheets-config.js   ❌ Never commit (has API keys)
│
├── public/                       ✅ Public web root
│   └── config/                   ❌ Generated configs for browser
│       ├── firebase-config.js    ❌ Never commit (has API keys)
│       └── google-sheets-config.js ❌ Never commit (has API keys)
│
└── functions/                    ⚙️ Firebase Cloud Functions
    ├── .env                      ❌ Never commit (server credentials)
    └── index.js                  ✅ Commit (uses environment variables)
```

## Incident Response

### If Credentials Are Exposed

1. **Immediately rotate compromised credentials:**
   - Firebase: Regenerate API keys in Firebase Console
   - EmailJS: Create new service and templates
   - Google Sheets: Delete and recreate API keys

2. **Check git history:**
   ```bash
   # Search for exposed credentials
   git log --all --full-history --source -- .env
   git log --all --full-history --source -- "*config.js"
   ```

3. **Remove from git history if found:**
   ```bash
   # Use git filter-branch or BFG Repo-Cleaner
   # Contact GitHub support to clear caches
   ```

4. **Update credentials everywhere:**
   - Update `.env` locally
   - Update environment variables in Netlify
   - Update Firebase Functions config
   - Redeploy all services

## Monitoring

### Enable Monitoring For:

- Firebase usage and quota alerts
- EmailJS usage and quota alerts
- Google Cloud Platform billing alerts
- Unusual traffic patterns
- Failed authentication attempts

### Regular Security Audits

- Review Firebase security rules monthly
- Check API usage for anomalies
- Rotate credentials quarterly
- Review access logs
- Update dependencies regularly

## Contact

For security concerns or to report vulnerabilities, contact:
- Email: sarasotagospel@gmail.com
- Phone: 941-800-5211
