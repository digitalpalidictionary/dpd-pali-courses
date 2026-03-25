"""
Script to find and remove dead links in Markdown files.
Specifically targets list items in index files that link to removed .md files.
"""
import os
import re
from pathlib import Path

def resolve_link(base_file: Path, link_target: str) -> Path:
    # If the link has an anchor like target.md#section, strip it
    if '#' in link_target:
        link_target = link_target.split('#')[0]
    
    # We only care about .md files
    if not link_target.endswith('.md'):
        return None

    # Resolve relative path
    target_path = (base_file.parent / link_target).resolve()
    return target_path

def clean_dead_links_in_file(file_path: Path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    changed = False
    
    # Match markdown links: [text](target.md)
    # We specifically want to find lines that are list items with links
    # e.g., "- [Topic](topic.md)"
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+\.md(?:#[^)]*)?)\)')
    
    for line in lines:
        matches = link_pattern.finditer(line)
        line_has_dead_link = False
        
        for match in matches:
            target = match.group(2)
            resolved_path = resolve_link(file_path, target)
            
            if resolved_path and not resolved_path.exists():
                line_has_dead_link = True
                break
                
        # If the line is just a list item with a dead link, we skip the entire line
        if line_has_dead_link and line.strip().startswith('- '):
            changed = True
            continue
            
        new_lines.append(line)
        
    if changed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False

def main():
    docs_dir = Path('docs').resolve()
    total_changed = 0
    
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                if clean_dead_links_in_file(file_path):
                    print(f"Removed dead link(s) from {file_path.relative_to(docs_dir)}")
                    total_changed += 1
                    
    if total_changed > 0:
        print(f"Cleaned dead links in {total_changed} files.")

if __name__ == '__main__':
    main()
