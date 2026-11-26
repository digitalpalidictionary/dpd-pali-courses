# BPC key audit — `docs/bpc_key/`

Date: 2026-11-13
Scope: all 16 Markdown files under `docs/bpc_key/` (index + classes 1–15; 8 235 lines, 5 466 table rows, as counted by `mech_checks.py`).
No file in `docs/` was modified. This is a findings list only.

This file replaces the audit of 2026-11-11, which was written before `kamma/audit/audit-guide.md` existed and was read by parallel agents. It is the result of two passes over every slice by one reader: a fresh read by the guide's full checklist, and a re-check of every row of the old audit. A row that comes from the old audit ends its `Problem` with `(old <id>)`: Part 1 ids are written bare (`(old C9)`), Part 2 ids as `(old 4.1)`.

Related to #6 Course enhancement with AI

## Method and limits

| Check | How | Result |
| --- | --- | --- |
| Mechanical checks | `uv run python kamma/audit/scripts/mech_checks.py docs/bpc_key --links-out kamma/audit/scratch/bpc-key/links.txt` (footnotes per file: the folder has one definition) | Exit 0. 0 table column mismatches, 0 index/H1 differences, footnotes 1 ref / 1 def, 2 stray-character lines (Mechanical detail, M1) |
| Key sentence vs exercise sentence | `uv run python kamma/audit/scripts/key_vs_ex.py docs/bpc_key docs/bpc_ex --glob "*_class.md"` | 465 items compared; 71 differ after normalising quotes, bold, `<br>` spacing and `ṁ`; 97 label or `<br>`-spacing differences (M2) |
| Project verifier | `uv run python scripts/verify_key.py --course bpc --warnings --dpd --report kamma/audit/scratch/bpc-key/verify-key-dpd.txt` | Exit 0. Numbering, POS vocabulary, grammar vocabulary, root format, stray characters: 0 errors. Word coverage: 465 warnings (M3) |
| Word forms vs DPD | The `--dpd` report of the same run (advisory) | 4 324 rows: 1 123 confirmed, 2 087 ambiguous, 1 079 skipped, 17 IMPOSSIBLE, 12 NOT-FOUND, 22 ROOT-MISMATCH. The 51 flagged rows were read with their class (M4) |
| Sutta links | `uv run python scripts/check_sutta_links.py docs/bpc_key` | 219 links / 104 pages, all pass (exit 0). The folder has no other external links |
| Full read of every file | Line by line, by the main session, 14 class slices and 1 cross-file slice; the guide's "What to look for" list, categories A–I and the key checks (tag against the sentence, Root column, gloss against translation, translation against sentence, the same word tagged in two ways) applied to each | Done; every slice file ends with its checklist note |
| Re-check of the old audit | Every row of the old Part 1 and Part 2 re-checked against the source | 369 old ids all accounted for: in a row here or in the dropped list (see "Old rows") |
| DPD lookups | `uv run python kamma/audit/scripts/dpd_lookup.py <lemma> …`, run once over the 107 lemmas the reader had listed as suspicious | 104 rows waited for it: 30 dropped because DPD agrees with the text, 74 finalised against the DPD entry. 6 lemmas are not DPD headwords: `accagacchati`, `bahujanahita`, `bāhuppacālaka`, `ceto`, `panuda`, `uccāsoṇḍa` |
| Excerpt check | `uv run python kamma/audit/scripts/verify_rows.py docs/bpc_key …` on every slice file and on this file: each backtick excerpt in `Current` searched in the cited file within 2 lines of the cited line | 488 excerpts pass, 0 fail (rows with no source file found: 0) |
| Merge | `uv run python kamma/audit/scripts/merge_audit.py kamma/audit/scratch/bpc-key/merge.toml` | This file |

Not verified:

- The DPD lookups were deferred to one run, on the owner's instruction: the reader listed what looked suspicious, and only those 107 lemmas were looked up. A tag, root or gloss that did not look suspicious rests on the reader's knowledge of the language. Each row carries a confidence score (1–10). Below 8, check DPD or the text before changing anything.
- `dpd_lookup.py` prints headwords, not inflection tables, and it does not print the `･` / `×` mark of the Root column. Rows that say `DPD lookup` name what was not confirmed.
- The number after a root in the lookup output is DPD's homonym number; the number in the key's Root column is the root group. Root findings were judged from the root and the conjugational sign.
- The 2 087 "ambiguous" rows of the DPD form check were not reviewed one by one.
- `verify_key.py` cannot align class 15 word by word: the class is laid out in paragraphs, and 209 of the 465 word-coverage warnings come from it. Class 15 was read in full, but it has no scripted word check behind it.
- Canonical readings were not compared with a text edition. Rows that depend on a reading say `verify`.
- The link checker proves that the page and anchor exist, not that the sentence is in that sutta.
- `docs/bpc_ex/` was read only where it differs from the key (M2). Exercise-side errors are noted, not listed in full.
- Translation rewordings in section C are suggestions, not corrections.
- Rendered output (site, PDF, DOCX) was not built.

Paths below are relative to `docs/bpc_key/`. In `Current`, `\|` is a table pipe in the source.

Overall confidence: 9/10 that the quoted text is where the row says (scripted). 8/10 for categories D, E, F and G (visible in the source). 7/10 for A, B, C and H as a group: DPD was consulted for the tags, roots and glosses that looked doubtful, but no text edition was. Use the per-row score.

## Old rows: mapped, corrected, dropped

The old audit had its own scheme (Part 1, scripted cross-file checks A–F; Part 2, reading notes numbered by class). Every old row is now in one of the guide's categories A–I and keeps its old id in the `Problem` cell. All 369 old ids are accounted for.

Dropped (9), each with its reason:

| Old id | Reason |
| --- | --- |
| A1 | Not a finding: it records that numbering, column counts and the tag vocabulary are clean (`mech_checks.py` confirms 0 table column mismatches). |
| B4 | The exercise gives the sandhi-resolved form (`"samaṇā amha" iti`) by design, as in other classes; the key table rows already follow it. The `amha-` hyphen is kept as old 4.3. |
| E1 | Not a defect: the empty header row on follow-up tables is the same across the folder and is how the build renders them. |
| F11 | No change needed: the old row itself says "Leave"; DPD's reflexive-aorist reading of `avoca` does not make the plain `aor` tag wrong for a beginner key. |
| 5.1 | The owner rejected the same point in the BPC lesson audit (bpc A13); see above. |
| 6.7 | DPD supports the text: dakkhati 1 is `pr` "sees" (the future is dakkhati 2), so `pr.3rd.pl`, "see" is a DPD reading. |
| 6.8 | DPD supports the text: atthi 1.2 is `pr 3rd pl of atthi`, "there are". |
| 6.9 | No change needed: DPD supports the tag (garu 5 masc "respect"); the old row itself suggested "Leave". |
| 11.5 | DPD supports the text: `opanayika` is the DPD headword; the CST spelling `opaneyyiko` is a variant reading, not an error. |

Corrected by the DPD lookup (same id, different content):

- 7.14 (`gāhaṃ`, 7:333): the old row wanted the root `√gāh`. DPD derives every `gāha` from `√gah`, so the Root cell stands; what is doubtful is the gloss "hiding place".
- D7 (`virājiya`, 14:651): the old row wanted a separate root "colour". DPD has the same √raj with the causative sign `*e`; only the sign is wrong.
- 13.8 (`nirujjhamānā`, 13:283): DPD does call `nirujjhati` a passive, so the row is now about the two classes disagreeing and the gloss "is ceased".
- 14.6 (`acchejji`, 14:802): the tag `caus.pass` follows DPD; only the MN2 reading is left to verify.
- 12.10: `yena ¦ ind ¦ adv` (12:110) is a DPD reading; the row now cites only `sarena` (12:492).
- 12.7 (`parābhavato`, 12:657): the tag is a DPD reading; tag and gloss still disagree.
- A14: only 6:175 has `..`; 5:413, 10:636 and 11:341 have `...`.

## Fresh findings dropped after the DPD lookup

27 fresh rows were written as "to confirm" during the read and dropped when DPD agreed with the text. They are listed here so that the same doubts are not raised again:

- Genders that agree with DPD: `cetas` / `ceto` masc (7:202, 12:194, 14:462, 15:351), `mano` masc (14:225), `ayo` masc (14:74), `thālaka` masc, `vassa` "rainy season" masc, `saṅgara` nt, `kucchi` masc, `pātimokkha` masc (DPD has masc and nt), `addhāna` nt.
- Roots and signs that agree with DPD: `pavattar` √vac, `paṭighāta` and `paṭigha` √ghaṭ `*e`, `sāraṇīya` √raj ya, `sakka` "Sakyan" √sak, `ādeti` √ādā ya, `niddā` √dā ya, `ajjhosita` √sā, `aṅga` √añj `*e`, `saṃyojana` √yuj `*e`, `sammodati` √mud `*a`.
- Tags that agree with DPD: `vijjati` as a passive, `sañcicca` as `ind ¦ adv`.
- Notation: `jīvitu'kāmo`, `amaritu'kāmo`, `gantu'kāmo` (9:433, 434, 452) and `bhottu'kamyatā` (13:228). DPD builds these from the infinitive in `-tuṃ`, so the mark stands for the dropped `ṃ`.

The starred sign `\*a` (9 cells, e.g. 5:83, 8:215, 10:473, 14:665) is DPD's own notation for a strengthened root vowel and is not reported. The passive sign `ya` after the root group (`√labh･1 ya`, 22 rows) is the key's convention and is not reported either.

## Decisions for the owner

These are not decided in the audit; the rows say `owner decision`:

- Elision marks inside one word where a sandhi consonant is inserted or nothing is dropped: `añña'd'atthu` (5:481), `yāva'd'eva` (7:370), `eta'r'ahi` (11:638, 13:103), `atthaṅ'gate` (10:181), `samanta'pāsādiko` (12:369). DPD writes each as one word. If the marks are a deliberate notation for sandhi, they can stay, but the rule should be stated once in the key.
- One rendering for recurring terms (`brāhmaṇa`, `dhammavinaya`, `samaṇa`, `mettā`, "Venerable sir").
- Phrase items with no source reference (class 1, and 13 items in class 2), and commentary references with no link (5:49, 8:101).
- AN3 labels run one higher than their link anchors (AN3.66 → `#an3.65`, and five more): the labels seem to follow the VRI numbering and the anchors SuttaCentral's. Decide which numbering the label should show.

## The GOLDEN RULE

When apply approved suggestions:

Always correct corresponding sentences and tables in the docs/bpc_ex/ since there we have exercise not only sentences but also some pre-filled values in gramatical analisis. Keep those pre filed values, which deliberatley has been choosen for material which has not been covered by the time of that exact senteces. So when you change some of the grammar in the key - dounde check maybe in the exercise that grammar is prefilled as well and need to be corrected and synced with the key.

**SBS sync.** Every key sentence is also stored in the SBS table of dpd-db (`class_*` fields, `class_anki` = class number), which feeds Anki and the other exports, so the SBS table must correspond to the key. When a fix changes a key sentence's translation, its Pāli text, or the POS/headword of a word (e.g. noun → adj/pp, a separate DPD row), find and update the SBS rows with `uv run python kamma/audit/scripts/sbs_sync.py` (`check <key file> --since <rev>` lists what the edit put out of sync; `replace`, `set`, `move`, `clear` change the DB, dry run until `--apply`). Get the owner's approval before writing to the DB.

**Word gloss vs sentence translation.** When a fix changes the gloss, POS or reading of a word in the analysis table, check the sentence translation below the table and change it to match (and then the SBS translation, see above). A table-only fix leaves the translation telling a different story (e.g. `vo` changed from "surely" to "your" in 27_class.md, but the translation kept "surely").

**Moving an item between main and Extra.** When an approved fix moves an exercise item from the main list to `## Class N Extra` or back (e.g. it turns out to be an irregular case):
1. Move the whole item (header line with its link, Pāli line, table, bold translation) byte for byte, in the key and in `docs/bpc_ex/` together; no line may be lost.
2. Append it at the end of the target list, then renumber both lists in both files (only the leading `N.` of each item header).
3. SBS: set `class_extra=extra` on the item's rows when it moves to Extra, `class_extra=` (empty) when it moves to main: `uv run python kamma/audit/scripts/sbs_sync.py set <id> class_extra=extra` (dry run, then `--apply` after approval and a backup). `check` does not compare `class_extra`; confirm with a query on `class_anki` + `class_source`.
4. Run `uv run python scripts/verify_key.py`; it must exit 0.
5. Log the move in "Item moves (main ↔ Extra)" below. Move rows are a permanent record: they are **not** removed when applied, only their Status changes.

## Item moves (main ↔ Extra)

One row per move, kept after it is applied. Item numbers are the ones at the time of the move; the Source column identifies the item after later renumbering. Status: `proposed` → `approved` (owner) → `applied <commit>`; a rejected proposal is removed. Paths are relative to `docs/bpc_key/` and `docs/bpc_ex/`.

| Date | File | From | To | Source | Reason | SBS (`class_extra`) | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-11-26 | 11_class.md | main 11 | Extra 7 | SNP8 (`sakko ujū ca suhujū ca …`) | Irregular: `ujū`, `suhujū` are nom.sg with metrical `ū` (`masc.nom.sg (u \> ū)`); thread `20261126_dpd_example_match` (a1, task 6.1a). Main 12–26 become 11–25. | 7 rows → `extra`: 3539, 14392, 26341, 52961, 56382, 64530, 64657 | applied (uncommitted; SBS `class_extra` set 2026-11-26) |

## A. Pāli and grammar content errors

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 8_class.md:522 | `[^1]: Alternatively, can be taken as a noun masc instr sg - (having illuminated) with extraordinary appearance` | An instrumental of `vaṇṇa` would be `-vaṇṇena`; `-vaṇṇā` (line 422) cannot be instr.sg. (old 8.8) | Reword the note (e.g. "a bahubbīhi, fem.nom.sg") | 4 |
| 8_class.md:661 | `nārīsu \| noun \| fem.loc.pl \| with regard to women` | Dhp 284 reads `nārisu` (short i, for the metre); the item is not marked `(simpl)`; also the sentence (line 648). (old 8.1) | verify; `nārisu` | 6 |
| 9_class.md:253 | `bahujanahitāya \| noun \| nt.dat.sg [dat of purpose]` | verify_key IMPOSSIBLE (no DPD reading matches `nt.dat.sg`). `bahujanahita` is not a DPD headword, so the report has no reading to compare; the tag may still be right. | DPD lookup (`hita`) | 3 |
| 9_class.md:426 | `kiṃ \| ind \| interr \| what` | A predicate pronoun ("what am I?"); also the object at line 469 (`taṃ kiṃ maññasi`); tagged `pron` at line 729. (old 9.11) | `pron \| nt.nom.sg` / `nt.acc.sg` | 5 |
| 9_class.md:487 | `tassa \| pron \| masc.gen.sg \| of that` | `tassa me` is "to me (being such)": `tassa` agrees with `me` (line 488, dat). (old 9.10) | `masc.dat.sg` | 6 |
| 9_class.md:584 | `parikkhāre \| noun \| masc.acc.pl \| requisites; accessories` | With `ussukā` the objects of concern are locative ("in regard to"), and the verse continues with a locative; also `bhesajje`, `paccaye` (lines 585, 587). (old 9.9) | `loc.sg` "in regard to" | 6 |
| 10_class.md:289 | `sahatthā \| ind \| masc.instr.sg` | POS `ind` with a case tag. (old 10.4) | `noun \| masc.abl.sg` (DPD has only the masc noun sahattha "one's own hand"), or `ind \| adv`; not `ind` with a case | 6 |
| 10_class.md:389 | `purato \| ind \| prep \| in front` | An adverb here, like the parallel `pacchato` (line 387). (old 10.7) | `adv` | 6 |
| 10_class.md:806 | `anekajāti \| adj \| masc.nom.sg \| with many rebirths; having multiple lives` | Dhp 153 has the compound `anekajātisaṃsāraṃ`; the first member cannot be nom.sg. The sentence (line 801) also splits it. (old 10.2) | `anekajātisaṃsāraṃ`, or tag as a compound member | 8 |
| 11_class.md:54 | `ādittacelo \| noun \| masc.nom.sg \| whose clothes are on fire; with blazing garments` | A bahubbīhi glossed as an adjective but tagged `noun`; its members get case tags (`āditta- \| pp \| masc.nom.sg`, `-celo \| adj`, lines 55–56, 59–60). (old 11.11) | Compound `adj` (DPD: ādittacela adj, kammadhāraya > bahubbīhi); members without case | 7 |
| 11_class.md:139 | `khataṃ \| pp \| masc.acc.sg \| injured, uprooted \| √khan･1 a (hurt, break)` | The gloss joins two DPD homonyms: `khata` "hurt; injured" is the pp of khanati (√khan, as in the Root cell); "dug up; uprooted" is the pp of khaṇati (√khaṇ). DPD also lists the idiom `khata upahata` "hurt and injured". | Gloss "injured" only | 6 |
| 11_class.md:255 | `mettāya \| noun \| fem.instr.sg \| with goodwill` | In apposition to `cetovimuttiyā` in the loc abs ("goodwill-liberation of mind"). (old 11.12) | `fem.loc.sg (loc abs)` | 5 |
| 11_class.md:476 | `evaṃ \| ind \| emph \| thus` | "thus" is the adverb; the same tag was flagged in class 10 (10_class.md line 424). | `adv` | 6 |
| 11_class.md:528 | `tassa \| ind \| adv \| therefore; thus; so; because of that` | In `tassa me … accayaṃ` the class 9 key reads `tassa` as a pronoun agreeing with `me` (9_class.md line 487). DPD has both readings (tassa pron; tassa 4 ind adv "therefore"). | One reading in both classes; with `me` the pronoun (`pron \| masc.gen.sg`) fits | 5 |
| 11_class.md:603 | `attaniye \| adj \| masc.loc.sg [loc abs] \| since belonging to oneself` | A substantive "what belongs to self": neuter. (old 11.13) | `nt.loc.sg` | 5 |
| 11_class.md:659 | `eta'r'ahi \| ind \| adv \| at present` | `etarahi` split with two elision marks; also in the sentence (line 643). (old 11.4) | `etarahi` (DPD: `eta + [r] + ahi`), unless the marks are a deliberate sandhi notation: owner decision | 5 |
| 11_class.md:684 | `dheyyaṃ \| noun \| nt.nom.sg \| the realm of; the sphere of` | No nominative role: it is what is crossed. Also `suduttaraṃ` (line 685); the translation (line 687) leaves it dangling. (old 11.10) | `nt.acc.sg`; "…will cross the realm of death, so hard to cross" | 6 |
| 12_class.md:169 | `mano- \| noun \| masc.nom.sg \| mind, heart` | A compound member (`manosañcetanā`, line 146) given a case tag. (The gender agrees with DPD: mano 1, masc, in comps.) | No case for the member: `mano- \| noun \| masc` | 6 |
| 12_class.md:253 | `chattiṃsa \| card \| fem.nom.pl \| thirty-six` | verify_key IMPOSSIBLE: DPD has `chattiṃsā` card fem nom sg. (old F6) | `fem.nom.sg`; check the spelling | 6 |
| 12_class.md:364 | `caturāsītīnaṃ \| card \| fem.dat.pl \| for eighty-four` | verify_key NOT-FOUND: a plural of a decade numeral. DN14 has `caturāsītiyā pāṇasahassānaṃ`; the sentence (line 357) is reworded without `(simpl)`. (old 12.3) | verify; `caturāsītiyā` | 6 |
| 12_class.md:438 | `satehi \| adj \| masc.instr.pl \| with one hundred` | `noun \| nt.instr.pl` for the same word at line 92. (old 12.5) | `card \| nt.instr.pl` (DPD: sata 2.1 card, nt), and the same tag at line 92 | 7 |
| 12_class.md:482 | `vīsati \| card \| fem.acc.sg \| twenty (20)` | verify_key IMPOSSIBLE: DPD has `vīsati` as fem nom sg; the acc. sg. is `vīsatiṃ`. (old F7) | Re-tag, or note the elided form | 5 |
| 12_class.md:696 | `bhagavā \| noun \| masc.nom.sg \| Blessed One` | With `brūhi` (imp.2nd.sg) this is an address; the translation (line 702) "May the Blessed One tell [us]" turns it into 3rd person. (old 12.6) | `masc.voc.sg`; "Tell [us] …, Blessed One" | 6 |
| 12_class.md:699 | `parābhavato \| noun \| masc.abl.sg \| for/of the downfall` | The gloss is gen/dat, the tag abl.; usually read as the gen. sg. of the prp ("of one who is declining"). (old 12.7) | Either keep the tag (verify_key: `parābhava` noun masc abl sg is a DPD reading) and gloss it as an ablative, or `prp \| masc.gen.sg` "of one who is declining"; tag and gloss must agree | 5 |
| 13_class.md:108 | `eta'r'ahi \| ind \| adv \| now` | `etarahi` split with two elision marks, as at 11_class.md line 659; also in the sentence (line 101). | `etarahi` (DPD: `eta + [r] + ahi`), unless the marks are a deliberate sandhi notation: owner decision | 5 |
| 13_class.md:175 | `kiṃ \| pron \| nt.nom.sg \| why` | Adverbial "why" is not nominative; the same phrase is `ind` at line 37. (old 13.14) | `ind \| interr` | 5 |
| 13_class.md:297 | `nirujjhamānā \| prp. pass \| fem.nom.sg \| ceasing` | DPD: `nirujjhati` is `pr, pass of ni √rudh`, "ceases", so the passive tag is defensible. But it is used here and at line 298 (`verb. pass … is ceased`) only; class 15 (15_class.md lines 376, 377) has `prp`, `verb \| ceases`. "is ceased" is not English. (old 13.8) | One tag in both classes; gloss "ceases" | 7 |
| 13_class.md:383 | `munī \| noun \| masc.nom.sg \| sage, monk` | verify_key IMPOSSIBLE: `munī` is nom.pl by form; nom.sg only by metrical lengthening. (old F8) | Add "(metrical)" | 5 |
| 13_class.md:423 | `uddhaṃ \| ind \| prep \| above` | Free adverbs here; also `adho`, `tiriyaṃ` (lines 424, 426). (old 13.15) | `adv` | 4 |
| 13_class.md:563 | `sallaviddhānaṃ \| adj \| masc.gen.pl (gen abs) \| when pierced by an arrow` | Three words for the same people get two cases (`āturānaṃ` dat.pl, line 559; `ruppataṃ` gen.pl, line 564); the "gen abs" has no separate subject. (old 13.13) | Same case; drop "(gen abs)" | 5 |
| 13_class.md:577 | `accagamā \| verb \| imperf.3rd.sg` | The only `imperf` tag in the key. | `aor.3rd.sg`; DPD lookup (`accagacchati` is not a DPD headword, so the tense was not confirmed) | 4 |
| 14_class.md:176 | `akāsi \| verb \| aor.2nd.sg \| did; made` | The subject `āyasmā` (line 173) is nominative, which takes the 3rd person (respectful address); `akāsi` is both 2nd and 3rd sg, so the tag is a choice. (old 14.9) | `aor.3rd.sg` | 5 |
| 14_class.md:231 | `adhicittam- \| noun \| nt \| meditation, higher mind` | An accusative governed by `anuyutta` (`adhicittaṃ + anuyuttena`), not a bare stem. (old 14.15) | `nt.acc.sg` | 5 |
| 14_class.md:483 | `paṭikūlasaññāya \| noun \| fem.instr.sg (+loc)` | AN7.49 has one compound, `āhāre paṭikūlasaññāparicitena`; the key splits it into an inflected `paṭikūlasaññāya` + `paricitena` (sentence line 477), not marked `(simpl)`. (old 14.1) | verify; `paṭikūlasaññā-` + `paricitena` | 7 |
| 14_class.md:523 | `dukkhasamudayaṃ \| noun \| nt.nom.sg` | verify_key IMPOSSIBLE: DPD has `dukkhasamudaya` masc only (`-aṃ` = acc.sg); nom.sg nt works only as an adjective of `saccaṃ`, as the gloss says. (old F5) | `adj \| nt.nom.sg` | 6 |
| 14_class.md:674 | `virājiya \| verb \| abs \| removing; cleansing \| √raj･3 ya (desire)` | `virājeti` is a causative: DPD gives it the sign `\*e` (caus of virajjati), from the same √raj as `virajjati` (sign ya). So the root is right but the sign `ya` is the non-causative one; the old audit's separate root "colour" is not what DPD has. (old D7) | Sign `\*e` in place of `ya`. Re-check 2026-11-25: DPD's own `virājiya` entry is `√raj 2 \*e` (colour, group 1), meaning "cleansing; removing", so the cell would be `√raj･1 \*e (colour)`; `virājeti` (detaches) is √raj 1 (desire, group 3). Owner: pick the sense | 7 |
| 14_class.md:830 | `acchejji \| verb. caus.pass \| aor.3rd.sg` | The tag follows DPD (acchejji: aor of caus pass of ā √chid, "completely cut out"), so it stands. The old row's other point remains: MN2 is said to read `acchecchi`, which DPD has as a separate headword (aor of the intensive, same meaning). (old 14.6) | verify the MN2 reading; if `acchecchi`, change sentence and row | 4 |
| 15_class.md:137 | `dhammaṃ \| noun \| masc.acc.sg \| doctrine, teaching` | In `yathādhammaṃ` ("properly, according to the rule") the compound is an adverb; the translation (lines 141, 155) has "in accordance with the Doctrine". Also line 151. | `yathādhammaṃ \| ind \| adv` (DPD: ind, adv, abyayībhāva, "fairly; correctly; justly; legally") | 6 |
| 15_class.md:361 | `n'ādhiṭṭhāti \| verb \| pr.3rd.sg \| does not take a stand` | Contains the negative but has no `+neg`, unlike `n'atthī'ti \| verb \| pr.3rd.sg +neg` (line 427). (old 15.5) | Add `+neg` | 6 |
| 15_class.md:441 | `ubho \| pron \| masc.acc.pl \| both` | verify_key IMPOSSIBLE: DPD tags `ubho` as dual. Not wrong for a beginner key. (old F9) | Leave, or note `dual` | 3 |
| 9_class.md:188 | `samaṇo \| noun \| masc.nom.sg \| the recluse \| √sam･3 ya (exert, strive)` | Verb mark `･` where the old audit's DB comparison has DPD's `×`: `samaṇo` ×5 (also 10:440, 11:184, 12:526, 13:513), `mettā` ×4 (11:253, 12:192, 13:390, 15:218), `bhusaṃ` (12:571). (old D20) | DPD lookup: `×` if DPD has it (the lookup output does not print the `･` / `×` mark, so the old claim was not re-confirmed) | 4 |
| 5_class.md:72 | `davāya \| noun \| masc.dat.sg \| for fun, for play \| √dū×1 a (go, run)` | 17 rows with `×` where the old audit's DB comparison has DPD's `･`: also 5:158, 8:51, 8:262, 8:476, 8:620, 9:21, 9:560, 11:170, 11:172, 11:336, 11:640, 12:492, 13:423, 13:425, 14:463, 14:484. (old D21) | DPD lookup | 5 |

## B. Tables, paradigms and lists that disagree with each other or themselves

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 2_class.md:91 | `iti'pi \| sandhi (iti + api)` | The sentence (line 86) writes `itipi`. (old 2.1) | One spelling | 8 |
| 3_class.md:56 | `sabba-rasaṃ \| noun \| masc.acc.sg` | Hyphenated in the table only; the sentence (line 51) writes `sabbarasaṃ dhammaraso`. The same for `joti-pālaṃ` (line 91) vs `jotipālaṃ` (line 85). (old 3.1) | Match the sentence | 6 |
| 4_class.md:26 | `3. [AN3.70](https://s.dhamma.gift/an/an3/index.html#an3.69)<br>abhisaṅkharoti kāyena kusalaṃ.` | Word order differs from the exercise (`kāyena kusalaṃ abhisaṅkharoti`, bpc_ex/4_class.md line 26); the exercise is marked `(simpl)`, the key is not. (old B1) | Align sentence and marker with the exercise | 6 |
| 4_class.md:291 | `saccaṃ bhavantaṃ gotamaṃ apucchimha` | The exercise (bpc_ex/4_class.md line 253) has `saccaṃ mayaṃ bhavantaṃ …`; the key drops `mayaṃ`. (old B2) | Align | 6 |
| 4_class.md:37 | `ime tilā ime taṇḍulā'ti` | The key ends `taṇḍulā'ti`, the exercise (bpc_ex/4_class.md line 37) `taṇḍulā (honti)`; the table has a row `(honti)` (line 54) for a word that is not in the key sentence, and no row for `iti`. (old B3) (old 4.5) | Align sentence and table with the exercise | 6 |
| 4_class.md:329 | `26. [MN86](https://s.dhamma.gift/mn/mn86/index.html) (simpl)<br>` | `(simpl)` in the key only; the exercise (bpc_ex/4_class.md line 286) has no marker. (old B5) | Align | 5 |
| 5_class.md:3 | `viññāṇaṃ na tumhākaṃ, taṃ pajahatha.` | The exercise (bpc_ex/5_class.md line 3) has `viññāṇaṃ, bhikkhave, na (hoti) tumhākaṃ`; the key drops `bhikkhave` and `(hoti)`. (old B6) | Align | 6 |
| 5_class.md:648 | `6. [SNP70](https://s.dhamma.gift/kn/snp/index.html#snp5.16) <br>te diṭṭhiṃ n'ābhijānāmi` | The exercise (bpc_ex/5_class.md line 556) marks the item `(simpl)`, the key does not. The text (Mogharāja) has `diṭṭhiṃ te nābhijānāti` (3rd sg: "the world does not know your view"), so the simplification changes the person. (old B5) | Add `(simpl)` | 6 |
| 6_class.md:3 | `bhagavā bhikkhū āmantesi, bhikkhavo'ti.` | The exercise sentence goes on with `"bhadante"ti`; the key stops at `bhikkhavo'ti`. (old B7) | Align | 6 |
| 6_class.md:104 | `8. [DN16.26](https://s.dhamma.gift/dn/dn16/index.html) (simpl)` | `(simpl)` in the key only; the exercise (bpc_ex/6_class.md line 95) has no marker. | Align | 5 |
| 6_class.md:308 | `atha \| ind \| \| then` | Empty Grammar cell; also `va \| ind \| \| as, like` (line 562). | `adv`; `emph`/`comp` as elsewhere | 8 |
| 6_class.md:323 | `ca \| ind \| conj \| and` | The sentence (line 317) has three `ca`, the table one row; at lines 577–587 the second `ca` (`ācariye ca`) has no row either. Repeated particles get their own rows elsewhere (lines 223–230). (old 6.5) | Add rows | 5 |
| 6_class.md:390 | `sukhitattā \| adj \| masc.nom.pl \| happy` | The sentence (line 378) writes `sukhit'attā`. (old 6.2) | One form | 8 |
| 7_class.md:162 | `anāgatamaddhānaṃ \| ind \| adv \| in the future` | The same phrase from the same sutta is `anāgatam'addhānaṃ` at lines 331 and 343. (old 7.4) | One spelling | 8 |
| 7_class.md:344 | `evaṃvedano \| adj \| masc.nom.sg \| having such feeling` | The second `siyaṃ anāgatam'addhānaṃ` of the sentence (line 331) has no rows, while repeated words get rows elsewhere. | Add the rows, or mark the repeat | 4 |
| 8_class.md:43 | `nāma-gottāni \| noun \| nt.acc.pl` | Hyphen in the table only; the sentence (line 33) writes `nāmagottāni`. The same for `abhijjhā-domanassaṃ` (line 146) vs `abhijjhādomanassaṃ` (line 123). (old 8.3) | Match the sentence | 6 |
| 9_class.md:53 | `nālaṃ \| ind \| neg \| not possible; not able` | The sentence (line 46) writes `n'ālaṃ`; the table `nālaṃ` (also lines 55, 57). | One spelling | 6 |
| 9_class.md:62 | `samudayāya. katamāni tīṇi?` | The question is in the key sentence but not in the table, the translation (line 74) or the exercise (bpc_ex/9_class.md line 45); item 6 (lines 101–114) does include its `katamāni cattāri`. (old B8) (old 9.1) | Remove, or add rows and "What three?" | 9 |
| 10_class.md:143 | `na ca kiñci loke upādiyati` | The key has `ca`; the exercise (bpc_ex/10_class.md line 113) has `na kiñci loke`. (old B11) | verify against SN35.234; align | 6 |
| 10_class.md:344 | `[SN12.22](https://s.dhamma.gift/sn/sn12/index.html#sn12.22) (simpl)` | `(simpl)` in the key only; the exercise (bpc_ex/10_class.md line 275) gives the same sentence without it. (old B5) | Align | 5 |
| 11_class.md:719 | `ca-assa \| verb \| opt.3rd.sg \| and he should be` | `cassa` (= `ca assa`) is one row with a hyphen, while the sentence's other `ca` has its own row (line 179). | Two rows: `ca`, `assa` | 5 |
| 11_class.md:543 | `sammāsaṅkappagocarā.` | The exercise (bpc_ex/11_class.md line 444) has `sammāsaṅkappe gocarā`; Dhp 12 has the compound, so the key is right. Exercise-side. (old B12) | Fix the exercise | 7 |
| 14_class.md:72 | `divasaṃsantatte ayokaṭāhe` | The sentence writes one word; the table splits it as `divasaṃ-` (line 77) with a compound hyphen and tags it `ind`; the exercise (bpc_ex/14_class.md) has `divasaṃ santatte`. | One compound `divasaṃsantatta` (DPD headword, adj, `divasaṃ + santatta`); one spelling in sentence, table and exercise | 6 |
| 15_class.md:162 | `kho, \| ind \| emph \| indeed; certainly` | The table for `imehi kho, bhikkhave, tīhi dhammehi samannāgato bālo veditabbo` (line 157) stops after two rows; six words have no row. Items 1 and 3 give full tables for their closing sentence. (old 15.1) | Add the rows, or a note that they repeat lines 102-107 | 7 |

## C. Translation and gloss problems

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 2_class.md:9 | `kira \| ind \| adv \| indeed, truly` | In SN10.8 Anāthapiṇḍika hears the news second-hand: `kira` marks hearsay ("it is said"). The translation (line 13) follows the gloss. (old 2.11) | "it is said; reportedly" (DPD kira 2); translation "A Buddha, it is said, has arisen in the world." DPD also has "really; truly" (kira 1), so the gloss is a possible sense: owner decision | 4 |
| 2_class.md:57 | `**the state of a superior human being, the attainment of knowing and seeing, suitable for a noble person,**` | `uttarimanussadhamma` is a state beyond the human (a "superhuman state"), not the state of a superior human; the rendering follows the drill split on line 45, not the compound. | "a superhuman state, a distinction in knowledge and vision worthy of the noble ones" (DPD uttarimanussadhamma: "super-human state") | 6 |
| 2_class.md:107 | `endowed with wisdom and ethical conduct` | The gloss of `vijjācaraṇasampanno` (line 96) says `knowledge and conduct`. (old 2.9) | Align ("knowledge and conduct") | 6 |
| 2_class.md:366 | `domanassa- \| noun \| - \| depression` | One word, several renderings: `domanassa` "distresses" (line 233), "depression" here, "displeasure" in the translation (line 370); `jarā` "old age" (line 361) vs "aging"; `upāyāsā` "afflictions" (line 367) vs "despair". (old 2.10) | One rendering per word within the item | 5 |
| 2_class.md:27 | `**At the foot of a tree in a forest, in valleys, and in caves.**` | `rukkhānaṃ` is gen.pl (line 21, "of trees"); the translation has a singular. (old 2.7) | "At the foot of trees in a forest, in valleys and in caves." | 6 |
| 3_class.md:120 | `**He experiences pleasure by means of the body.**` | `ca` (line 116) is left untranslated. (old 3.3) | "And he experiences pleasure with the body." | 5 |
| 3_class.md:345 | `**You see that offence.**` | In the Vinaya this line is a question put to the monk. (old 3.5) | "Do you see that offence?" | 4 |
| 3_class.md:237 | `(on tour) in the Mallans.` | `mallesu` with a verb of going is "to/among the Mallas"; "in the Mallans" is not idiomatic, and the people are usually called the Mallas and the Kosalans/Kosalas. | "sets out from the Kosalans to the Mallas (on tour)" | 4 |
| 4_class.md:22 | `upapajjāmi \| verb \| pr.1st.sg \| I am reborn; I go towards` | `upapajjati` + acc of a destination is "is reborn in"; the translation (line 24) chose the weaker "I go towards". (old 4.10) | "I am reborn in a good destination, a heavenly world." | 6 |
| 4_class.md:391 | `pessako \| noun \| masc.nom.sg \| messenger` | In MN98's list the sense is "servant"; `vāṇijo` is "merchant" (line 388) in the table but "a trader" in the translation (line 395). (old 4.13) | "servant" (DPD pessaka 2; "messenger" is pessaka 1, so both are DPD senses); one word for `vāṇija` | 5 |
| 4_class.md:35 | `**He does good deeds by means of the body.**` | `kusalaṃ` is singular (line 33). (old 4.14) | "He does a good deed by means of the body." | 5 |
| 4_class.md:408 | `**One is disenchanted in suffering, this [is] the path for purification.**` | Idiom: "disenchanted with". (old 4.14) | "One becomes disenchanted with suffering; this is the path to purification." | 5 |
| 4_class.md:463 | `**It was a thought of the recluse.**` | `ahu` + genitive is possession: "the recluse had a thought". (old 4.14) | "A thought arose in the recluse." / "The recluse had a thought." | 6 |
| 4_class.md:327 | `**May you all be happy (and) free from disease.**` | Order reversed against the sentence (`arogā sukhitā`). (old 4.14) | "May you all be healthy and happy." | 4 |
| 5_class.md:40 | `**Our lifestyle should be purified.**` | The same MN39 construction (`parisuddho no … bhavissati`) is "will be pure/purified" at line 375; the table (line 38) gives both "will" and "should". (old 5.17) | "Our livelihood will be purified." | 6 |
| 5_class.md:121 | `**False teaching leads to no good fortune, the Teaching leads to a good destination.**` | `nirayaṃ` is glossed `hell; no good fortune` (line 115); the translation uses the etymological gloss and loses the contrast with `suggatiṃ`. (old 5.13) | "False teaching leads to hell; the Teaching leads to a good destination." | 6 |
| 5_class.md:293 | `**Whatever conversation was with wandering ascetics,` | Ungrammatical. (old 5.18) | "Whatever conversation there had been with the wandering ascetics, …" | 6 |
| 5_class.md:348 | `**Services (done) on us could be of great fruits.**` | `bhavissanti` is future (line 346 has "could be" as a second gloss); "fruits" for "fruit". (old 5.18) | "Services done for us will be of great fruit." | 6 |
| 5_class.md:572 | `kadariyaṃ \| noun \| nt.acc.sg \| stinginess` | In Dhp 223 it parallels `alikavādinaṃ`, a person ("the liar"); `kadariya` is also an adjective "miserly". The translation (line 578) has "conquer liar by truth". (old 5.5) | `adj \| masc.acc.sg \| the miser` (DPD kadariya 1 adj "miserly"; the nt noun "miserliness" is kadariya 2, so the tag is also a DPD reading); "Conquer the miser by giving, the liar by truth." | 6 |
| 5_class.md:627 | `**You are truly for us equal to the Brahma.**` | Word order, article, diacritic. (old 5.16) | "Truly, for us you are equal to Brahmā." | 6 |
| 5_class.md:667 | `brāhmaṇa \| noun \| masc.voc.sg \| monk; sage; holy man` | Rendered "Monk" in the translation (line 678). In SN40.1 the Buddha addresses Moggallāna, so the choice is defensible, but "monk" is not a sense of `brāhmaṇa`. (old 5.12) | "brahmin" with a note on the addressee | 4 |
| 6_class.md:212 | `**"(He) who is equanimous [and] mindful lives at ease."**` | `sukhavihārī` is an adjective, the third item of a list (`upekkhako satimā sukhavihārī`), not a finite verb. | "Equanimous, mindful, one who lives at ease." | 4 |
| 6_class.md:437 | `would approach [there], cause an alteration in a robe…` | The futures (glossed "will", lines 432, 435) are rendered "would"; the two clauses have no "and". (old 6.13) | "If that monk … will approach and cause an alteration in a robe…" | 5 |
| 6_class.md:482 | `**The looking after mother and father, the support of the wife and son.**` | The Pāli order is son, then wife; "The looking after mother" lacks "of". (old 6.14) | "Looking after mother and father, supporting son and wife." | 5 |
| 6_class.md:498 | `**Just make an effort today;` | `eva` qualifies `ajja`: "this very day". (old 6.15) | "Make an effort this very day;" | 5 |
| 6_class.md:570 | `who sees fault, he is (like) one who points out the treasure.**` | Comma splice; `nidhīnaṃ` is gen.pl (line 561, "of treasures"). (old 6.11) | "…who sees faults, like one who points out treasures." | 6 |
| 6_class.md:580 | `atho \| ind \| ind \| and then; after that` | `atho` here adds an item ("and also"); it is not temporal. The translation (line 589) says "and after that". (old 6.12) | "and also"; "and also towards the eldest brother" | 5 |
| 7_class.md:83 | `**How then could thieves not steal my valuables?**` | `kinti … na corā hareyyuṃ` expresses concern or purpose ("how can I make sure thieves don't take my wealth?"); the English reads as surprise that they could not steal it. | "How can I make sure that thieves do not steal my possessions?" | 5 |
| 7_class.md:242 | `**And now there could be, Ananda, for you it would occur like this:` | `siyā` and `assa` both rendered; the sentence breaks. (old 7.17) | "Now, Ānanda, it could be that you think thus:" | 5 |
| 7_class.md:311 | `which I am grasping [and] would not be with faults` | `upādiyamāno` is subordinate to `assaṃ`, not a coordinate verb. (old 7.16) | "…which, grasping it, I would not be blameworthy." | 6 |
| 7_class.md:462 | `**Bhikkhus, the monks will establish mindfulness individually` | `bhikkhave` and `bhikkhū` are rendered two ways in one line; the quoted clause is a question in the Pāli. (old 7.19) | "Monks, the monks will…" | 5 |
| 7_class.md:500 | `**What one could do with a well, if there always would be water?; Having cut off the craving from the source, why would he go about searching?**` | Word order; `?;`; `taṇhāya` is tagged gen (line 493) but translated as the object. (old 7.20) | "What could one do with a well if there were water at all times? Having cut craving at the root, why would one go about searching?" | 6 |
| 7_class.md:519 | `parihāyanti \| verb \| pr.3rd.pl \| wasting away; decreasing` | Participle gloss for a finite verb. (old 7.20) | "they decline; they fall away" | 6 |
| 8_class.md:348 | `**This monk who speaks according to the Dhamma, and this monk who speaks according to the Vinaya, speaks according to (i.e. in accordance with) our preference and approval…**` | Three coordinated predications ("this monk is a speaker of Dhamma, … of Vinaya, … speaks taking up our wish") are turned into one relative clause. (old 8.12) | "This monk speaks according to the Dhamma, this monk speaks according to the Vinaya, and this monk speaks with our consent and approval…" | 6 |
| 8_class.md:388 | `having done this just for that reason, [and] no other` | `etaṃ eva paccayaṃ karitvā anaññaṃ` is "having made just this the reason and no other"; `eva` is glossed `thus; just` (line 382), but it is not "thus". (old 8.13) | "having made just this, and nothing else, the reason" | 6 |
| 8_class.md:441 | `sabbanimittānaṃ \| noun \| nt.gen.pl \| of all objects` | The same stem `nimitta` is "signless" (`animitta`, lines 438, 444); "objects" hides the link. (old 8.15) | "of all signs" | 4 |
| 8_class.md:590 | `that monk can set [it] aside for a month at the most` | `nikkhipeyya` is glossed "should set aside" (line 583); the translation says "can". (old 8.15) | "should set it aside" / "may keep it" | 4 |
| 8_class.md:567 | `**He generates interest, puts forth effort, arouses energy, exerts his mind and strives for the continuance, non-disappearance , increase and fulfillment by development, maturity, of wholesome qualities that have arisen.**` | The order of the datives is garbled, and `bhāvanāya` is tagged dat (line 556) but translated "by". (old 8.14) | "…for the persistence, non-decay, increase, abundance, development and fulfilment of wholesome qualities that have arisen." | 6 |
| 8_class.md:636 | `dhammo \| noun \| masc.nom.sg \| the teaching; the doctrine` | In `kocideva dhammo samuppādo uppajjeyya` `dhammo` is "a matter, an issue"; the translation (line 646) adds "[concerning] the teaching". | "some matter (dispute) could arise" | 4 |
| 9_class.md:225 | `**Seeing danger in the slightest fault, train yourself [by] undertaking the training precepts.**` | `vajjesu` is plural; the locative `sikkhāpadesu` ("in the training rules") is lost; "precepts" vs the gloss "rules" (line 223). (old 9.19) | "Seeing danger in the slightest faults, undertake and train in the training rules." | 5 |
| 9_class.md:698 | `I, too, will myself be able to make safety.**` | `api` goes with `ekam'ekena` ("even by a single one"); `attānaṃ sotthiṃ kātuṃ` is "to make myself safe". (old 9.17) | "…even by a single one of these eleven doors to the deathless, I will be able to make myself safe." | 6 |
| 9_class.md:710 | `anissito \| pp \| masc.nom.sg \| unhindered; independent (of)` | In context "unsupported"; "independent" (also in the translation, line 715) hides why he cannot cross. (old 9.18) | "unsupported" | 6 |
| 10_class.md:61 | `passeyyaṃ \| verb \| opt.1st.sg (reflexive) \| I could see by myself` | The tag is right (DPD: `passati` reflx opt 1st sg; the verify_key IMPOSSIBLE flag comes from the `(reflexive)` wording), but the reflexive ending does not mean "by myself". The translation (line 65) repeats "I myself" and drops the implied quote after `ākaṅkhati` ("If he wishes: 'May I see…'"). | "I could see"; "If he wishes, [he thinks:] 'I could see beings…'" | 6 |
| 10_class.md:176 | `eva \| ind \| emph \| just; thus` | `eva` is not "thus", yet the translation (line 179) says "thus". Gloss and translation also disagree for `parinibbāyati` ("is completely quenched", line 177, vs "attains final liberation") and for `paritassati`/`aparitassaṃ` ("perturbed" vs "shaking", lines 168, 174). (old 10.15) | "just"; align glosses with the translation | 6 |
| 10_class.md:354 | `sampassamānena \| prp \| masc.instr.sg \| by means of seeing; considering` | With `alaṃ` the instrumental marks the person for whom it is fitting: "for one who considers… it is fitting to strive"; the translation (line 360) keeps "by considering". (old 10.14) | "for one considering" | 6 |
| 10_class.md:409 | `āpajjato \| prp \| masc.dat.sg<br>(or) <br>masc.gen.sg \| for arousing; <br>(or) when exhibiting` | Two different verbs in one gloss; with `parivīmaṃsaṃ` the verb is "engages in, undertakes" (the translation, line 414, has "exhibiting"). (old 10.18) | "engaging in" | 6 |
| 10_class.md:459 | `this is my instruction to them.**` | `evarūpī` ("of such a kind", line 455) is not translated. (Old 10.18 also said "this" is not in the Pāli; it is: `ayaṃ`.) (old 10.18) | "…for them my instruction is of this kind." | 6 |
| 10_class.md:558 | `idaṃ \| pron \| nt.nom.sg \| that; lit. this` | One word glossed three ways in one sentence ("that; lit. this", "this" line 566, "that" line 571); also `amutra` "there" / "in such-and-such place" (lines 744, 748) and `imesaṃ` "of those" / "to these" (lines 746, 752). (old 10.17) | Align | 6 |
| 10_class.md:816 | `searching the builder of this house` | "searching for"; "this" is not in the Pāli (`gahakāraṃ`). (old 10.18) | "seeking the house-builder" | 6 |
| 11_class.md:71 | `hoti \| verb \| pr.3rd.sg \| there is; there was` | "there was" is not a present-tense gloss. (old 11.18) | "there is" | 6 |
| 11_class.md:144 | `**The foolish, untrained, wicked man maintains himself injured and damaged.**` | Gloss and translation disagree: `asappuriso` "not a good man" (line 138) vs "wicked man"; `pariharati` "carries around" (line 142) vs "maintains". | Align | 5 |
| 11_class.md:158 | `adhunā- \| ind \| adv \| soon, recently` | "soon" is wrong. Also `yassa` "of which; whoever" (line 697) is "whose"; `ye`/`yo` "which" for persons (lines 649, 653, 657); `sāsane` "the teachings" (line 587) lacks "in". (old 11.20) | "recently, just now"; "whose"; "who"; "in the teaching" | 6 |
| 11_class.md:346 | `[that] which [is] near or far away` | Order reversed (`dūre santike`). Also "about Venerable Gotama" (line 31) leaves `taṃ` out, and "straight, upright" (line 179) loses the `su-` of `suhujū`. (old 11.21) | "far or near"; "very upright" | 5 |
| 11_class.md:433 | `**For one perceiving acquisition as a personal acquisition of forms` | The genitive chain is attached to the wrong noun, and "personal" has no source. (old 11.16) | "For one regarding the acquisition of forms … as an acquisition…" | 6 |
| 11_class.md:451 | `**The teaching by the Blessed One [is] well taught,` | `bhagavatā` goes with `svākkhāto`: "well proclaimed by the Blessed One is the Dhamma". | "Well proclaimed by the Blessed One is the Dhamma…" | 6 |
| 11_class.md:630 | `‘that which the world [is] the self (world = self);` | Garbled: `so loko so attā` is "that [which is] the world, that [is] the self"; the third `so` is untranslated. (old 11.15) | Reword | 7 |
| 12_class.md:13 | `api \| ind \| \| just only` | `pi` is "also, even", not limiting, yet the item glosses "just two" … "just one hundred thousand births" (lines 15–28); in item 21 `api` is "only" (lines 471, 485, 489) and "even" (lines 475, 493) in one sentence, and the translation (line 499) says "just one year". The Grammar cell is empty. (old 12.16) | "even; also" | 6 |
| 12_class.md:92 | `bhikkhu-satehi \| noun \| nt.instr.pl \| with one hundred monks` | A plural ("hundreds"); also `sahassānaṃ` "for one thousand" (line 366). (old 12.15) | "with hundreds of monks"; "thousands" | 6 |
| 12_class.md:514 | `aṭṭhakavaggikāni \| adj \| nt.acc.pl \| from the fourth chapter of the Sutta Nipāta` | The translation (line 520) has "belonging to the groups of eight", which reads as a count, not the Aṭṭhakavagga. | "…all sixteen [suttas] of the Aṭṭhakavagga" | 6 |
| 12_class.md:631 | `having then seen that should speak` | "then" has no source; `tam'enaṃ` is "him" (so the table, line 617). (old 12.14) | "having seen him, should speak…" | 6 |
| 12_class.md:641 | `vanappagumbe \| noun \| masc.loc.sg \| forest grove` | Tagged locative (also `phussit'agge`, line 643), but the translation (line 654) makes it the subject of the simile. (old 12.8) | Tag and translation should agree | 5 |
| 12_class.md:646 | `gimhe \| noun \| masc.loc.sg \| in heat; hot` | `paṭhamasmiṃ gimhe` is "in the first month of summer", not "the first heat of the hot month" (line 654); the translation also drops `tath'ūpamaṃ` and attaches `paramaṃ` to Nibbāna. (old 12.13) | "in the first month of summer"; "so too he taught the sublime teaching leading to Nibbāna, for the highest benefit" | 6 |
| 13_class.md:30 | `**He touches the earth evenly with the entire sole of [his] foot**` | `pādatalehi` is plural ("soles of [his] feet"), as the gloss (line 26) says; `samaṃ` is "evenly" (line 13) but "in a balanced manner" (line 20). (old 13.20) | "…with the entire soles of [his] feet"; "evenly" throughout | 6 |
| 13_class.md:133 | `bhante \| noun \| masc.voc.sg \| lord, master` | "venerable sir" everywhere else; the translation (line 137) says "Master". | "venerable sir" | 5 |
| 13_class.md:234 | `tassa \| pron \| masc.dat.sg \| for this` | "that"; also `lokasmiṃ` "the world" without "in" (line 337) and `assā'ti` "would he" (line 240), a fragment with no end-quote note. (old 13.21) | "for that"; "in the world" | 6 |
| 13_class.md:300 | `**for what [is] pleasant and enticing in the world this craving here` | `yaṃ` is nominative, there is no "for"; the adjective order is swapped against the table; "is ceased" (see the row above). (old 13.17) | "Whatever in the world is enticing and pleasant: here this craving, being abandoned, is abandoned; here, ceasing, it ceases." | 7 |
| 13_class.md:501 | `(a helper) should come up with that robe cloth` | In NP 10 the subject of `abhinipphādeyya` is the monk who stands silently; the translation invents another subject. (old 13.18) | "…he should get that robe cloth produced" | 6 |
| 13_class.md:545 | `**He [is one] who makes subside evil deeds` | `ca` dropped and `sabbaso` moved to the second clause; at line 451 the table has `ca` but the translation "or". (old 13.22) | Reword | 5 |
| 14_class.md:19 | `**He causes this very body to overflow, to flow around, to fill up all around, to suffuse with the joy and happiness born from separation` | `parippharati` (line 17) is plain `verb`, not causative; "this very body … to suffuse" reverses who suffuses what; "happiness" and "separation" against the glosses "ease" (line 13) and "solitude" (line 12). (old 14.22) | "He drenches, steeps, fills and suffuses this very body with the joy and ease born of solitude." | 6 |
| 14_class.md:98 | `eva \| ind \| \| only` | In `c'eva … na ca` ("both … and not") `eva` does not mean "only"; the Grammar cell is empty. `c'eva` is analysed three ways in this file (`ca-` + `eva` lines 97-98, `ind+ind` line 395, `ind+emph` line 644), as are `atha kho` (lines 26, 61 against 686-687) and `yo pana bhikkhu` (line 303 against 306-308, 507-509). (old 14.30) | One analysis per phrase; `c'eva` "both" | 7 |
| 14_class.md:165 | `**Just this is the end of the underlying tendency towards conflict.**` | `anusayānaṃ` (line 163) is plural; at line 653 `c'eva … ca` is "both … and", not "and even". (old 14.24) | "…of the underlying tendencies to aversion"; "both unarisen taints do not arise and arisen taints are abandoned" | 6 |
| 14_class.md:292 | `āsavānaṃ \| noun \| masc.gen.pl \| of impurities, defilements` | `āsava` is "effluents; taints" at lines 645, 650, 675; `sutte` "scripture(s)" (lines 390, 394) against "discourse(s)" (line 699); `pācittiyaṃ` "a case requiring confession" (line 315) against "an offence" (line 591); four wordings of the two robes (lines 580-585). (old 14.28) | One rendering each | 6 |
| 14_class.md:368 | `āvuso \| ind \| voc.sg \| friend` | In MN18 Mahākaccāna addresses a group of monks; also the translation (line 381). (old 14.12) | "friends" | 6 |
| 14_class.md:475 | `**they will practise accepting the training rules as they had been formulated.**` | The third condition of the `yāvakīvaṃ` clause reads as a main clause; "had been" is the wrong tense. (old 14.23) | "[and] will proceed, having undertaken the training rules as they have been laid down," | 6 |
| 14_class.md:522 | `pan'idaṃ \| ind \| ind+pron \| moreover` | `idaṃ` is lost in the gloss, and `taṃ` (line 520) is glossed "this" to make up for it. (old 14.26) | "moreover, this"; `taṃ` "that" | 6 |
| 14_class.md:624 | `**He doesn't know the things that should be adhered to, he doesn't know the practices that should not be adhered to.**` | `dhamme` is "things" and "practices" inside one sentence (also line 611); `padabyañjanāni` "words and letters" (line 691) but "words and phrases" (line 695). (old 14.25) | Align | 7 |
| 15_class.md:189 | `**Monks, speech endowed with five factors is well-spoken` | `aṅgehi` is "factors" here and "these five qualities" in the closing sentence (line 250); glosses "parts, factors; qualities" (line 176) against "qualities" (line 237). (old 15.12) | One rendering | 6 |
| 15_class.md:268 | `kittāvatā \| ind \| adv+interr \| in what way` | The correlative `ettāvatā` (line 400) is "to this extent"; also the translation (line 275). (old 15.10) | "to what extent" | 6 |
| 15_class.md:312 | `**Certainly, for one seeing the source of the world as it truly is` | Vocative `kaccāna` (line 301) is left out here and at line 331, but translated at lines 344 and 406. (old 15.11) | Add "Kaccāna" | 6 |
| 15_class.md:432 | `**"Everything does not exist": this is the second extreme.**` | `sabbaṃ n'atthi` is "nothing exists"; "everything does not exist" reads as "not everything exists". | "'Nothing exists': this is the second extreme." | 6 |
| 5_class.md:678 | `**Monk, don't be careless about meditation` | Recurring terms rendered several ways: `brāhmaṇa` as Brahman / brahmin / priest / holy man and "Monk" here; `dhammavinaya` five ways; `samaṇa` ascetic / recluse / monk; `mettā`; `Venerable sir` / `venerable sir` / `Venerable Sir`; names without diacritics (`Ananda`, `Sariputta`, `Kalamas`). UK and US spelling mixed (`honor`/`honour`, `practiced`, `offence`): a recurring owner-decision topic. (old E18) | A short glossary; spelling: owner decision | 6 |

## D. English typos and grammar

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 2_class.md:57 | `**the state of a superior human being, the attainment of knowing and seeing, suitable for a noble person,**` | Lower-case start and a trailing comma; every other translation line ends without a comma. | Capitalise; end with a full stop | 6 |
| 2_class.md:302 | `O, brahmin!` | Comma after the vocative particle; also line 304. | "O brahmin!" | 6 |
| 3_class.md:383 | `bhāsitassa \| noun \| nt.gen.sg \| statement` | Genitive gloss without "of"; `etassa` on line 382 has it. (old 3.4) | "of the statement" | 6 |
| 3_class.md:304 | `come on!; come now! let's!` | Mixed `!;` and a missing separator before `let's!`. (old 3.6) | "come on; come now; let's" | 6 |
| 4_class.md:351 | `ariyassa \| adj \| masc.gen.sg \| of noble` | Truncated gloss; `samādhissa` (line 352) has no "of". (old 3.4) | "of the noble"; "of stillness, composure" | 6 |
| 5_class.md:308 | `"alaṃ, gāmaṇi. mā maṃ etaṃ pucchi` | Opening quotation mark never closed. (old 5.4) | Remove `"` or close it | 8 |
| 6_class.md:167 | `lit: one having eyes quality` | Unidiomatic; also `lit. breathing being` (line 94) for a plural. (old 6.16) | "lit. possessing eyes"; "lit. breathing beings" | 6 |
| 8_class.md:294 | `bārāṇasiyaṃ \| noun \| fem.loc.sg \| in Varanasi` | Modern spelling; the course writes Pāli names with diacritics elsewhere (`Isipatana`, `Ānanda`). | "in Bārāṇasī" | 5 |
| 8_class.md:380 | `hotī"ti \| verb \| pr.3rd.sg \| there is` | The sentence (line 368) has a closing `"` with no opening one; a double quote inside a table word; the sandhi vowel is long here but short in `hoti"ti` at 15_class.md line 273. (old 8.2) (old F10) | Open the quote in the sentence; one treatment (`hotī'ti`) in both classes. Class 8 done 2026-11-25; class 15 left: there the `"` closes a real quotation | 7 |
| 10_class.md:589 | `samanupassato \| prp \| masc.gen.sg<br>(gen abs) (or)<br>masc.dat.sg \| when sees; perceives (or)<br>for one seeing` | "when sees" has no subject. | "when he sees; perceives" | 6 |
| 11_class.md:498 | `'khīṇā jāti vusitaṃ brahmacariyaṃ` | An opening quote that is never closed, carried into the table cell `'khīṇā` (line 516). (old 11.2) | Remove it, or close it | 7 |
| 11_class.md:595 | `diṭṭhiṭṭhānaṃ, — so loko so attā` | Comma plus dash, twice in the sentence; the closing `'ti` of `ṭhassāmī'ti` has no opening quote. (old 11.3) | Tidy | 6 |
| 12_class.md:48 | `there could be hen's eggs` | The supplied words are not in brackets. Also "I will clarify" (line 564) for the present `āvikaromi`, and "knowledge and vision were not" (line 296) for a singular. (old 12.17) | "[there were] a hen's eggs"; "I clarify"; "was not" | 5 |
| 13_class.md:617 | `yato tvaṃ, bāhiya, na tena tato tvaṃ, bāhiya, na tattha` | Comma missing after the second `na tena` (the parallel has one); `"ti` at the end has no opening quote. (old 13.6) | Add the comma | 6 |

## E. Markdown defects that affect rendering

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 2_class.md:314 | `**[Good are] friends in [arisen] need <br>[Good are] friends when need [arises]**` | Bold spans a `<br>`; two alternative translations in one bold line. | Bold each line separately, or keep one translation | 6 |
| 3_class.md:386 | `**It would be good if the meaning of this statement may become evident to Venerable Sāriputta. (so that he could explain it to us)<br>fig: It would be good if Ven. Sāriputta would explain the meaning of this statement.**` | Bold spans a `<br>`; a bracketed clause stands after the full stop. (old 3.6) | Bold each line; put the bracket before the full stop | 7 |
| 4_class.md:436 | `**Practice for restraint of the body (faculty), guard the body (faculty), <br>arouse restraint in regard to the body (faculty).**` | Bold spans a `<br>`. | Bold each line, or drop the `<br>` | 7 |
| 8_class.md:266 | `**Having shaved hair and beard, and having clothed myself in brown robes, let me go forth from the household life to homelessness. <br>[What if I shave hair and beard, clothe myself in brown robes and go forth…?]**` | Bold spans a `<br>`. | Bold each line | 7 |
| 6_class.md:54 | `**This is a common Pāli idiom.**` | Notes and sub-headings in bold exactly like a sentence translation: also `**passive verbs:**` (13_class.md line 77), `**Potential Participles**` (14_class.md line 130), `**(or)**` (14_class.md line 580), `**Translation Assignment**` (15_class.md line 3). (old A17) | Plain text or a heading | 6 |

## F. Convention drift

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 1_class.md:11 | `sammā - \| ind \| adv` | Space before the hyphen. The sentence (line 3) writes `sammā-sambuddhassa`; class 2 (2_class.md line 95) keeps the whole compound `sammāsambuddho`. (old 1.1) | `sammā-`; one treatment of the compound across classes | 7 |
| 2_class.md:134 | `**for dispassion, for cessation**` | Phrase translations start lower case here and at lines 143, 162, 202, 211, 223, 266, but capitalised at lines 116, 125, 172, 245. | One style | 4 |
| 3_class.md:1 | `# Class 3 Key to Exercises` | No blank line between the heading and item 1 (line 2); every other key file has one. (old A3) | Add a blank line | 6 |
| 3_class.md:92 | `young gentleman, Brahman` | The translation (line 95) writes `(brahmin)`; the course elsewhere writes "brahmin". (old 3.6) | "young brahmin" | 7 |
| 4_class.md:128 | `amha- \| verb \| pr.1st.pl \| we are` | The hyphen marks compound stems elsewhere; here it is on a finite verb shortened in sandhi (`amhā'ti`, line 122). (old 4.3) | `amha` | 6 |
| 5_class.md:518 | `añña'd'atthu \| ind \| adv` | Two elision marks inside one indeclinable (`aññadatthu`), also in the sentence (line 506). | `aññadatthu` (DPD headword, `añña + [d] + atthu`), unless the marks are a deliberate sandhi notation: owner decision | 5 |
| 6_class.md:219 | `thero \| adj \| masc.nom.sg \| elderly; senior` | The same word is `noun` at lines 270 and 287 (`therā`, `there`). | One POS | 5 |
| 7_class.md:76 | `kinti \| ind \| pron+ind \| how then` | The sentence (line 71) writes `kin'ti`; the same word is tagged `interr` at line 448. (old 7.2) | `kin'ti`; one tag | 8 |
| 7_class.md:135 | `vā \| ind \| - \| or` | The Grammar cell of a particle is `-` here (also lines 118, 137, 139), `conj` at line 322, and empty at lines 199, 429, 431, 470. | `conj` (or the class's usual label) throughout | 7 |
| 7_class.md:184 | `yaṃnūn'āhaṃ \| idiom \| ind+pron.1st.nom.sg` | The same idiom is `yan'nūn'āhaṃ` with `pron+ind+pron.1st.nom.sg` at 8_class.md lines 251, 256 (and in class 13, line 48). (old 7.5) | One spelling and one analysis | 8 |
| 7_class.md:399 | `yāva'd'eva \| ind \| ind+adv` | Two elision marks inside one indeclinable (`yāvadeva`); also the sentence (line 394). | `yāvadeva` (DPD: `yāva + [d] + eva`), unless the marks are a deliberate sandhi notation: owner decision | 5 |
| 8_class.md:168 | `etad- \| pron \| nt.acc.sg \| this` | A hyphen marks a compound stem elsewhere; here it marks sandhi with `avoca` (sentence `etadavoca`, line 150). Class 6 writes `etad` (6_class.md line 157). | `etad` | 5 |
| 9_class.md:101 | `pañha-vyākaraṇāni` | The exercise (bpc_ex/9_class.md line 73) writes `pañhabyākaraṇāni`. (old B9) | One spelling (`pañhabyākaraṇāni`) | 6 |
| 9_class.md:155 | `yaṃ nūna \| pron+ind \| interr \| what if, let's` | A third spelling and analysis of the idiom: `yaṃnūn'āhaṃ` (7_class.md line 184) and `yan'nūn'āhaṃ` (8_class.md line 256). | One spelling and one analysis | 6 |
| 10_class.md:137 | `ca \| ind \| \| and, but` | Empty Grammar cell; `ca` is `conj` elsewhere in the class (lines 157, 368). Also `yāvatā-` (line 726). | `conj` | 6 |
| 10_class.md:190 | `atthaṅ'gate \| pp \| masc.loc.sg<br>(loc abs)` | An elision mark inside the compound `atthaṅgata` where nothing is elided; same in the sentence (line 181). | `atthaṅgate` (DPD headword atthaṅgata, `atthaṃ + gata`), unless the mark is a deliberate sandhi notation: owner decision | 4 |
| 10_class.md:214 | `passasāmī'ti \| verb \| pr.1st.sg + quote` | `+ quote` in the Grammar column here, not in the twin row at line 208; at lines 253 and 257 it sits in the English column (`I will breathe in + quote`). | One place, or drop it | 6 |
| 10_class.md:224 | `seyyathāpi \| ind \| pron+adv+ind \| just like` | A construction in the Grammar column; line 94 has `seyyathāpi \| ind \| -`. | `-` | 5 |
| 10_class.md:715 | `yāvat'āssa vigatamiddho` | The mark implies `yāvat` + `āssa`; the table splits `yāvatā-` + `assa` (lines 726, 727). (old 10.3) | Match the table (`yāvatā'ssa`) | 5 |
| 10_class.md:728 | `(or) \| pron \| masc.dat.sg \| for him` | `(or)` stands in the Pāli column as if it were a word; also line 730. Line 377 gives alternatives inside the cell. (old A10) | Use the in-cell `(or)` pattern of line 402 | 7 |
| 11_class.md:52 | `seyyathāpi \| ind \| \| just like, as` | Empty Grammar cell; the same word has `pron+adv+ind` at lines 122 and 242. `vā` has `disj` (lines 333, 335), `conj` (line 57) and an empty cell (lines 184, 186). | One value per word | 5 |
| 11_class.md:110 | `sampajāna-kārī \| adj \| masc.nom.sg` | Hyphen in the table, none in the sentence (`sampajānakārī`, line 101); also `sammāsaṅkappa-gocarā` (line 557) against the sentence's `sammāsaṅkappagocarā`. | Match the sentence | 6 |
| 11_class.md:137 | `abyatto \| adj \| masc.nom.sg \| untrained \| √añj･8 \*aya (distinguish)` | Sign `*aya` here; `byattaṃ` has `√añj･8 *e` (10_class.md line 645). This line follows DPD (abyatta, √añj \*aya); `byatta` was not looked up. | DPD lookup (byatta) | 3 |
| 11_class.md:202 | `aniccato \| ind \| adv \| as impermanent` | The same "-to = as X" form is `ind \| adv` here and at lines 204–210, 369–379, but `noun \| masc.abl.sg` for `paṭilābhato` (line 430) and `accayato` (line 533). (old 11.14) | One tag | 6 |
| 11_class.md:237 | `seyyathā'pi suddhaṃ vatthaṃ apagataṃ kāḷakā` | Sentence `seyyathā'pi`, table `seyyathāpi` (line 242); also sentence `vigat'ūpakkilese` (line 471) vs table `vigatūpakkilese` (line 482). (old 11.1) | Match | 8 |
| 11_class.md:276 | `[AN4.61](https://s.dhamma.gift/an/an4/index.html#an4.61)(simpl)` | No space before `(simpl)`; every other `(simpl)` in the class has one (lines 250, 304, 453). | `… (simpl)` | 5 |
| 11_class.md:704 | `maṅgalam \| noun \| nt.nom.sg \| blessing` | The table keeps the sandhi `-m` of `maṅgalam'uttamaṃ`; the same phrase in class 10 has `maṅgalaṃ` (10_class.md line 709). | `maṅgalaṃ` | 5 |
| 12_class.md:13 | `api \| ind \| \| just only` | `ekam'pi` is split into `ekaṃ` + `api` (lines 12–13), while `dve'pi`, `tisso'pi` … `jātisatasahassam'pi` (lines 15–28) keep the `'pi` in one row. | One way | 5 |
| 12_class.md:50 | `evam'eva kho, bhikkhave, ayaṃ dhammavinayo` | Sentence `evam'eva`, table `evameva kho` (line 66). (old 11.1) | Match | 8 |
| 12_class.md:91 | `pañca-mattehi \| adj \| nt.instr.pl \| with five in number; five measures` | Hyphens in the table that the sentence (line 75) does not have: also `bhikkhu-satehi` (line 92), `an-uppanno` (line 118), `yathā-idaṃ`, `paṭigha-nimittaṃ` (lines 126, 128; sentence `yathayidaṃ`, `paṭighanimittaṃ`), `ariya-saccāni.` (line 140). | Match the sentence | 6 |
| 12_class.md:389 | `samanta'pāsādiko \| adj \| masc.nom.sg` | An elision mark where nothing is elided; also in the sentence (line 377). (old 12.4) | `samantapāsādiko` (DPD headword samantapāsādika, `samanta + pāsādika`), unless the mark is a deliberate compound notation: owner decision | 5 |
| 12_class.md:478 | `tīṇi \| card \| nt.acc.pl \| three (3)` | Digits in brackets in this item only (lines 478–488). (old 12.19) | Remove them | 5 |
| 12_class.md:532 | `seyyath'idaṃ \| ind \| pron+adv+pron \| namely; that is` | `seyyath'idaṃ` here and in the sentence (line 522), `seyyathidaṃ` in item 1 (lines 3, 11). | One spelling | 5 |
| 13_class.md:312 | `samanuyuñjiyamāno \| prp. pass \| masc.nom.sg \| being cross-questioned by \| √yuj･2 ṃa + iya (yoke, join)` | The passive sign is written four ways in the class: `ṃa + iya` here, `iya` (lines 192, 313, 314), `īya` (lines 294, 295), `ya` (line 86 and most others). | One notation | 5 |
| 14_class.md:32 | `etadavoca \| verb \| aor.3rd.sg \| he said this` | The sentence (line 21) has `etad'avoca`; likewise the table has `tasmā't'iha` (line 137) against `tasmātiha` in the sentence (line 132). (old 14.3) | Match | 5 |
| 14_class.md:97 | `ca- \| ind \| conj \| and, but` | Trailing hyphen on sandhi-split words that are not compound members: also `evaṃ-` (line 263), `cattāro-` (line 278). (old 14.5) | Drop the hyphen | 6 |
| 14_class.md:311 | `√sic･2 ṃa (sprinkle, pour)+ ṃa \> siñca+eyya` | Free-form derivation inside the Root cell (also line 313); no other Root cell in the folder does this. (old D19) | `√sic･2 ṃa (sprinkle, pour)` | 7 |
| 14_class.md:319 | `sampajānamusāvādo assa hoti` | The rule reads `sampajānamusāvādassa hoti`; the Pāli line prints the commentarial resolution `-vādo assa` without saying so. Same silent resolution: `vā assa` (line 529), `evaṃ assa` (line 554), `rāgaṃ ca dosaṃ ca, avijjaṃ ca` (line 655), `ṭhānaṃ etaṃ` (line 361), `idha ahaṃ` (line 706); the file keeps `kathañ'ca` (line 180) and `evañ'ca` (line 258). (old 14.2) | One convention, or mark the resolution | 5 |
| 14_class.md:399 | `sandissanti \| verb. pass \| pr.3rd.pl (+loc)` | Root `√dis･1 iya`: passive sign `iya` where the key's convention is `ya` (`√vac･1 ya`, line 820); also `√vatt･1 iya` (line 285), `√hā･1 īya` (line 651). Folder count in the cross slice. (old D17) | `√dis･1 ya` | 6 |
| 14_class.md:535 | `pana \| ind \| ind \| but; and so` | The same word in the same rule formula is `ind \| conj` at line 325; `ce` is `ind \| cond` at lines 345, 389, 587 but has an empty Grammar cell at line 150. | One Grammar value each | 6 |
| 14_class.md:864 | `vuṭṭhāpiyamānaṃ \| prp \| masc.acc.sg [+instr]` | Causative passive by its own Root cell (`\*āpe + iya`; also `saṃvesiyamānaṃ`, line 866) without the label that `bhāviyamānā` (line 283) and `otāriyamānāni` (line 391) carry; `ārādhayiṃsu` (line 716, `\*aya`) is plain `verb` while `vivattayi` (line 832) is `verb.caus`. (old 14.14) | `prp.caus.pass`; `verb.caus` | 6 |
| 15_class.md:185 | `ananuvajjā \| adj, <br>(\<ptp)` | One POS written three ways in one item: `adj(\<ptp)` (line 183), `adj (\<ptp)` (line 244), `adj, <br>(\<ptp)` (here and line 246). | `adj (\<ptp)` | 6 |
| 15_class.md:221 | `metta- \| adj \| masc (in comp)` | A gender on a compound-member adjective whose head (`cittena`) is nt; `attha-` (line 216) has `masc. (in comp)` with a full stop. (old 15.6) | `in comp` | 6 |
| 15_class.md:256 | `"dvayanissito kho ayaṃ, kaccāna, loko yebhuyyena — atthitaṃ ca eva n'atthitaṃ ca.` | SN12.15 has `khvāyaṃ`, `atthitañceva natthitañca`, `tañcāyaṃ`, `dukkhameva`, `ñāṇamevassa`; item 4 prints every sandhi resolved without saying so, while item 1 shows its resolutions in brackets (line 9). | verify; mark the resolutions as in item 1 | 4 |
| 6_class.md:313 | `visuddhiyā \| noun \| fem.dat.sg<br>fem.gen.sg` | Raw `<br>` inside table cells (Pāli, POS, Grammar and English columns); 614 `<br>` in the folder, most of them between citation and sentence. A recurring owner-decision topic. (old A11) | owner decision | 5 |
| 9_class.md:72 | `samudayāya. \| noun \| masc.dat.sg` | Sentence punctuation kept inside the Pāli cell (classes 9–12, and class 15 throughout, e.g. `hoti,` at 15_class.md line 46); the other classes strip it. (old A12) | Strip. Done 2026-11-25 in classes 9, 12, 15 (key and exercise); classes 10 and 11 left | 7 |
| 11_class.md:276 | `[AN4.61](https://s.dhamma.gift/an/an4/index.html#an4.61)(simpl) <br>` | The gap between citation, `(simpl)` and `<br>` is written five ways: `) <br>` ×298, `)<br>` ×71, `) (simpl) <br>` ×52, `) (simpl)<br>` ×40, `)(simpl) <br>` ×1 (this line). (old A15) | One form | 6 |
| 10_class.md:24 | `**Or knowing, he said, "I don't know"**` | Translations of a split sentence: some start upper-case and end without a full stop, others the reverse, even inside one item (10_class.md line 33 "or, not seeing"). (old A16) | One rule for split sentences | 4 |
| 11_class.md:543 | `[DHP012](https://s.dhamma.gift/kn/dhp/index.html#dhp1)` | Zero-padded Dhp labels (`DHP012`, `DHP026`, `DHP085`–`DHP088`: 6) beside unpadded ones (`DHP76`, `DHP130` and 13 more). (old C13) | One form | 6 |
| 6_class.md:56 | `[VIN1.2.12](https://s.dhamma.gift/vin/tv/pli-tv-bu-vb-ss/index.html#pli-tv-bu-vb-ss12)` | Two label systems for the Vinaya: numeric `VIN1.2.12`, `VIN1.1.4`, `VIN2.5.1.2`, `VIN4.1.14` (7) against `VIN PAT SA 12`, `VIN PAT PC 20` (41 linked, 5 unlinked). (old C14) | One form | 6 |
| 5_class.md:74 | `madāya \| noun \| masc.dat.sg \| for intoxication \| √mad･3 ya (be mad, intoxicated)` | Root glosses differ from current DPD wording in about 65 rows (`√chid` as `(cut, steal)` and `(cut)`; `(breath, blow)`; `(destroy, exhaust)`), mostly DPD rewording since the key was written. (old D22) | DPD lookup; refresh the glosses in one pass | 6 |
| 5_class.md:88 | `ānanda \| noun \| masc.voc.sg \| O Ānanda! (lit. joyful)` | The same word has a root in one row and none in another: `ānanda` (here vs 6_class.md line 49), `medhāvī`, `saṅgha`, `atthi`, `khamo` (15:44 vs 15:36), `samannāgatā` (15:235 vs 15:104), `sādhukaṃ` (14:419 vs 14:668), `apaññattaṃ`/`paññāpessanti` (14:434, 14:436 vs 14:437). (old D25) | Fill or leave empty consistently | 6 |
| 4_class.md:200 | `abhinanduṃ \| verb \| aor.3rd.pl \| they were pleased with (+acc)` | Governed case written `(+acc)` ×39, `[+acc]` ×36, bare `+acc` ×4 (e.g. `+loc` at 15_class.md line 384), sometimes after a `<br>`, and here in the English column. Supplied words in translations: `[and]` (2_class.md line 84) against `(and)`, `(about)`, `(for)` (3_class.md line 371, 5_class.md line 305). (old E2) (old 4.16) | One form, in the Grammar column | 7 |
| 10_class.md:291 | `asante \| prp \| masc.loc.sg \| (when) … not present (loc abs)` | Absolute constructions written `(loc abs)` / `(gen abs)` ×37, `[loc abs]` ×14 (e.g. 11_class.md line 477), `(loc.abs)` ×4, `<br>loc abs` ×2; here in the English column. (old E3) | One form, in the Grammar column | 6 |
| 11_class.md:508 | `vimuttam'iti \| pp \| nt.nom.sg \| liberated +endquote` | End of quotation written `+end quote` ×5, `+endquote` ×8, `+ endquote` ×2, `+ end quote` ×2, `+ quote` ×4, or as a separate `iti`/`'ti` row ×21; here in the English column; nothing at 11_class.md lines 628, 639, 14_class.md line 229, 16_class.md line 246. (old E4) | One form | 7 |
| 13_class.md:368 | `dissanti \| verb \| pr.pass.3rd.pl \| are seen` | Passive and causative written in about 15 ways in the POS column (`verb.pass`, `verb. pass`, `prp. pass`, `prp caus pass`, `ptp caus pass` …) or inside Grammar (here; 14_class.md line 565); classes 3–12 tag the same words plain `verb` (`vuccati` 9_class.md line 320 vs 14_class.md line 820; `paripūreti` 3_class.md line 106 vs 14_class.md line 16). (old E5) | One form; decide whether earlier classes get the label | 8 |
| 13_class.md:368 | `√dis･1 ya (see)` | The passive sign after a group-1 root is `ya` in 22 cells, `iya` in 5 and `īya` in 3 (e.g. 14_class.md lines 399, 651); compound signs `+ iya` ×6, `ṃa + iya` ×1, once without `+`. Folder counts for the rows in the class 13 and 14 slices. | `ya` throughout | 6 |
| 11_class.md:651 | `atītā \| adj (pp) \| masc.nom.pl \| past` | Participle used as adjective: `adj (pp)` ×4, `adj [pp]` ×2, `adj<br>[pp]`, `pp [adj]`, `adj (\<ptp)`, `adj(\<ptp)`, `adj, <br>(\<ptp)` ×2, `adj<br>(ptp)`. (old E6) | One form | 6 |
| 10_class.md:765 | `kati \| pron interr \| masc.nom.pl \| how many?` | Interrogative pronoun as `pron interr` ×4, `pron, interr`, `pron.<br>interr`, `pron<br>interr`; plain `pron` for `ko` ×3. (old E7) | `pron`, with `interr` in Grammar | 6 |
| 5_class.md:157 | `bhogī \| adj. \| masc.nom.sg` | Stray POS values: `adj.` (also 13_class.md line 474), `noun (comp)`, `adj, comp`, `proper noun`, `ind<br>(comp)`, `pron+noun [idiom]`, `pron+verb`. (old E8) | Fold into the standard set | 6 |
| 11_class.md:672 | `ca \| ind \| adv \| and` | Grammar cell of particles: `ca` `conj` ×80, empty ×4, `adv` (here), `ind` (15_class.md line 351); `vā`, `kho`, `eva`, `api`, `pana`, `ce`, `hi` likewise; 25 `ind` rows have an empty Grammar cell and 36 have `-`. `seyyathāpi`: `-` (10_class.md line 94), empty (11_class.md line 52), `pron+adv+ind` (11_class.md line 242). (old E9) | One tag per particle | 7 |
| 8_class.md:436 | `āvuso \| ind \| voc.sg or voc.pl \| o friend; brother` | `āvuso` is `ind \| voc.sg` (5:589, 14:348) or `voc.sg or voc.pl`; verify_key flags the `voc.sg` cells IMPOSSIBLE (DPD: `ind`). `bhante` is `noun \| masc.voc.sg` ×14. (old E11) | `ind` with a plain note, or treat both alike | 5 |
| 9_class.md:203 | `atha \| ind \| ind \| after` | Fixed phrases analysed several ways: `atha kho` (five tags; split here into `atha` "after" + `kho` "that"), `evam'eva`, `seyyathāpi`, `kiṃ nu kho`, `yo pana bhikkhu`, `n'eva`, `c'eva` (`sandhi \| ind+ind`, `ind \| ind+ind`, `ind \| ind+emph`). (old E12) | One analysis per phrase | 7 |
| 1_class.md:11 | `sammā - \| ind \| adv \| fully; completely` | Compound members: Grammar `-` ×17 (class 2), empty, bare gender, `masc (in comp)`, full `masc.nom.sg` on a stem; stems written `sammā -` (space before the hyphen, here), `adhicittam-`, `divasaṃ-`, `ca-`. (old E13) | One form | 6 |
| 6_class.md:37 | `sāvaka-saṅgho \| noun \| masc.nom.sg` | Hyphen in the table that the sentence does not have: also 8_class.md line 45, 11_class.md line 128, 14_class.md line 27, 16_class.md line 102 (`yathā-dhammaṃ` vs `yathādhammaṃ` at line 127), and the rows of classes 11–13 listed in their slices. (old E14) | Match the sentence | 6 |
| 11_class.md:260 | `[lit:made a vehicle]` | The literal-meaning note is written `lit:` ×64 and `lit.` ×38 (mech count), in round or square brackets or none, once `Lit:`. (old E15) | One form | 6 |
| 12_class.md:654 | `(The Buddha) taught the sublime teaching` | Supplied words in round brackets (`(The Buddha)`, `(his)`, `(done)`) beside the majority in square brackets (`[your]`). (old E16) | Square brackets | 5 |
| 15_class.md:176 | `with parts, factors; qualities` | Gloss separators: comma and semicolon both used, often in one cell. (old E17) | One separator | 4 |
| 5_class.md:35 | `parisuddho \| pp \| masc.nom.sg \| cleaned, purified` | Same word, different POS: `parisuddho` pp here, adj at 5_class.md line 370; `āyasmato` noun/adj; `sabba` adj/pron; `ekaṃ`/`eko` card/adj; `adassāvī` and `pariyāyena` inside one sentence; `āgatā` adj/pp; `subhāsitā` pp vs `dubbhāsitā` adj (15_class.md lines 179, 182). (old E19) | One POS per word and function | 6 |

## G. Links

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 11_class.md:65 | `[ITI111](https://s.dhamma.gift/kn/iti/index.html)` | The only KN link in the class with no anchor. (old C12) | Add the anchor if the site has one | 5 |
| 13_class.md:392 | `2. APA 3 (simpl) <br>jahanti purimaṃ nāmaṃ` | Unlinked and too vague to locate. (old C9) | Add a precise reference and link if one exists | 7 |
| 14_class.md:132 | `[AN3.83](https://s.dhamma.gift/an/an3/index.html#an3.82)` | The exercise (bpc_ex/14_class.md line 109) cites `AN4.73` for the same item; the label and the anchor also differ by one (folder-wide AN3 pattern, see the cross slice). (old C7) | Check the text; make key and exercise agree | 7 |
| 9_class.md:553 | `[TH251](https://s.dhamma.gift/kn/thag/index.html#thag16.1)` | The label gives the verse number; the anchor always points to the first poem of the nipāta (Raṭṭhapāla is Thag 16.4, Pārāpariya 16.10). Also 9_class.md line 578, 11_class.md line 330, 14_class.md line 502, 2_class.md line 15. (old C11) | Confirm whether the site has finer anchors | 5 |

## H. Data to re-verify (forms, references, counts)

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 1_class.md:3 | `1. namo tassa bhagavato arahato sammā-sambuddhassa` | No source reference. In class 2, 13 phrase items (8–11, 13, 14, 17–19, 21, 24, 27, 30) have none either. (old C10) | owner decision: confirm intended | 5 |
| 2_class.md:73 | `6. VIN PAT NID nidānuddeso<br>` | Reference with no link, unlike every other labelled item in the class. (old C9) | Add the s.dhamma.gift link to the Pātimokkha nidāna if the site has one; verify | 6 |
| 2_class.md:257 | `aparena samayena buddho` | MN39 has the prison simile (`bandhanāgāre baddho assa. so aparena samayena …`): the word there is `baddho` "bound", and the three words are not contiguous. `buddho` "the Awakened One" (line 264) may rest on a misreading. (old C19) | verify against MN39 | 5 |
| 2_class.md:247 | `vinipātaṃ nirayaṃ` | The old audit did not find the phrase in SN12.41 by text search (it found it in SN12.70). Not checked against a text here. (old C19) | verify | 4 |
| 3_class.md:181 | `16. [MN2.4](https://s.dhamma.gift/mn/mn2/index.html)<br>parikkhāraṃ paṭisevāmi` | MN2 has the 3rd person (`… parikkhāraṃ paṭisevati`); the 1st person is the recollection chant. The item is not marked `(simpl)`. (old C19) | verify; mark `(simpl)` if the 1st person is kept | 5 |
| 3_class.md:336 | `29. VIN<br>passasi taṃ āpattiṃ` | `VIN` alone cannot be located and has no link. (old C9) | Give the exact Vinaya reference and link; verify | 7 |
| 4_class.md:280 | `22. [SN46.53](https://s.dhamma.gift/sn/sn46/index.html#sn46.53) (simpl)<br>bhikkhū paribbājakehi sammodiṃsu` | The old audit found the phrase in SN46.52 and 46.54 by text search, not in 46.53. Not checked against a text here. (old C19) | verify | 3 |
| 5_class.md:53 | `5. UD-a 43 <br>ahaṃ te aparimitaṃ dhanaṃ dassāmi` | A commentary reference with no link (the site has no commentaries). (old C9) | owner decision: keep as plain text, or give a canonical source | 6 |
| 6_class.md:3 | `1. [DN2.9](https://s.dhamma.gift/dn/dn2/index.html) <br>bhagavā bhikkhū āmantesi, bhikkhavo'ti.` | The exercise (bpc_ex/6_class.md line 3) cites the same item as `SN22.59`. (old C1) | verify the source; make both files agree | 8 |
| 6_class.md:30 | `3. [DN11.6](https://s.dhamma.gift/dn/dn11/index.html) <br>esa bhagavato sāvakasaṅgho` | The old audit could not place the saṅgha formula in DN11. Not checked against a text here. (old C15) | verify | 4 |
| 6_class.md:42 | `4. [DN16.7](https://s.dhamma.gift/dn/dn16/index.html) <br>atha kho āyasmato ānandassa etad'ahosi` | The exercise (bpc_ex/6_class.md line 35) has `DN16.17`. (old C2) | Make both agree | 8 |
| 6_class.md:56 | `5. [VIN1.2.12](https://s.dhamma.gift/vin/tv/pli-tv-bu-vb-ss/index.html#pli-tv-bu-vb-ss12)` | The exercise (bpc_ex/6_class.md line 47) cites `VIN PAT SA 12` (Pātimokkha, `pm4`); the key cites the Vibhaṅga in another label style. (old C3) | Make both agree | 8 |
| 6_class.md:73 | `6. [MN152](https://s.dhamma.gift/mn/mn152/index.html) (simpl)` | The exercise (bpc_ex/6_class.md line 64) cites `MN19`. The formula is in both suttas. (old C4) | Make both agree | 7 |
| 6_class.md:214 | `16. [AN10.71](https://s.dhamma.gift/an/an10/index.html#an10.71)<br>thero bhikkhu sabrahmacārīnaṃ piyo ca hoti` | The old audit took the wording for AN5 (`thera` suttas), not AN10.71. Not checked here. (old C15) | verify | 4 |
| 6_class.md:470 | `1. [SNP16](https://s.dhamma.gift/kn/snp/index.html#snp2.4) <br>mātāpitu upaṭṭhānaṃ, puttassa ca dārassa saṅgaho` | The Maṅgalasutta reads `puttadārassa saṅgaho`; the key splits the compound into `puttassa ca dārassa` without a `(simpl)` marker. | Mark `(simpl)`, or keep the compound | 6 |
| 7_class.md:166 | `13. [MN10.16](https://s.dhamma.gift/mn/mn10/index.html)<br>aho vata mayaṃ na maraṇadhammā assāma` | The expanded truths passage with `na maraṇadhammā assāma` is in DN22; in MN10 it is found only in the Burmese edition. (old C15) | verify against the edition the course follows | 4 |
| 8_class.md:107 | `7. DNa2.3 <br>therī pattaṃ gahetvā ākāse khipi.` | A commentary reference with no link. (old C9) | owner decision: keep as plain text | 6 |
| 8_class.md:191 | `11. [VIN PAT PA 1](https://s.dhamma.gift/vin/tv/pli-tv-bu-pm/index.html#pli-tv-bu-pm3) <br>yo pana bhikkhu sikkhaṃ apaccakkhāya` | The rule is shortened (`bhikkhūnaṃ sikkhāsājīvasamāpanno` and `antamaso tiracchānagatāyapi` are left out) with no `(simpl)` marker and no ellipsis. | Add `(simpl)` | 4 |
| 9_class.md:553 | `tasmā hi paññā eva dhanena seyyā, yāya vosānaṃ idha adhigacchati.` | Thag 16.4 / MN82 read `paññāva dhanena seyyo` and `karonti mohā` (pl); the key has `seyyā` and `karoti` (line 573) with no `(simpl)` marker. | verify; mark `(simpl)` if the changes are kept | 4 |
| 9_class.md:615 | `vatthuṃ desanāya` | The Pātimokkha has the compound `vatthudesanāya`; the key splits it without `(simpl)`. (old 9.4) | verify; mark `(simpl)` | 4 |
| 10_class.md:362 | `na ca khuddaṃ samācare kiñci` | The Mettasutta reads `khuddamācare` (= `khuddaṃ ācare`); `samācare` adds a syllable to the pāda. The exercise has the same text; the table tags `samācare` (line 370). (old 10.1) | verify; `khuddaṃ ācare` | 6 |
| 11_class.md:416 | `lok'āmisena paṭisaṃyuttānaṃ paṭilābhaṃ paṭilābhato` | Reworded against MN137 (`lokāmisapaṭisaṃyuttānaṃ … paṭilābhaṃ vā`) without `(simpl)`; line 237 likewise splits DN14's `apagatakāḷakaṃ` into `apagataṃ kāḷakā`. (old 11.6) | verify; add `(simpl)` | 5 |
| 12_class.md:99 | `yena anuppanno byāpādo uppajjati, yathayidaṃ` | AN1.12 has `anuppanno vā byāpādo uppajjati uppanno vā …`; the key shortens it without `(simpl)`. Line 377 likewise drops `pi` and `bhikkhave` from AN10.61 (`pañcapāhaṃ, bhikkhave`); for line 357 see the `caturāsītīnaṃ` row. (old 11.6) | verify; add `(simpl)` | 5 |
| 13_class.md:196 | `ce bhikkhuṃ aññe bhikkhū jāneyyuṃ` | The rule reads `tañce bhikkhuṃ`; enclitic `ce` cannot open a sentence, and the translation still supplies "[that]". Not marked `(simpl)`. (old 13.2) | verify; `tañ'ce bhikkhuṃ` + a `taṃ` row | 6 |
| 13_class.md:220 | `bhiyyo'ti \| ind \| adv+end quote \| more"` | The rule continues `bhiyyo, na ca tassa bhikkhuno…`; the `'ti` and the closing quote are not in it. (old 13.3) | verify; `bhiyyo` | 5 |
| 13_class.md:282 | `[MN10.18](https://s.dhamma.gift/mn/mn10/index.html)` | The expanded truths passage is in DN22; in MN10 only in the Burmese edition. (old C15) | verify | 4 |
| 13_class.md:302 | `evam'pi kho bhikkhu tehi bhikkhūhi` | Abridged without `(simpl)`; line 483 splits the compound `chakkhattuparamaṃ` into `chakkhattuṃ paramaṃ`, also unmarked (items 2, 4, 7 are marked). (old 13.5) | verify; mark `(simpl)` | 5 |
| 13_class.md:474 | `supatiṭṭhitā \| adj. \| fem.nom.sg \| well placed; well established` | Khp 7 in CST reads `suppatiṭṭhitā` (DPD has both lemmas); stray full stop in the POS cell. (old 13.4) | verify; `adj` | 5 |
| 14_class.md:144 | `es'ev'anto paṭigh'ānusayānaṃ,` | MN18 lists `esevanto rāgānusayānaṃ` first, then `esevanto paṭighānusayānaṃ`; the key (and the exercise, bpc_ex/14_class.md line 119) jump to the second item with no `…` or `(simpl)`. | verify; add `…` or `(simpl)` | 5 |
| 14_class.md:428 | `[DN16.21](https://s.dhamma.gift/dn/dn16/index.html)` | Sub-numbers after DN/MN labels (`DN16.21`, also for two other passages at 9_class.md lines 246, 282; `DN23.20`, `DN14.4`, `MN2.2`, `MN2.8`; 47 labels) match no SuttaCentral segment numbering, and the scheme is not stated. (old C20) | State the numbering scheme, or drop the sub-numbers | 5 |
| 4_class.md:14 | `[AN3.66](https://s.dhamma.gift/an/an3/index.html#an3.65)` | AN3 labels run one higher than their anchors: AN3.66→#an3.65 (also 9_class.md line 116), AN3.70→#an3.69, AN3.71→#an3.70, AN3.79→#an3.78, AN3.156→#an3.155, AN3.83→#an3.82 (14_class.md line 132). The labels follow another edition's numbering; the anchors follow SuttaCentral. | Align the labels with the anchors, or state the numbering | 6 |

## I. Further details on the material under review

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 15_class.md:9 | `**"pañcime (pañca + ime), bhikkhave, caṅkame ānisaṃsā.` | The source paragraph is bold with `(a + b)` sandhi notes in items 1–2 (also line 96), plain with none in items 3–4 (lines 168, 256-258); item 4 (line 252) lacks the `(paragraph N)` note. (old 15.2) | One layout for the four items | 6 |
| 15_class.md:1 | `# Class 15 Key to Exercises` | Classes 1 and 15 have no `## Class N Extra` section; classes 2–14 all have one. Class 15 is a translation assignment, so this is probably intended. (old A2) | Confirm intended | 3 |
| 5_class.md:130 | `assasissāmi \| verb \| fut.1st.sg \| I will breathe in \| √sas･1 a (breath)` | The root gloss is copied from DPD, which has a noun where a verb is expected; also 5_class.md line 143 and 11_class.md lines 211-262. DPD-side. (old D23) | Raise upstream ("breathe") | 6 |
| 5_class.md:72 | `√dū×1 a (go, run)` | The root mark `×` (78 cells) beside `･` (1 729 cells, mech counts) is explained nowhere in docs/bpc, docs/bpc_ex or docs/bpc_key. (old D24) | Explain the two marks once (e.g. in index.md) | 8 |

## Mechanical detail

Counts from the scripts. Items that are also rows in the tables above are marked.

### M1. Tables, footnotes, characters (`mech_checks.py docs/bpc_key`)

- 16 files, 8 235 lines, 5 466 table rows, 0 column mismatches.
- Index link text vs page H1: 0 differences.
- Footnotes: 1 reference, 1 definition (`8_class.md`).
- Cyrillic character: `13_class.md:412`. Row above.
- Trailing space: `11_class.md:527`. Row above.
- No tab, NBSP, zero-width or non-NFC character was reported. No line with a double space.
- External links: 442 occurrences, 219 unique, all on `s.dhamma.gift`; 219 links on 104 pages pass `check_sutta_links.py`.

### M2. Key sentence vs exercise sentence (`key_vs_ex.py`)

- 15 class files, 465 numbered items compared.
- 71 items differ after normalising quotes, bold, `<br>` spacing and `ṁ`. Most are by design: the exercise resolves sandhi (`jānāmī'ti` in the key, `jānāmi iti` in the exercise; `imam'eva` / `imaṃ eva`). The differences that are not sandhi are rows above (cross-file slice and the class slices).
- 97 items differ only in the citation label or in the spacing around `<br>`.

### M3. Project verifier (`verify_key.py --course bpc --warnings`)

- Numbering, POS vocabulary, grammar vocabulary, root format, stray characters: 0 errors each.
- Word coverage: 465 warnings ("row not in sentence", "sentence word has no row"). 209 of them are in `15_class.md`, which is laid out in paragraphs that the word check cannot align. The rest were read with their class; those that are real mismatches are rows above.

### M4. Word forms vs DPD (`verify_key.py --dpd`, advisory)

| Bucket | Rows |
| --- | --- |
| CONFIRMED | 1 123 |
| AMBIGUOUS (more than one DPD reading; not reviewed one by one) | 2 087 |
| SKIPPED | 1 079 |
| IMPOSSIBLE | 17 |
| NOT-FOUND | 12 |
| ROOT-MISMATCH | 22 |
| Total | 4 324 |

Flagged rows per class:

| Bucket | 2 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IMPOSSIBLE | 0 | 1 | 3 | 2 | 0 | 1 | 1 | 1 | 0 | 3 | 1 | 3 | 1 |
| NOT-FOUND | 1 | 1 | 0 | 0 | 3 | 2 | 0 | 0 | 0 | 1 | 1 | 1 | 2 |
| ROOT-MISMATCH | 0 | 0 | 0 | 2 | 1 | 1 | 6 | 4 | 1 | 1 | 1 | 3 | 2 |

The 51 flagged rows were read with their class. Those that are errors are rows above, with `verify_key` named in the `Problem` cell. A flag is not always an error: a compound that is not a DPD headword (`bahujanahitāya`, 9:239) is flagged IMPOSSIBLE because the report has nothing to compare it with.

### M5. Convention counts

| Item | Total | Where |
| --- | --- | --- |
| `ṁ` | 6 | classes 11 (2), 12 (4) |
| straight `'` | 459 | classes 2–15 |
| curly `’` | 0 | |
| curly `‘` | 25 | classes 3, 4, 6, 9–15 (10 in class 15) |
| straight `"` | 241 | classes 2–15 |
| curly `“”` | 0 | |
| `<br>` | 614 | classes 2–15 |
| `...` | 10 | classes 3, 5, 10, 11, 12 (6 in class 12) |
| `…` | 56 | classes 2–4, 6–15 |
| ` - ` | 60 | classes 1, 2, 7–10, 12, 13 |
| `–` | 9 | classes 4, 6, 11, 12, 15 |
| `—` | 11 | classes 3, 4, 7, 9, 11, 14, 15 |
| `Pāli` | 29 | all classes |
| `Pāḷi` | 0 | |
| `{:` | 0 | |
| `lit:` | 64 | classes 2, 5–15 |
| `lit.` | 38 | classes 3–6, 8–12, 14, 15 |
| root mark `･` | 1 729 | classes 5–15 |
| root mark `×` | 78 | classes 5–15 |
