import os
import re

def fix_spacing(content):
    # 1. Ensure display math has blank lines around it
    # First, strip existing whitespace around $$
    content = re.sub(r'\n*\s*\$\$\s*\n*', r'\n\n$$\n', content)
    content = re.sub(r'\n*\s*\$\$\s*\n*', r'\n$$\n\n', content)
    
    # Actually, a better way:
    content = re.sub(r'(?<!\n)\n?\s*\$\$(.*?)\$\$\s*\n?(?!\n)', r'\n\n$$\1$$\n\n', content, flags=re.DOTALL)

    # 2. Ensure "The Story:", "Calculation:", "The Setup:" etc have blank lines before them
    markers = [
        r'\*\*The Story:\*\*', 
        r'\*\*The Setup:\*\*', 
        r'\*\*Calculation:\*\*', 
        r'\*\*The Calculation:\*\*',
        r'### \d+\.', # Example headers
        r'## ', # Major headers
        r'> \[!', # Blockquotes
    ]
    
    for marker in markers:
        content = re.sub(f'(?<!\n\n)\n?({marker})', r'\n\n\1', content)

    # 3. Clean up triple or more newlines
    content = re.sub(r'\n{3,}', r'\n\n', content)
    
    # 4. Handle blockquote titles and content spacing
    # Sometimes blockquotes have no space after the title [!TYPE]
    content = re.sub(r'(> \[!.*?\])\s*\n(?!>)', r'\1\n> \n', content)
    
    return content.strip()

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
