## Thread
- **ID:** 20261126_sbs_sync_preexisting
- **Objective:** Resolve the SBS ↔ key mismatches for classes 2–29 that predate the audit commits (RULE/JUDGE gather, Pro verdicts, owner approval, apply).

## Files Changed
- `docs/bpc_key/13_class.md` — MN20 header gets `(simpl)` (#275)
- `docs/bpc_key/14_class.md` — NP 7 merged into one table, in-cell ` / or / ` alternatives, both readings as full sentences (#286)
- `docs/bpc_key/15_class.md` — `(What)`/`(what)` brackets in the translation (#304)
- `docs/ipc_key/18_class.md` — `āvaraṇo` noun → adj, gloss replaced with DPD āvaraṇa 1 gloss (#353)
- `docs/ipc_key/29_class.md` — `abbatā` noun fem → adj nt.instr.sg, two places (#513)
- `kamma/audit/bpc-key-audit.md` — removed the resolved row `13_class.md:31`
- `AGENTS.md` — SBS search rule and translation-bracket rule (from #46/#304); also the ` / ` and `— ` rules (owner edit, with `kamma/tech.md`)
- `kamma/audit/scratch/sbs_preexisting.py`, `tests/test_sbs_preexisting.py` — one-off script and tests (gitignored)
- dpd.db `sbs` table — 1257 commands (1253 set, 2 clear, 1 move, 1 replace)

## Findings
| # | Severity | Location | What | Why | Fix |
|---|----------|----------|------|-----|-----|
| 1 | minor | `kamma/threads/20261126_sbs_sync_preexisting/handoff.md` (draft commit msg) | The message said it adds the script and tests, but `kamma/audit/scratch/` and `tests/` are gitignored | The commit would describe files it does not contain | Fixed: line removed, note added |
| 2 | minor | `docs/ipc_key/18_class.md:169` | The #353 edit swaps the gloss `obstruction; obstacle; blockage; impediment` for the DPD adj gloss. The owner's recorded answer is only "key → adj" | Data-preservation principle: gloss text was dropped and the approval of that exact text is not recorded. The bold translation still reads "is an obstruction" | Resolved 2026-11-26: owner keeps the adj analysis; translation `18_class.md:178` → "ill will is an obstructing hindrance of the mind…", SBS ids 1344, 12998, 20450, 33690, 33691 synced (backup `kamma/audit/scratch/sbs_backup_an5_51.json`) |
| 3 | minor | `AGENTS.md` | The handoff lists AGENTS.md as "owner edits, not this thread", but plan 3.1 says the bracket rule from this thread was added there | Commit scope is unclear | Resolved 2026-11-26: owner commits AGENTS.md in full with this thread |
| 4 | nit | `sbs_preexisting.py:676-683` | `final` cuts everything after `## Final check`, which deletes the hand-added `sāraṃ` residual note (happened during review; restored from backup) | A re-run loses the note | Leave (one-off); the residual is also in plan 4.5 |
| 5 | nit | `sbs_preexisting.py:616-624` | `_issue_key`: unused `label` parameter, redundant `bold` regex | Dead code | Optional cleanup |
| 6 | nit | `plan.md` Phase 2 | The "MODEL SWITCH REQUIRED (Pro tier)" line appears twice | Noise | Optional |

## Fixes Applied
- Finding 1: draft commit message corrected in `handoff.md`.
- Restored `sbs-sync-preexisting-proposals.md` after the review's `final` re-run removed the residual note (finding 4).

## Test Evidence
- `uv run pytest tests/test_sbs_preexisting.py tests/test_sbs_sync.py` (scope: rule logic + sbs_sync unit tests) → 40 passed
- ruff check / ruff format --check / pyright / pyrefly (scope: script + test) → clean, 0 diagnostics
- `uv run python scripts/verify_key.py` (scope: whole bpc+ipc key/ex) → exit 0
- DB cross-check script (scope: all 1255 final `set` targets in the JSON vs dpd.db) → 0 mismatches. Every other change to backup rows maps to the 2 clears, the 1 move and the 1 replace; backup has 1258 unique ids
- `sbs_preexisting.py final` (scope: all key files, classes 2–29) → TRANS 55 / POS 162 / PALI 43 / ORPHAN 13 / NO-SBS 26; 1 uncovered (`sāraṃ` id 62423, owner-confirmed check limitation)
- `verify_rows.py` bpc → OK 27 / FAIL 249; ipc → OK 46 / FAIL 288 (pre-existing stale-line baseline 250/288, minus the 1 removed row)
- `coderabbit review --agent --base main --type uncommitted` (scope: tracked diff only; script/test are ignored and were not seen) → 0 findings
- #286 block: checked by hand. All 13 old rows, both readings and the second clause are kept; the merged rows match the 12-row exercise table

## Not Verified
- The linguistic correctness of the 239 RULE TRANS syncs and the Pro verdicts beyond the 5 key edits. Owner-approved; not re-judged here.
- `check` limits (fragment matches, first `(or)` only, multi-line bold), so counts are lower bounds as the spec states.
- `verify_rows.py` cannot exit 0 until the stale audit line numbers are refreshed (pre-existing; owner decision).
- Rendered web/PDF/DOCX output of the merged `14_class.md` table with ` / or / ` cells was not built.

## Verdict
PASSED (no blocking or major findings; findings 2 and 3 resolved by the owner; after the AN5.51 sync: no old text left in sbs, `check` shows no issue on the sentence, `verify_key.py` exit 0)
- Review date: 2026-11-26
- Reviewer: Claude Opus 5.5 (fresh session, Claude Code)
