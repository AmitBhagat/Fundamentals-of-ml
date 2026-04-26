import os
import re

content_dir = 'content'

def fix_setup_spacing(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Ensure blank line before **The Setup:** if it follows a header
    content = re.sub(r'(### \d+\..*)\n\*\*The Setup:\*\*', r'\1\n\n**The Setup:**', content)
    
    # Ensure blank line before ### X. Title if it follows text or a horizontal rule
    content = re.sub(r'(---\n)(### \d+\..*)', r'\1\n\2', content)

    # Clean up double blank lines
    content = re.sub(r'\n{3,}', r'\n\n', content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

for root, dirs, files in os.walk(content_dir):
    for file in files:
        if file.endswith('.md'):
            fix_setup_spacing(os.path.join(root, file))
