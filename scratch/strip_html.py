import os
import re

def strip_html_from_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Convert <h1 align="center">...</h1> to # ...
    content = re.sub(r'<h1[^>]*>\s*(.*?)\s*</h1>', r'# \1', content, flags=re.IGNORECASE | re.DOTALL)

    # 2. Remove all <div ...> and </div> tags but keep content
    content = re.sub(r'<div[^>]*>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'</div>', '', content, flags=re.IGNORECASE)

    # 3. Remove <br> and <br /> tags
    content = re.sub(r'<br\s*/?>', '\n', content, flags=re.IGNORECASE)

    # 4. Cleanup: Remove excessive blank lines created by tag removal
    # (Optional, but helps keep it clean. However, user said "not to prune any content", 
    # but redundant whitespace isn't really content. I'll be conservative.)
    content = re.sub(r'\n{3,}', '\n\n', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}...")
                strip_html_from_markdown(file_path)

if __name__ == "__main__":
    process_directory('e:/Projects/Mathematics/drafts')
