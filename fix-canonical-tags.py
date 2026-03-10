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
    
    # Pattern for existing canonical link (handles any format)
    # This pattern removes the link even if there's extra whitespace/content around it
    canonical_pattern = r'<link\s+rel="canonical"\s+href="[^"]*"\s*/?>'
    
    # Remove any existing canonical tags
    new_content = re.sub(canonical_pattern, '', content, flags=re.IGNORECASE)
    
    # Create the new canonical tag with proper formatting
    canonical_tag = f'    <link rel="canonical" href="{canonical_url}">\n'
    
    # Find </head> case-insensitive and insert canonical tag right before it
    # This regex finds </head> and puts the canonical link on the line before it
    head_close_pattern = r'(\s*)</head>'
    
    def replace_head_close(match):
        whitespace = match.group(1)
        return f'{canonical_tag}' + whitespace + '</head>'
    
    new_content = re.sub(head_close_pattern, replace_head_close, new_content, flags=re.IGNORECASE)
    
    # Write the updated content
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    fixed_count += 1
    print(f"✓ {rel_path}")

print(f"\n✓ Successfully processed {fixed_count} HTML files")
print("Done!")
