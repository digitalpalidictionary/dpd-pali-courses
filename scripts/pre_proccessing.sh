#!/usr/bin/env bash

set -e

echo "Starting Pre-Processing for Pāḷi Courses build..."

echo "1. Generating/Updating mkdocs.yaml..."
uv run python scripts/generate_mkdocs_yaml.py

echo "2. Checking and correcting sentence numbering..."
uv run python scripts/check_renumber.py

echo "3. Re-ordering footnotes sequentially..."
uv run python scripts/renumber_footnotes.py

echo "4. Cleaning dead links..."
uv run python scripts/clean_dead_links.py

echo "5. Generating index pages..."
export PYTHONPATH=$PYTHONPATH:.
uv run python scripts/generate_indexes.py

echo "6. Updating CSS..."
uv run python scripts/update_css.py

echo "7. Verifying numbers..."
uv run python scripts/verify_numbering.py

echo ""
echo "All pre-processing complete!"
echo ""

