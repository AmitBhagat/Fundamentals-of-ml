import os
from pathlib import Path
import re

def convert_to_aligned(text):
    def replace_chained(match):
        content = match.group(1).strip()
        
        # Count separators
        count_implies = content.count(r'\implies')
        count_eq = content.count('=')
        
        # Only convert if it's long (2 or more separators)
        if count_implies + count_eq < 2:
            return match.group(0)
            
        # Strategy: Split by \implies first, then by = if needed
        # We want to align at the first '=' of each step, or at the \implies
        
        # Split by \implies
        steps = re.split(r'\s*\\implies\s*', content)
        
        aligned_steps = []
        for i, step in enumerate(steps):
            prefix = r'\implies ' if i > 0 else ''
            # Find the first '=' in this step for alignment
            if '=' in step:
                parts = step.split('=', 1)
                aligned_steps.append(f"{prefix}{parts[0].strip()} &= {parts[1].strip()}")
            else:
                aligned_steps.append(f"{prefix}{step.strip()}")
                
        new_content = "\n  " + " \\\\\n  ".join(aligned_steps) + "\n"
        return f"$$\n\\begin{{aligned}}{new_content}\\end{{aligned}}\n$$"

    # Match $$ content $$ (single line or block)
    return re.sub(r'\$\$(.*?)\$\$', replace_chained, text, flags=re.DOTALL)

def process_all_files():
    content_dir = Path('content')
    for p in content_dir.rglob('*.md'):
        text = p.read_text(encoding='utf-8')
        new_text = convert_to_aligned(text)
        if text != new_text:
            p.write_text(new_text, encoding='utf-8')
            print(f"Refactored equations in {p}")

if __name__ == "__main__":
    process_all_files()
