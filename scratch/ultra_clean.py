import os
import re
from pathlib import Path

def ultra_clean(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Regex to find the colored boxes and turn them into Alerts
    # This regex is very lenient with whitespace and attributes
    pattern = re.compile(r'<div\s+style="background-color:\s*(#[a-fA-F0-9]+).*?>(.*?)</div>', re.DOTALL | re.IGNORECASE)
    
    def replacer(match):
        color = match.group(1).lower()
        inner = match.group(2).strip()
        
        # Mapping
        alert = "NOTE"
        if "#f0f7ff" in color: alert = "NOTE"
        elif "#f0fff4" in color: alert = "TIP"
        elif "#fff5f5" in color: alert = "CAUTION"
        elif "#fffaf0" in color: alert = "WARNING"
        
        # Cleanup inner
        inner = re.sub(r'###\s*Prerequisite', '', inner, flags=re.IGNORECASE)
        inner = re.sub(r'\*\*THE INTUITION\*\*', '', inner, flags=re.IGNORECASE)
        inner = re.sub(r'\*\*Critical Insight:\*\*', '', inner, flags=re.IGNORECASE)
        inner = re.sub(r'\*\*Debugging Tip:\*\*', '', inner, flags=re.IGNORECASE)
        
        lines = [f"> {l.strip()}" if l.strip() else ">" for l in inner.split('\n')]
        
        header_map = {
            "NOTE": "**Prerequisite**",
            "TIP": "**THE INTUITION**",
            "CAUTION": "**CRITICAL INSIGHT**",
            "WARNING": "**Debugging Tip**"
        }
        header = header_map.get(alert, "**Note**")
        
        return f"\n\n> [!{alert}]\n> {header}\n>\n" + "\n".join(lines) + "\n\n"

    content = pattern.sub(replacer, content)
    
    # 2. Cleanup any residual HTML
    content = re.sub(r'<(div|/div|h1|/h1).*?>', '', content, flags=re.IGNORECASE)
    
    # 3. Fix structural markers
    markers = ['Setup', 'Calculation', 'Story']
    for m in markers:
        content = re.sub(rf'^\s*\*{{0,2}}{m}:?\*{{0,2}}\s*$', f'\n\n**{m}:**\n\n', content, flags=re.MULTILINE | re.IGNORECASE)

    # 4. Final spacing
    content = re.sub(r'\n{3,}', r'\n\n', content)

    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content.strip() + '\n')

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    if p.name == 'index.md': continue
    ultra_clean(str(p))

print("Ultra clean complete.")
