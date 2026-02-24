#!/usr/bin/env python3
import os
import re
from pathlib import Path
from datetime import datetime

# Dictionary to store all articles by category
articles_by_category = {}

# Categories and their folders
categories = {
    'understand': 'blog-posts/understand',
    'around': 'blog-posts/around',
    'work': 'blog-posts/work',
    'enhance': 'blog-posts/enhance',
    'reveal': 'blog-posts/reveal',
    'mfs': 'blog-posts/mfs'
}

# Estimate read time based on file size
def estimate_read_time(word_count):
    if word_count < 1500:
        return 8
    elif word_count < 2000:
        return 10
    elif word_count < 2500:
        return 12
    elif word_count < 3000:
        return 14
    else:
        return 16

# Function to extract metadata from HTML file
def extract_metadata(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract description
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
    description = desc_match.group(1) if desc_match else ''
    
    # Extract published date
    date_match = re.search(r'<meta property="article:published_time" content="(\d{4}-\d{2}-\d{2})"', content)
    published_date = date_match.group(1) if date_match else '2024-01-01'
    
    # Extract headline from structured data
    headline_match = re.search(r'"headline": "([^"]+)"', content)
    headline = headline_match.group(1) if headline_match else 'Article'
    
    # Extract H1 from article body
    h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
    h1_title = h1_match.group(1) if h1_match else headline
    
    # Rough word count estimate (simple: count words in content)
    word_count = len(content.split())
    read_time = estimate_read_time(word_count)
    
    return {
        'title': h1_title.strip(),
        'description': description,
        'date': published_date,
        'headline': headline,
        'read_time': read_time
    }

# Extract all articles
for category, folder_path in categories.items():
    articles_by_category[category] = []
    full_path = Path(folder_path)
    
    if full_path.exists():
        for html_file in sorted(full_path.glob('*.html')):
            metadata = extract_metadata(html_file)
            metadata['filename'] = html_file.name
            metadata['relative_path'] = f'{folder_path}/{html_file.name}'
            articles_by_category[category].append(metadata)

# Sort articles by date within each category
for category in articles_by_category:
    articles_by_category[category].sort(key=lambda x: x['date'])

# Format date function
def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%b %Y')

# Generate HTML for each category
print("\n\n=== ARTICLE GRIDS HTML ===\n")

for category, articles in articles_by_category.items():
    print(f"\n<!-- {category.upper()} SECTION: {len(articles)} articles -->")
    print(f"""    <section id="{category}" class="category-section">
        <div class="category-header">""")
    
    # Category header (you may need to customize icons and titles)
    category_info = {
        'understand': ('🎓', 'Understand SAP EWM'),
        'around': ('🔄', 'Around SAP EWM'),
        'work': ('💼', 'Working as a EWM Consultant'),
        'enhance': ('🔧', 'Enhance SAP EWM'),
        'reveal': ('🔍', 'Reveal SAP EWM'),
        'mfs': ('🏗️', 'Discover SAP EWM MFS')
    }
    
    icon, title = category_info[category]
    tool_icon_class = 'tool-icon' if category == 'enhance' else ''
    
    print(f"""            <div class="category-icon">{f'<span class="{tool_icon_class}">' + icon + '</span>' if tool_icon_class else icon}</div>
            <h2>{title}</h2>
            <span class="count">{len(articles)} articles</span>
        </div>
        <div class="article-grid">""")
    
    # Articles
    for idx, article in enumerate(articles, 1):
        article_num = f"{idx:02d}"
        article_date = format_date(article['date'])
        # Truncate description if too long
        desc = article['description'][:120] + "..." if len(article['description']) > 120 else article['description']
        
        print(f"""            <a href="blog-posts/{category}/{article['filename']}" class="article-card">
                <span class="article-number">{article_num}</span>
                <h3>{article['title']}</h3>
                <p>{desc}</p>
                <div class="article-meta">
                    <span>🕒 {article['read_time']} min</span>
                    <span>📅 {article_date}</span>
                </div>
            </a>""")
    
    print("""        </div>
    </section>""")

print("\n\n=== DEBUG INFO ===\n")
for category, articles in articles_by_category.items():
    print(f"\n{category.upper()} ({len(articles)} articles):")
    for idx, article in enumerate(articles, 1):
        print(f"  {idx:2d}. {article['filename']:40s} | {article['date']} | {article['title'][:50]}")
