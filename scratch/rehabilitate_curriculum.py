import os
import re
from pathlib import Path

def rehabilitate_file(backup_path, target_path):
    with open(backup_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Extract the title from the H1 tag at the top
    title_match = re.search(r'<h1 align="center"> Chapter \d+: (.*?) </h1>', content)
    title = title_match.group(1).strip() if title_match else Path(backup_path).stem.split('_', 1)[-1].replace('_', ' ').title()
    
    # 2. Strip the HTML wrappers (h1, div, etc.)
    # Remove <h1 ...> ... </h1>
    content = re.sub(r'<h1.*?>.*?</h1>', '', content, flags=re.DOTALL)
    # Remove the large justify div
    content = re.sub(r'<div style="text-align: justify;">', '', content)
    # Remove all trailing </div>
    content = content.replace('</div>', '')
    
    # 3. Convert HTML callout boxes to Modern Alert blocks
    # Note/Prerequisite (blue) -> [!NOTE]
    content = re.sub(r'<div style="background-color: #f0f7ff;.*?>(.*?)', r'> [!NOTE]\n>', content, flags=re.DOTALL)
    # Intuition (green) -> [!TIP]
    content = re.sub(r'<div style="background-color: #f0fff4;.*?>(.*?)', r'> [!TIP]\n>', content, flags=re.DOTALL)
    # Critical Insight (red) -> [!CAUTION]
    content = re.sub(r'<div style="background-color: #fff5f5;.*?>(.*?)', r'> [!CAUTION]\n>', content, flags=re.DOTALL)
    # Debugging Tip (yellow/orange) -> [!WARNING]
    content = re.sub(r'<div style="background-color: #fffaf0;.*?>(.*?)', r'> [!WARNING]\n>', content, flags=re.DOTALL)

    # 4. Fix the blockquote lines (ensure every line starts with >)
    # This is tricky because we have multiple blocks.
    # We'll split by [!TYPE] and process each.
    parts = re.split(r'(> \[\!.*?\])', content)
    new_parts = [parts[0]]
    for i in range(1, len(parts), 2):
        marker = parts[i]
        body = parts[i+1]
        # Find the end of this block (usually at the next marker or EOF or large gap)
        # In the backup, blocks were closed by </div> or ---
        block_end_match = re.search(r'\n\n(?!\n)|---|\*\*\*', body)
        if block_end_match:
            block_content = body[:block_end_match.start()]
            remaining = body[block_end_match.start():]
        else:
            block_content = body
            remaining = ""
            
        # Clean block content: strip whitespace and add > to every non-empty line
        clean_lines = []
        for line in block_content.split('\n'):
            line = line.strip()
            if line:
                clean_lines.append(f"> {line}")
            else:
                clean_lines.append(">")
        
        new_parts.append(f"{marker}\n" + "\n".join(clean_lines))
        new_parts.append(remaining)
    content = "".join(new_parts)

    # 5. Fix structural markers (Setup, Calculation, The Story)
    # Bold them if not bolded, ensure double newlines
    markers = ['Setup', 'Calculation', 'The Story', 'The Calculation', 'The Setup']
    for m in markers:
        # Match marker with colon, maybe bolded
        pattern = rf'^\s*\*{{0,2}}{m}:?\*{{0,2}}\s*$'
        content = re.sub(pattern, f'\n\n**{m}:**\n\n', content, flags=re.MULTILINE | re.IGNORECASE)

    # 6. Final cleanup: remove residual HTML and fix spacing
    content = content.replace('***', '\n\n***\n\n')
    content = content.replace('---', '\n\n***\n\n')
    content = re.sub(r'\n{3,}', r'\n\n', content)
    
    # 7. Assemble with clean Frontmatter
    final_content = f"---\ntitle: \"{title}\"\ndescription: \"Mastering {title} for Machine Learning.\"\ncomplexity: \"Intermediate\"\nestimated_time: \"20 min\"\nprerequisites: [\"Foundations\"]\n---\n\n# {title}\n\n***\n\n{content.strip()}\n"
    
    # Write to target
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(final_content)

# Map backup files to content structure
backup_dir = Path('drafts-backup')
content_dir = Path('content')

# Define the subject mapping based on the folder names in 'content/'
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

# Invert map for easier lookup
file_to_subject = {}
for sub, ids in subject_map.items():
    for i in ids:
        file_to_subject[i] = sub

for p in backup_dir.glob('*.md'):
    file_id = int(p.name.split('_')[0])
    if file_id in file_to_subject:
        subject = file_to_subject[file_id]
        # Get target filename (strip ID and subject prefix if present)
        target_name = p.name.split('_', 1)[1]
        target_path = content_dir / subject / target_name
        rehabilitate_file(p, target_path)

print("Rehabilitation complete.")
