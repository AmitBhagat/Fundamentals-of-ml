import os
import re

content_dir = r'e:\Projects\Mathematics\content'
drafts_dir = r'e:\Projects\Mathematics\drafts'

# Get drafts names (without number prefix)
drafts_files = os.listdir(drafts_dir)
drafts_names = set()
for f in drafts_files:
    # Match something like "36_probability_density_functions_pdf.md"
    match = re.match(r'\d+_(.*)\.md', f)
    if match:
        drafts_names.add(match.group(1))

# Get content files
extra_files = []
for root, dirs, files in os.walk(content_dir):
    for f in files:
        if f.endswith('.md') and f != 'index.md':
            basename = f.replace('.md', '')
            if basename not in drafts_names:
                # Also check if it matches a draft name with underscores instead of dashes (though usually they match)
                extra_files.append(os.path.join(root, f))

print(f"Found {len(extra_files)} extra files in content:")
for f in extra_files:
    print(f)
