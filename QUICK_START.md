# Quick Start: Header/Footer Components

## 🚀 30-Second Setup

### Choose One Option:

## ⚡ Option 1: Python Build (Production-Ready)

**Best for**: GitHub Pages, SEO, professional sites

```bash
# 1. Files already created. Just run:
python build.py

# 2. Update your HTML files:
# Replace: <header>...</header> → {{HEADER}}
# Replace: <footer>...</footer> → {{FOOTER}}

# 3. Run build again:
python build.py

# 4. Done! Commit and push
git add -A && git commit -m "Build: inject components" && git push
```

---

## ✨ Option 2: JavaScript (Development-Friendly)

**Best for**: Rapid development, instant preview, no build step

```bash
# 1. Files already created. Just add to your HTML:
# Replace: <header>...</header> → <header id="header-container"></header>
# Replace: <footer>...</footer> → <footer id="footer-container"></footer>

# 2. Add script before </body>:
# <script src="js/inject-components.js" async></script>

# 3. Save and reload browser - that's it!

# 4. Commit and push:
git add -A && git commit -m "Add: JS component injection" && git push
```

---

## 📁 What Was Created For You

```
templates/
├── header.html          ← Edit your header here
├── footer.html          ← Edit your footer here
└── page-template.html   ← Template for new pages

js/
└── inject-components.js ← JavaScript injection script

build.py                ← Python build script

.github/workflows/
└── build.yml          ← GitHub Actions automation (optional)

COMPONENTS_README.md    ← Full documentation
MIGRATION_GUIDE.md      ← Detailed migration steps
QUICK_START.md          ← This file
```

---

## 📚 Full Documentation

For detailed setup, troubleshooting, and advanced features, see:
- **[COMPONENTS_README.md](./COMPONENTS_README.md)** - Complete guide with comparisons
- **[MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md)** - Step-by-step migration instructions

---

## ❓ Which Should I Use?

### Use **Python Build Script** if:
- You want best SEO on GitHub Pages ✅
- You want fastest page speed ✅
- You prefer pre-built production HTML ✅
- You're deploying a professional site ✅

### Use **JavaScript Injection** if:
- You want instant preview while editing ✅
- You don't want build complexity ✅
- You want to see changes immediately ✅
- You prefer fewer operations ✅

---

## 🎯 My Recommendation

**Start with JavaScript injection** during development → **Switch to Python build for production**

This gives you the best of both worlds:
- 🚀 Fast iteration during writing
- 📦 Production-ready HTML before deploying to GitHub

---

## 💡 Pro Tips

### Edit Header/Footer in One Place
```
templates/header.html ← All changes here affect entire site
templates/footer.html ← All changes here affect entire site
```

### Add New Pages
```bash
cp templates/page-template.html new-page.html
# Edit new-page.html
python build.py  # (if using Python approach)
```

### Change Navigation
Edit `templates/header.html` and update the `<nav>` section:
```html
<nav>
    <a href="index.html">Latest</a>
    <a href="blog-overview.html">All Articles</a>
    <a href="about.html">About</a>
</nav>
```

All pages automatically get the updated navigation! 

---

## ✅ Next Step

Choose Python or JavaScript above and follow the 30-second setup.

Questions? See **COMPONENTS_README.md** for comprehensive docs.
