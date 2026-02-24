# DRY Header/Footer Solution for Static Site

This solution provides two approaches to manage headers and footers without repetition:

## 📋 Quick Comparison

| Feature | Python Build Script | JavaScript Injection |
|---------|-------------------|---------------------|
| **SEO Impact** | ✅ None - pre-processed HTML | ⚠️ Minor - content injected after DOM load |
| **PageSpeed** | ✅ Fastest - no JS execution | ⚠️ Slower - JS must run in browser |
| **GitHub Pages** | ✅ Perfect - pre-build locally | ✅ Works - no build step needed |
| **Development** | ⚠️ Requires build step | ✅ Preview instantly in browser |
| **Browser support** | ✅ All | ⚠️ Requires JS enabled |
| **Maintenance** | ✅ Single source of truth | ✅ Single source of truth |

---

## 🐍 Option 1: Python Build Script (RECOMMENDED)

### Why Choose This?
- **Best for SEO**: Produces fully-rendered static HTML that search engines see immediately
- **Best for PageSpeed**: Zero JavaScript overhead
- **Best for GitHub Pages**: Works exactly as GitHub Pages expects

### Setup

1. **Install Python** (if not already installed):
   ```bash
   python --version  # Should be 3.6+
   ```

2. **Files are already created**:
   - `templates/header.html` - Your header content
   - `templates/footer.html` - Your footer content  
   - `build.py` - The build script
   - `templates/page-template.html` - Template for new pages

### Usage

#### Process all HTML files:
```bash
python build.py
```

#### Process specific files:
```bash
python build.py about.html article-template.html
```

#### Adding to your workflow:
```bash
# Build before pushing to GitHub
python build.py
git add -A
git commit -m "Build: inject components"
git push
```

### Create New Pages

1. Copy `templates/page-template.html` to your desired location:
   ```bash
   cp templates/page-template.html new-page.html
   ```

2. Edit the page content, keep `{{HEADER}}` and `{{FOOTER}}` placeholders

3. Run `python build.py` to inject the components

4. Commit the processed versions to GitHub

### Example Workflow

**Source file** (`new-article.html`):
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>My Article | WMexperts</title>
    <!-- ... other head content ... -->
</head>
<body>

    {{HEADER}}

    <main>
        <h1>My Article Title</h1>
        <p>Article content here...</p>
    </main>

    {{FOOTER}}

</body>
</html>
```

**After build** (what GitHub Pages serves):
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>My Article | WMexperts</title>
    <!-- ... other head content ... -->
</head>
<body>

    <header>
        <a href="index.html" class="logo">WM<span style="color: var(--text-dark);">experts.online</span></a>
        <nav>
            <a href="index.html" class="nav-link-latest">Latest</a>
            <a href="blog-overview.html" class="nav-link-articles">All Articles</a>
            <a href="about.html" class="nav-link-about">About</a>
        </nav>
    </header>

    <main>
        <h1>My Article Title</h1>
        <p>Article content here...</p>
    </main>

    <footer>
        <p>&copy; 2026 WMexperts.online • Functional & Technical SAP EWM Expertise</p>
    </footer>

</body>
</html>
```

### Updating Header/Footer

1. Edit `templates/header.html` or `templates/footer.html`
2. Run `python build.py` to rebuild all pages with new components
3. Commit and push

---

## 💻 Option 2: Client-Side JavaScript Injection

### Why Choose This?
- **Instant preview** during development - no build step
- **No build complexity** - just write HTML
- **Works offline** without setup

### Setup

1. **Files already created**:
   - `js/inject-components.js` - The injection script
   - `templates/header.html` - Header content
   - `templates/footer.html` - Footer content

2. **Update your HTML pages** to use containers:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>My Page | WMexperts</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        /* Your styles here */
        :root {
            --sap-blue: #005597;
            --sap-blue-light: #0066B3;
            --bg-page: #F5F7FA;
            --bg-card: #FFFFFF;
            --text-dark: #111827;
            --text-muted: #6B7280;
            --border: #E5E7EB;
            --accent: #EEF6FC;
        }
        /* ... rest of CSS ... */
    </style>
</head>
<body>

    <!-- Empty header that gets filled by JavaScript -->
    <header id="header-container"></header>

    <!-- Your page content -->
    <main>
        <h1>My Page Title</h1>
        <p>Page content here...</p>
    </main>

    <!-- Empty footer that gets filled by JavaScript -->
    <footer id="footer-container"></footer>

    <!-- Load the injection script at the END of body -->
    <script src="js/inject-components.js" async></script>

</body>
</html>
```

### Usage
- Just include `<script src="js/inject-components.js" async></script>` in your pages
- Add empty `<header id="header-container"></header>` and `<footer id="footer-container"></footer>`
- The script auto-detects the current page and sets the active nav link

### Performance Notes
- Script is small (~2KB unminified)  
- Uses `async` attribute so it doesn't block page rendering
- Non-critical elements (header/footer) don't delay page load

---

## 🎯 Recommendation: Hybrid Approach

For the best of both worlds:

1. **During development**: Use JavaScript injection to preview instantly
2. **Before deploying to GitHub**: Run the Python build script to create production HTML

```bash
# Develop with JS injection
# ... edit files, preview in browser ...

# Before pushing to production
python build.py
git add -A
git commit -m "Production build: pre-processed components"
git push origin main
```

---

## 📝 Updating Components

### Python Build Approach:
```bash
# Edit the template
nano templates/header.html

# Rebuild all pages with the new header
python build.py

# Commit and push
git add -A
git commit -m "Update: header navigation links"
git push
```

### JavaScript Approach:
```bash
# Edit the template
nano templates/header.html

# Save and reload browser - changes appear instantly
# No build step needed!
```

---

## 🚀 GitHub Pages Deployment

### With Python Build Script:
```bash
# On your local machine
python build.py                    # Generate production HTML
git add -A
git commit -m "Build: inject components"
git push origin main               # Push to GitHub Pages

# GitHub Pages automatically serves the rendered HTML
```

### With JavaScript Injection:
```bash
# Just push directly - no build needed
git add -A
git commit -m "Update: new article"
git push origin main

# GitHub Pages serves HTML, JS runs in browser and injects components
```

---

## ⚠️ SEO & Performance Considerations

### Python Build Script:
- ✅ **Best for SEO**: Search engines see fully rendered HTML immediately
- ✅ **Best for PageSpeed**: No JavaScript, instant render
- ✅ **Better for old browsers**: Doesn't require JavaScript
- ✅ **Social media**: Meta tags and structured data in initial HTML

**Recommendation for:** Public-facing content, articles, landing pages

### JavaScript Injection:
- ⚠️ **SEO**: Search engines must execute JS to see header/footer (slower indexing)
- ⚠️ **PageSpeed**: JS execution adds ~50-100ms to page load
- ⚠️ **noscript users**: Page doesn't work without JavaScript
- ✅ **Dynamic nav highlighting**: Easier to implement active state

**Recommendation for:** Rapid development, internal pages, low-SEO content

---

## 🛠️ Troubleshooting

### Python Build Script

**"ModuleNotFoundError"**: 
- Ensure you're running from the project root: `cd /path/to/wmexperts.online`

**"Template not found"**:
- Make sure `templates/header.html` and `templates/footer.html` exist
- Check file paths are correct

**Files not updating**:
- Run `python build.py` with no arguments to process all files
- Check that files contain `{{HEADER}}` or `{{FOOTER}}` placeholders

### JavaScript Injection

**Header/footer not appearing**:
1. Check browser console for errors (F12)
2. Verify `js/inject-components.js` path is correct
3. Ensure `<header id="header-container"></header>` is in your HTML
4. Add `defer` to script tag if `.innerHTML` isn't working: `<script src="..." async defer></script>`

**Active nav link not highlighting**:
- The script auto-sets `.active` class based on current page
- Make sure your CSS includes: `nav a.active { color: var(--sap-blue); font-weight: 600; }`

---

## 📚 File Structure After Setup

```
wmexperts.online/
├── index.html
├── about.html
├── blog-overview.html
├── build.py                 # Python build script
├── js/
│   └── inject-components.js # JS injection script
├── templates/
│   ├── header.html         # Shared header
│   ├── footer.html         # Shared footer
│   └── page-template.html  # Template for new pages
├── blog-posts/
│   ├── ... existing posts ...
└── assets/
    └── ... images, favicon, etc ...
```

---

## ✅ Checklist

- [ ] Decide: Python Build Script or JavaScript Injection (or both)?
- [ ] Update all HTML pages with `{{HEADER}}` and `{{FOOTER}}` placeholders (Python) or empty containers (JS)
- [ ] Test that header and footer appear correctly
- [ ] Update navigation links if needed in `templates/header.html`
- [ ] Run `python build.py` before pushing to GitHub (Python approach)
- [ ] Verify on GitHub Pages that site looks correct

---

## Questions?

- **Need to update multiple pages at once?** Use Python build script
- **Want instant preview during editing?** Use JavaScript injection  
- **Want best SEO?** Use Python build script
- **Want minimal setup?** Use JavaScript injection

Both are lightweight, maintainable, and won't negatively impact your site if implemented correctly.
