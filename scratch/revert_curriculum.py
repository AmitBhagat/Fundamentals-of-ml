import os
import re

def revert_content(content):
    # 1. Revert [!TYPE] blockquotes back to <div> blocks (roughly)
    # This is hard because we lost the original colors, but we can use classes or themed divs
    
    type_to_style = {
        'NOTE': 'background-color: #f0f7ff; padding: 20px; border-radius: 12px; color: #1f2328; margin-bottom: 24px; border: 1px solid rgba(0,0,0,0.05);',
        'TIP': 'background-color: #f0fff4; padding: 20px; border-radius: 12px; color: #1f2328; margin-bottom: 24px; border: 1px solid rgba(0,0,0,0.05);',
        'CAUTION': 'background-color: #fff5f5; padding: 20px; border-radius: 12px; color: #1f2328; margin-bottom: 24px; border: 1px solid rgba(0,0,0,0.05);',
        'WARNING': 'background-color: #fffaf0; padding: 20px; border-radius: 12px; color: #1f2328; margin-bottom: 24px; border: 1px solid rgba(0,0,0,0.05);',
        'IMPORTANT': 'background-color: #f5f3ff; padding: 20px; border-radius: 12px; color: #1f2328; margin-bottom: 24px; border: 1px solid rgba(0,0,0,0.05);',
    }

    def blockquote_to_div(match):
        type_name = match.group(1).upper()
        inner = match.group(2).strip()
        
        # Remove > prefixes
        lines = inner.split('\n')
        clean_lines = []
        for line in lines:
            clean_lines.append(re.sub(r'^>\s?', '', line))
        inner_content = '\n'.join(clean_lines).strip()
        
        # Special case for Calculation: if it was wrapped, unwrap it but keep math display
        if '### Calculation' in inner_content:
            inner_content = inner_content.replace('### Calculation\n', '**Calculation:**\n')
            if type_name == 'NOTE':
                return inner_content # Unwrap Calculation
        
        style = type_to_style.get(type_name, type_to_style['NOTE'])
        return f'<div style="{style}">\n\n{inner_content}\n\n</div>'

    # Revert blockquotes
    content = re.sub(r'> \[!(NOTE|TIP|WARNING|IMPORTANT|CAUTION)\]\n((?:>.*\n?)+)', blockquote_to_div, content, flags=re.MULTILINE)

    return content

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = re.split(r'^---\s*\n', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3: return
    
    new_body = revert_content(parts[2])
    new_content = f"---\n{parts[1]}---\n\n{new_body.strip()}\n"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

for root, dirs, files in os.walk('content'):
    for file in files:
        if file.endswith('.md') and file != 'index.md':
            process_file(os.path.join(root, file))
