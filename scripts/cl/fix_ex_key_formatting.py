import os
import re

def process_table_merged_row(filepath):
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
                if has_separator and new_lines and '|' in new_lines[-1] and not new_lines[-1].strip() == '| |':
                    new_lines.append('| |')
                in_table = False
                has_separator = False
            new_lines.append(line)
            
    if in_table:
        if has_separator and new_lines and '|' in new_lines[-1] and not new_lines[-1].strip() == '| |':
            new_lines.append('| |')
            
    temp_content = '\n'.join(new_lines)
    final_content = temp_content.replace('**&nbsp;**', '')
    final_content = re.sub(r'\|\s*\|\n\n\n+', r'| |\n\n', final_content)
    final_content = '\n'.join([line.rstrip() for line in final_content.splitlines()])
    
    if final_content != content:
        with open(filepath, 'w') as f:
            f.write(final_content)
        return True
    return False

def process_footnotes_bold(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Target pattern: **[^1]: ...**
    # Using a regex to catch bolded footnote definitions at the start of a line
    new_content = re.sub(r'^\s*\*\*(\[\^\d+\]:.*?)\*\*', r'\1', content, flags=re.MULTILINE)
    
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        return True
    return False

def main():
    # 1. Process ipc_ex tables
    folder_ipc_ex = 'docs/ipc_ex'
    changed_tables = 0
    for root, _, files in os.walk(folder_ipc_ex):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                if process_table_merged_row(filepath):
                    print(f"Updated tables: {filepath}")
                    changed_tables += 1
    
    # 2. Process bold footnotes in specified folders
    folders_footnotes = ['docs/bpc_ex', 'docs/bpc_key', 'docs/ipc_ex', 'docs/ipc_key']
    changed_footnotes = 0
    for folder in folders_footnotes:
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith('.md'):
                    filepath = os.path.join(root, file)
                    if process_footnotes_bold(filepath):
                        print(f"Updated footnotes: {filepath}")
                        changed_footnotes += 1
                        
    print(f"Total files updated (tables): {changed_tables}")
    print(f"Total files updated (footnotes): {changed_footnotes}")

if __name__ == '__main__':
    main()
