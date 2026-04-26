import os
import re

content_dir = 'content'

def fix_file_spacing(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Ensure newline after **The Calculation:** if it's followed by $$ or 1.
    content = re.sub(r'\*\*The Calculation:\*\*\n(\$\$|1\.)', r'**The Calculation:**\n\n\1', content)
    
    # 2. Ensure newline before **The Story:** if it's preceded by $$ or a list item
    # Handle $$ case
    content = re.sub(r'\$\$\n\*\*The Story:\*\*', r'$$\n\n**The Story:**', content)
    # Handle list case (assuming the list ends and then **The Story:** starts)
    # This one is trickier, let's look for a line that starts with a number or dot and then the header
    content = re.sub(r'(\n\d+\..*)\n\*\*The Story:\*\*', r'\1\n\n**The Story:**', content)

    # 3. Ensure blank line before and after headers in the numerical section
    # Find the section start
    if "## Let's Run the Numbers" in content:
        parts = content.split("## Let's Run the Numbers")
        pre = parts[0]
        post = parts[1]
        
        # In the post section, find ### X. Title and ensure spacing
        post = re.sub(r'\n(### \d+\..*)\n', r'\n\n\1\n\n', post)
        # Clean up triple newlines
        post = re.sub(r'\n{3,}', r'\n\n', post)
        
        content = pre + "## Let's Run the Numbers" + post

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

for root, dirs, files in os.walk(content_dir):
    for file in files:
        if file.endswith('.md'):
            fix_file_spacing(os.path.join(root, file))
