import os
import re
import xml.etree.ElementTree as ET

# --- PATHS ---
BASE_DIR = r'C:\Users\g7schuh1\AppData\Local\SynologyDrive\SystemFolders\1\GIT_wmexperts.online\wmexperts.online\migrate'
XML_FILE = os.path.join(BASE_DIR, 'export.xml')
TEMPLATE_FILE = os.path.join(BASE_DIR, 'article-template.html')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'articles')

NAMESPACES = {'content': 'http://purl.org/rss/1.0/modules/content/', 'wp': 'http://wordpress.org/export/1.2/'}

def migrate():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    print("Checking XML...")
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    
    for item in root.findall('.//item'):
        p_type = item.find('wp:post_type', NAMESPACES)
        p_status = item.find('wp:status', NAMESPACES)

        if p_type is not None and p_type.text == 'post' and p_status.text == 'publish':
            title = item.find('title').text or "Untitled"
            content = item.find('content:encoded', NAMESPACES).text or ""
            
            # --- RE-READ TEMPLATE EVERY TIME ---
            with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
                fresh_template = f.read()

            # --- FORCE ONLY ONE REPLACEMENT ---
            # The '1' at the end ensures it doesn't loop
            output_html = fresh_template.replace('', content, 1)
            
            # --- SAFETY CIRCUIT BREAKER ---
            if len(output_html) > 500000: # If file is > 0.5MB, stop!
                print(f"🛑 SAFETY STOP: {title} is too large. Check your template for loops.")
                break

            filename = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') + ".html"
            
            with open(os.path.join(OUTPUT_FOLDER, filename), 'w', encoding='utf-8') as f:
                f.write(output_html)
            
            print(f"Done: {filename}")

if __name__ == "__main__":
    migrate()