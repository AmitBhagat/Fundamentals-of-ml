import os
import re
from pathlib import Path

def polish_v9(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Aligned math for multi-step derivations
    # If we see multiple display math blocks or long derivations, wrap them
    def align_repl(match):
        inner = match.group(0).strip()
        # If it's already aligned, skip
        if '\\begin{aligned}' in inner: return inner
        # Split into display blocks
        blocks = re.findall(r'\$\$(.*?)\$\$', inner, flags=re.DOTALL)
        if len(blocks) > 1:
            clean = " \\\\\n  ".join([b.strip().replace('=', '&=', 1) if '=' in b and '&=' not in b else b.strip() for b in blocks])
            return f"$$\n\\begin{{aligned}}\n  {clean}\n\\end{{aligned}}\n$$"
        return inner

    # Detect sequences of display math
    content = re.sub(r'(\$\$.*?\$\$\s*){2,}', align_repl, content, flags=re.DOTALL)

    # 2. Add THE INTUITION and other headers BACK to the cards but in a clean way
    # If a block starts with [!TIP], and doesn't have a bold header, add it
    content = content.replace('> [!TIP]\n>\n', '> [!TIP]\n> **THE INTUITION**\n>\n')
    content = content.replace('> [!CAUTION]\n>\n', '> [!CAUTION]\n> **CRITICAL INSIGHT**\n>\n')
    content = content.replace('> [!WARNING]\n>\n', '> [!WARNING]\n> **Debugging Tip**\n>\n')
    content = content.replace('> [!NOTE]\n>\n', '> [!NOTE]\n> **Prerequisite**\n>\n')

    # 3. Final Spacing
    content = re.sub(r'\n{3,}', r'\n\n', content)
    
    # 4. Remove leading # for examples (keep them as ##)
    content = re.sub(r'^#\s*Example', '## Example', content, flags=re.MULTILINE)

    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content.strip() + '\n')

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    if p.name == 'index.md': continue
    polish_v9(str(p))

print("Final polish v9 complete.")
