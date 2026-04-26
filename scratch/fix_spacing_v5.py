import os
import re

def fix_spacing(content):
    # 1. Bold Markers: Ensure blank line before
    markers = [
        r'\*\*The Story:\*\*', 
        r'\*\*The Setup:\*\*', 
        r'\*\*Calculation:\*\*', 
        r'\*\*The Calculation:\*\*',
        r'\*\*Calculation\*\*'
    ]
    for m in markers:
        # Match marker that is NOT preceded by a blank line
        # Use \n([^\n]) to find a single newline followed by content
        content = re.sub(r'([^\n])\n' + m, r'\1\n\n' + m.replace('\\', ''), content)

    # 2. Display Math: Ensure blank lines around
    content = re.sub(r'([^\n])\n\$\$', r'\1\n\n$$', content)
    content = re.sub(r'\$\$\n([^\n])', r'$$\n\n\1', content)

    # 3. Example Headers: Ensure blank line before
    content = re.sub(r'([^\n])\n### (\d+\.)', r'\1\n\n### \2', content)
    
    # 4. Blockquotes: Ensure blank line before
    content = re.sub(r'([^\n])\n> \[!', r'\1\n\n> [!', content)

    return content

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = re.split(r'^---\s*\n', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3: return
    
    fm = parts[1]
    body = parts[2]
    
    new_body = fix_spacing(body)
    new_content = f"---\n{fm}---\n\n{new_body}\n"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

for root, dirs, files in os.walk('content'):
    for file in files:
        if file.endswith('.md'):
            process_file(os.path.join(root, file))
