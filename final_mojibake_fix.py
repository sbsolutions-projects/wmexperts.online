import os

# Byte-level replacements 
byte_replacements = [
    (b'\xc3\xa2\xe2\x80\xa0\xe2\x80\x99', b'\xe2\x86\x92'),  # broken -> arrow
    (b'\xc3\xa2\xe2\x96\xb6', b'\xe2\x96\xb6'),  # broken -> play button
]

exclude_files = ['header-content.html', 'footer-content.html', 'article-template.html', 'blog-post-template.html']
fixed_count = 0
total_replacements = 0

for root, dirs, files in os.walk('.'):
    for file in files:
        if not file.endswith('.html') or any(x in file for x in exclude_files):
            continue
        if 'fix_' in file or file.endswith('.py'):
            continue
            
        filepath = os.path.join(root, file)
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            
            original = content
            count = 0
            
            for broken_bytes, fixed_bytes in byte_replacements:
                while broken_bytes in content:
                    content = content.replace(broken_bytes, fixed_bytes)
                    count += 1
            
            if content != original:
                with open(filepath, 'wb') as f:
                    f.write(content)
                print('Fixed: {0} ({1} replacements)'.format(filepath, count))
                fixed_count += 1
                total_replacements += count
                    
        except Exception as e:
            print('Error: {0}'.format(e))

print('Summary: Fixed {0} files with {1} total replacements'.format(fixed_count, total_replacements))
