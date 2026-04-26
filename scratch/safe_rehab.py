import os
import re
from pathlib import Path

def safe_rehabilitate(backup_path, target_path):
    with open(backup_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Strip H1 and outer div
    content = re.sub(r'<h1.*?>.*?</h1>', '', content, flags=re.DOTALL)
    content = content.replace('<div style="text-align: justify;">', '').replace('</div>', '')
    
    # 2. Convert HTML boxes to Alerts (Precise replacement)
    box_map = {
        '#f0f7ff': 'NOTE',   # Prerequisite
        '#f0fff4': 'TIP',    # Intuition
        '#fff5f5': 'CAUTION', # Critical Insight
        '#fffaf0': 'WARNING'  # Debugging Tip
    }
    
    for color, alert in box_map.items():
        pattern = rf'<div style="background-color: {color}.*?>(.*?)</div>'
        def repl(m):
            inner = m.group(1).strip()
            # Remove redundant internal markers like **THE INTUITION** or ### Prerequisite
            # so we can use the card header pattern the user liked.
            inner = re.sub(r'###\s*Prerequisite', '', inner, flags=re.IGNORECASE)
            inner = re.sub(r'\*\*THE INTUITION\*\*', '', inner, flags=re.IGNORECASE)
            
            clean_inner = "\n".join([f"> {line}" if line.strip() else ">" for line in inner.split('\n')])
            return f"> [!{alert}]\n>\n{clean_inner}"
        content = re.sub(pattern, repl, content, flags=re.DOTALL)

    # 3. Standardize Markers (Setup, Calculation, The Story)
    # Use bold markers with a MANDATORY blank line after
    markers = ['Setup', 'Calculation', 'The Story', 'The Calculation', 'The Setup']
    for m in markers:
        # Match marker on its own line (possibly with stars/colon)
        pattern = rf'^\s*\*{{0,2}}{m}:?\*{{0,2}}\s*$'
        content = re.sub(pattern, f'\n\n**{m}:**\n\n', content, flags=re.MULTILINE | re.IGNORECASE)

    # 4. Spacing for Equations
    # DO NOT use global replace('$$', ...). Instead, wrap existing equations if they aren't wrapped.
    # Pattern: \nEquation\n -> \n\nEquation\n\n
    content = re.sub(r'\n(\$\$.*?\$\$)\n', r'\n\n\1\n\n', content)
    
    # 5. Fix Titles
    title_match = re.search(r'Chapter \d+: (.*?)\n', content)
    title = title_match.group(1).strip() if title_match else Path(backup_path).stem.split('_', 1)[-1].replace('_', ' ').title()
    content = re.sub(r'^.*?Chapter \d+:.*?\n', '', content) # Remove title line from body
    
    # 6. Final Polish
    content = content.replace('***', '\n\n***\n\n')
    content = content.replace('---', '\n\n***\n\n')
    content = re.sub(r'\n{3,}', r'\n\n', content)

    # 7. Assemble
    final = f"---\ntitle: \"{title}\"\ndescription: \"Mastering {title} for ML.\"\ncomplexity: \"Intermediate\"\nestimated_time: \"20 min\"\nprerequisites: [\"Foundations\"]\n---\n\n# {title}\n\n***\n\n{content.strip()}\n"
    
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(final)

# Run mapping
subject_map = {
    'calculus': [23, 24, 25, 26, 27, 28, 29, 30, 31, 32],
    'linear-algebra': [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    'probability': [33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50],
    'statistics': [51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67],
    'information-theory': [68, 69, 70, 71, 72, 73, 74],
    'optimization': [75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85],
    'numerical-methods': [86, 87, 88, 89, 90, 91, 92],
    'discrete-math': [93, 94, 95, 96, 97, 98],
    'differential-equations': [99, 100, 101, 102, 103],
    'foundations': [1, 2, 3]
}

file_to_subject = {}
for sub, ids in subject_map.items():
    for i in ids: file_to_subject[i] = sub

backup_dir = Path('drafts-backup')
content_dir = Path('content')

for p in backup_dir.glob('*.md'):
    try:
        file_id = int(p.name.split('_')[0])
        if file_id in file_to_subject:
            subject = file_to_subject[file_id]
            target_name = p.name.split('_', 1)[1]
            safe_rehabilitate(p, content_dir / subject / target_name)
    except: continue

print("Safe rehabilitation complete.")
