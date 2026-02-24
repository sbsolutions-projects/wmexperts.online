# Migration Guide: Converting Existing Pages

This guide shows how to convert your current pages to work with the header/footer component system.

## Choose Your Approach First

- **Python Build Script**: Better for SEO, production GitHub Pages
- **JavaScript Injection**: Faster development, instant preview, no build step

## Option A: Python Build Script Migration

### Step 1: Update `index.html`

Go to line 349 in your current `index.html` and replace:

```html
    <header>
        <a href="index.html" class="logo">WM<span style="color: var(--text-dark);">experts.online</span></a>
        <nav>
            <a href="#latest">Latest</a>
            <a href="blog-overview.html">All Articles</a>
            <a href="about.html">About</a>
        </nav>
    </header>
```

With:

```html
    {{HEADER}}
```

Then at the footer (end of file, before `</body>`), replace:

```html
    <footer>
        <p>&copy; 2026 WMexperts.online • Functional & Technical SAP EWM Expertise</p>
    </footer>
```

With:

```html
    {{FOOTER}}
```

### Step 2: Update `blog-overview.html`

Replace lines 248-257 (the header) with:

```html
    {{HEADER}}
```

Replace the footer with:

```html
    {{FOOTER}}
```

### Step 3: Update `about.html` and All Blog Post Files

Repeat the same process for every `.html` file:
1. Find the `<header>...</header>` block
2. Replace it with `{{HEADER}}`
3. Find the `<footer>...</footer>` block  
4. Replace it with `{{FOOTER}}`

### Step 4: Run the Build

```bash
python build.py
```

This will process all `.html` files and inject the actual header/footer content.

### Step 5: Verify

- Open files in your browser - header and footer should appear
- Check Git diff to see the changes
- Commit the built files: `git add -A && git commit -m "Build: inject components"`

---

## Option B: JavaScript Injection Migration

### Step 1: Update All HTML Files

For each `.html` file (`index.html`, `about.html`, `blog-overview.html`, and all blog posts):

**Replace** your current header code:
```html
    <header>
        <a href="index.html" class="logo">WM<span style="color: var(--text-dark);">experts.online</span></a>
        <nav>
            <a href="index.html">Latest</a>
            <a href="blog-overview.html">All Articles</a>
            <a href="about.html">About</a>
        </nav>
    </header>
```

**With** this empty container:
```html
    <header id="header-container"></header>
```

**Replace** your current footer:
```html
    <footer>
        <p>&copy; 2026 WMexperts.online • Functional & Technical SAP EWM Expertise</p>
    </footer>
```

**With** this empty container:
```html
    <footer id="footer-container"></footer>
```

### Step 2: Add the Script

At the **very end** of the `<body>` tag (before `</body>`), add:

```html
    <script src="js/inject-components.js" async></script>
</body>
```

**Make sure** it's the last line before `</body>`.

### Step 3: Test Locally

Open any `.html` file in your browser. You should see:
- Header with logo and navigation
- Your page content
- Footer

The navigation should auto-highlight based on the current page.

### Step 4: Commit

```bash
git add -A
git commit -m "refactor: use component injection for header/footer"
git push
```

---

## Quick Command Reference

### Python Build Script Approach

```bash
# Process all files
python build.py

# Process specific files
python build.py index.html about.html

# Check which files have placeholders
grep -r "{{HEADER}}" *.html blog-posts/**/*.html
```

### JavaScript Approach

No build commands needed! Just:

```bash
# Commit your changes
git add -A
git commit -m "refactor: use JS component injection"
git push
```

---

## Troubleshooting Migration

### Python Approach

**Q: "File not found" error?**
A: Make sure you're in the project root directory:
```bash
cd /path/to/wmexperts.online
python build.py
```

**Q: Some files didn't update?**
A: Check that they contain `{{HEADER}}` or `{{FOOTER}}`:
```bash
grep -l "{{HEADER}}" *.html blog-posts/**/*.html
```

**Q: Need to revert?**
A: Git can help:
```bash
git diff                    # See what changed
git checkout -- file.html   # Revert specific file
git reset --hard            # Revert all changes
```

### JavaScript Approach

**Q: Header/footer not showing?**
A: Check:
1. Browser console (F12) for errors
2. Does `js/inject-components.js` exist?
3. Is the script tag in your HTML?
4. Is the path correct? (should be `js/inject-components.js`)

**Q: Still not working?**
A: Try adding the `defer` attribute:
```html
<script src="js/inject-components.js" defer></script>
```

**Q: Old browser issues?**
A: Add a noscript fallback:
```html
<header id="header-container">
    <noscript>
        <!-- Fallback header for browsers with JS disabled -->
    </noscript>
</header>
```

---

## Verify Everything Works

### After Migration (Both Approaches)

1. **Visual Check**
   - [ ] Header appears at top of page
   - [ ] Navigation links work
   - [ ] Active page is highlighted in nav
   - [ ] Footer appears at bottom
   - [ ] All links work (Latest, All Articles, About)

2. **Technical Check**
   - [ ] No errors in browser console (F12)
   - [ ] CSS still applies (colors, fonts, styling)
   - [ ] Responsive design works (test on mobile)
   - [ ] Page speed hasn't degraded

3. **Git Check**
   - [ ] All changes committed
   - [ ] No broken files
   - [ ] Ready to push to GitHub Pages

---

## What Gets Deployed

### Python Build Script
- ✅ Fully processed HTML with injected content
- ✅ No placeholders in final files
- ✅ Identical to what was there before
- ✅ GitHub Pages serves production-ready HTML

### JavaScript Injection
- ✅ HTML with placeholder containers
- ✅ `js/inject-components.js` included
- ✅ Templates in `templates/` folder
- ✅ GitHub Pages serves HTML + JS + templates

---

## Next Steps

1. Choose your approach above
2. Follow the migration steps for your HTML files
3. Test locally in browser
4. Commit changes to Git
5. Push to GitHub
6. Update header/footer in single `templates/` file for future changes

The components system is now active and you can maintain your header/footer in a single location!
