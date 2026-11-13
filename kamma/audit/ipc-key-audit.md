# IPC key audit — `docs/ipc_key/`

Date: 2026-11-13 (light pass over the audit of 2026-11-12)
Scope: all 15 Markdown files under `docs/ipc_key/` (index + classes 16–29; 9 068 lines, 6 604 table rows, as counted by `mech_checks.py`).
No file in `docs/` was modified. This is a findings list only.

The audit of 2026-11-12 was close to `kamma/audit/audit-guide.md`, so the folder was not read again. This pass put the old rows into the guide's format, ran the shared scripts, sent every doubtful row through one DPD round, added category I and cross-checked the result with the new `ipc-audit.md`. Every row comes from the old audit and ends its `Problem` with `(old <id>)`; the ids were given by category and order (`A1`, `A2`, …) when the old file was frozen.

Related to #6 Course enhancement with AI

## Method and limits

| Check | How | Result |
| --- | --- | --- |
| Freeze of the old audit | `git show HEAD:kamma/audit/ipc-key-audit.md` into `kamma/audit/scratch/ipc-key/old-audit.md`, each row of sections A–H numbered | 703 ids: A 129, B 159, C 89, D 117, E 58, F 122, G 10, H 19 |
| Conversion of the old rows | One-off script: one slice file per class, `(old <id>)` appended, `\|` written as `¦`; then `uv run python kamma/audit/scripts/verify_rows.py docs/ipc_key kamma/audit/scratch/ipc-key/k*.md` | 703 rows in 14 slices; `OK 813  FAIL 0`, which proves the conversion |
| Mechanical checks | `uv run python kamma/audit/scripts/mech_checks.py docs/ipc_key --folder-footnotes --links-out kamma/audit/scratch/ipc-key/links.txt` | No column mismatch, no index/H1 difference, footnotes 55 refs / 55 defs with 8 out of order (classes 19, 27), no stray character. Nothing that the old rows or old M1 and M3 did not already hold |
| Key sentence vs exercise sentence | `uv run python kamma/audit/scripts/key_vs_ex.py docs/ipc_key docs/ipc_ex --glob "*_class.md"` | The same 28 differing sentences as old M2, plus 31 label and `<br>`-spacing items, all covered: 68 script items covered, 0 new |
| Non-sutta links | `curl -s -o /dev/null -w '%{http_code}' -L --max-time 15 <url>` for each link not on `s.dhamma.gift` | No such link: all 271 link occurrences (185 unique) are on `s.dhamma.gift` |
| DPD triage | Every row with confidence below 8, or with `verify` or `DPD lookup` in `Suggested`, re-read against its source line (254 rows) | 68 rows had a question DPD can answer; the others say `verify` (a reading, an inflection, a translation choice) or `owner decision`. 4 note-only rows moved to category I |
| DPD lookups | `uv run python kamma/audit/scripts/dpd_lookup.py <lemma> …`, run once over the 81 lemmas of those 68 rows | All 68 finalised against the DPD entry; none dropped. 1 lemma is not a DPD headword (`assādato`) |
| Old-id accounting | Shell loop over the 703 ids: `grep -qF "(old $id)"` in the slice files | 0 missing; no old row was dropped |
| Cross-check with the ipc audit | One-off token match of the A, B and C rows of `ipc-audit.md` against the rows here (3 199 candidate lines, 221 tokens), then a search of these rows for every form, root and gloss the ipc audit deals with | 2 overlaps aligned on the ipc side; no row here had to change (see "Cross-check with the ipc audit") |
| Excerpt check | `uv run python kamma/audit/scripts/verify_rows.py docs/ipc_key …` on every slice file and on this file: each backtick excerpt in `Current` searched in the cited file within 2 lines of the cited line | OK 813, FAIL 0 (slices and final); 0 rows with no source file |
| Merge | `uv run python kamma/audit/scripts/merge_audit.py kamma/audit/scratch/ipc-key/merge.toml` | This file |

Carried from the audit of 2026-11-12 and not run again:

- The full line-by-line read of every file, by the main session, one class per slice.
- `uv run python scripts/verify_key.py --course ipc --warnings`: exit 0; 63 word-coverage warnings (Mechanical detail, M1).
- `uv run python scripts/verify_key.py --course ipc --dpd` (advisory): 85 IMPOSSIBLE, 21 NOT-FOUND, 4 ROOT-MISMATCH, all looked at during the read (M4).
- `uv run python scripts/check_sutta_links.py docs/ipc_key`: 185 links / 79 pages, all pass.
- The targeted DPD lookups made during the read.

Not verified:

- The folder was not read again. A defect that the first read missed is still missing.
- Rows at confidence 8 or above were not looked at in this pass, apart from the cross-check.
- `dpd_lookup.py` prints headwords, not inflection tables. Rows whose doubt is an inflected form (`addasā`, `āgā`, `sakhā`, `sukhe`) say `verify` or `DPD lookup`.
- Canonical readings were not compared with a text edition. Rows that depend on a reading say `verify`.
- The link checker proves that the page and anchor exist, not that the sentence is in that sutta.
- The 2 345 "ambiguous" rows of the DPD form check were not reviewed one by one.
- `docs/ipc_ex/` was read only where it differs from the key (M2).
- Translation rewordings in section C are suggestions, not corrections.
- Rendered output (site, PDF, DOCX) was not built.

Paths below are relative to `docs/ipc_key/`. In `Current`, `\|` is a table pipe in the source. `ex NN` is a line number in the exercise file of the same class.

## Summary

| Category | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | new | Total | Conf. ≥ 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A. Pāli and grammar content errors | 6 | 5 | 4 | 5 | 2 | 3 | 13 | 24 | 17 | 8 | 9 | 10 | 10 | 12 | 0 | 128 | 102 |
| B. Tables, paradigms and lists that disagree with each other or themselves | 9 | 10 | 6 | 15 | 19 | 14 | 19 | 15 | 12 | 9 | 10 | 7 | 5 | 9 | 0 | 159 | 127 |
| C. Translation and gloss problems | 4 | 4 | 6 | 5 | 9 | 6 | 14 | 10 | 7 | 5 | 6 | 5 | 4 | 4 | 0 | 89 | 29 |
| D. English typos and grammar | 6 | 8 | 9 | 15 | 10 | 8 | 7 | 10 | 9 | 9 | 6 | 8 | 5 | 7 | 0 | 117 | 89 |
| E. Markdown defects that affect rendering | 4 | 2 | 5 | 5 | 6 | 3 | 4 | 5 | 6 | 6 | 1 | 4 | 5 | 2 | 0 | 58 | 41 |
| F. Convention drift | 20 | 13 | 8 | 11 | 11 | 7 | 9 | 9 | 7 | 5 | 6 | 6 | 4 | 6 | 0 | 122 | 93 |
| G. Links | 0 | 2 | 0 | 1 | 0 | 1 | 0 | 0 | 2 | 2 | 0 | 1 | 1 | 0 | 0 | 10 | 3 |
| H. Data to re-verify (forms, references, counts) | 0 | 1 | 1 | 0 | 0 | 2 | 4 | 4 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 16 | 3 |
| I. Further details on the material under review | 2 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 1 |
| **Total** | **51** | **46** | **39** | **57** | **57** | **45** | **70** | **77** | **61** | **45** | **38** | **41** | **35** | **41** | **0** | **703** | **488** |

A row often covers several locations, so the number of places to edit is higher than the row count.

Overall confidence: 9/10 that the quoted text is where the row says (scripted). 8/10 for categories D, E, F and G (visible in the source). 7/10 for A, B, C and H as a group: DPD was consulted for the doubtful forms but no text edition was; use the per-row score.

## Decisions for the owner

These recur through the folder. The audit lists where they occur and does not decide them.

- `ger` or `abs` for the `-tvā` / `-ya` form: 32 `ger` against 56 `abs`, mixed within most classes (M3). DPD itself uses `ger` for some headwords.
- Sandhi apostrophes: in classes 16–18 and 21–23 one part of the items marks sandhi with apostrophes in the sentence and the rows, the other part does not (first row: `16_class.md:316`).
- Empty cells: blank in one part of a class, `-` in the other (first row: `16_class.md:411`). Same drift in the grammar label of `iti` (`quote`, `quotation mark`, `-`, blank).
- Inserted consonants (`[d]`, `[r]`, `[y]`, `[m]`): shown in the sandhi tables, not in the word tables.
- Bahubbīhi notation: `kammadhāraya \> bahubbīhi`, unescaped `>`, ` - `, or a footnote.
- `lit:` (124) or `lit.` (80); round or square brackets for supplied words; `...` or `…`.
- `<br>` in table cells and translation lines against the "no raw HTML in sources" rule (502 occurrences).
- Reference label styles: `UD45` / `UD5.10`, `SNP7` (running number) / anchors by vagga, `DHP064`, `VIN1.1.2`, `VIN PAT PC 68`; `DN2.4` (`25_class.md:143`) is volume.sutta and links to the wrong sutta.
- Thag / Thig anchors: the link rule sends every verse to the first poem of its nipāta (`#thagN.1`); the labels are verse numbers.
- Three references without links: `17_class.md:637` (`VV 52`), `27_class.md:42` (`VIN PAT NID`), `27_class.md:252` (`VIN PAT SA`).
- Editorial footnotes in the first person (classes 20, 24, 25, 27) and footnotes that argue against the analysis in their own row (53 and 55 in class 29).
- Reflexive forms translated literally ("I myself", "oneself") in class 21, and the tag for `-eyyaṃ` (`opt.1st.sg` or `opt.reflx.1st.sg`).
- UK or US spelling.
- Bold target words and supplied verbs (`(passati)`, `(addasa)`) in the sentence: in the key, the exercise, or both.
- Class 23 extra example 10 repeats item 13 word for word (key and exercise).
- The old root column (classes 16–22) and the construction column (classes 23–29): keep both systems or bring one through.

## What the DPD round changed

68 rows waited for the lookup. All were kept, and their `Suggested` now names the DPD entry. Three old claims were corrected on the way:

- `abyāpajjha` (`17_class.md:590`, old B14): DPD does have the masculine noun the key uses; the adjective is the better fit beside `cetasā`, so the row stays at confidence 6.
- `kiñci` (`21_class.md:252`, old A25): DPD lists `kiñci` as masc and nt acc sg, so the key's tag is sound. Only the reading of Kp 9 is left; the row moved from A to H.
- `evañcetaṃ` (`17_class.md:495`, old A11): DPD has both `evaṃ + ce + etaṃ` (the key's analysis) and `evaṃ + ca + etaṃ`; the row asks only which fits AN 10.61.

Compound types and roots now given from DPD: `catutthī tappurisa` for the `X-anusaya` compounds and `brahmacariyānuggaha`; `chaṭṭhī tappurisa` for `upādānakkhandha`, `iddhividhā`, `muttakarīsapuṇṇa`; `digu` for `aṭṭhaṅgika`; `dvanda` for `bhavūpapatti` and for the noun `pītisukha`; `kammadhāraya > bahubbīhi` for `kumbhūpama`, `tapparāyaṇa`, `vippariṇāmadhamma`; `√khandh`, `√jhā` for `ajjheti`, `√kup` for `asaṅkuppa`, `√bhū` for `bhante`; the prefix `nī` in `parinibbuta` and `niccheyya`; `card` for the numerals.

## Old rows dropped

None. All 703 old ids have a row here.

## Cross-check with the ipc audit

The rows here were compared with `ipc-audit.md` wherever both touch the same form, root or gloss. Two overlaps were aligned, both by changing the ipc row:

- `gahetvā` (`23_class.md:570`) and the lesson's `gahetabba` (`ipc/class_27/2_kicca.md:35`): both audits now say that `gahe` is an irregular base, which the sign `ṇhā` does not produce.
- `bhagavā` and `tathāgata` (`24_class.md:209`, `19_class.md:324`, and the C rows of classes 16 and 17): the ipc audit now names the same rendering, `the Blessed One`.

Agreeing without change: `ger` / `abs` and UK / US spelling are owner decisions in both audits; `pāva` is a perfect of `vadati` in both; the prefix is `nī` in `parinibbuta` and `niccheyya` here and in the verbs of ipc class 23; `veyaggha` is the derived adjective in both; `samādhiyati` is a passive in both; `√ādā` (in `anādiya`, `23_class.md:749`) is a DPD root, and the ipc audit no longer reports it.

## A. Pāli and grammar content errors

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 16_class.md:355 | `anuggahāya \| noun \| nt.dat.sg` | DPD: `anuggaha` "support, help" is masculine (old A1) | `masc.dat.sg` | 9 |
| 16_class.md:224 | `bhante \| noun \| masc.voc.sg \| venerable sir \| √bhad×1 a (be good, lucky)` | DPD derives `bhante` from `bhavant` (√bhū). Flagged ROOT-MISMATCH by `verify_key.py --dpd`. Same at 17_class.md:671 and 20_class.md:454 (old A2) | `√bhū･1 a (be, become)` or leave the root empty | 8 |
| 16_class.md:800 | `\#nāda \| noun \| masc.nom.sg \| a roar` | Stem form tagged as nominative singular; the final member of `sīhanādo` is `nādo` (cf. `\#karo`, `\#mūlo`) (old A3) | `\#nādo` | 9 |
| 16_class.md:367 | `āvuso \| noun \| masc.voc.pl \| friends` | AN4.45 is spoken to one person (Rohitassa), so singular. Also DPD: `āvuso` is an indeclinable. Translation line 377 has "friends" (old A4) | `ind \| voc.sg \| friend`; translation "friend" | 8 |
| 16_class.md:44 | `vutti + assa \| vuttassa` | `i + a` normally gives `y` (`vutyassa`, the Kaccāyana example); `vuttassa` looks like the genitive of `vutta` (old A5) | verify; probably `vutyassa` | 6 |
| 16_class.md:56 | `nu + ayaṃ \| nāyaṃ` | Expected `nvāyaṃ` (`u + a > vā`, as in `kho + ayaṃ > khvāyaṃ` on line 59); `nāyaṃ` is `na + ayaṃ` (old A6) | verify | 5 |
| 17_class.md:125 | `\#evaṃ \| ind \| emph \| only; just` | Gloss and tag of `eva` given to `evaṃ` (first member of `evarūpaṃ`) (old A7) | `\#evaṃ \| ind \| adv \| thus; such` | 9 |
| 17_class.md:458 | `āvuso \| noun \| masc.voc.pl \| friends` | AN4.45 is addressed to one person (Rohitassa; he answers `bhante` in extra example 8). Translation line 489 also has "friends" (old A8) | `voc.sg \| friend` | 8 |
| 17_class.md:215 | `\#yāvaṃ \| adj \| nt.nom.sg \| as many as; however many` | DPD analyses `yāvañcidaṃ` as `yāva + [ṃ] + ca + idaṃ`; `yāva` is an indeclinable, not an adjective `yāvaṃ` (old A9) | `\#yāva \| ind \| adv \| as far as` (DPD: `yāva` ind, adv) | 8 |
| 17_class.md:20 | `pati + √i + \*a \| paccayā` | The construction gives the stem `paccaya` (the other rows give stems: `saññama`, `accanta`) (old A10) | `paccaya`; verify | 7 |
| 17_class.md:495–497 | `evañcetaṃ \| - \| - \| even if this` / `\#ce \| ind \| - \| if` | AN10.61 `evañcetaṃ … vuccati, atha ca pana …` is usually resolved `evaṃ + ca + etaṃ` ("and though this is said") (old A11) | verify which fits AN 10.61: DPD has both `evaṃ + ce + etaṃ` ("even if this", the key's reading) and `evaṃ + ca + etaṃ` ("and this is the case") | 5 |
| 18_class.md:262 | `\#āpa \| noun \| masc.nom.sg \| water, liquid` | Stem tagged as nominative singular (not a possible nom.sg; flagged by the DPD check). Same at 265 (`\#teja`) and 268 (`\#vāya`). The members in the compounds are `āpo`, `tejo`, `vāyo` (old A12) | `\#āpo \| noun \| masc` (stem), likewise `tejo`, `vāyo` | 9 |
| 18_class.md:210 | `\#\#rūpa \| adj \| masc.nom.pl \| of quality, of kind` | Stem with a nom.pl tag; the member of `tathārūpā` is `rūpā` (old A13) | `\#\#rūpā` | 9 |
| 18_class.md:69 | `\#etaṃ \| pron \| nt.acc.sg \| this` | In `icc'etaṃ kusalaṃ` ("thus this is good") `etaṃ` is the subject (old A14) | `nt.nom.sg` | 8 |
| 18_class.md:483 | `taṃ \| pron \| masc.acc.sg \| that` | Refers to `kāraṇaṃ` (line 463, `nt`); the translation says "that (task)" (old A15) | `nt.acc.sg`; verify | 7 |
| 19_class.md:385 | `**sīlakathā \< sīlaṃ + kathā (dutiyā tappurisa)**` | Contradicts the table (362–363: `chaṭṭhī tappurisa`, `\#sīlassa \| noun \| nt.gen.sg`) and DPD (`chaṭṭhī tappurisa sīlassa + kathā`) (old A16) | `sīlakathā \< sīlassa + kathā (chaṭṭhī tappurisa)` | 9 |
| 19_class.md:488 | `abhāsi \| verb \| aor.3rd.sg \| spoke \| a√bhā･1 a (shine, speak)` | `abhāsi` "spoke" is from `√bhās` (DPD `a + √bhās + i`); `√bhā` is "shine". The augment is also written inside the root cell (old A17) | `√bhās･1 a (speak)` | 8 |
| 19_class.md:161 | `\#paññā [eva] \| noun \| fem.nom.pl \| wisdom [just]` | First member tagged nominative plural; also 166 (`\#vimutti [eva] \| noun \| fem.nom.pl`). 156 has the stem tag `fem.` for the same pattern (old A18) | `fem` | 8 |
| 19_class.md:362–365 | `sīlakathāya \| noun \| fem.gen.sg (gen abs)` … `kacchamānāya \| prp pass \| fem.gen.sg (gen abs)` | Feminine `-āya` is also locative, and the usual absolute is the locative (cf. `abhikkantāya rattiyā … (loc abs)` at 430–431) (old A19) | verify; probably `fem.loc.sg (loc abs)` | 6 |
| 19_class.md:520 | `\#dūrā \| adj \| masc.nom.pl \| far away` | In `kīva dūr'ev'ime` the elided word is more likely the adverb `dūre` ("how far away") (old A20) | verify; `\#dūre \| ind \| adv` is possible (DPD has the adverb `dūre` beside the adjective `dūra`) | 6 |
| 20_class.md:225 | `\#vivakasmā \| noun \| masc.abl.sg \| from separation` | Misspelt; the analysis line 241 has `vivekasmā` (old A21) | `\#vivekasmā` | 9 |
| 20_class.md:628, 632 | `uttarimanussadhammā \| noun \| masc. \| superhuman attainments` / `\#dhammā \| noun \| masc.nom.pl \| states` | Case missing on the compound row; in `natthi … uttarimanussadhammā alamariyañāṇadassanaviseso` it is ablative singular ("beyond the human state"), not nom.pl. Row 632 is also one `\#` level too high (it belongs under `\#manussadhammā`) (old A22) | `masc.abl.sg`; `\#\#dhammā \| noun \| masc.abl.sg`; verify the case (DPD confirms the compound as masc, `uttari + manussadhamma`, which supports moving row 632 one level down) | 7 |
| 21_class.md:51 | `\#ātītā \| pp \| masc.nom.pl \| gone past` | Misspelt: the member of `khaṇ'ātītā` is `atītā` (`khaṇa + atīta`); not in DPD (old A23) | `\#atītā` | 9 |
| 21_class.md:126 | `√khand･1 a (jump up, pile up)` | DPD derives `khandha` from `√khandh` (flagged ROOT-MISMATCH by `verify_key.py --dpd`) (old A24) | `√khandh` (DPD: `√khandh + a`) | 9 |
| 21_class.md:529 | `\#uggahitaṃ \| pp \| nt.nom.sg \| grasped` | Short `i`; the verse and the compound row 527 have `paramuggahītaṃ`. DPD has both `uggahita` and `uggahīta`, and gives `paramuggahīta` as `parama + uggahīta` (old A26) | `\#uggahītaṃ` | 9 |
| 22_class.md:18 | `settha \| verb \| aor.2nd.pl \| you slept` | DPD: `settha` = aor reflx 1st sg of `sesi` ("I myself slept"). The speaker laments his own night; the translation (32) follows the wrong person (old A27) | `aor.reflx.1st.sg \| I slept` | 9 |
| 22_class.md:30 | `\#cārī \| noun \| masc.nom.sg \| one who is wandering \| √car･1 a (act, behave)` | Gloss "wandering" with the root meaning "(act, behave)". DPD: `cārī` "roaming; wandering" is from the "move, walk" root (so `caranti` at 21_class.md:514); "behaving" is the other `√car` (old A28) | `√car･1 a (move, walk)` (DPD: `cārī` 2.1 "roaming; wandering" is under `√car` 1; "acting; behaving" is `√car` 2) | 7 |
| 22_class.md:193 | `\#vīriyadhuraṃ \| noun \| nt.acc.sg \| the yoke of effort` | First member of a `tatiyā tappurisa` ("reined in by …") given in the accusative; also `\#\#dhuraṃ \| noun \| nt.acc.sg` at 195. Compare `\#hiriyā \| noun \| fem.instr.sg` at 140 (old A29) | `\#vīriyadhurena \| noun \| nt.instr.sg \| by the yoke of effort`; `\#\#dhurena` | 8 |
| 22_class.md:200 | `gamissase \| verb \| fut.reflx.2nd.sg \| you yourself will go \| √gam･1 \*e (go)` | Sign `\*e`; the same root is `√gam･1 a (go)` at 130, 403, 537, 620 (old A30) | `√gam･1 a (go)` | 9 |
| 22_class.md:223 | `\#evaṃ \| ind \| \| thus` | `evāhaṃ` is `eva + ahaṃ`; the sandhi row (222) is glossed "I just" and the translation has "I just thought" (old A31) | `\#eva \| ind \| emph \| just` | 9 |
| 22_class.md:260 | `\#vāsa \| noun \| masc.nom.sg \| living` | Stem form tagged nom.sg (flagged IMPOSSIBLE by `verify_key.py --dpd`) (old A32) | `\#vāso` | 9 |
| 22_class.md:400 | `\#mattāya \| adj \| fem.abl.sg \| from measure` | `mattā` is a feminine noun in DPD (old A33) | `noun` | 8 |
| 22_class.md:459 | `sakhā \| noun \| masc.nom.pl \| companions` | DPD: `sakhā` is nom.sg of `sakha` (flagged IMPOSSIBLE). `\#ñāti (ca)` at 457 is also tagged `masc.nom.sg` inside a plural dvanda (old A34) | verify; `masc.nom.sg \| companion` (DPD: `sakha` masc, atta group; the inflection table is not in the headword output: DPD lookup) | 6 |
| 22_class.md:497 | `\#\#ābādha \| noun \| fem. \| disease; sickness; illness; affliction` | `ābādha` is masculine (so `ābādhāya \| noun \| masc.dat.sg` at 319). `\#\#appa \| adj \| fem.` at 496 and 503 follows the same slip (503 stands before `ātaṅka \| noun \| masc`) (old A35) | `masc.` | 9 |
| 22_class.md:500 | `sañjānissatha \| verb \| fut.2nd.pl \| you will know, etc \| √ñā･5 ya (know)` | `ya` is the passive sign (as in `paññāyetha`, 261); the active future takes `nā` (71, 93). Gloss "etc" is unfinished; the translation has "will experience" (old A36) | `√ñā･5 nā (know)`; "you will perceive; experience" | 9 |
| 22_class.md:577 | `\#nibbānassa \| noun \| nt.acc.sg \| nibbāna` | Genitive/dative form tagged accusative (flagged IMPOSSIBLE); the same member is `\#nibbānaṃ \| noun \| nt.acc.sg \| to nibbāna` at 570 and 574 (old A37) | `\#nibbānaṃ \| noun \| nt.acc.sg \| to nibbāna` | 9 |
| 22_class.md:615 | `\#dārā \| noun \| fem.nom.pl \| wives` | `dāra` is masculine in DPD (old A38) | `masc.nom.pl` | 9 |
| 22_class.md:627 | `\#soṇa (+ca) \| noun \| masc.nom.pl \| dogs` | Stem form tagged nom.pl; the other members are `kukkuṭā`, `sūkarā`, `siṅgālā` (old A39) | `\#soṇā` | 9 |
| 23_class.md:65 | `\#**hitena** \| pp \| masc.instr.sg \| lit. placed \| dhā + ita` | Root sign `√` missing; also `labh + tvāna` at 585 (old A40) | `√dhā + ita`; `√labh + tvāna` | 9 |
| 23_class.md:122 | `\#yācaṃ \| noun \| nt.acc.sg \| something asked for; begged item` | The compound (121) is `dutiyā tappurisa \> bahubbīhi`; DPD has `yācayoga` as `sattamī tappurisa > bahubbīhi`, `yāce + yoga` (old A41) | `sattamī tappurisa \> bahubbīhi` at 121; `\#yāce \| noun \| nt.loc.sg` (DPD: `yāce + yoga`) | 7 |
| 23_class.md:157 | `\#samo \| adj \| masc.nom.sg \| like; equal` | Predicate of the neuter `kiñci` ("anything"); `sam'atthi` resolves as `samaṃ + atthi` (old A42) | `\#samaṃ \| adj \| nt.nom.sg`; verify | 7 |
| 23_class.md:177 | `\#aṭṭhaṅgikaṃ \| adj \| masc.acc.sg \| eightfold \| kammadhāraya \> bahubbīhi` | A compound with a numeral first member; DPD: `digu aṭṭha + aṅgika` (old A43) | `digu` (DPD: `aṭṭha + aṅgika`) | 8 |
| 23_class.md:182 | `\#dukkhūpasamaṃ \| adj \| masc.acc.sg \| calming of suffering; relief from suffering \| chaṭṭhī tappurisa` | Noun glosses and a noun type; DPD: masc noun (old A44) | `noun` | 9 |
| 23_class.md:230 | `**vihaṃsu** \| verb \| aor.3rd.pl \| they lived \| vi + √har + suṃ` | The ending of `vihaṃsu` is `ṃsu`, not `suṃ`; DPD: `vi + ha + ṃsu` (irregular) (old A45) | `vi + √har > ha + ṃsu` | 8 |
| 23_class.md:231–232 | `tap'**parāyaṇā** \| adj \| masc.nom.pl \| with that as final goal (lit: culminating in that) \| dutiyā tappurisa` / `\#taṃ \| pron \| nt.acc.sg \| that` | The gloss "with that as final goal" is a bahubbīhi reading; DPD: `kammadhāraya > bahubbīhi`, `tad + parāyaṇa` (old A46) | `kammadhāraya \> bahubbīhi`; first member `tad` (DPD: `tad + parāyaṇa`) | 7 |
| 23_class.md:274 | `\#avatthārakena \| noun \| nt.instr.sg \| by covering over` | `avatthāraka` is masculine in DPD, and the compound row (272) is `masc.instr.sg` (old A47) | `masc.instr.sg` | 9 |
| 23_class.md:292 | `**√ṭhā 1 āpe (to stand) \> ṭhape (caus). thape + tvā**` | `thape` for `ṭhape`; the same line is repeated at 294 with the same slip (old A48) | `ṭhape + tvā` | 9 |
| 23_class.md:355 | `\#sotaṃ \| noun \| masc.nom.sg \| the stream` | Accusative form tagged nominative (flagged IMPOSSIBLE); DPD: `dutiyā tappurisa > bahubbīhi chinna + sotaṃ` (old A49) | `masc.acc.sg` | 9 |
| 23_class.md:364 | `**√jhe 1 a (to think) . na + ā + √jhe + ti**` | Root written `√jhe` with sign `a`; the lines for `jhāyanti` (329–335) have `√jhā 3 ya`, and DPD gives `ajjheti` as `√jhā`, `ā + jhe + ti`. Space before the full stop (old A50) | `√jhā … ya (to think) \> jhe. na + ā + jhe + ti`, with the key's root number as at 329–335 (DPD: `ajjheti` = `√jhā`, sign `ya`, `ā + jhe + ti`; `√jhe a` is DPD's "burn" root) | 8 |
| 23_class.md:398 | `**√kir 1 a (to scatter, sprinkle) \> kira. ava + kira + ti**` | Singular ending `ti` for the plural `okiranti`; also 400 (`ajjhokiranti`), 588 (`dadanti`), 598 (`abhipatthayanti`), 687 (`abhigijjhanti`). `ti` for an optative at 455 and 861 (`anvāssaveyyuṃ`) and 545 (`saṃvatteyya`). Line 402 has `nti` (old A51) | `nti`; `eyyuṃ`; `eyya` | 9 |
| 23_class.md:469–471 | `iddhividhaṃ \| noun \| fem.acc.sg \| kinds of psychic power \| kammadhāraya` / `\#vidhaṃ \| adj \| fem.acc.sg \| of the kind` | DPD: `iddhividhā`, `chaṭṭhī tappurisa iddhiyā + vidhā` (noun + noun) (old A52) | `chaṭṭhī tappurisa`; `\#vidhaṃ \| noun` (DPD: `iddhiyā + vidhā`) | 8 |
| 23_class.md:485 | `āvibhāvaṃ \| noun \| masc.acc.sg \| appearance \| abyayībhāva` | A declined masculine noun is not an abyayībhāva; also `tirobhāvaṃ` 488. DPD: `tirobhāva` kammadhāraya (old A53) | `kammadhāraya` | 8 |
| 23_class.md:529 | `kāyakammaṃ \| noun \| nt.nom.sg \| physical action \| kammadhāraya` | DPD: `tatiyā tappurisa kāyena + kamma`; the sentence itself has `kāyena kammaṃ` (old A54) | `tatiyā tappurisa`; `\#kāyena` | 8 |
| 23_class.md:556 | `\#se \| pron \| masc.nom.sg \| that; it` | DPD: `se` in `seyyathāpi` is nt nom sg of `ta` (flagged IMPOSSIBLE); also 641, there glossed "he; that" (old A55) | `nt.nom.sg \| that; it` | 9 |
| 23_class.md:570 | `gahetvā \| verb \| abs \| having taken; having seized \| √gah + ṇhā + tvā` | `gahetvā` has no `ṇhā`; line 802 of this class gives `gahe (irreg base). gahe + tvā`, as DPD does (old A56) | `√gah \> gahe + tvā` | 8 |
| 23_class.md:622 | `\#payirupāsanā \| noun \| fem.acc.sg \| attending closely` | Nominative forms tagged accusative (flagged IMPOSSIBLE): `payirupāsanā` here, `\#anussati` at 626; the sandhi rows have `payirupāsanam…`, `anussatim…` (old A57) | `\#payirupāsanaṃ`; `\#anussatiṃ` | 9 |
| 23_class.md:651 | `**ucco** \| adj \| masc.nom.sg \| high; tall \| ud + tya` | DPD: `ud + ya` (old A58) | `ud + ya` (DPD) | 9 |
| 23_class.md:673–674 | `manoduccaritena \| adj \| nt.instr.sg \| mental misconduct; misbehavior by mind` / `\#manasā \| adj \| nt.instr.sg \| by mental; with mind` | The third of three parallel compounds; the first two and their members are nouns (667–672) (old A59) | `noun`; "by mind" | 9 |
| 23_class.md:689 | `**analaṅ'katā** \| adj \| masc.nom.pl (+loc) \| with insatiable appetite (for) [lit: not made enough] \| kammadhāraya \> bahubbīhi` | DPD: `kammadhāraya na + alaṅkata`, no bahubbīhi step. Sandhi apostrophe inside the compound (old A60) | `kammadhāraya` (DPD: `na + alaṅkata`) | 8 |
| 23_class.md:756 | `\#**parinibbuto** \| pp \| masc.nom.sg \| completely quenched; entirely liberated \| pari + nir + √vā + ta` | DPD: `pari + nī + √vā`; the key writes `nī + √sar` at 916 (old A61) | `pari + nī + √vā + ta` (DPD) | 8 |
| 23_class.md:876 | `upādānakkhandhānaṃ \| noun \| masc.gen.pl \| of these grasping aggregates \| kammadhāraya` | DPD: `chaṭṭhī tappurisa upādānassa + khandha`. "these" in the gloss belongs to `imesaṃ` (874) (old A62) | `chaṭṭhī tappurisa` (DPD: `upādānassa + khandha`); "of the grasping aggregates" | 8 |
| 23_class.md:306 | `\#āvuso \| noun \| masc.voc.sg \| friends, brothers` | Singular tag with plural glosses (flagged IMPOSSIBLE; DPD: `ind`, voc sg and pl) (old A63) | `ind` (DPD: ind, voc sg & pl), or `masc.voc.pl`; as in class 16 | 8 |
| 24_class.md:7 | `**pati + √gah + ṇhā + ti**` | Example word is `paṭiggaṇhāmi` (line 5); the ending is `mi`, as at 23_class.md:31 (old A64) | `pati + √gah + ṇhā + mi` | 9 |
| 24_class.md:27 | `**jīyissati** \| verb \| fut.3rd.sg \| will get old; will age \| √jī + ya + ti` | Future forms analysed without the future sign: 27, 30 (`√mar + īya + ti`), 33 (`√kup + ya + ti`), 36 (`√pih + \*e + ti`), 132 (`gacchissanti … √gam + a + ti`, plural too), 381 (`ājānissāmā'ti … ā + jānā + ti`), 447. Lines 127 and 438 give `issa` / `ssa` (old A65) | `√jī + ya + issa + ti` etc. | 9 |
| 24_class.md:106 | `\#\#ñassāmi \| verb \| fut.1st.sg \| I will know \| √ñā + ssa + ssa + mi` | `ssa` twice; DPD: `√ñā + ssa + ti` (old A66) | `√ñā + ssa + mi` | 9 |
| 24_class.md:109, 112 | `aññ'indriyaṃ \| noun \| nt.nom.sg \| faculty of enlightenment \| kammadhāraya` / `aññātāv'indriyaṃ \| noun \| nt.nom.sg \| faculty of one who is enlightened \| kammadhāraya` | Genitive glosses with the type kammadhāraya; DPD: `chaṭṭhī tappurisa aññāya + indriya`, `aññātāvino + indriya` (old A67) | `chaṭṭhī tappurisa` | 8 |
| 24_class.md:181 | `addasā \| verb \| imperf.2nd.sg \| you saw \| √dis + a \> disa \> dasa (irreg)` | DPD knows `addasā` only as imperf 3rd sg (flagged IMPOSSIBLE); the address `samaṇa` makes the sense second person (old A68) | verify; note the form | 6 |
| 24_class.md:193 | `evamārocimha \| verb \| aor.1st.pl \| we informed thus \| evaṃ + ārocesi` | Sandhi (`evam'ārocimha` in the sentence) tagged as a verb; the construction cell gives a 3rd sg form instead of a breakdown (old A69) | `sandhi`; `\#ārocimha \| verb \| aor.1st.pl \| … \| ā + √ruc + \*e + imha` | 8 |
| 24_class.md:218 | `vibhajeyyā'ti \| verb \| opt.3rd.sg \| he could analyse, dissect" \| vi + bhaja + ti` | Ending `ti` for an optative; sandhi with `iti` tagged as a verb; stray closing quote in the gloss (old A70) | `sandhi`; `vi + bhaja + eyya` | 9 |
| 24_class.md:263 | `\#samādhinā \| noun \| masc.instr.sg \| with mental stability \| saṃ + ā + √dhā + i + inā` | The instrumental ending is `nā`; DPD: `saṃ + ā + √dhā + i` (old A71) | `saṃ + ā + √dhā + i + nā` | 8 |
| 24_class.md:299 | `brahmacariyavāso \| adj \| masc.nom.sg \| living the holy life \| dutiyā tappurisa` | A noun (so tagged at 22_class.md:256; DPD: masc) (old A72) | `noun` | 9 |
| 24_class.md:359 | `nappaṭikkosiṃsu \| verb \| aor.3rd.pl \| nor rejected \| a + pati + kosa + iṃsu` | The word is `na + paṭikkosiṃsu`; the construction starts with `a`, and 366 writes the negative as `na \> a`. Sandhi with `na` not split (old A73) | `na + pati + kosa + iṃsu`; verify | 7 |
| 24_class.md:489 | `\#se \| pron \| masc.nom.sg \| it, that` | DPD: nt nom sg of `ta` (flagged IMPOSSIBLE); also 547; see 23_class.md:556 (old A74) | `nt.nom.sg` | 9 |
| 24_class.md:520 | `\#ādhāna \| noun \| nt.loc.sg \| receptacle; bucket` | Stem form tagged locative (flagged IMPOSSIBLE) (old A75) | `\#ādhāne` | 9 |
| 24_class.md:522 | `**kāriyamānassa** \| prp pass \| masc.gen.sg (gen abs) \| being made to do \| √kar + iya +māna` | "being made to do" is the passive of the causative (DPD: `√kar \*e iya`, `kāriya + māna`); the construction has no causative sign, and no space after `+`. `prp pass` here, `prp` for the passive `vuyhamāno` at 466 (old A76) | `√kar + \*e + iya + māna` | 8 |
| 24_class.md:523 | `honti \| verb \| pr.3rd.pl \| there are \| √hū + a + ti` | Singular ending for a plural form (old A77) | `√hū + a + nti` | 9 |
| 24_class.md:525 | `\#ye \| ind \| masc.nom.pl \| just; only` | `y'eva` is `eva` with an inserted `y` (DPD: `[y] + eva`), not `ye + eva`; pos `ind` with a case tag (old A78) | `\#y \| consonant` (as at 22_class.md:175) | 9 |
| 24_class.md:339 | `appaṭivāniñ'ca \| noun \| fem.acc.sg \| and tireless determination \| na \> a + pati + √vā + na + ī` | DPD has `appaṭivānī` as masculine (old A79) | `masc.acc.sg` (DPD: `appaṭivānī` masc) | 7 |
| 24_class.md:425 | `brahmacariyānuggahāya \| noun \| masc.dat.sg \| for supporting the spiritual path \| chaṭṭhī tappurisa` | DPD: `catutthī tappurisa brahmacariyassa + anuggaha` (old A80) | `catutthī tappurisa` (DPD) | 8 |
| 25_class.md:15 | `cātummahārājikānaṃ \| adj \| masc.gen.pl \| of the Four Great Kings \| *cātumahārāja + \*ika*` | The base is given with the lengthened vowel that the suffix produces; DPD: `catumahārāja + *ika`. Word with `mm`, base with `m` (old A81) | `*catumahārāja + \*ika*` | 8 |
| 25_class.md:84 | `bhāsitā \| noun \| masc.nom.sg \| speaker; who talks (about) \| √bhās + ita` | Agent noun; the suffix is `itar` (DPD: `√bhās + itar`), `ita` is the pp suffix (old A82) | `√bhās + itar` | 9 |
| 25_class.md:262 | `**vāca + \*ika**` | DPD derives `vācasika` from `vacas`: `vacas + *ika` (old A83) | `vacas + \*ika` | 8 |
| 25_class.md:418 | `kusalānaṃ \| noun \| masc.gen.pl \| wholesome` | Adjective qualifying `dhammānaṃ` (old A84) | `adj` | 9 |
| 25_class.md:538 | `\#veyaggha \| noun \| masc. \| tiger` | `veyaggha` is the derived adjective (line 547: `vyaggha + \*a`; DPD: "belonging to a tiger"); "tiger" is `vyaggha` (old A85) | `adj \| belonging to a tiger` | 8 |
| 25_class.md:522 | `**tevijjā + ka**` | DPD: `tevijja + ka`, adjective "related to the three Vedas"; row 514 tags `tevijjaka` as a noun, "master of three vedas" (old A86) | `tevijja + ka` (DPD); DPD has the word as an adjective, so check the `noun` tag at 514 | 7 |
| 25_class.md:168 | `**rūpa + \*iya<br>rūpiya + maya**` | `\*` marks a suffix that lengthens the first vowel; `rūpiya` and `jātijarāmaraṇiya` (240) show no lengthening and DPD writes `+ iya` for both (old A87) | `rūpa + iya`; `jātijarāmaraṇa + iya` (DPD) | 8 |
| 25_class.md:181–182 | `aveccappasādena \| noun \| masc.instr.sg \| with perfect clarity; absolute faith \| syntactical compound` / `\#avecca \| ind \| ger` | DPD: `kammadhāraya avecca + pasāda`, and `avecca` as `ind` (flagged IMPOSSIBLE). "syntactical compound" occurs only here (old A88) | owner decision | 6 |
| 26_class.md:63 | `**āsītikaṃ** \| adj \| masc.acc.sg \| eighty years old \| āsīti + ka` | The base is `asīti` and the suffix `\*ika`, as in the parallel `navuti + \*ika` two rows below (DPD: `asīti > āsīti + *ika`). Three parallel words, three notations (63, 65, 67) (old A89) | `asīti + \*ika` | 8 |
| 26_class.md:98 | `anatthasañhito \| adj \| masc.nom.sg \| unprofitable; unbeneficial \| kammadhāraya` | Member gloss is "connected with" (100); DPD: `tatiyā tappurisa anatthena + saṃhita` (old A90) | `tatiyā tappurisa` | 8 |
| 26_class.md:148 | `ekaputtaka \| sandhi \| \| only young son` | A compound tagged as sandhi (DPD: `digu eka + puttaka`); 152 is the real sandhi (`ekaputtakā'ti`) (old A91) | `noun \| masc.voc.sg \| … \| digu` | 9 |
| 26_class.md:168 | `\#sammanti \| verb \| pr.pass.3rd.pl \| is (lit: are) calmed; is (are) appeased \| √sam + ya + ti` | Singular ending for a plural form (old A92) | `√sam + ya + nti` | 9 |
| 26_class.md:260 | `\#\#sat \| ind \| \| good; right; true` | `sat` in `sappurisa` is an adjective, not an indeclinable; `\#\#purisaṃ \| noun \| masc.` (261) has an accusative ending with a stem tag (old A93) | `adj`; `\#\#purisa` (DPD: `sappurisa` = kammadhāraya `sat + purisa`; `sat` itself was not looked up: DPD lookup) | 7 |
| 26_class.md:350 | `\#sukhaṃ \| adj \| nt.nom.sg \| comfortable; at ease` | Predicate of a masculine first person (`avitakko'mhi … satimā`); a neuter nominative adjective does not agree (old A94) | `ind \| adv \| comfortably` (DPD: `sukhaṃ` ind, adv) | 8 |
| 26_class.md:380 | `**vipanna + diṭṭhi + ī (taddhita)**` | The word in the verse is `vipannadiṭṭhi` with short `i`, and DPD gives no suffix (`kammadhāraya > bahubbīhi vipanna + diṭṭhi`) (old A95) | Remove the line, or `vipanna + diṭṭhi` (DPD) | 8 |
| 26_class.md:535 | `diṭṭhapadassa \| noun \| masc.dat.sg \| for (one who has) seen the path \| dutiyā tappurisa` | Gloss "one who has seen the path" is a bahubbīhi; DPD: adj, `dutiyā tappurisa > bahubbīhi` (old A96) | `adj`; add `\> bahubbīhi` (DPD) | 8 |
| 26_class.md:120 | `**aññātikāya** \| adj \| fem.gen.sg \| of a not blood-related \| na + √ñā + ta + ka` | The construction is that of `aññātaka`; the feminine has `ikā` (DPD: `aññātaka + ikā`) (old A97) | `na + √ñā + ta + ka + ikā` (DPD: `aññātaka + ikā`) | 8 |
| 27_class.md:30 | `\#sat \| ind \| \| true; good` | `sat` in `sappurisa` is an adjective (see 26_class.md:260) (old A98) | `adj` (see 26_class.md:260; `sat` itself was not looked up: DPD lookup) | 7 |
| 27_class.md:121–122 | `attapaṭilābhassa \| noun \| masc.gen.sg \| of the acquisition of a self \| dutiyā tappurisa` / `\#attānaṃ \| noun \| masc.acc.sg \| a self` | Gloss "acquisition of a self" is genitive; DPD: `chaṭṭhī tappurisa attano + paṭilābha` (old A99) | `chaṭṭhī tappurisa`; `\#attano \| noun \| masc.gen.sg` | 8 |
| 27_class.md:130 | `vo \| ind \| emph \| indeed; surely` | DPD has `vo` only as the 2nd person plural pronoun; here "for you [who practise thus]". The translation (138) follows the particle reading: "surely" (old A100) | `pron \| 2nd.gen.pl \| of you; your` | 8 |
| 27_class.md:133 | `pahīyissanti \| verb \| fut.pass.3rd.pl \| will be abandoned \| pa + √hā + īya + ti` | Future plural analysed with neither `issa` nor `nti`; also 136 (`abhi + √vaḍḍh + a + ti`). Singular `ti` for plural presents at 172 (`gacchanti`) and 422 (`panudanti`) (old A101) | `pa + √hā + īya + issa + nti` etc. | 9 |
| 27_class.md:289 | `**ubbhatasmiṃ** \| pp \| nt.loc.sg (loc abs) \| when has been withdrawn; lifted up \| ud + √dhar + ta` | DPD: `ubbhata` is pp of `ud √bhar`, `ud + √bhar + ta` (old A102) | `ud + √bhar + ta` | 9 |
| 27_class.md:366 | `\#saññāvedayitassa \| noun \| masc.gen.sg \| of perception and feeling \| dvanda` | DPD: `saññāvedayita` is neuter (old A103) | `nt.gen.sg` | 8 |
| 27_class.md:392 | `\#āhacca \| adj (ptp) \| masc. \| removable; detachable (lit: to be carried away) \| ā + √han + tya` | Gloss and "lit: to be carried away" belong to `ā + √har`; DPD: `āhacca` "removable" is ptp of `āharati`, `ā + √har + tya` (`√han` gives "striking") (old A104) | `ā + √har + tya` | 9 |
| 27_class.md:410 | `gāth'**ābhigītaṃ** \| adj \| nt.acc.sg \| chanted over with verses; recited over \| tatiyā tappurisa` | In the first line it is the subject of `abhojaneyyaṃ` (`nt.nom.sg`, 414); accusative only in the third line (421) (old A105) | `nt.nom.sg` | 8 |
| 27_class.md:454 | `pāva \| verb \| perf.3rd.sg \| revealed, told of \| √vad + a + a` | The construction shows no source for the `pā-`; DPD: `pāv + a` (old A106) | `pāv + a` (DPD; root `√vad`) | 7 |
| 27_class.md:261 | `vīsatigaṇo \| noun \| masc.nom.sg \| group of twenty \| digu as bahubbīhi` | A bahubbīhi qualifying `bhikkhusaṅgho` tagged as a noun and glossed as one; DPD: adj, "with a quorum of twenty monks" (old A107) | `adj`; "with a quorum of twenty"; `digu \> bahubbīhi` (DPD) | 8 |
| 28_class.md:29 | `**maṅgalam'uttamaṃ** \| sandhi \| \| highest blessing \| kammadhāraya` | Two inflected words joined by sandhi (members 30–31 are both `nt.nom.sg`) given a compound type (old A108) | Remove the type | 8 |
| 28_class.md:68 | `pariyāpuṇanti \| verb \| pr.3rd.pl \| study well; learn thoroughly (lit: reach) \| pari + ā + √ap + uṇā + ti` | Singular ending `ti` for plural forms: 68, 90 (`pavanti`), 189 (`anumodanti`), 191 (`karonti`), 236 (`accayanti`), 394 (`enti`) (old A109) | `nti` | 9 |
| 28_class.md:73 | `**udānaṃ** \| noun \| nt.acc.sg \| inspired saying; exclamation \| ud + √an + \*a` | `udāna` is masculine in DPD (flagged IMPOSSIBLE) (old A110) | `masc.acc.sg` | 8 |
| 28_class.md:98 | `\#paṭhama \| ordin \| masc. \| first \| pa√ṭhā･1 a (stand)+ ma` | Derivation from `√ṭhā` in a mixed notation found nowhere else; DPD: `pa + tama > ṭhama` (no root) (old A111) | `pa + tama` | 8 |
| 28_class.md:318 | `pahīyetha \| verb \| opt.pass.3rd.sg \| decreases; is abandoned \| pa + √hā + īya + etha` | `-etha` is the reflexive 3rd sg ending (flagged IMPOSSIBLE without `reflx`; so tagged for `jāyetha`, 24_class.md:24); present-tense glosses for an optative (old A112) | `opt.pass.reflx.3rd.sg \| would be abandoned` | 8 |
| 28_class.md:432 | `niggahessāmi \| verb \| fut.1st.sg \| will restrain; will hold back \| ni + √gah + ṇhā + ssa + ssa + mi` | `ssa` twice, and `ṇhā` is not in the form; DPD: `ni + gahessa + ti` (old A113) | `ni + √gah + e + ssa + mi` | 9 |
| 28_class.md:448 | `aṭṭha**padakatā** \| sandhi \| \| arranged in eight parts; plaited eightfold \| dutiyā tappurisa` | A compound tagged as sandhi; DPD: adj, `kammadhāraya aṭṭhapada + kata` (old A114) | `adj \| masc.nom.pl`, type `kammadhāraya` (DPD: `aṭṭhapada + kata`) | 9 |
| 28_class.md:463 | `pāra**gavesino** \| adj \| masc.nom.pl \| seeking salvation; who is looking for the beyond; lit. seeking the far shore \| dutiyā tappurisa` | Parallel to `bālassa` ("enough for a fool's delusion, but not for one seeking the far shore"); the translation itself has "for those seeking". `gavesino` is dat/gen sg of `gavesī`; member 465 is `masc.nom.pl` too (old A115) | `masc.dat.sg`; verify | 7 |
| 28_class.md:41 | `**jarā** \| noun \| fem.abl.sg \| from old age \| √jar + ā` | The feminine ablative singular is `jarāya` (flagged IMPOSSIBLE); `yāva jarā` is a set phrase (old A116) | verify; note the form | 6 |
| 28_class.md:134 | `**bhante** \| noun \| masc.voc.sg \| Venerable sir \| √bhad + anta + e` | DPD derives `bhante` from `bhavant` (see 16_class.md:224) (old A117) | `√bhū`; `bhava + nta + e` (DPD: voc of `bhavant`) | 8 |
| 29_class.md:32 | `\#ragaṃ \| noun \| masc.acc.sg \| lust; passion (m.c. for rāgaṃ)` | The three accusatives are the names of Māra's daughters, as the translation (35) says; DPD: `ragā`, fem, "name of one of the three daughters of Death" (flagged IMPOSSIBLE as masc) (old A118) | `fem.acc.sg`; drop the m.c. note | 8 |
| 29_class.md:56 | `mutta-karīsa-puṇṇaṃ \| sandhi \| \| full of urine and excrement \| kammadhāraya` | A compound tagged as sandhi; hyphens added inside it (also in the verse, 19 and 48). DPD: adj, `chaṭṭhī tappurisa muttakarīsassa + puṇṇa` (old A119) | `muttakarīsapuṇṇaṃ \| adj \| nt.nom.sg`, type `chaṭṭhī tappurisa` (DPD: `muttakarīsassa + puṇṇa`) | 9 |
| 29_class.md:132 | `\#bhavūpapattiṃ \| noun \| fem.acc.sg \| rebirth (or re-arising) into existence \| kammadhāraya` | DPD: `dvanda bhava ca upapatti ca`, "state of being and rebirth" (old A120) | `dvanda`, "state of being and rebirth" (DPD: `bhava ca upapatti ca`) | 7 |
| 29_class.md:177 | `niccheyya \| verb \| ger \| evaluating; discriminating \| nis + √ci + \*ya` | Prefix `nis`; DPD: `nī + √ci`, and the key writes `nī` in `nissajja` (338) (old A121) | `nī + √ci + \*ya` (DPD) | 8 |
| 29_class.md:202 | `adassaṃ \| verb \| aor.1st.sg \| I saw \| a + √dis + a + ī` | The ending of `adassaṃ` is `aṃ`, not `ī` (flagged IMPOSSIBLE: DPD has it as reflexive aor 1st sg) (old A122) | `a + √dis + a + aṃ` | 8 |
| 29_class.md:231 | `te \| pron \| nt.acc.pl \| them` | `te` is masculine (it resumes `vinicchayā`, masc); the neuter is `tāni`. Same for `ete \| pron \| nt.acc.pl` at 336 (old A123) | `masc.acc.pl`; verify | 7 |
| 29_class.md:299 | `\#\#sīlā (+ca) \| noun \| nt.instr.sg \| virtue` | `sīlā` tagged instrumental; the same member is `\#\#sīla (+ca) \| noun \| nt.instr.sg \| by virtue` at 388 (stem with a case tag) and `\#sīla (ca) \| noun \| nt.` at 120 (old A124) | `\#\#sīlena (+ca)` in both | 9 |
| 29_class.md:441 | `paccenti \| verb \| pr.3rd.pl \| believe; assume \| pati + √i + a + ti` | Singular ending for a plural; also 872 (`vicaranti`). Line 833 has `nti` (old A125) | `nti` | 9 |
| 29_class.md:531 | `vivadetha \| verb \| opt.3rd.sg (+instr) \| might quarrel \| vi + √vad + a + etha` | `-etha` is the reflexive ending (flagged IMPOSSIBLE; also 590); see 28_class.md:318 (old A126) | `opt.reflx.3rd.sg` | 8 |
| 29_class.md:552 | `\#visesi \| adj \| masc.nom.sg \| superior` | Short `i`; `visesī` at 517 and in the verse (flagged IMPOSSIBLE) (old A127) | `\#visesī` | 9 |
| 29_class.md:769 | `\#vedaṃ \| noun \| nt.acc.sg \| knowledge; understanding` | `veda` is masculine in DPD (old A128) | `masc.acc.sg` | 8 |
| 29_class.md:476 | `\#āgā \| verb \| imperf.2nd.sg \| you have come \| ā +√gam +ā` | DPD knows `āgā` only as imperf 3rd sg (flagged IMPOSSIBLE); spaces missing in the construction. Same question for `n'āddakkhi \| verb \| aor.2nd.sg` (486), where the translation adds "(lit: he did not see)" (old A129) | verify; `ā + √gam + ā` | 6 |

## B. Tables, paradigms and lists that disagree with each other or themselves

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 16_class.md:701–702 | `\#dukkhaṃ \| noun \| nt.nom.sg \| suffering \| \|` / `\#idaṃ \| pron \| nt.nom.sg \| this \| √dukkh･1 a (be painful)` | Root is on the `idaṃ` row instead of the `dukkhaṃ` row (old B1) | Move the root one row up | 9 |
| 16_class.md:604 | `natthi \| sandhi \| \| is not \| √as･1 a (be)` | Root on the sandhi row, none on `\#atthi` (line 606); lines 532–534 do the opposite (old B2) | Root on `\#atthi` | 8 |
| 16_class.md:691 | `\#evaṃ \| ind \| emph \| thus` | `evaṃ` is `adv` at line 559 (old B3) | `adv` | 8 |
| 16_class.md:343 | `\#cattāro \| adj \| masc.nom.pl \| four` | Numerals are `card` at lines 137, 652, 738, 747 but `adj` at 343, 384, 389, 430 (old B4) | `card` throughout | 8 |
| 16_class.md:693 | `taṇh'ānusaye \| noun \| masc.loc.sg (loc.abs) \| when underlying tendency of craving \| kammadhāraya` | The same pattern is `chaṭṭhī tappurisa` at lines 813, 820, 827 (`rāgānusayānaṃ` …) (old B5) | `catutthī tappurisa` for every `X-anusaya` row (DPD: `taṇhānusaya`, `rāgānusaya`, `paṭighānusaya`, `diṭṭhānusaya`) | 8 |
| 16_class.md:655–656 | `brahmacariyaṃ \| noun \| nt.acc.sg \| the holy life; spiritual path \| \|` / `\#brahma \| adj \| nt` | Sub-rows but no compound type, and `brahma` is `nt` here, `masc` at lines 80 and 112 (where the type is `kammadhāraya`) (old B6) | add `kammadhāraya` (DPD: `brahma + cariya`); one treatment of `\#brahma` in all three places (DPD `brahma` 4 is an adjective: divine; holy) | 7 |
| 16_class.md:101–103 | `samma'd'eva \| sandhi` / `\#sammā` / `\#eva` | The inserted consonant `d` has no row, while the first table writes `sammā + [d] + akkhāto` (line 23). Same for `puna'r'eva` (686), `sāsapo'r'iva` (764), `ta'y'idaṃ` (296) (old B7) | owner decision: show `[d]`, `[r]`, `[y]` or not | 6 |
| 16_class.md:204 | `\#dhammaṃ \| adj \| nt.nom.sg \| nature` | Glossed as a noun but tagged `adj`; `\#dhammo \| noun` at line 283 in the same kind of compound (old B8) | `noun` (DPD: `dhamma` 1.01 masc, "nature; character") | 7 |
| 16_class.md:351 | `sambhavesīnaṃ \| noun \| masc.gen.pl \| for those seeking birth` | Tag genitive, gloss dative ("for") (old B9) | `masc.dat.pl`, or gloss "of those seeking birth"; verify | 6 |
| 17_class.md:468–469 | `lokañca \| - \| - \| the world and \| √lok･8 \*e (look)` / `\#lokaṃ \| noun \| masc.acc.sg \| world \| \|` | Root on the sandhi row, not on `\#lokaṃ`; column 2 is `-` instead of `sandhi` (old B10) | Move root; `sandhi` | 9 |
| 17_class.md:301 | `vihareyyan'ti` | Sentence has an apostrophe, the row (318) has `vihareyyanti` (old B11) | Same form in both | 9 |
| 17_class.md:477 | `\#loka \| noun \| masc \| world` | First member is the stem here, the genitive `\#lokassa` in the two neighbouring compounds (473, 481) (old B12) | `\#lokassa \| noun \| masc.gen.sg` | 8 |
| 17_class.md:87 | `\#evaṃ \| ind \| emph \| thus` | `evaṃ` is `emph` at 87, 125, 631 and `adv` at 53, 643 (old B13) | `adv` | 8 |
| 17_class.md:590 | `abyāpajjhena \| noun \| masc.instr.sg \| with good heartedness; benevolence; harmlessness` | In the sentence it qualifies `cetasā` like `averena` (line 587, `adj`). DPD has both the masculine noun (2.1, the key's gloss) and the adjective (2.2) (old B14) | `adj \| masc.instr.sg \| free from ill will` (DPD `abyāpajjha` 2.2); verify | 6 |
| 17_class.md:27 | `mahabbhayaṃ \| mahanta + bhayaṃ` | First member written `mahanta` here, `mahā` at lines 10 and 30 (old B15) | `mahā + bhayaṃ` (DPD: `mahā + bhaya`) | 8 |
| 17_class.md:166–168 | `tathārūpaṃ \| adj \| nt.acc.sg` / `\#rūpaṃ \| noun \| nt.acc.sg \| kind; type` | In `evarūpaṃ` (126) the same member is `adj \| fem.acc.sg \| of kind; of type` (old B16) | One treatment of the member `rūpa` in `tathārūpa` and `evarūpa`; `noun \| nt` fits (DPD types both as kammadhāraya with `rūpa`, and does not tag the member) | 7 |
| 17_class.md:442–443 | `tathā \| ind \| adv \| such` / `tathā \| ind \| adv \| such` | Repeated adverb split into two rows; `tato tato` at 646 is one `idiom` row (old B17) | One treatment; verify | 7 |
| 17_class.md:278–279 | `m'ānubyañjanaggāhī \| adj \| masc.nom.sg \| don't be [one] enticed by the details` / `\#mā \| ind \| neg` | Sandhi of `mā` + compound tagged as one adjective; the sandhi part and the compound members are mixed in one level of `\#` rows (old B18) | `sandhi` row, compound rows at `\#\#`; verify | 7 |
| 17_class.md:572 | `\#sabba \| pron \| masc.` | `\#sabba \| adj` at line 223 (old B19) | `pron` in both places (DPD: `sabba` pron) | 8 |
| 18_class.md:129–130 | `viharati \| verb \| pr.3rd.sg \| he dwells \| \|` / `appamāṇacetaso \| adj \| masc.nom.sg \| … \| √har･1 a (live)` | Root of `viharati` is one row too low (old B20) | Move it up | 9 |
| 18_class.md:362 | `seyyathā'pi gunnaṃ` | Sentence has the apostrophe three times, the rows (371, 377, 383) have `seyyathāpi` (old B21) | Same form in both | 9 |
| 18_class.md:134 | `\#cetaso \| adj \| masc.nom.sg \| having an immeasurable mind` | Member row carries the gloss of the whole compound; same at 494 (`\#soto \| adj \| masc.nom.sg \| with applied ear`) (old B22) | `noun … mind`; `noun … ear` | 8 |
| 18_class.md:122 | `byāpajjati \| verb \| pr.3rd.sg (+acc)` | The sentence construes it with the locative (`appiyarūpe rūpe`), like `adhimuccati … (+loc)` at 114 (old B23) | `(+loc)`, as the sentence has it; DPD lookup (the headword output gives no case) | 6 |
| 18_class.md:559 | `rājamahāmattānaṃ \| noun \| masc.gen.pl \| of the royal minister` | Plural tag, singular gloss (also 561 "of the chief minister"); translation "royal ministers" (old B24) | "of the royal ministers"; verify | 7 |
| 18_class.md:68 | `\#iti \| ind \| emph \| thus` | `iti` "thus" is `adv` at 92, 433, 512 (old B25) | `adv`; verify | 7 |
| 19_class.md:179 | `\#ti \| ind \| quotation mark \| ""` | Every other analysis writes `\#iti` (old B26) | `\#iti` | 9 |
| 19_class.md:575, 578 | `\#na \| prefix \| \| not` / `\#na \| ind \| neg \| not` | The negative member is `prefix` in `avitakkaṃ` and `ind \| neg` in `avicāraṃ` two rows below; also `ind \| neg` at 108, `prefix` at 90, 497 (old B27) | `prefix` | 9 |
| 19_class.md:220 | `vayadhammānupassī \| adj \| masc.nom.sg \| … \| \|` | Compound type missing; the parallel rows 213 and 227 have `dutiyā tappurisa` (old B28) | `dutiyā tappurisa` | 8 |
| 19_class.md:231 | `\#\#\#vaya (ca) \| noun \| masc \| decay \| √i･1 a (come, go)` | Root given here, empty for the same word at 221 (old B29) | Same in both | 8 |
| 19_class.md:109 | `\#āsavaṃ \| adj \| fem.acc.sg \| effluents; taints` | Member of `anāsavaṃ` is the noun `āsava` (masc), glossed as a noun but tagged `adj \| fem.acc.sg` (flagged impossible by the DPD check) (old B30) | `\#āsava \| noun \| masc` | 8 |
| 19_class.md:157, 162 | `\#ādhipateyyā \| adj \| masc.nom.pl \| authority; influence; power` / `\#uttarā \| noun \| masc.nom.pl \| higher; superior` | POS and gloss crossed: noun gloss tagged `adj`, adjective gloss tagged `noun` (old B31) | Swap the POS | 8 |
| 19_class.md:476 | `\#nidānaṃ \| adj \| nt.nom.sg \| background story; narrative setting` | Noun gloss (DPD `nidāna 4`, nt) tagged `adj` (old B32) | `noun` | 8 |
| 19_class.md:262 | `\#tathāgatena \| noun \| masc \| (by) Realised One; Buddha` | Inflected form with a stem tag; also 307, 399 (`\#samayaṃ \| noun \| masc`), 563 (`\#vitakkā [ca] \| noun \| masc.`). Items 1–6 tag such members fully (`\#saddhāya \| noun \| fem.instr.sg`, 141) (old B33) | `masc.instr.sg`, or the stem `tathāgata` | 8 |
| 19_class.md:263 | `\#pavedita \| pp \| -` | Items 7–13 and extra 6 give the last member as a bare stem with `-` (263, 272, 277, 282, 308, 315, 318, 407, 446, 449, 620, 623); items 1–6 and extras 1–5 give the inflected form (`\#pabbajitena \| pp \| masc.instr.sg`) (old B34) | One method | 8 |
| 19_class.md:484 | `√bhaj･1 a (divide)` | Root meaning shortened; `(divide, distribute)` at 452, 457. Also `√sukh･1 a (please)` 196 and `(be comfortable)` 585 vs `(please, be comfortable)`; `√kup･3 ya (shake)` 498 vs `(shake, be angry)` 367; `√muh･3 ya (be confused)` 525; `√tus･3 ya (be content)` 545 (old B35) | Full DPD root meaning | 8 |
| 19_class.md:89 | `avivādāya \| adj \| masc.dat.sg \| not quarrelling; harmony` | One of four parallel datives; the others are nouns (88, 92, 93). DPD: `avivāda` masc noun (old B36) | `noun` (DPD: `avivāda` masc) | 9 |
| 19_class.md:214–216 | `\#samudaya` / `\#dhamma` / `\#anupassī` | Three members at one level here and at 221–223; nested (`\#`, `\#\#`, `\#\#\#`) for the third compound (228–233) and in the analysis lines 240–252 (old B37) | Nest all three; verify | 7 |
| 19_class.md:584 | `\#pīti [ca] \| noun \| fem.acc.sg \| joy; delight [and]` | `pīti` is not an accusative form; class 20 line 228 tags the same member `fem.` (old B38) | `fem`; verify | 7 |
| 19_class.md:291 | `**atthaveda \< atthā + veda (pañcamī tappurisa)**` | Ablative written `atthā`, `dhammā` (293) here, `atthasmā`, `dhammasmā` in the table (271, 276) (old B39) | One form; verify | 6 |
| 19_class.md:26 | `aṭṭhiṃ + katvā \| aṭṭhiṃkatvā` | Written as two words in class 18 (`aṭṭhiṃ katvā \| idiom`, 18_class.md:484) (old B40) | one treatment: `aṭṭhiṃkatvā` as one word in class 18 as well (DPD headword: abs, comp vb) | 7 |
| 20_class.md:634 | `\#alamariya \| adj \| \| suitable for a noble person \| catutthī tappurisa` | The analysis line 657 says `alamariya \< alaṃ + ariya (kammadhāraya)`. DPD: `catutthī tappurisa > bahubbīhi` (old B41) | `catutthī tappurisa` in both | 9 |
| 20_class.md:382 | `… pāmojjaṃ jāyati, pamuditassa pīti jāyati, pītimanassa kāyo passambhati, passaddhakāyo sukhaṃ vedeti, sukhino cittaṃ samādhiyati.` | The exercise (`ipc_ex/20_class.md:209`) stops at `pāmojjaṃ jāyati`; the key analyses four more clauses (old B42) | Same sentence in both | 9 |
| 20_class.md:230 | `paṭhamaṃ \| adj \| nt.acc.sg \| first` | Ordinals are `ordin` at 521 and in class 19 (188, 586) (old B43) | `ordin` | 9 |
| 20_class.md:285 | `**vinayavādī \< vinaya + vādī (dutiyā tappurisa - bahubbīhi)**` | First member uninflected; the four parallel lines have `kālena`, `bhūtaṃ`, `atthaṃ`, `dhammaṃ` (old B44) | `vinayaṃ + vādī` | 8 |
| 20_class.md:441 | `**visuddhamatta \< visuddha + atta (kammadhāraya)**` | The table (392–394) treats `visuddhamattānaṃ` as a sandhi of two accusatives (`visuddhaṃ` + `attānaṃ`); same for `vimuttamatta` (443 vs 396–398) (old B45) | One analysis | 8 |
| 20_class.md:17 | `\#cittaṃ \| noun \| nt.nom.sg \| a mind` | Last member of `abyāpannacitto`; in `byāpannacitto` (166) it is `\#citto \| noun \| masc.nom.sg` (old B46) | One form | 8 |
| 20_class.md:108 | `rāgadosā \| adj \| fem.nom.sg \| … \| kammadhāraya` | Same structure as `tiṇadosāni` (104), which is `kammadhāraya \> bahubbīhi` (old B47) | `kammadhāraya \> bahubbīhi` | 8 |
| 20_class.md:257 | `\#vādī \| adj \| \| who speaks` | Grammar cell empty; `masc.nom.sg` at 251, 254, 260, 263. Compound type given only for `kālavādī` (249), not for 252, 255, 258, 261 (old B48) | Fill | 8 |
| 20_class.md:369 | `\#mattena \| adj \| masc. \| by the fact of` | Inflected member with a stem tag, and `masc` although the compound (365) is `nt.instr.sg` (old B49) | `nt.instr.sg` | 8 |
| 20_class.md:388 | `imehi \| adj \| masc.abl.pl \| from these` | `ima` is `pron` everywhere else (old B50) | `pron` | 8 |
| 20_class.md:540–542 | `n'ādhimuccati \| verb \| pr.3rd.sg (+loc) \| … \| na+adhi√muc･2 ya (release, free)` / `\#adhimuccati \| verb \| pr.3rd.sg \| … \| \|` | Sandhi row tagged `verb`, with the root (including `na+`) on it and none on `\#adhimuccati`; class 18 line 112 has `sandhi` and the root on the sub-row (old B51) | As in class 18 | 8 |
| 20_class.md:511, 514 | `\#\#na \| ind \| neg \| not` / `\#\#na \| prefix \| \| not` | Negative member `ind \| neg` in `adukkhaṃ` and `prefix` in `asukhaṃ` three rows below; `prefix` at 15, `ind \| neg` at 143, 575 (old B52) | `prefix` | 9 |
| 20_class.md:86 | `yathādhammaṃ \| adj \| nt.acc.sg \| fairly; correctly (lit: according to the law) \| abyayībhāva[^17]` | Other abyayībhāva rows are `ind \| adv` (34, 58, 192, 327); DPD `ind, adv` (old B53) | `ind \| adv` (DPD: ind, adv, abyayībhāva) | 9 |
| 20_class.md:86, 183 | `abyayībhāva[^17]` / `[^17]: So also Ñāṇatusita, but puna(r) is an ind.` | The first sentence of the footnote is about `punakammāya` (line 92), but the marker is on `yathādhammaṃ` (old B54) | Move the marker, or split the note; verify | 6 |
| 20_class.md:465 | `udakorohakā \| noun \| masc.nom.pl \| bather; ritual bather; lit. who descends into water` | Singular gloss for a plural; `noun` while the four parallel words (455–462) are `adj`; 462 "who looks after" also singular; 576 "one for whom there are clothes" (old B55) | Plural glosses ("bathers"); `noun` agrees with DPD (masc, agent), so the POS can stay | 7 |
| 20_class.md:545, 551 | `kos'ohite \| adj \| masc.loc.sg` / `\#guyhe \| ptp \| masc.loc.sg` | Both belong to `vatthaguyhe`, tagged `nt.loc.sg` (549) (old B56) | `nt.loc.sg` (DPD: `vatthaguyha` nt) | 8 |
| 20_class.md:437 | `samādhiyati \| verb \| pr.3rd.sg \| becomes composed, settled \| √dhā･1 iya` | Passive (root sign `iya`) not marked, unlike `pahīyissati \| pass.fut.3rd.sg` (372) (old B57) | `pass.pr.3rd.sg` (DPD: pass of `samādahati`) | 8 |
| 20_class.md:227 | `pītisukhaṃ \| noun \| nt.acc.sg \| joy and happiness \| dvanda \> bahubbīhi` | Plain `dvanda` for the same word in the same formula at 19_class.md:583 (old B58) | `dvanda` (DPD: the noun is `dvanda`; `dvanda > bahubbīhi` is the adjective) | 8 |
| 20_class.md:625 | `natthi \| verb \| pr.3rd.sg \| there is not` | Split as sandhi `na + atthi` in class 16 (532, 604) (old B59) | One treatment; verify | 7 |
| 21_class.md:132 | `\#ti \| ind \| quotation mark \| ""` | `\#ti` instead of `\#iti` here, at 146 and 501; `\#iti` at 203, 329 (old B60) | `\#iti` | 9 |
| 21_class.md:136, 144 | `sikkhassū"ti` / `sikkhassū'ti \| sandhi` | Sentence has `"`, the row has `'` (old B61) | Same in both | 9 |
| 21_class.md:184, 196 | `sataṃ saddhammamaññāya` / `saddhammam'aññāya \| sandhi` | Row has an apostrophe, the sentence has none (old B62) | Same in both | 9 |
| 21_class.md:232–233 | `maccurājassa \| … \| √mar･1 a (die)<br>chaṭṭhī tappurisa` / `\#maccuno \| noun \| masc.gen.sg \| of death \| \|` | Root of `maccu` on the compound row together with the type; at 169–170 the root is on `\#maccuno` (old B63) | Root on the sub-row | 9 |
| 21_class.md:49–50 | `khaṇ'ātītā \| noun \| masc.nom.pl \| … \| kammadhāraya\> bahubbīhi` / `\#khaṇaṃ \| noun \| masc.acc.sg` | An accusative first member means `dutiyā tappurisa`, not `kammadhāraya`; space missing before `\>` (old B64) | `dutiyā tappurisa \> bahubbīhi` | 8 |
| 21_class.md:89–90 | `\#sīla (ca) \| noun \| nt.nom.pl` / `\#vatāni (ca) \| noun \| nt.nom.pl` | Compound (88) is `nt.acc.pl`; `sīla` is a stem tagged nom.pl (old B65) | `\#sīla \| noun \| nt`; `\#vatāni \| nt.acc.pl` | 8 |
| 21_class.md:235 | `gacche'ti \| verb \| opt.3rd.sg \| he could go` | Sandhi with `iti` tagged as a verb, no sub-rows; also 294 (`bhāvethā'ti`), 388 (`samajjhagā'ti`). Split at 201–203, 327–329 (old B66) | `sandhi` + sub-rows | 8 |
| 21_class.md:361 | `tayo \| adj \| masc.acc.pl \| three` | Numerals `adj` here, 365, 399; `card` in class 20 (old B67) | `card` | 8 |
| 21_class.md:378 | `samūhataṃ \| pp \| nt.acc.sg` | Qualifies `rajaṃ`, tagged `masc.acc.sg` (377); class 17 line 611 has `masc.acc.sg` (old B68) | `masc.acc.sg` | 8 |
| 21_class.md:402 | `tatreko \| adj \| masc.nom.sg \| there one` | Sandhi (`tatra + eko`) tagged `adj`; also 257 (`nāññamaññassa \| pron`), 385 (`idheva \| ind`), 418 (`nappaṭiggaṇhāti \| verb`), 526 (`natthī \| verb`) (old B69) | `sandhi` | 8 |
| 21_class.md:316 | `paraṃ \| adj \| masc.acc.sg \| another` | `paraṃ \| pron` at 245 (old B70) | `pron` (DPD `para` 1: other; another (person)) | 8 |
| 21_class.md:457 | `\#dīgham \| adj \| nt.acc.sg \| long` | Final `m` instead of `ṃ` (sandhi form kept in the analysis) (old B71) | `\#dīghaṃ` | 8 |
| 21_class.md:482–484 | `vippariṇāmadhammaṃ \| adj \| nt.acc.sg \| … \| kammadhāraya` / `\#dhammaṃ \| noun \| masc.acc.sg` | Same compound is `kammadhāraya > bahubbīhi` with `\#dhammaṃ \| adj \| nt.nom.sg` at 16_class.md:202–204 (there spelt `vipariṇāma-`) (old B72) | `kammadhāraya > bahubbīhi` in both classes (DPD, for both spellings `vipariṇāma-` and `vippariṇāma-`); `\#dhamma` as `noun` in both | 8 |
| 21_class.md:527 | `paramuggahītaṃ \| - \| - \| grasped as supreme` | Compound row with no pos, no grammar and no compound type; the case sits on the sub-row only. DPD: adj, pañcamī tappurisa (old B73) | `adj \| nt.nom.sg \| … \| pañcamī tappurisa` | 8 |
| 22_class.md:43, 50 | `\#maññitaṃ \| pp (as noun) \| nt.nom.sg` / `\#maññitaṃ \| noun \| nt.nom.sg` | Same word in the same sentence: `pp (as noun)` at 43, `noun` at 50 and 56 (old B74) | `pp (as noun)` | 9 |
| 22_class.md:45 | `ayam'aham'asmī'ti \| sandhi \| \| "this I am"` | Sub-rows give `ayaṃ`, `ahaṃ`, `asmi` but no `\#iti` row; the other three quotations have one (40, 54, 61) (old B75) | Add `\#iti` | 9 |
| 22_class.md:110 | `dukkham'addakkhu \| sandhi \| adj + nt \| saw discomfort; saw suffering` | Grammar cell `adj + nt` on a sandhi row whose members are tagged noun and verb (111–112). Other sandhi rows with a filled grammar cell: 19 `interr`, 119 `adv + aor`, 279 `masc.nom.sg`, 466 `pp + prp`, 477 `2nd.nom.pl` (blank at 490, 531); the rest are blank (old B76) | Blank | 8 |
| 22_class.md:122, 126 | `sammādiṭṭhisamādānā \| adj \| masc.nom.pl \| who have undertaken right view \| dutiyā tappurisa` / `\#samādānā \| noun \| nt.nom.pl[^26]` | Adjective masc.nom.pl whose head member is a neuter noun, so the type needs the bahubbīhi step (DPD: `dutiyā tappurisa > bahubbīhi`; the key writes it that way at 139 and 250). Footnote marker sits in the grammar cell (old B77) | Add `\> bahubbīhi` | 8 |
| 22_class.md:127 | `sabbaṃ \| pron or ind \| nt.acc.sg \| all <br>entirely; completely` | Two readings in one row; the grammar cell fits only the pronoun. The translation uses "all suffering" (old B78) | One reading, or two rows; verify | 7 |
| 22_class.md:166–168 | `tattha tattha \| idiom \| \| right there; here and now` / `tattha \| ind \| adv \| there` | The two member rows have no `\#`; member rows of `evameva kho \| idiom` (526–528) have it (old B79) | `\#tattha` | 8 |
| 22_class.md:170–171 | `asaṃhiraṃ \| ptp \| masc.acc.sg` / `asaṅkuppaṃ \| adj \| masc.acc.sg \| immovable; steady` | Parallel formations tagged differently; DPD has `asaṅkuppa` as ptp of `na saṃkuppati` (`√kup`). Root cell blank (old B80) | `ptp`; add `√kup` (DPD: ptp of `na saṃkuppati`) | 8 |
| 22_class.md:25 | `paridevaneyye \| adj (ptp) \| masc.acc.pl \| sorrowful; lamentable` | Root cell blank for a word with a DPD root (`√dev`). Also blank: `nindaṃ` 147 (`√nind`), `anupadajjeyya` 434 (`√dā` given at 423), `etha` 476, `\#gāho` 561 (`√gah` given at 551, 556), `brahmacariyaṃ` 294 (type given at 257) (old B81) | Fill | 8 |
| 22_class.md:241–244 | `attabhāvapaṭilābho \| noun \| masc.nom.sg \| personal existence` / `\#attabhāvaṃ \| noun \| masc. \|` | Type cell blank (DPD: chaṭṭhī tappurisa `attabhāvassa + paṭilābha`). Members `\#attabhāvaṃ`, `\#\#bhāvaṃ` (244) and `\#\#uṭṭhānaṃ \| noun \| nt.` (510) carry an accusative ending with a stem-only tag (old B82) | `chaṭṭhī tappurisa`; `\#attabhāvassa \| noun \| masc.gen.sg` | 8 |
| 22_class.md:255 | `\#idaṃ \| pron \| nt.acc.sg \| this` | Inside `nayidaṃ`, with a masculine nominative subject (`brahmacariyavāso`). The same `nayidaṃ` at 317 has `\#idaṃ \| ind \| adv \| here; in this case` (old B83) | As at 317 | 8 |
| 22_class.md:261 | `paññāyetha \| verb \| pass.opt.reflx.3rd.sg \| would be evident` | Three notations for the same form: `verb \| pass.opt.reflx.3rd.sg` (261, and `labbhetha` 321), `verb \| opt.reflx.3rd.sg` (357), `verb. pass \| opt.reflx.3rd.sg` (596) (old B84) | One notation | 9 |
| 22_class.md:291 | `evamidaṃ \| pron \| nt.nom.sg \| thus this` | A sandhi row with sub-rows tagged as a pronoun (flagged IMPOSSIBLE) (old B85) | `sandhi`, grammar blank | 9 |
| 22_class.md:331 | `mā ahesun'ti \| verb \| aor.3rd.pl \| may they not be` | `mā`, `ahesuṃ` and `iti` merged in one row tagged as a verb; elsewhere `mā` has its own row and `…'ti` is a sandhi row with sub-rows (old B86) | Split | 9 |
| 22_class.md:420–421 | `\#kiñci \| pron \| masc \| anything; something; some` / `\#mattaṃ \| noun \| masc.acc.sg \| amount; measure` | The same compound twelve rows below (432–433) has `\#kiñci \| ind \| \|` and `\#mattaṃ \| adj \| masc.acc.sg`. The compound is `nt.acc.sg` in both places, its member `masc.acc.sg` (old B87) | One analysis; `nt.acc.sg` | 9 |
| 22_class.md:437, 441 | `\#piṇḍapātamattaṃ \| noun \| masc.acc.sg \| morsel of alms food \| chaṭṭhī tappurisa` / `\#\#mattaṃ \| adj \| masc.acc.sg \| mere; simple` | Type and gloss treat `matta` as a noun ("morsel of"); the member row is an adjective "mere". Masculine here, while `kiñcimattaṃ` is neuter (419) (old B88) | `kammadhāraya`, "mere alms food" (DPD: `piṇḍapāta + matta`, masc); the member row `mere` then fits | 8 |
| 22_class.md:494 | `appābādhatañ'ca \| noun \| fem.acc.sg \| good health and` | Sandhi rows with `ca` tagged as nouns: 494, 501, 507 (gloss without "and"), 512 `balañ'ca` (no sub-rows, root in the row), 513 `phāsuvihārañ'cā'ti`. Compare `paccuppannañ'ca \| sandhi` at 161 (old B89) | `sandhi`; sub-rows for 512 | 8 |
| 22_class.md:571, 575 | `\#ninnā \| adj \| masc.nom.pl` / `\#poṇā \| noun \| masc.nom.pl \| slanting; inclining to` | Three parallel members: `ninnā` adj, `poṇā` and `pabbhārā` (578) noun. DPD has all three as adjectives in this sense (old B90) | `adj` | 8 |
| 22_class.md:595 | `nayidha \| ind \| - \| not here` | Same sandhi at 349 is `nayidha \| sandhi` with `\#na` and `\#idha` (old B91) | As at 349 | 9 |
| 22_class.md:622 | `ajeḷakā \| noun \| masc.nom.pl \| goats and sheep` | No `dvanda` label and no member rows; the two compounds beside it (623, 626) have both. DPD: `ajeḷaka` nt, dvanda `aja ca eḷaka ca` (old B92) | Add `dvanda` and the member rows (`aja`, `eḷaka`); DPD has the compound as nt: `nt.nom.pl` | 7 |
| 23_class.md:47 | `**Please pay attention to the syntax: underline the subject, object(s), and predicate of the sentences**` | The key repeats the instruction but marks no subject, object or predicate anywhere; bold marks the prefixed words instead. No final full stop (27 has one) (old B93) | owner decision | 6 |
| 23_class.md:156 | `sam'atthi \| sandhi \| \| there is equal (to); there is comparable (to) +instr` | Case note `+instr` inside the gloss cell; elsewhere it is `(+instr)` in the grammar cell (245) (old B94) | Move | 8 |
| 23_class.md:199 | `\#kicco \| noun (ptp) \| masc.nom.sg \| obligation (for); duty (for); work (for)` | Neuter member nouns given the compound's masculine ending: `kicco` here, `\#indriyo \| noun \| masc.nom.sg \| senses; mental faculties` at 206 (plural gloss too). `\#vutti \| noun \| fem.nom.sg` (203) and `\#sotaṃ` (355) keep their own gender (old B95) | One treatment | 8 |
| 23_class.md:201 | `**sallahuka**vutti \| adj \| masc.nom.sg (fem?) \| of frugal livelihood; living lightly` | Editorial query left in the grammar cell (old B96) | `masc.nom.sg` | 9 |
| 23_class.md:281 | `gihippaṭisaṃyuttan'ti \| adj \| nt.acc.sg \| (offences) concerning lay people \| tatiyā tappurisa` | Sandhi with `iti` tagged as an adjective although it has an `\#iti` sub-row (284) (old B97) | `sandhi`; tag and type on `\#gihippaṭisaṃyuttaṃ` | 8 |
| 23_class.md:286 | `**adhi + √kar + aṇa**` | In items 9–15 and extras 9–11 the constructions stand as bold lines under the table without naming the word they analyse; identical lines repeat (292 = 294) (old B98) | Name the word; verify | 7 |
| 23_class.md:316, 320 | `jhāyinomhā \| verb \| pr.1st.pl \| we are meditators` / `\#jhāyinomhā \| verb \| pr.1st.pl \| we are meditators` | Sandhi of a noun and a verb tagged as a verb (flagged IMPOSSIBLE), twice (old B99) | `sandhi`, grammar blank | 9 |
| 23_class.md:343 | `yodha \| ind \| - \| whoever here` | Unsplit sandhi rows tagged as single words: `yodha` (343), `nājjheti \| verb` (352), `tamenaṃ \| pron` (778, has sub-rows), `assādañca \| noun` (880, also 884, 888), `nābbhaññāsiṃ \| verb` (895), `tāvāhaṃ \| pron` (899, has sub-rows) (old B100) | `sandhi` with sub-rows | 9 |
| 23_class.md:431–433 | `abhijjhādomanassā \| noun \| masc.nom.pl \| covetousness and grief \| dvanda` / `\#domanassā (+ca) \| noun \| nt. \| grief, distress` | Member carries the plural ending of the compound with a stem-only tag (old B101) | `\#domanassa (+ca)`; verify | 7 |
| 23_class.md:532–536 | `attabyābādhāyapi \| noun \| masc.dat.sg \| hurting oneself, harm to oneself` / `attabyābādhāya \| noun \| masc.dat.sg` | Sandhi row tagged as a noun (flagged IMPOSSIBLE); its first member has no `\#`, the compound members have one `\#` instead of two, and `\#api` follows them. Same structure at 793–797 (`antaguṇampi`) (old B102) | `sandhi`; `\#attabyābādhāya`; `\#\#attano`, `\#\#byābādhāya`; `\#api` | 9 |
| 23_class.md:661 | `ariyasāvako \| noun \| masc.nom.sg \| a noble disciple \| chaṭṭhī tappurisa<br>(or)<br>kammadhāraya` | Two types here, one (`chaṭṭhī tappurisa`) for the same word at 101; the member rows fit the tappurisa only. `<br>` in the type cell (old B103) | One treatment | 8 |
| 23_class.md:812 | `10. [MN107](https://s.dhamma.gift/mn/mn107/index.html) <br>cakkhunā rūpaṃ disvā mā nimittaggāhino ahuvattha` | Extra example 10 (812–863) repeats exercise item 13 (406–457) word for word: sentence, table, constructions, translation. The exercise file has it twice as well (ex 267, 530) (old B104) | owner decision: replace or remove | 9 |
| 23_class.md:764, 784 | `gahetvā sahasā asaṅkhāditvā ajjhohari` / `asaṅkhāditvā \| verb \| abs \| having not chewed; without having chewed` | The exercise (ex 504) has `**saṅkhāditvā**`, the opposite meaning ("having chewed"). The key row and translation follow `asaṅkhāditvā`. DPD has both headwords (old B156) | verify the reading in the source edition; same word in key and exercise | 8 |
| 23_class.md:49 | `so navaṃ santh'āgāraṃ **pavisati**, saddhiṃ mahesiyā brāhmaṇena ca **purohitena**.` | The exercise (ex 51) gives the long sentence (`so puratthimena nagarassa navaṃ santhāgāraṃ kārāpetvā kesamassuṃ **ohāretvā** kharājinaṃ **nivāsetvā** …`) with three more bold target verbs; the key analyses only this shortened sentence, so about 15 exercise words have no key (old B158) | Same sentence in both | 9 |
| 23_class.md:163; 26_class.md:59 | `(passati) dukkhaṃ dukkha**samuppādaṃ**` / `(addasa) **āsītikaṃ** vā **nāvutikaṃ** vā` | The key adds a supplied verb in brackets to the Pāli sentence; the exercise (ex 127, ex 50) does not have it, and it has no table row (old B159) | owner decision: in both, or in the translation only | 7 |
| 24_class.md:44 | `kumbh'ūpamaṃ \| adj \| masc.acc.sg \| like a clay pot \| kammadhāraya` | Adjective compounds typed without the bahubbīhi step: 44, 51 (DPD: `kammadhāraya > bahubbīhi`); with it elsewhere in the key. `(as bahubbīhi)` at 354 is a third notation (old B105) | `kammadhāraya \> bahubbīhi` (DPD: `kumbhūpama`, `nagarūpama`) | 8 |
| 24_class.md:103 | `anaññātaññassāmī't'indriyaṃ \| sandhi \| nt.nom.sg \| the faculty that senses "I will know the unknown" \| kammadhāraya` | Sandhi row carrying grammar and a compound type (old B106) | Blank; or tag as noun; verify | 7 |
| 24_class.md:124 | `**santadassāvī** \| adj \| masc.nom.sg \| who sees peace (in) +loc \| dutiyā tappurisa` | `+loc` in the gloss cell (see 23_class.md:156); "who sees" here, "who has seen" at 126 and in the translation (old B107) | `masc.nom.sg (+loc)` | 8 |
| 24_class.md:159, 161 | `khādanīyaṃ \| ptp \| nt.acc.sg \| uncooked food; food to be chewed` / `bhojanīyaṃ \| noun \| nt.acc.sg \| cooked food (lit: to be savored)` | Parallel words, `ptp` and `noun` (old B108) | One tag | 8 |
| 24_class.md:196 | `vihāra-samāpattīnaṃ \| noun \| fem.gen.pl \| of meditation attainments` | Hyphen added to the compound (sentence: `vihārasamāpattīnaṃ`); no type, no member rows. Unsplit sandhi rows around it: `imāsañ'ca \| pron` (194, 195), `lābhino'ti \| noun` (198) (old B109) | No hyphen; split | 9 |
| 24_class.md:226, 234 | `kiṃsu \| pron \| nt.acc.sg \| what?` / `kissassu \| - \| - \| of which?` | `kiṃsu` as a pronoun (flagged IMPOSSIBLE; DPD: `ind`), unsplit; `kiṃ'sū` at 22_class.md:9 is a sandhi with `\#kiṃ` and `\#sū`. `kissassu` has sub-rows but `-` for pos (old B110) | `sandhi` in both | 8 |
| 24_class.md:315 | `seyyathāpi \| ind \| - \| just like` | `ind` here; `sandhi` with `\#se`, `\#yathā`, `\#api` at 488 and 546. Other unsplit sandhi rows: `n'eva \| ind` (357, 406), `yathāyaṃ \| ind` (281, with sub-rows), `c'āhāro \| noun` (581; `cāhāro` at 600), `cā'ti \| ind` (453), `chandañ'ca \| noun` and six more (335–341), `purāṇañ'ca \| adj` (432, 435) (old B111) | `sandhi` with sub-rows | 9 |
| 24_class.md:381–383 | `ājānissāmā'ti \| verb \| fut.1st.pl \| we will learn, understand \| ā + jānā + ti` / `\#ājānissāma \| verb \| fut.1st.pl` | Sandhi row tagged as a verb and carrying the construction; the member row has none (old B112) | `sandhi`; construction on `\#ājānissāma` | 9 |
| 24_class.md:387, 450 | `yātrā ca no bhavissati anavajjatā ca phāsu vihāro cā'ti` / `phāsuvihāro \| noun \| masc.nom.sg` | Two words in the sentence, one compound in the table (no type given; `kammadhāraya` at 22_class.md:514) (old B113) | `phāsuvihāro` | 9 |
| 24_class.md:551, 553 | `purisassa \| noun \| masc.gen[^35].sg \| to a person (by a person)` / `adiṭṭhapubbo \| adj \| masc.nom.sg (+dat) \| never seen before` | 551 and footnote 35 call the case a (subjective) genitive; 553 says `(+dat)` (old B114) | `(+gen)` | 8 |
| 24_class.md:559, 565 | `\#yena \| pron \| masc.instr.sg \| by which` / `\#tena \| ind \| adv \| there` | The two halves of `yena … tena` tagged differently; sandhi gloss (558) is "where a certain" (old B115) | `ind \| adv \| where` | 8 |
| 24_class.md:602–605 | `asaddhammassavanantissa \| sandhi \| \| "not hearing the pure teaching"` / `\#saddhamma \| noun \| masc \| true, good teaching` | Compound members stand directly under the sandhi row with no compound row; "pure" in the sandhi gloss, "true, good" in the member, "true" in the translation (old B116) | Add `\#asaddhammassavanaṃ`; one rendering; verify | 7 |
| 25_class.md:71 | `\#bahujanassa \| adj \| masc.dat.sg \| to/for many people \| kammadhāraya` | A noun compound tagged `adj` (71, 76). Gloss "to/for the people" at 76 and "charming to the people" at 75 drop "many" (old B117) | `noun`; "to many people" | 8 |
| 25_class.md:79 | `manāpā \| adj \| fem.nom.sg \| pleasant; likeable` | Second member of `bahujanamanāpā` without `\#` (compare `\#kantā`, 74) (old B118) | `\#manāpā` | 9 |
| 25_class.md:80 | `tathārūpiṃ \| adj \| fem.acc.sg \| such; such kind \| kammadhāraya` | The same compound is `kammadhāraya \> bahubbīhi` at 113 (so DPD for this sense) (old B119) | `kammadhāraya \> bahubbīhi` | 8 |
| 25_class.md:213 | `samitāssa \| - \| - \| calmed his` | Sandhi row with `-` for pos (sentence: `samit'āssa`). Other sandhi rows tagged as words: `sikkhassū'ti \| verb` (255), `sūcivāṇijako'ti \| noun` (308), `evam'eva kho \| ind` (349), `tumhe'pi \| pron` (352) (old B120) | `sandhi` with sub-rows | 9 |
| 25_class.md:292 | `etad'avoca \| pron+verb \| aor.3rd.sg \| he said this \| sandhi` | `sandhi` in the last column and `pron+verb` as pos; no sub-rows (old B121) | `etad'avoca \| sandhi`; `\#etaṃ`, `\#avoca` | 9 |
| 25_class.md:331 | `dhammadāy'ādā \| noun \| masc.nom.pl \| inheritors of the Dhamma \| chaṭṭhī tappurisa` | Apostrophe inside the word in the table (331, 337), none in the sentence (314) (old B122) | `dhammadāyādā` | 9 |
| 25_class.md:345 | `13. [SN35.241](https://s.dhamma.gift/sn/sn35/index.html#sn35.241) <br>evam'eva kho, bhikkhave, sace tumhe'pi na orimaṃ tīraṃ upagacchatha` | The same sentence is analysed at 22_class.md:522–547 with other tags: `evameva kho \| idiom` with sub-rows (here `ind`), `tumhepi \| sandhi` (here `pron`), `majjhe \| adj` (here `noun`, 362); "veer to" at 356, "veer towards" at 360 (old B123) | Align the two | 8 |
| 25_class.md:420 | `pubbarattā'pararattaṃ \| sandhi \| adv \|` | Apostrophe after `ā` in the table, before it in the sentence (`pubbaratt'āpararattaṃ`, 402); `\#bhāvanā'nuyogam` (432) ends in `m`, the other members in `ṃ` (old B124) | `pubbaratt'āpararattaṃ` | 9 |
| 25_class.md:502–507 | `aho \| ind \| excl \| I say! Oh!` / `aho vata re \| ind \| excl \| oh!` | Three rows for the first `aho vata re`, one merged row for the second and third (507, 512) (old B125) | One treatment; verify | 7 |
| 26_class.md:75 | `daṇḍaparāyaṇaṃ \| adj \| \| leaning on a stick; supported by a staff \| sattamī tappurisa` | Grammar cell empty for a declined word; also 91 (`atta**kilamath**'ānuyogo \| noun \| \|`) (old B126) | `masc.acc.sg`; `masc.nom.sg` | 9 |
| 26_class.md:92 | `\#atta**kilamath**assa \| noun \| masc.gen.sg \| self-mortification \| dutiyā tappurisa` | `kilamath` is bold as the target derivative, but no construction is given for it anywhere in the item (DPD: `kilama + tha`) (old B127) | Add `kilama + tha` | 8 |
| 26_class.md:174 | `eso \| pron \| masc.nom.sg \| this` | The sentence (159) has `esa dhammo` (old B128) | `esa` | 9 |
| 26_class.md:191 | `ottappiyaṃ \| noun \| nt.nom.sg \| fear of wrongdoing` | Secondary derivatives left without bold or construction although the task is to find all of them: `ottappiyaṃ` (191), `pārivattakā` (126), `upanāhī` (363), `thenakehi` (506), `dukkhito` (216) (old B129) | Add or state the selection; verify | 6 |
| 26_class.md:224 | `nacchādesi \| verb \| aor.3rd.sg \| it did not please` | Unsplit sandhi rows tagged as words: `nacchādesi` (224), `ajjatanām'iva \| adj` (286, has sub-rows), `natthi \| verb` (303), `cā'ti \| ind` (329), `muhuttam'pi \| ind` (398), `seyyathāpi \| ind` (493), `kiñ'c'āpi \| ind` (520), `idam'pi \| pron` (539) (old B130) | `sandhi` with sub-rows | 9 |
| 26_class.md:294, 298 | `bahubhāṇinaṃ \| adj \| masc.acc.sg \| who talks a lot \| kammadhāraya` / `\#mitabhāṇiṃ \| adj \| masc.acc.sg \| one who talks in measure \| dutiyā tappurisa` | Parallel compounds typed differently (DPD: kammadhāraya for both, with `> bahubbīhi` for the first); `\#bhāṇinaṃ` (296) and `\#\#bhāṇiṃ` (300) for the same stem (old B131) | One type | 8 |
| 26_class.md:325 | `khamati \| verb \| pr.3rd.sg \| seems good (+dat)` | Case notes in the gloss cell: 325, 401 (`(+abl)`), 432 (`(+loc)`), 530 (`(+inf or +dat)`); in the grammar cell at 24, 33, 122, 125 (old B132) | Grammar cell | 8 |
| 26_class.md:349 | `sukhamasmī'ti \| sandhi \| \| I am comfortable, at ease ""` | Sandhi with `iti` and no `\#iti` sub-row; the `""` is in the sandhi gloss instead (old B133) | Add `\#iti` | 8 |
| 26_class.md:426 | `sāṭheyyāni \| noun \| nt.nom.pl \| treachery \| \|` | First of four parallel `-eyya` derivatives; the other three are marked `taddhita` and have a construction line (440–444), this one has neither (old B134) | `taddhita`; `saṭha + \*eyya` | 9 |
| 26_class.md:455 | `\#ambilaggehi \| adj \| masc.instr/abl.pl \| predominantly sour \| kammadhāraya` | Four parallel compounds: the first is `instr/abl` and not bold, the others `instr` and bold (460, 465, 470); the third has no type (465) (old B135) | Align | 8 |
| 27_class.md:86–87 | `**pānīyaṃ** \| noun (ptp) \| nt.acc.sg \| the drinking water (lit: to be drunk)` / `**paribhojanīyaṃ** \| adj (ptp) \| nt.acc.sg \| rinsing water (lit: to be used)` | Parallel nouns, `noun (ptp)` and `adj (ptp)`; `phoṭṭhabbā \| noun (ptp)` at 328, `gārayhā \| adj (ptp)` at 277 (old B136) | `noun (ptp)` | 8 |
| 27_class.md:104–106 | `ekam'antaṃ \| sandhi \| \| to one side` / `\#eka \| card \| masc. \| one` | The first member of the sandhi is the inflected `ekaṃ`, given as a stem with a stem tag (old B137) | `\#ekaṃ \| adj \| masc.acc.sg`; verify | 7 |
| 27_class.md:166 | `micchādiṭṭhisamādānā \| noun \| masc.nom.pl \| believing in wrong views (lit: taking up wrong views) \| dutiyā tappurisa as bahubbīhi<br>` | The parallel `sammādiṭṭhisamādānā` at 22_class.md:122 is `adj … dutiyā tappurisa`; here `noun` (flagged IMPOSSIBLE as masc.nom.pl) with the type notation `as bahubbīhi` and a trailing `<br>`. `\#\#micchā \| adj \| fem.` (168) against `\#\#sammā \| ind \| adv` (22_class.md:124) (old B138) | `adj`; `dutiyā tappurisa \> bahubbīhi` | 9 |
| 27_class.md:445 | `pajahati \| verb \| pr.3rd.sg \| gives up; abandons \| pa + √hā + a + ti<br>with metrically lengthened ā` | The row has `pajahati`, the sentence (433) `pajahāti`. DPD lists `pajahāti` as an irregular form, not a metrical one. `<br>` in the cell (old B139) | `pajahāti`; verify the note | 8 |
| 27_class.md:451 | `diṭṭhī[^50] \| noun \| masc.nom.sg \| who has a view; who has the opinion` | Footnote 50 says the masculine reading "leaves the following pāva without a subject"; the translation (458) makes exactly this word the subject: "the one with view revealed him" (old B140) | Reword the footnote; verify | 7 |
| 27_class.md:362–364 | `na'y'idaṃ \| sandhi \| \| not this` / `\#idaṃ \| pron \| nt.nom.sg \| this` | Third treatment of `idaṃ` in `nayidaṃ` (see 22_class.md:255); the inserted `y` has no row, unlike `[r] inserted between vowels` at 427 (old B141) | One treatment; verify | 7 |
| 27_class.md:226, 241 | `kāmehi ritto **apurekkharāno**,` / `**apurekkharāno** \| prp \| masc.nom.sg` | The exercise (ex 180, 193) has `apurakkharāno`. The same verse in class 29 has `apurekkharāno` in key (650) and exercise. DPD has both headwords (old B157) | One spelling in key and exercise | 8 |
| 28_class.md:128 | `dānaṃ dīyittha **samaṇa**-**brāhmaṇa**-**kapaṇ'addhika**-vanibbaka-**yācakānaṃ**.` | Hyphens added inside the compound in the sentence; the row (139) has none (old B142) | No hyphens | 8 |
| 28_class.md:145 | `**yācakānaṃ** (ca) \| noun \| masc.dat.pl \| to beggars \| √yāc + aka` | Last dvanda member without `\#` (140–144 have it); `vanibbaka` (144) has no construction (old B143) | `\#**yācakānaṃ** (ca)` | 9 |
| 28_class.md:350 | `va \| ind \| conj \| or` | The sentence (333) has `diṭṭhaṃ va sutaṃ mutaṃ vā`; both rows (347, 350) have `va` (old B144) | `vā` | 9 |
| 28_class.md:359 | `n'ūparato \| pp \| masc.nom.sg \| not restrained; not stopped \| na + upa + √ram + ta` | Sandhi of `na` and `uparato` tagged as a pp, with the separate word `na` inside the construction; "not abstained" in the translation (365) (old B145) | `sandhi`; `\#uparato \| pp \| … \| upa + √ram + ta` | 8 |
| 28_class.md:375–376 | `tayo \| card \| masc.acc.pl \| three` / `sukhe \| noun \| nt.acc.pl \| comforts; pleasures` | Numeral masculine, its noun neuter (old B146) | One gender for numeral and noun; DPD has `sukha` as nt only, and `-e` is a masculine accusative plural ending: verify the form (inflection table: DPD lookup) | 6 |
| 29_class.md:89–91 | `etādisaṃ[^53] \| adj \| nt.acc.sg \| such as this; of this type \| kammadhāraya` / `\#ādisaṃ \| adj \| nt.nom.sg \| kind; quality` | The table analyses `eta + ādisa`; footnote 53 calls `ādisa` "a ghost word in DPD" and gives `etad + disa` (DPD: `alutta dutiyā tappurisa etaṃ + disa`). Member tagged `nt.nom.sg` under an accusative; `nt.acc.sg` at 139. Same conflict at 217: footnote 55 argues against the `masc.nom.pl` tag in the row (old B147) | Follow the footnote or drop it | 8 |
| 29_class.md:41 | `n'āhosi \| verb \| aor.3rd.sg \| there was no(t) \| na + √hū + a + si` | Sandhi with `na` tagged as a verb, `na` inside the construction; also `n'āddakkhi` (486), `n'atthi` (605) (old B148) | `sandhi` with sub-rows | 9 |
| 29_class.md:71 | `naṃ \| pron \| nt.acc.sg \| her` | Neuter tag, "her" in the gloss, "it" in the translation (76) (old B149) | One reading | 8 |
| 29_class.md:194, 198 | `ajjhatta-santiṃ pacinaṃ adassaṃ.` / `ajjhattasantiṃ \| noun \| fem.acc.sg \| inner peace \| kammadhāraya` | Compounds hyphenated in the verse lines (19, 150, 208, 818, 819) and at 243–244 in the table, not in the other rows (old B150) | No hyphens | 8 |
| 29_class.md:323 | `asīlatā(ya) \| noun \| fem.instr.sg \| without moral conduct` | The same line is analysed again at 412 with `asīlatā` and no `(ya)`; `sīlabbaten'āpi` is "also by" at 297 and "even by" at 386 (old B151) | One analysis | 8 |
| 29_class.md:376–378 | `iti māgaṇḍiyo \| sandhi \| \| "...[said] Māgaṇḍiya"` / `iti \| ind \| quotation mark \| ""` | Two separate words tagged as sandhi; the member rows have no `\#` (the same words at 220–221 are plain rows) (old B152) | Remove the sandhi row | 9 |
| 29_class.md:529 | `maññati \| verb \| pr.3rd.sg \| thinks; imagines \| √man + ya + ti` | The verse (506, 524) has the metrical `maññatī`; no note. Metrical `munī` (233, 736; flagged IMPOSSIBLE) has none either, while `ragaṃ` (32) has "m.c." (old B153) | `maññatī` with a note | 8 |
| 29_class.md:656, 668 | `apurekkharāno \| prp \| masc.nom.sg \| … \| na + pure + √kar + o + āna` / `kayirā \| verb \| opt.3rd.sg \| he should do; he should make \| √kar + o + eyya` | The same verse is analysed at 27_class.md:226–248 with other constructions (`na + pure + √kar + āna`, `√kar + iya + ā`) and glosses (`kathaṃ` "speech; talk" there, "argument; debate" here) (old B154) | Align the two | 8 |
| 29_class.md:239 | `ajjhatta-santī'ti yam'etam'atthaṃ` | Repeated verse lines differ in punctuation from the stanza block: 239 (no comma; 208 has one), 480 (no comma; 448), 494 (no full stop; 449), 719 (comma; 675 full stop); `māgaṇḍiyāti` at 446, 453 against `māgaṇḍiyā'ti` at 147, 267 (old B155) | Same text in both places | 8 |

## C. Translation and gloss problems

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 16_class.md:285 | `[But now] for him that has been abandoned, it has been uprooted like a palm tree` | `ucchinnamūlo` (row 269 "cut off at the root") is not translated (old C1) | Add "cut off at the root," | 8 |
| 16_class.md:858 | `As soon as he saw the Fortunate One` | `bhagavā` is "the Blessed One" in the row (838), "the Buddha" at 404, 412 and 421, "the Fortunate One" here (old C2) | One rendering | 8 |
| 16_class.md:815 | `\#anusayānaṃ \| noun \| masc.gen.pl \| of underlying tendency` | Same word in one sentence glossed three ways and in the singular: "of underlying tendency" (815), "of sleeping tendency" (822, 829); compounds "latent tendencies" (813), "inherent tendency" (820), "dormant views" (827); translation "latent tendencies" (old C3) | One gloss, plural; verify | 7 |
| 16_class.md:377 | `But I also say, friends, that without reaching the end of the world, (there is) no ending of suffering.` | "also" has no source word; `na … vadāmi` is "I do not say" (old C4) | "But I do not say, friend, that there is an ending of suffering without having reached the end of the world."; verify | 6 |
| 17_class.md:345 | `a disciple of the Buddha reflects in this way` | Row 332 glosses `ariyasāvako` "a disciple of the noble one". `bhagavato` is "the Buddha's" at 322 but "of the Blessed One" in rows 308, 374 and translations 208, 380, 662 (old C5) | One rendering per term | 8 |
| 17_class.md:132 | `vadeyyaṃ \| verb \| opt.reflx.1st.sg \| I myself should say` | `-eyyaṃ` is the ordinary 1st sg optative; "myself" (also in the translation, line 134) over-translates the ending (old C6) | "I should say"; verify | 7 |
| 17_class.md:489 | `in this very fathom length body with its perception and intelligence (is) the world, the source of the world` | Does not follow the Pāli syntax (`lokañca paññāpemi` = "I declare the world …"); `samanake` is "with mind" in row 467, "intelligence" here (old C7) | "… that in this very fathom-long body, with its perception and mind, I declare the world, …"; verify | 6 |
| 17_class.md:408 | `alobho \| noun \| masc.nom.sg \| not greed` | Unidiomatic; translation line 426 "is not greed" (old C8) | "non-greed" (DPD) | 8 |
| 18_class.md:79 | `[this is a case] relating to the community in the beginning and in the end.` | The row (74) glosses `saṅghādiseso` "offence requiring suspension"; member 77 "remains; remainder" does not give "in the end" (old C9) | One rendering in row and translation; DPD: "offence requiring communal rehabilitation" (`saṅgha + ādi + sesa`) | 7 |
| 18_class.md:272 | `"In this very body there is the solid state, the liquid state, the fire state and the air state."` | No `eva` in `atthi imasmiṃ kāye` ("very" belongs to `imameva kāyaṃ` earlier). Rows: `āpodhātu` "liquid state", `vāyodhātū'ti` "gaseous state" (267) vs "air state" here (old C10) | "In this body …"; one gloss per element; verify | 7 |
| 18_class.md:360 | `to re-enter or to go out and to visit the outlying districts` | Third `vā` rendered "and" (old C11) | "or to visit"; verify | 7 |
| 18_class.md:458 | `\#enaṃ \| pron \| masc.acc.sg \| that` | Refers to the elephant: "him" (translation 466 "has him perform") (old C12) | "him"; verify | 7 |
| 18_class.md:96 | `Whichever of these human beings [are] seers. (Thus said venerable Puṇṇaka)` | `ye` (row 85) not rendered; `isayo manujā` are two nominatives ("these seers and men"); full stop missing inside the bracket (old C13) | "Whatever seers and men here … (thus the venerable Puṇṇaka)"; verify | 6 |
| 18_class.md:201 | `One should touch unstable and firm beings with kindness` | Row 187 glosses `tasathāvarāni` "the moving and unmoving, lit. trembling and steady" (old C14) | One rendering; verify | 6 |
| 19_class.md:324 | `preached by the Such Become One` | `tathāgata` is "Realised One; Buddha" in the rows (262, 307), "the Buddha" at 285, "the Such Become One" here (old C15) | One rendering | 8 |
| 19_class.md:440 | `rattiyā \| noun \| fem.loc.sg (loc abs) \| of the night` | Genitive gloss for a locative absolute (431 has "when night") (old C16) | "when the night" | 8 |
| 19_class.md:556 | `(source text uses past tense)[^15]` | The quoted sentence has present tense verbs (`ujjhāyanti khiyyanti vipācenti`, tagged `pr` in rows 552–554), and footnote 15 says the opposite ("The historical present can be translated in the past tense") (old C17) | Remove the bracket or reword: "(historical present)"; verify | 7 |
| 19_class.md:626 | `proliferations, perceptions and concepts regarding forms` | Row 612 glosses `papañcasaññāsaṅkhā` "proliferation of opinions, concepts and constructs; (or) classification of diverse perceptions"; three renderings of one compound (old C18) | Align with one of the analyses at 632–636; verify | 6 |
| 19_class.md:129 | `an individual, having personally experienced in this life directly knowing by himself the liberation of the mind without taints, liberation by wisdom, dwells having reached [this state].` | Hard to read; the same clause is translated more clearly at 16_class.md:125 (old C19) | Reword on the model of class 16; verify | 6 |
| 20_class.md:231 | `jhānaṃ \| noun \| nt.acc.sg \| stage of meditation` | "state of deep meditative calm" at 522 and 19_class.md:587; translation at 526 "fourth stage of meditation" against its own row 522 (old C20) | One gloss; verify | 7 |
| 20_class.md:222–223 | `savitakkaṃ \| adj \| nt.acc.sg \| with thinking` / `savicāraṃ \| … \| with discursive thought` | `vitakka`/`vicāra` are "thoughts"/"examinations" (19_class.md:562), "thinking"/"examining" (19_class.md:574–579) and "thinking"/"discursive thought" here (old C21) | One pair; verify | 7 |
| 20_class.md:235 | `joy and happiness born from solitude` | Row 224: "born from separation" (old C22) | One word; verify | 7 |
| 20_class.md:16 | `\#\#byāpanna (or vyāpanna) \| adj (pp) \| masc. \| ill-will` | Noun gloss for a participle; "malevolent; evil" at 165 (old C23) | "malevolent" (DPD: malevolent; evil; hating) | 8 |
| 20_class.md:366 | `\#saṅghāṭidhāraṇa \| noun \| nt. \| wearing an outer robe` | `saṅghāṭi` is "patchwork robe" at 360, 362, 365 and in the translation, "outer robe" at 366–367 (old C24) | One gloss; verify | 7 |
| 20_class.md:307 | `an excess of speech is to be expected. When there is an abundance of talk` | `kathābāhulla` rendered two ways in one sentence (rows 299, 303 likewise) (old C25) | One rendering; verify | 7 |
| 20_class.md:503 | `somanassadomanassānaṃ \| noun \| nt.gen.pl \| satisfaction and dissatisfaction` | Genitive not shown; translation 526 has "joy and dejection" (old C26) | "of joy and dejection"; verify | 7 |
| 20_class.md:76 | `[Even] if a fool associates closely with a wise person for the rest of his life` | "Even" is in the text (`api`, row 61, glossed "just; only"), so not a supplied word; row 57 says "as long as one lives", not "the rest of" (old C27) | "Even if … for his whole life"; `api` "even"; verify | 7 |
| 20_class.md:459 | `garlanded with aquatic plants; aquatic plant garland maker` | Translation 478 has "who wear moss garlands" (old C28) | One rendering; verify | 6 |
| 21_class.md:249 | `\#atimaññetha \| verb \| opt.reflx.3rd.sg \| he should not despise` | Sub-row gloss includes the "not" of `\#na` (old C29) | "he should despise" | 8 |
| 21_class.md:165 | `āgamaṃ \| verb \| aor.reflx.1st.sg \| I myself have come` | Reflexive endings translated literally throughout the class: "I myself" (165, 175, 291, 296, 319–321), "associate oneself" (191), "make oneself" (193), "one oneself gets" (459), "you could get yourself" (521). In verse these are ordinary middle forms (old C30) | owner decision; plain active in translations | 7 |
| 21_class.md:420 | `(but) that monk does not accept (his apology).` | Present tense after three past tenses for the same historical present (`deseti` is rendered "confessed") (old C31) | "did not accept"; verify | 7 |
| 21_class.md:390 | `One stills thoughts and plans` | `vicāritāni` is "thought about; contemplated; investigated" (372), "examinations" in 17_class.md:613 for the same line (old C32) | One rendering; verify | 7 |
| 21_class.md:503 | `"Let the venerables regain what is your own; do not let what is your own get lost."` | Person switches ("the venerables … your"); row 492 "must try (to) (get back)" (old C33) | "Venerables, regain what is yours; …"; verify | 6 |
| 21_class.md:531 | `They wander around at peace, not opposing a view with views. In them, what could you get yourself` | `ye … tesu` ("those who … from them") is rendered as two independent sentences; `pana` and `idha` are not translated (old C34) | "But those who wander … not opposing a view with views, from them what could you get, Pasūra, …?"; verify | 6 |
| 22_class.md:32 | `Alas, you slept (lit: sleep) badly! Where do I (myself) sleep today?` | Follows the wrong tag at 18; `sessaṃ` is future (so tagged at 22, but glossed "I myself sleep") (old C35) | "Alas, I slept badly! Where will I sleep today?" | 9 |
| 22_class.md:88, 101 | `ādittato'haṃ \| sandhi \| \| I [am] as on fire` / `I am as on fire, [although] engaged in serenity; when will I see with wisdom this state for myself?` | `ādittato` ("as blazing") is the complement of `dacchaṃ`: "when will I … see this as blazing". Reading it as a predicate of `ahaṃ` forces the supplied "[although]" (old C36) | verify; "When will I, yoked to serenity, see this with wisdom as ablaze?" | 6 |
| 22_class.md:133 | `(They have seen) in what is non-self as 'non-self', they have perceived what is foul as foul.` | "in what is non-self as" is not English; tense changes from "saw" to "have perceived" within the verse; "Taking upon themselves" for a compound glossed "who have undertaken" (122) (old C37) | "(They saw) what is non-self as non-self, they saw the foul as foul. Having undertaken right view, …"; verify | 7 |
| 22_class.md:155 | `A person, restrained by conscience, exists somewhere in the world` | `koci` is "any; some(one)" (row 143), not "somewhere"; `bhadro` glossed "good; fortunate" (150), translated "fortunate horse" (old C38) | "Some person … exists in the world"; "good horse"; verify | 6 |
| 22_class.md:216 | `pañhapaṭibhānāni \| noun \| nt.acc.pl \| intelligent answer to a question; eloquent response to a question; lucid reply to a question` | Singular glosses for a plural (the translation has "answers") (old C39) | Plural | 8 |
| 22_class.md:262 | `sammā \| ind \| adv \| thorough, complete` | Adjective glosses for an adverb (old C40) | "thoroughly; completely" | 8 |
| 22_class.md:267 | `this much personal existence that is stable, permanent, eternal, with an unchanging nature` | Order differs from `nicco dhuvo sassato` (rows 247–249: permanent, stable, eternal); `paṭilābho` not rendered; row 250 glosses the adjective `avipariṇāmadhammo` as "unchanging nature" (old C41) | "permanent, stable, eternal"; "of unchanging nature"; verify | 7 |
| 22_class.md:301 | `Sir Gotama, if only you were successful in this holy life, but the monks would not be successful` | `imaṃ dhammaṃ` is "this teaching" (row 278); "holy life" only comes in the last clause. `bhavaṃyeva gotamo` is "only Master Gotama" (row 279 "only sir"), not "if only you" (old C42) | "if only Master Gotama were successful in this teaching, but not the monks, …" | 8 |
| 22_class.md:348, 359 | `asaṅkhataṃ \| pp (as noun) \| nt.nom.sg \| unfabricated` / `unmade and uncreated … the made and the created.` | Row glosses "unfabricated", "of the fabricated" (355); translation "uncreated", "the created" (old C43) | One rendering | 8 |
| 22_class.md:376, 386 | `devo \| noun \| masc.nom.sg \| rain cloud` / `and if the rain clouds would not provide thorough downpour from time to time` | Singular in the row, plural in the translation; "If there were no" for `nevassa` (row 366 "not even would be") (old C44) | Align; verify | 6 |
| 22_class.md:425 | `evañ'ca \| sandhi \| \| and if` | Gloss "and if"; members are "thus" and "and". The translation also drops "thus": "having said [this]" (old C45) | "and thus"; verify | 7 |
| 22_class.md:539 | `pārimaṃ \| adj \| nt.acc.sg \| far shore` | Noun gloss for an adjective that stands before `tīraṃ` ("bank"); `orimaṃ` at 535 is "nearest" (old C46) | "furthest" (DPD: (of shore) furthest; most distant) | 8 |
| 22_class.md:307 | `saṅkhārā \| noun \| masc.nom.pl \| mental intentions; thought processes` | Rows: "mental intentions" (307, 318, 323, 326, 330); translation (333): "mental processes" (old C47) | One rendering; verify | 6 |
| 22_class.md:630 | `(this is my) uncle's wife, (these are) wives of teachers.` | `ācariyabhariyā'ti` ("teacher's wife", row 609) is left out: four items for five (old C48) | Add "(this is my) teacher's wife" | 9 |
| 23_class.md:124, 136 | `dāna**saṃvibhāga**rato \| adj \| masc.nom.sg \| who delights in sharing gifts \| sattamī tappurisa` / `and who delights in sharing gifts.` | The member row (125) analyses `dānasaṃvibhāga` as a dvanda, "in giving and sharing" (so DPD); gloss and translation read it as "sharing of gifts" (old C49) | "who delights in giving and sharing" | 8 |
| 23_class.md:146 | `yad'**ajjhagā** \| sandhi \| \| which attained; was experienced that` | Garbled gloss (old C50) | "which [he] attained" | 8 |
| 23_class.md:386, 404 | `tathāgatassa \| noun \| masc.gen.sg \| of the Thus-Become-One` / `cover the body of the Tathagata, in worship of the Tathagata.**` | Row gloss and translation differ; `Tathagata` without diacritics (old C51) | One rendering; verify | 7 |
| 23_class.md:435 | `akusalā \| adj \| masc.nom.pl \| unhealthy` | "unhealthy" in the row (also 841), "unwholesome" in the translation (457), "unskillful" for the same word at 247 (old C52) | One rendering; verify | 7 |
| 23_class.md:483 | `eko \| adj \| masc.nom.sg \| just one` | "just" belongs to `ekopi` (473), not to plain `eko` (old C53) | "one" | 8 |
| 23_class.md:536 | `\#api \| ind \| \| only; just` | In `attabyābādhāyapi` `api` is "also; even" ("could lead also to my own harm"); the translation (547) leaves it out. Same gloss in `seyyathā'pi` at 558 (old C54) | "also; even"; verify | 7 |
| 23_class.md:590, 600 | `luddhā \| adj (pp) \| masc.nom.pl \| who are greedy, who want` / `[And] because of greed, they make a stockpile [of] wealth` | Translation renders the nominative plural as a cause, parallel to `mohā` (old C55) | "The greedy make a stockpile of wealth" | 8 |
| 23_class.md:606 | `savanampāhaṃ \| sandhi \| \| even I, by hearing` | `api` goes with `savanaṃ`, the object of `vadāmi`: "even the hearing … I say". "even I, by …" also at 617, 621, 625, 629; the translation (634) has it right (old C56) | "even hearing, I" | 8 |
| 23_class.md:677 | `is high and even broad [for protecting its inhabitants]` | `c'eva … ca` is "both … and"; row 652 glosses `c'eva` "and even" (old C57) | "both high and broad"; verify | 7 |
| 23_class.md:928 | `the satisfaction as satisfaction, the danger as the danger, and the escape as the escape` | Article in two of three; "danger" for a word glossed "disadvantage" (884–887); "unsurpassed perfect enlightenment" against "the highest enlightenment" (904); `evaṃ` not translated (old C58) | Align; verify | 6 |
| 24_class.md:58, 70 | `**yodhetha** \| verb \| opt.reflx.3rd.sg \| one would/should fight (against) by oneself; engage in battle (with) by himself` / `you should fight against death with the weapon of wisdom; one should protect the conquest` | Third person in the row, "you" in the translation, then "one" in the same sentence; "by oneself … by himself" in one gloss (old C59) | "one should fight" | 8 |
| 24_class.md:140, 147 | `me \| pron \| 1st.instr.sg \| by me` / `and my teacher will (have) be(en) served with goodwill."` | Row: instrumental "by me"; translation: "my". Brackets inside words ("be(come)", "(have) be(en)") (old C60) | "the teacher will have been served by me"; verify | 7 |
| 24_class.md:209 | `bhagavatā \| noun \| masc.instr.sg \| by the Buddha` | "the Buddha" here, "the Blessed One" in the translation (220) and at 376 (old C61) | "by the Blessed One" | 8 |
| 24_class.md:305 | `sammā \| ind \| - \| complete, perfect` | Adjective glosses for an adverb (see 22_class.md:262) (old C62) | "completely" | 8 |
| 24_class.md:338 | `ussoḷhiñ'ca \| noun \| fem.acc.sg \| and energy, effort` | Same gloss as `ussāhañ'ca` in the row above; the translation (344) has "endurance" (so DPD) (old C63) | "and endurance; exertion" | 8 |
| 24_class.md:446 | `no \| pron \| 1st.dat.pl \| for us` | Plural "for us" / "we will have" (455) inside a first person singular reflection ("I will destroy … I will not cause"); the usual text of the formula has `me`. Key and exercise read `no` (old C64) | verify the reading | 6 |
| 24_class.md:610 | `And monks, lack of belief has a fuel, it is not fuel-less.` | `assaddhiyampāhaṃ … vadāmi` ("lack of faith too, I say, has …") loses "too" and "I say"; "lack of belief" for a word glossed "disbelief, lack of confidence" (old C65) | "Lack of faith too, monks, I say has a fuel"; verify | 7 |
| 25_class.md:29 | `the deities belonging to the (Heaven of the) Thirty Three proclaimed aloud.**` | `saddaṃ` (row 26) is not translated; comma missing after "Kings" (old C66) | "raised the cry"; verify | 6 |
| 25_class.md:174 | `there were four gates of four colours` | The text has "gates of four colours", not "four gates"; "crystals" for "crystal" (164) (old C67) | "there were gates of four colours"; verify | 7 |
| 25_class.md:289, 312 | `mahākassapo \| noun \| masc.nom.sg \| great Kassapa` / `Then the great venerable Kassapa said this` | The name is split and "great" moved before "venerable" (old C68) | "the venerable Mahākassapa"; verify | 7 |
| 25_class.md:456 | `tassa \| pron \| masc.gen/dat.sg \| to him; to that one` | `tassa me` is "of that me" (so glossed at 318: "of that [me]"); here it reads as a third person (old C69) | "of that [me]"; verify | 7 |
| 25_class.md:259 | `bhavanti \| verb \| pr.3rd.pl \| there are, there will be` | "there are" at 249, "there are, there will be" at 259, future in the translation (264) (old C70) | One rendering; verify | 6 |
| 26_class.md:157 | `**And just as they would eat (or, were eating) the flesh of [their] son, they would beat their breasts` | `c'eva … ca` is "both … and" (row 140 "and just"), not "just as" (old C71) | "They would both eat the flesh of their son and beat their breasts"; verify | 7 |
| 26_class.md:337 | `which person seems good to you, more excellent and sublime?**` | `paṇītataro` is a comparative ("more refined", row 328) (old C72) | "more excellent and more sublime"; verify | 7 |
| 26_class.md:346 | `avicāro \| adj \| masc.nom.sg \| without planning \| kammadhāraya > bahubbīhi` | "planning" for `vicāra`; DPD: "free from discursive thought". The translation (356) merges `avitakko` and `avicāro` into one phrase (old C73) | "free from discursive thought" (DPD) | 7 |
| 26_class.md:376, 384 | `jaññā \| verb \| opt.3rd.sg \| one should know` / `you should know that person as "an outcast".**` | Third person in the row, second in the translation; "slanders badly of others" is not English; `kodhano` "irritable" (362), translated "angry" (old C74) | "one should know him as an outcast"; verify | 7 |
| 26_class.md:554 | `by the truth of this statement, may you be well!**` | `suvatthi hotu` is "may there be well-being" (rows 545–546); commas missing in "by body speech or mind" (old C75) | "may there be well-being"; verify | 6 |
| 26_class.md:454, 474 | `**ambil**'aggehi'pi \| sandhi \| \| just predominantly sour` / `**khārikehi**'pi \| sandhi \| \| even hot` | `api` is "just" in the first four items and "even" in the last four, while every member row says "just"; the translation (487) has neither (old C76) | "also" throughout; verify | 6 |
| 27_class.md:115–117 | `oḷārikassa'pi \| sandhi \| \| even of gross` / `\#api \| ind \| \| but` | "even" in the sandhi row, "but" in the member row and in the translation (138) (old C77) | One rendering; verify | 7 |
| 27_class.md:134, 138 | `**vodāniyā** \| ptp \| masc.nom.pl \| purifying; cleansing (lit: to be purified)` / `and mental states to be purified will increase more and more.**` | The translation uses the literal gloss, which reverses the sense ("purifying states will increase") (old C78) | "purifying mental states" | 8 |
| 27_class.md:338, 344 | `te \| pron \| 2nd.dat.sg \| by you` / `that you do not feel and could not be felt by you?**` | `na ca te hoti 'phuseyyan'ti` is "nor does it occur to you: 'I might feel [them]'"; row 340 has "I would myself touch". Opening quotation mark of the translation never closed (old C79) | "and of which you do not think 'I might feel them'"; verify | 7 |
| 27_class.md:404 | `should sit down or lie down hard on a bench or on a bed with detachable legs` | Order reversed against `mañcaṃ vā pīṭhaṃ vā` (bed, bench) (old C80) | "on a bed or a bench"; verify | 6 |
| 27_class.md:437, 458 | `**diṭṭhena** \| noun \| nt.instr.sg \| by the seen` / `**If through the seeing there is a man’s purity,` | "by the seen" in the row, "through the seeing" in the translation; curly apostrophe; the fourth line starts in lower case after a full stop (old C81) | "through what is seen"; `'`; capital | 8 |
| 28_class.md:107 | `**The trees laden with pollen exude a sweet smell all around by means of flower pollen; the first month of the season, spring, [is] pleasant` | "pollen" translated twice; `paṭhamavasanto sukho utu` is "early spring is a pleasant season" (row 97: "first month of spring; early spring") (old C82) | "The trees, covered with flower pollen, exude a sweet smell all around; early spring is a pleasant season"; verify | 7 |
| 28_class.md:139, 147 | `to ascetics, priests, tramps, paupers and beggars` / `to ascetics, brahmins, tramps and travellers, mendicants and beggars.**` | Five glosses for six members in the row, and "priests" for a member glossed "brahmins" (141); the translation has six (old C83) | Use the translation's list | 8 |
| 28_class.md:420 | `\#yena \| ind \| adv \| because of` | In `yen'icchakaṃ` ("wherever it wants", 419) `yena` is "where; wherever" (old C84) | "where; wherever" | 8 |
| 28_class.md:126 | `**One gives to a newcomer, one gives to a traveller, one gives to one who is ill, one gives during a famine.**` | `dānaṃ` ("a gift", rows 114–123) is not translated (old C85) | "One gives a gift to …"; verify | 6 |
| 29_class.md:31 | `ragañ'ca \| sandhi \| \| and` | The sandhi gloss leaves out the word (old C86) | "and Ragā (lust)" | 8 |
| 29_class.md:305, 307 | `\#āha \| verb \| perf.3rd.sg \| it is said (i.e. I say; speak)` / `**also not by virtue and practice, do I speak of purity.**` | Third person tag, first person translation; the same line at 394–396 is "one speaks" (old C87) | One reading; verify | 7 |
| 29_class.md:729 | `**and unsullied by water and mud,**` | `ca` joins `jalena` and `paṅkena` ("by water and mud"); the first "and" is extra (old C88) | "unsullied by water and mud"; verify | 6 |
| 29_class.md:856 | `\#saññaṃ \| noun \| fem.acc.sg \| label; concept; idea; notion` | "and perception" in the sandhi row (855), "notion(s)" in the translation (864), "perception" for the same word at 829 (old C89) | One rendering; verify | 7 |

## D. English typos and grammar

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 16_class.md:527 | `√an･1 a (breath, blow)` | Verb needed: "breathe". Also line 530 (old D1) | `(breathe, blow)` | 9 |
| 16_class.md:548 | `shall, what if, perhaps, \|` | Trailing comma (old D2) | Remove | 9 |
| 16_class.md:612 | `'I have sons, I have wealth'; He even does not own himself` | Capital after a semicolon; word order (old D3) | "…; he does not even own himself" | 8 |
| 16_class.md:395 | `Monks there are these two things. What two? Effort and tranquility.` | Comma missing after the vocative; `tranquility` here, `tranquillity` in row 392 (old D4) | "Monks, there are …"; one spelling | 8 |
| 16_class.md:750 | `seven [span] across inside` | Plural (old D5) | `[spans]`; verify | 7 |
| 16_class.md:622 | `should beat; should strike; gives a blow (to)` | Third gloss is present indicative for an optative (old D6) | "should give a blow (to)"; verify | 7 |
| 17_class.md:74 | `In the same way, Sunakkhatta, is it possible that here an individual person would be focused on material pleasure.` | Inverted word order of a question in a statement (old D7) | "… it is possible that …" | 9 |
| 17_class.md:208 | `said this to the Blessed one:` | Capital (old D8) | `Blessed One` | 9 |
| 17_class.md:605 | `investigated ; examined` | Space before the semicolon (old D9) | `investigated; examined` | 9 |
| 17_class.md:256 | `this is for them highest blessing"` | Article and final full stop missing (old D10) | "this is the highest blessing for them." | 8 |
| 17_class.md:555 | `\#sāla \| noun \| masc. \| sal tree` | `sāl` in the compound row (554) and translation (559) (old D11) | `sāl tree` | 8 |
| 17_class.md:199 | `there palm placed together; there venerated` | Plural (row 201 has "palms") (old D12) | `there palms placed together`; verify | 7 |
| 17_class.md:677 | `bhoja (a country)` | Proper name in lower case (old D13) | `Bhoja`; verify | 7 |
| 17_class.md:147 | `[like] a monkey wishing only for fruit in a forest grove.` | Translation starts in lower case; also 648 `thus like this chattering` (old D14) | Capital; verify | 6 |
| 18_class.md:409 | `**"In regard to what is not self, [the notion] "(This is) self" is the distortion of perception` | Opening quotation mark never closed; nested double quotes; `bhikkhave` not translated (old D15) | Remove the first `"`; add "monks," | 9 |
| 18_class.md:286 | `siyā. \| verb \| opt.3rd.sg` | Full stop in the word cell (old D16) | `siyā` | 9 |
| 18_class.md:497 | `having focused and paid attention on that (task)` | Preposition (old D17) | "paid attention to" | 8 |
| 18_class.md:426 | `"...hot season and so` | Quotation mark not closed (old D18) | Close or remove | 8 |
| 18_class.md:492 | `listening attentively lit. with applied ear` | Separator missing before `lit.` (old D19) | `listening attentively; lit. with applied ear` | 8 |
| 18_class.md:466 | `to whichever task the elephant trainer has him perform,` | "to" is superfluous (old D20) | "whichever task …"; verify | 7 |
| 18_class.md:173 | `Monks, ill will is an obstruction` | `ill-will` in row 162 (old D21) | One spelling; verify | 7 |
| 18_class.md:294 | `With oneself truly well-tamed<br>one obtains a protector that is hard to get.` | Lines 1–3 of the verse start with a capital, line 4 does not (old D22) | One style; verify | 6 |
| 18_class.md:595 | `[^2]: the iti could here also simply indicate a list` | Footnote starts in lower case; it is defined 150 lines after its reference (428) (old D23) | Capital; move below item 1; verify | 7 |
| 19_class.md:98 | `creating affection and respect, for maintaining relationships lead to, non-dispute, concord and unity.` | Words out of order (old D24) | "…, [which] lead to maintaining relationships, non-dispute, concord and unity." | 9 |
| 19_class.md:285 | `is being preached, monk does not get inspiration` | Article missing (old D25) | "a monk" | 9 |
| 19_class.md:381 | `curses, gets angry is repelled and is obstinate` | Comma missing (old D26) | "gets angry, is repelled" | 9 |
| 19_class.md:106 | `√khī･1 a ( exhaust)` | Space after the bracket; also 553 (old D27) | `(exhaust)` | 9 |
| 19_class.md:591 | `[which is ] free from thinking` | Space before the bracket (old D28) | `[which is]` | 9 |
| 19_class.md:393 | `panānanda \| - \| - \| and Ananda` | `Ananda` without macron at 393, 395, 404, 414 (twice), 429, 462; `Ānanda` in class 17 (old D29) | `Ānanda` | 9 |
| 19_class.md:201 | `from Skt saṃran̄janı̄ya, "causing delight."` | `n̄` and `ı̄` are n / dotless i with combining macrons (extraction artefact); the outer quotation mark opened after "notes:" is never closed (old D30) | `saṃrañjanīya`; close the quote | 9 |
| 19_class.md:562 | `vitakkavicārānaṃ \| noun \| masc.gen.pl \| thoughts examinations` | "of … and" missing (old D31) | "of thoughts and examinations" | 8 |
| 19_class.md:96 | `lead to; are conducive for` | Preposition (old D32) | "conducive to" | 8 |
| 19_class.md:512 | `Unshakable mental liberation, brahmin, - this holy life [has] that as a goal[^12].` | Comma followed by a spaced hyphen (old D33) | "…, brahmin – this holy life …" | 8 |
| 19_class.md:192 | `outflow of wholesome` | Article (also 199) (old D34) | "of the wholesome"; verify | 7 |
| 19_class.md:414 | `Just like Ananda, in the early dawn time of night` | Reads as "like Ānanda"; `vā pana` untranslated (old D35) | "Or just as, Ānanda, at dawn …"; verify | 7 |
| 19_class.md:617 | `among past future and present` | Commas (old D36) | "past, future and present"; verify | 7 |
| 19_class.md:203 | `[^6]: as bahubbīhi, qualifying dhammā` | Footnotes 6, 7, 10, 12, 14 start in lower case and have no full stop; 3, 5, 9, 11, 13, 15 are full sentences (old D37) | One style; verify | 7 |
| 19_class.md:462, 626; 24_class.md:440 | `and said this to the Blessed One**` / `overwhelm a man**` / `to arise**` | Translations without a final full stop (script: bold lines that follow a table). Also 22:230, 22:386, 23:600 and 28:467, already listed under their classes (old D117) | Add | 8 |
| 20_class.md:643 | `Venerable Sariputta heard when Lucky Star, the young Licchavi, was talking in the Vesali assembly (saying), "The Ascetic Gotama has no super-powers, a distinction of knowledge and vision worthy of the Noble One's."` | `Sariputta`, `Vesali` without diacritics (also row 620); possessive apostrophe in a plural (`Noble One's`; row 617 `Son of the Licchavi's`); proper names translated ("Lucky Star", "Son of Sāri") (old D38) | `Sāriputta`, `Vesālī`, "noble ones", "Licchavis" | 9 |
| 20_class.md:435 | `for who is at ease` | "one" missing; also translation 439 (old D39) | "for one who is at ease" | 9 |
| 20_class.md:544 | `has faith (in); inclines (towards); \|` | Trailing semicolon (old D40) | Remove | 9 |
| 20_class.md:604 | `Pāṇinī has two parallel rules to that effect7 and Kaccāyana … D III.102 "**` | Quotation pasted with the source's footnote number (`effect7`), `Pāṇinī` for `Pāṇini`, an unclosed quotation mark, and a lower-case start ("this can be classified") (old D41) | Clean up | 9 |
| 20_class.md:206 | `as first priority; to the fore lit. around the front` | Separator missing before `lit.` (old D42) | `; lit.` | 8 |
| 20_class.md:568 | `dreadlocked ascetics` | `dread-locked` in the translation (600) (old D43) | One spelling | 8 |
| 20_class.md:574 | `those for whom there are no clothes. \|` | Full stop in a gloss cell (old D44) | Remove | 8 |
| 20_class.md:411 | `**for one who is happy delight arises.**` | Partial translations 411, 421, 439 start in lower case; 403 and 431 with a capital (old D45) | One style; verify | 7 |
| 20_class.md:275 | `[he speaks] reasonable, within a limit and [what is] advantageous.` | Ungrammatical (old D46) | "[he speaks words that are] reasoned, measured and beneficial"; verify | 6 |
| 20_class.md:455 | `from Western lands; belonging to the western district` | Capital W (also 478) (old D47) | lower case; verify | 6 |
| 21_class.md:21 | `which they say with immediate results.` | Verb missing (old D48) | "which they say [is] with immediate results" | 8 |
| 21_class.md:55 | `delivered (to); \|` | Trailing semicolon; also 88 (`precepts and practices;`), 509 (`at peace;`) (old D49) | Remove | 9 |
| 21_class.md:175 | `[so that ] the king of death` | Space before the bracket (old D50) | `[so that]` | 9 |
| 21_class.md:179 | `"imperf. of pa5 + ✓vac;? or aor. of pa5 + avati2;?"` | `✓` (check mark) for `√`; `pa5`, `avati2` keep the source's superscript homonym numbers (old D51) | `√vac`; remove or superscript | 8 |
| 21_class.md:401 | `they quarreled` | US spelling (also 420); UK elsewhere (`unskilful`, 367, 390) but `skillful` at 100 and 296 (old D52) | One spelling | 8 |
| 21_class.md:522 | `pasūra \| noun \| masc.voc.sg \| Pasura` | Diacritic (old D53) | `Pasūra` | 9 |
| 21_class.md:134 | `would be apparent. (lit. make itself known)"` | Full stop before the bracket, inside the quotation (old D54) | Move; verify | 7 |
| 21_class.md:531 | `Pasura, in whom there is nothing grasped as the highest.**` | A question that ends with a full stop; `Pasura` without the diacritic (as in row 522) (old D55) | `Pasūra`; `?` | 9 |
| 22_class.md:63 | `"I will be." is imagination; "I will not be." is imagination.**` | Full stop inside the quotation in mid-sentence, twice; the first two quotations have none (old D56) | Remove | 9 |
| 22_class.md:82 | `hard to achieve, hard to attain . Come` | Space before the full stop (old D57) | Remove | 9 |
| 22_class.md:230 | `(lit. an opposition should be made)**` | Translation without a final full stop; also 386 (old D58) | Add | 8 |
| 22_class.md:352 | `jātassa \| pp (as noun) \| nt.gen.sg \| of born` | Article missing; the next rows have "of the become", "of the made" (old D59) | "of the born" | 9 |
| 22_class.md:580 | `sloping to going out, (nibbāna) slanting to going out` | The bracket stands after the comma (old D60) | "going out (nibbāna), slanting" | 9 |
| 22_class.md:205 | `you won't go far from here, mind".**` | Full stop outside the closing quotation mark here and at 520; inside at 133, 333 (old D61) | One way; verify | 7 |
| 22_class.md:226 | `√an･1 a (breath, blow)` | Noun "breath" among verb meanings; same at 16_class.md:527, 530, 20_class.md:23, 21_class.md:66 (old D62) | DPD lookup; "breathe"; verify | 6 |
| 23_class.md:3 | `**Break up following words in suitable ways**` | Article missing; no full stop (old D63) | "Break up the following words in suitable ways."; verify | 7 |
| 23_class.md:319 | `jhāyinomhāti \| sandhi \| \| we are meditators" \|` | Closing quotation mark with no opening one; also `I will sit"` at 732 (old D64) | Remove or pair | 9 |
| 23_class.md:337 | `"These (monks say) 'We are meditators, we are meditators!" but they meditate, brood, overthink, mis-meditate."**` | The inner quotation opens with `'` and closes with `"`; "Here friends" without a comma (old D65) | `'We are meditators, we are meditators!'` | 9 |
| 23_class.md:345 | `accatari \| verb \| aor.3rd.sg \| transcended, overcome, escaped` | "overcome" among past forms (old D66) | "overcame" | 8 |
| 23_class.md:378 | `ānanda \| noun \| masc.voc.sg \| Ananda` | Names without diacritics: `Ananda` (378, 404), `Tathagata` (404), `Rahula` (514, 547); "Sal trees" 379, "sal trees" 381 (old D67) | `Ānanda`, `Rāhula`, `Tathāgata` | 8 |
| 23_class.md:414, 419 | `focusing on prominent features` / `focussing on the secondary characteristics` | Two spellings five rows apart (again at 820, 825); `misbehavior` (667, 670, 673) beside `realised` (907) (old D68) | owner decision (UK/US) | 8 |
| 23_class.md:575 | `[and] torture [him]....**` | Four dots; translations without a final full stop at 600; `" ...` at 547 (old D69) | `…` | 8 |
| 23_class.md:869 | `and as long as I, lit. how long - that long – and - I` | Hyphens and an en dash mixed in one gloss (old D70) | One dash | 8 |
| 23_class.md:907 | `abhisambuddho'ti \| pp \| masc.nom.sg \| " realised"` | Gloss with a stray space after the opening quote; the row is a sandhi with `iti` tagged `pp` and has no `\#iti` sub-row (old D71) | `sandhi`; `"…realised"`; add sub-rows | 9 |
| 23_class.md:928 | `to the unsurpassed perfect enlightenment."**` | Closing quotation mark with no opening one (old D72) | Remove | 9 |
| 24_class.md:67 | `without attaching; without clinging (lit. homeless). \|` | Full stop at the end of a gloss; also 167 (old D73) | Remove | 8 |
| 24_class.md:171 | `ima designates what is nearest, accantasamipa, either physically or in thought` | `accantasamipa` for `accantasamīpa`; first person editorial note ("I did not note this earlier") (old D74) | `accantasamīpa`; owner decision on the voice | 8 |
| 24_class.md:276 | `**Whoever monks, would say thus, "**` | Comma after instead of around "monks"; the quotation opened here is never closed (292). Stray closing quotes in glosses at 218, 290 (`he experiences"`), 585 (`lack of confidence"`); closing quote with no opening one at 455 (old D75) | "Whoever, monks, would say thus:" | 9 |
| 24_class.md:344 | `for putting out that exact clothes or head.**` | Number ("that … clothes"); verbs supplied in brackets three times in one sentence (old D76) | "that very cloth or head"; verify | 7 |
| 24_class.md:396 | `hohi \| verb \| imp.2nd.sg \| You must be` | Capital in a gloss (old D77) | "you must be" | 8 |
| 24_class.md:427 | `**Only for as much the continuance of this body` | Not English (old D78) | "Only for the continuance and nourishment of this body, …" | 8 |
| 24_class.md:482 | `carried along by its (the rivers) current` | Possessive without apostrophe (old D79) | "the river's" | 9 |
| 24_class.md:480 | `āpajjeyya \| verb \| opt.3rd.sg \| would experience; gets; lit. come to[^33]` | Three verb forms in one gloss; footnote marker in the gloss cell (old D80) | "would experience; would get; lit. would come to"; verify | 7 |
| 24_class.md:576 | `ko c'āhāro ayonisomanasikārassa. assaddhiyan'ti'ssa vacanīyaṃ.` | Two questions end with a full stop (translated with `?`); no final full stop (old D81) | `?`; verify | 7 |
| 25_class.md:291 | `ānandaṃ \| noun \| masc.acc.sg \| Ananada` | Misspelt; names without diacritics: `Ananda` (148, 295, 312), `Kusavati` (147), `Moggallana` (281, against `Moggallāna` 271), `Mara` (454, 470); the translation at 174 has `Ānanda`, `Kusāvatī` (old D82) | `Ānanda` etc. | 9 |
| 25_class.md:162 | `veḷuriyamayaṃ \| adj \| nt.nom.sg \| made of cats eye` | Apostrophe missing ("cat's eye" at 174) (old D83) | "cat's eye" | 9 |
| 25_class.md:66 | `heart warming; from the heart; touching the heart; \|` | Gloss ends with a semicolon; also 70, 395, 407, 420 (old D84) | Remove | 8 |
| 25_class.md:337, 343 | `āmisadāy'ādā \| noun \| masc.nom.pl \| inheritor of worldly things` / `not inheritor of worldly things.**` | Singular for a plural (old D85) | "inheritors" | 8 |
| 25_class.md:400 | `**Whatever Bhikkhu, having himself assigned a robe to a monk` | "Bhikkhu" with a capital and "monk" in one sentence (old D86) | "Whatever monk" | 8 |
| 25_class.md:442 | `wholesome qualities, We will live` | Capital after a comma; space before the closing quotation mark (`night. "**`) (old D87) | Fix | 9 |
| 25_class.md:470 | `by the name of dūsī (corrupter), [and] I had a sister by the name of kāḷī.` | Names in lower case (old D88) | `Dūsī`, `Kāḷī`, `Māra` | 8 |
| 25_class.md:195 | `viññūhī'ti \| sandhi \| masc.instr.pl \| by wise people" \|` | Closing quotation mark with no opening one; also 255 (`train yourself in"`). Grammar on a sandhi row (old D89) | Remove | 9 |
| 25_class.md:543 | `brāhmaṇo \| noun \| masc.nom.sg \| Brahman` | "Brahman" here and at 549; "brahmin" at 536 and in class 24 (old D90) | One spelling; verify | 7 |
| 26_class.md:57 | `having given long-life, strength, beauty, happiness and understanding, he has long life` | "long-life" and "long life" in one sentence (old D91) | "long life" | 8 |
| 26_class.md:81 | `supported by a staff….?**` | Ellipsis, full stop and question mark (old D92) | `…?` | 8 |
| 26_class.md:178 | `hatred is never appeased by hatred; they are appeased by non-hatred.` | Number changes from "hatred is" to "they are" (old D93) | "it is appeased" | 8 |
| 26_class.md:273 | `who has entered a unalterable fixed course, entered the level of the superior man` | "a unalterable"; "superior man" for a compound glossed "honourable man" (258) (old D94) | "an unalterable"; one rendering | 9 |
| 26_class.md:363 | `upanāhī \| adj \| masc.nom.sg \| resentful, \|` | Gloss ends with a comma (old D95) | Remove | 9 |
| 26_class.md:414 | `what is that other than foolishness!?**` | Double punctuation (old D96) | `?`; verify | 7 |
| 27_class.md:69 | `it is to be silent.` | Not English (old D97) | "one should be silent" | 8 |
| 27_class.md:127, 129 | `when practiced (lit: like gone along)` / `for (those who are) practising; lit. gone along` | "practiced" and "practising" in adjacent rows; "practice" as a verb at 138 (old D98) | owner decision (UK/US) | 8 |
| 27_class.md:140 | `ko jaññā maraṇaṃ suve,` | Quotation ends with a comma (old D99) | Full stop or `?` | 8 |
| 27_class.md:224 | `should be made to do by one of three rules[^44]:` | Not English (footnote 44 gives the readable version); the third of three parallel phrases drops the brackets: `according to a case` (old D100) | Use the footnote wording; verify | 7 |
| 27_class.md:307 | `cf. DN-a: "ñatva".` | `ñatva` for `ñatvā` (old D101) | `ñatvā` | 8 |
| 27_class.md:309 | `The agens in the expression vaso vatteti stands in the genetive` | "genetive"; "agens" (old D102) | "genitive"; "agent" | 9 |
| 27_class.md:398 | `should sit down hard(on)` | Space missing (old D103) | `hard (on)` | 9 |
| 27_class.md:285 | `**niṭṭhita**cīvarasmiṃ \| noun \| nt.loc.sg (loc abs) \| when the robe cloth is complete (loc abs)` | `(loc abs)` in the grammar cell and again in the gloss (old D104) | Remove from the gloss | 8 |
| 28_class.md:33 | `satisfaction and gratitude, Hearing the teaching at the right time` | Capital after a comma (old D105) | "hearing" | 9 |
| 28_class.md:278 | `tirelessly throughout the day and night, – it is, indeed, he` | Comma followed by a dash (old D106) | One mark | 8 |
| 28_class.md:442 | `wandered around on a walking tour wherever it wants, wherever it liked, according to its pleasure, now I will restrain that` | Tense changes ("wants … liked"); comma splice before "now" (old D107) | "wherever it wanted, wherever it liked, …; now" | 8 |
| 28_class.md:467 | `but not for those seeking the far shore**` | No final full stop; footnote 51 (469) has none either (old D108) | Add | 8 |
| 28_class.md:157 | `mahābrahmā \| noun \| masc.nom.sg \| great God almighty; supreme spirit` | "God" here, "god" at 156, 159 and in the translation (181); "you're" at 331 (old D109) | One form; verify | 7 |
| 29_class.md:7 | `**Please make line by line translation. Breaking all sandhi and comp (naming type of comp). And fill construction of verbs and participles on the last column**` | Not English; no final full stop (old D110) | "Translate line by line, resolve every sandhi and compound (naming the compound type), and give the construction of verbs and participles in the last column." | 8 |
| 29_class.md:237 | `**indeed, not grasping them, Sage say,**` | Not English (old D111) | "indeed, Sage, you speak of not grasping them," | 8 |
| 29_class.md:380 | `nor by knowledge, ([said] Māgaṇḍiya")**` | Closing quotation mark inside the bracket, with no opening one for it; "nor even by virtue and observance(s) that one speaks of purity" (396) has a stray "that" (old D112) | Fix | 8 |
| 29_class.md:463 | `\#māgaṇḍiya \| noun \| masc.voc.sg \| Magaṇḍiya` | `Magaṇḍiya` for `Māgaṇḍiya` (462, 463, 467) (old D113) | `Māgaṇḍiya` | 9 |
| 29_class.md:484 | `because of this ; lit. from this` | Space before the semicolon (old D114) | Remove | 9 |
| 29_class.md:787 | `tammayo \| adj \| masc.nom.sg \| identified(with) (lit: made of that)` | Space missing (old D115) | `identified (with)` | 9 |
| 29_class.md:775, 792 | `**He who has perfect knowledge [does] not by view, nor by thought**` / `**go to conceit, he is not made-of-that` | Sentence split so that neither half reads; line translations start with a capital at 544, 607, 690, 717, 775, 849 and in lower case elsewhere (old D116) | Reword; one convention; verify | 7 |

## E. Markdown defects that affect rendering

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 16_class.md:193 | `vipariṇāma-dhammaṃ` | Hyphen inside a Pāli word in the sentence; row 202 and the exercise have `vipariṇāmadhammaṃ` (old E1) | Remove the hyphen | 8 |
| 16_class.md:715 | `\# yācitāya \> yācikāya` | Space after `\#` (old E2) | `\#yācitāya` | 9 |
| 16_class.md:374 | `antakiriyaṃ (antaṃ + kiriyā) \| noun \| fem.acc.sg \| ending, relief \| dutiyā tappurisa` | Compound analysis inside the word cell instead of `\#` sub-rows; `verify_key.py` reports the row as "not in sentence" (old E3) | Two `\#` rows | 8 |
| 16_class.md:540 | `once born or even twice born,<br>who has no compassion` | `<br>` inside a bold translation line; no other translation in the class has one (old E4) | One line; verify | 7 |
| 17_class.md:650 | `[UD45](https://s.dhamma.gift/kn/ud/index.html#ud5.5). <br>` | Full stop after the reference; not in the exercise (old E5) | Remove | 9 |
| 17_class.md:243 | `*[+m]*` | Italic note about the inserted `m` in the root column; nothing similar elsewhere (old E6) | owner decision (cf. `[d]` in class 16) | 7 |
| 18_class.md:201 | `as "a flank of the <br>Dark One."` | `<br>` in the middle of a phrase (old E7) | Remove this `<br>` | 9 |
| 18_class.md:568 | `aññen'eva pādaṃ karomī"ti.` | Closing `"` with no opening one (the inner quote uses `'…'`); row 589 repeats it (old E8) | `karomī'ti` or add the opening quote | 9 |
| 18_class.md:81 | `"ye kec'ime isayo manujā, (icc'āyasmā puṇṇako)` | Opening `"` never closed (old E9) | Remove or close | 9 |
| 18_class.md:213 | `**(the reading tathārūpassa also exists)**` | Note formatted like a translation line, between two halves of one table; same at 407 (`**vipallāsa = vi + pari \> …**`) (old E10) | Footnote or plain text; verify | 7 |
| 18_class.md:220 | `√su･4 ṇā (hear) (ssu in comps) +ta+ā` | Extra derivation note appended to the root cell (old E11) | Root only; verify | 7 |
| 19_class.md:354 | `**lokadhātu \> loka + dhātu (kammadhāraya)**` | Arrow reversed: analysis lines use `\<` (240–252, 287–295, 326–332, 383, 416–418); `\>` at 354, 464, 466 (old E12) | `\<` | 9 |
| 19_class.md:387 | `āloko pātubhavissatī"ti?` | Closing `"` with no opening one; repeated in row 410 (old E13) | Add the opening quote or drop this one | 9 |
| 19_class.md:500 | `\#ceto (or)<br>\#cetaso \| noun (as adj) \| -<br>masc.gen.sg \| mind<br>of mind` | Two alternative rows stacked in one row with `<br>`; also 499 and 173 (`sattamī tappurisa<br>or <br>kammadhāraya`) (old E14) | Two rows, or a footnote; verify | 7 |
| 19_class.md:597 | `    **Bh. Bodhi puts it nicely: "The bahubbīhi is not a different kind of compound …"**` | Bold, indented continuation paragraph of footnote 13 (old E15) | Plain text; verify | 6 |
| 19_class.md:201–207, 593–600 | `[^3]: Bh. Bodhi notes:` … `[^11]: Alt.:` | Footnote definitions sit in two blocks in the middle of the file (after item 6 and after extra 5), not after their own items; footnote 5 (131) does follow its item. Ids 3, 4, 5 are therefore defined in the order 5, 3, 4 (old E16) | Place each after its item, as at 131; verify | 7 |
| 20_class.md:173–181 | `[^16]: The relevant meaning of uddesa here would be, cf. Cone s.v.: "that to which one refers, point` / `    **of authority".**` | Footnote broken in the middle of a quotation; the continuation paragraphs are bold. Same bold continuation in footnotes 17 (185) and 18 (604) (old E17) | One paragraph, no bold | 9 |
| 20_class.md:142 | `kammadhāraya<br>na` | Stray `<br>na` in the compound-type cell (old E18) | `kammadhāraya` | 9 |
| 20_class.md:471–472 | `\# tesaṃ` / `\# ahaṃ` | Space after `\#` (old E19) | `\#tesaṃ`, `\#ahaṃ` | 9 |
| 20_class.md:214 | `**piṇḍapāta \> piṇḍaṃ + pāta (dutiyā tappurisa)**` | Arrow reversed (all other lines in the class use `\<`) (old E20) | `\<` | 9 |
| 20_class.md:645 | `**sāriputto \< sāriyā + putto (chaṭṭhī tappurisa)<br>sunakkhatta \< su + nakkhatta (kammadhāraya)**` | Two analyses in one bold line joined by `<br>`; `licchavīnaṃ+ putta` (647) lacks a space (old E21) | One line each | 8 |
| 20_class.md:11 | `\#padosaṃ<br>[ca]` | `<br>` inside the word cell (old E22) | `\#padosaṃ [ca]` | 8 |
| 21_class.md:488 | `mā vo sakaṃ vinassā"ti.` | Closing `"` with no opening one (also row 499) (old E23) | Add or remove | 9 |
| 21_class.md:308 | `kammadhāraya<br>\> bahubbīhi` | `<br>` in the type cell (old E24) | One line | 8 |
| 21_class.md:177–182 | `[^20]: Cone s.v. āha, āhu …` | Footnotes 20–24 are defined in one block after item 8 (old E25) | After their items; verify | 7 |
| 22_class.md:269 | `**abhavissaṃsu.**` | Full stop inside the bold (old E26) | `**abhavissaṃsu**.` | 9 |
| 22_class.md:180 | `[^26]: Alt. this could be seen as an abl.sg.` | Footnote of item 5 (row 126) defined after item 7 (old E27) | After item 5 | 8 |
| 22_class.md:139 | `tatiyā tappurisa<br>\> bahubbīhi` | `<br>` in the type cell (also 250) (old E28) | One line | 8 |
| 22_class.md:34 | `asmī'ti, bhikkhave, maññitam'etaṃ, 'ayam'aham'asmī'ti` | First quotation has no opening `'`; the other three have. No final full stop (also 103, 135). Closing-only quotes: `upaccagun'ti` 103, `cittā'ti` 182, 407, 472 (old E29) | `'asmī'ti` | 8 |
| 23_class.md:677 | `in the same way, indeed, a <br>noble disciple` | Line break in the middle of the sentence (old E30) | Remove `<br>` | 9 |
| 23_class.md:189 | `**santussako[^28]** ca **subharo** ca` | Footnote marker inside the bold. Footnotes 27 and 28 (items 2 and 6) are defined at 257–258 after item 8; 29 and 30 (extras 3 and 4) at 761–762 after extra 8 (old E31) | Marker outside; definitions after their items | 8 |
| 23_class.md:721 | `bhāsitaṃ \| noun or<br>pp \| nt.acc.sg \| utterance; saying<br>what is said` | `<br>` in the pos and gloss cells (old E32) | owner decision (`<br>`) | 7 |
| 23_class.md:116 | `**\#payata** \| pp (as adj) \| masc. \| generous; liberal` | Bold opens before the `\#` (116, 119, 148) or after it (105, 170, 229, 669). Bold words of the sentence not bold in the table: `sadhane` 583, the three verbs at 571–573, `dubbalataraṃ` 562 (old E33) | `\#**payata**` | 8 |
| 23_class.md:260 | `[VIN5.4.7](https://s.dhamma.gift/vin/tv/pli-tv-kd14/index.html) tiṇavatthārakaṃ<br>` | A topic word after the reference, before the `<br>`; no other item has one (`verify_key.py`: "sentence word has no row") (old E58) | Remove, or put it in brackets; verify | 7 |
| 24_class.md:317 | `ādittacelo<br>\#āditta<br>\#celo \| noun<br>pp<br>noun \| masc.nom.sg \| whose clothes are on fire <br>on fire<br>clothes \| bahubbīhi` | Three table rows packed into one with `<br>`, again at 319; pos `noun` for a bahubbīhi adjective (DPD: adj, `kammadhāraya > bahubbīhi`) (old E34) | Three rows | 9 |
| 24_class.md:479 | `\#byasanaṃ<br>(+ca) \| noun \| nt.acc.sg \| disaster` | `<br>` inside the word cell (old E35) | `\#byasanaṃ (+ca)` | 9 |
| 24_class.md:185 | `8. [MN31](https://s.dhamma.gift/mn/mn31/index.html) kiṃ nu kho mayaṃ` | No `<br>` between the reference and the sentence (the exercise has it) (old E36) | Add `<br>` | 9 |
| 24_class.md:551 | `masc.gen[^35].sg` | Footnote marker in the middle of the grammar tag; also in a gloss (49, 480) and a type cell (60) (old E37) | After the tag | 8 |
| 24_class.md:574 | `    **Cf. Syntax, p. 231: "The subjective Gen. can also be regarded` | A long quotation set wholly in bold, indented as a continuation of footnote 35. Footnotes 31–32 are defined after item 6, 33–35 after extra 4 (old E38) | Plain text; definitions after their items; verify | 7 |
| 24_class.md:563 | `√dis + a + **āvī**` | Bold inside the construction cell (not at 126); `bhuttāvī` (156) bold in the sentence, not in the table (old E39) | One way; verify | 7 |
| 25_class.md:87 | `***pema + anīya***` | Constructions are set in italics (15, 23, 98, 389, 406), partly in italics (44 `*tila* + \*a`), in bold italics (87, 89), in bold (166–172, 199–205) or plain (36, 60, 120, 391) (old E40) | One style | 8 |
| 25_class.md:47 | `ahosi \| verb \| aor.3rd.sg \| was \| √hū･1 a (be)<br> + a \> ho` | `<br>` inside the cell; old-style root cells here and at 37 in a class that otherwise gives constructions (old E41) | One line | 8 |
| 25_class.md:137 | `    **Cf. Māgadhabhāsā, p. 128: "The future passive participle can also function as a verb` | Long quotations in bold, indented under footnotes 36 and 37 (137, 141); footnote 37 is in the first person ("which I have not seen elsewhere"); marker in the pos cell (`adj[^37]`, 115) (old E42) | Plain text; owner decision on the voice | 7 |
| 25_class.md:449 | `bhūta + pubba + aṃ[^38]` | A footnote in the construction cell whose whole text is "kammadhāraya" (496, defined after extra example 4) (old E43) | Put the type in the cell | 8 |
| 25_class.md:431 | `bhāvanā'nuyogam'anuyuttā \| adj, <br>sandhi \| \|` | `<br>` in the pos cell (old E44) | `sandhi` | 8 |
| 25_class.md:120 | `**dvayena** \| adj \| masc.instr.sg \| by twofold; dual; double \| dvi + \*a` | Target words are bold in the table here and in extra examples 3–4; not in items 1–4 (15, 23, 36, 65) or extras 1–2, though bold in the sentences (old E45) | One way; verify | 7 |
| 26_class.md:146 | `paṭipiseyyuṃ \| verb \| opt.3rd.pl<br>(+acc) \| they would beat against` | `<br>` in the grammar cell (old E46) | `opt.3rd.pl (+acc)` | 8 |
| 27_class.md:460 | `[^50]: Norman reads diṭṭhī as fem.nom.sg` | Footnote 50 is defined before 46–49 (462–465); 39–45 are all defined after item 12 (old E47) | In order, after their items | 8 |
| 27_class.md:311 | `    **"What do you think, Aggivessana, would a noble, head-anointed king in his own realm have the power` | An alternative translation in bold, indented under footnote 42 (old E48) | Plain text; verify | 7 |
| 27_class.md:54 | `āpattiyā \| noun \| fem.loc.sg<br>(loc abs) \| [when] the offence` | `<br>` in the grammar cell (not at 53) (old E49) | `fem.loc.sg (loc abs)` | 8 |
| 27_class.md:214 | `dhammānaṃ \| noun \| masc.gen.pl \| of[^43] law; case; rule` | Footnote marker in the middle of a gloss; singular glosses for a plural (old E50) | After the gloss; plural | 8 |
| 28_class.md:321 | `**moggallāna** \| noun \| masc.voc.sg \| **Moggallāna** \| muggala + \*yāna` | Bold in the gloss cell (old E51) | Plain | 9 |
| 28_class.md:424 | `**\#**kāmaṃ \| ind \| adv \| freely; according to one's wishes` | Bold on the `\#` only (old E52) | `\#kāmaṃ` | 9 |
| 28_class.md:35 | `**sīlaṃ[^51]** yāva **jarā** **sādhu**,` | Footnote marker inside the bold (old E53) | `**sīlaṃ**[^51]` | 8 |
| 28_class.md:239 | `\#**rattā (ca)** \| noun \| nt.nom.pl \| nights and \| ratti + a` | Bold covers `(ca)`; bold before the `\#` at 140, 166, 168, 178, 353, 423, 435, after it at 94, 99, 169, 224, 246. `vasī` (175) bold in the table, not in the sentence (old E54) | One way | 8 |
| 28_class.md:405 | `is obtained; is found<br>(used here in pl.)` | `<br>` in the gloss cell (old E55) | owner decision (`<br>`) | 7 |
| 29_class.md:17 | `disvāna taṇhaṃ aratiṃ ragañ'ca,` | The stanza blocks (17–20, 78–81, 147–150, …) are four or six consecutive lines with no `<br>` and no trailing spaces, so Markdown joins them into one paragraph; the other classes use `<br>` (old E56) | verify in the built site | 7 |
| 29_class.md:637 | `leaving home, wandering around homeless,` | The only line translation not in bold (old E57) | Bold | 9 |

## F. Convention drift

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 16_class.md:200 | `\#aniccaṃ \| adj. \|` | POS with a full stop (old F1) | `adj` | 9 |
| 16_class.md:270 | `\#ucchinna \| pp \| masc. \|` | Stem gender with a full stop here and at 297 (`nt.`), 652, 694 (`fem.`), 743, 795; without at 74, 203, 282, 490, 556, 656, 665 (old F2) | No full stop | 9 |
| 16_class.md:626 | `opt.3rd.sg (reflex) (+dat)` | Reflexive written `(reflex)` here, `opt.reflx.3rd.sg` at 459 and `opt.reflx.1st.sg` at 563 (old F3) | `opt.reflx.3rd.sg (+dat)` | 9 |
| 16_class.md:677 | `nt.loc.sg (loc.abs)` | `(loc.abs)` here and at 693; `(loc abs)` in classes 19, 20, 25, 27 (old F4) | `(loc abs)` | 9 |
| 16_class.md:460 | `nayidaṃ \| - \| - \| not that` | Every other sandhi row has `sandhi` in column 2 (old F5) | `nayidaṃ \| sandhi \| \|` | 9 |
| 16_class.md:598 | `iti \| ind \| quotation mark \| ""` | Grammar of `iti` written four ways: `quote` (219), `quotation mark` (598), `-` (334, 419, 446, 496, 538, 564, 856), `adv` (232) (old F6) | One label | 8 |
| 16_class.md:411 | `na \| ind \| - \| not` | `na` is `neg` elsewhere (183, 363, 435); `-` at 411 and 533. In general items 9–21 and extra 7–8 fill empty grammar cells with `-`, items 1–8 leave them blank (old F7) | `neg`; one way to mark an empty cell | 8 |
| 16_class.md:316 | `neso dhammo neso vinayo netaṃ satthusāsananti` | Items 1–8 and extra 1–6 mark sandhi with apostrophes in the sentence and in the rows (`c'eva`, `pan'etaṃ`); items 9–21 and extra 7–8 do not (`neso`, `cāhaṃ`, `esevanto`) (old F8) | owner decision | 8 |
| 16_class.md:346 | `food, nutriments, fuels` | Alternative glosses separated by commas in items 9–21, by semicolons in items 1–8 (`bodily action; physical action`, line 73) (old F9) | Semicolons | 8 |
| 16_class.md:133 | `iti'ss'ime \| sandhi \| ind+pron+pron` | Sandhi rows give the parts in column 3 at 133, 144, 167, 177, 211, 221, 234, 238, 646 …, leave it blank at 83, 95, 101, 107, 115, 198, 264 and in all of items 9–21 (old F10) | One style | 8 |
| 16_class.md:120–122 | `abhiññā[^1] \| verb \| ger` / `sacchikatvā \| verb \| abs` / `upasampajja \| verb \| ger` | `ger` and `abs` for the same form in consecutive rows (also `ger` 242; `abs` 369, 554, 558, 837) (old F11) | owner decision (gerund or absolutive) | 8 |
| 16_class.md:202 | `kammadhāraya > bahubbīhi` | `>` unescaped here and at 269, 272, 281; escaped `\>` at 699, 714, 715, 739 and in class 23 (old F12) | One form | 8 |
| 16_class.md:327 | `vi+√nī･1 a (lead, carry)` | Only root cell in the class with a prefix; `pabbajanti` (106), `vihaññati` (600), `nibbattati` (699) give the bare root (old F13) | `√nī･1 a (lead, carry)` | 8 |
| 16_class.md:481 | `masc.nom.sg (instr)` | Governed case written `(instr)`; `(+instr)` at 304, `(+dat)` at 636, `(+acc)` at 773; `excl +acc` at 628 (old F14) | `(+instr)`; `excl (+acc)` | 8 |
| 16_class.md:314 | `(because of) having knowledge or rather (because of) having lifestyle` | Supplied words in round brackets here and at 377, 638, 733, 803; in square brackets at 158, 191, 285, 668, 750, 776 (old F15) | One bracket style | 8 |
| 16_class.md:612 | `'I have sons, I have wealth'` | Single quotes in a translation; double quotes at 226, 421, 508, 540, 858 (old F16) | Double quotes | 8 |
| 16_class.md:776 | `are dropped (caused to fall), like a mustard seed from the tip of a needle - that one I call a brahmin` | Literal meaning without `lit:` (cf. `(lit: this indeed not)` 226; `lit.` in cells 144, 719, 743, 797); spaced hyphen as a dash (the sentence at 193 uses `—`) (old F17) | `(lit: caused to fall)`; `–`; verify | 7 |
| 16_class.md:432 | `dhārayissasi \| verb \| fut.2nd.sg \| you will hold; will keep; will carry \| \|` | Root cell empty for a plain verb; also `jaññā` (536), `\#amhi` (492), `\#atthi` (593, 597, 606), `sacchikatvā` (121) (old F18) | Fill or state that roots are optional; verify | 6 |
| 16_class.md:563 | `\#vītināmeyyaṃ \| verb \| opt.reflx.1st.sg` | The `-eyyaṃ` optative is tagged reflexive here (DPD does the same) but plain `opt.1st.sg` at 23_class.md:472 (`paccanubhaveyyaṃ`) (old F19) | One tag; verify | 6 |
| 16_class.md:316 | `[AN8.53](https://s.dhamma.gift/an/an8/index.html#an8.53) <br>` | Space before `<br>` in 136 of the 271 numbered sentences that have a `<br>`, none in 135; both in every class (27 and 28: 3 with, 29 without). Key and exercise differ in this at 23 items (old F119) | One form | 9 |
| 17_class.md:305 | `yamahaṃ \| - \| - \| whichever I` | Sandhi rows with `-` instead of `sandhi`: 305, 351, 468, 495, 668; `idappaccayā` (503) is a compound with `-` (old F20) | `sandhi` | 9 |
| 17_class.md:376 | `"...approved of…"` | `...` and `…` in one cell; the sentence at 185 has `...` (old F21) | `…` | 9 |
| 17_class.md:70 | `\#āmisa \| noun \| nt. \|` | Stem gender with a full stop (70, 95, 217, 223, 240, 267, 275, 280, 523, 534, 552, 555, 556, 572, 582, 677), without (66, 69, 317, 357, 387, 463, 477) (old F22) | No full stop | 9 |
| 17_class.md:80 | `of that (gen abs)` | Genitive absolute noted in the gloss column (80–83); the locative absolute is noted in the grammar column (195–196) (old F23) | `masc.gen.sg (gen abs)` in column 3 | 8 |
| 17_class.md:594 | `vi√har･1 a (live)` | Prefix in the root cell here and at 611 (`saṃ+ud√han･1 a`); bare root elsewhere (`vihareyyaṃ` 319, `uttiṇṇo` 112) (old F24) | Bare root | 8 |
| 17_class.md:398 | `<br>(Buddharakkhita): Mind precedes all mental states.` | A second, published translation inside the bold line, after `<br>`; at 426 `(Sujato)` without colon (old F25) | owner decision; one style | 8 |
| 17_class.md:114 | `with (my) hands and (my) feet` | Supplied words in round brackets here, square in the rows (106, 108) and in the same translation (`[was]`, `[and]`) (old F26) | Square | 8 |
| 17_class.md:491 | `'idappaccayā avijjā'ti` | Items 11–19 and extra 7–8 have no sandhi apostrophes, except 301 `vihareyyan'ti`, 450 `paṭipadan'ti` and 491 (old F27) | owner decision (see class 16) | 8 |
| 17_class.md:65 | `purisapuggalo \| noun \| masc.nom.sg \| individual person \| \|` | Compound type missing: class 17 gives it for only three compounds (462, 571, 676); class 16 gives it for all (old F28) | Fill, or state that it is optional; verify | 7 |
| 17_class.md:500 | `pass.pr.3rd.sg` | Voice before tense here and at 502; after tense at 606 (`pr.caus.3rd.sg`) (old F29) | One order; verify | 7 |
| 17_class.md:377 | `aor.3rd.pl +acc` | Governed case without brackets; `(+acc)` at 105, 242, 276 (old F30) | `(+acc)` | 8 |
| 17_class.md:290 | `\#na \| prefix \| \| not, without` | Grammar of the negative prefix blank (171, 180, 290, 588) or `neg` (293, 585, 591) (old F31) | One form | 8 |
| 17_class.md:369 | `\#avoca \| verb \| aor.3rd.sg \| said \| \|` | Item 14 leaves the root empty for `avoca`, `bhagavā`, `bhikkhū`, `bhāsitaṃ`; the same words have roots at 206, 198, 169 (old F32) | Fill; verify | 7 |
| 18_class.md:593 | `(lit.: with)` | Third form of the marker: `lit.` (187, 421, 484), `lit:` (421, 436), `lit.:` here (old F33) | One form | 9 |
| 18_class.md:441 | `thus these two-and-a-half months, ...` | `...` (441, 426, 582, 589) vs `…` (526) (old F34) | `…` | 9 |
| 18_class.md:75 | `\#saṅgha \| noun \| masc. \|` | Stem gender with full stop (75, 76, 109, 116, 118, 126, 131, 133, 151, 259, 436, 460, 461, 472, 476, 493, 507, 537, 543, 555), without (219, 398, 401, 404, 437, 438, 578) (old F35) | No full stop | 9 |
| 18_class.md:3 | `**Dis-join the sandhis**` | The table is derivations (`saṃ + √kath + yā`), not sandhi; class 17 heads the same kind of table `**Disjoin the following words**` (old F36) | `**Disjoin the following words**`; verify | 7 |
| 18_class.md:233 | `vāyodhātū'ti` | Items 5–13 carry no sandhi apostrophes except here (and row 267), 175 `pakkho'ti`, 296 `rūpan'ti`, 362 (old F37) | owner decision (see class 16) | 8 |
| 18_class.md:112 | `n'ādhimuccati \| sandhi \| pr.3rd.sg` | Sandhi row with an inflection tag (also 267, 319); other sandhi rows have a blank or the parts (`ind+pron`) (old F38) | One style; verify | 7 |
| 18_class.md:237 | `puna \| ind \| - \| again` | Empty grammar cells are `-` in items 5–13 (237, 248, 279, 306, 371), blank in items 1–4 and the extras (515, 573, 587) (old F39) | One style | 8 |
| 18_class.md:74 | `saṅghādiseso \| noun \| masc.nom.sg \| offence requiring suspension \| \|` | Compound type given for 6 compounds only (187, 218, 323, 471, 475, 559) (old F40) | Fill or drop; verify | 7 |
| 19_class.md:155 | `kammadhāraya[^6]` | Bahubbīhi marked by a footnote here and at 165, 542, 548; by `kammadhāraya \> bahubbīhi` at 503 and in the analysis line 328 (old F41) | `kammadhāraya \> bahubbīhi` | 8 |
| 19_class.md:320 | `bhaññamānesu \| prp pass \|` | Passive present participle is `prp pass` at 320 and 365, plain `prp` at 267 (`desiyamāne`) and 343 (`bhaññamāne`) (old F42) | One tag | 8 |
| 19_class.md:230 | `\#\#\#samudaya (ca)` | `(ca)` at 230, 231, 265, 266; `[ca]` at 530, 531, 563, 564, 584, 585 (old F43) | One bracket | 8 |
| 19_class.md:442 | `\#uṭṭhāya \| ind \| abs` | Absolutive is `verb \| abs` elsewhere (450, 456); `ger` at 58, 122, 126, 588 (old F44) | `verb \| abs`; owner decision ger/abs | 8 |
| 19_class.md:68 | `saṃ√idh･3 ya (succeed)` | Prefix in the root cell: 68, 170 (`ava√gāh`), 527 (`apa√kam`); bare root for `payojeyya` (62), `upasampajja` (126), `paṭikkanto` etc. (old F45) | Bare root | 8 |
| 19_class.md:62 | `he would engage in (acc)` | Governed case in the gloss; `(+dat)` in the grammar column at 96, `(+gen)` at 565 (old F46) | `opt.3rd.sg (+acc)` | 8 |
| 19_class.md:181 | `have understanding as (their) highest, all things have liberation as [their] core` | Round and square brackets for supplied words in one sentence (old F47) | Square | 9 |
| 19_class.md:240 | `**samudayadhamma \< samudaya + dhamma (kammadhāraya)**` | Items 7–13 and extra 6 add bold analysis lines under the translation (as the instruction at line 43 asks); items 1–6 and extras 1–5 give the type only in column 5; items 7–13 leave column 5 mostly empty (old F48) | One method; verify | 7 |
| 19_class.md:441 | `uṭṭhāyāsanā \| - \| -` | Sandhi rows with `-` instead of `sandhi`: 393, 441, 453, 458 (old F49) | `sandhi` | 9 |
| 19_class.md:535 | `[VIN1.1.2]` | Vinaya label style differs from `VIN PAT PC 57` (class 18) (old F50) | owner decision | 6 |
| 19_class.md:492 | `akuppā cetovimutti - etad'attham'idaṃ, brāhmaṇa, brahmacariyaṃ` | The key adds a spaced hyphen and two commas that the exercise (ex 300) does not have; no final full stop in either (old F121) | Same punctuation in both; `–`; verify | 7 |
| 20_class.md:345 | `**yathāninnaṃ \< yathā + ninnaṃ (avyayībhāva)**` | `avyayībhāva` here and in footnote 17 (185); `abyayībhāva` at 34, 58, 86, 92, 212 (old F51) | `abyayībhāva` | 9 |
| 20_class.md:337 | `paripūreti \| verb \| caus.pr.3rd.sg` | Order `caus.pr`; `pr.caus.3rd.sg` in classes 17–19 (old F52) | `pr.caus.3rd.sg` | 9 |
| 20_class.md:53 | `[DHP064]` | Leading zero; `DHP62`, `DHP356` elsewhere (old F53) | `DHP64` | 9 |
| 20_class.md:393 | `\#visuddhaṃ \| pp. \|` | POS with full stop (393, 397); `adj. (as noun)` at 25 (old F54) | `pp` | 9 |
| 20_class.md:277 | `(tatiyā tappurisa - bahubbīhi)` | Bahubbīhi marked with ` - ` at 277–285, 462, 484, 486; with `\>` at 13, 104, 237–243, 445; with unescaped `>` at 287, 376, 447, 480, 482 (old F55) | `\> bahubbīhi` | 8 |
| 20_class.md:38 | `āvuso \| ind \| voc.sg \| friend; brother` | Third way of tagging `āvuso`: `noun \| masc.voc.pl` (16_class.md:367, 17_class.md:458), `noun \| masc.voc.sg` (classes 23, 25, 27) (old F56) | One tag (DPD: `ind`) | 8 |
| 20_class.md:539 | `vi√cit･8 cha (think, intend)` | Prefix in the root cell: 95, 539, 540, 544, 547, 586, 598; bare root elsewhere in the class (old F57) | Bare root | 8 |
| 20_class.md:228 | `\#pīti (ca)` | `(ca)` at 228, 229, 588–590 (with `[and]` in the gloss); `[ca]` at 10, 11, 504, 505, 510, 513; `(+ca)` at 639, 640 (old F58) | One bracket | 8 |
| 20_class.md:453 | `brāhmaṇā \| noun \| masc.nom.pl \| Brahmans` | `brahmin` in classes 16–19 (old F59) | `brahmins` | 8 |
| 20_class.md:181 | `Based on this, I would take the meaning of samaṇuddesa as … But: cum grano salis.` | Footnotes 16 and 17 are editorial notes in the first person ("I would take", "I wonder if") (old F60) | owner decision | 7 |
| 20_class.md:34 | `abyayībhāva (adverbial compound)` | Type explained in brackets here and at 58; not at 86, 92; `digu (numerical compound)` at 19_class.md:93 (old F61) | owner decision | 6 |
| 21_class.md:30 | `paṇītaṃ \| adj as noun \|` | `adj as noun` (30), `noun or adj` (68), `agent noun` (91, 151), `(agent) noun` (444); `adj (as noun)`, `noun (agent)` in class 20 (old F62) | One notation | 8 |
| 21_class.md:373 | `sameti \| verb \| caus.pr.3rd.sg \| he causes to be calm` | `pr.caus.3rd.sg` for the same word at 17_class.md:606; `pr.reflx.3rd.sg` at 446, 459 (old F63) | tense before voice | 9 |
| 21_class.md:207 | `[UD5.10]` | `UD5.10` here and at 333 (exercise: `UD50`); `UD45` in classes 17 and 19 (old F64) | One label style | 8 |
| 21_class.md:279 | `cedaṃ \| - \| -` | Sandhi rows with `-`: 279, 323, 523, 527 (old F65) | `sandhi` | 9 |
| 21_class.md:34 | `sakyamunī \| noun \| masc.nom.sg` | Metrical lengthening not noted (flagged impossible by the DPD check; also 36, `natthī` 526); noted at 16_class.md:699 `(i \> ī)` (old F66) | Add the note; verify | 7 |
| 21_class.md:78 | `imperf.3rd.sg +acc` | Without brackets; `(+acc)` at 13, `(+loc)` at 55, `(+gen)` at 412 (old F67) | `(+acc)` | 8 |
| 21_class.md:184 | `sabbhireva **samāsetha**` | Items 9–16 and extra 4 have no sandhi apostrophes, except 184 `suggatin'ti`, 207 `gacche'ti`, 239 `n'ātimaññetha`, 267, 298, 357 (old F68) | owner decision (see class 16) | 8 |
| 22_class.md:155 | `**(lit:) A person` | `(lit:)` and `(Figuratively):` in one line: case and colon position differ (old F69) | One form | 8 |
| 22_class.md:182 | `na yito dūraṃ **gamissase** cittā'ti.` | Items 8–14 and extra examples 1, 4–6 have no sandhi apostrophes except `cittā'ti` (182) and `phāsuvihārañcā'ti` (472); items 1–7 and extras 2–3 have them. In extras 4 and 6 the rows add apostrophes the sentence lacks (`appābādhatañ'ca` 494, `mātā'ti` 597) (old F70) | owner decision (see class 16) | 8 |
| 22_class.md:207 | `kātabbaṃ **amaññissaṃ**.` | Target verbs are bold in items 8–14 and extras 4–6, not in items 1–7 or extras 1–3 (old F71) | One way; verify | 7 |
| 22_class.md:203 | `\#iti \| ind \| - \| ""` | Grammar of `iti`: `quotation mark` (40, 54, 61, 117, 131, 424), `-` (203, 599–616), blank (518) (old F72) | `quotation mark` | 9 |
| 22_class.md:273 | `sace \| ind \| - \| if` | Empty grammar cell of indeclinables written `-` (273, 274, 324, 530, 593) or left blank (223, 292, 378, 412); `na` is `neg` (58), blank (350, 378) or `-` (593) (old F73) | One form | 8 |
| 22_class.md:403 | `abhi+ud√gam･1 a (go)` | Only root cell in the class with prefixes; `vinayetha` 26, `vipassati` 169, `upagacchatha` 537 give the bare root (class 21 writes `vi√nas` without `+`) (old F74) | `√gam･1 a (go)` | 8 |
| 22_class.md:457–458 | `\#ñāti (ca) \| noun \| masc.nom.sg \| family` / `\#mittā (ca)` | Dvanda members marked `(ca)` (457, 458, 628) or `(+ca)` (624, 625, 627) (old F75) | One form | 9 |
| 22_class.md:589 | `dve \| adj \| x.nom.pl \| two` | Numeral tagged `adj` with DPD's `x` gender; `eka \| card` at 483, and `tayo`, `cattāro` are `card \| masc.…` in other classes. DPD: `card` (old F76) | `card` (DPD: `dvi` card) | 8 |
| 22_class.md:135; 26_class.md:516 | `asso bhadro kasām'iva` / `etena saccena suvatthi hotu` | No final full stop in the key sentence; the exercise has one (ex 93, ex 355). The reverse at 21:333 and 21:357 (full stop in the key, none in ex 237, 258) (old F122) | Same in both | 8 |
| 23_class.md:267 | `\#patta \| pp \| nt \| reached \| √ap･4 uṇā (reach, attain)` | Three formats in one class: items 1–8 and extras 1–8 put the construction in column 5; items 9–15 and extras 9–11 put it in bold lines under the table; item 9 also has class 16–22 root cells (267, 275, 276, 280) (old F77) | One format | 9 |
| 23_class.md:300 | `idh'āvuso, dhammayogā bhikkhū jhāyī bhikkhū apasādenti, ime pana jhāyino'mhā, jhāyino'mhā'ti` | Sandhi apostrophes in the sentence but not in the rows (`idhāvuso` 304, `jhāyinomhā` 316). Same at 459 / 473, 508 / 532, 764 / 778, 865 / 869 (old F78) | owner decision (see class 16) | 9 |
| 23_class.md:749 | `**anādiya** \| verb \| ger \| not taking up \| na + √ādā + ya` | `ger` at 719, 749, 753; `abs` at 276, 412, 570, 744, 782 in the same class (old F79) | owner decision (ger / abs) | 9 |
| 23_class.md:413 | `mā \| ind \| prohib \| do not` | `prohib` here (also 418, 819, 824); `neg (+aor)` at 73, 77 (old F80) | One form | 8 |
| 23_class.md:152 | `**samāhito** \| pp (as adj.) \| masc.nom.sg` | `pp (as adj.)` with a full stop; `pp (as adj)` at 105, 116; `adj (pp)` at 212, 590, 655; `adj, comparative` at 562 (old F81) | One notation | 8 |
| 23_class.md:883 | `assādato \| noun \| masc.abl.sg \| as the satisfaction, enjoyment` | `-to` forms meaning "as …" are `ind \| adv` in class 22 (`aniccato`, `dukkhato`, 22_class.md:108, 113) and ablative nouns here (883, 887, 891) (old F82) | One treatment: `ind \| adv` in both classes; `assādato` is not a DPD headword, but DPD tags such `-to` forms as `ind, adv` (e.g. `momuhato`): DPD lookup | 6 |
| 23_class.md:875 | `pañcannaṃ \| adj \| x.gen.pl \| of five` | Numeral tagged `adj` with DPD's `x` gender (see 22_class.md:589); `aṭṭha \| card \| x.` at 178 (old F83) | `card` (DPD: `pañca` card) | 8 |
| 23_class.md:41 | `**e.g. viññāṇaṃ : vi + √ñā + aṇa**` | Space before the colon (not at 29); root meaning "(to grasp)" at 35, "(know)" at 45 (old F84) | One form; verify | 7 |
| 23_class.md:472 | `paccanubhaveyyaṃ \| verb \| opt.1st.sg \| I could manifest` | DPD tags `-eyyaṃ` as reflexive opt 1st sg (flagged IMPOSSIBLE); the key tags the parallel `-ssaṃ` futures `fut.reflx.1st.sg` in class 22 (old F85) | owner decision | 6 |
| 24_class.md:24 | `**jāyetha** \| verb \| opt.reflx.pass.3rd.sg` | Order of tense, voice and mood varies: `opt.reflx.pass` (24), `pass.opt.reflx` (22_class.md:261), `pass.pr` (304) against `pr.pass` (23_class.md:130), `caus.pr` (239), `caus.fut` (438), `opt.caus` (509), `abs (caus)` (57) (old F86) | One order | 9 |
| 24_class.md:229 | `seti \| verb \| pr.3rd.sg \| he sleeps \| √sī + a \> se` | Constructions change form within the class: `√root + sign + ending` in items 1–9; base only (229, 391, 396, 447) or `base + ending` without the root (233 `soca + ti`, 239, 286, 301, 304, 596) from item 10; old root cells at 290, 368, 369 (old F87) | One form | 8 |
| 24_class.md:215 | `na \> a + vi + √bhaj + ta` | Negative written `na \> a` (215, 262, 339, 365, 366, 448, 586) or `na` (25, 28, 31, 34, 67, 81, 158, 535, 554, 598) (old F88) | One form | 8 |
| 24_class.md:258 | `abhibhuyya \| verb \| ger \| overcoming` | `ger` here; `abs` at 50, 57, 227, 365, 402; `ind \| abs` at 368 (old F89) | owner decision (ger / abs) | 9 |
| 24_class.md:276 | `**Whoever monks, would say thus, "**` | Items 12–15 split the table into parts with a translation after each; all other items have one table and one translation (old F90) | One layout; verify | 7 |
| 24_class.md:49 | `\#imaṃ \| pron. \| masc.acc.sg \| this[^31] (here)` | `pron.` with a full stop; `masc` without one at 45, 604 against `nt.` at 52 (old F91) | `pron`; `masc.` | 8 |
| 24_class.md:587 | `\#ti \| ind \| - \| ""` | `\#ti` (587, 606) against `\#iti` (107, 145, 242, 383); grammar `quotation mark` (107, 145) or `-` (242, 383) (old F92) | `\#iti \| ind \| quotation mark` | 8 |
| 25_class.md:62 | `kaṇṇasukhā \| adj \| fem.nom.sg \| easy on the ear; pleasant to hear \| catutthī (dat) tappurisa` | `(dat)` added to the type here and at 70, 75 only; `(upapada)` at 412 (old F93) | One form; verify | 7 |
| 25_class.md:225 | `dukkhavipākā \| adj \| masc.nom.pl \| with painful results \| kammadhāraya > bahubbīhi` | `>` not escaped here and at 407; `\>` at 113 and in the other classes (old F94) | `\>` | 8 |
| 25_class.md:230 | `\#jāti ca \| noun \| fem. \| birth and` | Dvanda members marked `jāti ca` here (230–232), `(ca)` / `(+ca)` in classes 22–24; no `dvanda` label on 229 (old F95) | One form | 8 |
| 25_class.md:68 | `\#gamā \| adj. \| fem.nom.sg \| going; able to go` | `adj.` with a full stop (old F96) | `adj` | 8 |
| 25_class.md:152 | `catunnaṃ \| adj \| masc.gen.pl \| of four` | Numerals: `adj \| masc.` here, `adj \| x.` at 534 and 23_class.md:875, `card` at 16, 515 (old F97) | `card` (DPD: `catu` card) | 8 |
| 26_class.md:207 | `10. [MN39](https://s.dhamma.gift/mn/mn39/index.html) <br>ahaṃ kho pubbe ābādhiko ahosiṃ dukkhito bāḷhagilāno, bhattañca me nacchādesi` | Two formats in one class: items 1–9 and extra 1 bold the derivatives and give the construction in column 5; items 10–17 and extras 2–3 have no bold, write `taddhita` in column 5 and put the construction in a bold line under the table. Sandhi apostrophes stop in the sentences from item 10 but stay in the rows (`bhattañ'ca` 220, `porāṇam'etaṃ` 279, `avitakko'mhi` 343) (old F98) | One format | 9 |
| 26_class.md:406 | `**muhu + tta + aṃ (taddhita)**` | `(taddhita)` added to some construction lines (380, 406, 408, 508, 510), not to the others (old F99) | One form; verify | 7 |
| 26_class.md:250 | `vuccati \| verb pass \| pr.3rd.sg \| is called` | Passive marked in the pos cell; `verb \| pr.pass.3rd.sg` at 168, 173 and in the other classes (old F100) | `verb \| pr.pass.3rd.sg` | 9 |
| 26_class.md:344 | `\#avitakko \| adj \| masc.nom.sg \| without thought \| kammadhāraya > bahubbīhi` | `>` not escaped (344, 346, 371, 498, 499); `\>` at 46 (old F101) | `\>` | 8 |
| 26_class.md:522 | `kamma (irreg) \| noun \| nt.acc.sg \| action, deed` | Note on the form inside the word cell; the metrical `abhabba` (530, flagged IMPOSSIBLE as `masc.nom.sg`) has no note (old F102) | Note both the same way; verify | 7 |
| 26_class.md:16 | `akuhako \| (agent) noun \| masc.nom.sg \| who is honest; not deceitful \| na + √kuh + aka` | `(agent) noun`; plain `noun` for the agent nouns `dātā` (33) and `āvikattā` (432) (old F103) | One notation; verify | 7 |
| 27_class.md:373 | `paññāyetha \| verb \| opt.pass.reflx.3rd.sg` | A fifth order for this form (see 24_class.md:24); `phuseyyaṃ \| verb \| opt.reflx.1st.sg` at 341 against `paccanubhaveyyaṃ \| verb \| opt.1st.sg` at 23_class.md:472 (old F104) | One order | 9 |
| 27_class.md:231 | `pahāya \| verb \| ger \| leaving behind` | `ger` at 231, 244; `abs` at 103 (old F105) | owner decision (ger / abs) | 9 |
| 27_class.md:247 | `\#kayirā \| verb. \| opt.3rd.sg \| he would do` | `verb.` with a full stop (old F106) | `verb` | 9 |
| 27_class.md:34 | `ariyasaccāni \| noun \| nt.acc.pl \| noble truths \| kammadhāraya[^39]` | An alternative compound type given in a footnote ("OR chaṭṭhī tappurisa"); in the cell itself at 23_class.md:661 (`(or)`) (old F107) | One way; verify | 7 |
| 27_class.md:462 | `[^46]: Although Cone has not reached the letter s yet` | A dated editorial remark in a footnote (old F108) | owner decision | 6 |
| 27_class.md:96 | `**sammodanīyaṃ** kathaṃ **sāraṇīyaṃ** vītisāretvā` | Bold target words in the sentence differ between key and exercise: bold only in the key at 56 items (22:232, 24:92, classes 25–28), only in the exercise at 19 items (class 18 items 5–12; class 23 from item 9), different spans at 11 items (22:182 and class 23, e.g. `kāya**duccaritena**` against `**kāyaduccaritena**` at 23:636) (old F120) | owner decision: bold the same words in both | 8 |
| 28_class.md:312 | `ce \| ind \| conj \| if` | `conj` here, `cond` for `sace` at 393 and for `ce` at 27_class.md:259; `evaṃ \| ind \| emph` at 314 against `adv` at 256 (old F109) | `cond`; `adv` | 8 |
| 28_class.md:138 | `dīyittha \| verb \| aor.pass.reflx.3rd.sg \| was offered` | Tense first here and in `pr.pass.reflx` (397), voice in the middle; other orders in 24_class.md:24 (old F110) | One order | 8 |
| 28_class.md:225 | `\#**pasuto** \| pp (adj) \| masc.nom.sg (+loc)` | `pp (adj)`; `pp (as adj)` at 95, `adj (pp)` at 353, `noun (as adj)` at 270 (old F111) | One notation | 8 |
| 28_class.md:322 | `ubho \| pron \| nt.acc.dual \| both` | `dual` occurs only here (old F112) | `nt.acc.pl`; verify | 7 |
| 29_class.md:42 | `chando \| noun \| masc.nom.sg +loc \| desire (for)` | Case note without brackets (42, 351, 655, 804, 862); `(+instr)`, `(+acc)`, `(+loc)` at 531, 616, 752, 812, 872 (old F113) | `(+loc)` | 8 |
| 29_class.md:53 | `\#kiṃ \| pron. \| nt.nom.sg \| what?` | `pron.` with a full stop (53, 55, 158, 788); `pron` elsewhere (old F114) | `pron` | 8 |
| 29_class.md:500 | `momuhato \| ind \| adv (masc.abl.sg) \| as very foolish; as completely confused` | Third treatment of a `-to` form meaning "as …" (see 23_class.md:883) (old F115) | One treatment for the `-to` forms; this row agrees with DPD (`ind, adv, abl sg of momuha`), so use `ind \| adv` at 22_class.md:108, 113 and 23_class.md:883 as well | 7 |
| 29_class.md:737 | `santivādo \| adj \| masc.nom.sg \| professing peace; (a proponent of) a doctrine of peace \| kammadhāraya > bahubbīhi` | `>` not escaped (old F116) | `\>` | 8 |
| 29_class.md:177 | `niccheyya \| verb \| ger \| evaluating; discriminating` | `ger` throughout this class (177, 190, 235, 338, 339, 348, 460, 632, 666, 698); `abs` for `disvāna` at 28 (old F117) | owner decision (ger / abs) | 9 |
| 29_class.md:816 | `**he is not led into any adhering (of views) [lit. abode]**` | `[lit. abode]` in square brackets; `(lit: …)` at 170, 492, 558 (old F118) | `(lit: abode)`; verify | 7 |

## G. Links

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 17_class.md:598 | `[ITI87](https://s.dhamma.gift/kn/iti/index.html)` | Itivuttaka link has no anchor; other KN links point to the sutta or vagga (`#ud5.5`, `#snp2.4`) (old G1) | Add the anchor; verify | 7 |
| 17_class.md:637 | `6. VV 52<br>` | Reference without a link (also in the exercise) (old G2) | owner decision | 6 |
| 19_class.md:334 | `[AN3.125](https://s.dhamma.gift/an/an3/index.html#an3.124)` | The exercise has `[AN3.126](…#an3.125)` for the same sentence. `akampittha` closes the Gotamakacetiya sutta, which I believe is `an3.125` on the site (old G3) | verify; align key with exercise | 7 |
| 21_class.md:357 | `[ITI87](https://s.dhamma.gift/kn/iti/index.html)` | No anchor (as at 17_class.md:598) (old G4) | Add the anchor; verify | 7 |
| 24_class.md:92 | `[ITI62](https://s.dhamma.gift/kn/iti/index.html)` | No anchor (as at 17_class.md:598 and 21_class.md:357) (old G5) | Add the anchor; verify | 7 |
| 24_class.md:346 | `[SN46.52](https://s.dhamma.gift/sn/sn46/index.html#sn46.52)/[53](https://s.dhamma.gift/sn/sn46/index.html#sn46.53)` | Double reference in the key; the exercise (ex 272) has `[SN46.53]` only (old G10) | One reference in both | 8 |
| 25_class.md:143 | `6. [DN2.4](https://s.dhamma.gift/dn/dn2/index.html)` | The Kusāvatī passage is from the Mahāsudassana Sutta (DN 17, the fourth sutta of the second volume); the link goes to DN 2. The other DN labels in this key (`DN16.27`, `DN3.13`) are sutta.section. Same in the exercise (91) (old G6) | `[DN17]`, `/dn/dn17/index.html` | 8 |
| 25_class.md:314 | `[ITI100](https://s.dhamma.gift/kn/iti/index.html)` | No anchor (as at 24_class.md:92) (old G7) | Add the anchor; verify | 7 |
| 27_class.md:42 | `2. VIN PAT NID<br>yassa siyā āpatti` | Reference without a link; also `VIN PAT SA` at 252. All other Pātimokkha references are linked (old G8) | Add links (`pli-tv-bu-pm`) | 8 |
| 28_class.md:367 | `[ITI76](https://s.dhamma.gift/kn/iti/index.html)` | No anchor (as at 24_class.md:92) (old G9) | Add the anchor; verify | 7 |

## H. Data to re-verify (forms, references, counts)

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 17_class.md:185 | `[UD45]` | Label is a running number (anchor `#ud5.5`); class 21 uses `UD5.10` for the same book (old H3) | One label style; verify | 7 |
| 18_class.md:362 | `[AN3.83](https://s.dhamma.gift/an/an3/index.html#an3.82)` | Label and anchor differ by one; also AN3.71 → `#an3.70` (499), AN3.51 → `#an3.50` (548) (old H5) | none if intended (two numbering systems); verify | 5 |
| 21_class.md:252 | `kiñci \| pron \| masc.acc.sg \| anyone` | Most editions of Kp 9 read `katthaci na kañci`; the exercise has `naṃ kiñci` too. The tag itself agrees with DPD (`kiñci` 3: masc & nt acc sg of `kaci`) (old A25) | verify the reading of Kp 9 | 5 |
| 21_class.md:424 | `[SN2.8](…#sn2.8) (Dhp 313)` | Linked here, plain text `SN.2.8 (Dhp 313)` in the exercise (old H6) | Align the exercise | 8 |
| 22_class.md:135 | `yo nindaṃ apabodheti, asso bhadro kasām'iva` | The exercise (93) has `apabodhati`; DPD has both forms. Editions differ here (`niddaṃ` / `nindaṃ`, `apabodheti` / `appabodhati`) (old H8) | verify against the source edition; align key and exercise | 6 |
| 22_class.md:157 | `paccuppannañ'ca yaṃ dhammaṃ, tattha tattha vipassati.` | The usual reading of the verse is `yo dhammaṃ` ("whoever sees …"); `yaṃ` in key and exercise. Row 164 and the translation follow `yaṃ` (old H9) | verify the reading | 6 |
| 22_class.md:182 | `[TH206](https://s.dhamma.gift/kn/thag/index.html#thag5.1)` | The verse belongs to the ninth poem of the Fives (Vijitasena, Thag 5.9); the anchor is the start of the nipāta, as the link rule (`#thagN.1`) prescribes (old H10) | owner decision: `#thag5.9` if the site has the anchor | 6 |
| 22_class.md:522 | `[SN35.194](https://s.dhamma.gift/sn/sn35/index.html#sn35.194)` | The log simile (Dārukkhandhopama) is SN 35.241 in the numbering used for item 2 (`SN35.248`), SN 35.200 in PTS. Same label in the exercise (359). The key itself labels the same sentence `SN35.241` at 25_class.md:345 (old H11) | `[SN35.241]`, `#sn35.241` | 8 |
| 23_class.md:115 | `**payata**pāṇi \| adj \| masc.nom.sg \| open-handed; freely giving (lit: stretched-out hand) \| kammadhāraya \> bahubbīhi` | DPD has the headword as `payatapāṇī` (nom.sg in `-ī`; flagged IMPOSSIBLE) and the type as plain kammadhāraya (old H12) | verify the reading (`payatapāṇi` / `payatapāṇī`); the DPD headword is `payatapāṇī`, type `kammadhāraya` | 6 |
| 23_class.md:189 | `**appagabbho** kulesu **ananugiddho**.` | The usual text of the verse has the sandhi `kulesvananugiddho`; here it is resolved (key and exercise) (old H13) | verify; note the resolution | 6 |
| 23_class.md:216 | `[TH257](https://s.dhamma.gift/kn/thag/index.html#thag16.1)` | The verse is from the tenth poem of the Twenties (Thag 16.10); `[TH251]` at 577 is from the fourth (16.4). Both anchors point to the start of the nipāta, as the link rule prescribes (old H14) | owner decision (see 22_class.md:182) | 6 |
| 23_class.md:406 | `13. [MN107](https://s.dhamma.gift/mn/mn107/index.html) <br>cakkhunā rūpaṃ disvā mā nimittaggāhino ahuvattha` | MN 107 has the singular `mā nimittaggāhī hohi`; the plural wording `nimittaggāhino ahuvattha` is that of SN 35.127. Same label at 812 and in the exercise. Judged from memory (old H15) | verify label and link | 6 |
| 24_class.md:246 | `[AN3.91](https://s.dhamma.gift/an/an3/index.html#an3.90)` | Label and anchor differ by one, also `[AN3.101]` → `#an3.100` at 267 (same in the exercise). Other labels follow the numbering of the anchors (old H16) | One numbering in the label | 8 |
| 25_class.md:31 | `[TH257](https://s.dhamma.gift/kn/thag/index.html#thag16.1)` | The verse is from Thag 16.10; anchor at the start of the nipāta by the link rule (old H17) | owner decision (see 22_class.md:182) | 6 |
| 28_class.md:444 | `aṭṭha**padakatā** kesā, **nettā** **añjanamakkhitā**.` | The usual reading is `aṭṭhāpadakatā` (DPD has both headwords). `[TH251]` and `[TH133]` (232) land on the first poem of their nipāta, by the link rule (old H18) | verify the reading; owner decision on the anchors | 6 |
| 29_class.md:143 | `so it seems this is a ghost word in DPD.` | A statement about DPD in a footnote; DPD does list `ādisa` (adj, in comps, from `ādisati`) but derives `etādisa` from `etaṃ + disa` (old H19) | owner decision: keep, reword or remove | 7 |

## I. Further details on the material under review

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 16_class.md:616 | `[DHP389](https://s.dhamma.gift/kn/dhp/index.html#dhp383)` | Label and anchor differ because the site anchors by vagga (also DHP407 → `#dhp383` at 752, DHP338 → `#dhp334` at 670, DHP62 → `#dhp60` at 586). This follows the dhp anchor rule in `kamma/tech.md` (`#dhpA`, first verse of the vagga), so it is not an error (old H1) | None | 8 |
| 16_class.md:833 | `[SNP7](https://s.dhamma.gift/kn/snp/index.html#snp1.7)` | Label style `SNP7` (running sutta number) next to `SNP62` → `#snp5.8` (line 287); the anchor uses vagga.sutta (old H2) | owner decision on label style | 5 |
| 17_class.md:400 | `[AN3.70](https://s.dhamma.gift/an/an3/index.html#an3.69)` | Label and anchor differ by one. The quoted text (`yadapi … alobho tadapi kusalamūlaṃ`) is the Mūla sutta, AN 3.69 in SuttaCentral numbering, so the anchor is right and the label follows another numbering (old H4) | None, or label `AN3.69`; verify | 7 |
| 21_class.md:451 | `[TH251](https://s.dhamma.gift/kn/thag/index.html#thag16.1)` | Label `TH251`; the verse is from the Raṭṭhapāla verses (Thag 16.4). Counting the poems of nipātas 1–15 (247) makes Thag 16.4 poem 251, so `TH251` is the running poem number and `#thag16.1` follows the `#thagN.1` rule in `kamma/tech.md` (old H7) | None, if the count holds; verify | 7 |

## Mechanical detail

Carried from the audit of 2026-11-12. In this pass `mech_checks.py docs/ipc_key --folder-footnotes` gave the same table, index, footnote and convention figures as M1 and M3 (6 604 table rows, no column mismatch, 55 footnote references and 55 definitions with 8 out of order in classes 19 and 27, identical convention counts), and `key_vs_ex.py` gave the same 28 differing sentences as M2. `mech_checks.py` counts footnote 44 correctly, so the false report mentioned in M1 came from the older one-off script. The `verify_key.py` figures in M1 and M4 were not run again.

### M1. Structure

| Check | Result |
| --- | --- |
| Table column counts | 6 604 table rows, no row with a column count different from its table |
| Characters | No `ṁ`, tab, non-breaking space, HTML entity, zero-width character, Cyrillic letter, trailing space, double space or odd number of `**` in any class file. All files are NFC and end with a newline |
| Raw HTML | Only `<br>`: 502 occurrences in classes 16–28, none in class 29 (its stanza blocks rely on plain line breaks; check the rendering when the site is built) |
| Index | `index.md` lists all 14 classes in order; every link text equals the page H1 |
| Footnotes | Ids 1–55 run across the whole course; each is defined once and referenced once. The script reported `[^44]` as never referenced; that is false, the reference is at `27_class.md:224` (`rules[^44]:`, the marker is followed by a colon). Definitions are out of order in classes 19 and 27 and sit in blocks away from their items in most classes (rows in section E) |
| `verify_key.py` word coverage | 63 warnings. None is a new finding: footnote markers attached to a word, multi-word idiom rows such as `atha kho`, `kiṃ nu kho`, `tattha tattha`, reference labels read as words (`VV 52`, `VIN PAT NID`, `(Dhp 313)`), dashes and `…`, bracketed additions (`(passati)`, `(addasa)`, `(ca)`, `(ya)`), bold sub-rows written `**\#word**`, and cells packed with `<br>`. The real ones are rows: `16_class.md:374`, `23_class.md:260`, `26_class.md:174` |

### M2. Key sentences against `docs/ipc_ex/`

272 numbered sentences in classes 16–28 were compared after removing quotes, apostrophes, bold and `<br>` spacing. 28 differ:

| Kind | Items (key line) |
| --- | --- |
| Footnote marker in the key sentence only (no real difference) | 23:69, 23:189, 23:602, 23:636, 25:93, 27:96, 28:35 |
| Different word | 22:135 `apabodheti` / `apabodhati`; 23:764 `asaṅkhāditvā` / `saṅkhāditvā`; 27:226 `apurekkharāno` / `apurakkharāno` |
| Different length | 20:382 (key longer); 23:49 (key shorter); 24:387 (exercise line 299 repeats the last clause, with `uppādessāma` for `uppādessāmi`) |
| Word added in the key | 23:163 `(passati)`; 26:59 `(addasa)` |
| Hyphens or punctuation inside the sentence | 16:193, 19:492, 28:128; final full stop 21:333, 21:357, 22:135, 26:516 |
| Reference label or link | 17:650 (full stop after the label); 19:334 (`AN3.125` / `AN3.126`, different anchors); 21:207 and 21:333 (`UD5.10` / `UD50`); 21:424 (linked / plain `SN.2.8`); 24:346 (`SN46.52/53` / `SN46.53`) |
| Reference after the sentence in the exercise | 21:136 (exercise line 95); 28:149 (exercise line 125) |

Class 29 has no numbered items, so the script skipped it. A separate diff of its verse lines and first-column words found only the hyphen and punctuation differences already listed under class 29.

Exercise-side defects seen on the way (the exercise folder is otherwise out of scope):

- `ṁ` instead of `ṃ`: `ipc_ex/17_class.md:93–103`, `22_class.md:27–37`, `25_class.md:285–301`.
- Curly apostrophe: `ipc_ex/17_class.md:435` (`icc’evaṃ`).
- Two spaces after the item number: `ipc_ex/18_class.md:196`, `246`. No `<br>` after the reference: `ipc_ex/24_class.md:445`.

Formatting drift between the two folders: bold target words only in the key at 56 items, only in the exercise at 19, different spans at 11; ` <br>` against `<br>` at 23 items.

### M3. Convention counts (classes 16–29)

| Item | Count | Note |
| --- | --- | --- |
| Straight `'` | 976 | Mostly sandhi apostrophes in Pāli. One curly `’`: `27_class.md:458` (`a man’s purity`) |
| Straight `"` | 578 | No curly double quotes |
| `...` / `…` | 43 / 19 | Both in classes 17–19, 21, 23–26, 28; only `...` in 20, 22, 27, 29 |
| ` - ` / `–` / `—` | 245 / 14 / 2 | ` - ` is mostly the `-` placeholder in an empty cell; `—` only at `16_class.md:193` and `22_class.md:303` |
| `lit:` / `lit.` | 124 / 80 | Both in every class; class 27 has 25 / 1 |
| `\>` | 106 | No `→` |
| Root notation `･` / `×` | 1 160 / 58 | Classes 16–22 give `√root･group sign (gloss)` in column 5; from class 23 on the column holds constructions (`pa + √vis + a + ti`), with 10 leftovers of the old style in classes 23–25 and 28 |
| `ger` / `abs` in tag cells | 32 / 56 | Per class (ger/abs): 16 3/5, 17 1/5, 18 0/5, 19 4/5, 20 5/2, 21 2/6, 22 0/1, 23 3/11, 24 1/8, 25 1/5, 26 0/1, 27 2/1, 28 0/0, 29 10/1 |
| `Pāli` / `Pāḷi` | 0 / 0 | The word is not used in the key |
| Translation lines without final punctuation | 8 of 326 | `17:256`, `19:462`, `19:626`, `22:230`, `22:386`, `23:600`, `24:440`, `28:467`. Not counted: class 29 verse lines and the part-translations of split tables (`18_class.md:452–479`, class 24 items 12–15) |

### M4. Advisory DPD form check (`verify_key.py --course ipc --dpd`)

5 717 rows: 1 294 confirmed, 2 345 ambiguous, 1 972 skipped, 85 IMPOSSIBLE, 21 NOT-FOUND, 4 ROOT-MISMATCH. The 110 flagged rows were looked at during the read. Those that are real are rows in sections A and B and say "flagged" in `Problem`. The others are metrical or sandhi forms, stems in compound sub-rows, and tags where the key follows the sentence and DPD lists only the headword's usual use. The 2 345 ambiguous rows were not reviewed one by one.
