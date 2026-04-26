import os
import re
from pathlib import Path

def repair_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix Math Spacing (Most critical for rendering)
    # Ensure $$ are isolated
    content = re.sub(r'([^\s\n])\$\$', r'\1\n\n$$', content)
    content = re.sub(r'\$\$([^\s\n])', r'$$\n\n\1', content)
    content = content.replace('$$', '\n\n$$\n\n')
    
    # Ensure \begin{aligned} are isolated
    content = content.replace('\\begin{aligned}', '\n\\begin{aligned}\n')
    content = content.replace('\\end{aligned}', '\n\\end{aligned}\n')

    # 2. Fix the missing "Let's Run the Numbers" section
    # If we see "Example 1" but no "Run the Numbers", insert it
    if 'Example 1' in content and "Run the Numbers" not in content:
        content = re.sub(r'## Example 1', r'## Let\'s Run the Numbers\n\n***\n\n## Example 1', content)

    # 3. Fix missing "ML Applications" section
    if 'ML Applications' not in content:
        # Try to find the list after the last "Story"
        parts = content.split('**Story:**')
        if len(parts) > 1:
            last_part = parts[-1]
            if '\n1.' in last_part or '\n- ' in last_part:
                parts[-1] = re.sub(r'\n(1\.|\- )', r'\n\n***\n\n## ML Applications\n\n\1', last_part, count=1)
                content = '**Story:**'.join(parts)

    # 4. Remove the "Chapter XX: Title" artifacts from body
    content = re.sub(r'\nChapter \d+:.*?\n', '\n', content)
    
    # 5. Fix Blockquote/Alert Headers
    # Ensure they have double spacing and correct bolding
    content = content.replace('> [!NOTE]\n> **Prerequisite**', '> [!NOTE]\n> ### Prerequisite')
    content = content.replace('> [!TIP]\n> **THE INTUITION**', '> [!TIP]\n> **THE INTUITION**')
    
    # 6. Final Spacing pass
    content = re.sub(r'\n{3,}', r'\n\n', content)
    content = content.replace('***', '\n\n***\n\n')
    content = re.sub(r'\n\s*\*\*\*\s*\n\s*\*\*\*\s*\n', r'\n\n***\n\n', content)

    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content.strip() + '\n')

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    if p.name == 'index.md': continue
    repair_file(str(p))

print("REPAIR STATION COMPLETE.")
