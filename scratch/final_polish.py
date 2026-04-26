import os
import re
from pathlib import Path

def clean_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split frontmatter
    parts = re.split(r'^---\s*\n', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3: return
    
    fm = parts[1]
    body = parts[2]
    
    # 1. Remove weird artifacts like # on its own line
    body = re.sub(r'^\s*#\s*$', '', body, flags=re.MULTILINE)
    
    # 2. Fix math blocks: ensure they are tight internally but padded externally
    # Remove excessive newlines inside $$
    body = re.sub(r'\$\$\s*\n\s*\n\s*', r'$$\n', body)
    body = re.sub(r'\n\s*\n\s*\$\$', r'\n$$', body)
    
    # 3. Fix bold marker spacing
    body = re.sub(r'\n\s*\*\*The Story:\*\*\s*\n\s*', r'\n\n**The Story:**\n', body)
    body = re.sub(r'\n\s*\*\*The Setup:\*\*\s*\n\s*', r'\n\n**The Setup:**\n', body)
    body = re.sub(r'\n\s*\*\*Calculation:\*\*\s*\n\s*', r'\n\n**Calculation:**\n', body)
    
    # 4. Remove duplicate titles if any
    title_match = re.search(r'title: "(.*?)"', fm)
    title = title_match.group(1) if title_match else "Chapter"
    
    body = re.sub(f'^# {re.escape(title)}\\s*\\n\\s*\\*\\*\\*\\s*', '', body, flags=re.MULTILINE)
    
    # 5. Clean up multiple newlines
    body = re.sub(r'\n{3,}', r'\n\n', body)
    
    final_content = f"---\n{fm.strip()}\n---\n\n# {title}\n\n***\n\n{body.strip()}\n"
    
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(final_content)

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    if p.name == 'index.md': continue
    clean_file(str(p))
