import os
from pathlib import Path

def inject_frontmatter():
    content_dir = Path('content')
    for p in content_dir.rglob('*.md'):
        text = p.read_text(encoding='utf-8')
        if text.startswith('---'):
            continue
            
        title = p.stem.replace('_', ' ').title()
        subject = p.parent.name.replace('-', ' ').title()
        
        frontmatter = f"""---
title: "{title}"
description: "Master the core concepts of {title} in the context of {subject} for Machine Learning."
complexity: "Intermediate"
estimated_time: "15 min"
prerequisites: ["Foundations"]
---

"""
        p.write_text(frontmatter + text, encoding='utf-8')
        print(f"Injected frontmatter into {p}")

if __name__ == "__main__":
    inject_frontmatter()
