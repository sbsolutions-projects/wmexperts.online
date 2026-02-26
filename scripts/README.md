# WMexperts Index Updater

This script automatically updates the `index.html` page to display the featured post (most recent) and the 5 next most recent blog posts.

## Setup

### Prerequisites
- Python 3.6 or later

### Installation

No additional dependencies are required! The Python script only uses the standard library.

## Usage

### Quick Start (Recommended)

**Windows (Batch):**
```bash
Double-click: update-index.bat
```

**Windows (PowerShell):**
```powershell
PowerShell -ExecutionPolicy Bypass -File update-index.ps1
```

**Command Line (All platforms):**
```bash
python update-index.py
```

### What the Script Does

1. **Scans** the entire `blog-posts/` directory recursively for all HTML files
2. **Extracts** metadata including:
   - Publication date (`article:published_time` meta tag)
   - Title (`og:title` meta tag)
   - Description (`og:description` meta tag)
   - Category (based on folder structure)
   - Icon and category tag
3. **Sorts** posts by publication date (newest first)
4. **Updates** the `index.html` file with:
   - The most recent post as the **featured card** (takes 2 grid columns)
   - The next 5 most recent posts as regular cards below

## Blog Post Structure Requirements

For the script to work correctly, each blog post HTML file must include:

```html
<meta property="article:published_time" content="YYYY-MM-DD">
<meta property="og:title" content="Your Post Title | WMexperts">
<meta property="og:description" content="Your post description">
```

### Example Blog Post Metadata

```html
<head>
    <meta property="article:published_time" content="2025-05-17">
    <meta property="article:modified_time" content="2025-05-17">
    <meta property="og:type" content="article">
    <meta property="og:title" content="How to become a good EWM Consultant">
    <meta property="og:description" content="Discover the essential skills required to become a successful SAP EWM consultant.">
    <!-- ... other tags ... -->
</head>
```

## Category Mapping

The script automatically assigns categories based on the folder where your blog post is located:

- `mfs/` → 🏗️ Discover SAP EWM MFS
- `understand/` → 🎓 Understand SAP EWM
- `enhance/` → 🔧 Enhance SAP EWM
- `reveal/` → 🔍 Reveal SAP EWM
- `around/` → 📊 Around SAP EWM
- `work/` → 💼 Work with EWM

## Workflow

For each new blog post:

1. Create your blog post HTML file in the appropriate category folder (e.g., `blog-posts/mfs/my-post.html`)
2. Ensure it has the required metadata:
   - `<meta property="article:published_time" content="YYYY-MM-DD">`
   - `<meta property="og:title" content="Your Title | WMexperts">`
   - `<meta property="og:description" content="Your description">`
3. Run the script (double-click `update-index.bat` or use command: `python update-index.py`)
4. The index page will automatically be updated with your new post

## Troubleshooting

### Script says "No publication date found"
- Check that your blog post has the `article:published_time` meta tag in the correct format (YYYY-MM-DD)
- Example: `<meta property="article:published_time" content="2025-05-17">`

### Grid not updating
- Verify the index.html hasn't been manually modified in a way that breaks the grid structure
- The script looks for: `<div class="grid" id="posts-grid">`
- Make sure this element exists with this exact ID
- Check that the HTML comment `<!-- VIEW ALL LINK -->` exists after the grid

### Python not recognized
- Make sure Python is installed: https://www.python.org/downloads/
- Verify Python is in your system PATH
- Try using the full path: `C:\Python39\python.exe update-index.py` (adjust version as needed)

### "Article Title | WMexperts" shows in the featured card
- This means the `og:title` meta tag wasn't found
- Check that the meta tag exists and has the correct property name: `property="og:title"`

## Files Included

- `update-index.py` - Main Python script (runs on all platforms)
- `update-index.bat` - Windows batch file (double-click to run)
- `update-index.ps1` - PowerShell script (for advanced Windows users)
- `QUICK-START.md` - Quick reference guide
- `README.md` - This file

## Notes

- The featured card will always be the most recent post
- Only posts with a valid `article:published_time` meta tag will be included
- The script looks for "X min read" patterns in the page content for reading time
- Reading time defaults to "10 min read" if not found
- The script modifies the index.html file directly
- A backup is recommended before first run (though the script is non-destructive to other content)
