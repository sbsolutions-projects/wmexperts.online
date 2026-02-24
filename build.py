#!/usr/bin/env python3
"""
Build script to inject header and footer into HTML files.
Solves the DRY principle for static site on GitHub Pages.

Usage:
    python build.py                    # Process all .html files
    python build.py about.html         # Process specific file
    
This script:
1. Reads header and footer from templates/
2. Injects them into pages that have {{HEADER}} and {{FOOTER}} placeholders
3. Creates/updates the output files with fully resolved HTML
4. Preserves all metadata and styling
5. Automatically features the latest blog post on index.html

GitHub Pages Deployment:
- Commit source files with placeholders to a 'source' branch or folder
- Run build.py before deploying
- Push processed HTML files to main branch
"""

import os
import sys
import glob
import re
from pathlib import Path
from datetime import datetime

def load_template(template_name):
    """Load a template file from the templates directory."""
    template_path = Path(__file__).parent / "templates" / f"{template_name}.html"
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    return template_path.read_text(encoding='utf-8')

def feature_latest_article(content):
    """
    Parse article cards and feature the one with the latest date.
    
    Looks for cards with data-date attribute in YYYY-MM-DD format.
    Adds the 'featured' class to the card with the latest date.
    Also updates the tag to show "📌 Featured" for the featured article.
    
    Args:
        content: HTML content string
    
    Returns:
        Updated HTML content with latest article featured
    """
    # Find all article cards with data-date attribute
    card_pattern = r'<a[^>]*class="card"[^>]*data-date="(\d{4}-\d{2}-\d{2})"[^>]*>(.*?)</a>'
    
    cards = list(re.finditer(card_pattern, content, re.DOTALL))
    
    if not cards:
        return content  # No dated cards found
    
    # Find the card with the latest date
    latest_idx = 0
    latest_date = datetime.strptime(cards[0].group(1), '%Y-%m-%d')
    
    for i, match in enumerate(cards):
        card_date = datetime.strptime(match.group(1), '%Y-%m-%d')
        if card_date > latest_date:
            latest_date = card_date
            latest_idx = i
    
    # Add 'featured' class to the latest card
    latest_card_full = cards[latest_idx].group(0)
    updated_card = latest_card_full.replace('class="card"', 'class="card featured"')
    
    # Update the tag to show featured badge instead of regular tag
    # Find the tag within this card
    tag_pattern = r'<span class="tag">.*?</span>'
    if re.search(tag_pattern, updated_card):
        updated_card = re.sub(tag_pattern, '<span class="tag">📌 Featured</span>', updated_card, count=1)
    
    content = content.replace(latest_card_full, updated_card)
    
    return content

def process_file(filepath, header, footer):
    """
    Process a single HTML file, replacing placeholders with header and footer.
    
    Args:
        filepath: Path to the HTML file to process
        header: Header HTML string
        footer: Footer HTML string
    
    Returns:
        True if file was processed, False if no placeholders found
    """
    content = Path(filepath).read_text(encoding='utf-8')
    
    # Check if file has placeholders
    if '{{HEADER}}' not in content and '{{FOOTER}}' not in content:
        # For index.html, still process to feature latest article even without placeholders
        if filepath.endswith('index.html'):
            content = feature_latest_article(content)
            Path(filepath).write_text(content, encoding='utf-8')
            return True
        return False
    
    # Replace placeholders
    content = content.replace('{{HEADER}}', header)
    content = content.replace('{{FOOTER}}', footer)
    
    # If this is index.html, also feature the latest article
    if filepath.endswith('index.html'):
        content = feature_latest_article(content)
    
    # Write back to file
    Path(filepath).write_text(content, encoding='utf-8')
    return True

def main():
    """Main build process."""
    print("🔨 Building static site with injected header/footer...")
    
    try:
        # Load templates once
        header = load_template('header')
        footer = load_template('footer')
        print("✓ Templates loaded")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    
    # Determine which files to process
    if len(sys.argv) > 1:
        # Process specific files
        files = sys.argv[1:]
    else:
        # Process all HTML files in root and subdirectories (except templates)
        html_files = glob.glob("**/*.html", recursive=True)
        files = [f for f in html_files if 'templates' not in f and 'node_modules' not in f]
    
    processed_count = 0
    skipped_count = 0
    
    for filepath in files:
        if not Path(filepath).exists():
            print(f"⚠ File not found: {filepath}")
            continue
        
        try:
            if process_file(filepath, header, footer):
                print(f"✓ Processed: {filepath}")
                processed_count += 1
            else:
                print(f"⊘ Skipped (no placeholders): {filepath}")
                skipped_count += 1
        except Exception as e:
            print(f"✗ Error processing {filepath}: {e}")
    
    print(f"\n✓ Build complete: {processed_count} files processed, {skipped_count} files skipped")

if __name__ == '__main__':
    main()
