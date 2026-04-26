import os
import re
from pathlib import Path

def fix_velite(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Force fix frontmatter
    # Find the FIRST --- and the SECOND ---
    matches = list(re.finditer(r'^---\s*$', content, re.MULTILINE))
    if len(matches) >= 2:
        start_fm = matches[0].start()
        end_fm = matches[1].end()
        
        fm_content = content[matches[0].end() : matches[1].start()].strip()
        body_content = content[matches[1].end() :].strip()
        
        # Clean HTML out of frontmatter
        clean_fm_lines = []
        html_remnants = []
        for line in fm_content.split('\n'):
            if '<div' in line or '</div' in line or 'style=' in line:
                html_remnants.append(line)
            elif ':' in line:
                # Quote values if they have special chars
                key, val = line.split(':', 1)
                val = val.strip()
                if (val.startswith('[') and val.endswith(']')):
                    # Array, leave as is but check internal quotes
                    pass
                elif not (val.startswith('"') and val.endswith('"')):
                    val = f'"{val.replace('"', '\\"')}"'
                clean_fm_lines.append(f"{key}: {val}")
            else:
                # Just text, maybe a list item?
                if line.strip().startswith('- '):
                    html_remnants.append(line) # Move to body
        
        new_fm = '\n'.join(clean_fm_lines)
        new_body = '\n'.join(html_remnants) + '\n\n' + body_content
        
        content = f"---\n{new_fm}\n---\n\n{new_body}"

    # 2. Fix the \frac vs /frac issue if it exists
    content = content.replace('$/frac', '$\\frac')
    content = content.replace('/partial', '\\partial')
    content = content.replace('/nabla', '\\nabla')
    
    # 3. Final cleanup of double frontmatter if any
    content = re.sub(r'---\n---\n', '---\n', content)
    
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    if p.name == 'index.md': continue
    try:
        fix_velite(str(p))
    except Exception as e:
        print(f"Error fixing {p}: {e}")

print("Velite fix complete.")
