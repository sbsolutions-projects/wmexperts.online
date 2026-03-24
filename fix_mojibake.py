#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

exclude_files = ['header-content.html', 'footer-content.html', 'article-template.html', 'blog-post-template.html']

# String replacements for mojibake patterns
# Format: broken -> fixed
string_replacements = {
    'â†'': '→',
    'â–¶': '▶',
    'Dâ€™': "D'",
    'Material Flowâ€™': "'Material Flow'",
}

fixed_count = 0
total_files = 0
total_replacements = 0

for root, dirs, files in os.walk('.'):
    for file in files:
        if not file.endswith('.html'):
            continue
        if any(x in file for x in exclude_files):
            continue
        if 'fix_' in file:
            continue
            
        filepath = os.path.join(root, file)
        total_files += 1
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            original_content = content
            replacements = 0
            
            for broken, fixed in string_replacements.items():
                if broken in content:
                    count = content.count(broken)
                    content = content.replace(broken, fixed)
                    replacements += count
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print('Fixed: {0} ({1} changes)'.format(filepath, replacements))
                fixed_count += 1
                total_replacements += replacements
                
        except Exception as e:
            print('Error with {0}: {1}'.format(filepath, e))

print("\nSummary: Fixed {0} files out of {1} total HTML files with {2} total changes".format(
    fixed_count, total_files, total_replacements))
