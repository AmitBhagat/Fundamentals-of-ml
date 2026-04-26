import os
import re
from pathlib import Path

def aligned_refurbish(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Detect multiple $$ blocks in a row and merge them into \begin{aligned}
    # Pattern: $$ (anything) $$ \s* $$ (anything) $$
    def merge_aligned(match):
        # Extract all content between $$...$$
        blocks = re.findall(r'\$\$(.*?)\$\$', match.group(0), flags=re.DOTALL)
        clean_blocks = []
        for b in blocks:
            b = b.strip()
            if b:
                # If block contains = but not &=, and it's multiple lines or has multiple =, try to align
                # For now, just stack them with \\
                clean_blocks.append(b.replace('=', '&=', 1) if '=' in b and '&=' not in b else b)
        
        inner = " \\\\\n  ".join(clean_blocks)
        return f"$$\n\\begin{{aligned}}\n  {inner}\n\\end{{aligned}}\n$$"

    # Match 2 or more consecutive display math blocks
    content = re.sub(r'(\$\$.*?\$\$\s*){2,}', merge_aligned, content, flags=re.DOTALL)

    # 2. Fix the # # example titles
    content = re.sub(r'^#\s*#\s*(\d+)\.', r'## Example \1:', content, flags=re.MULTILINE)
    
    # 3. Fix the list-based calculations (like in Backpropagation)
    # If a line starts with a number or bullet and has math, and the next line does too...
    # This is harder to automate perfectly, so I'll do a targeted replacement for common ones.
    
    # 4. Spacing reinforcement
    content = content.replace('**The Setup:**', '\n**Setup:**\n')
    content = content.replace('**The Calculation:**', '\n**Calculation:**\n')
    content = content.replace('**The Story:**', '\n**Story:**\n')

    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    if p.name == 'index.md': continue
    aligned_refurbish(str(p))

print("Aligned refurbishment complete.")
