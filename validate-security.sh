#!/bin/bash
# ===== SECURITY VALIDATION SCRIPT =====
# Checks that no private credentials are exposed in public files
#
# Usage: bash validate-security.sh
#
# This script validates that:
#   1. No private keys in public/ directory
#   2. No service account credentials in public/ directory
#   3. .env files are not tracked in git
#   4. Config files are not tracked in git

set -e

echo "========================================="
echo "🔒 Security Validation"
echo "========================================="
echo ""

ERRORS=0
WARNINGS=0

# ===== CHECK 1: Private keys in public directory =====
echo "📋 Check 1: Scanning for private keys in public/ directory..."

# Check for EmailJS private key
if grep -r "EMAILJS_PRIVATE_KEY\|emailjs.private" public/ 2>/dev/null; then
    echo "❌ ERROR: EMAILJS_PRIVATE_KEY found in public/ directory"
    echo "   This key should ONLY be in Firebase Functions, never client-side!"
    ERRORS=$((ERRORS + 1))
else
    echo "   ✅ No EmailJS private key found"
fi

# Check for private key patterns
if grep -r "BEGIN PRIVATE KEY\|BEGIN RSA PRIVATE KEY" public/ 2>/dev/null; then
    echo "❌ ERROR: Private key detected in public/ directory"
    echo "   Private keys should NEVER be in client-side code!"
    ERRORS=$((ERRORS + 1))
else
    echo "   ✅ No private key patterns found"
fi

# Check for service account JSON
if grep -r "service_account.*private_key\|GOOGLE_SERVICE_ACCOUNT_JSON" public/ 2>/dev/null; then
    echo "❌ ERROR: Service account credentials found in public/ directory"
    echo "   Service accounts should ONLY be in Firebase Functions!"
    ERRORS=$((ERRORS + 1))
else
    echo "   ✅ No service account credentials found"
fi

echo ""

# ===== CHECK 2: Git tracking sensitive files =====
echo "📋 Check 2: Verifying .env and config files are not tracked in git..."

if git ls-files | grep -E "^\.env$|^functions/\.env$" 2>/dev/null; then
    echo "❌ ERROR: .env file is tracked in git"
    echo "   Run: git rm --cached .env && git rm --cached functions/.env"
    ERRORS=$((ERRORS + 1))
else
    echo "   ✅ .env files not tracked in git"
fi

if git ls-files | grep -E "^config/.*\.js$" 2>/dev/null; then
    echo "⚠️  WARNING: Config files are tracked in git"
    echo "   These files contain credentials and should be in .gitignore"
    echo "   Run: git rm --cached config/*.js"
    WARNINGS=$((WARNINGS + 1))
else
    echo "   ✅ Config files not tracked in git"
fi

echo ""

# ===== CHECK 3: .gitignore configuration =====
echo "📋 Check 3: Verifying .gitignore includes sensitive patterns..."

if ! grep -q "^\.env$" .gitignore 2>/dev/null; then
    echo "⚠️  WARNING: .env not in .gitignore"
    WARNINGS=$((WARNINGS + 1))
else
    echo "   ✅ .env in .gitignore"
fi

if ! grep -q "config/.*config\.js" .gitignore 2>/dev/null; then
    echo "⚠️  WARNING: config files might not be properly gitignored"
    WARNINGS=$((WARNINGS + 1))
else
    echo "   ✅ Config files in .gitignore"
fi

if ! grep -q "service-account.*\.json\|serviceAccount.*\.json" .gitignore 2>/dev/null; then
    echo "⚠️  WARNING: Service account files not in .gitignore"
    WARNINGS=$((WARNINGS + 1))
else
    echo "   ✅ Service account files in .gitignore"
fi

echo ""

# ===== CHECK 4: Public credentials are safe patterns =====
echo "📋 Check 4: Verifying public credentials follow safe patterns..."

# Check that Firebase config exists and has expected structure
if [ -f "public/config/firebase-config.js" ]; then
    if grep -q "apiKey.*AIza" public/config/firebase-config.js && \
       grep -q "authDomain.*firebaseapp.com" public/config/firebase-config.js; then
        echo "   ✅ Firebase config structure looks correct"
    else
        echo "⚠️  WARNING: Firebase config might be incomplete"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo "   ℹ️  Firebase config not generated yet (run build.sh)"
fi

# Check that Google Sheets config exists and has expected structure
if [ -f "public/config/google-sheets-config.js" ]; then
    if grep -q "apiKey.*AIza" public/config/google-sheets-config.js && \
       grep -q "clientId.*apps.googleusercontent.com" public/config/google-sheets-config.js; then
        echo "   ✅ Google Sheets config structure looks correct"
    else
        echo "⚠️  WARNING: Google Sheets config might be incomplete"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo "   ℹ️  Google Sheets config not generated yet (run build.sh)"
fi

echo ""

# ===== SUMMARY =====
echo "========================================="
echo "📊 Validation Summary"
echo "========================================="
echo "Errors:   $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [ $ERRORS -gt 0 ]; then
    echo "❌ VALIDATION FAILED"
    echo "   Critical security issues found. Fix errors before deploying!"
    echo ""
    exit 1
elif [ $WARNINGS -gt 0 ]; then
    echo "⚠️  VALIDATION PASSED WITH WARNINGS"
    echo "   Consider fixing warnings for better security."
    echo ""
    exit 0
else
    echo "✅ VALIDATION PASSED"
    echo "   No security issues detected. Safe to deploy!"
    echo ""
    exit 0
fi
