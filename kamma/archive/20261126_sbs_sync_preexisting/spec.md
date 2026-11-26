# Spec: SBS ↔ key sync — mismatches that predate the audit commits

Source handoff: `kamma/draft/sbs-sync-preexisting-handoff.md` (2026-11-26).

## Overview

The SBS table in dpd-db (`sbs.class_*`, `class_anki` = class number 1–29) feeds the Anki decks and other exports and must match the course keys (`docs/bpc_key/`, `docs/ipc_key/`). Most important: each key sentence's bold translation must equal `class_example_translation` on every SBS row that carries that sentence.

The mismatches added by commits `d35b4299` (bpc key) and `b4df24ea` (ipc key) are already fixed (groups A/B/C1 in `kamma/audit/scratch/sbs-sync-proposals.md`, applied 2026-11-26). This thread handles the rest: mismatches that were there before those commits.

Tool: `kamma/audit/scripts/sbs_sync.py` (README → Course Audits). DB path from `$DPD_DB`, default `/Users/deva/Documents/dpd-db/dpd.db`. `set`, `replace`, `move` and `clear` are dry runs until `--apply`. `check <key file> [--only KIND…]` compares one key file with the `class_*` rows of its class.

## Current counts (verified 2026-11-26, `check` over all 29 key files, after commit ffa1b5a0)

| Kind | All | In scope (class 1 excluded) |
| --- | --- | --- |
| TRANS: key translation ≠ `class_example_translation` | 271 | 271 (152 differ only in diacritics, punctuation, `[ ]`/`( )` or case; 12 have more than one differing DB value) |
| PALI: SBS sentence is a ≥ 85 % spelling variant of a key sentence | 48 | 48 |
| POS: DPD pos of the bold headword ≠ key POS column | 168 | 168 (79 flagged "DPD example = this sentence: question the key") |
| ORPHAN: SBS sentence of class N not found in key N | 37 | 14 (class 2: 11, classes 3/5/8: 1 each) |
| NO-SBS: key sentence with no SBS row | 28 | 27 |

The most common POS pairs (DPD vs key): pp/adj 45, adj/noun 19, sandhi/ind 15, idiom/ind 11, ptp/adj 8.

## What it should do

Four stages: one switch to the Pro model and back, and one owner approval.

**Stage 1: Gather (Fast).** Run the `check` logic over the key files for classes 2–29 and split every finding into "decided by rule" (RULE) and "needs judgment" (JUDGE). Results: a JSON file `kamma/audit/scratch/sbs-sync-preexisting-proposals.json` (source of truth) and a rendered `kamma/audit/scratch/sbs-sync-preexisting-proposals.md` for the owner.

- TRANS is RULE when SBS differs from the key only in diacritics, punctuation, `[ ]`/`( )` or case, **and** the key is the fuller form (the key has the diacritics or brackets that SBS lacks). Proposed change: SBS → key text. Everything else is JUDGE, including the reverse case where SBS has the diacritics and the key does not.
- POS is RULE ("no conflict", verdict `leave`) when:
  - DPD has `pp`/`ptp`/`prp` and the key has `adj`;
  - the key POS contains `sandhi`;
  - the key has `ind adv` and DPD has `adj`.

  All other POS items are JUDGE. The 79 items flagged "DPD example" keep that flag.
- PALI, ORPHAN and NO-SBS are always JUDGE.
- **Audit cross-check.** For each finding, record the open rows in `kamma/audit/bpc-key-audit.md` / `kamma/audit/ipc-key-audit.md` whose Location names the same key file and a line from the start of the sentence's Pāli block to its bold translation line. A finding that would be RULE but has such audit rows becomes JUDGE: the key at that spot is still under review.
- Evidence attached to JUDGE items:
  - all items: key location, SBS ids, both texts;
  - ORPHAN: the closest key sentence in the same class;
  - POS: `kamma/audit/scripts/dpd_lookup.py <word> --sentence "<key sentence>"` output.

**Stage 2: Decide (Pro, once).** Pro sets a verdict and a short reason for each JUDGE item only. It does not re-check RULE items.

- Verdicts: `SBS→key` / `key→SBS` (a key edit + `docs/*_ex` sync) / `move` / `clear` / `leave` / `gap` (NO-SBS only).
- Default: the key is right, because the audits corrected it and SBS was copied from an older key.
- Owner rule (`kamma/audit/audit-guide.md` step 2): if a DPD headword quotes the key sentence in `example_1`/`example_2`, that is strong evidence for that headword's reading. Change the key only for a real grammatical error.
- PALI compound cards (the bold is a compound headword that the key writes split, e.g. AN10.48 `alam'ariyañāṇadassanaviseso`): `leave`, marked "owner decides".
- Items with open audit rows: either adopt the audit's suggestion as the target text, or `leave` with "pending audit row <loc>". Never sync SBS to a key text that an open audit row wants changed without saying so. (As decided in Phase 2: a third option is used, syncing SBS to the current key with a reason that names the audit row and says to re-sync after it is resolved; see plan 2.1.)
- NO-SBS: `gap` only where a word is really missing. Skip intentional ones, where every word was marked in an earlier class or the line is a short question such as "katame pañca?".

**Stage 3: Owner approval.** The owner reviews the whole `.md` (RULE batch groups plus the Pro verdicts) and approves, edits or rejects rows. Batch approvals are allowed. This is the only stop.

**Stage 4: Apply (Fast).** Approved rows only.

1. Back up the full `sbs` rows of every touched id to JSON.
2. Run the stored `sbs_sync.py` commands with `--apply`.
3. Make the key and `docs/*_ex` edits for the `key→SBS` rows, and remove the audit rows those edits resolve (following commit ffa1b5a0).
4. Re-check every row of the same class+source for the old value. Spelling variants and `<b>`-split rows are not grouped together, so this check catches rows the commands missed.
5. Re-run `check` and record the final counts.

## Assumptions & uncertainties

- Verified this session:
  - the counts above;
  - the `sbs_sync.py` commands and their behaviour (source read);
  - `check_key`/`main` can be reused through `importlib`, as `tests/test_sbs_sync.py` does;
  - the class 1 breakdown;
  - the owner rule text;
  - the `sqlite3` CLI is available (3.54, supports `-json`);
  - the dpd-example-match prerequisite is done (commit ffa1b5a0);
  - the `verify_rows.py` roots are `docs/bpc_key` / `docs/ipc_key`.
- `check` limits:
  - only exact or variant matches have their translation compared; 62 fragment matches are POS-checked only;
  - only the first "**(or)**" alternative is compared;
  - partly bolded compound members are not POS-checked.

  The counts are lower bounds, and "done" means done within what `check` sees.
- Found in Phase 2 (2026-11-26):
  - **The audit Location line numbers are stale.** `verify_rows.py` gives bpc FAIL 250 / ipc FAIL 288 now, against bpc FAIL 2 at the audit commit 0b91870d. So the audit cross-check has to locate each row by its `Current` excerpt, not by the cited line (plan task 1.5). This failure predates the thread, so `verify_rows.py` cannot exit 0 in task 4.4 until the owner decides whether to refresh the audit line numbers.
  - **`check` also compares too little text in three more cases.** It reads only the first bold line, so it misses: translations that run over several bold lines (verses, `Lit:`/`Fig:`, `(or)`); split sentences, which it joins with no punctuation between the parts; and IPC items where bold construction lines (`√… + …`) come before the translation. Here SBS often already holds the full text. Verdicts for these records use `key_text_full`, and their reason starts with `check limitation:`, because `check` will still flag them after the sync.
- The direction test (counting combining marks and brackets) may miss a mixed case where the key is poorer on one word and richer on another. RULE rows still go through owner approval.
- The share of real conflicts in POS and ORPHAN is unknown until reviewed.
- If the key changes before Stage 1 runs, the counts will differ. Stage 1 quotes whatever `check` reports at that time.
- The Summary table in the audit files is labelled "numbers before approval". The assumption is that it is not updated. Task 4.4 reads the ffa1b5a0 diff and follows what that commit did.

## Constraints

- Never write to dpd-db without the owner's approval of the exact rows. Only `dpd.db` is written. dpd-db's own uncommitted files (`AGENTS.md`, `db_tests/dps_internal_tests.tsv`, `gui2/data/*`, `kamma/lessons.md`, `misc/pat-bi/`) are not touched.
- Pro only analyses and decides: no `--apply`, no `docs/` edits. All writes are done by Fast.
- `sbs_sync.py` is not changed.
- A key change must also be made in `docs/*_ex` (golden rule in `kamma/audit/*-key-audit.md`). `uv run python scripts/verify_key.py` must exit 0 before any commit that touches key/ex. Never remove data from `docs/`.
- No commits by the agent. Prepare a draft commit message; the owner commits.
- Before reporting done, check `git status --short docs/` and keep exporter changes in `docs/generated/` out of scope.

## How we'll know it's done

- Every finding for classes 2–29 is one of: applied, owner `no`, `leave` (with a reason) or `gap` (NO-SBS report).
- The final `check` run shows no issue that lacks such a record.
- A backup JSON exists for the applied batch, and the post-write class+source re-check finds no old values.
- If the key changed:
  - `verify_key.py` exits 0;
  - `_ex` is in sync;
  - resolved audit rows are removed;
  - `verify_rows.py` passes on both key audits.
- The new script's test passes, and ruff/pyright/pyrefly are clean.

## What's not included

- SBS class 1, all kinds (its 23 ORPHANs and 1 NO-SBS).
- Changes to `sbs_sync.py` or the `check` logic.
- Creating SBS rows for NO-SBS gaps (report only).
- Changes to DPD headwords (at most suggested in the report).
- `kamma/audit/ipc-audit.md` (it covers the IPC lessons, not the key).
