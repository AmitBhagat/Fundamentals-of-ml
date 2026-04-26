import os
import re
from pathlib import Path

def remove_html_and_standardize(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Force conversion of HTML boxes to Alerts
    def repl_html(match):
        style = match.group(1)
        inner = match.group(2).strip()
        
        # Map style to type
        alert = "NOTE"
        if "#f0f7ff" in style: alert = "NOTE"
        elif "#f0fff4" in style: alert = "TIP"
        elif "#fff5f5" in style: alert = "CAUTION"
        elif "#fffaf0" in style: alert = "WARNING"
        
        # Clean inner: remove redundant headers
        inner = re.sub(r'###\s*Prerequisite', '', inner, flags=re.IGNORECASE)
        inner = re.sub(r'\*\*THE INTUITION\*\*', '', inner, flags=re.IGNORECASE)
        inner = re.sub(r'\*\*Critical Insight:\*\*', '', inner, flags=re.IGNORECASE)
        inner = re.sub(r'\*\*Debugging Tip:\*\*', '', inner, flags=re.IGNORECASE)
        
        # Prefix every line with >
        lines = inner.split('\n')
        clean_lines = [f"> {l.strip()}" if l.strip() else ">" for l in lines]
        
        # Add the header back inside the block
        header_map = {
            "NOTE": "**Prerequisite**",
            "TIP": "**THE INTUITION**",
            "CAUTION": "**CRITICAL INSIGHT**",
            "WARNING": "**Debugging Tip**"
        }
        header = header_map.get(alert, "**Note**")
        
        return f"> [!{alert}]\n> {header}\n>\n" + "\n".join(clean_lines)

    content = re.sub(r'<div style="background-color:\s*(.*?);.*?>(.*?)</div>', repl_html, content, flags=re.DOTALL)
    
    # Remove any stray divs
    content = re.sub(r'<div.*?>', '', content)
    content = content.replace('</div>', '')

    # 2. Fix spacing for markers again
    markers = ['Setup', 'Calculation', 'Story']
    for m in markers:
        content = re.sub(rf'^\s*\*{{0,2}}{m}:?\*{{0,2}}\s*$', f'\n\n**{m}:**\n\n', content, flags=re.MULTILINE | re.IGNORECASE)

    # 3. Final Spacing
    content = re.sub(r'\n{3,}', r'\n\n', content)

    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content.strip() + '\n')

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    if p.name == 'index.md': continue
    remove_html_and_standardize(str(p))

print("HTML removed and structure standardized.")
