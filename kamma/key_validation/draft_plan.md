# Plan: BPC + IPC key sentence-level review (<DATE>)

Read `spec.md` and `kamma/key_validation/new_thread.md` first. Run on Sonnet; sub-agents `model: "sonnet"`.
Never run the full pytest suite. Do not run git.

## Phase 1 — Intake
- [ ] Regenerate the report: `uv run python scripts/verify_key.py --course all --dpd --report temp/key_dpd_report.tsv`
  → verify: exit 0; record bucket counts in Notes.

## Phase 2 — Small buckets (IMPOSSIBLE, NOT-FOUND, ROOT-MISMATCH)
- [ ] One sub-agent per course (prompt: `new_thread.md` §5) → `checklist_<course>.tsv` with header.
  → verify: `comm -3` of checklist vs report row_keys for these buckets is empty; verdicts ∈
  {CORRECT, FALSE-POSITIVE, CONFIRMED}; every CORRECT has new_pos and new_grammar.

## Phase 3 — AMBIGUOUS, per class file
- [ ] One sub-agent per class file (bpc 1–15, ipc 16–29; ≤4 parallel) → `parts/<course>_<N>_class.tsv`;
  merge into the checklists after each batch.
  → verify: rows per class = report AMBIGUOUS count for that class; no duplicate row_keys in the checklist.
- [ ] Full coverage check → verify: `comm -3` of report vs checklist row_keys is empty for both courses.

## Phase 4 — Approval files, then STOP
- [ ] Build `approval_bpc.md` / `approval_ipc.md` (CORRECT only).
  → verify: list-item count = CORRECT rows in the checklist.
- [ ] Present paths and counts. **STOP.** → verify: `git status --short docs/` is empty.

## Phase 5 — Apply (only after the user confirms the edited files)
- [ ] Apply each remaining item (method: `new_thread.md` §7).
  → verify: one changed line per item in `git diff --stat docs/`; only POS/Grammar/Root/gloss cells change.
- [ ] `uv run python scripts/verify_key.py` and `... --course all --dpd --report temp/key_dpd_report.tsv`.
  → verify: both exit 0; no applied row_key is IMPOSSIBLE (or each is reported).
- [ ] Tell the user the work is ready to commit; flag every interpreted or deviating item.

## Notes (fill during execution)
