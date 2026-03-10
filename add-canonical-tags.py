#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Base directory (workspace root)
base_dir = Path(__file__).parent
base_url = "https://wmexperts.online"

# Find all HTML files
html_files = list(base_dir.glob('**/*.html'))
print(f"Found {len(html_files)} HTML files")

for html_file in sorted(html_files):
    # Skip the script itself
    if html_file.name == 'add-canonical-tags.py':
        continue
    
    # Calculate relative path and canonical URL
    rel_path = html_file.relative_to(base_dir)
    # Convert Windows path to web path
    web_path = str(rel_path).replace('\\', '/')
    canonical_url = f"{base_url}/{web_path}"
    
    # Read the file
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file has <head> tag
    if '<head' not in content.lower():
        print(f"⚠ SKIP {rel_path} - No <head> tag found (likely a fragment)")
        continue
    
    # Check if file has </head> tag
    if '</head>' not in content.lower():
        print(f"⚠ SKIP {rel_path} - No </head> tag found")
        continue
    
    # Pattern for existing canonical link (more flexible to handle various formats)
    canonical_pattern = r'<link\s+rel="canonical"\s+href="[^"]*"\s*/?>'
    
    # Check if canonical tag already exists
    existing_canonical = re.search(canonical_pattern, content, re.IGNORECASE)
    
    if existing_canonical:
        # Replace existing canonical tag
        old_tag = existing_canonical.group(0)
        new_tag = f'<link rel="canonical" href="{canonical_url}">'
        new_content = content.replace(old_tag, new_tag)
        action = "UPDATE"
    else:
        # Find the closing </head> tag and insert before it
        # Look for </head> with optional whitespace before it
        head_close_pattern = r'(\n\s*)</head>'
        match = re.search(head_close_pattern, content, re.IGNORECASE)
        
        if match:
            # Insert the canonical tag before </head>
            insert_pos = match.end(1)  # Position right after the newline
            canonical_tag = f'    <link rel="canonical" href="{canonical_url}">\n'
            new_content = content[:insert_pos] + canonical_tag + content[insert_pos:]
            action = "INSERT"
        else:
            print(f"⚠ ERROR {rel_path} - Could not find </head> with proper formatting")
            continue
    
    # Write the updated content
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ {action} {rel_path}")
    print(f"  URL: {canonical_url}")

print("\nDone!")
