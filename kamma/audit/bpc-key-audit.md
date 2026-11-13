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

## Summary

| Category | idx–2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | cross | Total | Conf. ≥ 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A. Pāli and grammar content errors | 3 | 1 | 6 | 6 | 3 | 10 | 9 | 11 | 10 | 12 | 10 | 12 | 13 | 6 | 4 | 116 | 35 |
| B. Tables, paradigms and lists that disagree with each other or themselves | 1 | 1 | 4 | 4 | 6 | 3 | 3 | 5 | 3 | 2 | 3 | 2 | 1 | 1 | 0 | 39 | 15 |
| C. Translation and gloss problems | 6 | 3 | 8 | 13 | 8 | 9 | 10 | 7 | 15 | 9 | 8 | 10 | 11 | 8 | 1 | 126 | 12 |
| D. English typos and grammar | 6 | 5 | 6 | 5 | 4 | 7 | 8 | 6 | 3 | 4 | 2 | 4 | 3 | 1 | 2 | 66 | 30 |
| E. Markdown defects that affect rendering | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 6 | 0 |
| F. Convention drift | 3 | 2 | 1 | 1 | 2 | 5 | 1 | 3 | 6 | 7 | 6 | 2 | 12 | 3 | 27 | 81 | 14 |
| G. Links | 0 | 0 | 1 | 0 | 2 | 0 | 0 | 1 | 0 | 2 | 0 | 1 | 3 | 0 | 1 | 11 | 6 |
| H. Data to re-verify (forms, references, counts) | 4 | 2 | 2 | 1 | 7 | 2 | 3 | 2 | 1 | 1 | 1 | 5 | 1 | 0 | 2 | 34 | 3 |
| I. Further details on the material under review | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 3 | 5 | 2 |
| **Total** | **24** | **15** | **29** | **30** | **32** | **36** | **35** | **35** | **38** | **38** | **30** | **36** | **44** | **21** | **41** | **484** | **117** |

A row often covers several locations, so the number of places to edit is higher than the row count. The `cross` column holds the folder-wide findings and the old Part 1 rows that do not belong to one class.

Overall confidence: 9/10 that the quoted text is where the row says (scripted). 8/10 for categories D, E, F and G (visible in the source). 7/10 for A, B, C and H as a group: DPD was consulted for the tags, roots and glosses that looked doubtful, but no text edition was. Use the per-row score.

## Owner decisions carried over

None. The owner has not reviewed the old key audit, so every old row was re-checked like a new finding.

One decision from the BPC lesson audit was applied here: old row 5.1 (the split of `mā pamādattha`) is dropped, because the owner rejected the same point there (bpc A13) and the key follows the lesson. The owner may want to confirm this.

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

- `<br>` in table cells versus the "no raw HTML in sources" rule (614 in the folder).
- Elision marks inside one word where a sandhi consonant is inserted or nothing is dropped: `añña'd'atthu` (5:481), `yāva'd'eva` (7:370), `eta'r'ahi` (11:638, 13:103), `atthaṅ'gate` (10:181), `samanta'pāsādiko` (12:369). DPD writes each as one word. If the marks are a deliberate notation for sandhi, they can stay, but the rule should be stated once in the key.
- `kira` in SN10.8 (2:8): "it is said" or "truly". Both are DPD senses.
- One rendering for recurring terms (`brāhmaṇa`, `dhammavinaya`, `samaṇa`, `mettā`, "Venerable sir").
- Phrase items with no source reference (class 1, and 13 items in class 2), and commentary references with no link (5:49, 8:101).
- AN3 labels run one higher than their link anchors (AN3.66 → `#an3.65`, and five more): the labels seem to follow the VRI numbering and the anchors SuttaCentral's. Decide which numbering the label should show.

## A. Pāli and grammar content errors

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 2_class.md:46 | `uttarissa \| adj \| masc.gen.sg` | Not in DPD (verify_key NOT-FOUND). `uttarimanussadhamma` is `uttari` + `manussadhamma`; a declined gen.sg `uttarissa` is built for the drill and is tagged as a real form. (old 2.2) | Tag `uttari` as a compound member (DPD: uttari adj / ind; compound `uttari + manussadhamma`), or label line 42 as a drill decomposition | 5 |
| 2_class.md:221 | `dukkhehi \| noun \| masc.instr.pl<br>masc.abl.pl` | The noun `dukkha` is neuter (4_class.md tags it nt, line 193). (old 2.3) | `nt.instr.pl<br>nt.abl.pl` (DPD: the noun dukkha is nt) | 9 |
| 2_class.md:222 | `domanassehi \| noun \| masc.instr.pl<br>masc.abl.pl` | `domanassa` is neuter. (old 2.4) | `nt.instr.pl<br>nt.abl.pl` (DPD: the noun domanassa is nt) | 9 |
| 3_class.md:62 | `‘idaṃ dukkhan'ti \| pron+noun+ind \| nt.nom.sg` | One row and one grammar tag for three words: `idaṃ` (pron), `dukkhaṃ` (noun) and the quotative `iti` (ind), which takes no case. | Split into three rows, or tag `nt.nom.sg + nt.nom.sg + quote` | 5 |
| 4_class.md:253 | `paggaṇhahi \| verb \| imp.2nd.sg \| raise up` | Not a valid imperative (short a before `-hi`); verify_key NOT-FOUND. The sentence (line 249) has the same form. AN4.48 reads `paggaṇhe` (opt). (old 4.1) (old F2) | `paggaṇhāhi` in sentence and table (DPD base `gaṇhā`); verify the AN4.48 reading | 8 |
| 4_class.md:47 | `tilā \| noun \| masc.nom.pl \| sesame` | DPD has `tila` as nt only; verify_key IMPOSSIBLE (DPD reading: nt nom pl). The text's `ime tilā` shows masculine concord, so the tag follows the sentence, not DPD. (old F4) (old 4.8) | `nt.nom.pl`, or a note on the masculine concord | 6 |
| 4_class.md:107 | `byādhi \| noun \| masc.nom.sg \| sickness` | The source has the compound `byādhidhammomhi` (the exercise writes `byādhi-dhammo`); the first member is tagged as a nominative. (old 4.2) | `byādhi-dhammo` as one adj row (DPD: byādhidhamma, adj, "liable to get sick"), or `byādhi-` untagged for case | 7 |
| 4_class.md:149 | `panūda \| verb \| imp.2nd.sg \| dispel` | SN2.8 and Dhp 383 read `panuda`; also in the sentence (line 141). (old 4.4) | `panuda`; verify against the text (the headword lookup cannot confirm an imperative form) | 5 |
| 4_class.md:204 | `gahassa \| noun \| masc.gen.sg \| of a house` | `gaha` "house" is neuter; masc `gaha` is "seizing", "planet". (old 4.7) | `nt.gen.sg` (DPD: gaha 2 nt "house") | 8 |
| 4_class.md:313 | `vissuto \| adj \| masc.nom.sg \| famous, renowned` | Tagged adj; also `sukhitā \| adj` (line 299), while `upaddutā` (line 335) and `diṭṭho` (line 206) are pp. (old 4.9) | `pp` for both (DPD: vissuta pp of vi √su; sukhita pp of sukheti) | 6 |
| 5_class.md:45 | `gamissāmi \| verb \| fut.1st.sg \| I will go \| √gam･1 \*e (go)` | `gamissati` belongs to `gacchati` (`√gam･1 a`); the `*e` sign comes from an unrelated causative headword. (old D14) | `√gam･1 a (go)` (DPD: gacchati, √gam a) | 8 |
| 5_class.md:295 | `etaṃ \| pron \| masc.acc.sg \| this` | The thing asked about is a neuter "this". (old 5.6) | `nt.acc.sg` | 6 |
| 5_class.md:305 | `no \| pron \| 1st.acc.pl \| us` | The translation (line 313) says "to us"; with `byākaroti` the person told is dative. (old 5.7) | `1st.dat.pl \| to us` | 5 |
| 5_class.md:356 | `uccāsoṇḍaṃ \| noun \| fem.acc.sg \| a high trunk` | Gender and POS of `uccāsoṇḍa` to confirm (compound with `soṇḍā` fem "trunk"). | DPD lookup (`uccāsoṇḍa` is not a DPD headword; `soṇḍā` was not looked up) | 3 |
| 5_class.md:529 | `jina \| verb \| imp.2nd.sg \| you must win, conquer, defeat \| √ji･5 nā (conquer)` | Not a valid imperative of `jināti` (that is `jināhi`); verify_key IMPOSSIBLE. Dhp 223 has the optative `jine`; the same at line 532 and in the sentence (line 525). | `jine` with `opt.3rd.sg` (the Dhp 223 reading; verify), or `jināhi` (DPD base `jinā`) | 6 |
| 5_class.md:596 | `phāsu \| noun \| masc.nom.sg \| ease; comfort` | As predicate of `hoti`, an adjective or indeclinable reading is more natural; 10_class.md line 476 tags it `ind \| adv`. (old 5.8) | One tag in both classes. DPD has all three readings (phāsu adj, masc "ease; comfort", ind adv), so neither line is wrong by itself | 4 |
| 6_class.md:358 | `vā \| ind \| conj \| or` | Snp 1.8 reads `sukhinova` = `sukhino va` (emphatic or "as it were"), not "or"; the translation (line 366) follows "or". (old 6.3) | verify; `va \| ind \| emph`, "happy and secure" | 6 |
| 6_class.md:415 | `bāhu-pacālakaṃ \| ind \| adv` | Hyphen inside one word; the Sekhiya reads `bāhuppacālakaṃ`; also the sentence (line 410). (old 6.4) | `bāhuppacālakaṃ`; verify against the Sekhiya text (not a DPD headword) | 5 |
| 6_class.md:548 | `mānaṃ \| noun \| nt.acc.sg \| pride; conceit` | `māna` "conceit" is masculine; the neuter `māna` is "measure". (old 6.6) | `masc.acc.sg` (DPD: māna 1.1 masc "pride; conceit"; māna 2.1 nt "measure") | 9 |
| 7_class.md:175 | `abhitthaveyyāmi \| verb \| opt.1st.sg \| I would praise` | verify_key NOT-FOUND. SN8.11 reads `abhitthaveyyaṃ`. | `abhitthaveyyaṃ` (verify_key finds no DPD form `abhitthaveyyāmi`; the headword lookup cannot show the inflection table) | 6 |
| 7_class.md:216 | `ananda \| noun \| masc.voc.sg \| Ananda` | Short first vowel; verify_key NOT-FOUND. The sentence (line 210) has the same; the source reads `panānanda`. (old 7.1) (old F1) | `ānanda`, `Ānanda` | 9 |
| 7_class.md:267 | `atītaṃ \| adj \| masc.acc.sg \| the past` | Used as a noun "the past" (nt); also `anāgataṃ` (line 270) "the future". (old 7.10) | `atītaṃ`: `noun \| nt.acc.sg` (DPD atīta 1 nt "past; what is past"); `anāgataṃ`: `noun \| masc.acc.sg` (DPD anāgata 3 masc "future") | 6 |
| 7_class.md:270 | `anāgataṃ \| adj \| masc.acc.sg \| the future \| √gam･1 \*e (go)` | `anāgata` is from `√gam･1 a`; `*e` is the causative sign. The same for `upasaṅkami` (`√kam`) at 8_class.md line 57. (old D13) | `√gam･1 a (go)` (DPD: anāgata, √gam a); `√kam･1 a` | 8 |
| 7_class.md:333 | `gāhaṃ \| noun \| masc.acc.sg \| hiding place \| √gah･6 ṇhā (grasp)` | DPD derives every `gāha` from `√gah`, so the Root cell follows DPD and the old audit's `√gāh` is not supported. But DPD has no sense "hiding place" for `gāha` (its senses: capture, being caught; idea; aquatic predator); the gloss and the translation (`where they would go [for] a hiding place`) may be wrong. (old 7.14) | verify the gloss against MN 25 (DPD gāha 1.2 "capture; being caught") | 4 |
| 7_class.md:441 | `koci'd'eva \| ind \| pron+ind \| some or other; just some` | A declined pronoun agreeing with `paccayo`; tagged `ind` here and `idiom` at 8_class.md line 601. (old 7.9) | `pron \| masc.nom.sg` | 6 |
| 7_class.md:455 | `āpā \| noun \| masc.nom.pl \| water` | Gender of `āpa` to confirm (nt in DPD per the old audit; `āpas` masc). (old 7.8) | `nt.nom.pl` (DPD has `āpa` only as nt, in compounds); DPD lookup (`āpo`) for the free-standing noun | 5 |
| 7_class.md:462 | `kissa \| pron.<br>interr \| masc.dat.sg \| for what reason?; why?` | The neuter fits "why"; `<br>` inside the POS cell. (old 7.12) | `pron \| nt.dat.sg` | 5 |
| 7_class.md:463 | `pariyesanaṃ \| ind \| adv \| searching for; looking for` | `pariyesanaṃ` is the accusative of the noun `pariyesanā` (object of `care`), not an indeclinable. | `noun \| fem.acc.sg \| a search` (DPD: pariyesanā fem; no indeclinable) | 6 |
| 7_class.md:482 | `assavanatā \| noun \| fem.instr.sg (+gen) \| by the fact of not hearing` | `-tā` is not an instrumental ending; it is usually explained as an ablative of cause (`assavanatā` abl.sg). (old 7.11) | `fem.abl.sg` (DPD gives only the headword, fem abstr; the case is not settled by the lookup) | 4 |
| 8_class.md:174 | `pallaṅkena \| ind \| adv \| in cross-legged posture` | `pallaṅkena` is the instrumental of the noun `pallaṅka`, tagged `noun \| masc.acc.sg` at line 260. | `noun \| masc.instr.sg` (DPD: pallaṅka masc only; no indeclinable) | 7 |
| 8_class.md:206 | `aññataro \| adj \| masc.nom.sg \| a certain` | `aññatara` is a pronoun; `aññaṃ`, `anaññaṃ` (lines 92, 364) and `ekaccassa` are tagged `pron`. (old 8.5) | `pron` (DPD: aññatara pron) | 8 |
| 8_class.md:234 | `dūramaṃ \| adj \| masc.acc.sg [+loc] \| difficult to find delight (in)` | No masculine accusative noun to agree with; it is the predicate of the `yattha` clause. (old 8.7) | `nt.nom.sg` | 5 |
| 8_class.md:250 | `pabbajeyyāmi \| verb \| opt.1st.sg \| I would go forth` | verify_key NOT-FOUND; MN27 reads `pabbajeyyaṃ`. Same pattern as `abhitthaveyyāmi` (7_class.md line 175). | `pabbajeyyaṃ` (verify_key finds no DPD form `pabbajeyyāmi`; the headword lookup cannot show the inflection table) | 6 |
| 8_class.md:339 | `vīsatigaṇo \| noun \| masc.nom.sg \| group of twenty` | A bahubbīhi qualifying `bhikkhusaṅgho` ("a saṅgha numbering twenty"). (old 8.6) | `adj` (DPD: vīsatigaṇa adj, digu > bahubbīhi, "with a quorum of twenty monks") | 8 |
| 8_class.md:376 | `dakkhiṇena \| adj \| masc.instr.sg \| with right` | The adjective must agree with `passena` (nt, line 377); "right" also sits in the gloss of `passena`. (old 8.4) | `nt.instr.sg`; `passena` "with the side" | 8 |
| 8_class.md:495 | `[^1]: Alternatively, can be taken as a noun masc instr sg - (having illuminated) with extraordinary appearance` | An instrumental of `vaṇṇa` would be `-vaṇṇena`; `-vaṇṇā` (line 399) cannot be instr.sg. (old 8.8) | Reword the note (e.g. "a bahubbīhi, fem.nom.sg") | 4 |
| 8_class.md:577 | `uparujjhati \| verb \| pr.3rd.sg \| is ended \| √rudh･2 ṃa (obstruct)` | The same verb has `√rudh･2 ya` at line 572 in the same item. (old D10) | `√rudh･2 ya (obstruct)`, as at line 572 (DPD: uparujjhati, √rudh with the sign ya) | 8 |
| 8_class.md:626 | `nārīsu \| noun \| fem.loc.pl \| with regard to women` | Dhp 284 reads `nārisu` (short i, for the metre); the item is not marked `(simpl)`; also the sentence (line 614). (old 8.1) | verify; `nārisu` | 6 |
| 9_class.md:85 | `kallaṃ \| ind \| - \| is it suitable?` | `kalla` is an adjective "proper, fitting", here the predicate (nt.nom.sg). (old 9.12) | `adj \| nt.nom.sg` (DPD: kalla 1.4 adj "proper; valid; legitimate"; no indeclinable) | 7 |
| 9_class.md:76 | `yaṃ \| pron \| nt.acc.sg \| whatever` | `yaṃ aniccaṃ dukkhaṃ vipariṇāmadhammaṃ` is a nominal relative clause ("whatever is impermanent…"), so the four words (lines 76–79) are nominative; only `taṃ` (line 86) is the object. The same at line 373 (`yaṃ … na tumhākaṃ`). (old 9.7) | `nt.nom.sg` | 7 |
| 9_class.md:119 | `vicikicchituṃ \| verb \| inf \| to be unsure, be confused \| √cit･8 cha (think, intend)` | Sign `cha` for a desiderative whose sign is `sa`; the same for `jegucchī` (line 632, `√gup･1 cha`) and `vicikicchati` at 15_class.md line 383. (old D16) | Sign `sa` (DPD: vicikicchati, √cit with sa; jegucchī, √gup with sa) | 8 |
| 9_class.md:182 | `dassanāya \| noun \| masc.dat.sg [dat of purpose] \| to see; to look at` | `dassana` is neuter. (old 9.6) | `nt.dat.sg` (DPD: the noun dassana is nt) | 9 |
| 9_class.md:239 | `bahujanahitāya \| noun \| nt.dat.sg [dat of purpose]` | verify_key IMPOSSIBLE (no DPD reading matches `nt.dat.sg`). `bahujanahita` is not a DPD headword, so the report has no reading to compare; the tag may still be right. | DPD lookup (`hita`) | 3 |
| 9_class.md:260 | `anupubbasikkhā \| noun \| fem.acc.pl \| gradual training[s]` | With `sakkā … paññapetuṃ` the logical object is nominative singular; the translation (line 265) is singular; also lines 261, 262. (old 9.8) | `fem.nom.sg` | 7 |
| 9_class.md:334 | `ajjhāvasatā \| noun \| masc.nom.sg [+acc] \| one who is domestically settled` | A present participle, instrumental singular (the agent of `na sukaraṃ … carituṃ`); `-atā` cannot be nominative. (old 9.5) | `prp \| masc.instr.sg [+acc] \| by one living in (a house)` | 9 |
| 9_class.md:363 | `saggaṃ \| adj \| masc.acc.sg \| heavenly \| √gam･1 a (go)` | Root copied from `sugatiṃ` (line 362); verify_key ROOT-MISMATCH. (old D3) | `√sar` with the sign `a` (DPD: sagga 1.1 adj "heavenly", `√sar + ga`) | 9 |
| 9_class.md:404 | `kiṃ \| ind \| interr \| what` | A predicate pronoun ("what am I?"); also the object at line 445 (`taṃ kiṃ maññasi`); tagged `pron` at line 692. (old 9.11) | `pron \| nt.nom.sg` / `nt.acc.sg` | 5 |
| 9_class.md:463 | `tassa \| pron \| masc.gen.sg \| of that` | `tassa me` is "to me (being such)": `tassa` agrees with `me` (line 464, dat). (old 9.10) | `masc.dat.sg` | 6 |
| 9_class.md:555 | `parikkhāre \| noun \| masc.acc.pl \| requisites; accessories` | With `ussukā` the objects of concern are locative ("in regard to"), and the verse continues with a locative; also `bhesajje`, `paccaye` (lines 556, 558). (old 9.9) | `loc.sg` "in regard to" | 6 |
| 10_class.md:160 | `paritassati \| verb \| pr.3rd.sg \| he is perturbed; is shaken; is agitated; is anguished \| √tas･3 ya (be agitated)` | verify_key ROOT-MISMATCH here and for `aparitassaṃ` (line 166). (old D6) | DPD lookup: DPD has `paritassati` from √tas with the sign ya, which agrees with the cell; what verify_key objects to (root gloss or homonym) is not visible in the report | 4 |
| 10_class.md:273 | `sahatthā \| ind \| masc.instr.sg` | POS `ind` with a case tag. (old 10.4) | `noun \| masc.abl.sg` (DPD has only the masc noun sahattha "one's own hand"), or `ind \| adv`; not `ind` with a case | 6 |
| 10_class.md:365 | `purato \| ind \| prep \| in front` | An adverb here, like the parallel `pacchato` (line 363). (old 10.7) | `adv` | 6 |
| 10_class.md:396 | `evaṃ \| ind \| emph \| thus; in this way` | `evaṃ` "thus" is an adverb, tagged `adv` in the same sentence (line 398); also `emph` at line 141. (old 10.6) | `adv` | 8 |
| 10_class.md:454 | `ādiyamāno \| prp \| masc.nom.sg [+acc] \| taking; stealing \| √dā･1 a (give)` | verify_key ROOT-MISMATCH; the class has `√ādā･3 ya` for `upādiyati` (line 152). (old D5) | `√ādā･3 ya (take, seize)`, as at line 152 (DPD: ādiyati, √ādā ya) | 8 |
| 10_class.md:467 | `sametu \| verb \| imp.3rd.sg \| he should agree (with); let him harmonize (with) \| √sam･3 \*e (be calm, tired)` | `sameti` "agrees" is a different homonym from `sameti` "calms" (√sam). (old D4) | `√i･1 a (go)` (DPD: sameti 2.2 "agrees; matches", `saṃ + e + ti`, √i) | 9 |
| 10_class.md:490 | `uddharāpeyya \| verb \| opt.3rd.sg \| should cause removing; make to take away; cause to pack up \| √dhar･1 a (hold, carry, endure)` | A causative given the plain sign `a`. (old D15) | `√dhar･1 \*āpe` (DPD: uddharāpeti, caus of uddharati, √dhar \*āpe) | 8 |
| 10_class.md:519 | `imasmiṃ \| pron \| masc.loc.sg<br>(loc.abs) \| when this` | The referent is neuter (`idaṃ`, `imassa` nt.gen.sg, lines 521, 523); also `sati`, `imasmiṃ`, `asati` (lines 520, 527, 528). (old 10.5) | `nt.loc.sg` | 7 |
| 10_class.md:535 | `nirujjhati \| verb \| pr.3rd.sg \| ceases \| √rudh･2 ṃa (obstruct)` | Sign `ṃa`; `√rudh･2 ya` elsewhere in the key (8_class.md line 572, 13_class.md line 283); also `nirodhā` (line 533). (old D10) | `√rudh･2 ya` (DPD: nirujjhati, √rudh with the sign ya) | 8 |
| 10_class.md:748 | `anekajāti \| adj \| masc.nom.sg \| with many rebirths; having multiple lives` | Dhp 153 has the compound `anekajātisaṃsāraṃ`; the first member cannot be nom.sg. The sentence (line 744) also splits it. (old 10.2) | `anekajātisaṃsāraṃ`, or tag as a compound member | 8 |
| 11_class.md:50 | `ādittacelo \| noun \| masc.nom.sg \| whose clothes are on fire; with blazing garments` | A bahubbīhi glossed as an adjective but tagged `noun`; its members get case tags (`āditta- \| pp \| masc.nom.sg`, `-celo \| adj`, lines 51–52, 55–56). (old 11.11) | Compound `adj` (DPD: ādittacela adj, kammadhāraya > bahubbīhi); members without case | 7 |
| 11_class.md:128 | `khataṃ \| pp \| masc.acc.sg \| injured, uprooted \| √khan･1 a (hurt, break)` | The gloss joins two DPD homonyms: `khata` "hurt; injured" is the pp of khanati (√khan, as in the Root cell); "dug up; uprooted" is the pp of khaṇati (√khaṇ). DPD also lists the idiom `khata upahata` "hurt and injured". | Gloss "injured" only | 6 |
| 11_class.md:170 | `ujū \| adj \| masc.nom.pl \| straight, upright` | The subject is singular (`sakko … suvaco cassa`); the `-ū` is metrical lengthening. Also `suhujū` (line 172). (old 11.7) | `masc.nom.sg` | 9 |
| 11_class.md:253 | `mettāya \| noun \| fem.instr.sg \| with goodwill` | In apposition to `cetovimuttiyā` in the loc abs ("goodwill-liberation of mind"). (old 11.12) | `fem.loc.sg (loc abs)` | 5 |
| 11_class.md:465 | `evaṃ \| ind \| emph \| thus` | "thus" is the adverb; the same tag was flagged in class 10 (10_class.md line 396). | `adv` | 6 |
| 11_class.md:495 | `vimuttasmiṃ \| pp \| nt.loc.sg [loc abs] \| when liberated \| √muc･2 ya (release, free)` | Sign `ya`; the old audit gives `√muc･2 ṃa`. Also `vimuccati` (line 494). (old D11) | `√muc･2 ṃa` for `vimuttasmiṃ` (DPD: vimutta, √muc ṃa); `vimuccati` keeps `ya` (DPD: muccati, √muc ya) | 7 |
| 11_class.md:515 | `tassa \| ind \| adv \| therefore; thus; so; because of that` | In `tassa me … accayaṃ` the class 9 key reads `tassa` as a pronoun agreeing with `me` (9_class.md line 463). DPD has both readings (tassa pron; tassa 4 ind adv "therefore"). | One reading in both classes; with `me` the pronoun (`pron \| masc.gen.sg`) fits | 5 |
| 11_class.md:566 | `maṃ \| pron \| masc.acc.sg \| me` | Personal pronouns carry person, not gender. (old 11.8) | `1st.acc.sg` | 9 |
| 11_class.md:584 | `attaniye \| adj \| masc.loc.sg [loc abs] \| since belonging to oneself` | A substantive "what belongs to self": neuter. (old 11.13) | `nt.loc.sg` | 5 |
| 11_class.md:638 | `eta'r'ahi \| ind \| adv \| at present` | `etarahi` split with two elision marks; also in the sentence (line 624). (old 11.4) | `etarahi` (DPD: `eta + [r] + ahi`), unless the marks are a deliberate sandhi notation: owner decision | 5 |
| 11_class.md:650 | `ca \| ind \| adv \| and` | `ca` is `conj` in the other rows. (old 11.9) | `conj` | 9 |
| 11_class.md:662 | `dheyyaṃ \| noun \| nt.nom.sg \| the realm of; the sphere of` | No nominative role: it is what is crossed. Also `suduttaraṃ` (line 663); the translation (line 665) leaves it dangling. (old 11.10) | `nt.acc.sg`; "…will cross the realm of death, so hard to cross" | 6 |
| 12_class.md:492 | `sarena \| ind \| adv \| sweetly; melodiously` | An instrumental noun tagged as an adverb (DPD: sara "sound; voice" is masc only). The old row also cited `yena \| ind \| adv` (line 110); that is a DPD reading (yena 2, ind adv "because of which") and stands. (old 12.10) | `noun \| masc.instr.sg` | 6 |
| 12_class.md:159 | `mano- \| noun \| masc.nom.sg \| mind, heart` | A compound member (`manosañcetanā`, line 137) given a case tag. (The gender agrees with DPD: mano 1, masc, in comps.) | No case for the member: `mano- \| noun \| masc` | 6 |
| 12_class.md:209 | `catutthaṃ \| ordin \| fem.acc.sg \| the fourth (direction)` | verify_key IMPOSSIBLE: the fem. of `catuttha` is `catutthī`; DPD gives `catutthaṃ` as nt or `ind`. | `ind \| adv` or `nt.acc.sg` | 7 |
| 12_class.md:239 | `chattiṃsa \| card \| fem.nom.pl \| thirty-six` | verify_key IMPOSSIBLE: DPD has `chattiṃsā` card fem nom sg. (old F6) | `fem.nom.sg`; check the spelling | 6 |
| 12_class.md:345 | `caturāsītīnaṃ \| card \| fem.dat.pl \| for eighty-four` | verify_key NOT-FOUND: a plural of a decade numeral. DN14 has `caturāsītiyā pāṇasahassānaṃ`; the sentence (line 339) is reworded without `(simpl)`. (old 12.3) | verify; `caturāsītiyā` | 6 |
| 12_class.md:416 | `satehi \| adj \| masc.instr.pl \| with one hundred` | `noun \| nt.instr.pl` for the same word at line 87. (old 12.5) | `card \| nt.instr.pl` (DPD: sata 2.1 card, nt), and the same tag at line 87 | 7 |
| 12_class.md:458 | `vīsati \| card \| fem.acc.sg \| twenty (20)` | verify_key IMPOSSIBLE: DPD has `vīsati` as fem nom sg; the acc. sg. is `vīsatiṃ`. (old F7) | Re-tag, or note the elided form | 5 |
| 12_class.md:597 | `pācittiyena \| noun \| masc.instr.sg \| by an offence requiring confession` | `pācittiya` is neuter, as in the key at 10_class.md line 185 (`pācittiyaṃ \| noun \| nt.nom.sg`); `pārājikena` (line 593) is nt, `saṅghādisesena` (line 595) masc. (old 12.9) | `nt.instr.sg` (DPD: pācittiya 1 nt) | 8 |
| 12_class.md:654 | `bhagavā \| noun \| masc.nom.sg \| Blessed One` | With `brūhi` (imp.2nd.sg) this is an address; the translation (line 660) "May the Blessed One tell [us]" turns it into 3rd person. (old 12.6) | `masc.voc.sg`; "Tell [us] …, Blessed One" | 6 |
| 12_class.md:657 | `parābhavato \| noun \| masc.abl.sg \| for/of the downfall` | The gloss is gen/dat, the tag abl.; usually read as the gen. sg. of the prp ("of one who is declining"). (old 12.7) | Either keep the tag (verify_key: `parābhava` noun masc abl sg is a DPD reading) and gloss it as an ablative, or `prp \| masc.gen.sg` "of one who is declining"; tag and gloss must agree | 5 |
| 13_class.md:31 | `gaccheyyāmi'ti` | The vowel before `'ti` is lengthened: the exercise has `gaccheyyāmī'ti`. (old B14) | `gaccheyyāmī'ti` | 7 |
| 13_class.md:88 | `vinassantu \| verb.pass \| imp.3rd.pl \| may they be destroyed` | `vinassati` is an active group-3 verb (DPD `pr`), as the row's own `√nas･3 ya` says. (old 13.7) | `verb`; "may they perish" | 9 |
| 13_class.md:103 | `eta'r'ahi \| ind \| adv \| now` | `etarahi` split with two elision marks, as at 11_class.md line 638; also in the sentence (line 97). | `etarahi` (DPD: `eta + [r] + ahi`), unless the marks are a deliberate sandhi notation: owner decision | 5 |
| 13_class.md:167 | `kiṃ \| pron \| nt.nom.sg \| why` | Adverbial "why" is not nominative; the same phrase is `ind` at line 35. (old 13.14) | `ind \| interr` | 5 |
| 13_class.md:225 | `tasmiṃ \| pron \| masc.loc.sg (loc abs) \| when that` | The vomited thing is the food (nt): a locative of reference with `assa` ("would that man have a desire for that vomit?"); also `vante` (line 226). The translation (line 231) makes the man the agent. (old 13.12) | `nt.loc.sg`; reword | 6 |
| 13_class.md:283 | `nirujjhamānā \| prp. pass \| fem.nom.sg \| ceasing` | DPD: `nirujjhati` is `pr, pass of ni √rudh`, "ceases", so the passive tag is defensible. But it is used here and at line 284 (`verb. pass … is ceased`) only; class 15 (15_class.md lines 373, 374) has `prp`, `verb \| ceases`. "is ceased" is not English. (old 13.8) | One tag in both classes; gloss "ceases" | 7 |
| 13_class.md:320 | `saṃvijjamānā \| prp. pass \| masc.nom.pl` | DPD: `saṃvijjati` is `pr` "exists". (old 13.9) | `prp` (DPD: saṃvijjati 1.1 is plain `pr`, "exists; is found") | 7 |
| 13_class.md:364 | `munī \| noun \| masc.nom.sg \| sage, monk` | verify_key IMPOSSIBLE: `munī` is nom.pl by form; nom.sg only by metrical lengthening. (old F8) | Add "(metrical)" | 5 |
| 13_class.md:401 | `uddhaṃ \| ind \| prep \| above` | Free adverbs here; also `adho`, `tiriyaṃ` (lines 402, 404). (old 13.15) | `adv` | 4 |
| 13_class.md:412 | `dūre vasanti avidūre` | The `c` of `ye ca` before this is Cyrillic U+0441 (mech_checks CYRILLIC); it breaks search and DPD lookup. (old A5) | Latin `ca` | 10 |
| 13_class.md:532 | `sallaviddhānaṃ \| adj \| masc.gen.pl (gen abs) \| when pierced by an arrow` | Three words for the same people get two cases (`āturānaṃ` dat.pl, line 528; `ruppataṃ` gen.pl, line 533); the "gen abs" has no separate subject. (old 13.13) | Same case; drop "(gen abs)" | 5 |
| 13_class.md:545 | `accagamā \| verb \| imperf.3rd.sg` | The only `imperf` tag in the key. | `aor.3rd.sg`; DPD lookup (`accagacchati` is not a DPD headword, so the tense was not confirmed) | 4 |
| 14_class.md:27 | `uttaraṃ \| noun \| masc.acc.sg \| Uttara; lit. higher \| √tar･1 a (cross)` | The name is the comparative `ud + tara` "higher"; `√tar` belongs to `uttara` "crossing over". (old 14.16) | Empty Root cell (DPD: uttara 2.04 masc, name, `ud + tara`, no root) | 8 |
| 14_class.md:61 | `kumārassa \| noun \| masc.dat.sg \| for prince \| √kumār×8 \*e (play)` | verify_key ROOT-MISMATCH: DPD `kumāra` has no root. (old 14.17) | Empty root | 7 |
| 14_class.md:166 | `akāsi \| verb \| aor.2nd.sg \| did; made` | The subject `āyasmā` (line 163) is nominative, which takes the 3rd person (respectful address); `akāsi` is both 2nd and 3rd sg, so the tag is a choice. (old 14.9) | `aor.3rd.sg` | 5 |
| 14_class.md:218 | `adhicittam- \| noun \| nt \| meditation, higher mind` | An accusative governed by `anuyutta` (`adhicittaṃ + anuyuttena`), not a bare stem. (old 14.15) | `nt.acc.sg` | 5 |
| 14_class.md:328 | `vassānaṃ \| noun \| masc.gen.pl \| of years` | `vassa` "year" is neuter in DPD (vassa 1.3); the masculine is "rain; rainy season". (old 14.11) | `nt.gen.pl` | 8 |
| 14_class.md:415 | `abhiññā \| adj \| masc.nom.pl \| with direct knowledge` | Tagged as an adjective of `dhammā`, but glossed and translated (line 425) adverbially; reads as the absolutive "having directly known". (old 14.8) | `verb \| abs` (DPD: abhiññā 3, ger of abhijānāti, "directly knowing") | 7 |
| 14_class.md:458 | `paṭikūlasaññāya \| noun \| fem.instr.sg (+loc)` | AN7.49 has one compound, `āhāre paṭikūlasaññāparicitena`; the key splits it into an inflected `paṭikūlasaññāya` + `paricitena` (sentence line 453), not marked `(simpl)`. (old 14.1) | verify; `paṭikūlasaññā-` + `paricitena` | 7 |
| 14_class.md:497 | `dukkhasamudayaṃ \| noun \| nt.nom.sg` | verify_key IMPOSSIBLE: DPD has `dukkhasamudaya` masc only (`-aṃ` = acc.sg); nom.sg nt works only as an adjective of `saccaṃ`, as the gloss says. (old F5) | `adj \| nt.nom.sg` | 6 |
| 14_class.md:562 | `sāditabbaṃ \| ptp \| nt.nom.sg \| could/should be accepted by \| √sād･1 \*e (taste, relish)` | verify_key ROOT-MISMATCH; the old row gives DPD's group as 8. Also `sādiyeyya` (line 571). (old D8) | `√sād･8 \*e` | 7 |
| 14_class.md:651 | `virājiya \| verb \| abs \| removing; cleansing \| √raj･3 ya (desire)` | `virājeti` is a causative: DPD gives it the sign `\*e` (caus of virajjati), from the same √raj as `virajjati` (sign ya). So the root is right but the sign `ya` is the non-causative one; the old audit's separate root "colour" is not what DPD has. (old D7) | Sign `\*e` in place of `ya` | 7 |
| 14_class.md:774 | `bhedanāya \| noun \| nt.dat.sg \| for breaking \| √bhid･2 ṃa (break, split)` | DPD derives `bhedana` from the causative bhedeti: √bhid with the sign `\*e`. (old D12) | `√bhid･2 \*e` | 7 |
| 14_class.md:802 | `acchejji \| verb. caus.pass \| aor.3rd.sg` | The tag follows DPD (acchejji: aor of caus pass of ā √chid, "completely cut out"), so it stands. The old row's other point remains: MN2 is said to read `acchecchi`, which DPD has as a separate headword (aor of the intensive, same meaning). (old 14.6) | verify the MN2 reading; if `acchecchi`, change sentence and row | 4 |
| 14_class.md:807 | `mān'ābhisamayā \| noun \| masc.instr.sg` | `-ā` on a masculine a-stem is ablative, as `amanasikārā \| noun \| masc.abl.sg` (line 612). (old 14.7) | `masc.abl.sg`; "through the full penetration of conceit" | 8 |
| 15_class.md:135 | `dhammaṃ \| noun \| masc.acc.sg \| doctrine, teaching` | In `yathādhammaṃ` ("properly, according to the rule") the compound is an adverb; the translation (lines 139, 153) has "in accordance with the Doctrine". Also line 149. | `yathādhammaṃ \| ind \| adv` (DPD: ind, adv, abyayībhāva, "fairly; correctly; justly; legally") | 6 |
| 15_class.md:181 | `anavajjā \| adj(\<ptp) \| fem.nom.sg \| faultless; blameless; irreproachable \| √vad･1 a (say, speak)` | The same two words get different roots in the opening and closing sentences: `anavajjā` `√vad･1 a` here, `√vad･8 \*e` at line 241; `ananuvajjā` `√vad･1 a` at line 183, `√vad･8 \*e` at line 243. DPD has `anavajja` from √vad with the sign `\*e` and `ananuvajja` from √vad with the sign `a`, so lines 183 and 241 follow DPD. (old D9) | `anavajjā` `√vad･8 \*e`; `ananuvajjā` `√vad･1 a` | 8 |
| 15_class.md:192 | `katamehi \| pron \| masc.instr.pl \| with what; with which (of the many)` | It qualifies `aṅgehi`, tagged nt (line 174); also `imehi \| pron \| masc.instr.pl` (line 230). Copied from item 2, where the referent `dhammehi` is masc. (old 15.3) | `nt.instr.pl` | 8 |
| 15_class.md:299 | `yathābhūtaṃ \| adj \| masc.acc.sg \| as it truly is` | Adverbial gloss; `ind \| adv` at 3_class.md line 63; also line 318. (old 15.4) | `ind \| adv` (DPD: yathābhūtaṃ ind, adv, "as it truly is") | 8 |
| 15_class.md:358 | `n'ādhiṭṭhāti \| verb \| pr.3rd.sg \| does not take a stand` | Contains the negative but has no `+neg`, unlike `n'atthī'ti \| verb \| pr.3rd.sg +neg` (line 424). (old 15.5) | Add `+neg` | 6 |
| 15_class.md:438 | `ubho \| pron \| masc.acc.pl \| both` | verify_key IMPOSSIBLE: DPD tags `ubho` as dual. Not wrong for a beginner key. (old F9) | Leave, or note `dual` | 3 |
| 6_class.md:488 | `bhante \| noun \| masc.voc.sg \| Venerable sir \| √bhad×1 a (be good, lucky)` | verify_key ROOT-MISMATCH: DPD derives `bhante` from `bhavant` (√bhū). 12 rows: also 7:473, 8:600, 9:349, 9:460, 9:651, 10:308, 11:517, 12:482, 13:127, 15:263, 15:268 (class:line). (old D1) | `√bhū･1 a (be, become)` | 8 |
| 6_class.md:291 | `maggo \| noun \| masc.nom.sg \| the path \| √magg･8 \*e (seek, search)` | The old audit gives DPD's root for `magga` as `√magg･1 a`; also 9_class.md lines 285, 466. (old D2) | `√magg･1 a` (DPD: magga, √magg with the sign a) | 7 |
| 9_class.md:177 | `samaṇo \| noun \| masc.nom.sg \| the recluse \| √sam･3 ya (exert, strive)` | Verb mark `･` where the old audit's DB comparison has DPD's `×`: `samaṇo` ×5 (also 10:440, 11:184, 12:526, 13:513), `mettā` ×4 (11:253, 12:192, 13:390, 15:218), `bhusaṃ` (12:571). (old D20) | DPD lookup: `×` if DPD has it (the lookup output does not print the `･` / `×` mark, so the old claim was not re-confirmed) | 4 |
| 5_class.md:66 | `davāya \| noun \| masc.dat.sg \| for fun, for play \| √dū×1 a (go, run)` | 17 rows with `×` where the old audit's DB comparison has DPD's `･`: also 5:158, 8:51, 8:262, 8:476, 8:620, 9:21, 9:560, 11:170, 11:172, 11:336, 11:640, 12:492, 13:423, 13:425, 14:463, 14:484. (old D21) | DPD lookup | 5 |

## B. Tables, paradigms and lists that disagree with each other or themselves

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 2_class.md:84 | `iti'pi \| sandhi (iti + api)` | The sentence (line 80) writes `itipi`. (old 2.1) | One spelling | 8 |
| 3_class.md:51 | `sabba-rasaṃ \| noun \| masc.acc.sg` | Hyphenated in the table only; the sentence (line 47) writes `sabbarasaṃ dhammaraso`. The same for `joti-pālaṃ` (line 83) vs `jotipālaṃ` (line 78). (old 3.1) | Match the sentence | 6 |
| 4_class.md:24 | `3. [AN3.70](https://s.dhamma.gift/an/an3/index.html#an3.69)<br>abhisaṅkharoti kāyena kusalaṃ.` | Word order differs from the exercise (`kāyena kusalaṃ abhisaṅkharoti`, bpc_ex/4_class.md line 26); the exercise is marked `(simpl)`, the key is not. (old B1) | Align sentence and marker with the exercise | 6 |
| 4_class.md:269 | `saccaṃ bhavantaṃ gotamaṃ apucchimha` | The exercise (bpc_ex/4_class.md line 253) has `saccaṃ mayaṃ bhavantaṃ …`; the key drops `mayaṃ`. (old B2) | Align | 6 |
| 4_class.md:34 | `ime tilā ime taṇḍulā'ti` | The key ends `taṇḍulā'ti`, the exercise (bpc_ex/4_class.md line 37) `taṇḍulā (honti)`; the table has a row `(honti)` (line 50) for a word that is not in the key sentence, and no row for `iti`. (old B3) (old 4.5) | Align sentence and table with the exercise | 6 |
| 4_class.md:304 | `26. [MN86](https://s.dhamma.gift/mn/mn86/index.html) (simpl)<br>` | `(simpl)` in the key only; the exercise (bpc_ex/4_class.md line 286) has no marker. (old B5) | Align | 5 |
| 5_class.md:3 | `viññāṇaṃ na tumhākaṃ, taṃ pajahatha.` | The exercise (bpc_ex/5_class.md line 3) has `viññāṇaṃ, bhikkhave, na (hoti) tumhākaṃ`; the key drops `bhikkhave` and `(hoti)`. (old B6) | Align | 6 |
| 5_class.md:588 | `gaccha \| verb \| imp.2nd.sg \| go! begone!` | The sentence (line 584) has `na me tayā saddhiṃ kathā vā nisajjā vā`; `tayā` has no table row. (old 5.2) | Add `tayā \| pron \| 2nd.instr.sg \| with you` | 9 |
| 5_class.md:594 | `vā \| ind \| \| or` | Empty Grammar cell; every other `vā` has `conj`. | `conj` | 8 |
| 5_class.md:601 | `6. [SNP70](https://s.dhamma.gift/kn/snp/index.html#snp5.16) <br>te diṭṭhiṃ n'ābhijānāmi` | The exercise (bpc_ex/5_class.md line 556) marks the item `(simpl)`, the key does not. The text (Mogharāja) has `diṭṭhiṃ te nābhijānāti` (3rd sg: "the world does not know your view"), so the simplification changes the person. (old B5) | Add `(simpl)` | 6 |
| 6_class.md:3 | `bhagavā bhikkhū āmantesi, bhikkhavo'ti.` | The exercise sentence goes on with `"bhadante"ti`; the key stops at `bhikkhavo'ti`. (old B7) | Align | 6 |
| 6_class.md:35 | `āhuneyyo \| adj \| masc.nom.sg \| worthy of offerings` | The table and the translation (line 37) have `āhuneyyo`, but the sentence (line 28, `esa bhagavato sāvakasaṅgho`) does not. (old 6.1) | Add `āhuneyyo` to the sentence | 9 |
| 6_class.md:97 | `8. [DN16.26](https://s.dhamma.gift/dn/dn16/index.html) (simpl)` | `(simpl)` in the key only; the exercise (bpc_ex/6_class.md line 95) has no marker. | Align | 5 |
| 6_class.md:287 | `atha \| ind \| \| then` | Empty Grammar cell; also `va \| ind \| \| as, like` (line 525). | `adv`; `emph`/`comp` as elsewhere | 8 |
| 6_class.md:301 | `ca \| ind \| conj \| and` | The sentence (line 296) has three `ca`, the table one row; at lines 539–549 the second `ca` (`ācariye ca`) has no row either. Repeated particles get their own rows elsewhere (lines 207–214). (old 6.5) | Add rows | 5 |
| 6_class.md:364 | `sukhitattā \| adj \| masc.nom.pl \| happy` | The sentence (line 353) writes `sukhit'attā`. (old 6.2) | One form | 8 |
| 7_class.md:150 | `anāgatamaddhānaṃ \| ind \| adv \| in the future` | The same phrase from the same sutta is `anāgatam'addhānaṃ` at lines 307 and 318. (old 7.4) | One spelling | 8 |
| 7_class.md:299 | `vā \| ind \| conj \| or` | The sentence (line 291) has `kupitā vā anattamanā vā`; the second `vā` has no row, unlike lines 125–129. (old 7.3) | Add the row | 7 |
| 7_class.md:319 | `evaṃvedano \| adj \| masc.nom.sg \| having such feeling` | The second `siyaṃ anāgatam'addhānaṃ` of the sentence (line 307) has no rows, while repeated words get rows elsewhere. | Add the rows, or mark the repeat | 4 |
| 8_class.md:8 | `kho \| ind \| - \| -` | `-` in the English column; every other `kho` has a gloss ("indeed", line 282). | "indeed" | 6 |
| 8_class.md:40 | `nāma-gottāni \| noun \| nt.acc.pl` | Hyphen in the table only; the sentence (line 31) writes `nāmagottāni`. The same for `abhijjhā-domanassaṃ` (line 138) vs `abhijjhādomanassaṃ` (line 116). (old 8.3) | Match the sentence | 6 |
| 8_class.md:568 | `ca \| \| \| and` | Empty POS and Grammar cells; also line 570. (old A9) | `ind \| conj` | 8 |
| 9_class.md:50 | `nālaṃ \| ind \| neg \| not possible; not able` | The sentence (line 44) writes `n'ālaṃ`; the table `nālaṃ` (also lines 52, 54). | One spelling | 6 |
| 9_class.md:59 | `samudayāya. katamāni tīṇi?` | The question is in the key sentence but not in the table, the translation (line 70) or the exercise (bpc_ex/9_class.md line 45); item 6 (lines 95–107) does include its `katamāni cattāri`. (old B8) (old 9.1) | Remove, or add rows and "What three?" | 9 |
| 9_class.md:85 | `kallaṃ \| ind \| - \| is it suitable?` | The sentence (line 72) has `kallaṃ nu taṃ`; `nu` has no row. (old 9.2) | Add `nu \| ind \| interr` | 9 |
| 9_class.md:635 | `vā \| ind \| conj \| or` | The sentence (line 628) has four `vā`, the table three rows; the final `vā` is missing. (old 9.3) | Add the row | 7 |
| 9_class.md:681 | `yesu idha n'atthi paramaṃ uggahītaṃ` | The exercise (bpc_ex/9_class.md line 633) has the typo `paraṃaṃ`; the key is right. Exercise-side error. (old B10) | Fix the exercise | 9 |
| 10_class.md:136 | `na ca kiñci loke upādiyati` | The key has `ca`; the exercise (bpc_ex/10_class.md line 113) has `na kiñci loke`. (old B11) | verify against SN35.234; align | 6 |
| 10_class.md:325 | `[SN12.22](https://s.dhamma.gift/sn/sn12/index.html#sn12.22) (simpl)` | `(simpl)` in the key only; the exercise (bpc_ex/10_class.md line 275) gives the same sentence without it. (old B5) | Align | 5 |
| 10_class.md:539 | `attānaṃ samanupassato pāmojjaṃ jāyati.` | The exercise (bpc_ex/10_class.md line 477) writes `attānaṁ` and `pāmojjaṁ` with `ṁ`. Exercise-side. (old B15) | Fix the exercise | 9 |
| 11_class.md:174 | `ca-assa \| verb \| opt.3rd.sg \| and he should be` | `cassa` (= `ca assa`) is one row with a hyphen, while the sentence's other `ca` has its own row (line 171). | Two rows: `ca`, `assa` | 5 |
| 11_class.md:530 | `sammāsaṅkappagocarā.` | The exercise (bpc_ex/11_class.md line 444) has `sammāsaṅkappe gocarā`; Dhp 12 has the compound, so the key is right. Exercise-side. (old B12) | Fix the exercise | 7 |
| 12_class.md:94 | `n'āhaṃ, bhikkhave, aññaṃ ekadhammam'pi samanupassāmi` | Both `bhikkhave` in the sentence have no table row (lines 98–120); every other item lists it. (old 12.2) | Add the rows | 7 |
| 12_class.md:377 | `ko ca āhāro pañcannaṃ nīvaraṇānaṃ?` | The exercise (bpc_ex/12_class.md line 312) has the typo `ahāro`. Exercise-side. (old B13) | Fix the exercise | 9 |
| 12_class.md:462 | `vassaṁ \| noun \| nt.acc.sg \| year` | The sentence (line 437) has `cattārīsaṃ api vassāni` and `paññāsaṃ api vassāni`; this row and line 466 are copies of line 448. (old 12.1) | `vassāni \| noun \| nt.acc.pl \| years` | 9 |
| 13_class.md:31 | `[MN20](https://s.dhamma.gift/mn/mn20/index.html) <br>kiṃ nu kho ahaṃ sīghaṃ gacchāmi?` | The exercise (bpc_ex/13_class.md line 22) marks this item `(simpl)`, the key does not. (old B5) | Align | 5 |
| 13_class.md:537 | `yathābālaṃ yathāmūḷhaṃ yathāakusalaṃ` | `yathāakusalaṃ` has no table row (lines 546–548); the translation (line 557) has "so unskilfully". (old 13.1) | Add the row | 10 |
| 14_class.md:68 | `divasaṃsantatte ayokaṭāhe` | The sentence writes one word; the table splits it as `divasaṃ-` (line 72) with a compound hyphen and tags it `ind`; the exercise (bpc_ex/14_class.md) has `divasaṃ santatte`. | One compound `divasaṃsantatta` (DPD headword, adj, `divasaṃ + santatta`); one spelling in sentence, table and exercise | 6 |
| 15_class.md:160 | `kho, \| ind \| emph \| indeed; certainly` | The table for `imehi kho, bhikkhave, tīhi dhammehi samannāgato bālo veditabbo` (line 155) stops after two rows; six words have no row. Items 1 and 3 give full tables for their closing sentence. (old 15.1) | Add the rows, or a note that they repeat lines 101-106 | 7 |

## C. Translation and gloss problems

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 2_class.md:8 | `kira \| ind \| adv \| indeed, truly` | In SN10.8 Anāthapiṇḍika hears the news second-hand: `kira` marks hearsay ("it is said"). The translation (line 12) follows the gloss. (old 2.11) | "it is said; reportedly" (DPD kira 2); translation "A Buddha, it is said, has arisen in the world." DPD also has "really; truly" (kira 1), so the gloss is a possible sense: owner decision | 4 |
| 2_class.md:53 | `**the state of a superior human being, the attainment of knowing and seeing, suitable for a noble person,**` | `uttarimanussadhamma` is a state beyond the human (a "superhuman state"), not the state of a superior human; the rendering follows the drill split on line 42, not the compound. | "a superhuman state, a distinction in knowledge and vision worthy of the noble ones" (DPD uttarimanussadhamma: "super-human state") | 6 |
| 2_class.md:100 | `endowed with wisdom and ethical conduct` | The gloss of `vijjācaraṇasampanno` (line 89) says `knowledge and conduct`. (old 2.9) | Align ("knowledge and conduct") | 6 |
| 2_class.md:347 | `domanassa- \| noun \| - \| depression` | One word, several renderings: `domanassa` "distresses" (line 222), "depression" here, "displeasure" in the translation (line 351); `jarā` "old age" (line 342) vs "aging"; `upāyāsā` "afflictions" (line 348) vs "despair". (old 2.10) | One rendering per word within the item | 5 |
| 2_class.md:25 | `**At the foot of a tree in a forest, in valleys, and in caves.**` | `rukkhānaṃ` is gen.pl (line 19, "of trees"); the translation has a singular. (old 2.7) | "At the foot of trees in a forest, in valleys and in caves." | 6 |
| 2_class.md:367 | `ābādhāya \| noun \| masc.dat.sg \| to sufferings` | Plural gloss for a singular; the translation (line 369) says "to suffering". (old 2.6) | "to affliction" | 8 |
| 3_class.md:110 | `**He experiences pleasure by means of the body.**` | `ca` (line 106) is left untranslated. (old 3.3) | "And he experiences pleasure with the body." | 5 |
| 3_class.md:316 | `**You see that offence.**` | In the Vinaya this line is a question put to the monk. (old 3.5) | "Do you see that offence?" | 4 |
| 3_class.md:217 | `(on tour) in the Mallans.` | `mallesu` with a verb of going is "to/among the Mallas"; "in the Mallans" is not idiomatic, and the people are usually called the Mallas and the Kosalans/Kosalas. | "sets out from the Kosalans to the Mallas (on tour)" | 4 |
| 4_class.md:20 | `upapajjāmi \| verb \| pr.1st.sg \| I am reborn; I go towards` | `upapajjati` + acc of a destination is "is reborn in"; the translation (line 22) chose the weaker "I go towards". (old 4.10) | "I am reborn in a good destination, a heavenly world." | 6 |
| 4_class.md:145 | `chinda \| verb \| imp.2nd.sg \| cross, lit. cut` | `chinda` is "cut"; "cross" is `tarati`. The translation (line 152) says "Cross the stream". (old 4.11) | "cut"; "Cut the stream" | 6 |
| 4_class.md:236 | `**He says, "There are here some noblemen [and] brahmins."**` | `ca` is in the sentence and the table (line 231), so "and" is not a supplied word. (old 4.12) | "and" without brackets | 7 |
| 4_class.md:361 | `pessako \| noun \| masc.nom.sg \| messenger` | In MN98's list the sense is "servant"; `vāṇijo` is "merchant" (line 358) in the table but "a trader" in the translation (line 365). (old 4.13) | "servant" (DPD pessaka 2; "messenger" is pessaka 1, so both are DPD senses); one word for `vāṇija` | 5 |
| 4_class.md:32 | `**He does good deeds by means of the body.**` | `kusalaṃ` is singular (line 30). (old 4.14) | "He does a good deed by means of the body." | 5 |
| 4_class.md:377 | `**One is disenchanted in suffering, this [is] the path for purification.**` | Idiom: "disenchanted with". (old 4.14) | "One becomes disenchanted with suffering; this is the path to purification." | 5 |
| 4_class.md:427 | `**It was a thought of the recluse.**` | `ahu` + genitive is possession: "the recluse had a thought". (old 4.14) | "A thought arose in the recluse." / "The recluse had a thought." | 6 |
| 4_class.md:302 | `**May you all be happy (and) free from disease.**` | Order reversed against the sentence (`arogā sukhitā`). (old 4.14) | "May you all be healthy and happy." | 4 |
| 5_class.md:37 | `**Our lifestyle should be purified.**` | The same MN39 construction (`parisuddho no … bhavissati`) is "will be pure/purified" at line 349; the table (line 35) gives both "will" and "should". (old 5.17) | "Our livelihood will be purified." | 6 |
| 5_class.md:72 | `vibhūsanāya \| noun \| nt.dat.sg \| for decoration, for bulk` | "for bulk" does not fit `vibhūsana`; the translation (line 74) has "physical appearance", which matches neither gloss. (old 5.14) | "for decoration; for beautification", and the same in the translation | 5 |
| 5_class.md:112 | `**False teaching leads to no good fortune, the Teaching leads to a good destination.**` | `nirayaṃ` is glossed `hell; no good fortune` (line 106); the translation uses the etymological gloss and loses the contrast with `suggatiṃ`. (old 5.13) | "False teaching leads to hell; the Teaching leads to a good destination." | 6 |
| 5_class.md:273 | `**Whatever conversation was with wandering ascetics,` | Ungrammatical. (old 5.18) | "Whatever conversation there had been with the wandering ascetics, …" | 6 |
| 5_class.md:324 | `**Services (done) on us could be of great fruits.**` | `bhavissanti` is future (line 322 has "could be" as a second gloss); "fruits" for "fruit". (old 5.18) | "Services done for us will be of great fruit." | 6 |
| 5_class.md:361 | `**Having not raised up a high trunk, I will approach families. [I will not arrogantly approach families]**` | `na` negates `upasaṅkamissāmi`: the monk will not approach families with his trunk raised. The main translation negates the absolutive instead and so says the opposite; only the bracket is right. | "I will not approach families with a raised trunk (arrogantly)." | 7 |
| 5_class.md:380 | `sarīraṃ \| noun \| nt.acc.sg \| the corpse; dead body` | In DN16 the flowers fall on the living Tathāgata, lying between the sāla trees; the translation (line 383) also says "dead body". (old 5.9) | "body" | 7 |
| 5_class.md:381 | `okiranti \| verb \| pr.3rd.pl \| are sprinkled on` | Passive gloss for an active verb whose subject is `pupphā`; the translation (line 383) follows it. (old 5.10) | "strew; scatter on" (DPD: okirati "sprinkles; scatters down (onto)"); translation as proposed in the lesson audit (bpc class_5/5_trans.md:17), which needs a transitive verb: "Flowers cover the body of the Tathāgata." | 6 |
| 5_class.md:530 | `kadariyaṃ \| noun \| nt.acc.sg \| stinginess` | In Dhp 223 it parallels `alikavādinaṃ`, a person ("the liar"); `kadariya` is also an adjective "miserly". The translation (line 536) has "conquer liar by truth". (old 5.5) | `adj \| masc.acc.sg \| the miser` (DPD kadariya 1 adj "miserly"; the nt noun "miserliness" is kadariya 2, so the tag is also a DPD reading); "Conquer the miser by giving, the liar by truth." | 6 |
| 5_class.md:549 | `**It is enough for deluding a fool not one seeking Nibbāna.**` | The contrast is unmarked. (old 5.15) | "It is enough to delude a fool, but not one seeking the far shore." | 7 |
| 5_class.md:582 | `**You are truly for us equal to the Brahma.**` | Word order, article, diacritic. (old 5.16) | "Truly, for us you are equal to Brahmā." | 6 |
| 5_class.md:629 | `you must make [your] mind unified!**` | The second `jhāne` (line 624) is untranslated. (old 5.11) | "…make your mind unified in meditation!" | 7 |
| 5_class.md:618 | `brāhmaṇa \| noun \| masc.voc.sg \| monk; sage; holy man` | Rendered "Monk" in the translation (line 629). In SN40.1 the Buddha addresses Moggallāna, so the choice is defensible, but "monk" is not a sense of `brāhmaṇa`. (old 5.12) | "brahmin" with a note on the addressee | 4 |
| 6_class.md:197 | `**"(He) who is equanimous [and] mindful lives at ease."**` | `sukhavihārī` is an adjective, the third item of a list (`upekkhako satimā sukhavihārī`), not a finite verb. | "Equanimous, mindful, one who lives at ease." | 4 |
| 6_class.md:342 | `hirimanto \| adj \| masc.nom.pl \| conscientious` | The glosses of `hirimanto` and `ottappino` (line 344, `feeling shame`) look swapped; class 5 (5_class.md line 168) has `ottappino … conscientious`. DPD: hirimant "having a conscience; with scruples", ottappī "afraid of wrong; conscientious"; "feeling shame" fits neither DPD entry for `ottappī`. (old 6.10) | `hirimanto` "having a sense of shame; having a conscience"; `ottappino` "afraid of wrong; conscientious" | 7 |
| 6_class.md:390 | `paricara \| verb \| imp.2nd.sg \| you must minister; enjoy` | "enjoy" does not fit the imperative "attend on, serve". (old 6.16) | "attend on; serve" | 5 |
| 6_class.md:408 | `would approach [there], cause an alteration in a robe…` | The futures (glossed "will", lines 403, 406) are rendered "would"; the two clauses have no "and". (old 6.13) | "If that monk … will approach and cause an alteration in a robe…" | 5 |
| 6_class.md:450 | `**The looking after mother and father, the support of the wife and son.**` | The Pāli order is son, then wife; "The looking after mother" lacks "of". (old 6.14) | "Looking after mother and father, supporting son and wife." | 5 |
| 6_class.md:465 | `**Just make an effort today;` | `eva` qualifies `ajja`: "this very day". (old 6.15) | "Make an effort this very day;" | 5 |
| 6_class.md:533 | `who sees fault, he is (like) one who points out the treasure.**` | Comma splice; `nidhīnaṃ` is gen.pl (line 524, "of treasures"). (old 6.11) | "…who sees faults, like one who points out treasures." | 6 |
| 6_class.md:542 | `atho \| ind \| ind \| and then; after that` | `atho` here adds an item ("and also"); it is not temporal. The translation (line 551) says "and after that". (old 6.12) | "and also"; "and also towards the eldest brother" | 5 |
| 7_class.md:77 | `**How then could thieves not steal my valuables?**` | `kinti … na corā hareyyuṃ` expresses concern or purpose ("how can I make sure thieves don't take my wealth?"); the English reads as surprise that they could not steal it. | "How can I make sure that thieves do not steal my possessions?" | 5 |
| 7_class.md:121 | `rājāno \| noun \| masc.nom.pl \| king's men` | `rājāno` is "kings"; the translation (line 131) follows the gloss. (old 7.18) | "kings [i.e. the king's men]" | 5 |
| 7_class.md:124 | `haneyyuṃ \| verb \| opt.3rd.pl \| they could punish` | In Pārājika 2 `haneyyuṃ` is "would kill/execute" (`√han`, "strike, kill" in the Root cell); "punish" weakens it. | "they could execute" | 5 |
| 7_class.md:225 | `**And now there could be, Ananda, for you it would occur like this:` | `siyā` and `assa` both rendered; the sentence breaks. (old 7.17) | "Now, Ānanda, it could be that you think thus:" | 5 |
| 7_class.md:289 | `which I am grasping [and] would not be with faults` | `upādiyamāno` is subordinate to `assaṃ`, not a coordinate verb. (old 7.16) | "…which, grasping it, I would not be blameworthy." | 6 |
| 7_class.md:362 | `upāsikāyo \| noun \| fem.nom.pl \| female disciples` | "lay" missing; the translation (line 364) has "female lay disciples". (old 7.15) | "female lay disciples" | 7 |
| 7_class.md:431 | `**Bhikkhus, the monks will establish mindfulness individually` | `bhikkhave` and `bhikkhū` are rendered two ways in one line; the quoted clause is a question in the Pāli. (old 7.19) | "Monks, the monks will…" | 5 |
| 7_class.md:466 | `**What one could do with a well, if there always would be water?; Having cut off the craving from the source, why would he go about searching?**` | Word order; `?;`; `taṇhāya` is tagged gen (line 459) but translated as the object. (old 7.20) | "What could one do with a well if there were water at all times? Having cut craving at the root, why would one go about searching?" | 6 |
| 7_class.md:484 | `parihāyanti \| verb \| pr.3rd.pl \| wasting away; decreasing` | Participle gloss for a finite verb. (old 7.20) | "they decline; they fall away" | 6 |
| 8_class.md:42 | `**The great rivers, upon reaching the mighty ocean, they give up (their) old names.**` | `-gottāni` ("family names", line 40) is dropped; redundant "they". (old 8.9) | "The great rivers, on reaching the great ocean, give up their former names and family names." | 7 |
| 8_class.md:329 | `**This monk who speaks according to the Dhamma, and this monk who speaks according to the Vinaya, speaks according to (i.e. in accordance with) our preference and approval…**` | Three coordinated predications ("this monk is a speaker of Dhamma, … of Vinaya, … speaks taking up our wish") are turned into one relative clause. (old 8.12) | "This monk speaks according to the Dhamma, this monk speaks according to the Vinaya, and this monk speaks with our consent and approval…" | 6 |
| 8_class.md:367 | `having done this just for that reason, [and] no other` | `etaṃ eva paccayaṃ karitvā anaññaṃ` is "having made just this the reason and no other"; `eva` is glossed `thus; just` (line 361), but it is not "thus". (old 8.13) | "having made just this, and nothing else, the reason" | 6 |
| 8_class.md:385 | `uṭṭhānasaññaṃ \| noun \| fem.acc.sg \| wake-up time` | `saññā` is "perception, notion": "the perception (thought) of getting up", not a time; the translation (line 388) follows the gloss. | "the thought of getting up" | 5 |
| 8_class.md:417 | `sabbanimittānaṃ \| noun \| nt.gen.pl \| of all objects` | The same stem `nimitta` is "signless" (`animitta`, lines 414, 420); "objects" hides the link. (old 8.15) | "of all signs" | 4 |
| 8_class.md:448 | `**"This [is] my mother, this [is] the mother of my mother"; [the sequence] of that man's mothers' mothers would not even be exhausted.**` | `bhikkhave` (line 442) is left out. (old 8.10) | Add "monks" | 7 |
| 8_class.md:560 | `that monk can set [it] aside for a month at the most` | `nikkhipeyya` is glossed "should set aside" (line 553); the translation says "can". (old 8.15) | "should set it aside" / "may keep it" | 4 |
| 8_class.md:538 | `**He generates interest, puts forth effort, arouses energy, exerts his mind and strives for the continuance, non-disappearance , increase and fulfillment by development, maturity, of wholesome qualities that have arisen.**` | The order of the datives is garbled, and `bhāvanāya` is tagged dat (line 527) but translated "by". (old 8.14) | "…for the persistence, non-decay, increase, abundance, development and fulfilment of wholesome qualities that have arisen." | 6 |
| 8_class.md:602 | `dhammo \| noun \| masc.nom.sg \| the teaching; the doctrine` | In `kocideva dhammo samuppādo uppajjeyya` `dhammo` is "a matter, an issue"; the translation (line 612) adds "[concerning] the teaching". | "some matter (dispute) could arise" | 4 |
| 8_class.md:636 | `of a man enamoured with regard to women, just that long he [is] like a suckling calf towards [its] mother.**` | `paṭibaddhamano` is nominative and goes with `so`, not with the genitive `narassa`. (old 8.11) | "…just that long is he bound in mind, like a suckling calf to its mother." | 7 |
| 9_class.md:191 | `atha \| ind \| ind \| after` | `kho` (line 192) is glossed `that`: "after that" was split across the two words. Line 127 treats `atha kho` as one unit. (old 9.13) | One row `atha kho`, "and then" | 9 |
| 9_class.md:213 | `**Seeing danger in the slightest fault, train yourself [by] undertaking the training precepts.**` | `vajjesu` is plural; the locative `sikkhāpadesu` ("in the training rules") is lost; "precepts" vs the gloss "rules" (line 211). (old 9.19) | "Seeing danger in the slightest faults, undertake and train in the training rules." | 5 |
| 9_class.md:367 | `**Is the Blessed One, the Arahant, the Perfectly Enlightened One able to act in such a way` | `bhante` and `pana` (lines 348, 349) are untranslated. (old 9.14) | "But, venerable sir, is the Blessed One…" | 8 |
| 9_class.md:486 | `**But because form is not self, therefore it leads to oppression.**` | `bhikkhave` is left out; "oppression" is the "lit." gloss, not the primary "illness" (line 483). (old 9.15) | "But because form, monks, is not self, form leads to affliction." | 8 |
| 9_class.md:564 | `**They were not overly zealously desiring medicines and requisites for life.**` | `paccaye` ("supports", line 558) is left out; the order is changed. (old 9.16) | "They were not overly eager for the requisites of life, medicines and supports." | 7 |
| 9_class.md:663 | `I, too, will myself be able to make safety.**` | `api` goes with `ekam'ekena` ("even by a single one"); `attānaṃ sotthiṃ kātuṃ` is "to make myself safe". (old 9.17) | "…even by a single one of these eleven doors to the deathless, I will be able to make myself safe." | 6 |
| 9_class.md:674 | `anissito \| pp \| masc.nom.sg \| unhindered; independent (of)` | In context "unsupported"; "independent" (also in the translation, line 679) hides why he cannot cross. (old 9.18) | "unsupported" | 6 |
| 10_class.md:10 | `āha \| verb \| perf.3rd.sg \| he had said` | Pluperfect here; "he said" for the same form at lines 19, 29, 38 and in every translation. (old 10.16) | "he said" | 8 |
| 10_class.md:59 | `passeyyaṃ \| verb \| opt.1st.sg (reflexive) \| I could see by myself` | The tag is right (DPD: `passati` reflx opt 1st sg; the verify_key IMPOSSIBLE flag comes from the `(reflexive)` wording), but the reflexive ending does not mean "by myself". The translation (line 63) repeats "I myself" and drops the implied quote after `ākaṅkhati` ("If he wishes: 'May I see…'"). | "I could see"; "If he wishes, [he thinks:] 'I could see beings…'" | 6 |
| 10_class.md:168 | `eva \| ind \| emph \| just; thus` | `eva` is not "thus", yet the translation (line 171) says "thus". Gloss and translation also disagree for `parinibbāyati` ("is completely quenched", line 169, vs "attains final liberation") and for `paritassati`/`aparitassaṃ` ("perturbed" vs "shaking", lines 160, 166). (old 10.15) | "just"; align glosses with the translation | 6 |
| 10_class.md:219 | `**Just like a monkey [who is] wandering around in a woodland, in a forest.**` | `bhikkhave` is left out; forest and woodland are in reverse order (`araññe pavane`). (old 10.10) | "Just as, monks, a monkey wandering in a forest, in a woodland…" | 8 |
| 10_class.md:274 | `haritabbāni \| ptp \| nt.nom.pl \| it can be carried` | A plural ptp of obligation: "they are to be carried"; the translation (line 278) has "it could be carried". (old 10.13) | "are to be carried" | 6 |
| 10_class.md:285 | `me \| pron \| 1st.gen.sg (gen abs) \| while me` | "while me" is not English; the translation (line 291) is right. | "(while) I" | 5 |
| 10_class.md:334 | `sampassamānena \| prp \| masc.instr.sg \| by means of seeing; considering` | With `alaṃ` the instrumental marks the person for whom it is fitting: "for one who considers… it is fitting to strive"; the translation (line 340) keeps "by considering". (old 10.14) | "for one considering" | 6 |
| 10_class.md:384 | `āpajjato \| prp \| masc.dat.sg<br>(or) <br>masc.gen.sg \| for arousing; <br>(or) when exhibiting` | Two different verbs in one gloss; with `parivīmaṃsaṃ` the verb is "engages in, undertakes" (the translation, line 389, has "exhibiting"). (old 10.18) | "engaging in" | 6 |
| 10_class.md:405 | `**The mind of him who sees and knows is released` | Order reversed (`jānato … passato`) and both `evaṃ` dropped. (old 10.11) | "…of him who knows thus, who sees thus…" | 7 |
| 10_class.md:428 | `this is my instruction to them.**` | `evarūpī` ("of such a kind", line 424) is not translated. (Old 10.18 also said "this" is not in the Pāli; it is: `ayaṃ`.) (old 10.18) | "…for them my instruction is of this kind." | 6 |
| 10_class.md:445 | `**One who has gone forth certainly does not harm another, a monk is not troubling another.**` | Subject and predicate inverted: Dhp 184 says one who harms another is not one gone forth, one who troubles another is not an ascetic. (old 10.8) | "One who harms another is not one gone forth; one who troubles another is not an ascetic." | 8 |
| 10_class.md:521 | `idaṃ \| pron \| nt.nom.sg \| that; lit. this` | One word glossed three ways in one sentence ("that; lit. this", "this" line 529, "that" line 534); also `amutra` "there" / "in such-and-such place" (lines 691, 695) and `imesaṃ` "of those" / "to these" (lines 693, 699). (old 10.17) | Align | 6 |
| 10_class.md:636 | `**When a monk having desire for sense pleasure internally` | `idha, bhikkhave` dropped; `santaṃ` agrees with `kāmacchandaṃ` ("sensual desire being present"); no "when" in the Pāli; `pajānāti` (line 644) is only in the next translation. (old 10.12) | "Here, monks, a monk, when sensual desire is present internally, knows…" | 7 |
| 10_class.md:704 | `**Thus, having heard here,` | Nothing means "thus"; `ito` is "from here" (line 688). (old 10.9) | "Having heard from here…" | 8 |
| 10_class.md:758 | `searching the builder of this house` | "searching for"; "this" is not in the Pāli (`gahakāraṃ`). (old 10.18) | "seeking the house-builder" | 6 |
| 11_class.md:66 | `hoti \| verb \| pr.3rd.sg \| there is; there was` | "there was" is not a present-tense gloss. (old 11.18) | "there is" | 6 |
| 11_class.md:133 | `**The foolish, untrained, wicked man maintains himself injured and damaged.**` | Gloss and translation disagree: `asappuriso` "not a good man" (line 127) vs "wicked man"; `pariharati` "carries around" (line 131) vs "maintains". | Align | 5 |
| 11_class.md:146 | `adhunā- \| ind \| adv \| soon, recently` | "soon" is wrong. Also `yassa` "of which; whoever" (line 674) is "whose"; `ye`/`yo` "which" for persons (lines 628, 632, 636); `sāsane` "the teachings" (line 569) lacks "in". (old 11.20) | "recently, just now"; "whose"; "who"; "in the teaching" | 6 |
| 11_class.md:306 | `tāni \| pron \| nt.nom.pl \| these` | `tāni` is "those", as in the translation (line 319). (old 11.17) | "those" | 7 |
| 11_class.md:341 | `[that] which [is] near or far away` | Order reversed (`dūre santike`). Also "about Venerable Gotama" (line 29) leaves `taṃ` out, and "straight, upright" (line 178) loses the `su-` of `suhujū`. (old 11.21) | "far or near"; "very upright" | 5 |
| 11_class.md:367 | `sallato \| ind \| adv \| as an arrow; a dagger` | `salla` is a dart or arrow, not a dagger; the translation (line 376) has only "as a dagger". (old 11.19) | "as a dart" | 6 |
| 11_class.md:425 | `**For one perceiving acquisition as a personal acquisition of forms` | The genitive chain is attached to the wrong noun, and "personal" has no source. (old 11.16) | "For one regarding the acquisition of forms … as an acquisition…" | 6 |
| 11_class.md:442 | `**The teaching by the Blessed One [is] well taught,` | `bhagavatā` goes with `svākkhāto`: "well proclaimed by the Blessed One is the Dhamma". | "Well proclaimed by the Blessed One is the Dhamma…" | 6 |
| 11_class.md:611 | `‘that which the world [is] the self (world = self);` | Garbled: `so loko so attā` is "that [which is] the world, that [is] the self"; the third `so` is untranslated. (old 11.15) | Reword | 7 |
| 12_class.md:12 | `api \| ind \| \| just only` | `pi` is "also, even", not limiting, yet the item glosses "just two" … "just one hundred thousand births" (lines 14–27); in item 21 `api` is "only" (lines 447, 461, 465) and "even" (lines 451, 469) in one sentence, and the translation (line 475) says "just one year". The Grammar cell is empty. (old 12.16) | "even; also" | 6 |
| 12_class.md:29 | `**I recollected manifold past lives,` | `anussarāmi` is present, glossed "I remember" (line 9). (old 12.11) | "I recollect" | 7 |
| 12_class.md:87 | `bhikkhu-satehi \| noun \| nt.instr.pl \| with one hundred monks` | A plural ("hundreds"); also `sahassānaṃ` "for one thousand" (line 347). (old 12.15) | "with hundreds of monks"; "thousands" | 6 |
| 12_class.md:375 | `**Surely, a monk endowed with these ten qualities` | `bhikkhave` is untranslated. (old 12.12) | "Surely, monks, a monk…" | 8 |
| 12_class.md:489 | `aṭṭhakavaggikāni \| adj \| nt.acc.pl \| from the fourth chapter of the Sutta Nipāta` | The translation (line 495) has "belonging to the groups of eight", which reads as a count, not the Aṭṭhakavagga. | "…all sixteen [suttas] of the Aṭṭhakavagga" | 6 |
| 12_class.md:599 | `having then seen that should speak` | "then" has no source; `tam'enaṃ` is "him" (so the table, line 585). (old 12.14) | "having seen him, should speak…" | 6 |
| 12_class.md:605 | `vanappagumbe \| noun \| masc.loc.sg \| forest grove` | Tagged locative (also `phussit'agge`, line 607), but the translation (line 618) makes it the subject of the simile. (old 12.8) | Tag and translation should agree | 5 |
| 12_class.md:610 | `gimhe \| noun \| masc.loc.sg \| in heat; hot` | `paṭhamasmiṃ gimhe` is "in the first month of summer", not "the first heat of the hot month" (line 618); the translation also drops `tath'ūpamaṃ` and attaches `paramaṃ` to Nibbāna. (old 12.13) | "in the first month of summer"; "so too he taught the sublime teaching leading to Nibbāna, for the highest benefit" | 6 |
| 13_class.md:29 | `**He touches the earth evenly with the entire sole of [his] foot**` | `pādatalehi` is plural ("soles of [his] feet"), as the gloss (line 25) says; `samaṃ` is "evenly" (line 12) but "in a balanced manner" (line 19). (old 13.20) | "…with the entire soles of [his] feet"; "evenly" throughout | 6 |
| 13_class.md:127 | `bhante \| noun \| masc.voc.sg \| lord, master` | "venerable sir" everywhere else; the translation (line 131) says "Master". | "venerable sir" | 5 |
| 13_class.md:148 | `parimuccati \| verb.pass \| pr.3rd.sg \| he is released` | The same verb in one sentence is "is freed" (line 151), "is completely freed" (lines 156, 161). (old 13.19) | One rendering | 7 |
| 13_class.md:223 | `tassa \| pron \| masc.dat.sg \| for this` | "that"; also `lokasmiṃ` "the world" without "in" (line 321) and `assā'ti` "would he" (line 229), a fragment with no end-quote note. (old 13.21) | "for that"; "in the world" | 6 |
| 13_class.md:286 | `**for what [is] pleasant and enticing in the world this craving here` | `yaṃ` is nominative, there is no "for"; the adjective order is swapped against the table; "is ceased" (see the row above). (old 13.17) | "Whatever in the world is enticing and pleasant: here this craving, being abandoned, is abandoned; here, ceasing, it ceases." | 7 |
| 13_class.md:347 | `kulāni \| noun \| nt.nom.pl \| householders; supporters` | `kula` is "family"; the translation (line 355) says "the householders". | "families" | 5 |
| 13_class.md:475 | `(a helper) should come up with that robe cloth` | In NP 10 the subject of `abhinipphādeyya` is the monk who stands silently; the translation invents another subject. (old 13.18) | "…he should get that robe cloth produced" | 6 |
| 13_class.md:516 | `**He [is one] who makes subside evil deeds` | `ca` dropped and `sabbaso` moved to the second clause; at line 427 the table has `ca` but the translation "or". (old 13.22) | Reword | 5 |
| 13_class.md:563 | `jayaṃ \| noun \| nt.nom.sg \| victory` | DPD has a neuter `jaya`, so the tag is possible, but the commentary on Dhp 201 reads the prp ("the victor"), pairing with `parājito`; translation line 570. (old 13.10) | `prp \| masc.nom.sg`; "The victor breeds enmity" | 6 |
| 13_class.md:633 | `[are] neither not here, nor in another world` | The double negative reverses the sense. (old 13.16) | "neither here, nor in another world" | 9 |
| 14_class.md:18 | `**He causes this very body to overflow, to flow around, to fill up all around, to suffuse with the joy and happiness born from separation` | `parippharati` (line 16) is plain `verb`, not causative; "this very body … to suffuse" reverses who suffuses what; "happiness" and "separation" against the glosses "ease" (line 12) and "solitude" (line 11). (old 14.22) | "He drenches, steeps, fills and suffuses this very body with the joy and ease born of solitude." | 6 |
| 14_class.md:42 | `**You should develop wholesome qualities.**` | `bhikkhave` (line 39) is not translated, nor at line 51 or line 441, where `ca` of `yāvakīvañ'ca` is also dropped. (old 14.20) | Add "monks"; "And as long as…" | 7 |
| 14_class.md:92 | `eva \| ind \| \| only` | In `c'eva … na ca` ("both … and not") `eva` does not mean "only"; the Grammar cell is empty. `c'eva` is analysed three ways in this file (`ca-` + `eva` lines 91-92, `ind+ind` line 374, `ind+emph` line 622), as are `atha kho` (lines 24, 57 against 686-687) and `yo pana bhikkhu` (line 286 against 306-308, 507-509). (old 14.30) | One analysis per phrase; `c'eva` "both" | 7 |
| 14_class.md:156 | `**Just this is the end of the underlying tendency towards conflict.**` | `anusayānaṃ` (line 154) is plural; at line 631 `c'eva … ca` is "both … and", not "and even". (old 14.24) | "…of the underlying tendencies to aversion"; "both unarisen taints do not arise and arisen taints are abandoned" | 6 |
| 14_class.md:276 | `āsavānaṃ \| noun \| masc.gen.pl \| of impurities, defilements` | `āsava` is "effluents; taints" at lines 623, 628, 652; `sutte` "scripture(s)" (lines 369, 373) against "discourse(s)" (line 675); `pācittiyaṃ` "a case requiring confession" (line 298) against "an offence" (line 573); four wordings of the two robes (lines 551-564). (old 14.28) | One rendering each | 6 |
| 14_class.md:348 | `āvuso \| ind \| voc.sg \| friend` | In MN18 Mahākaccāna addresses a group of monks; also the translation (line 361). (old 14.12) | "friends" | 6 |
| 14_class.md:451 | `**they will practise accepting the training rules as they had been formulated.**` | The third condition of the `yāvakīvaṃ` clause reads as a main clause; "had been" is the wrong tense. (old 14.23) | "[and] will proceed, having undertaken the training rules as they have been laid down," | 6 |
| 14_class.md:478 | `**[his] mind withdraws from, bends back from, rolls back from craving for tastes,**` | `na sampasāriyati` (lines 475-476) is not translated. (old 14.18) | Add "[and] is not drawn out towards it" | 9 |
| 14_class.md:496 | `pan'idaṃ \| ind \| ind+pron \| moreover` | `idaṃ` is lost in the gloss, and `taṃ` (line 494) is glossed "this" to make up for it. (old 14.26) | "moreover, this"; `taṃ` "that" | 6 |
| 14_class.md:585 | `asevitabbe \| ptp \| masc.acc.pl \| should not be associated with; should be followed` | The second gloss drops the negation. (old 14.19) | "should not be followed" | 9 |
| 14_class.md:603 | `**He doesn't know the things that should be adhered to, he doesn't know the practices that should not be adhered to.**` | `dhamme` is "things" and "practices" inside one sentence (also line 590); `padabyañjanāni` "words and letters" (line 667) but "words and phrases" (line 671). (old 14.25) | Align | 7 |
| 15_class.md:65 | `gacchati, \| verb \| pr.3rd.sg \| he gets; lit. goes; moves` | The subject is the neuter "what has been eaten, drunk…" (lines 59-62), not "he". (old 15.9) | "it goes (to)" | 7 |
| 15_class.md:137 | `paṭikaroti, \| verb \| pr.3rd.sg (+acc) \| redress, fix, make amends` | Bare verbs for pr.3rd.sg, where other rows inflect; also `engage in` (line 355), `grasp; cling to` (line 357). (old 15.13) | "redresses…"; "engages in"; "grasps" | 7 |
| 15_class.md:147 | `desentassa \| prp \| masc.gen.sg (gen abs) \| when pointing out; preaching; expounding` | `accayaṃ deseti` is "confesses a fault"; "pointing out" (also the translation, line 153) reads as another person criticising the fool. (old 15.7) | "when another is confessing a fault" | 7 |
| 15_class.md:187 | `**Monks, speech endowed with five factors is well-spoken` | `aṅgehi` is "factors" here and "these five qualities" in the closing sentence (line 247); glosses "parts, factors; qualities" (line 174) against "qualities" (line 234). (old 15.12) | One rendering | 6 |
| 15_class.md:265 | `kittāvatā \| ind \| adv+interr \| in what way` | The correlative `ettāvatā` (line 397) is "to this extent"; also the translation (line 272). (old 15.10) | "to what extent" | 6 |
| 15_class.md:309 | `**Certainly, for one seeing the source of the world as it truly is` | Vocative `kaccāna` (line 298) is left out here and at line 328, but translated at lines 341 and 403. (old 15.11) | Add "Kaccāna" | 6 |
| 15_class.md:362 | `**But this (person) does not grasp, does not get involved, with engagement and grasping` | Verb order reversed against the Pāli and the table (`upeti` line 355, then `upādiyati` line 357); stray comma before "with". (old 15.8) | "does not get involved with, does not grasp, that engagement…" | 7 |
| 15_class.md:429 | `**"Everything does not exist": this is the second extreme.**` | `sabbaṃ n'atthi` is "nothing exists"; "everything does not exist" reads as "not everything exists". | "'Nothing exists': this is the second extreme." | 6 |
| 5_class.md:629 | `**Monk, don't be careless about meditation` | Recurring terms rendered several ways: `brāhmaṇa` as Brahman / brahmin / priest / holy man and "Monk" here; `dhammavinaya` five ways; `samaṇa` ascetic / recluse / monk; `mettā`; `Venerable sir` / `venerable sir` / `Venerable Sir`; names without diacritics (`Ananda`, `Sariputta`, `Kalamas`). UK and US spelling mixed (`honor`/`honour`, `practiced`, `offence`): a recurring owner-decision topic. (old E18) | A short glossary; spelling: owner decision | 6 |

## D. English typos and grammar

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 2_class.md:53 | `**the state of a superior human being, the attainment of knowing and seeing, suitable for a noble person,**` | Lower-case start and a trailing comma; every other translation line ends without a comma. | Capitalise; end with a full stop | 6 |
| 2_class.md:49 | `worthy of an enlightened` | Truncated gloss. (old 2.8) | "worthy of an enlightened one" | 8 |
| 2_class.md:207 | `samaṇena \| noun \| masc.instr.sg \| with recluse` | Missing article; the same at lines 209 and 210 (`with brahmin`, `with deity`). (old 2.8) | "with a recluse", "with a brahmin", "with a deity" | 7 |
| 2_class.md:211 | `mārena \| noun \| masc.instr.sg \| with Mara` | Missing diacritic; also in the translation (line 213). (old 2.12) | `Māra` | 9 |
| 2_class.md:318 | `**in the discipline of the Kassapa**` | Article before a personal name; also `of the Kassapa` (line 315) and `of the Gotama` (line 309). (old 2.12) | "of Kassapa", "of Gotama" | 8 |
| 2_class.md:287 | `O, brahmin!` | Comma after the vocative particle; also line 289. | "O brahmin!" | 6 |
| 3_class.md:95 | `with born from seclusion` | Ungrammatical gloss. | "born from seclusion" | 7 |
| 3_class.md:351 | `bhāsitassa \| noun \| nt.gen.sg \| statement` | Genitive gloss without "of"; `etassa` on line 350 has it. (old 3.4) | "of the statement" | 6 |
| 3_class.md:43 | `he reaches, he attains.` | Stray full stop inside a gloss cell. (old 3.6) | Remove the full stop | 8 |
| 3_class.md:134 | `is conducive for calmness` | Idiom: "conducive to". (old 3.6) | "conducive to calmness, full awakening and total emancipation" | 7 |
| 3_class.md:278 | `come on!; come now! let's!` | Mixed `!;` and a missing separator before `let's!`. (old 3.6) | "come on; come now; let's" | 6 |
| 4_class.md:72 | `upasaṅkami, \| verb \| aor.3rd.sg` | Punctuation inside a Pāli cell; also `nisīdi.` (line 74). (old 4.6) | Strip | 8 |
| 4_class.md:83 | `rāhulo \| noun \| masc.nom.sg \| Rahula` | Missing diacritic; also line 88; `Angulimāla` (lines 312, 318) lacks `ṅ`. (old 4.15) | `Rāhula`, `Aṅgulimāla` | 9 |
| 4_class.md:314 | `buddhaṃ \| noun \| masc.acc.sg \| The Buddha` | Capital `The` inside a gloss. (old 4.15) | "the Buddha" | 7 |
| 4_class.md:209 | `**O, Builder of a house, you are seen.**` | Comma after "O" and a capital B mid-sentence. (old 4.15) | "O house-builder, you are seen." | 7 |
| 4_class.md:49 | `taṇḍulā'ti \| noun \| masc.nom.pl \| dehusked rice"` | Stray closing quote in the gloss. (old 4.15) | "dehusked rice" | 9 |
| 4_class.md:324 | `ariyassa \| adj \| masc.gen.sg \| of noble` | Truncated gloss; `samādhissa` (line 325) has no "of". (old 3.4) | "of the noble"; "of stillness, composure" | 6 |
| 5_class.md:9 | `tumhākaṃ, \| pron \| 2nd.gen.pl` | Comma carried into the Pāli cell. (old 5.3) | `tumhākaṃ` | 8 |
| 5_class.md:95 | `sāriputtena \| noun \| masc.instr.sg \| with Sariputta` | Missing diacritic; also line 99, and `Brahma` at lines 578 and 582 (`Sāriputta` at line 433). (old 6.18) | `Sāriputta`, `Brahmā` | 9 |
| 5_class.md:190 | `**After my passing away, the Doctrine and Discipline taught by me to you, will become a teacher for you.**` | Comma between subject and verb. (old 6.19) | Remove the comma | 7 |
| 5_class.md:320 | `in reference to us; on us; for us; \|` | Trailing semicolon in the gloss. (old 6.19) | Remove | 7 |
| 5_class.md:287 | `"alaṃ, gāmaṇi. mā maṃ etaṃ pucchi` | Opening quotation mark never closed. (old 5.4) | Remove `"` or close it | 8 |
| 6_class.md:45 | `ānandassa \| noun \| masc.dat.sg \| ānanda` | Lower-case name in the English column and no dative sense; `this[thought]` (line 46) lacks a space; `Ananda` (line 48) lacks the diacritic and the full stop. (old 6.17) | "to Ānanda"; "this [thought]"; "…Venerable Ānanda." | 9 |
| 6_class.md:155 | `lit: one having eyes quality` | Unidiomatic; also `lit. breathing being` (line 87) for a plural. (old 6.16) | "lit. possessing eyes"; "lit. breathing beings" | 6 |
| 6_class.md:380 | `are conducive for the non-decline` | Idiom "conducive to"; also the gloss `are conducive for` (line 378). Line 447 of class 5 has "conducive to". (old 6.19) | "conducive to" | 7 |
| 6_class.md:322 | `**The intelligent man [who is] a giver of happiness, acquires happiness.**` | Comma between subject and verb. (old 6.19) | Remove the comma | 7 |
| 7_class.md:32 | `mallā, \| noun \| masc.nom.pl` | Comma in the Pāli cell. (old 7.6) | `mallā` | 7 |
| 7_class.md:35 | `was extinguished""` | Doubled stray quote in the gloss. (old 7.21) | "was extinguished" | 9 |
| 7_class.md:34 | `kusinārāyaṃ \| noun \| fem.loc.sg \| in Kusinara` | Names without diacritics: `Kusinara` (also line 37), `Vesali` (lines 45, 51), `Ananda` (lines 216, 225). (old 7.22) | `Kusinārā`, `Vesālī`, `Ānanda` | 8 |
| 7_class.md:115 | `**whichever monk should bathe sooner than a fortnight, that is an offence requiring confession**` | Lower-case start and no full stop; line 37 also lacks the full stop. (old 7.21) | Capitalise; add the full stop | 7 |
| 7_class.md:374 | `[dat or purpse]` | Typos for "dat of purpose" (the form used elsewhere, e.g. line 444). (old 7.21) | `[dat of purpose]` | 9 |
| 7_class.md:454 | `udapānena \| noun \| masc.instr.sg \| with well` | Missing article. (old 7.21) | "with a well" | 8 |
| 7_class.md:321 | `"may I be of such form in the future, may I be having such feeling in the future.**` | Opening quote never closed. (old 7.21) | Close the quote | 8 |
| 8_class.md:48 | `mahāmoggallāno \| noun \| masc.nom.sg \| The Great Mogallana` | Misspelt and without diacritics (line 84 of class 7 has "Moggallāna"); also line 59; `Ananda` at lines 79 and 162. (old 7.22) | "Mahāmoggallāna"; "Ānanda" | 8 |
| 8_class.md:112 | `it remained, it stayed.` | Full stop inside a gloss cell. (old 8.16) | Remove | 7 |
| 8_class.md:114 | `**Senior nun grabbed a bowl and threw it into the sky.` | Missing article; the same at line 304 (`of man's intention to a woman`). (old 8.16) | "The senior nun…"; "a man's intention … a woman's intention" | 7 |
| 8_class.md:363 | `having done[something]` | Missing space; `&` in a gloss at line 138; missing commas in the list at line 470 (`not a female demon not a female ghost`). (old 8.16) | "having done [something]"; "and"; add commas | 7 |
| 8_class.md:277 | `bārāṇasiyaṃ \| noun \| fem.loc.sg \| in Varanasi` | Modern spelling; the course writes Pāli names with diacritics elsewhere (`Isipatana`, `Ānanda`). | "in Bārāṇasī" | 5 |
| 8_class.md:359 | `hotī"ti \| verb \| pr.3rd.sg \| there is` | The sentence (line 348) has a closing `"` with no opening one; a double quote inside a table word; the sandhi vowel is long here but short in `hoti"ti` at 15_class.md line 270. (old 8.2) (old F10) | Open the quote in the sentence; one treatment (`hotī'ti`) in both classes | 7 |
| 8_class.md:468 | `mahattarī \| adj \| fem.nom.sg \| older than` | Stray "than": the comparative stands alone here ("[one] older", line 470). (old 8.15) | "older" | 5 |
| 8_class.md:538 | `non-disappearance ,` | Space before a comma. (old A13) | Remove the space | 8 |
| 9_class.md:11 | `brāhmaṇa \| noun \| masc.voc.sg \| Brahman` | "Brahman" here and in the translation (line 15), "brahmin" at line 447. (old 9.23) | "brahmin" | 7 |
| 9_class.md:30 | `sāriputtassa \| noun \| masc.gen.sg \| of the Son of Sari` | Etymological gloss for a name; `Kalamas` (line 116) lacks the diacritic; `gotama` (line 178) is lower case; `Sāvatthi` (lines 138, 195) for the stem `Sāvatthī`. (old 9.22) | "of Sāriputta"; "Kālāmas"; "Gotama"; "Sāvatthī" | 7 |
| 9_class.md:95 | `pañha-vyākaraṇāni .` | Space before the full stop; `vyākaraṇāni.` (line 103) keeps the full stop in the Pāli cell. (old A13) | Remove the space and the cell full stop | 8 |
| 9_class.md:244 | `sukhāya \| noun \| nt.dat.sg \| for the comfort of` | Stray "of" in the gloss. (old 9.23) | "for the comfort" | 7 |
| 9_class.md:417 | `āgato \| pp \| masc.nom.sg \| have come` | Agreement: "has come"; also "it will be" for "he will be" (line 421), `vaḍḍhati … increase` (line 581) and `actions; deed` (line 544). (old 9.20) | "has come"; "he will be"; "increases"; "deeds" | 7 |
| 9_class.md:542 | `any states o existence` | Typo. (old 9.21) | "of" | 10 |
| 10_class.md:21 | `jānāmī'ti \| verb \| pr.1st.sg \| I know"` | Closing quote with no opening quote; also lines 40, 197 (`I breathe in"`), 203. Lines 11 and 30 have both quotes. | `"I know"` | 7 |
| 10_class.md:142 | `asamanupassanto \| prp \| masc.nom.sg \| not seeing perceiving` | Two glosses with no separator. Other broken English in the class: "When one investigating…" (line 389) and "When one seeing himself…" (line 555) have no verb after "when"; "How many staying awake", "By how many one grasps" (line 722); `pāragāmino` "cross over" (line 733) and `anudhāvati` "run along" (line 740) are bare verbs for an adjective and a 3rd sg verb; "wise would reprove" (line 356) lacks "the". (old 10.19) | "not seeing; not perceiving"; fix the others | 7 |
| 10_class.md:551 | `samanupassato \| prp \| masc.gen.sg<br>(gen abs) (or)<br>masc.dat.sg \| when sees; perceives (or)<br>for one seeing` | "when sees" has no subject. | "when he sees; perceives" | 6 |
| 11_class.md:15 | `**Bhikkhus you should dwell with yourselves as an island,` | "Bhikkhus" here, "Monks" everywhere else; no comma after it. Other English slips in the class: "imagine if…" starts lower-case (line 119); "pliable workable" lacks a comma (line 477); "conducive for" (line 319); "whoever acting according to" (line 665); `[lit:made a vehicle]` lacks a space (line 258); a closing `"` with no opening one in two gloss cells (`I will remain"` line 609, `doctrine of fools"` line 620). (old 11.23) | "Monks, you should…"; fix the others | 8 |
| 11_class.md:141 | `ānanda \| noun \| masc.voc.sg \| ānanda` | Lower-case name in the English column; the translation (line 151) has "Ananda" without the macron and "[who] recently come". (old 11.22) | "Ānanda"; "[who have] recently come" | 9 |
| 11_class.md:487 | `'khīṇā jāti vusitaṃ brahmacariyaṃ` | An opening quote that is never closed, carried into the table cell `'khīṇā` (line 504). (old 11.2) | Remove it, or close it | 7 |
| 11_class.md:577 | `diṭṭhiṭṭhānaṃ, — so loko so attā` | Comma plus dash, twice in the sentence; the closing `'ti` of `ṭhassāmī'ti` has no opening quote. (old 11.3) | Tidy | 6 |
| 12_class.md:46 | `there could be hen's eggs` | The supplied words are not in brackets. Also "I will clarify" (line 536) for the present `āvikaromi`, and "knowledge and vision were not" (line 281) for a singular. (old 12.17) | "[there were] a hen's eggs"; "I clarify"; "was not" | 5 |
| 12_class.md:222 | `**Some monks and brahmins who speaking thus, holding such view…**` | Ungrammatical. Also "…noble truths, which four?" (line 135) is a comma splice, and `aspects….` (line 281) has an ellipsis plus a full stop. (old 12.18) | "…who speak thus and hold such a view…" | 8 |
| 13_class.md:69 | `ovadati \| verb \| pr.3rd.sg \| advises, admonish` | Agreement. Also "that; that" (line 300), "who lies" in a plural row (line 329), "make subside" (line 505), "miniscule" (lines 507, 516), "; What indeed" (line 535). (old 13.24) | "admonishes"; "that"; "who lie"; "makes subside"; "minuscule"; ". What indeed" | 8 |
| 13_class.md:129 | `nīyati \| verb.pass \| pr.3rd.sg \| is lead` | The past participle is "led"; also the translation (line 131). (old 13.23) | "is led" | 10 |
| 13_class.md:141 | `na parimuccati jātiyā … , na parimuccati` | A space before the comma. (old A13) | Remove the space | 8 |
| 13_class.md:582 | `yato tvaṃ, bāhiya, na tena tato tvaṃ, bāhiya, na tattha` | Comma missing after the second `na tena` (the parallel has one); `"ti` at the end has no opening quote. (old 13.6) | Add the comma | 6 |
| 14_class.md:25 | `pāyāsi \| noun \| masc.nom.sg \| Payasi` | Names without diacritics (`Payasi`; `Bandhuma`, `Vipassi` at line 66); lower-case start `"monk, this is your bowl.` (line 777); the verse translation (line 658) opens a quote it never closes; `understood.` with a full stop inside a cell (line 179); `how!?` (line 174); "not approved of nor rejected" (line 671). (old 14.29) | Pāyāsi, Bandhumā, Vipassī; "Monk"; close the quote; drop the full stop; "how?"; "neither approved of nor rejected" | 7 |
| 14_class.md:32 | `And then, having had summoned a young brahmin Uttara, Payasi, the young nobleman, said this.` | Ungrammatical ("having had summoned"); the name order hides the subject. (old 14.21) | "And then Pāyāsi the young nobleman, having had the young brahmin Uttara summoned, said this." | 8 |
| 14_class.md:98 | `vicāreti \| verb.caus \| pr.3rd.sg \| investigate; examine` | Bare verbs (no "he"); "being cause to see together" (line 372); singular "fits with", "is seen together with" on 3rd pl verbs (lines 375, 378); "lit: causing to be heard along" on a passive (line 310); "lit. causes to know" on a future (line 356); "should cause pour" (line 296); "who restrained" (line 795); "with no patron; owner" (line 728). (old 14.27) | "investigates; examines"; "being caused…"; "fit with"; "are seen…"; "being caused to be heard"; "will cause to know"; "should cause to pour"; "who is restrained"; "with no patron or owner" | 7 |
| 15_class.md:43 | `padhāna- \| noun \| nt \| exertion, energetic effort, striving,` | Trailing comma in a gloss; full stops in gloss cells (`understood.` line 72, `at the right moment.` line 201); `Thus- Gone` (line 442); `duality–on` (line 290); `"right view?"` with the question mark inside the quote (line 272). (old 15.14) | Fix the punctuation | 8 |
| 3_class.md:318 | `gahapati, pucchasi — "... diṭṭhiyo loke uppajjanti…` | The quote is never closed; `...` and `…` in one line. Not placed in the class 3 slice. (old 3.2) | Close the quote; `…` | 8 |
| 6_class.md:175 | `samaye corā balavanto honti..` | Two dots where an ellipsis is meant (the folder has 56 `…`). The old row also cited 5:413, 10:636 and 11:341: those have three ASCII dots (`...`, 10 in the folder by mech count), not two. (old A14) | `…` | 8 |

## E. Markdown defects that affect rendering

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 2_class.md:298 | `**[Good are] friends in [arisen] need <br>[Good are] friends when need [arises]**` | Bold spans a `<br>`; two alternative translations in one bold line. | Bold each line separately, or keep one translation | 6 |
| 3_class.md:354 | `**It would be good if the meaning of this statement may become evident to Venerable Sāriputta. (so that he could explain it to us)<br>fig: It would be good if Ven. Sāriputta would explain the meaning of this statement.**` | Bold spans a `<br>`; a bracketed clause stands after the full stop. (old 3.6) | Bold each line; put the bracket before the full stop | 7 |
| 4_class.md:403 | `**Practice for restraint of the body (faculty), guard the body (faculty), <br>arouse restraint in regard to the body (faculty).**` | Bold spans a `<br>`. | Bold each line, or drop the `<br>` | 7 |
| 8_class.md:252 | `**Having shaved hair and beard, and having clothed myself in brown robes, let me go forth from the household life to homelessness. <br>[What if I shave hair and beard, clothe myself in brown robes and go forth…?]**` | Bold spans a `<br>`. | Bold each line | 7 |
| 15_class.md:25 | `katame pañca? \| \| \| \|` | The sentence is placed as the first table row with four empty cells; also `katamehi tīhi?` (line 112), `katamehi pañcahi?` (line 191). (old A8) | Move the sentence above the table | 7 |
| 6_class.md:50 | `**This is a common Pāli idiom.**` | Notes and sub-headings in bold exactly like a sentence translation: also `**passive verbs:**` (13_class.md line 74), `**Potential Participles**` (14_class.md line 123), `**(or)**` (14_class.md line 553), `**Translation Assignment**` (15_class.md line 3). (old A17) | Plain text or a heading | 6 |

## F. Convention drift

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 1_class.md:11 | `sammā - \| ind \| adv` | Space before the hyphen. The sentence (line 3) writes `sammā-sambuddhassa`; class 2 (2_class.md line 88) keeps the whole compound `sammāsambuddho`. (old 1.1) | `sammā-`; one treatment of the compound across classes | 7 |
| 2_class.md:315 | `kassapassa \| proper noun` | The only `proper noun` POS; other names are `noun` (`gotamo`, lines 116, 304). (old 2.5) | `noun` | 8 |
| 2_class.md:127 | `**for dispassion, for cessation**` | Phrase translations start lower case here and at lines 136, 154, 192, 201, 213, 253, but capitalised at lines 109, 118, 164, 234. | One style | 4 |
| 3_class.md:1 | `# Class 3 Key to Exercises` | No blank line between the heading and item 1 (line 2); every other key file has one. (old A3) | Add a blank line | 6 |
| 3_class.md:84 | `young gentleman, Brahman` | The translation (line 87) writes `(brahmin)`; the course elsewhere writes "brahmin". (old 3.6) | "young brahmin" | 7 |
| 4_class.md:118 | `amha- \| verb \| pr.1st.pl \| we are` | The hyphen marks compound stems elsewhere; here it is on a finite verb shortened in sandhi (`amhā'ti`, line 113). (old 4.3) | `amha` | 6 |
| 5_class.md:481 | `añña'd'atthu \| ind \| adv` | Two elision marks inside one indeclinable (`aññadatthu`), also in the sentence (line 470). | `aññadatthu` (DPD headword, `añña + [d] + atthu`), unless the marks are a deliberate sandhi notation: owner decision | 5 |
| 6_class.md:203 | `thero \| adj \| masc.nom.sg \| elderly; senior` | The same word is `noun` at lines 251 and 267 (`therā`, `there`). | One POS | 5 |
| 6_class.md:428 | `tam \| pron \| masc.acc.sg \| that` | Plain `m` on a free-standing word; also the sentence (line 421). (old F3) | `taṃ` | 9 |
| 7_class.md:70 | `kinti \| ind \| pron+ind \| how then` | The sentence (line 66) writes `kin'ti`; the same word is tagged `interr` at line 417. (old 7.2) | `kin'ti`; one tag | 8 |
| 7_class.md:125 | `vā \| ind \| - \| or` | The Grammar cell of a particle is `-` here (also lines 109, 127, 129), `conj` at line 299, and empty at lines 184, 399, 401, 438. | `conj` (or the class's usual label) throughout | 7 |
| 7_class.md:170 | `yaṃnūn'āhaṃ \| idiom \| ind+pron.1st.nom.sg` | The same idiom is `yan'nūn'āhaṃ` with `pron+ind+pron.1st.nom.sg` at 8_class.md lines 238, 242 (and in class 13, line 44). (old 7.5) | One spelling and one analysis | 8 |
| 7_class.md:295 | `ce \| ind \| ind \| if` | `ce` is `ind` here and at line 456 (and 8_class.md line 545), `cond` at line 386. (old 7.13) | `cond` | 7 |
| 7_class.md:370 | `yāva'd'eva \| ind \| ind+adv` | Two elision marks inside one indeclinable (`yāvadeva`); also the sentence (line 366). | `yāvadeva` (DPD: `yāva + [d] + eva`), unless the marks are a deliberate sandhi notation: owner decision | 5 |
| 8_class.md:159 | `etad- \| pron \| nt.acc.sg \| this` | A hyphen marks a compound stem elsewhere; here it marks sandhi with `avoca` (sentence `etadavoca`, line 142). Class 6 writes `etad` (6_class.md line 146). | `etad` | 5 |
| 9_class.md:87 | `samanupassituṃ \| ind \| inf` | Infinitives are `verb \| inf` (18 rows), but `ind \| inf` here and at lines 117 and 708. (old E10) | `verb` | 8 |
| 9_class.md:95 | `pañha-vyākaraṇāni` | The exercise (bpc_ex/9_class.md line 73) writes `pañhabyākaraṇāni`. (old B9) | One spelling (`pañhabyākaraṇāni`) | 6 |
| 9_class.md:146 | `yaṃ nūna \| pron+ind \| interr \| what if, let's` | A third spelling and analysis of the idiom: `yaṃnūn'āhaṃ` (7_class.md line 170) and `yan'nūn'āhaṃ` (8_class.md line 242). | One spelling and one analysis | 6 |
| 10_class.md:130 | `ca \| ind \| \| and, but` | Empty Grammar cell; `ca` is `conj` elsewhere in the class (lines 149, 347). Also `yāvatā-` (line 676). | `conj` | 6 |
| 10_class.md:181 | `atthaṅ'gate \| pp \| masc.loc.sg<br>(loc abs)` | An elision mark inside the compound `atthaṅgata` where nothing is elided; same in the sentence (line 173). | `atthaṅgate` (DPD headword atthaṅgata, `atthaṃ + gata`), unless the mark is a deliberate sandhi notation: owner decision | 4 |
| 10_class.md:203 | `passasāmī'ti \| verb \| pr.1st.sg + quote` | `+ quote` in the Grammar column here, not in the twin row at line 197; at lines 239 and 243 it sits in the English column (`I will breathe in + quote`). | One place, or drop it | 6 |
| 10_class.md:212 | `seyyathāpi \| ind \| pron+adv+ind \| just like` | A construction in the Grammar column; line 90 has `seyyathāpi \| ind \| -`. | `-` | 5 |
| 10_class.md:666 | `yāvat'āssa vigatamiddho` | The mark implies `yāvat` + `āssa`; the table splits `yāvatā-` + `assa` (lines 676, 677). (old 10.3) | Match the table (`yāvatā'ssa`) | 5 |
| 10_class.md:678 | `(or) \| pron \| masc.dat.sg \| for him` | `(or)` stands in the Pāli column as if it were a word; also line 680. Line 377 gives alternatives inside the cell. (old A10) | Use the in-cell `(or)` pattern of line 377 | 7 |
| 11_class.md:48 | `seyyathāpi \| ind \| \| just like, as` | Empty Grammar cell; the same word has `pron+adv+ind` at lines 112 and 241. `vā` has `disj` (lines 328, 330), `conj` (line 53) and an empty cell (lines 185, 187). | One value per word | 5 |
| 11_class.md:104 | `sampajāna-kārī \| adj \| masc.nom.sg` | Hyphen in the table, none in the sentence (`sampajānakārī`, line 96); also `sammāsaṅkappa-gocarā` (line 543) against the sentence's `sammāsaṅkappagocarā`. | Match the sentence | 6 |
| 11_class.md:126 | `abyatto \| adj \| masc.nom.sg \| untrained \| √añj･8 \*aya (distinguish)` | Sign `*aya` here; `byattaṃ` has `√añj･8 *e` (10_class.md line 602). This line follows DPD (abyatta, √añj \*aya); `byatta` was not looked up. | DPD lookup (byatta) | 3 |
| 11_class.md:203 | `aniccato \| ind \| adv \| as impermanent` | The same "-to = as X" form is `ind \| adv` here and at lines 205–211, 363–373, but `noun \| masc.abl.sg` for `paṭilābhato` (line 422) and `accayato` (line 520). (old 11.14) | One tag | 6 |
| 11_class.md:237 | `seyyathā'pi suddhaṃ vatthaṃ apagataṃ kāḷakā` | Sentence `seyyathā'pi`, table `seyyathāpi` (line 241); also sentence `vigat'ūpakkilese` (line 461) vs table `vigatūpakkilese` (line 471). (old 11.1) | Match | 8 |
| 11_class.md:274 | `[AN4.61](https://s.dhamma.gift/an/an4/index.html#an4.61)(simpl)` | No space before `(simpl)`; every other `(simpl)` in the class has one (lines 249, 301, 444). | `… (simpl)` | 5 |
| 11_class.md:681 | `maṅgalam \| noun \| nt.nom.sg \| blessing` | The table keeps the sandhi `-m` of `maṅgalam'uttamaṃ`; the same phrase in class 10 has `maṅgalaṃ` (10_class.md line 661). | `maṅgalaṃ` | 5 |
| 12_class.md:12 | `api \| ind \| \| just only` | `ekam'pi` is split into `ekaṃ` + `api` (lines 11–12), while `dve'pi`, `tisso'pi` … `jātisatasahassam'pi` (lines 14–27) keep the `'pi` in one row. | One way | 5 |
| 12_class.md:48 | `evam'eva kho, bhikkhave, ayaṃ dhammavinayo` | Sentence `evam'eva`, table `evameva kho` (line 62). (old 11.1) | Match | 8 |
| 12_class.md:86 | `pañca-mattehi \| adj \| nt.instr.pl \| with five in number; five measures` | Hyphens in the table that the sentence (line 71) does not have: also `bhikkhu-satehi` (line 87), `an-uppanno` (line 111), `yathā-idaṃ`, `paṭigha-nimittaṃ` (lines 119, 120; sentence `yathayidaṃ`, `paṭighanimittaṃ`), `ariya-saccāni.` (line 131). | Match the sentence | 6 |
| 12_class.md:369 | `samanta'pāsādiko \| adj \| masc.nom.sg` | An elision mark where nothing is elided; also in the sentence (line 358). (old 12.4) | `samantapāsādiko` (DPD headword samantapāsādika, `samanta + pāsādika`), unless the mark is a deliberate compound notation: owner decision | 5 |
| 12_class.md:454 | `tīṇi \| card \| nt.acc.pl \| three (3)` | Digits in brackets in this item only (lines 454–464). (old 12.19) | Remove them | 5 |
| 12_class.md:506 | `seyyath'idaṃ \| ind \| pron+adv+pron \| namely; that is` | `seyyath'idaṃ` here and in the sentence (line 497), `seyyathidaṃ` in item 1 (lines 3, 10). | One spelling | 5 |
| 13_class.md:297 | `samanuyuñjiyamāno \| prp. pass \| masc.nom.sg \| being cross-questioned by \| √yuj･2 ṃa + iya (yoke, join)` | The passive sign is written four ways in the class: `ṃa + iya` here, `iya` (lines 183, 298, 299), `īya` (lines 280, 281), `ya` (line 82 and most others). | One notation | 5 |
| 13_class.md:351 | `dissanti \| verb \| pr.pass.3rd.pl \| are seen` | The same word in the same sentence is `verb.pass \| pr.3rd.pl` (line 343). (old 13.11) | `verb.pass \| pr.3rd.pl` | 9 |
| 14_class.md:30 | `etadavoca \| verb \| aor.3rd.sg \| he said this` | The sentence (line 20) has `etad'avoca`; likewise the table has `tasmā't'iha` (line 129) against `tasmātiha` in the sentence (line 125). (old 14.3) | Match | 5 |
| 14_class.md:62 | `tayo \| adj \| masc.acc.pl \| three` | Every other numeral in the key is `card` (`dve`, `tīṇi`, lines 76-78). (old 14.10) | `card` | 7 |
| 14_class.md:91 | `ca- \| ind \| conj \| and, but` | Trailing hyphen on sandhi-split words that are not compound members: also `evaṃ-` (line 248), `cattāro-` (line 262). (old 14.5) | Drop the hyphen | 6 |
| 14_class.md:294 | `√sic･2 ṃa (sprinkle, pour)+ ṃa \> siñca+eyya` | Free-form derivation inside the Root cell (also line 296); no other Root cell in the folder does this. (old D19) | `√sic･2 ṃa (sprinkle, pour)` | 7 |
| 14_class.md:296 | `siñcāpeyya \| verb \| opt.caus.3rd.sg` | "caus" in the Grammar column, as `pabbājentī"ti \| verb \| pr.caus.3rd.pl` (line 537), while `pabbājenti` three rows earlier (line 534) is `verb. caus \| pr.3rd.pl`. (old 14.13) | `verb.caus` | 8 |
| 14_class.md:302 | `sampajānamusāvādo assa hoti` | The rule reads `sampajānamusāvādassa hoti`; the Pāli line prints the commentarial resolution `-vādo assa` without saying so. Same silent resolution: `vā assa` (line 503), `evaṃ assa` (line 527), `rāgaṃ ca dosaṃ ca, avijjaṃ ca` (line 633), `ṭhānaṃ etaṃ` (line 342), `idha ahaṃ` (line 682); the file keeps `kathañ'ca` (line 170) and `evañ'ca` (line 244). (old 14.2) | One convention, or mark the resolution | 5 |
| 14_class.md:372 | `√dis･1 \*e iya (see)` | Compound signs are written with `+` (`√bhū･1 \*e + iya` line 267, `√tar･1 \*e + iya` line 370, `√sar･1 \*e + iya` line 476, `√ṭhā･1 \*āpe + iya` line 835, `√vis･1 \*e + iya` line 837; also 13_class.md line 297) and once without. (old D18) | One notation | 8 |
| 14_class.md:378 | `sandissanti \| verb. pass \| pr.3rd.pl (+loc)` | Root `√dis･1 iya`: passive sign `iya` where the key's convention is `ya` (`√vac･1 ya`, line 792); also `√vatt･1 iya` (line 269), `√hā･1 īya` (line 629). Folder count in the cross slice. (old D17) | `√dis･1 ya` | 6 |
| 14_class.md:508 | `pana \| ind \| ind \| but; and so` | The same word in the same rule formula is `ind \| conj` at line 307; `ce` is `ind \| cond` at lines 326, 368, 569 but has an empty Grammar cell at line 141. | One Grammar value each | 6 |
| 14_class.md:537 | `pabbājentī"ti` | A double quote as the quotation mark inside a word, also in the sentence (line 527); elsewhere an apostrophe (`paññāpessatī'ti`, line 356). verify_key cannot match it (NOT-FOUND). (old 14.4) | `pabbājentī'ti` | 8 |
| 14_class.md:678 | `sandassetabbāni \| ptp caus pass \| nt.nom.pl` | The parallel `otāretabbāni` two rows up (line 676) is `ptp.caus`; a potential participle is passive by itself, and no other `ptp` row adds `pass`. | `ptp.caus` | 7 |
| 14_class.md:835 | `vuṭṭhāpiyamānaṃ \| prp \| masc.acc.sg [+instr]` | Causative passive by its own Root cell (`\*āpe + iya`; also `saṃvesiyamānaṃ`, line 837) without the label that `bhāviyamānā` (line 267) and `otāriyamānāni` (line 370) carry; `ārādhayiṃsu` (line 691, `\*aya`) is plain `verb` while `vivattayi` (line 804) is `verb.caus`. (old 14.14) | `prp.caus.pass`; `verb.caus` | 6 |
| 15_class.md:183 | `ananuvajjā \| adj, <br>(\<ptp)` | One POS written three ways in one item: `adj(\<ptp)` (line 181), `adj (\<ptp)` (line 241), `adj, <br>(\<ptp)` (here and line 243). | `adj (\<ptp)` | 6 |
| 15_class.md:218 | `metta- \| adj \| masc (in comp)` | A gender on a compound-member adjective whose head (`cittena`) is nt; `attha-` (line 213) has `masc. (in comp)` with a full stop. (old 15.6) | `in comp` | 6 |
| 15_class.md:253 | `"dvayanissito kho ayaṃ, kaccāna, loko yebhuyyena — atthitaṃ ca eva n'atthitaṃ ca.` | SN12.15 has `khvāyaṃ`, `atthitañceva natthitañca`, `tañcāyaṃ`, `dukkhameva`, `ñāṇamevassa`; item 4 prints every sandhi resolved without saying so, while item 1 shows its resolutions in brackets (line 9). | verify; mark the resolutions as in item 1 | 4 |
| 11_class.md:511 | `saṁvarāya` | `ṁ` 6 times (mech count: 11_class 2, 12_class 4; also 11:523, 12:437, 12:448, 12:462, 12:466) against `ṃ` everywhere else. (old A6) | `ṃ` | 9 |
| 3_class.md:57 | `so ‘idaṃ dukkhan'ti yathābhūtaṃ pajānāti` | Curly opening `‘` (25 in the folder, 10 in class 15) closed by a straight `'`, or used as an elision mark; no `’` exists in the folder. 14_class.md line 735 has a doubled `‘‘`. (old A7) | Straight `'` throughout | 8 |
| 6_class.md:292 | `visuddhiyā \| noun \| fem.dat.sg<br>fem.gen.sg` | Raw `<br>` inside table cells (Pāli, POS, Grammar and English columns); 614 `<br>` in the folder, most of them between citation and sentence. A recurring owner-decision topic. (old A11) | owner decision | 5 |
| 9_class.md:68 | `samudayāya. \| noun \| masc.dat.sg` | Sentence punctuation kept inside the Pāli cell (classes 9–12, and class 15 throughout, e.g. `hoti,` at 15_class.md line 45); the other classes strip it. (old A12) | Strip | 7 |
| 11_class.md:274 | `[AN4.61](https://s.dhamma.gift/an/an4/index.html#an4.61)(simpl) <br>` | The gap between citation, `(simpl)` and `<br>` is written five ways: `) <br>` ×298, `)<br>` ×71, `) (simpl) <br>` ×52, `) (simpl)<br>` ×40, `)(simpl) <br>` ×1 (this line). (old A15) | One form | 6 |
| 10_class.md:23 | `**Or knowing, he said, "I don't know"**` | Translations of a split sentence: some start upper-case and end without a full stop, others the reverse, even inside one item (10_class.md line 32 "or, not seeing"). (old A16) | One rule for split sentences | 4 |
| 11_class.md:530 | `[DHP012](https://s.dhamma.gift/kn/dhp/index.html#dhp1)` | Zero-padded Dhp labels (`DHP012`, `DHP026`, `DHP085`–`DHP088`: 6) beside unpadded ones (`DHP76`, `DHP130` and 13 more). (old C13) | One form | 6 |
| 6_class.md:52 | `[VIN1.2.12](https://s.dhamma.gift/vin/tv/pli-tv-bu-vb-ss/index.html#pli-tv-bu-vb-ss12)` | Two label systems for the Vinaya: numeric `VIN1.2.12`, `VIN1.1.4`, `VIN2.5.1.2`, `VIN4.1.14` (7) against `VIN PAT SA 12`, `VIN PAT PC 20` (41 linked, 5 unlinked). (old C14) | One form | 6 |
| 5_class.md:68 | `madāya \| noun \| masc.dat.sg \| for intoxication \| √mad･3 ya (be mad, intoxicated)` | Root glosses differ from current DPD wording in about 65 rows (`√chid` as `(cut, steal)` and `(cut)`; `(breath, blow)`; `(destroy, exhaust)`), mostly DPD rewording since the key was written. (old D22) | DPD lookup; refresh the glosses in one pass | 6 |
| 5_class.md:81 | `ānanda \| noun \| masc.voc.sg \| O Ānanda! (lit. joyful)` | The same word has a root in one row and none in another: `ānanda` (here vs 6_class.md line 45), `medhāvī`, `saṅgha`, `atthi`, `khamo` (15:44 vs 15:36), `samannāgatā` (15:235 vs 15:104), `sādhukaṃ` (14:419 vs 14:668), `apaññattaṃ`/`paññāpessanti` (14:434, 14:436 vs 14:437). (old D25) | Fill or leave empty consistently | 6 |
| 4_class.md:185 | `abhinanduṃ \| verb \| aor.3rd.pl \| they were pleased with (+acc)` | Governed case written `(+acc)` ×39, `[+acc]` ×36, bare `+acc` ×4 (e.g. `+loc` at 15_class.md line 381), sometimes after a `<br>`, and here in the English column. Supplied words in translations: `[and]` (2_class.md line 78) against `(and)`, `(about)`, `(for)` (3_class.md line 340, 4_class.md line 282). (old E2) (old 4.16) | One form, in the Grammar column | 7 |
| 10_class.md:275 | `asante \| prp \| masc.loc.sg \| (when) … not present (loc abs)` | Absolute constructions written `(loc abs)` / `(gen abs)` ×37, `[loc abs]` ×14 (e.g. 11_class.md line 466), `(loc.abs)` ×4, `<br>loc abs` ×2; here in the English column. (old E3) | One form, in the Grammar column | 6 |
| 11_class.md:496 | `vimuttam'iti \| pp \| nt.nom.sg \| liberated +endquote` | End of quotation written `+end quote` ×5, `+endquote` ×8, `+ endquote` ×2, `+ end quote` ×2, `+ quote` ×4, or as a separate `iti`/`'ti` row ×21; here in the English column; nothing at 11_class.md lines 609, 620, 13_class.md line 229, 15_class.md line 245. (old E4) | One form | 7 |
| 13_class.md:351 | `dissanti \| verb \| pr.pass.3rd.pl \| are seen` | Passive and causative written in about 15 ways in the POS column (`verb.pass`, `verb. pass`, `prp. pass`, `prp caus pass`, `ptp caus pass` …) or inside Grammar (here; 14_class.md line 537); classes 3–12 tag the same words plain `verb` (`vuccati` 9_class.md line 303 vs 14_class.md line 792; `paripūreti` 3_class.md line 97 vs 14_class.md line 15). (old E5) | One form; decide whether earlier classes get the label | 8 |
| 13_class.md:351 | `√dis･1 ya (see)` | The passive sign after a group-1 root is `ya` in 22 cells, `iya` in 5 and `īya` in 3 (e.g. 14_class.md lines 378, 629); compound signs `+ iya` ×6, `ṃa + iya` ×1, once without `+`. Folder counts for the rows in the class 13 and 14 slices. | `ya` throughout | 6 |
| 11_class.md:630 | `atītā \| adj (pp) \| masc.nom.pl \| past` | Participle used as adjective: `adj (pp)` ×4, `adj [pp]` ×2, `adj<br>[pp]`, `pp [adj]`, `adj (\<ptp)`, `adj(\<ptp)`, `adj, <br>(\<ptp)` ×2, `adj<br>(ptp)`. (old E6) | One form | 6 |
| 10_class.md:710 | `kati \| pron interr \| masc.nom.pl \| how many?` | Interrogative pronoun as `pron interr` ×4, `pron, interr`, `pron.<br>interr`, `pron<br>interr`; plain `pron` for `ko` ×3. (old E7) | `pron`, with `interr` in Grammar | 6 |
| 5_class.md:145 | `bhogī \| adj. \| masc.nom.sg` | Stray POS values: `adj.` (also 13_class.md line 449), `noun (comp)`, `adj, comp`, `proper noun`, `ind<br>(comp)`, `pron+noun [idiom]`, `pron+verb`. (old E8) | Fold into the standard set | 6 |
| 11_class.md:650 | `ca \| ind \| adv \| and` | Grammar cell of particles: `ca` `conj` ×80, empty ×4, `adv` (here), `ind` (15_class.md line 348); `vā`, `kho`, `eva`, `api`, `pana`, `ce`, `hi` likewise; 25 `ind` rows have an empty Grammar cell and 36 have `-`. `seyyathāpi`: `-` (10_class.md line 90), empty (11_class.md line 48), `pron+adv+ind` (11_class.md line 241). (old E9) | One tag per particle | 7 |
| 8_class.md:412 | `āvuso \| ind \| voc.sg or voc.pl \| o friend; brother` | `āvuso` is `ind \| voc.sg` (5:589, 14:348) or `voc.sg or voc.pl`; verify_key flags the `voc.sg` cells IMPOSSIBLE (DPD: `ind`). `bhante` is `noun \| masc.voc.sg` ×14. (old E11) | `ind` with a plain note, or treat both alike | 5 |
| 9_class.md:191 | `atha \| ind \| ind \| after` | Fixed phrases analysed several ways: `atha kho` (five tags; split here into `atha` "after" + `kho` "that"), `evam'eva`, `seyyathāpi`, `kiṃ nu kho`, `yo pana bhikkhu`, `n'eva`, `c'eva` (`sandhi \| ind+ind`, `ind \| ind+ind`, `ind \| ind+emph`). (old E12) | One analysis per phrase | 7 |
| 1_class.md:11 | `sammā - \| ind \| adv \| fully; completely` | Compound members: Grammar `-` ×17 (class 2), empty, bare gender, `masc (in comp)`, full `masc.nom.sg` on a stem; stems written `sammā -` (space before the hyphen, here), `adhicittam-`, `divasaṃ-`, `ca-`. (old E13) | One form | 6 |
| 6_class.md:34 | `sāvaka-saṅgho \| noun \| masc.nom.sg` | Hyphen in the table that the sentence does not have: also 8_class.md line 42, 10_class.md line 119, 13_class.md line 25, 15_class.md line 95 (`yathā-dhammaṃ` vs `yathādhammaṃ` at line 118), and the rows of classes 11–13 listed in their slices. (old E14) | Match the sentence | 6 |
| 11_class.md:258 | `[lit:made a vehicle]` | The literal-meaning note is written `lit:` ×64 and `lit.` ×38 (mech count), in round or square brackets or none, once `Lit:`. (old E15) | One form | 6 |
| 12_class.md:618 | `(The Buddha) taught the sublime teaching` | Supplied words in round brackets (`(The Buddha)`, `(his)`, `(done)`) beside the majority in square brackets (`[your]`). (old E16) | Square brackets | 5 |
| 15_class.md:174 | `with parts, factors; qualities` | Gloss separators: comma and semicolon both used, often in one cell. (old E17) | One separator | 4 |
| 5_class.md:32 | `parisuddho \| pp \| masc.nom.sg \| cleaned, purified` | Same word, different POS: `parisuddho` pp here, adj at 5_class.md line 344; `āyasmato` noun/adj; `sabba` adj/pron; `ekaṃ`/`eko` card/adj; `adassāvī` and `pariyāyena` inside one sentence; `āgatā` adj/pp; `subhāsitā` pp vs `dubbhāsitā` adj (15_class.md lines 177, 180). (old E19) | One POS per word and function | 6 |

## G. Links

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 4_class.md:367 | `2. [DHP183](https://s.dhamma.gift/kn/dhp/index.html#dhp179)<br>nibbindati dukkhe esa maggo visuddhiyā` | `atha nibbindati dukkhe, esa maggo visuddhiyā` is the refrain of Dhp 277–279 (Maggavagga); Dhp 183 is `sabbapāpassa akaraṇaṃ`. Label and anchor are both wrong. (old C17) | `DHP277`, `#dhp273` | 9 |
| 6_class.md:82 | `7. [SNP9](https://s.dhamma.gift/kn/snp/index.html#snp1.9)` | `ye keci pāṇabhūtatthi` is the Mettasutta, Snp 1.8; the exercise (bpc_ex/6_class.md line 79) and the key itself (line 353) cite `SNP8`. (old C5) | `SNP8`, `#snp1.8` | 9 |
| 6_class.md:276 | `21. [DHP277](https://s.dhamma.gift/kn/dhp/index.html#dhp273)` | `sabbe dhammā anattā` is Dhp 279; the exercise (bpc_ex/6_class.md line 286) cites `DHP185`, also wrong. (old C6) | `DHP279` in both, anchor `#dhp273` | 9 |
| 9_class.md:3 | `1. VIN0 <br>āraddhaṃ kho pana me, brāhmaṇa, vīriyaṃ ahosi.` | Truncated label with no link; the same label at 11_class.md line 17, where the exercise has `[VIN1.0](…pli-tv-bu-vb-pj1)`. (old C8) | Use the exercise's labelled link | 9 |
| 11_class.md:17 | `2. VIN0 <br>taṃ bhavantaṃ gotamaṃ` | The key has a truncated label and no link; the exercise (bpc_ex/11_class.md line 16) has `[VIN1.0](…#pli-tv-bu-vb-pj1)`. (old C8) | Use the exercise's label and link | 9 |
| 11_class.md:61 | `[ITI111](https://s.dhamma.gift/kn/iti/index.html)` | The only KN link in the class with no anchor. (old C12) | Add the anchor if the site has one | 5 |
| 13_class.md:373 | `2. APA 3 (simpl) <br>jahanti purimaṃ nāmaṃ` | Unlinked and too vague to locate. (old C9) | Add a precise reference and link if one exists | 7 |
| 14_class.md:125 | `[AN3.83](https://s.dhamma.gift/an/an3/index.html#an3.82)` | The exercise (bpc_ex/14_class.md line 109) cites `AN4.73` for the same item; the label and the anchor also differ by one (folder-wide AN3 pattern, see the cross slice). (old C7) | Check the text; make key and exercise agree | 7 |
| 14_class.md:244 | `[DN16.11](https://s.dhamma.gift/dn/dn16/index.html)` | `evañca kho eso, bhikkhu, pañho pucchitabbo` is from DN11 (Kevaddha), not DN16. (old C16) | `[DN11](https://s.dhamma.gift/dn/dn11/index.html)` | 8 |
| 14_class.md:302 | `18. VIN PAT NID <br>yo pana bhikkhu yāvatatiyaṃ` | Unlinked reference; the other Pātimokkha items in this file are linked. (old C9) | Add the link (shape per kamma/tech.md → Sutta links) | 7 |
| 9_class.md:526 | `[TH251](https://s.dhamma.gift/kn/thag/index.html#thag16.1)` | The label gives the verse number; the anchor always points to the first poem of the nipāta (Raṭṭhapāla is Thag 16.4, Pārāpariya 16.10). Also 9_class.md line 550, 10_class.md line 312, 13_class.md line 477, 2_class.md line 14. (old C11) | Confirm whether the site has finer anchors | 5 |

## H. Data to re-verify (forms, references, counts)

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 1_class.md:3 | `1. namo tassa bhagavato arahato sammā-sambuddhassa` | No source reference. In class 2, 13 phrase items (8–11, 13, 14, 17–19, 21, 24, 27, 30) have none either. (old C10) | owner decision: confirm intended | 5 |
| 2_class.md:68 | `6. VIN PAT NID nidānuddeso<br>` | Reference with no link, unlike every other labelled item in the class. (old C9) | Add the s.dhamma.gift link to the Pātimokkha nidāna if the site has one; verify | 6 |
| 2_class.md:245 | `aparena samayena buddho` | MN39 has the prison simile (`bandhanāgāre baddho assa. so aparena samayena …`): the word there is `baddho` "bound", and the three words are not contiguous. `buddho` "the Awakened One" (line 251) may rest on a misreading. (old C19) | verify against MN39 | 5 |
| 2_class.md:236 | `vinipātaṃ nirayaṃ` | The old audit did not find the phrase in SN12.41 by text search (it found it in SN12.70). Not checked against a text here. (old C19) | verify | 4 |
| 3_class.md:166 | `16. [MN2.4](https://s.dhamma.gift/mn/mn2/index.html)<br>parikkhāraṃ paṭisevāmi` | MN2 has the 3rd person (`… parikkhāraṃ paṭisevati`); the 1st person is the recollection chant. The item is not marked `(simpl)`. (old C19) | verify; mark `(simpl)` if the 1st person is kept | 5 |
| 3_class.md:308 | `29. VIN<br>passasi taṃ āpattiṃ` | `VIN` alone cannot be located and has no link. (old C9) | Give the exact Vinaya reference and link; verify | 7 |
| 4_class.md:200 | `17. [DHP153](https://s.dhamma.gift/kn/dhp/index.html#dhp146) (simpl)<br>gahassa kāraka, diṭṭho asi` | `gahakāraka diṭṭhosi` is verse 154; verse 153 is `anekajātisaṃsāraṃ` (cited correctly at 10_class.md line 744). (old C18) | `DHP154` (anchor unchanged) | 7 |
| 4_class.md:259 | `22. [SN46.53](https://s.dhamma.gift/sn/sn46/index.html#sn46.53) (simpl)<br>bhikkhū paribbājakehi sammodiṃsu` | The old audit found the phrase in SN46.52 and 46.54 by text search, not in 46.53. Not checked against a text here. (old C19) | verify | 3 |
| 5_class.md:49 | `5. UD-a 43 <br>ahaṃ te aparimitaṃ dhanaṃ dassāmi` | A commentary reference with no link (the site has no commentaries). (old C9) | owner decision: keep as plain text, or give a canonical source | 6 |
| 6_class.md:3 | `1. [DN2.9](https://s.dhamma.gift/dn/dn2/index.html) <br>bhagavā bhikkhū āmantesi, bhikkhavo'ti.` | The exercise (bpc_ex/6_class.md line 3) cites the same item as `SN22.59`. (old C1) | verify the source; make both files agree | 8 |
| 6_class.md:28 | `3. [DN11.6](https://s.dhamma.gift/dn/dn11/index.html) <br>esa bhagavato sāvakasaṅgho` | The old audit could not place the saṅgha formula in DN11. Not checked against a text here. (old C15) | verify | 4 |
| 6_class.md:39 | `4. [DN16.7](https://s.dhamma.gift/dn/dn16/index.html) <br>atha kho āyasmato ānandassa etad'ahosi` | The exercise (bpc_ex/6_class.md line 35) has `DN16.17`. (old C2) | Make both agree | 8 |
| 6_class.md:52 | `5. [VIN1.2.12](https://s.dhamma.gift/vin/tv/pli-tv-bu-vb-ss/index.html#pli-tv-bu-vb-ss12)` | The exercise (bpc_ex/6_class.md line 47) cites `VIN PAT SA 12` (Pātimokkha, `pm4`); the key cites the Vibhaṅga in another label style. (old C3) | Make both agree | 8 |
| 6_class.md:68 | `6. [MN152](https://s.dhamma.gift/mn/mn152/index.html) (simpl)` | The exercise (bpc_ex/6_class.md line 64) cites `MN19`. The formula is in both suttas. (old C4) | Make both agree | 7 |
| 6_class.md:199 | `16. [AN10.71](https://s.dhamma.gift/an/an10/index.html#an10.71)<br>thero bhikkhu sabrahmacārīnaṃ piyo ca hoti` | The old audit took the wording for AN5 (`thera` suttas), not AN10.71. Not checked here. (old C15) | verify | 4 |
| 6_class.md:439 | `1. [SNP16](https://s.dhamma.gift/kn/snp/index.html#snp2.4) <br>mātāpitu upaṭṭhānaṃ, puttassa ca dārassa saṅgaho` | The Maṅgalasutta reads `puttadārassa saṅgaho`; the key splits the compound into `puttassa ca dārassa` without a `(simpl)` marker. | Mark `(simpl)`, or keep the compound | 6 |
| 7_class.md:154 | `13. [MN10.16](https://s.dhamma.gift/mn/mn10/index.html)<br>aho vata mayaṃ na maraṇadhammā assāma` | The expanded truths passage with `na maraṇadhammā assāma` is in DN22; in MN10 it is found only in the Burmese edition. (old C15) | verify against the edition the course follows | 4 |
| 7_class.md:188 | `avaṅkatā \| adj \| fem.nom.sg \| not dishonest` | Not in SN12.22 as the old audit read it (`avañjhā bhavissati saphalā saudrayā`); in DPD `avaṅkatā` is a fem. abstract noun "straightness". The item is `(simpl)`. (old 7.7) | `noun \| fem.nom.sg \| straightness; honesty` (DPD: avaṅkatā fem, abstr); verify the text | 6 |
| 8_class.md:101 | `7. DNa2.3 <br>therī pattaṃ gahetvā ākāse khipi.` | A commentary reference with no link. (old C9) | owner decision: keep as plain text | 6 |
| 8_class.md:181 | `11. [VIN PAT PA 1](https://s.dhamma.gift/vin/tv/pli-tv-bu-pm/index.html#pli-tv-bu-pm3) <br>yo pana bhikkhu sikkhaṃ apaccakkhāya` | The rule is shortened (`bhikkhūnaṃ sikkhāsājīvasamāpanno` and `antamaso tiracchānagatāyapi` are left out) with no `(simpl)` marker and no ellipsis. | Add `(simpl)` | 4 |
| 8_class.md:331 | `19. VIN PAT SA <br>ciṇṇamānatto bhikkhu` | `VIN PAT SA` names a whole chapter and has no link. (old C9) | Add the link to `pm4`; verify | 7 |
| 9_class.md:526 | `tasmā hi paññā eva dhanena seyyā, yāya vosānaṃ idha adhigacchati.` | Thag 16.4 / MN82 read `paññāva dhanena seyyo` and `karonti mohā` (pl); the key has `seyyā` and `karoti` (line 545) with no `(simpl)` marker. | verify; mark `(simpl)` if the changes are kept | 4 |
| 9_class.md:585 | `vatthuṃ desanāya` | The Pātimokkha has the compound `vatthudesanāya`; the key splits it without `(simpl)`. (old 9.4) | verify; mark `(simpl)` | 4 |
| 10_class.md:342 | `na ca khuddaṃ samācare kiñci` | The Mettasutta reads `khuddamācare` (= `khuddaṃ ācare`); `samācare` adds a syllable to the pāda. The exercise has the same text; the table tags `samācare` (line 349). (old 10.1) | verify; `khuddaṃ ācare` | 6 |
| 11_class.md:409 | `lok'āmisena paṭisaṃyuttānaṃ paṭilābhaṃ paṭilābhato` | Reworded against MN137 (`lokāmisapaṭisaṃyuttānaṃ … paṭilābhaṃ vā`) without `(simpl)`; line 237 likewise splits DN14's `apagatakāḷakaṃ` into `apagataṃ kāḷakā`. (old 11.6) | verify; add `(simpl)` | 5 |
| 12_class.md:94 | `yena anuppanno byāpādo uppajjati, yathayidaṃ` | AN1.12 has `anuppanno vā byāpādo uppajjati uppanno vā …`; the key shortens it without `(simpl)`. Line 377 likewise drops `pi` and `bhikkhave` from AN10.61 (`pañcapāhaṃ, bhikkhave`); for line 339 see the `caturāsītīnaṃ` row. (old 11.6) | verify; add `(simpl)` | 5 |
| 13_class.md:187 | `ce bhikkhuṃ aññe bhikkhū jāneyyuṃ` | The rule reads `tañce bhikkhuṃ`; enclitic `ce` cannot open a sentence, and the translation still supplies "[that]". Not marked `(simpl)`. (old 13.2) | verify; `tañ'ce bhikkhuṃ` + a `taṃ` row | 6 |
| 13_class.md:210 | `bhiyyo'ti \| ind \| adv+end quote \| more"` | The rule continues `bhiyyo, na ca tassa bhikkhuno…`; the `'ti` and the closing quote are not in it. (old 13.3) | verify; `bhiyyo` | 5 |
| 13_class.md:269 | `[MN10.18](https://s.dhamma.gift/mn/mn10/index.html)` | The expanded truths passage is in DN22; in MN10 only in the Burmese edition. (old C15) | verify | 4 |
| 13_class.md:288 | `evam'pi kho bhikkhu tehi bhikkhūhi` | Abridged without `(simpl)`; line 458 splits the compound `chakkhattuparamaṃ` into `chakkhattuṃ paramaṃ`, also unmarked (items 2, 4, 7 are marked). (old 13.5) | verify; mark `(simpl)` | 5 |
| 13_class.md:449 | `supatiṭṭhitā \| adj. \| fem.nom.sg \| well placed; well established` | Khp 7 in CST reads `suppatiṭṭhitā` (DPD has both lemmas); stray full stop in the POS cell. (old 13.4) | verify; `adj` | 5 |
| 14_class.md:136 | `es'ev'anto paṭigh'ānusayānaṃ,` | MN18 lists `esevanto rāgānusayānaṃ` first, then `esevanto paṭighānusayānaṃ`; the key (and the exercise, bpc_ex/14_class.md line 119) jump to the second item with no `…` or `(simpl)`. | verify; add `…` or `(simpl)` | 5 |
| 14_class.md:406 | `[DN16.21](https://s.dhamma.gift/dn/dn16/index.html)` | Sub-numbers after DN/MN labels (`DN16.21`, also for two other passages at 9_class.md lines 233, 267; `DN23.20`, `DN14.4`, `MN2.2`, `MN2.8`; 47 labels) match no SuttaCentral segment numbering, and the scheme is not stated. (old C20) | State the numbering scheme, or drop the sub-numbers | 5 |
| 4_class.md:13 | `[AN3.66](https://s.dhamma.gift/an/an3/index.html#an3.65)` | AN3 labels run one higher than their anchors: AN3.66→#an3.65 (also 9_class.md line 109), AN3.70→#an3.69, AN3.71→#an3.70, AN3.79→#an3.78, AN3.156→#an3.155, AN3.83→#an3.82 (14_class.md line 125). The labels follow another edition's numbering; the anchors follow SuttaCentral. | Align the labels with the anchors, or state the numbering | 6 |

## I. Further details on the material under review

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 11_class.md:527 | `## Class 11 Extra` | The line before this heading holds a single space (mech_checks trailing space). (old A4) | Empty line | 9 |
| 15_class.md:9 | `**"pañcime (pañca + ime), bhikkhave, caṅkame ānisaṃsā.` | The source paragraph is bold with `(a + b)` sandhi notes in items 1–2 (also line 95), plain with none in items 3–4 (lines 166, 253-255); item 4 (line 249) lacks the `(paragraph N)` note. (old 15.2) | One layout for the four items | 6 |
| 15_class.md:1 | `# Class 15 Key to Exercises` | Classes 1 and 15 have no `## Class N Extra` section; classes 2–14 all have one. Class 15 is a translation assignment, so this is probably intended. (old A2) | Confirm intended | 3 |
| 5_class.md:120 | `assasissāmi \| verb \| fut.1st.sg \| I will breathe in \| √sas･1 a (breath)` | The root gloss is copied from DPD, which has a noun where a verb is expected; also 5_class.md line 132 and 10_class.md lines 195-243. DPD-side. (old D23) | Raise upstream ("breathe") | 6 |
| 5_class.md:66 | `√dū×1 a (go, run)` | The root mark `×` (78 cells) beside `･` (1 729 cells, mech counts) is explained nowhere in docs/bpc, docs/bpc_ex or docs/bpc_key. (old D24) | Explain the two marks once (e.g. in index.md) | 8 |

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
