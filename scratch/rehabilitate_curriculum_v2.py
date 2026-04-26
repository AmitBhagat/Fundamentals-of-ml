import os
import re
from pathlib import Path

def rehabilitate_file_v2(backup_path, target_path):
    with open(backup_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Extract title
    title_match = re.search(r'<h1 align="center"> Chapter \d+: (.*?) </h1>', content)
    title = title_match.group(1).strip() if title_match else Path(backup_path).stem.split('_', 1)[-1].replace('_', ' ').title()
    
    # 2. Cleanup HTML
    content = re.sub(r'<h1.*?>.*?</h1>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div style="text-align: justify;">', '', content)
    
    # 3. Convert HTML blocks to Alert blocks
    # Note/Prerequisite
    def convert_block(match):
        type_str = match.group(1) # color/style info
        inner = match.group(2).strip()
        
        # Determine alert type based on color
        alert_type = "NOTE"
        if "#f0fff4" in type_str: alert_type = "TIP"
        elif "#fff5f5" in type_str: alert_type = "CAUTION"
        elif "#fffaf0" in type_str: alert_type = "WARNING"
        
        # Add > to every line of inner
        clean_inner = "\n".join([f"> {line}" if line.strip() else ">" for line in inner.split('\n')])
        return f"> [!{alert_type}]\n>\n{clean_inner}"

    content = re.sub(r'<div style="background-color: (.*?);.*?>(.*?)</div>', convert_block, content, flags=re.DOTALL)
    
    # Remove any stray </div>
    content = content.replace('</div>', '')
    
    # 4. Fix markers (Setup, Calculation, The Story)
    markers = ['Setup', 'Calculation', 'The Story']
    for m in markers:
        # Standardize to **Marker:** on its own line with padding
        content = re.sub(rf'^\s*\*{{0,2}}{m}:?\*{{0,2}}\s*$', f'\n\n**{m}:**\n\n', content, flags=re.MULTILINE | re.IGNORECASE)

    # 5. Spacing for Examples
    content = re.sub(r'### (Example \d+.*)', r'\n\n***\n\n## \1\n\n***\n\n', content)
    
    # 6. General spacing
    content = re.sub(r'\n{3,}', r'\n\n', content)
    content = content.replace('***', '\n\n***\n\n')
    content = re.sub(r'\n\s*\*\*\*\s*\n\s*\*\*\*\s*\n', r'\n\n***\n\n', content)

    # 7. Frontmatter
    final_content = f"---\ntitle: \"{title}\"\ndescription: \"Mastering {title} for Machine Learning.\"\ncomplexity: \"Intermediate\"\nestimated_time: \"20 min\"\nprerequisites: [\"Foundations\"]\n---\n\n# {title}\n\n***\n\n{content.strip()}\n"
    
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(final_content)

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
            rehabilitate_file_v2(p, content_dir / subject / target_name)
    except: continue

print("Rehabilitation v2 complete.")
