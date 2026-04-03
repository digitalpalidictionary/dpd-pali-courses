#!/usr/bin/env bash
# Regenerate vocab/abbrev pages from dpd-db

set -e

echo "Regenerating vocab/abbrev pages from dpd-db..."
unset VIRTUAL_ENV 
cd /Users/deva/Documents/dpd-db

uv run python scripts/change_in_db/class_relation.py
uv run python scripts/export/vocab_abbrev_pali_course.py
