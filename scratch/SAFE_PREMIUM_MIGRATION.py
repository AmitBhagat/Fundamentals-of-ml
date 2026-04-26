import os
import re
from pathlib import Path

def safe_migrate(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Convert HTML Boxes to Premium Alerts (Safe Replacement)
    # Note: #f0f7ff -> NOTE, #f0fff4 -> TIP, #fff5f5 -> CAUTION, #fffaf0 -> WARNING
    def repl_box(match):
        style = match.group(1).lower()
        inner = match.group(2).strip()
        
        alert = "NOTE"
        if "#f0f7ff" in style: alert = "NOTE"
        elif "#f0fff4" in style: alert = "TIP"
        elif "#fff5f5" in style: alert = "CAUTION"
        elif "#fffaf0" in style: alert = "WARNING"
        
        # Cleanup inner markers
        inner = re.sub(r'###\s*Prerequisite', '### Prerequisite', inner, flags=re.IGNORECASE)
        inner = re.sub(r'\*\*THE INTUITION\*\*', '**THE INTUITION**', inner, flags=re.IGNORECASE)
        inner = re.sub(r'\*\*Critical Insight:\*\*', '**CRITICAL INSIGHT**', inner, flags=re.IGNORECASE)
        inner = re.sub(r'\*\*Debugging Tip:\*\*', '**Debugging Tip**', inner, flags=re.IGNORECASE)
        
        lines = [f"> {l.strip()}" if l.strip() else ">" for l in inner.split('\n')]
        return f"\n\n> [!{alert}]\n" + "\n".join(lines) + "\n\n"

    # Match <div style="background-color: ..."> ... </div>
    content = re.sub(r'<div\s+style="background-color:\s*(#[a-fA-F0-9]+).*?>(.*?)</div>', repl_box, content, flags=re.DOTALL | re.IGNORECASE)

    # 2. Cleanup residual HTML and chapter artifacts
    content = re.sub(r'<(div|/div|h1|/h1).*?>', '', content, flags=re.IGNORECASE)
    content = content.replace('<div style="text-align: justify;">', '')
    content = re.sub(r'\nChapter \d+:.*?\n', '\n', content)

    # 3. Standardize Numerical Markers (Additive Spacing)
    markers = ['Setup', 'Calculation', 'Story']
    for m in markers:
        pattern = rf'^\s*\*{{0,2}}(?:The )?{m}:?\*{{0,2}}\s*$'
        content = re.sub(pattern, f'\n\n**{m}:**\n\n', content, flags=re.MULTILINE | re.IGNORECASE)

    # 4. Move Critical Insight above ML Applications (Surgical Swap)
    caution_pattern = re.compile(r'(> \[!CAUTION\].*?\n(?:>.*?\n)+)', re.DOTALL)
    caution_match = caution_pattern.search(content)
    if caution_match:
        caution_block = caution_match.group(1).strip()
        content = content.replace(caution_block, '')
        ml_apps_marker = "## ML Applications"
        if ml_apps_marker in content:
            content = content.replace(ml_apps_marker, f'***\n\n{caution_block}\n\n***\n\n{ml_apps_marker}')
        else:
            content += f'\n\n***\n\n{caution_block}\n'

    # 5. Clean Spacing
    content = re.sub(r'\n{3,}', r'\n\n', content)
    content = content.replace('***', '\n\n***\n\n')
    content = re.sub(r'\n\s*\*\*\*\s*\n\s*\*\*\*\s*\n', r'\n\n***\n\n', content)

    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content.strip() + '\n')

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    if p.name == 'index.md': continue
    try:
        safe_migrate(str(p))
    except Exception as e:
        print(f"Error migrating {p}: {e}")

print("SAFE PREMIUM MIGRATION COMPLETE.")
