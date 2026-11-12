# ipc_key audit — state / handoff (2026-11-12)

Task: audit `docs/ipc_key/` following `kamma/draft/audit/audit-guide.md`. Read-only on `docs/`. No commits.
Final file (NOT written yet): `kamma/draft/audit/ipc-key-audit.md`.

## Done

- Mechanical checks (step 1). Outputs in `scratch/`:
  - `mech-output.txt` — script `scripts/ipc_key_mech.py` (run from repo root: `uv run python kamma/draft/audit/scripts/ipc_key_mech.py`)
  - `verify_key-output.txt` — `uv run python scripts/verify_key.py --course ipc --warnings --dpd --report <path>`: exit 0, 63 coverage warnings; DPD: 85 IMPOSSIBLE, 21 NOT-FOUND, 4 ROOT-MISMATCH
  - `dpd-flags.tsv` — those 110 rows (file, line, word, pos, grammar, root, bucket, DPD readings)
  - Sutta links: `check_sutta_links.py docs/ipc_key` → 185 links / 79 pages, all pass. No non-sutta external links. 3 unlinked labels (17:637 `VV 52`, 27:42 `VIN PAT NID`, 27:252 `VIN PAT SA`).
- Line-by-line read, slices saved in `scratch/key-cNN.md` (format `| Cat | Location | Current | Problem | Suggested | Conf. |`, Location `NN_class.md:line`, `¦` = table pipe):
  - 16, 17, 18, 19, 20: complete
  - 21: lines 1–527 (file has 533 lines; only the tail of extra example 4 is unread)

## Not done

1. Read 21 (528–533), 22, 23, 24, 25, 26, 27, 28, 29 and `index.md`; one slice file each.
2. Mechanical findings still to turn into rows / a "Mechanical detail" section (all evidence is in `mech-output.txt`):
   - footnote `[^44]` defined (27:314) but never referenced; definitions out of order in 19 and 27; ids 1–55 run course-wide
   - key vs exercise: 28 real sentence differences (list in `mech-output.txt`), e.g. 19:334 label, 20:382 longer sentence, 22:135 `apabodheti`/`apabodhati`, 23:49 shortened sentence, 23:764 `asaṅkhāditvā`/`saṅkhāditvā`, 24:387 exercise repeats a clause, 27:226 `apurekkharāno`/`apurakkharāno`, 21:207 `UD5.10`/`UD50`; exercise-side: `ṁ` in ex 17:93, curly `’` in ex 17:435, reference after the sentence in ex 21:95 and 28:125
   - 31 label / `<br>`-spacing differences key vs ex
   - convention counts per class (quotes, `...` vs `…`, ` - ` vs `–`, `lit:` vs `lit.`, `<br>` 502 lines, root notation `･`/`×` stops after class 22: classes 23–29 put constructions in column 5)
   - go through the remaining `dpd-flags.tsv` rows for classes 22–29 while reading (classes 16–21 already considered)
   - idea not yet run: script check for translation lines without final punctuation, and tally of `ger` vs `abs`
3. Step 4: adapt `scripts/verify_rows.py` (paths: `docs/ipc_key`, file regex `\d+_class\.md`, slices `scratch/key-c*.md`) and fix failing rows.
4. Step 5: adapt `scripts/merge_audit.py` (slices `key-c16.md` … `key-c29.md`), write head (method/limits) and mid (owner decisions), generate `ipc-key-audit.md`.
5. Run ruff / pyright on the new scripts in `kamma/draft/audit/scripts/` (`ipc_key_mech.py`, `dpd_lookup.py`); not done yet.
6. Delete `scratch/` only after the final file is checked.

## Working notes

- The key follows DPD closely (roots, constructions, compound types, glosses). Check with `uv run python kamma/draft/audit/scripts/dpd_lookup.py <lemma> …` before calling a derivation wrong; several of my first suspicions were DPD-backed and dropped (`√ādā`, `jighacchādubbalya` dvanda, `aḍḍhateyya`, `upaghāta √ghaṭ`, `pātimokkha` masc).
- Real findings cluster in: context-dependent tags (case/gender in the sentence), roots shifted one row, stems tagged with case, sub-row glosses carrying the compound's gloss, analysis lines contradicting the table, translations vs row glosses, unbalanced quotes, and drift between the two halves of each class (items with sandhi apostrophes / blank cells vs items without / `-` cells).
- Recurring owner decisions seen so far: `ger` vs `abs`; sandhi apostrophes in half the items; `[d]`-type inserted consonants; bahubbīhi notation (`\>`, `>`, ` - `, footnote); first-person editorial footnotes (class 20); bracket style for supplied words; `lit:`/`lit.`; UK/US spelling; reflexive forms translated "myself/oneself"; label styles (`UD45`/`UD5.10`, `SNP7`, `DHP064`, `VIN1.1.2`).
- Limits to state in the final file: Pāli judged from knowledge plus targeted DPD lookups (not every form); canonical readings not checked against a text; link check proves the anchor exists only; rendered site/PDF not built.

## Restart prompt

"Continue the ipc_key audit. Read `kamma/draft/audit/audit-guide.md` and `kamma/draft/audit/scratch/STATE.md`, then carry on from 'Not done' item 1 (class 21 line 528, then class 22), saving one slice file per class and updating STATE.md after each."
