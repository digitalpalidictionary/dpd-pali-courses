import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    lines = content.splitlines()
    new_lines = []
    in_table = False
    has_separator = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('|') and stripped.endswith('|'):
            in_table = True
            if '---|' in line or '|---' in line:
                has_separator = True
            new_lines.append(line)
        else:
            if in_table:
                # Table just ended, add the merged row if it has a separator and not already there
                if has_separator and new_lines and '|' in new_lines[-1] and not new_lines[-1].strip() == '| |':
                    new_lines.append('| |')
                in_table = False
                has_separator = False
            new_lines.append(line)
            
    # Handle case where file ends with a table
    if in_table:
        if has_separator and new_lines and '|' in new_lines[-1] and not new_lines[-1].strip() == '| |':
            new_lines.append('| |')
            
    # 2. Remove **&nbsp;** and normalize empty lines
    temp_content = '\n'.join(new_lines)
    final_content = temp_content.replace('**&nbsp;**', '')
    # Normalize multiple newlines after a table row
    final_content = re.sub(r'\|\s*\|\n\n\n+', r'| |\n\n', final_content)
    # Remove extra spaces at ends of lines
    final_content = '\n'.join([line.rstrip() for line in final_content.splitlines()])
    
    if final_content != content:
        with open(filepath, 'w') as f:
            f.write(final_content)
        return True
    return False

def main():
    folder = 'docs/bpc_ex'
    changed_files = 0
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                if process_file(filepath):
                    print(f"Updated: {filepath}")
                    changed_files += 1
    print(f"Total files updated in bpc_ex: {changed_files}")

if __name__ == '__main__':
    main()
