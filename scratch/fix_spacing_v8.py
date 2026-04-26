import os
import re

def fix_spacing(content):
    content = content.replace('\r\n', '\n')
    
    markers = [
        '**The Story:**', 
        '**The Setup:**', 
        '**Calculation:**', 
        '**The Calculation:**',
        '**Calculation**'
    ]
    for m in markers:
        # Add a newline before every marker
        content = content.replace(m, '\n\n' + m)

    # Add newlines around math
    content = content.replace('$$', '\n\n$$\n\n')
    
    # Fix headers
    content = re.sub(r'(### \d+\.)', r'\n\n\1', content)
    content = re.sub(r'(## )', r'\n\n\1', content)
    content = re.sub(r'(> \[!)', r'\n\n\1', content)

    # Clean up mess (3+ newlines -> 2)
    while '\n\n\n' in content:
        content = content.replace('\n\n\n', '\n\n')
    
    # Clean up space after math block inside
    content = re.sub(r'\$\$\s*\n\s*\n', r'$$\n', content)
    content = re.sub(r'\n\s*\n\s*\$\$', r'\n$$', content)
    # Wait, the above might be wrong. Let's just use:
    content = re.sub(r'\n{2,}\$\$', r'\n\n$$', content)
    content = re.sub(r'\$\$\n{2,}', r'$$\n\n', content)

    return content.strip()

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    parts = re.split(r'^---\s*\n', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3: return
    new_body = fix_spacing(parts[2])
    new_content = f"---\n{parts[1]}---\n\n{new_body}\n"
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(new_content)

for root, dirs, files in os.walk('content'):
    for file in files:
        if file.endswith('.md'):
            process_file(os.path.join(root, file))
