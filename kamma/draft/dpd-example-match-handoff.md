# Handoff: make the DPD checks look for DPD's own example sentences

Date: 2026-11-26
Status: not started. Split out of `kamma/draft/sbs-sync-preexisting-handoff.md` (was its task 6). Do this before that handoff's POS task, because its results decide which side a POS mismatch should change.

## Context

- DB: dpd-db `dpd.db`, found through `$DPD_DB`, default `/Users/deva/Documents/dpd-db/dpd.db`. All scripts here only read it.
- dpd-db has its own uncommitted work (`AGENTS.md`, `gui2/data/*`, …). Don't touch it.
- Already done (2026-11-26, `/kamma:quick`): `kamma/audit/scripts/dpd_lookup.py` now also returns every headword that DPD's `lookup` table gives for the form, so `pallaṅkena` lists `pallaṅkena` (ind) together with `pallaṅka 1` and `pallaṅka 2`. The 6-row cap was removed. The sentence option below is still open.

## Rule (owner, 2026-11-26)

If a DPD headword has the key sentence (or a near-identical one) in `example_1` or `example_2`, that is a strong argument to keep the key's reading of the word under that headword (its POS, grammar and gloss). Change it only for a real grammatical error, not for a different but valid interpretation. Often the course material took DPD's examples in the first place. The material should be synced with DPD. In rare cases this also means suggesting a change to DPD.

**Case that set the rule:** `kallaṃ` in SN22.59 (`docs/bpc_key/9_class.md`). The audit fix in `d35b4299` changed it from `ind` "is it suitable?" to `adj nt.nom.sg` "suitable; proper". DPD's `kallaṃ` (id 20715, ind) quotes exactly this sentence in `example_1`, and SBS marks that headword/q. The owner had the key row (and the exercise row) reverted to `ind`.

## Scripts to adjust

- `scripts/verify_key.py --dpd` (`DpdDb`, `classify_row`): for each word, record whether one of its DPD readings has the sentence in `example_1`/`example_2`. Report that reading as the preferred one, and flag a key POS or grammar that disagrees with it.
- `kamma/audit/scripts/dpd_lookup.py`: optionally take the sentence and mark the headword whose example contains it.
- `kamma/audit/scripts/sbs_sync.py check`: for a POS mismatch, say whether the SBS headword's DPD example is this sentence. If it is, the key is the side to question.

## Matching

Normalise like `sbs_sync.norm` (strip tags, apostrophes, punctuation, case) and accept containment either way, because DPD examples are often longer or shorter than the key sentence (here DPD has `yaṃ pan'āniccaṃ …` against the key's simplified `yaṃ aniccaṃ …`).

## Audits

Add the rule to `kamma/audit/audit-guide.md` (DPD lookups) once the scripts support it, so no audit row changes a reading that DPD documents with this very sentence.
