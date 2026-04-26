import os
import re

def fix_spacing(content):
    # Standardize to \n
    content = content.replace('\r\n', '\n')
    
    # 1. Bold Markers: Ensure blank line before
    markers = [
        '**The Story:**', 
        '**The Setup:**', 
        '**Calculation:**', 
        '**The Calculation:**',
        '**Calculation**'
    ]
    for m in markers:
        # Match marker that is NOT preceded by a blank line
        # Use a loop to catch multiple occurrences
        while '\n' + m in content:
            new_content = content.replace('\n' + m, '\n\n' + m)
            if new_content == content: break
            content = new_content
            # Clean up triple newlines
            content = content.replace('\n\n\n', '\n\n')

    # 2. Display Math: Ensure blank lines around
    content = re.sub(r'([^\n])\s*\n\s*\$\$', r'\1\n\n$$', content)
    content = re.sub(r'\$\$\s*\n\s*([^\n])', r'$$\n\n\1', content)

    # 3. Example Headers: Ensure blank line before
    content = re.sub(r'([^\n])\s*\n\s*### (\d+\.)', r'\1\n\n### \2', content)
    
    # 4. Blockquotes: Ensure blank line before
    content = re.sub(r'([^\n])\s*\n\s*> \[!', r'\1\n\n> [!', content)

    # Clean up excess newlines
    content = re.sub(r'\n{3,}', r'\n\n', content)

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
    
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(new_content)

for root, dirs, files in os.walk('content'):
    for file in files:
        if file.endswith('.md'):
            process_file(os.path.join(root, file))
