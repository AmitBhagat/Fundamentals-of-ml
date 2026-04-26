import os
import re
from pathlib import Path

def clean_frontmatter(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Strip any existing frontmatter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
    # Also handle some edge cases
    content = re.sub(r'^---\s*\n.*?\n---', '', content, flags=re.DOTALL)

    # 2. Extract title from body if possible
    title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
        # Remove the title from the body to avoid duplication
        content = content.replace(title_match.group(0), '', 1).strip()
    else:
        title = Path(file_path).stem.replace('_', ' ').title()

    # 3. Create fresh, clean frontmatter
    fm = f"""---
title: "{title}"
description: "Master {title} concepts for Machine Learning."
complexity: "Intermediate"
estimated_time: "20 min"
prerequisites: ["Foundations"]
---"""

    # 4. Cleanup body from HTML remnants at the very top
    content = re.sub(r'^(?:<div.*?>|</div>|\s|\*)*', '', content).strip()
    # Remove any extra # or *** at the start
    content = re.sub(r'^(?:#|\*|\s)*', '', content).strip()

    final_content = f"{fm}\n\n# {title}\n\n***\n\n{content}\n"
    
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(final_content)

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    if p.name == 'index.md': continue
    clean_frontmatter(str(p))

print("Frontmatter reset complete.")
