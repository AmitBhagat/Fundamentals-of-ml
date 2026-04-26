import os
import re
from pathlib import Path

def repair_structure(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix the double-hash titles
    content = re.sub(r'^#\s*#\s*', '# ', content, flags=re.MULTILINE)
    
    # 2. Fix the broken currency/math mashing
    # It turned "$25$" into "$$ 25$" due to spacing script
    content = content.replace('$$\n\n25$', '$25$')
    content = content.replace('$$\n25$', '$25$')
    
    # 3. Fix redundant separators
    content = re.sub(r'\*\*\*\s*\n\s*\*\*\*', '***', content)
    
    # 4. Remove the extra headers added at the top
    # We want ONLY ONE # Title at the very top
    lines = content.split('\n')
    title_found = False
    new_lines = []
    for line in lines:
        if line.startswith('# ') and not title_found:
            new_lines.append(line)
            title_found = True
        elif line.startswith('# ') and title_found:
            # Check if it's a sub-example or section
            if 'Example' in line:
                new_lines.append(line.replace('# ', '## '))
            else:
                # Duplicate title, skip
                continue
        else:
            new_lines.append(line)
    content = '\n'.join(new_lines)

    # 5. Spacing for markers (Setup, Calculation, The Story)
    # Ensure they have a blank line AFTER them
    markers = ['**Setup:**', '**Calculation:**', '**The Story:**']
    for m in markers:
        # If marker is followed immediately by text, add newline
        content = re.sub(rf'({re.escape(m)})\n(?!\n)', r'\1\n\n', content)

    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    if p.name == 'index.md': continue
    repair_structure(str(p))

print("Structure repaired.")
