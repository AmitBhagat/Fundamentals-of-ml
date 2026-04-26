import os
import re
from pathlib import Path

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Extract/Add Frontmatter
    has_frontmatter = content.startswith('---')
    if has_frontmatter:
        parts = re.split(r'^---\s*\n', content, maxsplit=2, flags=re.MULTILINE)
        fm = parts[1]
        body = parts[2]
    else:
        # Create default frontmatter
        title_match = re.search(r'<h1.*?>\s*(?:Chapter \d+:\s*)?(.*?)\s*</h1>', content, re.IGNORECASE)
        title = title_match.group(1) if title_match else Path(file_path).stem.replace('_', ' ').title()
        fm = f'title: "{title}"\ndescription: "Mastering {title} for ML."\ncomplexity: "Intermediate"\nestimated_time: "20 min"\nprerequisites: ["Foundations"]'
        body = content

    # 2. Clean Body
    # Remove HTML title if duplicated
    body = re.sub(r'<h1.*?>.*?</h1>', '', body, flags=re.IGNORECASE)
    # Remove HR after title
    body = re.sub(r'^\s*\*\*\*\s*', '', body, flags=re.MULTILINE)
    # Remove justify div
    body = re.sub(r'<div style="text-align: justify;">', '', body)
    body = re.sub(r'</div>\s*$', '', body.strip())

    # 3. Fix Spacing (Aggressive)
    # Standardize markers
    body = body.replace('**The Story:**', '\n\n**The Story:**\n\n')
    body = body.replace('**The Setup:**', '\n\n**The Setup:**\n\n')
    body = body.replace('**Calculation:**', '\n\n**Calculation:**\n\n')
    body = body.replace('**The Calculation:**', '\n\n**The Calculation:**\n\n')
    
    # Standardize math blocks
    body = body.replace('$$', '\n\n$$\n\n')
    
    # Fix Headers
    body = re.sub(r'(### \d+\.)', r'\n\n\1', body)
    body = re.sub(r'(## )', r'\n\n\1', body)
    body = re.sub(r'(> \[!)', r'\n\n\1', body)
    
    # Deduplicate newlines
    body = re.sub(r'\n{3,}', r'\n\n', body)
    
    # 4. Final Assemblage
    new_title = fm.split('\n')[0].replace('title: "', '').replace('"', '')
    final_content = f"---\n{fm.strip()}\n---\n\n# {new_title}\n\n***\n\n{body.strip()}\n"
    
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(final_content)

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    if p.name == 'index.md': continue
    try:
        fix_file(str(p))
        print(f"Fixed: {p}")
    except Exception as e:
        print(f"Error fixing {p}: {e}")
