# Handoff: SBS ↔ key mismatches that predate the audit commits

Date: 2026-11-26
Status: not started. Findings only; none of these has been changed in dpd-db.

## Goal

The SBS table in dpd-db (`sbs.class_*`, `class_anki` = class number 1–29) must correspond to the course keys (`docs/bpc_key/`, `docs/ipc_key/`), because it feeds the Anki decks and other exports. Above all, every key sentence's bold translation must equal `class_example_translation` on every SBS row that carries that sentence. Those two must always be in sync.

## Context

- Tool: `kamma/audit/scripts/sbs_sync.py` (README → Course Audits). It finds the DB through `$DPD_DB`, default `/Users/deva/Documents/dpd-db/dpd.db`. Write commands are dry runs until `--apply`.
- The mismatches introduced by commits `d35b4299` (bpc key) and `b4df24ea` (ipc key) were handled in the session that wrote this handoff. Proposal table: `kamma/audit/scratch/sbs-sync-proposals.md`. The owner approved A (83 translations, 522 rows), B (6 Pāli texts) and C1 (`clear 70566`), and they were applied on 2026-11-26.
- **This handoff covers everything else.** The rest was already out of sync before those commits.

## Counts (2026-11-26, after the A/B/C1 writes; these are all pre-existing)

From `check` over all 29 key files: 814 key sentences, 4 073 SBS class rows, 62 fragment matches (translation not compared).

| Kind | Count |
| --- | --- |
| TRANS: key translation ≠ `class_example_translation` | 271 |
| PALI: SBS sentence is a spelling variant of a key sentence (≥ 85 % similar); its translation is compared too | 48 |
| POS: DPD pos of the bolded headword ≠ key POS column (includes the 7 commit-era rows judged no-change: C2–C8 in the proposals file) | 171 |
| ORPHAN: SBS sentence of class N not found in key N | 37 |
| NO-SBS: key sentence with no SBS row | 28 |

These are the counts after the spelling-variant pairing was added to `check`. TRANS went up from 259 because variant rows are now compared as well, and footnote markers (`[^n]`) are now ignored.

TRANS per file: bpc 2:6 3:4 4:9 5:13 6:7 7:10 8:8 9:13 10:13 11:20 12:17 13:11 14:16 15:9 · ipc 16:8 17:9 18:11 19:3 20:4 21:7 22:8 23:17 24:4 25:10 26:13 27:7 28:7 29:7.

Rows changed in the commit-era fix are backed up in `kamma/audit/scratch/sbs_backup_before_apply.json`, `…_2.json` and `…_3.json`.

## Tasks

1. **Translation sync (priority).** List the mismatches:
   `for f in docs/bpc_key/[0-9]*_class.md docs/ipc_key/[0-9]*_class.md; do uv run python kamma/audit/scripts/sbs_sync.py check $f --only TRANS; done`
   - For each mismatch, decide which side is right. The default is the key: the audits have corrected the key, and SBS was copied from an older key. If SBS is better, the key must change instead, and so must `docs/*_ex` per the golden rule.
   - Present a table (key location, SBS ids, change, short reason) for owner approval before any `--apply`.
   - Apply with `set <id> class_example_translation=…` on every id of the sentence. `replace … --field class_example_translation --class N --source S` works for small wording changes.
   - Many items differ only in diacritics (Ananda/Ānanda), punctuation or `[ ]` brackets. Batch those as one approval group.
2. **POS.** `check … --only POS`. Many are not real conflicts:
   - `pp`/`ptp`/`prp` in DPD against `adj` in the key.
   - Contracted forms that the key tags `sandhi` while SBS marks DPD's sandhi-form headword.
   - The key putting `ind adv` on a DPD adj.

   For each real one there are three options: `move <from> <to>` to the DPD row that matches the key's POS (it refuses if the target already has class data), `clear`, or change the key.
3. **PALI.** `check … --only PALI`. Fix `class_example` to the key's spelling with `replace` (it keeps the `<b>`). Leave rows whose bold is a compound headword the key writes split (e.g. AN10.48 `alam'ariyañāṇadassanaviseso`, now only in the key's footnote); those are SBS compound cards by design. Ask the owner.
4. **ORPHAN.** SBS sentences no longer found in the key.
   - Causes: spelling drift (e.g. `ananda`, `tam`, hyphens kept, spacing), sentences cut from the key, and class 1. SBS class 1 has 25 rows taken from other texts, but key class 1 has only one sentence.
   - For each: fix `class_example` to the key's Pāli and keep the `<b>` on the same word, or `clear` if the sentence was cut on purpose. Ask the owner about class 1.
5. **NO-SBS.** Key sentences with no SBS row. This is often intentional: every word was already marked in an earlier class, or the line is a short question such as "katame pañca?". Report only the ones that look like gaps.
6. **Make the DPD checks look for DPD's own example sentences.**
   - **Rule (owner, 2026-11-26):** if a DPD headword has the key sentence (or a near-identical one) in `example_1` or `example_2`, that is a strong argument to keep the key's reading of the word under that headword (its POS, grammar and gloss). Change it only for a real grammatical error, not for a different but valid interpretation.
   - **Case that set the rule:** `kallaṃ` in SN22.59 (`docs/bpc_key/9_class.md`). The audit fix in `d35b4299` changed it from `ind` "is it suitable?" to `adj nt.nom.sg` "suitable; proper". DPD's `kallaṃ` (id 20715, ind) quotes exactly this sentence in `example_1`, and SBS marks that headword/q. The owner had the key row (and the exercise row) reverted to `ind`.
   - about dpd-lookup - We need to develop dpd_lookup.py - right now it is stop when it find one headword, example `pallaṅkena` match `pallaṅkena` and `pallaṅka 1&2` but it does not see `pallaṅkena` as option there. The material should be syned with DPD. In rare cases it also means suggest change to DPD.
   - **Scripts to adjust:**
     - `scripts/verify_key.py --dpd` (`DpdDb`, `classify_row`): for each word, record whether one of its DPD readings has the sentence in `example_1`/`example_2`. Report that reading as the preferred one, and flag a key POS or grammar that disagrees with it.
     - `kamma/audit/scripts/dpd_lookup.py`: optionally take the sentence and mark the headword whose example contains it.
     - `kamma/audit/scripts/sbs_sync.py check`: for a POS mismatch, say whether the SBS headword's DPD example is this sentence. If it is, the key is the side to question.
   - **Matching:** normalise like `sbs_sync.norm` (strip tags, apostrophes, punctuation, case) and accept containment either way, because DPD examples are often longer or shorter than the key sentence (here DPD has `yaṃ pan'āniccaṃ …` against the key's simplified `yaṃ aniccaṃ …`).
   - **Audits:** add the rule to `kamma/audit/audit-guide.md` (DPD lookups) once the scripts support it, so no audit row changes a reading that DPD documents with this very sentence.

Note: done on 2026-11-26, the DN9.7 translation (`vo` = "your") was fixed in the key and in SBS, as part of the commit-era task.

## Known limits of `check` (read before trusting a count)

- The translation is compared when the SBS sentence equals a key sentence after normalisation, which removes tags, apostrophes, punctuation and case, or is a ≥ 85 % spelling variant of one (reported as PALI). Fragment and wider matches are POS-checked only.
- Where the key gives "**(or)**" alternatives, only the first bold line is compared. Split sentences (two tables, two bold lines) are joined.
- POS is checked only when the bold word equals a table cell exactly. Partly-bolded compound members are skipped.
- Mapping used: masc/nt/fem → noun; pr/aor/fut/imp/opt/perf/cond → verb; DPD `ger` = key `abs`. Anything else must match a token in the key POS or Grammar cell.

## Rules

- Never write to dpd-db without the owner's approval of the exact table.
- If the key changes, sync `docs/*_ex` as well (golden rule in `kamma/audit/*-audit.md`) and run `uv run python scripts/verify_key.py` before committing.
- dpd-db has its own uncommitted work (`AGENTS.md`, `gui2/data/*`, …). Don't touch it. Only `dpd.db` is written.
