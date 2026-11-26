# Plan: SBS ↔ key sync — pre-existing mismatches

Spec: `kamma/threads/20261126_sbs_sync_preexisting/spec.md`. Source handoff: `kamma/draft/sbs-sync-preexisting-handoff.md`.

## Architecture Decisions

- **One thread script**, `kamma/audit/scratch/sbs_preexisting.py`, with three subcommands: `gather`, `render` and `apply`.
  - It loads `kamma/audit/scripts/sbs_sync.py` with `importlib.util.spec_from_file_location`, the same way `tests/test_sbs_sync.py` does, and reuses `check_key`, `parse_key`, `norm`, `norm_tr`, `connect` and `main`.
  - No parsing of `check` text output and no `sys.path` hacks.
  - It is a one-off, so it is not added to the README script registry.
- **JSON is the source of truth**: `kamma/audit/scratch/sbs-sync-preexisting-proposals.json`, one record per finding. The `.md` is generated from it for the owner to read. Pro edits verdicts only in the JSON, then re-renders.
- **Commands stored per record** as `sbs_sync.py` argv lists, so `apply` runs exactly what was approved, through `sbs_sync.main(argv)`.
- **`sbs_sync.py` is not changed** (out of scope).
- The test covers only the risky rule logic: the TRANS direction test, the POS no-conflict filter and the audit-row demotion.

## Model Strategy

| Phase | Tier | Reason |
| --- | --- | --- |
| 1 Gather | Fast | script, checks, evidence collection |
| 2 Decide | Pro | linguistic verdicts on JUDGE items only |
| 3 Owner approval | (none) | owner reviews; agent records the answers |
| 4 Apply | Fast | backups, `--apply` writes, key/_ex/audit edits, verification |

## Phase 1 — Gather — *Fast*

- [x] 1.1 Write `kamma/audit/scratch/sbs_preexisting.py gather`. Start the file with a one-sentence purpose docstring.
  - Files: `docs/bpc_key/[0-9]*_class.md` and `docs/ipc_key/[0-9]*_class.md`. Skip class 1. Call `check_key(con, text, cls, label)` for each.
  - One record per Issue: `{n, kind, cls, key_loc, ids, key_text, db_texts, dpd_example_flag, audit_rows, group: "RULE"|"JUDGE", verdict, reason, commands, key_edit, owner: ""}`.
  - TRANS RULE: every db value equals the key after stripping diacritics (NFD, drop combining marks), punctuation, `[]()` and case, **and** the key is not poorer. "Poorer" means fewer combining marks than the db value, or fewer `[`/`(` characters.
    - Verdict `SBS→key`.
    - Commands: one `["set", id, "class_example_translation=<key text>"]` per id, where key text = `norm_tr` of the key bold line.
    - Every other TRANS is JUDGE.
  - POS RULE (verdict `leave`):
    - DPD pos ∈ {pp, ptp, prp} and the key has `adj`;
    - or the key POS contains `sandhi`;
    - or the key has `ind adv` and DPD has `adj`.

    Every other POS is JUDGE. Set `dpd_example_flag` when the message has "DPD example = this sentence".
  - PALI, ORPHAN and NO-SBS are JUDGE.
  - `audit_rows`: the open rows in `kamma/audit/bpc-key-audit.md` / `kamma/audit/ipc-key-audit.md` whose Location (`N_class.md:line[,line…]`) names the same file and a line from the start of the sentence's Pāli block to its bold translation line (both computed from the key file). A would-be RULE record with `audit_rows` becomes JUDGE.
  - Evidence for JUDGE:
    - ORPHAN: the closest key sentence in the same class (`difflib` best ratio) and its line;
    - POS: the output of `uv run python kamma/audit/scripts/dpd_lookup.py <bold word> --sentence "<key pāli>"`.

  → verify: run `uv run python kamma/audit/scratch/sbs_preexisting.py gather`, then print the record counts per kind. Expected: TRANS 271, PALI 48, POS 168, ORPHAN 14, NO-SBS 27. If the key has changed, these must equal the current `sbs_sync.py check` totals for classes 2–29; quote both.
- [x] 1.2 Add `tests/test_sbs_preexisting.py`, with one test per branch:
  - key "Ānanda" vs db "Ananda" → RULE;
  - key "Ananda" vs db "Ānanda" → JUDGE;
  - a punctuation-only difference → RULE;
  - a wording difference → JUDGE;
  - pp/adj → RULE leave;
  - noun/adj → JUDGE;
  - an audit row citing a line inside the sentence → JUDGE.

  → verify: `uv run pytest tests/test_sbs_preexisting.py -v`, all pass. Each test fails if its rule branch is removed.
- [x] 1.3 Add `render`: JSON → `kamma/audit/scratch/sbs-sync-preexisting-proposals.md`.
  - At the top: the RULE/JUDGE split per kind.
  - One section per kind: RULE rows in a batch table, then JUDGE rows.
  - Columns: #, key location, SBS ids, change (~~old~~ **new**), audit rows, verdict, reason, owner.
  → verify: the row count in the md equals the record count in the JSON (`grep -c '^| [0-9]'` vs `jq length`).
- [x] 1.4 Phase check: run `uv run ruff check --fix`, `uv run ruff format`, `uv run pyright` and `uv run --with pyrefly pyrefly check --min-severity warn` on the script and the test.
  → verify: all four report 0 errors and 0 warnings.

### Phase 1b — Re-anchor audit rows — *Fast* (added 2026-11-26 by Pro, see handoff)

⚠️ MODEL SWITCH REQUIRED (Fast tier): Pro found that the audit Location line numbers are stale, so the 1.1 cross-check attaches audit rows to the wrong sentences.

PRE-EXISTING — NOT CAUSED BY THIS THREAD: `verify_rows.py` on the key audits: bpc OK 27 / FAIL 250, ipc OK 46 / FAIL 288. At the audit commit 0b91870d bpc was OK 486 / FAIL 2. Later key edits (94fbacdc `<br>` cleanup, d35b4299, d01f73c1, ffa1b5a0) moved the lines. Example: the `8_class.md:560` row (`that monk can set [it] aside…`) is now at line 590, so gather attached it to DN22.18 (#125) and not to VIN PAT NP 3 (#129).

- [x] 1.5 Re-anchor the audit rows by their excerpts in `gather`.
  - For each open audit row, take the backtick excerpts from the `Current` cell (`\|` → `|`). Find each excerpt in the cited key file and use the line of the occurrence nearest the cited line. Keep the cited line only when no excerpt is found, and mark that row `"stale": true`.
  - Keep the full `Problem`/`Suggested` text in `audit_rows` (no 140-character cut), so Pro can judge whether a row targets the bold translation.
  - Add `key_text_full` to TRANS records: all bold lines after the table up to the next non-bold line, joined with a space, through `norm_tr`. Skip bold construction lines (they contain `√`, ` + `, `\>` or `\<`, or end in `bahubbīhi)`). For a split sentence (the record's `key_text` is longer than its first bold line) use `key_text`.
  - Re-run `gather` (it overwrites the JSON; no verdicts have been set yet), then `render`.
  - Add one test: an audit row with a stale line number whose excerpt sits inside a sentence's span is attached to that sentence.

  → verify: `uv run pytest tests/test_sbs_preexisting.py -v` passes. Print the RULE/JUDGE counts per kind and the number of records whose `audit_rows` changed against the old JSON (keep a copy before re-running). `jq` check: #129 (VIN PAT NP 3, 8_class.md:572) now has the `8_class.md:560` row and #125 does not. Report the number of `stale` rows. Run ruff/pyright/pyrefly on both files again.

## Phase 2 — Decide — *Pro*

⚠️ MODEL SWITCH REQUIRED (Pro tier): verdicts on the JUDGE items, after 1.5.

⚠️ MODEL SWITCH REQUIRED (Pro tier): verdicts on the JUDGE items.

- [x] 2.1 For every JUDGE record, set `verdict`, `reason` (one line) and `commands` or `key_edit`.
  - Verdicts:
    - `SBS→key`: `set`/`replace` commands.
    - `key→SBS`: no commands. `key_edit: {file, line, old, new}` plus the matching `docs/*_ex` line, and the SBS commands for the new text if the key's new text differs from the SBS text.
    - `move a b`, `clear`, `leave`, `gap` (NO-SBS only).
  - Default: the key is right.
  - POS items with `dpd_example_flag`: apply the owner rule in `kamma/audit/audit-guide.md` step 2.
  - PALI compound cards (bold = a compound headword the key writes split): `leave`, marked "owner decides".
  - Records with `audit_rows`: either adopt the audit's suggestion as the target text, or `leave` with "pending audit row <loc>".
  - *As done (2026-11-26):* no audit suggestion was adopted (no `key_edit` records). Where the audit row targets the translation but SBS is not closer to the audit's wording, the record is `SBS→key` to the current key and the reason says "open audit row <loc> targets this translation: … re-sync after it is resolved". `leave` + "pending audit row" is used only where SBS already holds what the audit asks for (e.g. #21, #45, #117, #129) or the key line carries an audit-flagged note (#360, #405).
  - *As done:* POS cards on the wrong headword: `clear` where the right headword already has the same card (#50, #172), `move` where it has none (#407), `leave` where it already holds another class's card (#106, #274, #491). PALI text fixes use `set class_example=…` with the bold kept, or `replace` (#439).
  - Check every Pāli claim with `kamma/audit/scripts/dpd_lookup.py`.
  - Do not touch RULE records. Run no `--apply`. Make no `docs/` edits.

  → verify: `jq '[.[] | select(.group=="JUDGE" and .verdict=="")] | length'` = 0, then re-run `render`.
- [x] 2.2 Phase check:
  - every record whose verdict is not `leave`/`gap` has non-empty `commands` or `key_edit`;
  - every `move` passes a dry run (`uv run python kamma/audit/scripts/sbs_sync.py move a b` without `--apply` does not refuse).

  → verify: a `jq` query for records missing both returns 0, and the dry-run log has no `!!` lines.

## Phase 3 — Owner approval — *(no model work)*

⚠️ MODEL SWITCH REQUIRED (Fast tier): mechanical execution resumes after this phase.

- [x] 3.1 STOP. Give the owner the path to `kamma/audit/scratch/sbs-sync-preexisting-proposals.md` and the summary counts. Record each answer in `owner`: `ok`, `no`, or an edited value (an edit also updates `commands`/`key_edit`). Batch-group approvals are allowed (e.g. "RULE TRANS: ok").
  - *Added 2026-11-26 at the owner's request:* every record has `confidence` (high/medium) and `review` (B1/B2/B3 batch tag or the medium-confidence doubt). Short review file: `kamma/audit/scratch/sbs-sync-preexisting-review.md`: high batch (374), batch questions B1 (79 audit re-syncs), B2 (42 compound cards), B3 (12 SBS-only drills), and 21 medium records to inspect.
  - *Owner answers (2026-11-26):* High ok; B1 sync; B2 ok; B3 ok; medium agreed except: #46 not a gap (abhinandi 1 already carded, class 4); #275 key right as (simpl): SBS gets the key text + source `MN20 (simpl)`, key header gets `(simpl)`; #304 keep brackets: key edit; #353 key → adj; #513 key → adj (case `nt.instr.sg` proposed by Pro, as `añāṇā`). `key_edit` is a **list** of `{file, line, old, new, ex}` (or `{file, start, end, old, new, ex, note}` for a block); the line edits have no `_ex` counterpart (ex has no translations / empty grammar cells, ex 13 already has `(simpl)`). Follow-up answers: #32/#304 follow the bracket rule (now in `AGENTS.md`); NP 7 (#286, block edit on `docs/bpc_key/14_class.md:578–606`) becomes one table with the alternative in-cell like `bpc_key/10_class.md:377`, noun reading first, both readings as full sentences in that order, no data dropped; the exercise already has the single 12-row table.
  → verify: `jq '[.[] | select(.owner=="")] | length'` = 0, then re-render. Done: 0 empty.

## Phase 4 — Apply — *Fast*

- [x] 4.1 Add `apply [--apply]`. It acts on records where `owner` ≠ `no` and `commands` is non-empty, in three steps:
  - (a) Dump the full `sbs` rows of every touched id to `kamma/audit/scratch/sbs_backup_preexisting.json`. Refuse to overwrite an existing file.
  - (b) Run each command through `sbs_sync.main(argv)`, adding `--apply` only when the flag is given.
  - (c) After writing, for each changed field, run `find "<old value>" --class N --source S` and list the rows still holding the old value.

  → verify: the dry run prints every command, has no `!!` lines and writes no backup.
- [x] 4.2 Run `uv run python kamma/audit/scratch/sbs_preexisting.py apply --apply`.
  → verify:
  - the backup JSON has one entry per touched id;
  - the step (c) report is empty, or every hit is explained as an unrelated short-string match;
  - `sqlite3 "$DPD_DB" "select class_example_translation from sbs where id=<id>"` shows the new text for 3 sampled ids.
- [x] 4.3 Apply the approved `key_edit` records: edit `docs/bpc_key`/`docs/ipc_key` and the matching `docs/bpc_ex`/`docs/ipc_ex` line. Never delete data.
  → verify: `uv run python scripts/verify_key.py` exits 0.
- [x] 4.4 Remove the audit rows that the applied key edits resolve. Follow commit ffa1b5a0: read `git show ffa1b5a0 -- kamma/audit/bpc-key-audit.md kamma/audit/ipc-key-audit.md` first and update the same sections it updated. Log item moves under "Item moves (main ↔ Extra)".
  → verify (exit 0 is impossible until the owner decides about the stale audit lines; see 1b):
  - `uv run python kamma/audit/scripts/verify_rows.py docs/bpc_key kamma/audit/bpc-key-audit.md`: no failures beyond the pre-existing baseline (OK 27 / FAIL 250, minus the rows removed);
  - `uv run python kamma/audit/scripts/verify_rows.py docs/ipc_key kamma/audit/ipc-key-audit.md`: same, baseline OK 46 / FAIL 288;
  - no removed row is still cited in the proposals md.
- [x] 4.5 Final check: re-run `check` for classes 2–29 and write the final counts per kind into the md.
  → verify: a script compares the remaining issue ids against the records with owner `no`, verdict `leave`/`gap`, or a reason that starts with `check limitation:` (the record was synced to `key_text_full`, which `check` cannot see); the difference is empty.
- [x] 4.6 Wrap up.
  - Run ruff/pyright/pyrefly and `uv run pytest tests/test_sbs_preexisting.py -v` on the touched Python again.
  - Run `git status --short docs/` and leave the `docs/generated/` exporter changes out.
  - Draft a commit message (the owner commits). It includes deleting the consumed `kamma/draft/sbs-sync-preexisting-handoff.md`.

  → verify: all checks pass, and `git status` shows only the thread's files, the scratch outputs and the approved key/_ex/audit edits.

### Phase 4 results (2026-11-26)

- 4.2: 1257 commands applied, backup `kamma/audit/scratch/sbs_backup_preexisting.json` (1258 rows). The old-value re-check found 14 hits, all substring matches inside longer SNP47 verse rows (no exact or normalised copy); log `kamma/audit/scratch/sbs-sync-preexisting-apply.log`.
- 4.3: 5 key edits (13_class:32, 14_class NP 7 block, 15_class:379, ipc 18_class:169, ipc 29_class:326, :415); `verify_key.py` exit 0; no `_ex` change needed.
- 4.4: removed 1 audit row (bpc `13_class.md:31` MN20 `(simpl)`). `verify_rows.py` bpc OK 27 / FAIL 249 (baseline 250), ipc OK 46 / FAIL 288 (baseline). Summary tables untouched, as in ffa1b5a0.
- 4.5: `final` subcommand. Remaining: TRANS 55, POS 162, PALI 43, ORPHAN 13, NO-SBS 26 (was 271/168/48/14/27). One issue has no record: POS id 62423 `sāraṃ`, a `check` limitation (same word twice in the sentence) exposed by #206; noted in the md, owner to confirm.
- Post-review (owner request 2026-11-26): refreshed the `Location` and in-prose line numbers of `bpc-key-audit.md` and `ipc-key-audit.md` (line diff from key rev 0b91870d, then excerpt re-anchor; only digits changed). `verify_rows.py` now bpc OK 234 / FAIL 42, ipc OK 298 / FAIL 36; all remaining failures are `NOT FOUND` (excerpt text drift such as removed `<br>`, renumbered footnotes), not line numbers. Removed the `## Summary` table from `bpc-key-audit.md`, `ipc-key-audit.md` and `ipc-audit.md` (the "Overall confidence" paragraph is kept). `ipc-audit.md` line numbers left as they were (OK 446 / FAIL 38, mostly text drift).

