import os
import re
from pathlib import Path

def normalize_lesson_structure(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix the common markers
    # Ensure they are bold and have blank lines around them
    markers = ['Setup', 'Calculation', 'The Story', 'The Calculation', 'The Setup']
    for m in markers:
        # Pattern: Optional whitespace, optional bolding, the marker, optional colon, trailing space/newline
        # Replace with \n\n**Marker:**\n\n
        pattern = rf'^\s*\*{{0,2}}{m}:?\*{{0,2}}\s*$'
        content = re.sub(pattern, f'\n\n**{m}:**\n\n', content, flags=re.MULTILINE | re.IGNORECASE)

    # 2. Fix specific LaTeX corruption like \$25 or similar
    # Remove escaped dollars if they are causing mashing
    content = content.replace('\\$25', '$25')
    
    # 3. Fix math block spacing (already mostly good, but reinforce)
    content = content.replace('$$', '\n\n$$\n\n')
    
    # 4. Clean up multiple newlines
    content = re.sub(r'\n{3,}', r'\n\n', content)
    
    # 5. Fix titles that might have been messed up
    content = re.sub(r'^#\s*(.*?)\s*$', r'# \1\n\n***\n', content, flags=re.MULTILINE)
    # Deduplicate separators
    content = re.sub(r'\n\s*\*\*\*\s*\n\s*\*\*\*\s*\n', r'\n\n***\n\n', content)

    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    if p.name == 'index.md': continue
    normalize_lesson_structure(str(p))

print("Structure normalized.")
