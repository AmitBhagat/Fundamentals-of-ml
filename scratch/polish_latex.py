import os
import re

def polish_latex(text):
    math_pattern = re.compile(r'(\$\$.*?\$\$|\$.*?\$)', re.DOTALL)

    def replace_math_content(match):
        math = match.group(0)
        is_block = math.startswith('$$')
        
        if is_block:
            content = math[2:-2]
        else:
            content = math[1:-1]

        # Fix accidental tab character from previous run (^\top where \t is a tab)
        content = content.replace('^\t' + 'op', r'^\top')
        
        # 1. Transpose: ^T -> ^\top
        content = re.sub(r'\^T\b', r'^\top', content)

        # 2. Ellipses: ... -> \dots
        content = content.replace('...', r'\dots')

        # 3. Scalar multiplication: * -> \cdot
        content = re.sub(r'(\w)\s*\*\s*(\w)', r'\1 \\cdot \2', content)

        # 4. Normalize spacing for inline math
        if not is_block:
            content = content.strip()

        if is_block:
            return f"$${content}$$"
        else:
            return f"${content}$"

    return math_pattern.sub(replace_math_content, text)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                polished = polish_latex(content)
                
                if polished != content:
                    print(f"Polishing LaTeX in {file_path}...")
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(polished)

if __name__ == "__main__":
    process_directory('e:/Projects/Mathematics/content')
