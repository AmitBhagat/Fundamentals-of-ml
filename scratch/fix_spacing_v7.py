import os
import re

def fix_spacing(content):
    content = content.replace('\r\n', '\n')
    
    # 1. Bold Markers: Ensure blank line before
    markers = [
        r'\*\*The Story:\*\*', 
        r'\*\*The Setup:\*\*', 
        r'\*\*Calculation:\*\*', 
        r'\*\*The Calculation:\*\*',
        r'\*\*Calculation\*\*'
    ]
    for m in markers:
        # Use regex to find single newline before marker and replace with double
        content = re.sub(r'(?<!\n)\n' + m, r'\n\n' + m, content)

    # 2. Display Math: Ensure blank lines around
    content = re.sub(r'(?<!\n)\n\$\$', r'\n\n$$', content)
    content = re.sub(r'\$\$\n(?!\n)', r'$$\n\n', content)

    # 3. Example Headers: Ensure blank line before
    content = re.sub(r'(?<!\n)\n### (\d+\.)', r'\n\n### \1', content)
    
    # 4. Blockquotes: Ensure blank line before
    content = re.sub(r'(?<!\n)\n> \[!', r'\n\n> [!', content)

    # Clean up excess newlines (3 or more -> 2)
    content = re.sub(r'\n{3,}', r'\n\n', content)

    return content

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
