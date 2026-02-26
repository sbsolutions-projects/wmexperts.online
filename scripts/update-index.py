#!/usr/bin/env python3
"""
WMexperts Index Updater
Automatically updates index.html with the featured post and 5 most recent blog posts.
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime
from html.parser import HTMLParser
from collections import namedtuple

# Define BlogPost structure
BlogPost = namedtuple('BlogPost', ['file_path', 'relative_path', 'date_published', 'title', 'description', 'reading_time', 'icon', 'tag'])

class MetaTagParser(HTMLParser):
    """Parse HTML meta tags to extract blog post metadata"""
    def __init__(self):
        super().__init__()
        self.date_published = None
        self.title = None
        self.description = None
        self.reading_time = '10 min read'
        
    def handle_starttag(self, tag, attrs):
        if tag == 'meta':
            attr_dict = dict(attrs)
            
            # Get publication date
            if attr_dict.get('property') == 'article:published_time':
                self.date_published = attr_dict.get('content')
            
            # Get title
            elif attr_dict.get('property') == 'og:title':
                self.title = attr_dict.get('content')
            
            # Get description
            elif attr_dict.get('property') == 'og:description':
                self.description = attr_dict.get('content')
            
            # Get reading time (meta name might vary)
            elif attr_dict.get('name') == 'reading-time':
                self.reading_time = attr_dict.get('content')

def extract_post_metadata(file_path, root_dir):
    """Extract metadata from a blog post HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        parser = MetaTagParser()
        parser.feed(content)
        
        if not parser.date_published:
            print(f"⚠️  No publication date found for: {file_path}")
            return None
        
        # Parse date
        try:
            date_obj = datetime.strptime(parser.date_published, '%Y-%m-%d')
        except ValueError:
            print(f"⚠️  Invalid date format for: {file_path}")
            return None
        
        # Get category from folder structure
        category_folder = Path(file_path).parent.name
        category_map = {
            'mfs': {'icon': '🏗️', 'tag': 'Discover SAP EWM MFS'},
            'understand': {'icon': '🎓', 'tag': 'Understand SAP EWM'},
            'enhance': {'icon': '🔧', 'tag': 'Enhance SAP EWM'},
            'reveal': {'icon': '🔍', 'tag': 'Reveal SAP EWM'},
            'around': {'icon': '📊', 'tag': 'Around SAP EWM'},
            'work': {'icon': '💼', 'tag': 'Working as a SAP EWM Consultant'}
        }
        
        category_info = category_map.get(category_folder, {'icon': '📄', 'tag': category_folder})
        
        # Get relative path from root (parent directory of scripts folder)
        relative_path = os.path.relpath(file_path, root_dir).replace('\\', '/')
        
        # Clean up title - remove "| WMexperts" suffix if present
        title = parser.title or 'Untitled'
        title = title.replace(' | WMexperts', '').strip()
        
        # Truncate description to 150 chars
        description = parser.description or ''
        description = ' '.join(description.split())[:150]
        
        return BlogPost(
            file_path=file_path,
            relative_path=relative_path,
            date_published=date_obj,
            title=title,
            description=description,
            reading_time=parser.reading_time,
            icon=category_info['icon'],
            tag=category_info['tag']
        )
    
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return None

def find_all_blog_posts(blog_dir):
    """Recursively find all HTML files in blog-posts directory"""
    posts = []
    for root, dirs, files in os.walk(blog_dir):
        for file in files:
            if file.endswith('.html'):
                posts.append(os.path.join(root, file))
    return posts

def format_date_display(date_obj):
    """Format date for display (e.g., 'May 2025')"""
    return date_obj.strftime('%b %Y')

def generate_card_html(post, is_featured=False):
    """Generate HTML for a blog card"""
    class_attr = ' featured' if is_featured else ''
    featured_tag = '<span class="tag">📌 Featured</span>' if is_featured else f'<span class="tag">{post.tag}</span>'
    
    return f"""                <a href="{post.relative_path}" class="card{class_attr}" data-date="{post.date_published.strftime('%Y-%m-%d')}">
                    <div class="card-header">
                        <div class="icon">{post.icon}</div>
                        {featured_tag}
                    </div>
                    <h3>{post.title}</h3>
                    <p>{post.description}</p>
                    <div class="card-meta">
                        <span>🕒 {post.reading_time}</span>
                        <span>📅 {format_date_display(post.date_published)}</span>
                    </div>
                </a>
"""

def update_index_html(index_file, featured, next_five):
    """Update the index.html file with new grid content"""
    try:
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the grid section
        pattern = r'<div class="grid" id="posts-grid">.*?</div>\s*\n\s*<!-- VIEW ALL LINK -->'
        
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            print("❌ Could not find grid section in index.html")
            return False
        
        # Generate new grid content
        new_grid = '            <div class="grid" id="posts-grid">\n'
        new_grid += generate_card_html(featured, True)
        for post in next_five:
            new_grid += generate_card_html(post, False)
        new_grid += '            </div>\n            \n            <!-- VIEW ALL LINK -->'
        
        # Replace the grid
        new_content = content[:match.start()] + new_grid + content[match.end():]
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    
    except Exception as e:
        print(f"❌ Error updating index.html: {e}")
        return False

def main():
    """Main function"""
    script_dir = Path(__file__).parent.absolute()
    root_dir = script_dir.parent  # Go up one level to the main project directory
    
    blog_posts_dir = root_dir / 'blog-posts'
    index_file = root_dir / 'index.html'
    
    # Verify directories exist
    if not blog_posts_dir.exists():
        print(f"❌ Blog posts directory not found: {blog_posts_dir}")
        sys.exit(1)
    
    if not index_file.exists():
        print(f"❌ Index file not found: {index_file}")
        sys.exit(1)
    
    print("🔍 Scanning blog posts...")
    
    # Find all blog posts
    all_posts = find_all_blog_posts(str(blog_posts_dir))
    print(f"📝 Found {len(all_posts)} blog post files")
    
    # Extract metadata
    posts = []
    for post_file in all_posts:
        metadata = extract_post_metadata(post_file, str(root_dir))
        if metadata:
            posts.append(metadata)
    
    if not posts:
        print("❌ No valid blog posts found!")
        sys.exit(1)
    
    # Sort by date (newest first)
    posts.sort(key=lambda x: x.date_published, reverse=True)
    
    print(f"✅ Processed {len(posts)} posts with valid dates")
    
    # Get featured and next 5
    featured = posts[0]
    next_five = posts[1:6]
    
    if len(next_five) < 5:
        print(f"⚠️  Warning: Only {len(next_five)} posts available (at least 5 recommended)")
    
    print(f"\n🌟 Featured: {featured.title}")
    print("📑 Next 5 posts:")
    for i, post in enumerate(next_five, 1):
        print(f"   {i}. {post.title}")
    
    # Update index.html
    print("\n📝 Updating index.html...")
    if update_index_html(str(index_file), featured, next_five):
        print("✅ Index page updated successfully!")
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
