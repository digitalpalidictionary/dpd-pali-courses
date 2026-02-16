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
        """Ensures the first heading in the file is an H1."""
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if line.strip().startswith("#"):
                # Found the first heading
                if not line.startswith("# "):
                    # It's a heading but not H1 (e.g., ##, ###)
                    # Convert to H1
                    new_line = "# " + line.lstrip("#").strip()
                    lines[i] = new_line
                break # Only fix the first heading found
        return "\n".join(lines) + ("\n" if text.endswith("\n") else "")

    def fix_links(self, text):
        """Fixes broken internal links or image references (placeholder)."""
        # TODO: Implement specific link fixing logic once requirements are clearer
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

    def fix_headers(self, text):
        """Ensures table separator rows have the correct number of columns."""
        lines = text.splitlines()
        new_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            # Detect potential table start (header row followed by separator row)
            if "|" in line and i + 1 < len(lines) and re.match(r"^\s*\|?([\s:-]*\|)+[\s:-]*\s*$", lines[i+1]):
                header_row = line
                separator_row = lines[i+1]
                
                header_cols = self.count_cols(header_row)
                sep_cols = self.count_cols(separator_row)
                
                if header_cols != sep_cols:
                    new_sep = "|" + "---|" * header_cols
                    if not header_row.strip().startswith("|"):
                        new_sep = new_sep[1:]
                    if not header_row.strip().endswith("|"):
                        new_sep = new_sep[:-1]
                    
                    new_lines.append(header_row)
                    new_lines.append(new_sep)
                    i += 2
                    continue
            
            new_lines.append(line)
            i += 1
        return "\n".join(new_lines) + ("\n" if text.endswith("\n") else "")

    def restructure_complex(self, text):
        """Ensures all rows in a table have the correct number of columns."""
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
                    
                    current_cols = self.count_cols(row)
                    if current_cols < max_cols:
                        stripped_row = row.strip()
                        if stripped_row.endswith("|"):
                            new_row = stripped_row + " |" * (max_cols - current_cols)
                        else:
                            new_row = stripped_row + " |" * (max_cols - current_cols)
                        fixed_table.append(new_row)
                    else:
                        fixed_table.append(row)
                
                new_lines.extend(fixed_table)
                i = j
                continue
            
            new_lines.append(line)
            i += 1
        return "\n".join(new_lines) + ("\n" if text.endswith("\n") else "")

class AdvancedCleaner:
    """Handles advanced Markdown cleaning operations."""
    
    def __init__(self):
        self.table_fixer = TableFixer()

    def clean(self, text):
        """Applies all advanced cleaning operations."""
        text = self.table_fixer.fix_headers(text)
        text = self.table_fixer.restructure_complex(text)
        # TODO: Add detect_false_headers if needed
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

def commit_file(file_path, message):
    """Stages and commits a single file."""
    try:
        subprocess.run(["git", "add", file_path], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error committing {file_path}: {e}")
        return False

def main():
    args = parse_arguments(sys.argv[1:])
    print(f"Running in {args.mode} mode on path: {args.path}{' (DRY RUN)' if args.dry_run else ''}")
    
    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist.")
        sys.exit(1)
        
    files = discover_files(args.path)
    print(f"Found {len(files)} Markdown files.")
    
    basic_cleaner = BasicCleaner()
    advanced_cleaner = AdvancedCleaner()
    
    modified_files = []
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        original_content = content
        
        if args.mode in ["basic", "both"]:
            content = basic_cleaner.clean(content)
            
        if args.mode in ["advanced", "both"]:
            content = advanced_cleaner.clean(content)
        
        if content != original_content:
            if not args.dry_run:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                
                # Commit only if the file is in the docs folder
                if file_path.startswith("docs/"):
                    relative_path = os.path.relpath(file_path, "docs")
                    commit_message = f"style(docs): Clean and format {relative_path}"
                    commit_file(file_path, commit_message)
            
            modified_files.append(file_path)
            print(f"  [FIXED] {file_path}")

    print(f"\nProcessing complete.")
    print(f"Total files scanned: {len(files)}")
    print(f"Files modified: {len(modified_files)}")

if __name__ == "__main__":
    main()
