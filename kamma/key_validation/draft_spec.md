# Spec: BPC + IPC key sentence-level review (<DATE>)

## Overview
`scripts/verify_key.py --dpd` checks every POS/Grammar/Root tag in `docs/bpc_key/` and `docs/ipc_key/`
against DPD. Rows DPD cannot settle alone fall in four buckets (IMPOSSIBLE, NOT-FOUND, ROOT-MISMATCH,
AMBIGUOUS; definitions in `kamma/key_validation/verifier.md`). This thread gives each row a verdict against
its sentence and translation, shows the user **only definite errors** in an approval file, stops, and after
the user confirms applies exactly the items left in it.

## Input
- Report `temp/key_dpd_report.tsv`, regenerated with
  `uv run python scripts/verify_key.py --course all --dpd --report temp/key_dpd_report.tsv`.
- Bucket counts at start (fill in): bpc IMPOSSIBLE <n> / NOT-FOUND <n> / ROOT-MISMATCH <n> / AMBIGUOUS <n>;
  ipc IMPOSSIBLE <n> / NOT-FOUND <n> / ROOT-MISMATCH <n> / AMBIGUOUS <n>.
- Columns and `row_key` semantics: `kamma/key_validation/verifier.md`.

## What it should do
1. Review all four buckets for both courses: small buckets first, then AMBIGUOUS one class file at a time.
2. Verdicts, decided from sentence, translation, gloss and DPD readings:
   - `CONFIRMED` — the key tag is a valid reading in context. Includes every case where several readings
     fit or the context is not decisive. **When in doubt: CONFIRMED.**
   - `CORRECT` — definite error; give new POS/Grammar (Root/gloss only if the row needs it) + one-line reason.
   - `FALSE-POSITIVE` — small buckets only: key right, DPD or the verifier's matching is the gap.
   - A clearly wrong translation: reason prefixed `TRANSLATION:` (report only, never fixed).
   There is no UNDECIDED verdict and no notes file: the user wants errors only.
3. Checklists (complete record for coverage): `checklist_bpc.tsv`, `checklist_ipc.tsv` in the thread folder,
   UTF-8 TSV with header: `row_key bucket word pos grammar verdict new_pos new_grammar new_root new_gloss reason`.
4. Approval files `approval_bpc.md`, `approval_ipc.md` (format: `kamma/key_validation/new_thread.md` §6):
   CORRECT items only, grouped by class file in numeric order.
5. **STOP** after both approval files exist; hand them to the user.
6. The user deletes rejected items, may edit targets, then confirms.
7. Apply every remaining item as in-place cell edits on that row only (method: `new_thread.md` §7).

## Decisions
- Review every row, not a sample (no safe subset exists in AMBIGUOUS).
- Checklists and approval files live in the thread folder.
- Gloss edits only as an explicit `gloss:` part of a CORRECT item.
- Sonnet throughout; sub-agents pinned `model: "sonnet"` explicitly.
- No new scripts: awk/comm for packets and coverage, a throwaway scratchpad script for applying.

## Constraints
- Data preservation: in-place cell edits only; never delete rows, Pāli or translations.
- Only `docs/bpc_key/*.md`, `docs/ipc_key/*.md` and the thread's own files change — not `*_ex/`,
  `bpc_hi_key/`, `scripts/verify_key.py`.
- Clean Markdown: keep `<br>` and escapes verbatim.
- Nothing in `docs/` changes before the user confirms the edited approval files.
- `uv run python scripts/verify_key.py` must exit 0 before any commit touching the keys.

## How we'll know it's done
- Every report `row_key` has exactly one checklist row (`comm -3` empty).
- Changed table rows in `git diff` = number of approved items; no other cells change.
- Final verifier and `--dpd` runs exit 0; no applied `row_key` reports IMPOSSIBLE (or each exception is reported).

## Not included
Verifier changes; word-coverage warnings; SKIPPED rows; translation fixes; Hindi key mirroring.
