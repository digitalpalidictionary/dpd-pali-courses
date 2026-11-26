# Course edit guide

The single home for every rule and step of an owner-requested change to course material. Other files point here. Entry point for agents: the `edit-all` skill (`.claude/skills/edit-all/SKILL.md`, local) and AGENTS.md → Course Edits.

## Scope

- English folders only: `docs/bpc*` and `docs/ipc*`. Hindi (`bpc_hi*`) is always out of scope; never ask whether to include it.
- One edit = one owner request. It may touch several sentences.
- Never write DPD headwords; a needed DPD change is only a suggestion listed for the owner. The SBS table is the only part of dpd-db an edit writes.
- Use this guide for: a key row, an exercise row, a translation, a lesson-page fix, an item moved between main and Extra, the SBS sync of any such change, and applying approved audit fixes.
- Edits come in large numbers. Never read past edits; read only the four files named in the next section.

## Start of session

1. Read `kamma/edits/guide.md` (this file), `kamma/edits/handoff.md`, `kamma/edits/learnings.md` and `kamma/edits/improvements.md`. Nothing else. Never read `kamma/edits/history/`: it is a write-only log.
2. If `improvements.md` lists any open points, or `handoff.md` has lines under "Noticed in docs/", start your first reply with a short warning that names them (one line each). It is only a warning: carry on with the edit unless the owner says to work on a point now.
3. If `handoff.md` is not empty, resume from it (open request, current step, approval, pre-apply rev). Otherwise start a new edit at Step 1.
4. Clean old backups (skip if `kamma/edits/backups/` does not exist, or if the handoff names a backup): delete SBS backups a month (30 days) old or older: `find kamma/edits/backups -name 'sbs_backup_edit_*.json' -mtime +29 -print -delete`.

## Places a change can touch

Check every place for every edit.

| Place | What must match |
| --- | --- |
| `docs/bpc_key/`, `docs/ipc_key/` | the analysis row (POS, grammar, gloss, root), the Pāli sentence line, the bold translation |
| `docs/bpc_ex/` | the same sentence; prefilled cells only. Empty cells stay empty; deliberate prefills for material not yet covered stay. |
| `docs/ipc_ex/` | no grammar prefills, but tables and sentences that must match the key |
| `docs/bpc/`, `docs/ipc/` (lesson pages) | a fix made there: check the matching ex and key. Key sentences are not quoted verbatim in lesson pages (verified 0/409 BPC, 0/258 IPC), so for a key edit change lesson pages only if the request names them. |
| SBS table in dpd-db | `class_*` fields (sentence, translation, the headword the example sits on), `class_anki` = class number, `class_extra` (Extra flag) |
| `docs/generated/` | never edit by hand: exporter output |

## Rules

### Rules that live only here

**Exercise sync.** Key and exercise must stay in sync: always correct the corresponding sentences and tables in the exercise folder (`docs/bpc_ex/` or `docs/ipc_ex/`), and in the key too when the change started in a lesson page.
- BPC: the exercise also has some prefilled values in the grammatical analysis. Keep the prefilled values that were deliberately chosen for material not yet covered at the time of that sentence. When you change some grammar in the key, double-check whether the exercise has that grammar prefilled too; if so, correct it and sync it with the key.
- IPC: the exercise has no grammatical analysis, but it still has tables, and something from the change may be relevant there.

**SBS sync.** Every key sentence is also stored in the SBS table of dpd-db (`class_*` fields, `class_anki` = class number), which feeds Anki and the other exports, so the SBS table must correspond to the key. When an edit changes a key sentence's translation (SBS column `class_example_translation`), its Pāli text (`class_example`), or the POS/headword of a word (e.g. noun → adj/pp, a separate DPD row), find and update the SBS rows with `uv run python kamma/edits/scripts/sbs_sync.py` (`check <key file> --since <rev>` lists what the edit put out of sync; `replace`, `set`, `move`, `clear` change the DB and are a dry run until `--apply`). Get the owner's approval before writing to the DB.

**SBS write safety.** Back up the touched rows first. After writing to the SBS table, re-check every row of the same class + source for the old value (spelling variants and `<b>`-split rows are not grouped together).

**Not in SBS.** SBS may card a key word with a different inflected form, in a different sentence, under the word's DPD headword. A search for the key's exact form then finds nothing although the word is carded. So before calling a key word "not in SBS", search `class_example`/`class_source` in every class for its other forms (`sbs_sync.py find "<stem>"`) and look up its headword (`sbs_sync.py show "<headword>"`), not only the exact bold form. Example of the principle: the key form `abhinanduṃ` (`docs/bpc_key/4_class.md`) gives 0 rows with `find abhinanduṃ`, but the word is carded under the headword `abhinandi 1` with the form `abhinandi` ("āyasmā rāhulo bhagavato bhāsitaṃ abhinandi", class 4).

**Analysis and translation tell one story.** The table gloss follows DPD (the meaning of the chosen headword) and always carries the word's declension or conjugation (e.g. gen "of you; your"). The bold translation may be freer (synonyms, figurative wording). What must agree is the reading: the chosen headword and meaning, and the grammar (case, number, tense, person, construction).
- When an edit changes the reading in the table (another headword or meaning, or other grammar, e.g. dat → gen), change the gloss to carry it and change the translation to match.
- When an edit changes the translation so that it implies a different reading, change the table rows to match, using the DPD gloss of the new headword in the new grammar.
- A change of wording alone (a synonym within the same headword and grammar), on either side, needs no change on the other side.

A changed translation then goes to SBS too (see SBS sync). Past case that led to this rule: in `docs/ipc_key/27_class.md` `vo` was re-read as the pronoun "your" (2nd.gen.pl) instead of "surely", but the translation kept "surely".

**Moving an item between main and Extra.** When an approved edit moves an exercise item from the main list to `## Class N Extra` or back (e.g. it turns out to be an irregular case):

1. Move the whole item (header line with its link, Pāli line, table, bold translation) byte for byte, in the key and in the matching exercise folder (`docs/bpc_ex/` or `docs/ipc_ex/`) together; no line may be lost.
2. Append it at the end of the target list, then renumber both lists in both files (only the leading `N.` of each item header).
3. SBS: set `class_extra=extra` on the item's rows when it moves to Extra, `class_extra=` (empty) when it moves to main: `uv run python kamma/edits/scripts/sbs_sync.py set <id> class_extra=extra` (dry run, then `--apply` after approval and a backup). `check` does not compare `class_extra`; confirm with a query on `class_anki` + `class_source`.
4. Run `uv run python kamma/edits/scripts/verify_key.py`; it must exit 0.

### Rule copied from the audit guide

`kamma/audit/audit-guide.md` is not always loaded, so this rule is kept in both files. When one copy changes, change the other.

- **DPD example (owner rule).** If a DPD headword quotes the key sentence (or a near-identical one) in `example_1`/`example_2`, that is strong evidence for the key's reading of the word under that headword (POS, grammar, gloss). Change that reading only for a real grammatical error, not for a different but valid interpretation; at most suggest a change to DPD. Check with `uv run python kamma/edits/scripts/dpd_lookup.py <word> --sentence "<key sentence>"`: matching headwords are prefixed `EXAMPLE`. (also in kamma/audit/audit-guide.md → Process; keep in sync)

### Rules in AGENTS.md

AGENTS.md is always loaded; these rules apply to every edit. Read them there:

- **Data preservation**: AGENTS.md → Project: DPD Pāḷi Courses
- **Clean Markdown**: AGENTS.md → Project Principles → Clean Markdown Sources
- **Reserved ` / `**: AGENTS.md → Project Principles
- **Reserved `— `**: AGENTS.md → Project Principles
- **No line numbers in lasting documents**: AGENTS.md → Project Principles
- **Key verification**: AGENTS.md → Key Verification
- **Translation brackets**: AGENTS.md → Course Audits
- **Sutta links**: AGENTS.md → Sutta Links

## Owner gate

One approval per edit: the proposal table (Step 3) covers both the `docs/` changes and the SBS commands. Wait for explicit approval before touching `docs/` or the DB.

If anything turns up that is not in the approved table (another out-of-sync row from `check`, a dry run that differs from the approved one, a new file to change), stop and ask again before doing it.

## Steps

1. **Request.** Restate the owner's change in one line; list every affected sentence (file:line, class, item, source). Create the history file (see Record).
2. **Locate.** For each sentence find the key row, the exercise row, the translation line, and the SBS rows: `uv run python kamma/edits/scripts/sbs_sync.py find "<text>" --class <N>` / `uv run python kamma/edits/scripts/sbs_sync.py show <id>`. Run `uv run python kamma/edits/scripts/dpd_lookup.py <word> --sentence "<key sentence>"` for every word whose reading changes. Draft the exact `set` / `replace` / `move` / `clear` commands for the SBS rows and run them as a dry run (no `--apply`: reads only).
3. **Proposal (owner gate).** One table: place | current → exact new text | reason, with the `docs/` rows first and then the SBS commands with their dry-run output. Include the translation line whenever a reading changes, the exercise row when it is prefilled, and `class_extra` for a main ↔ Extra move. Wait for approval.
4. **Apply to `docs/`.** Exactly the approved text. Record the pre-apply revision (`git rev-parse HEAD`) in the history file and in the handoff.
5. **Verify docs.** `uv run python kamma/edits/scripts/verify_key.py` exits 0; `git diff docs/` shows only the approved lines.
6. **Apply SBS.** Back up the full touched rows as JSON (`show` is a lossy summary, not a backup): `test -e kamma/edits/backups/sbs_backup_edit_<id>.json && echo "BACKUP EXISTS" || sqlite3 -json /Users/deva/Documents/dpd-db/dpd.db "select * from sbs where id in (<id>, …)" > kamma/edits/backups/sbs_backup_edit_<id>.json` (use `$DPD_DB` instead of the path if it is set; the `test -e` guard never overwrites an existing backup: if the file exists, stop and ask). Include the target id of every `move`; if a target has no sbs row yet, note that in the history file (`move` creates it, and the backup cannot hold a row that did not exist). Run the approved commands with `--apply`. Then re-check every row of the same class + source for the old value: `uv run python kamma/edits/scripts/sbs_sync.py find "<old text>" --class <N> --source <source>` must list nothing; for each touched key file `uv run python kamma/edits/scripts/sbs_sync.py check <key file> --since <pre-apply rev>` (optionally `--class <N>`, `--only TRANS PALI POS ORPHAN NO-SBS`) must show no issue; `check` does not compare `class_extra`: confirm it with a query. Anything outside the approved table: stop and ask (Owner gate).
7. **Record.** Finish the history file; update or reset `handoff.md`; add a lesson to `learnings.md` only if it qualifies; add any improvement to the skill (guide, folder, scripts) found but not done now to `improvements.md`. Draft a commit message; the owner commits.

## Record

- Each edit writes `kamma/edits/history/YYYYMMDD_NN_slug.md` (NN = running number of the day). Create `history/` if missing. Content: request, proposal, approvals, pre-apply rev, commands run, results.
- History is a write-only log and gitignored. Do not read it at session start.
- SBS backups: `kamma/edits/backups/sbs_backup_edit_<id>.json` (`<id>` = the history file's `YYYYMMDD_NN`; gitignored). Create `backups/` if missing. Only the touched rows of the `sbs` table, every column, as JSON (a few KB), never the whole database. Kept for a month (see Start of session).
- Restore from a backup (owner approval first, like any DB write): `uv run python kamma/edits/scripts/sbs_sync.py restore kamma/edits/backups/sbs_backup_edit_<id>.json` lists every field that differs from the backup (dry run); add `--apply` to write. It puts every column of each backed-up row back, and inserts a row the backup holds that is now missing. A row that a `move` created (noted in the history file) is not in the backup: empty it with `sbs_sync.py clear <id> --apply`.

## Handoff

`kamma/edits/handoff.md` (gitignored) holds only what is unresolved from the last session. When a session ends with the request done, reset the file to this template, but keep the lines under "Noticed in docs/" that the owner has not dealt with yet:

```
# Handoff

Nothing open.

- Open request:
- Current step:
- Approval (pending / given):
- Pre-apply rev:

## Noticed in docs/ (outside a request, for the owner)
```

"Nothing open." is the marker for the request: if the first non-title line is anything else, resume from the file. The "Noticed in docs/" list does not count as open work: it is shown to the owner (Start of session), and a line is removed when the owner turns it into a request or drops it. One line each: date, what, where (file and class/item; no line numbers).

## Learnings

`kamma/edits/learnings.md` keeps only lessons that apply broadly and will change future decisions (a recurring trap, a check that catches a class of misses). One-off decisions stay in that edit's history record. When a lesson turns into a rule, move it into this guide and remove it from learnings.

## Improvements

`kamma/edits/improvements.md` lists improvements to this skill found during an edit that are not for now: the guide (an unclear or missing step or rule), the structure of `kamma/edits/`, and the scripts in `kamma/edits/scripts/` (a bug, a gap, a missing check). Not course content: a problem in `docs/` outside the request is told to the owner and written to `handoff.md` → Noticed in docs/, not listed here. One line each: date, what, where (file, and class/item if needed; no line numbers). Do not stop the edit to do them. Every session starts with a warning that names the open points (Start of session). When a point is done or the owner drops it, remove its line.

Learnings change how future edits are decided; improvements are work still to do.
