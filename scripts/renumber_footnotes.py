"""
Script to renumber footnotes sequentially across all files in a course folder.
The counter starts at 1 and continues across files in course order, so class_1 footnotes
come before class_2 footnotes. Duplicate numbers and out-of-order numbers are corrected automatically.
"""
import os
import re
import argparse
from tools.printer import printer as pr

def get_files_sorted(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.md') and f != 'index.md']
    def sort_key(f):
        parts = f.split('_')
        if parts[0].isdigit():
            return (0, int(parts[0]))
        return (1, f)
    return sorted(files, key=sort_key)


def get_ordered_files_for_folder(base_dir):
    """Returns a list of markdown files in logical course order."""
    ordered_files = []

    index_path = os.path.join(base_dir, 'index.md')
    if os.path.exists(index_path):
        ordered_files.append(index_path)

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


def _is_line_def(content: str, pos: int, end: int) -> bool:
    """True if [^N]: is at the start of a line — Pandoc footnote definition syntax.
    Allows leading whitespace and markdown emphasis chars (* _) before [^N]:."""
    line_start = content.rfind('\n', 0, pos) + 1
    prefix = content[line_start:pos]
    return bool(re.match(r'^[\s*_]*$', prefix)) and content[end:end + 1] == ':'


def renumber_footnotes_in_files(files: list[str], dry_run: bool = False) -> int:
    # Counter persists across all files in this folder so numbering is globally unique.
    global_counter = 1
    total_changed = 0

    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Build occurrence map from references only (not line-start definitions).
        # Inline [^N]: (colon is part of surrounding sentence) counts as a reference.
        occurrence_map: dict[str, list[int]] = {}
        for match in re.finditer(r'\[\^(\d+)\]', content):
            if not _is_line_def(content, match.start(), match.end()):
                old_num = match.group(1)
                if old_num not in occurrence_map:
                    occurrence_map[old_num] = []
                occurrence_map[old_num].append(global_counter)
                global_counter += 1

        if not occurrence_map:
            continue

        needs_change = (
            any(new != int(old) for old, news in occurrence_map.items() for new in news)
            or any(len(v) > 1 for v in occurrence_map.values())
        )
        if not needs_change:
            continue

        total_changed += 1

        for old_num, new_nums in occurrence_map.items():
            if len(new_nums) > 1:
                pr.warning(f"Duplicate [^{old_num}] in {file_path} — split into {new_nums}")

        # Single-pass replacement: refs and defs tracked separately by occurrence index.
        # The Nth definition of a given number pairs with the Nth reference of that number.
        ref_occ: dict[str, int] = {}
        def_occ: dict[str, int] = {}

        def replacer(match: re.Match) -> str:  # type: ignore[type-arg]
            old = match.group(1)
            suffix = match.group(2)  # ':' or ''
            # Pass position after ] (before colon) — (:?) in the regex already consumed it.
            is_def = _is_line_def(content, match.start(), match.end() - len(suffix))
            occ = def_occ if is_def else ref_occ
            idx = occ.get(old, 0)
            occ[old] = idx + 1
            new_nums = occurrence_map.get(old, [int(old)])
            new = new_nums[idx] if idx < len(new_nums) else new_nums[-1]
            return f"[^{new}]{suffix}"

        new_content = re.sub(r'\[\^(\d+)\](:?)', replacer, content)

        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

    return total_changed


def main() -> None:
    parser = argparse.ArgumentParser(description="Renumber footnotes sequentially per course folder.")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be changed.")
    args = parser.parse_args()

    pr.green("Renumbering footnotes")
    target_dirs = ['docs/bpc', 'docs/ipc', 'docs/bpc_ex', 'docs/ipc_ex', 'docs/bpc_key', 'docs/ipc_key']

    total_changed = 0
    for d in target_dirs:
        if not os.path.exists(d):
            continue
        ordered_files = get_ordered_files_for_folder(d)
        total_changed += renumber_footnotes_in_files(ordered_files, dry_run=args.dry_run)

    if total_changed:
        pr.no(f"{total_changed} files")
    else:
        pr.yes("ok")


if __name__ == "__main__":
    main()
