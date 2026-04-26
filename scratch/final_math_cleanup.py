import os
import re
from pathlib import Path

def final_math_cleanup(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Ensure $$ are on their own lines
    content = content.replace('$$', '\n\n$$\n\n')
    
    # 2. Fix the mashing of text after $$
    # Pattern: $$Text -> $$\nText
    content = re.sub(r'(\$\$)([^\s\n])', r'\1\n\2', content)
    # Pattern: Text$$ -> Text\n$$
    content = re.sub(r'([^\s\n])(\$\$)', r'\1\n\2', content)

    # 3. Fix the \begin{aligned} spacing
    content = content.replace('\\begin{aligned}', '\n\\begin{aligned}\n')
    content = content.replace('\\end{aligned}', '\n\\end{aligned}\n')

    # 4. Remove excessive newlines created by replacements
    content = re.sub(r'\n{3,}', r'\n\n', content)

    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content.strip() + '\n')

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    if p.name == 'index.md': continue
    final_math_cleanup(str(p))

print("Final math cleanup complete.")
