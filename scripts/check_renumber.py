import os
import re
import argparse

def renumber_file(file_path, dry_run=False):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
    new_lines = []
    current_num = 0
    changed = False
    
    # Pattern to match starting numbers like "1. ", "2.  ", "10. "
    num_pattern = re.compile(r'^(\s*)(\d+)\.\s+(.*)$')

    for line in lines:
        match = num_pattern.match(line)
        if match:
            indent = match.group(1)
            old_num = int(match.group(2))
            text = match.group(3)
            current_num += 1
            
            if old_num != current_num:
                changed = True
                new_lines.append(f"{indent}{current_num}.  {text}")
            else:
                new_lines.append(line)
        else:
            # If we hit a heading, reset numbering
            if line.strip().startswith('#'):
                current_num = 0
            new_lines.append(line)

    if changed:
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines) + ('\n' if content.endswith('\n') else ''))
            print(f"  [RENUMBERED] {file_path}")
        else:
            print(f"  [WOULD RENUMBER] {file_path}")
    else:
        print(f"  [CORRECT] {file_path}")

def main():
    parser = argparse.ArgumentParser(description="Renumber Pāli sentences in markdown files.")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be changed without modifying files.")
    args = parser.parse_args()

    target_dirs = ['docs/bpc_ex', 'docs/bpc_key', 'docs/ipc_ex', 'docs/ipc_key']
    
    for d in target_dirs:
        if not os.path.exists(d):
            continue
        print(f"Checking directory: {d}")
        for root, _, files in os.walk(d):
            for file in files:
                if file.endswith('.md') and file != 'index.md':
                    fp = os.path.join(root, file)
                    renumber_file(fp, args.dry_run)

if __name__ == "__main__":
    main()
