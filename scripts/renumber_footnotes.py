"""
Script to renumber footnotes sequentially per main course folder.
Processes files in the order they appear in the course.
"""
import os
import re
import argparse

def get_files_sorted(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.md') and f != 'index.md']
    def sort_key(f):
        parts = f.split('_')
        if parts[0].isdigit(): return (0, int(parts[0]))
        return (1, f)
    return sorted(files, key=sort_key)

def get_ordered_files_for_folder(base_dir):
    """Returns a list of markdown files in logical course order."""
    ordered_files = []
    
    index_path = os.path.join(base_dir, 'index.md')
    if os.path.exists(index_path):
        ordered_files.append(index_path)

    # Check if it has class_ folders (like bpc, ipc) or just files (like bpc_ex)
    folders = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d.startswith('class_')]
    
    if folders:
        folders = sorted(folders, key=lambda x: int(x.split('_')[1]) if x.split('_')[1].isdigit() else 0)
        for folder in folders:
            folder_path = os.path.join(base_dir, folder)
            f_index = os.path.join(folder_path, 'index.md')
            if os.path.exists(f_index):
                ordered_files.append(f_index)
            for f in get_files_sorted(folder_path):
                ordered_files.append(os.path.join(folder_path, f))
    else:
        for f in get_files_sorted(base_dir):
            ordered_files.append(os.path.join(base_dir, f))
            
    return ordered_files

def renumber_footnotes_in_files(files, start_counter=1, dry_run=False):
    global_counter = start_counter
    total_changed = 0

    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find all footnote references in the text (ignoring definitions for now to get order)
        # References look like [^1], [^2]. But we want to ensure we don't catch definitions [^1]:
        # Using regex to find all matches of [^...]
        # We need to process line by line or finditer.
        # Actually, let's just find all [^X] that are NOT followed by a colon.
        refs = re.finditer(r'\[\^(\d+)\](?!:)', content)
        
        file_map = {}
        for match in refs:
            old_num = match.group(1)
            if old_num not in file_map:
                file_map[old_num] = global_counter
                global_counter += 1

        if not file_map:
            continue

        # Check if any numbering actually needs to change
        changed = any(str(old) != str(new) for old, new in file_map.items())
        
        if "docs/ipc/index.md" in file_path:
            print(f"DEBUG {file_path}: file_map = {file_map}, changed = {changed}")
        
        if not changed:
            continue

        total_changed += 1
        
        # Replace occurrences. To avoid replacing [^12] when looking for [^1], 
        # we can do a two-pass replacement or use a regex callback.
        
        def replacer(match):
            old_num = match.group(1)
            suffix = match.group(2) # captures the optional colon
            new_num = file_map.get(old_num, old_num) # if not in map, keep old (might be a detached definition)
            return f"[^{new_num}]{suffix}"

        # Match [^1] or [^1]:
        new_content = re.sub(r'\[\^(\d+)\](:?)', replacer, content)

        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  [RENUMBERED] {file_path}")
        else:
            print(f"  [WOULD RENUMBER] {file_path}")

    return total_changed

def main():
    parser = argparse.ArgumentParser(description="Renumber footnotes sequentially per course folder.")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be changed.")
    args = parser.parse_args()

    target_dirs = ['docs/bpc', 'docs/ipc', 'docs/bpc_ex', 'docs/ipc_ex', 'docs/bpc_key', 'docs/ipc_key']
    
    total_changed_across_all = 0
    for d in target_dirs:
        if not os.path.exists(d):
            continue
        ordered_files = get_ordered_files_for_folder(d)
        changed = renumber_footnotes_in_files(ordered_files, start_counter=1, dry_run=args.dry_run)
        total_changed_across_all += changed
        
    if total_changed_across_all > 0:
        print(f"Renumbered footnotes in {total_changed_across_all} files.")

if __name__ == "__main__":
    main()
