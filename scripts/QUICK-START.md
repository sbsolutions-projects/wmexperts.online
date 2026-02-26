# Quick Start Guide - Index Updater

## The Simplest Way to Run It

### On Windows:
**Just double-click:** `update-index.bat`

That's it! The script will:
1. Find all your blog posts
2. Sort them by date (newest first)
3. Update your index.html with the featured (most recent) and 5 newest posts

### Or from Command Line:
```bash
python update-index.py
```

---

## When to Run It

Run this script whenever you:
- ✅ Publish a new blog post
- ✅ Update a blog post's publication date
- ✅ Add a new blog to a category folder

---

## What Happens

**Before:**
```
index.html with old posts
```

**After running the script:**
```
index.html with:
  - Most recent post as FEATURED (large card)
  - Next 5 most recent posts below it
```

---

## Requirements for Blog Posts

Each blog post HTML file needs these meta tags in the `<head>`:

```html
<!-- REQUIRED - Publication date in YYYY-MM-DD format -->
<meta property="article:published_time" content="2025-12-22">

<!-- REQUIRED - Post title -->
<meta property="og:title" content="Your Post Title">

<!-- REQUIRED - Post description (1-2 sentences) -->
<meta property="og:description" content="A brief description of your post">
```

---

## What the Script Needs

✅ Blog posts located in: `blog-posts/[category]/`  
✅ Supported categories: `mfs`, `understand`, `enhance`, `reveal`, `around`, `work`  
✅ Python 3.6+ installed (already on your system!)  
✅ No internet or extra downloads needed

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Script won't run | Make sure you saved the meta tags correctly in your blog post |
| Featured post is wrong | Check the `article:published_time` date format: must be YYYY-MM-DD |
| Index didn't update | Verify the HTML structure hasn't changed; check `<!-- VIEW ALL LINK -->` comment exists |
| Python not found | Install Python from https://www.python.org/downloads/ |

---

## Example Blog Post Meta Tags

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta property="article:published_time" content="2025-12-22">
    <meta property="article:modified_time" content="2025-12-22">
    <meta property="og:type" content="article">
    <meta property="og:title" content="How to Learn SAP EWM - 4-Step Method">
    <meta property="og:description" content="Master SAP EWM with best practices using this proven 4-step method for beginners and experts.">
    <!-- rest of your page -->
</head>
<body>
    <!-- your content -->
</body>
</html>
```

---

## That's All! 🎉

Just run the script whenever you publish, and your index page stays fresh automatically.
