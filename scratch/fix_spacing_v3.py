import os
import re

content_dir = 'content'

def fix_header_spacing(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        stripped = line.lstrip()
        # If the line contains **The Calculation:** or **The Story:** or **The Setup:**
        if '**The Calculation:**' in stripped or '**The Story:**' in stripped or '**The Setup:**' in stripped:
            # Extract the header and the remaining text if any
            match = re.match(r'^\s*(\*\*(The Calculation|The Story|The Setup):\*\*)(.*)', line)
            if match:
                header = match.group(1)
                remaining = match.group(3).strip()
                
                # Add a blank line before the header if the previous line wasn't blank
                if new_lines and new_lines[-1].strip():
                    new_lines.append('\n')
                
                new_lines.append(header + '\n')
                
                if remaining:
                    new_lines.append('\n')
                    new_lines.append(remaining + '\n')
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    # Second pass: ensure blank line after headers if not already there
    final_lines = []
    for i in range(len(new_lines)):
        line = new_lines[i]
        final_lines.append(line)
        if line.strip() in ['**The Calculation:**', '**The Story:**', '**The Setup:**']:
            if i + 1 < len(new_lines) and new_lines[i+1].strip():
                final_lines.append('\n')

    # Clean up multiple blank lines
    content = "".join(final_lines)
    content = re.sub(r'\n{3,}', r'\n\n', content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

for root, dirs, files in os.walk(content_dir):
    for file in files:
        if file.endswith('.md'):
            fix_header_spacing(os.path.join(root, file))
