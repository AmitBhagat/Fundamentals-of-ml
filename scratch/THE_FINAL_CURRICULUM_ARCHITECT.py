import os
import re
from pathlib import Path

def architect_chapter(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        full_content = f.read()

    # Split into frontmatter and body
    parts = full_content.split('---\n', 2)
    if len(parts) < 3: return
    frontmatter = parts[1]
    body = parts[2]

    # Extract Title (H1)
    title_match = re.search(r'^#\s*(.*)$', body, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else ""
    body = re.sub(r'^#\s*.*$', '', body, count=1, flags=re.MULTILINE)

    # Helper to find cards
    def extract_card(content, type_name):
        pattern = rf'> \[!{type_name}\].*?\n(>.*?\n)+'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(0).strip(), content.replace(match.group(0), '')
        return None, content

    card_note, body = extract_card(body, "NOTE")
    card_tip, body = extract_card(body, "TIP")
    card_caution, body = extract_card(body, "CAUTION")
    card_warning, body = extract_card(body, "WARNING")

    # Split into sections
    sections = re.split(r'^##\s+', body, flags=re.MULTILINE)
    
    analogy = ""
    math_link = ""
    numericals = []
    ml_apps = ""
    
    for sec in sections:
        sec = sec.strip()
        if not sec: continue
        
        lines = sec.split('\n')
        header = lines[0].strip().lower()
        content = '\n'.join(lines[1:]).strip()
        
        if 'analogy' in header:
            analogy = content
        elif 'math link' in header:
            math_link = content
        elif 'run the numbers' in header or 'example' in header:
            # This section might contain multiple examples
            sub_examples = re.split(r'^###\s+', '\n' + content, flags=re.MULTILINE)
            for ex in sub_examples:
                ex = ex.strip()
                if not ex: continue
                
                # Split example into Setup/Calculation/Story
                ex_lines = ex.split('\n')
                ex_header = ex_lines[0].strip()
                ex_body = '\n'.join(ex_lines[1:]).strip()
                
                # Standardize Setup/Calculation/Story
                def get_part(txt, marker):
                    # Find marker (case insensitive, bold or not)
                    m = re.search(rf'\*\*?{marker}:?\*\*?', txt, re.IGNORECASE)
                    if not m: return ""
                    # Content is everything until the next marker
                    rest = txt[m.end():].strip()
                    next_m = re.search(rf'\*\*?(Setup|Calculation|Story|The Setup|The Calculation|The Story):?\*\*?', rest, re.IGNORECASE)
                    if next_m:
                        return rest[:next_m.start()].strip()
                    return rest
                
                setup = get_part(ex_body, 'Setup') or get_part(ex_body, 'The Setup')
                calc = get_part(ex_body, 'Calculation') or get_part(ex_body, 'The Calculation')
                story = get_part(ex_body, 'Story') or get_part(ex_body, 'The Story')
                
                # If Calculation is missing, look for math blocks
                if not calc:
                    math_match = re.search(r'\$\$.*?\$\$', ex_body, re.DOTALL)
                    if math_match: calc = math_match.group(0)
                
                numericals.append({
                    'title': ex_header,
                    'setup': setup,
                    'calculation': calc,
                    'story': story
                })
        elif 'ml applications' in header:
            ml_apps = content

    # Re-Assemble
    new_body = f"# {title}\n\n***\n\n"
    
    if card_note:
        new_body += f"{card_note}\n\n"
    
    if analogy:
        new_body += f"## Analogy\n\n{analogy}\n\n"
    
    if math_link:
        new_body += f"## The Math Link\n\n{math_link}\n\n"
        
    if card_tip:
        new_body += f"{card_tip}\n\n"
    
    new_body += "***\n\n## Let's Run the Numbers\n\n***\n\n"
    
    for i, ex in enumerate(numericals):
        # Clean title (remove "Example X:" if it exists)
        clean_title = re.sub(r'^\d+\.?\s*', '', ex['title'])
        clean_title = re.sub(r'^Example\s*\d+:?\s*', '', clean_title, flags=re.IGNORECASE)
        
        new_body += f"## Example {i+1}: {clean_title}\n\n"
        if ex['setup']: new_body += f"**Setup:**\n\n{ex['setup']}\n\n"
        if ex['calculation']: new_body += f"**Calculation:**\n\n{ex['calculation']}\n\n"
        if ex['story']: new_body += f"**Story:**\n\n{ex['story']}\n\n"
        new_body += "***\n\n"

    if card_caution:
        new_body += f"{card_caution}\n\n***\n\n"
        
    if ml_apps:
        new_body += f"## ML Applications\n\n{ml_apps}\n\n"
        
    if card_warning:
        new_body += f"{card_warning}\n\n"

    # Final cleanup (multiple newlines, etc.)
    final_body = re.sub(r'\n{3,}', r'\n\n', new_body)
    
    # Save
    final_content = f"---\n{frontmatter}---\n\n{final_body.strip()}\n"
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(final_content)

content_dir = Path('content')
# Skip specific files already manually fixed if needed, but the architect should be idempotent
for p in content_dir.rglob('*.md'):
    if p.name == 'index.md': continue
    try:
        architect_chapter(str(p))
    except Exception as e:
        print(f"Error processing {p}: {e}")

print("THE FINAL CURRICULUM ARCHITECT COMPLETE.")
