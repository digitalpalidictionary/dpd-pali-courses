# The verifier: `scripts/verify_key.py`

Registered in the root `README.md`. Read the source before relying on this page if it looks stale.

## Run
```
uv run python scripts/verify_key.py                       # structural checks, both courses; exit 0 required before any commit touching keys
uv run python scripts/verify_key.py --course bpc|ipc|all
uv run python scripts/verify_key.py --warnings            # also list word-coverage warnings (never affect exit code)
uv run python scripts/verify_key.py --course all --dpd --report temp/key_dpd_report.tsv
```
`--dpd [PATH]` checks every row against the local DPD SQLite DB (default
`/Users/deva/Documents/dpd-db/dpd.db`; local-only; advisory: never affects the exit code).
`--report` defaults to `temp/key_dpd_report.tsv` (git-ignored). Output is deterministic.

## Structural checks (gating, exit 1 on error)
Numbering vs the exercise files, POS vocabulary, Grammar vocabulary, root-cell format, compound-type
spelling (ipc), stray characters. A hand edit that breaks a tag format is caught here.

## DPD check and buckets (each key row gets one)
- `IMPOSSIBLE` — the key's tag is not among the DPD readings of the form (likely a real error).
- `NOT-FOUND` — the form is not in DPD.
- `ROOT-MISMATCH` — key root differs from the DPD root.
- `AMBIGUOUS` — tag is a valid DPD reading, but the form has other readings (gen/dat, nom/acc,
  gender only, …). Only the sentence can decide.
- `CONFIRMED` / `SKIPPED` — fine / not checkable (multi-alternative Grammar cells). Not reviewed.

## Report columns (TSV)
`row_key course file line section item occ word pos grammar root gloss sentence translation check bucket dpd_readings`
- `row_key` = `course/file/section/item/word/occ` (e.g. `ipc/16_class.md/main/4/aṅgāni/1`). It contains
  no tag, so it survives a tag correction. **Always key by `row_key`; `line` shifts after edits.**
- The same row can appear in two buckets, so a `row_key` may repeat in the report. Take the first occurrence.
- Course ranges: bpc classes 1–15, ipc classes 16–29.

## Key table format (what edits touch)
Row: `| word | pos | grammar | gloss | root |`. Gotchas:
- Word cell may be `\#word` or `**word**`; compare after stripping `\#` and `*`.
- Split cells on `|` (not ` | `): rows with an empty root cell end `| |`.
- Root cells use DPD style `√kar･7 \*e (do, make)`, not bare `√kar`.
- Causatives: POS `verb.caus`, grammar without "caus" (e.g. `opt.3rd.sg`).
- Keep `<br>` and backslash escapes verbatim; do not lose the trailing `|`.
