# Handoff — SBS sync pre-existing (all tasks done; next is review)

## State

- All tasks 1.1–4.6 are [x]. Owner confirmed the `sāraṃ` residual (POS id 62423, `check` limitation) and that everything is as it should be. Next: `/kamma:3-review 20261126_sbs_sync_preexisting` in a fresh session.
- Not committed. The owner commits.

## What was done in Phase 4 (2026-11-26)

- `sbs_preexisting.py` gained `apply [--apply]` (backup, run stored commands, old-value re-check) and `final` (re-run `check`, compare with records, append counts to the proposals md).
- 1257 commands applied to dpd.db. Backup: `kamma/audit/scratch/sbs_backup_preexisting.json` (1258 rows). Log: `kamma/audit/scratch/sbs-sync-preexisting-apply.log`. The 14 leftover old-value hits are fragments inside longer SNP47 verse rows, not copies.
- Key edits (5 spots): `docs/bpc_key/13_class.md:32`, `docs/bpc_key/14_class.md` NP 7 block (one table), `docs/bpc_key/15_class.md:379`, `docs/ipc_key/18_class.md:169`, `docs/ipc_key/29_class.md:326` and `:415`. No `_ex` change needed. `verify_key.py` exit 0.
- Audit: removed bpc row `13_class.md:31` (MN20 `(simpl)`). Summary tables untouched, as in ffa1b5a0.

## Validation

- ruff, pyright, pyrefly clean on the script and test; `tests/test_sbs_preexisting.py` + `tests/test_sbs_sync.py`: 40 passed.
- Final `check` classes 2–29: TRANS 55, POS 162, PALI 43, ORPHAN 13, NO-SBS 26 (before: 271/168/48/14/27). Every remaining issue has a covering record except the `sāraṃ` residual, noted at the end of the proposals md and confirmed by the owner.
- `verify_rows.py`: bpc OK 27 / FAIL 249, ipc OK 46 / FAIL 288. PRE-EXISTING — NOT CAUSED BY THIS THREAD: stale audit line numbers (baseline 250/288).
- `git status --short docs/`: only the 5 key files above.

## Draft commit message

```
audit: sync pre-existing SBS ↔ key mismatches for classes 2–29

- Apply 1257 approved sbs_sync commands to dpd-db (translations, example fixes, 2 clears, 1 move, 1 replace, MN20 source)
- Edit 5 key spots: bpc 13 (simpl), bpc 14 NP 7 as one table, bpc 15 brackets, ipc 18 āvaraṇo adj (AN5.51 translation and its 5 SBS rows updated to match), ipc 29 abbatā adj
- Remove the resolved bpc audit row 13_class.md:31
- AGENTS.md: SBS search rule, translation-bracket rule, reserved ` / ` and `— ` rules (with kamma/tech.md)
- Remove the consumed sbs-sync-preexisting handoff draft

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
```

The commit should also `git rm kamma/draft/sbs-sync-preexisting-handoff.md` (consumed).

Note (review 2026-11-26): `kamma/audit/scratch/` and `tests/` are gitignored, so `sbs_preexisting.py`, `tests/test_sbs_preexisting.py`, the proposals JSON/md, the backup and the apply log are not part of any commit unless force-added (`git add -f`). The earlier draft line "Add the one-off sbs_preexisting.py … and its tests" was removed for that reason.

## Open / not in scope

- Changing `sbs_sync.py check` to use the AGENTS.md SBS search rule, and to handle a word that occurs twice in one sentence: candidate follow-up thread.
- NOTICED — NOT TOUCHING: `docs/ipc_key/18_class.md:170` `nīvaraṇo` is tagged `noun masc.nom.sg` like `āvaraṇo` was.
- Pre-existing dirty files not from this thread: `AGENTS.md`, `kamma/tech.md` (owner edits), `kamma/draft/course-edit-loop-draft.md`.
