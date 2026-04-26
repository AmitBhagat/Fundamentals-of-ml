import os
import re
from pathlib import Path

def cleanup_nesting(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix the double-nesting created by previous script
    content = content.replace('> >', '>')
    
    # Ensure there is a blank line (just a >) after specific bold titles in blocks
    markers = [
        'THE INTUITION',
        'CRITICAL INSIGHT',
        'Debugging Tip',
        'Practical Tip',
        'Deep Dive',
        'Gotcha'
    ]
    
    for m in markers:
        # Pattern: line starting with > **MARKER**
        # If the next line starts with > and is NOT empty, insert an empty > line
        lines = content.split('\n')
        new_lines = []
        for i in range(len(lines)):
            new_lines.append(lines[i])
            if (f'**{m}**' in lines[i] or f'**{m}:**' in lines[i]) and lines[i].strip().startswith('>'):
                # Check if next line is already empty or a header
                if i+1 < len(lines) and lines[i+1].strip().startswith('>') and len(lines[i+1].strip()) > 1:
                    if '###' not in lines[i+1]: # Don't add if next is already a header
                        new_lines.append('>')
        content = '\n'.join(new_lines)

    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    if p.name == 'index.md': continue
    cleanup_nesting(str(p))

print("Nesting and spacing fixed.")
