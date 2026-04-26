import os
import re
from pathlib import Path

def final_swap(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Identify Sections
    # We want to move the [!CAUTION] block above ## ML Applications
    
    caution_pattern = re.compile(r'(> \[!CAUTION\].*?\n(?:>.*?\n)+)', re.DOTALL)
    caution_match = caution_pattern.search(content)
    
    if caution_match:
        caution_block = caution_match.group(1).strip()
        # Remove it from its current position
        content = content.replace(caution_block, '')
        
        # b. Find the ML Applications header
        ml_apps_marker = "## ML Applications"
        if ml_apps_marker.lower() in content.lower():
            # Find the actual case version to replace
            actual_marker = re.search(r'## ML Applications', content, re.IGNORECASE).group(0)
            content = content.replace(actual_marker, f'***\n\n{caution_block}\n\n***\n\n{actual_marker}')
        else:
            # If no ML Apps, just put it at the end
            content += f'\n\n***\n\n{caution_block}\n'

    # 2. Fix the Setup/Calculation/Story markers
    markers = ['Setup', 'Calculation', 'Story']
    for m in markers:
        # Match marker (case insensitive, with or without stars/colon)
        pattern = rf'^\s*\*{{0,2}}(?:The )?{m}:?\*{{0,2}}\s*$'
        content = re.sub(pattern, f'\n\n**{m}:**\n\n', content, flags=re.MULTILINE | re.IGNORECASE)

    # 3. Spacing reinforcement for math
    content = content.replace('$$', '\n\n$$\n\n')
    content = content.replace('\\begin{aligned}', '\n\\begin{aligned}\n')
    content = content.replace('\\end{aligned}', '\n\\end{aligned}\n')

    # 4. Final Spacing pass
    content = re.sub(r'\n{3,}', r'\n\n', content)
    content = content.replace('***', '\n\n***\n\n')
    content = re.sub(r'\n\s*\*\*\*\s*\n\s*\*\*\*\s*\n', r'\n\n***\n\n', content)

    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content.strip() + '\n')

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    if p.name == 'index.md': continue
    try:
        final_swap(str(p))
    except Exception as e:
        print(f"Error in {p}: {e}")

print("THE FINAL SWAP COMPLETE.")
