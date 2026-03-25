"""
Universal script to fix table headers in Markdown files.
If a table has data in the first cell of the header row, it moves that data to the body 
by inserting an empty header row.

Exceptions (labels that ARE allowed in headers):
- Pāli, Pali, Pāli1, Pali1
- Root
- prefix

Usage:
    uv run python scripts/fix_bpc_tables.py --dir docs/bpc/
"""
import os
import re
import argparse
from pathlib import Path

def fix_tables_in_content(content):
    lines = content.split('\n')
    new_lines = []
    i = 0
    changed = False
    
    # Exceptions: labels that should remain as headers
    exceptions = ["pāli", "pali", "pāli1", "pali1", "root", "prefix"]
    
    while i < len(lines):
        line = lines[i]
        
        # Detect table start: a line with pipes followed by a separator line
        if '|' in line and i + 1 < len(lines) and re.match(r'^\s*\|?(\s*:?---:?\s*\|)+\s*:?---:?\s*\|?\s*$', lines[i+1]):
            header_row = line
            separator_row = lines[i+1]
            
            # Extract header cells
            cells = [c.strip() for c in header_row.strip('|').split('|')]
            
            # RULE: If first cell is NOT empty, we need to fix it.
            if cells and cells[0] != "":
                first_cell = cells[0].strip('*_ ') # Remove bold/italic/spaces
                
                # EXCEPTIONS: If it's a known header label, skip fixing
                if first_cell.lower() in exceptions:
                    pass
                else:
                    # Create a dummy empty header with same column count
                    num_cols = len(cells)
                    dummy_header = "|" + "  |" * num_cols
                    
                    new_lines.append(dummy_header)
                    new_lines.append(separator_row)
                    new_lines.append(header_row)
                    
                    i += 2 # Skip original header and separator
                    changed = True
                    continue
        
        new_lines.append(line)
        i += 1
        
    return '\n'.join(new_lines), changed

def main():
    parser = argparse.ArgumentParser(description="Fix Markdown table headers by shifting data to body.")
    parser.add_argument("--dir", required=True, help="Directory to process (e.g. docs/bpc)")
    args = parser.parse_args()

    docs_dir = Path(args.dir)
    if not docs_dir.exists():
        print(f"Directory {docs_dir} not found.")
        return

    files_to_process = list(docs_dir.rglob('*.md'))

    total_fixed = 0
    for file_path in files_to_process:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content, changed = fix_tables_in_content(content)
        
        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed tables in {file_path}")
            total_fixed += 1
            
    print(f"\nTotal files updated: {total_fixed}")

if __name__ == "__main__":
    main()
