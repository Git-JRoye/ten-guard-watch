# Cloudflare Deployment Troubleshooting Guide

## Common Issues and Solutions

### 1. White Screen Issue

**Possible Causes:**
- Missing files or broken file paths
- CSS not loading properly
- JavaScript errors preventing page rendering
- Incorrect build configuration

**Solutions:**

#### Check File Structure
Ensure all files are in the correct locations:
```
WebsiteFinal/
├── index.html (main page)
├── about.html
├── services.html
├── contact.html
├── tenguardwatch.html
├── self-assessment.html (newly created)
├── styles_v5.css
├── script.js
├── assets/
│   ├── svglogo.svg
│   ├── background3.jpg
│   └── [other assets]
```

#### Verify Cloudflare Pages Settings
1. Go to Cloudflare Dashboard → Pages
2. Select your project
3. Go to Settings → Builds & deployments
4. Ensure these settings:
   - **Build command**: `echo "Static site - no build needed"`
   - **Build output directory**: `/` (root)
   - **Root directory**: `/` (empty)

#### Test Locally First
```bash
# Navigate to your project directory
cd WebsiteFinal

# Start a local server (Python 3)
python3 -m http.server 8000

# Or with Node.js
npx serve .

# Visit http://localhost:8000 to test
```

### 2. Broken Links Issue

**Common Causes:**
- Missing HTML files
- Incorrect relative paths
- Case sensitivity issues

**Solutions:**

#### Check All Links
All navigation links should work:
- `index.html` → Home page
- `about.html` → About page  
- `services.html` → Services page
- `contact.html` → Contact page
- `tenguardwatch.html` → TenGuard Watch page
- `self-assessment.html` → Security Assessment (now created)

#### Verify File Names
Ensure all file names match exactly (case-sensitive):
- `index.html` (not `Index.html`)
- `styles_v5.css` (not `styles_v5.CSS`)
- `script.js` (not `Script.js`)

### 3. Assets Not Loading

**Check Asset Paths:**
All assets should be in the `assets/` folder:
```
assets/
├── svglogo.svg
├── background3.jpg
├── cyberAlert.png
├── data1.png
├── continuity1.png
└── [other images]
```

**Verify CSS References:**
In your HTML files, ensure:
```html
<link rel="stylesheet" href="styles_v5.css">
```

**Verify Image References:**
```html
<img src="assets/svglogo.svg" alt="TenGuard Security Logo">
```

### 4. Deployment Steps

#### Step 1: Commit All Changes
```bash
git add .
git commit -m "Fix deployment issues and add missing files"
git push origin main
```

#### Step 2: Check Cloudflare Pages
1. Go to Cloudflare Dashboard
2. Navigate to Pages
3. Select your project
4. Check the latest deployment status
5. If failed, click "Retry deployment"

#### Step 3: Verify Build Output
In Cloudflare Pages:
1. Go to your project
2. Click on the latest deployment
3. Check the build logs for errors
4. Verify all files are present in the output

### 5. Quick Fixes

#### If Still Getting White Screen:
1. **Check Browser Console:**
   - Open Developer Tools (F12)
   - Look for JavaScript errors
   - Check Network tab for failed requests

2. **Test Individual Files:**
   - Try accessing `yoursite.com/index.html` directly
   - Try accessing `yoursite.com/styles_v5.css` directly

3. **Clear Cache:**
   - Hard refresh (Ctrl+F5 or Cmd+Shift+R)
   - Clear browser cache
   - Try incognito/private mode

#### If Links Still Broken:
1. **Check File Permissions:**
   - Ensure all files are readable
   - Check that HTML files have proper permissions

2. **Verify Case Sensitivity:**
   - Cloudflare Pages is case-sensitive
   - Ensure all file names match exactly

### 6. Testing Checklist

Before deploying, test locally:
- [ ] All pages load without errors
- [ ] Navigation links work
- [ ] Images display correctly
- [ ] CSS styling is applied
- [ ] JavaScript functions work
- [ ] No console errors

### 7. Emergency Rollback

If deployment fails:
1. Go to Cloudflare Pages dashboard
2. Select your project
3. Go to "Deployments" tab
4. Find a working deployment
5. Click "Rollback to this deployment"

### 8. Contact Support

If issues persist:
1. Check Cloudflare Pages documentation
2. Review build logs for specific errors
3. Test with a minimal HTML file first
4. Consider using a different deployment method

## Quick Test File

Create a simple `test.html` to verify deployment:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Test</title>
</head>
<body>
    <h1>Deployment Test</h1>
    <p>If you can see this, the deployment is working!</p>
</body>
</html>
```

Deploy this first to ensure basic functionality works.
