import os
import re
from pathlib import Path

def fix_truncated_titles(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find titles that end with (something, or (something vs
    # and add the closing quote/bracket if missing
    
    # Pattern: title: "Text (Text," -> title: "Text (Text)"
    content = re.sub(r'title: "(.*?) \((.*?),"', r'title: "\1 (\2)"', content)
    # Pattern: title: "Text (Text vs" -> title: "Text (Text vs. ...)"
    content = re.sub(r'title: "(.*?) \((.*?)\s+vs"', r'title: "\1 (\2 vs. ...)"', content)
    
    # Fix the missing ) in "Continuous Probability Distributions (Normal, Exponential,"
    content = content.replace('"Continuous Probability Distributions (Normal, Exponential,"', '"Continuous Probability Distributions (Normal, Exponential)"')
    content = content.replace('"Discrete Probability Distributions (Bernoulli, Bernoulli,"', '"Discrete Probability Distributions (Bernoulli, Binomial)"')
    content = content.replace('"Types of Hypothesis (H0 vs"', '"Types of Hypothesis (H0 vs. H1)"')

    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

content_dir = Path('content')
for p in content_dir.rglob('*.md'):
    fix_truncated_titles(str(p))

print("Truncated titles fixed.")
