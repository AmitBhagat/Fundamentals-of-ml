import os
import re
from pathlib import Path

def fix_cards_v2(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Standardize frontmatter
    parts = re.split(r'^---\s*$', content, flags=re.MULTILINE)
    if len(parts) >= 3:
        fm = parts[1].strip()
        body = '---'.join(parts[2:]).strip()
    else:
        fm = ""
        body = content.strip()

    # 2. Cleanup body
    # Remove redundant title
    title_match = re.search(r'title: "(.*?)"', fm)
    title = title_match.group(1) if title_match else Path(file_path).stem.replace('_', ' ').title()
    
    # Remove any # Title or # Chapter... at the start
    body = re.sub(r'^(?:#.*?\n|\*\*\*|\s)*', '', body).strip()
    
    # 3. Clean blockquotes
    body = re.sub(r'>\s*["\']\s*\n', '', body)
    body = re.sub(r'(> - \*\*.*?\*\*:) " (.*?) "', r'\1 \2', body)
    body = re.sub(r'> ## Prerequisite', r'> ### Prerequisite', body)
    
    # Remove triple-dash leftovers
    body = re.sub(r'^---\s*$', '***', body, flags=re.MULTILINE)

    # 4. Spacing cleanup
    body = re.sub(r'\n{3,}', r'\n\n', body)

    final_content = f"---\ntitle: \"{title}\"\ndescription: \"Mastering {title} for ML.\"\ncomplexity: \"Intermediate\"\nestimated_time: \"20 min\"\nprerequisites: [\"Foundations\"]\n---\n\n# {title}\n\n***\n\n{body.strip()}\n"
    
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(final_content)

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    if p.name == 'index.md': continue
    fix_cards_v2(str(p))

print("Cards correction v2 complete.")
