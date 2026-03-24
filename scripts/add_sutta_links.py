
"""
Script to right-align sutta references in 1_review.md files.
Uses the attr_list extension syntax ({: .align-right }) for clean Markdown source.
"""
import os
import re

def add_sutta_alignment(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Clean up ANY previous alignment attempts (both divs and {: .align-right })
    # Remove div wraps
    cleaned_content = re.sub(r'<div class="align-right"(?: markdown="1")?>\n*(.*?)\n*</div>', r'\1', content, flags=re.DOTALL)
    # Remove existing attr_list alignment if any
    cleaned_content = re.sub(r'\{: \.align-right \}', '', cleaned_content)
    # Remove excessive newlines that might have been left behind
    cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)
    
    # 2. Re-apply using the cleaner attr_list syntax
    prefixes = ['AN', 'SN', 'MN', 'DN', 'DHP', 'SNP', 'VIN', 'KHP', 'ITI', 'UD', 'Vism']
    prefix_pattern = '|'.join(prefixes)
    sutta_line_regex = re.compile(rf'^\s*[\[\*\_]*(?:{prefix_pattern})', re.IGNORECASE)
    
    lines = cleaned_content.split('\n')
    new_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if line matches sutta reference and is not a heading or nav-link
        if sutta_line_regex.match(line) and not line.strip().startswith('#') and 'nav-links' not in line:
            clean_line = line.strip()
            # We want:
            # Sutta Link
            # {: .align-right }
            
            # Ensure empty line BEFORE if not already there
            if new_lines and new_lines[-1].strip() != '':
                new_lines.append('')
            
            new_lines.append(clean_line)
            new_lines.append('{: .align-right }')
            
            # Ensure empty line AFTER if next line is not empty and not end of file
            if i + 1 < len(lines) and lines[i+1].strip() != '':
                new_lines.append('')
        else:
            new_lines.append(line)
        i += 1

    final_content = '\n'.join(new_lines)
    # Final cleanup of spacing
    final_content = re.sub(r'\n{3,}', '\n\n', final_content)
    
    if final_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        return True
    return False

def main():
    docs_dir = 'docs'
    files_affected = 0
    
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file == '1_review.md':
                path = os.path.join(root, file)
                if add_sutta_alignment(path):
                    files_affected += 1
                    print(f"Updated alignment to MD syntax in {path}")
                    
    print(f"\nTotal files affected: {files_affected}")

if __name__ == '__main__':
    main()
