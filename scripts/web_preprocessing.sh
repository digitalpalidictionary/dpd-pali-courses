#!/usr/bin/env bash
# Pre-processing steps required before building the MkDocs website.

set -e

scripts/regenerate_pages.sh

echo "Starting web pre-processing..."
uv run python scripts/generate_mkdocs_yaml.py
uv run python scripts/check_renumber.py
uv run python scripts/renumber_footnotes.py
uv run python scripts/clean_dead_links.py
uv run python scripts/fix_heading_hierarchy.py
uv run python scripts/fixing_tables.py
export PYTHONPATH=$PYTHONPATH:.
uv run python scripts/generate_indexes.py
uv run python scripts/update_css.py

echo ""
echo "Web pre-processing complete!"
echo ""
