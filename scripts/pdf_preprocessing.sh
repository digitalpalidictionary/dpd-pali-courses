#!/usr/bin/env bash
# Run pre-processing checks and corrections before generating PDF and DOCX documents.

set -e

echo "Starting PDF/DOCX pre-processing..."

uv run python scripts/generate_mkdocs_yaml.py
uv run python scripts/check_renumber.py
uv run python scripts/renumber_footnotes.py
uv run python scripts/clean_dead_links.py
uv run python scripts/fix_heading_hierarchy.py
uv run python scripts/fixing_tables.py

echo ""
echo "PDF/DOCX pre-processing complete!"
echo ""
