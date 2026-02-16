# Markdown Documentation Cleaner

A Python tool to automate the cleaning and formatting of Markdown files in the `docs/` folder.

## Features
- **Basic Cleaning:**
    - Removes `&nbsp;` entities.
    - Ensures the first heading is an H1.
    - Reduces multiple horizontal rules (`***`) to a single one.
    - Removes empty heading lines (e.g., `#`, `##`).
- **Advanced Cleaning:**
    - Fixes malformed table headers (mismatched separator columns).
    - Restructures complex tables to ensure consistent column counts across all rows.
- **Git Integration:**
    - Automatically stages and commits each modified file in the `docs/` folder with a descriptive message.
- **Dry Run:**
    - Use the `--dry-run` flag to preview changes without modifying files or committing.

## Usage

```bash
# Basic cleaning (default)
uv run python3 clean_docs.py

# Advanced cleaning
uv run python3 clean_docs.py --mode advanced

# Run both basic and advanced cleaning
uv run python3 clean_docs.py --mode both

# Preview changes without applying them
uv run python3 clean_docs.py --mode both --dry-run

# Specify a custom path
uv run python3 clean_docs.py --path my_other_docs/
```

## Development

Run tests using:
```bash
uv run python3 test_clean_docs.py
```
