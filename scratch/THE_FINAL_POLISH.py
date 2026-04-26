import os
import re
from pathlib import Path

def final_polish(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix Index Files (HTML boxes to Alerts)
    if file_path.endswith('index.md'):
        content = re.sub(r'<div style="background-color: #f0fff4;.*?>(.*?)</div>', r'> [!TIP]\n> **THE CORE PHILOSOPHY**\n>\n> \1', content, flags=re.DOTALL)
        content = re.sub(r'<div.*?>|</div>', '', content)

    # 2. Fix Section Order for chapters
    if not file_path.endswith('index.md'):
        # Ensure ## Let's Run the Numbers is followed by Examples
        # If Examples are ABOVE the header, move them
        examples_pattern = re.compile(r'(## Example \d+.*?\*\*\*)\n+(## Let\'s Run the Numbers)', re.DOTALL)
        content = examples_pattern.sub(r'\2\n\n\1', content)

    # 3. Specific Spacing for Setup/Calculation/Story
    # Ensure they are not mashed with the preceding text
    for marker in ['Setup', 'Calculation', 'Story']:
        pattern = rf'([^\n])\n\*\*?{marker}:?\*\*?'
        content = re.sub(pattern, rf'\1\n\n**{marker}:**', content, flags=re.IGNORECASE)

    # 4. Final Spacing pass
    content = re.sub(r'\n{3,}', r'\n\n', content)
    content = content.replace('***', '\n\n***\n\n')
    content = re.sub(r'\n\s*\*\*\*\s*\n\s*\*\*\*\s*\n', r'\n\n***\n\n', content)

    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content.strip() + '\n')

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    final_polish(str(p))

print("THE FINAL POLISH COMPLETE.")
