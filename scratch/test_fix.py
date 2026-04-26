import os
import re

def fix_spacing(content):
    # 1. Standardize line endings
    content = content.replace('\r\n', '\n')
    
    # 2. Add extra padding around key phrases
    content = content.replace('**The Story:**', '\n\n**The Story:**\n\n')
    content = content.replace('**The Setup:**', '\n\n**The Setup:**\n\n')
    content = content.replace('**Calculation:**', '\n\n**Calculation:**\n\n')
    content = content.replace('**The Calculation:**', '\n\n**The Calculation:**\n\n')
    
    # 3. Add padding around math
    content = content.replace('$$', '\n\n$$\n\n')
    
    # 4. Clean up the resulting newline explosion
    content = re.sub(r'\n{3,}', r'\n\n', content)
    
    return content.strip()

# Run on basis_and_dimension.md only to test
file_path = 'content/linear-algebra/basis_and_dimension.md'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()
parts = re.split(r'^---\s*\n', content, maxsplit=2, flags=re.MULTILINE)
new_body = fix_spacing(parts[2])
new_content = f"---\n{parts[1]}---\n\n{new_body}\n"
with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(new_content)
print("Fixed one file.")
