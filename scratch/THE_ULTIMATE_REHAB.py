import os
import re
from pathlib import Path

def ultimate_rehab(backup_path, target_path):
    with open(backup_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Title Extraction
    title_match = re.search(r'Chapter \d+: (.*?)\n', content)
    title = title_match.group(1).strip() if title_match else Path(backup_path).stem.split('_', 1)[-1].replace('_', ' ').title()
    content = re.sub(r'^.*?Chapter \d+:.*?\n', '', content)

    # 2. Convert HTML boxes to Modern Alerts
    def repl_box(match):
        style = match.group(1).lower()
        inner = match.group(2).strip()
        
        alert = "NOTE"
        if "#f0f7ff" in style: alert = "NOTE"
        elif "#f0fff4" in style: alert = "TIP"
        elif "#fff5f5" in style: alert = "CAUTION"
        elif "#fffaf0" in style: alert = "WARNING"
        
        # Cleanup inner
        inner = re.sub(r'###\s*Prerequisite', '', inner, flags=re.IGNORECASE)
        inner = re.sub(r'\*\*THE INTUITION\*\*', '', inner, flags=re.IGNORECASE)
        inner = re.sub(r'\*\*Critical Insight:\*\*', '', inner, flags=re.IGNORECASE)
        inner = re.sub(r'\*\*Debugging Tip:\*\*', '', inner, flags=re.IGNORECASE)
        
        lines = [f"> {l.strip()}" if l.strip() else ">" for l in inner.split('\n')]
        
        header_map = {
            "NOTE": "**Prerequisite**",
            "TIP": "**THE INTUITION**",
            "CAUTION": "**CRITICAL INSIGHT**",
            "WARNING": "**Debugging Tip**"
        }
        header = header_map.get(alert, "**Note**")
        return f"\n\n> [!{alert}]\n> {header}\n>\n" + "\n".join(lines) + "\n\n"

    # Match <div style="background-color: ..."> ... </div>
    content = re.sub(r'<div\s+style="background-color:\s*(#[a-fA-F0-9]+).*?>(.*?)</div>', repl_box, content, flags=re.DOTALL | re.IGNORECASE)

    # 3. Cleanup residual HTML
    content = re.sub(r'<(div|/div|h1|/h1).*?>', '', content, flags=re.IGNORECASE)
    content = content.replace('<div style="text-align: justify;">', '')

    # 4. Standardize Markers
    markers = ['Setup', 'Calculation', 'The Story', 'The Calculation', 'The Setup']
    for m in markers:
        pattern = rf'^\s*\*{{0,2}}{m}:?\*{{0,2}}\s*$'
        content = re.sub(pattern, f'\n\n**{m}:**\n\n', content, flags=re.MULTILINE | re.IGNORECASE)

    # 5. Spacing for Equations
    content = re.sub(r'\n(\$\$.*?\$\$)\n', r'\n\n\1\n\n', content)
    
    # 6. Aligned conversion for multi-step derivations
    def align_repl(match):
        blocks = re.findall(r'\$\$(.*?)\$\$', match.group(0), flags=re.DOTALL)
        if len(blocks) > 1:
            clean = " \\\\\n  ".join([b.strip().replace('=', '&=', 1) if '=' in b and '&=' not in b else b.strip() for b in blocks])
            return f"$$\n\\begin{{aligned}}\n  {clean}\n\\end{{aligned}}\n$$"
        return match.group(0)
    content = re.sub(r'(\$\$.*?\$\$\s*){2,}', align_repl, content, flags=re.DOTALL)

    # 7. Final Clean
    content = content.replace('***', '\n\n***\n\n')
    content = content.replace('---', '\n\n***\n\n')
    content = re.sub(r'\n{3,}', r'\n\n', content)

    # 8. Frontmatter
    final = f"---\ntitle: \"{title}\"\ndescription: \"Mastering {title} for ML.\"\ncomplexity: \"Intermediate\"\nestimated_time: \"20 min\"\nprerequisites: [\"Foundations\"]\n---\n\n# {title}\n\n***\n\n{content.strip()}\n"
    
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(final)

# Mapping and Execution
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
file_to_subject = {i: sub for sub, ids in subject_map.items() for i in ids}
backup_dir = Path('drafts-backup')
content_dir = Path('content')

for p in backup_dir.glob('*.md'):
    try:
        file_id = int(p.name.split('_')[0])
        if file_id in file_to_subject:
            subject = file_to_subject[file_id]
            target_name = p.name.split('_', 1)[1]
            ultimate_rehab(p, content_dir / subject / target_name)
    except: continue

print("THE ULTIMATE REHAB COMPLETE.")
