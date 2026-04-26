import os
import re
from pathlib import Path

def finalize_spacing(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Ensure exactly one blank line after every pedagogical marker
    markers = [r'\*\*Setup:\*\*', r'\*\*Calculation:\*\*', r'\*\*The Story:\*\*']
    for m in markers:
        # Replace Marker\n(Not \n) with Marker\n\n(Not \n)
        content = re.sub(rf'({m})\n(?!\n)', r'\1\n\n', content)
        # Replace Marker\n\n\n+ with Marker\n\n
        content = re.sub(rf'({m})\n\s*\n\s*\n+', r'\1\n\n', content)

    # 2. Fix the triple separator overkill
    content = re.sub(r'(\*\*\*|\-\-\-)\s*\n\s*(\*\*\*|\-\-\-)\s*\n\s*(\*\*\*|\-\-\-)', r'***', content)
    content = re.sub(r'(\*\*\*|\-\-\-)\s*\n\s*(\*\*\*|\-\-\-)', r'***', content)
    
    # 3. Final Spacing
    content = re.sub(r'\n{3,}', r'\n\n', content)
    
    # 4. Correct specific currency/math mashing again (just in case)
    content = content.replace('$$\n\n25$', '$25$')
    content = content.replace('$$\n25$', '$25$')

    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content.strip() + '\n')

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    if p.name == 'index.md': continue
    finalize_spacing(str(p))

print("Final spacing pass complete.")
