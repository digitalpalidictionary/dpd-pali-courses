#!/usr/bin/env bash
# Run pre-processing checks and corrections before generating PDF and DOCX documents.

set -e

echo "Starting PDF/DOCX pre-processing..."

echo "1. Generating/Updating mkdocs.yaml..."
uv run python scripts/generate_mkdocs_yaml.py

echo "2. Checking and correcting sentence numbering..."
uv run python scripts/check_renumber.py

echo "3. Re-ordering footnotes sequentially..."
uv run python scripts/renumber_footnotes.py

echo "4. Cleaning dead links..."
uv run python scripts/clean_dead_links.py

echo ""
echo "PDF/DOCX pre-processing complete!"
echo ""
