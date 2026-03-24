import os

# Mojibake emoji patterns that need fixing
# Key: broken bytes, Value: correct UTF-8 bytes for emoji
emoji_fixes = {
    # Newsletter/Email emoji (📧)
    b'\xc3\xb0\xc5\xb8\xe2\x80\x9d\xc2\xa7': b'\xf0\x9f\x93\xa7',  # v1
    b'\xc3\xb0\xc5\xb8\xe2\x80\x9c\xc2\xa7': b'\xf0\x9f\x93\xa7',  # v2
    # Play button (▶️)
    b'\xe2\x96\xb6\xc3\xaf\xc2\xb8\xc2\x8f': b'\xe2\x96\xb6\xef\xb8\x8f',
    
    # Page/Document patterns
    b'\xc3\xb0\xc5\xb8\xe2\x80\x9d\xe2\x80\x9e': b'\xf0\x9f\x93\x84',  # Around
    b'\xc3\xb0\xc5\xb8\xc4\x9e\xe2\x80\x9d': b'\xf0\x9f\x93\x84',  # Document
    
    # Briefcase/Work emoji patterns
    b'\xc3\xb0\xc5\xb8\xe2\x80\x99\xc2\xbc': b'\xf0\x9f\x92\xbc',  # Working
    b'\xc3\xb0\xc5\xb8\xc4\x9c\xc2\xbc': b'\xf0\x9f\x92\xbc',  # Briefcase
    
    # Info/Reveal emoji patterns
    b'\xc3\xb0\xc5\xb8\xe2\x80\x9d\xc2\x8d': b'\xf0\x9f\x94\x8d',  # Reveal
    
    # Map/MFS emoji patterns
    b'\xc3\xb0\xc5\xb8\xc2\x8f\xe2\x80\x94\xc3\xaf\xc2\xb8\xc2\x8f': b'\xf0\x9f\x97\xba',  # Map
    b'\xc3\xb0\xc5\xb8\xc4\x97\xc3\xaf\xc2\xb8': b'\xf0\x9f\x97\xba',  # Map
    
    # Clock/Time emoji patterns
    b'\xc3\xb0\xc5\xb8\xc4\x95\xe2\x80\x99': b'\xf0\x9f\x95\x90',
    b'\xc3\xb0\xc5\xb8\xc4\x95\xe2\x80\x99\xc2\x81': b'\xf0\x9f\x95\x91',
    b'\xc3\xb0\xc5\xb8\xe2\x80\xa2\xe2\x80\x99': b'\xe2\x8f\xb0',  # ⏰ Clock/Timer
    
    # Calendar emoji patterns
    b'\xc3\xb0\xc5\xb8\xc4\xa1\xe2\x80\xa6': b'\xf0\x9f\x93\x85',
    b'\xc3\xb0\xc5\xb8\xe2\x80\x9c\xe2\x80\xa6': b'\xf0\x9f\x93\x85',  # 📅
}

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
            
            # Apply byte-level replacements
            for broken_bytes, fixed_bytes in emoji_fixes.items():
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

print('\nSummary: Fixed {0} files with {1} total replacements'.format(fixed_count, total_replacements))
