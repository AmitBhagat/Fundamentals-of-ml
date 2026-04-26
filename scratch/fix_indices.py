import os
import re
from pathlib import Path

def fix_index_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Standardize Title
    parent_dir = Path(file_path).parent.name
    subject = parent_dir.replace('-', ' ').title()
    
    # 2. Extract Body (everything after any leading ---)
    # If it has --- but it's broken, we just take everything and clean it
    body = re.sub(r'^---\s*\n?', '', content)
    # Remove any other --- that might be there
    body = re.sub(r'^---\s*\n?', '', body, flags=re.MULTILINE)
    
    # 3. Clean Body
    body = re.sub(r'^(?:#.*?\n|\*\*\*|\s|<div.*?>|</div>)*', '', body).strip()

    # 4. Create proper frontmatter
    fm = f"""---
title: "{subject}: Index"
description: "Table of Contents and Subject Overview for {subject}."
complexity: "Beginner"
estimated_time: "5 min"
prerequisites: []
---"""

    final_content = f"{fm}\n\n# {subject}: The Architecture of Data\n\n***\n\n{body}\n"
    
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(final_content)

content_dir = Path('content')
for p in content_dir.rglob('index.md'):
    try:
        fix_index_file(str(p))
        print(f"Fixed index: {p}")
    except Exception as e:
        print(f"Error fixing {p}: {e}")
