"""Normalize markdown tables: cell padding, separator rows, and bold footnote definitions."""

import re
import glob
from tools.printer import printer as pr

def normalize_cell_padding(line: str) -> str:
    """Strip excessive whitespace in table cells to single-space padding."""
    if not line.startswith("|"):
        return line
    # Split by pipe, strip each cell, rejoin
    parts = line.split("|")
    # parts[0] is before first pipe (empty), parts[-1] is after last pipe (empty)
    if len(parts) < 3:
        return line
    inner = parts[1:-1]
    # Don't touch empty cells (whitespace-only)
    normalized = []
    for cell in inner:
        stripped = cell.strip()
        if stripped == "":
            normalized.append(" ")
        else:
            normalized.append(f" {stripped} ")
    return "|" + "|".join(normalized) + "|"


def normalize_separator_row(line: str) -> str:
    """Normalize separator rows like |-----|---| to | --- | --- |."""
    if not re.match(r"^\|[\s:]*-", line):
        return line
    parts = line.split("|")
    if len(parts) < 3:
        return line
    inner = parts[1:-1]
    normalized = []
    for cell in inner:
        cell = cell.strip()
        # Check if it's a separator cell (only dashes and optional alignment colons)
        if not re.match(r"^:?-+:?$", cell):
            return line  # Not a separator row
        # Preserve alignment markers
        left = cell.startswith(":")
        right = cell.endswith(":")
        sep = ""
        if left:
            sep += ":"
        sep += "---"
        if right:
            sep += ":"
        normalized.append(f" {sep} ")
    return "|" + "|".join(normalized) + "|"


def strip_bold_footnote_defs(line: str) -> str:
    """Strip bold wrapping from fully-bold footnote definitions."""
    # Match: **[^N]: text** — entire line is bold-wrapped footnote def
    m = re.match(r"^\*\*(\[\^\d+\]:.*?)\*\*$", line.strip())
    if m:
        return m.group(1)
    return line


def process_file(filepath: str) -> bool:
    """Process a single markdown file. Returns True if changes were made."""
    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()

    lines = original.split("\n")
    new_lines = []
    for line in lines:
        line = normalize_cell_padding(line)
        line = normalize_separator_row(line)
        line = strip_bold_footnote_defs(line)
        new_lines.append(line)

    result = "\n".join(new_lines)
    if result != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(result)
        return True
    return False


def main() -> None:
    pr.green("Fixing tables and formatting")
    files = sorted(glob.glob("docs/**/*.md", recursive=True))
    changed: list[str] = []
    for filepath in files:
        if process_file(filepath):
            changed.append(filepath)

    if changed:
        pr.no(f"{len(changed)} files")
        for filepath in changed:
            pr.warning(filepath)
    else:
        pr.yes("ok")


if __name__ == "__main__":
    main()
