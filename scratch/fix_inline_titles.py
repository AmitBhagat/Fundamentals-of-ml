import os
import re
from pathlib import Path

def fix_inline_titles(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Find blockquote blocks
    # Pattern: > [!TYPE] followed by lines starting with >
    
    # We want to find lines like:
    # > **THE INTUITION**
    # > Some text
    # And turn them into:
    # > **THE INTUITION**
    # >
    # > Some text
    
    # Also handle "Critical Insight" and "Debugging Tip"
    
    markers = [
        'THE INTUITION',
        'CRITICAL INSIGHT',
        'Debugging Tip',
        'Practical Tip',
        'Deep Dive',
        'Gotcha'
    ]
    
    for m in markers:
        # Match > **MARKER** followed by any text on same/next line without blank line
        # Use regex to find and replace
        pattern = rf'(>\s*\*\*{m}\*\*:?)(?!\s*\n>\s*\n)(?:\s*)(.*)'
        # Replacing with a blank line between header and content
        content = re.sub(pattern, r'\1\n>\n> \2', content, flags=re.IGNORECASE)

    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    if p.name == 'index.md': continue
    fix_inline_titles(str(p))

print("Inline titles corrected.")
