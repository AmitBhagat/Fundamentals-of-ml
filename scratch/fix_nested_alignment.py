import os
from pathlib import Path
import re

def fix_nested_alignment(text):
    # This script finds &= inside curly braces and replaces it with =
    # Example: \sum_{i &= 1} -> \sum_{i = 1}
    
    def replace_nested(match):
        content = match.group(0)
        return content.replace('&=', '=')
        
    # Match content inside curly braces that contains &=
    return re.sub(r'\{[^}]*&=[^}]*\}', replace_nested, text)

def process_all_files():
    content_dir = Path('content')
    for p in content_dir.rglob('*.md'):
        text = p.read_text(encoding='utf-8')
        new_text = fix_nested_alignment(text)
        if text != new_text:
            p.write_text(new_text, encoding='utf-8')
            print(f"Fixed nested alignment in {p}")

if __name__ == "__main__":
    process_all_files()
