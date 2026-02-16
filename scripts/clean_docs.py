import argparse
import sys
import os
import re
import subprocess

class BasicCleaner:
    """Handles basic Markdown cleaning operations."""

    def remove_nbsp(self, text):
        """Replaces &nbsp; with a standard space."""
        return text.replace("&nbsp;", " ")

    def standardize_headings(self, text):
        """
        Ensures ONLY the first heading in the file is an H1.
        All other headings must be at least H2.
        """
        lines = text.splitlines()
        first_heading_idx = -1
        
        # 1. Find the index of the first heading
        for idx, line in enumerate(lines):
            if re.match(r'^#+\s+', line):
                first_heading_idx = idx
                break
        
        if first_heading_idx == -1:
            return text

        new_lines = []
        for idx, line in enumerate(lines):
            match = re.match(r'^(#+)(\s+.*)$', line)
            if match:
                level = len(match.group(1))
                content = match.group(2).strip()
                
                if idx == first_heading_idx:
                    # Always make the very first heading H1
                    new_lines.append("# " + content)
                else:
                    # All subsequent headings MUST be at least H2
                    # If it was H1, it becomes H2. If it was H2+, it remains.
                    new_level = max(2, level)
                    new_lines.append("#" * new_level + " " + content)
            else:
                new_lines.append(line)
                
        return "\n".join(new_lines) + ("\n" if text.endswith("\n") else "")

    def fix_links(self, text):
        """Fixes broken internal links or image references (placeholder)."""
        return text

    def clean_horizontal_rules(self, text):
        """Reduces multiple consecutive horizontal rules (***) to a single one.
        Ensures it only matches lines containing ONLY the horizontal rule.
        """
        # Match lines that are exactly '***' (with optional whitespace)
        # We use re.MULTILINE to make ^ and $ match start/end of lines
        text = re.sub(r'^\s*\*\*\*\s*$', '___HR_MARKER___', text, flags=re.MULTILINE)
        # Reduce multiple markers (optionally separated by whitespace/newlines) to one
        text = re.sub(r'(\s*___HR_MARKER___\s*)+', '\n***\n', text)
        return text.strip()

    def remove_empty_headings(self, text):
        """Removes lines that consist only of '#' characters and whitespace."""
        lines = text.splitlines()
        new_lines = []
        for line in lines:
            # Match lines with one or more '#' and nothing else
            if re.match(r'^\s*#+\s*$', line):
                continue
            new_lines.append(line)
        return "\n".join(new_lines)

    def clean(self, text):
        """Applies all basic cleaning operations."""
        text = self.remove_nbsp(text)
        text = self.standardize_headings(text)
        text = self.fix_links(text)
        text = self.clean_horizontal_rules(text)
        text = self.remove_empty_headings(text)
        return text

class TableFixer:
    """Specialized class for fixing Markdown tables."""

    @staticmethod
    def count_cols(row):
        """Robust column counting for piped tables."""
        inner = row.strip()
        if inner.startswith("|"): inner = inner[1:]
        if inner.endswith("|"): inner = inner[:-1]
        return len(inner.split("|"))

    @staticmethod
    def get_cells(row):
        """Extracts cells from a table row."""
        inner = row.strip()
        if inner.startswith("|"): inner = inner[1:]
        if inner.endswith("|"): inner = inner[:-1]
        return [c.strip() for c in inner.split("|")]

    def format_title(self, text):
        """Wraps text in bold if not already bold. Smarter about internal boldness."""
        text = text.strip()
        # If already fully bolded
        if text.startswith("**") and text.endswith("**") and text.count("**") == 2:
            return text
        
        # If has internal boldness, strip it and wrap whole thing
        if "**" in text:
            clean_text = text.replace("**", "")
            return f"**{clean_text}**"
            
        return f"**{text}**"

    def is_empty_row(self, row):
        """Checks if a row consists only of pipes and whitespace."""
        cells = self.get_cells(row)
        return not any(c for c in cells)

    def restructure_sentence_analysis(self, text):
        """
        Specialized logic for bpc_key/ etc. tables.
        Spreads Pāli sentences and English translations across all columns.
        """
        lines = text.splitlines()
        new_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            # Detect table
            if "|" in line and i + 1 < len(lines) and re.match(r"^\s*\|?([\s:-]*\|)+[\s:-]*\s*$", lines[i+1]):
                table_lines = []
                j = i
                while j < len(lines) and "|" in lines[j]:
                    table_lines.append(lines[j])
                    j += 1
                
                max_cols = self.count_cols(table_lines[1])
                
                fixed_table = []
                for idx, row in enumerate(table_lines):
                    if idx == 1:
                        fixed_table.append(row)
                        continue
                    
                    cells = self.get_cells(row)
                    content_cells = [c for c in cells if c]
                    
                    # Heuristic for sentence/translation row: 
                    # Only first cell has content, and it's long or contains <br> or starts with Cap
                    is_pali_sentence = len(content_cells) == 1 and "<br>" in cells[0]
                    is_english_trans = len(content_cells) == 1 and re.match(r'^[A-Z]', cells[0]) and len(cells[0].split()) > 3
                    
                    if is_pali_sentence or is_english_trans:
                        # Spread across all columns: | Content | | | |
                        new_row = "| " + cells[0] + " | " + " | ".join([""] * (max_cols - 1)) + " |"
                        fixed_table.append(new_row)
                    else:
                        # Regular row normalization
                        current_cols = self.count_cols(row)
                        if current_cols < max_cols:
                            row = row.strip()
                            if not row.endswith("|"): row += " |"
                            row += " |" * (max_cols - current_cols)
                        fixed_table.append(row)
                
                new_lines.extend(fixed_table)
                i = j
                continue
            
            new_lines.append(line)
            i += 1
        return "\n".join(new_lines) + ("\n" if text.endswith("\n") else "")

    def adjust_structure(self, text):
        """
        Adjusts table structure.
        Ensures a horizontal rule follows every table.
        """
        lines = text.splitlines()
        new_lines = []
        i = 0
        current_section = ""
        
        while i < len(lines):
            line = lines[i]
            
            # Track current section to handle ### Extra Reading
            if line.startswith("#"):
                current_section = line.strip()

            # Detect table start (Header + Separator)
            if "|" in line and i + 1 < len(lines) and re.match(r"^\s*\|?([\s:-]*\|)+[\s:-]*\s*$", lines[i+1]):
                header_row = line
                separator_row = lines[i+1]
                col_count = self.count_cols(separator_row)
                
                header_cells = self.get_cells(header_row)
                if len(header_cells) < col_count:
                    header_cells.extend([''] * (col_count - len(header_cells)))
                
                non_empty_header = [c for c in header_cells if c]
                first_cell = header_cells[0] if header_cells else ""
                
                # Logic for headless tables (Type 2 / Extra Reading)
                is_extra_reading = "Extra Reading" in current_section
                is_false_header = col_count > 1 and re.match(r'^[a-z]', first_cell) and len(non_empty_header) > 1
                
                if is_extra_reading or is_false_header:
                    # Make it headless
                    new_lines.append(("| " * col_count) + "|")
                    new_lines.append("|---" + "|---" * (col_count - 1) + "|")
                    if not self.is_empty_row(header_row):
                        new_lines.append(header_row)
                    i += 2 # Skip original header and separator
                elif col_count > 1 and len(non_empty_header) == 1 and header_cells[0]:
                    # Type 1: Spanning Header - Extract title
                    new_lines.append(self.format_title(header_cells[0]))
                    new_lines.append(("| " * col_count) + "|")
                    new_lines.append("|---" + "|---" * (col_count - 1) + "|")
                    i += 2 # Skip original header and separator
                else:
                    # Normal table
                    new_lines.append(header_row)
                    new_lines.append(separator_row)
                    i += 2

                # Process Table Body
                while i < len(lines) and "|" in lines[i]:
                    row = lines[i]
                    if not row.strip() or "|" not in row:
                        break
                    
                    # Skip empty data rows
                    if self.is_empty_row(row):
                        i += 1
                        continue
                        
                    # Normalize column count
                    current_cols = self.count_cols(row)
                    if current_cols < col_count:
                        row = row.strip()
                        if not row.endswith("|"): row += " |"
                        row += " |" * (col_count - current_cols)
                    new_lines.append(row)
                    i += 1
                
                # End of table: Add horizontal rule
                new_lines.append("***")
                continue

            new_lines.append(line)
            i += 1
            
        return "\n".join(new_lines) + ("\n" if text.endswith("\n") else "")

class AdvancedCleaner:
    """Handles advanced Markdown cleaning operations."""
    
    def __init__(self):
        self.table_fixer = TableFixer()

    def clean(self, text, file_path=""):
        """Applies all advanced cleaning operations."""
        # Special restructuring for key/ex folders
        if any(x in file_path for x in ["_key/", "_ex/"]):
            text = self.table_fixer.restructure_sentence_analysis(text)
            
        text = self.table_fixer.adjust_structure(text)
        return text

def discover_files(path):
    """Recursively lists all .md files in the given path."""
    md_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    return sorted(md_files)

def parse_arguments(args):
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(description="Clean and reformat Markdown files in docs/ folder.")
    parser.add_argument(
        "--mode",
        choices=["basic", "advanced", "both"],
        default="basic",
        help="Cleaning mode: 'basic', 'advanced', or 'both' (default: basic)"
    )
    parser.add_argument(
        "--path",
        default="docs",
        help="Path to the directory containing Markdown files (default: docs)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Display changes without modifying files."
    )
    return parser.parse_args(args)

def main():
    args = parse_arguments(sys.argv[1:])
    print(f"Running in {args.mode} mode on path: {args.path}{' (DRY RUN)' if args.dry_run else ''}")
    
    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist.")
        sys.exit(1)
        
    files = discover_files(args.path)
    
    print(f"Found {len(files)} target Markdown files.")
    
    basic_cleaner = BasicCleaner()
    advanced_cleaner = AdvancedCleaner()
    
    modified_count = 0
    for file_path in files:
        # User requested to skip docs/ipc/class_18/11_ex.md as its changes were wrong
        if "ipc/class_18/11_ex.md" in file_path:
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        original_content = content
        
        if args.mode in ["basic", "both"]:
            content = basic_cleaner.clean(content)
            
        if args.mode in ["advanced", "both"]:
            content = advanced_cleaner.clean(content, file_path)
            
        # Final pass of basic cleaning to deduplicate rules that might have been added
        if content != original_content:
            content = basic_cleaner.clean_horizontal_rules(content)
        
        if content != original_content:
            if not args.dry_run:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
            modified_count += 1
            print(f"  [FIXED] {file_path}")

    print(f"\nProcessing complete.")
    print(f"Total target files scanned: {len(files)}")
    print(f"Files modified: {modified_count}")

if __name__ == "__main__":
    main()
