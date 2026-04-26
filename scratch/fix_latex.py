import os
from pathlib import Path
import re

def fix_latex_and_currency():
    content_dir = Path('content')
    for p in content_dir.rglob('*.md'):
        text = p.read_text(encoding='utf-8')
        
        # 1. Fix the "Currency Math Trap": \$12.50$ -> \$12.50 (no trailing $)
        # And ensure literal dollar signs are escaped
        fixed_text = re.sub(r'\\\$([\d,.]+)\$', r'\\$\1', text)
        
        # 2. Fix the "Double Dollar Currency" trap: $\$20.00$ -> \$20.00
        fixed_text = fixed_text.replace('$\$', r'\$')

        # 3. Fix cases where variables and text are merged: top-up$x$of -> top-up $x$ of
        fixed_text = re.sub(r'(\w)\$(\w+)\$(\w)', r'\1 $\2$ \3', fixed_text)
        
        if text != fixed_text:
            p.write_text(fixed_text, encoding='utf-8')
            print(f"Fixed LaTeX/Currency in {p}")

if __name__ == "__main__":
    fix_latex_and_currency()
