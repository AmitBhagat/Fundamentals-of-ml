import os
from pathlib import Path
import re

def deindent_math(text):
    # This script finds any lines starting with optional whitespace followed by $$ or \begin/\end
    # and makes them flush left.
    lines = text.splitlines()
    new_lines = []
    
    in_math_block = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('$$'):
            new_lines.append(stripped)
            in_math_block = not in_math_block
        elif stripped.startswith('\\begin{aligned}') or stripped.startswith('\\end{aligned}'):
            new_lines.append(stripped)
        elif in_math_block:
            # Optionally keep some indentation inside aligned, but make it clean
            new_lines.append('  ' + stripped)
        else:
            new_lines.append(line)
            
    return '\n'.join(new_lines)

def process_all_files():
    content_dir = Path('content')
    for p in content_dir.rglob('*.md'):
        text = p.read_text(encoding='utf-8')
        new_text = deindent_math(text)
        if text != new_text:
            p.write_text(new_text, encoding='utf-8')
            print(f"De-indented math in {p}")

if __name__ == "__main__":
    process_all_files()
