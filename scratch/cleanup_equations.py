import os
from pathlib import Path
import re

def cleanup_equations(text):
    # 1. Fix double-wrapped aligned blocks
    # Match \begin{aligned} \begin{aligned} content \end{aligned} \end{aligned}
    text = re.sub(
        r'\\begin\{aligned\}\s*\\begin\{aligned\}(.*?)\\end\{aligned\}\s*\\end\{aligned\}',
        r'\\begin{aligned}\1\\end{aligned}',
        text,
        flags=re.DOTALL
    )
    
    # 2. Fix double ampersands & &= or & &
    text = text.replace('& &=', '&=')
    text = text.replace('& &', '&=')
    
    # 3. Fix double newlines in aligned blocks
    text = re.sub(r'\\\\ \s*\\\\', r'\\\\', text)
    
    return text

def process_all_files():
    content_dir = Path('content')
    for p in content_dir.rglob('*.md'):
        text = p.read_text(encoding='utf-8')
        new_text = cleanup_equations(text)
        if text != new_text:
            p.write_text(new_text, encoding='utf-8')
            print(f"Cleaned up equations in {p}")

if __name__ == "__main__":
    process_all_files()
