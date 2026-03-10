#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Base directory (workspace root)
base_dir = Path(__file__).parent
base_url = "https://wmexperts.online"

# Find all HTML files
html_files = list(base_dir.glob('**/*.html'))
print(f"Found {len(html_files)} HTML files, fixing formatting...")

fixed_count = 0

for html_file in sorted(html_files):
    # Skip the script itself
    if html_file.name.endswith('.py'):
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
        continue
    
    # Check if file has </head> tag
    if '</head>' not in content.lower():
        continue
    
    # Check if canonical tag already exists
    if f'rel="canonical"' in content:
        # Remove the old one first - match it with any surrounding content on the same line
        # This pattern matches: ...content<link rel="canonical"...>rest of line...
        canonical_pattern = r'(\s*)<link\s+rel="canonical"\s+href="[^"]*"\s*/?>\s*'
        new_content = re.sub(canonical_pattern, r'\1', content, flags=re.IGNORECASE)
    else:
        new_content = content
    
    # Create the new canonical tag
    canonical_tag = f'    <link rel="canonical" href="{canonical_url}">'
    
    # Find </head> and ensure canonical tag is on the line immediately before it
    # Match: any character right before </head> (could be > from previous tag or whitespace)
    # We want to insert the canonical tag with a newline before </head>
    
    # First, let's check what's immediately before </head>
    head_close_pattern = r'([^<]*)</head>'
    
    def replace_head_close(match):
        before_head = match.group(1)
        # If before_head ends with newline or is just whitespace, we're good
        if before_head.strip() == '':
            # before_head is whitespace, insert canonical tag with proper newline
            return f'{canonical_tag}\n{before_head}</head>'
        else:
            # before_head has content, need to add newline before canonical tag
            return f'{before_head.rstrip()}\n{canonical_tag}\n    </head>'
    
    new_content = re.sub(head_close_pattern, replace_head_close, new_content, flags=re.IGNORECASE)
    
    # Write the updated content
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    fixed_count += 1
    if fixed_count % 10 == 0 or fixed_count <= 5:
        print(f"✓ {rel_path}")

print(f"\n✓ Successfully processed {fixed_count} HTML files")
print("Done!")
