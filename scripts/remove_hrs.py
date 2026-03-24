"""
Script to replace '***' horizontal rules with vertical space (empty lines) in Markdown files.
This maintains visual separation without the explicit line, providing a clean space between sentences.
Handles false positives for bold-italic '***' by ensuring the line contains only the horizontal rule.
"""
import os
import re

def replace_stars_with_space(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Match '***' on its own line (optionally with surrounding whitespace)
    # and its trailing newline. Replace it with two newlines (one blank line).
    hr_pattern = re.compile(r'^\s*\*\*\*\s*$\n?', re.MULTILINE)
    new_content = hr_pattern.sub('\n\n', content)
    
    # 2. Collapse any sequence of 3 or more newlines into exactly 2 newlines (one blank line).
    # This prevents triple or quadruple newlines when the original file already had empty lines
    # surrounding the '***'.
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return 1 # Return 1 for file affected
    return 0

def main():
    docs_dir = 'docs'
    total_replaced = 0
    files_affected = 0
    
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                # Note: count in previous version was HRs per file. 
                # This version returns 1 if file was modified.
                affected = replace_stars_with_space(path)
                if affected > 0:
                    files_affected += 1
                    print(f"Cleaned HRs in {path}")
                    
    print(f"\nTotal files affected: {files_affected}")

if __name__ == '__main__':
    main()
