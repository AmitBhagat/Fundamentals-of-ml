import os
import re
from pathlib import Path

def fix_content_v8(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Enforce Display Math Spacing (Critical for parsing)
    # Put every $$ on its own line
    content = content.replace('$$', '\n\n$$\n\n')
    
    # 2. Fix currency artifacts
    # \$25 -> $25
    content = content.replace('\\$25', '$25')
    content = content.replace(' $\$ ', ' $ ')
    
    # 3. Fix Setup/Calculation/The Story spacing
    # Ensure blank line AFTER
    markers = [r'\*\*Setup:\*\*', r'\*\*Calculation:\*\*', r'\*\*The Story:\*\*']
    for m in markers:
        content = re.sub(rf'({m})\n(?!\n)', r'\1\n\n', content)

    # 4. Cleanup excessive newlines
    content = re.sub(r'\n{3,}', r'\n\n', content)
    
    # 5. Fix titles that were turned into blockquotes or messed up
    # (Checking for # # or other artifacts)
    content = re.sub(r'^#\s*#\s*', '# ', content, flags=re.MULTILINE)

    # 6. Final Polish
    # Ensure there is a blank line before blockquotes
    content = content.replace('\n> [!', '\n\n> [!')

    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content.strip() + '\n')

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    if p.name == 'index.md': continue
    fix_content_v8(str(p))

print("Content fix v8 complete.")
