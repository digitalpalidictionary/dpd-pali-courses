# Track Handoff: verify_strict_20260327

## Current State
- Improved `normalize_text` and `extract_md_phrases` in `scripts/verify_strict.py`.
- Reduced false positives by handling diacritics, sandhi markers, and navigation anchors.
- Many mismatches still reported, especially for PDF (likely extraction artifacts).

## Blockers
- High volume of noise in `verify_strict.py` output makes it hard to find real data loss.

## Next Steps
1. Further refine `verify_strict.py` to handle list numbering differences and PDF extraction "glitches" (e.g. spaces in the middle of words).
2. Investigate specific "WEB MISSING" cases to see if they are real losses or just filtered content.
