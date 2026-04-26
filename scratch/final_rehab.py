import os
import re
from pathlib import Path

def final_rehabilitation(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Filename-based Title
    true_title = Path(file_path).stem.replace('_', ' ').title()
    if true_title == "Pca": true_title = "PCA"
    if true_title == "Svd": true_title = "SVD"
    if true_title == "Kk T": true_title = "KKT"
    if true_title == "Mdp": true_title = "MDP"
    if true_title == "Gcn": true_title = "GCN"
    
    # 2. Extract Body (everything after the second ---)
    parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) >= 3:
        body = parts[2].strip()
    else:
        body = content.strip()

    # 3. Clean Body from duplicate headers
    # Remove # Title, # Chapter, # <div..., *** at the very top
    body = re.sub(r'^(?:#.*?\n|\*\*\*|\s|<div.*?>|</div>)*', '', body).strip()

    # 4. Spacing Fix
    # Ensure blank lines before markers
    markers = ['**The Story:**', '**The Setup:**', '**Calculation:**', '**The Calculation:**']
    for m in markers:
        body = body.replace(m, '\n\n' + m + '\n')
    
    # Ensure blank lines around math
    body = body.replace('$$', '\n\n$$\n\n')
    
    # Clean up excessive newlines
    body = re.sub(r'\n{3,}', r'\n\n', body)

    # 5. Assemble
    fm = f"""---
title: "{true_title}"
description: "Mastering {true_title} for Machine Learning."
complexity: "Intermediate"
estimated_time: "20 min"
prerequisites: ["Foundations"]
---"""

    final_content = f"{fm}\n\n# {true_title}\n\n***\n\n{body.strip()}\n"
    
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(final_content)

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    if p.name == 'index.md': continue
    final_rehabilitation(str(p))

print("Final rehabilitation complete.")
