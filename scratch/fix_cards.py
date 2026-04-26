import os
import re
from pathlib import Path

def fix_cards(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Standardize frontmatter: only keep the first one
    parts = re.split(r'^---\s*$', content, flags=re.MULTILINE)
    if len(parts) >= 3:
        fm = parts[1].strip()
        # Combine everything else as body
        body = '---'.join(parts[2:]).strip()
    else:
        # No frontmatter? (Shouldn't happen now)
        fm = ""
        body = content.strip()

    # 2. Clean body from extra --- separators (replace with ***)
    body = re.sub(r'^---\s*$', '***', body, flags=re.MULTILINE)

    # 3. Clean blockquotes from quote artifacts
    # Remove lines like > " or > ' or > - " ... "
    body = re.sub(r'>\s*["\']\s*\n', '', body)
    
    # 4. Remove any " that were injected into prerequisites
    # Matches: > - **Title:** " Value "
    body = re.sub(r'(> - \*\*.*?\*\*:) " (.*?) "', r'\1 \2', body)
    
    # 5. Fix the Prerequisite header inside blocks
    # Ensure it's ### instead of ## if it's inside a block
    body = re.sub(r'> ## Prerequisite', r'> ### Prerequisite', body)

    # 6. Final Assemble
    title_match = re.search(r'title: "(.*?)"', fm)
    title = title_match.group(1) if title_match else Path(file_path).stem.replace('_', ' ').title()
    
    final_content = f"---\ntitle: \"{title}\"\ndescription: \"Mastering {title} for ML.\"\ncomplexity: \"Intermediate\"\nestimated_time: \"20 min\"\nprerequisites: [\"Foundations\"]\n---\n\n# {title}\n\n***\n\n{body.strip()}\n"
    
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(final_content)

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    if p.name == 'index.md': continue
    fix_cards(str(p))

print("Cards correction complete.")
