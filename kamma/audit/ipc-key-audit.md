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

## The GOLDEN RULE

When apply approved suggestions:

Always correct corresponding sentences and tables in the docs/ipc_ex/ since there we have exercise related to this class, just without gramatical analisis but still with tables and maybe something from here will be relevant there. key and ex need to be synced.

**SBS sync.** Every key sentence is also stored in the SBS table of dpd-db (`class_*` fields, `class_anki` = class number), which feeds Anki and the other exports, so the SBS table must correspond to the key. When a fix changes a key sentence's translation, its Pāli text, or the POS/headword of a word (e.g. noun → adj/pp, a separate DPD row), find and update the SBS rows with `uv run python kamma/audit/scripts/sbs_sync.py` (`check <key file> --since <rev>` lists what the edit put out of sync; `replace`, `set`, `move`, `clear` change the DB, dry run until `--apply`). Get the owner's approval before writing to the DB.

**Word gloss vs sentence translation.** When a fix changes the gloss, POS or reading of a word in the analysis table, check the sentence translation below the table and change it to match (and then the SBS translation, see above). A table-only fix leaves the translation telling a different story (e.g. `vo` changed from "surely" to "your" in 27_class.md, but the translation kept "surely").

**Moving an item between main and Extra.** When an approved fix moves an exercise item from the main list to `## Class N Extra` or back (e.g. it turns out to be an irregular case):
1. Move the whole item (header line with its link, Pāli line, table, bold translation) byte for byte, in the key and in `docs/ipc_ex/` together; no line may be lost.
2. Append it at the end of the target list, then renumber both lists in both files (only the leading `N.` of each item header).
3. SBS: set `class_extra=extra` on the item's rows when it moves to Extra, `class_extra=` (empty) when it moves to main: `uv run python kamma/audit/scripts/sbs_sync.py set <id> class_extra=extra` (dry run, then `--apply` after approval and a backup). `check` does not compare `class_extra`; confirm with a query on `class_anki` + `class_source`.
4. Run `uv run python scripts/verify_key.py`; it must exit 0.
5. Log the move in "Item moves (main ↔ Extra)" below. Move rows are a permanent record: they are **not** removed when applied, only their Status changes.

## Item moves (main ↔ Extra)

One row per move, kept after it is applied. Item numbers are the ones at the time of the move; the Source column identifies the item after later renumbering. Status: `proposed` → `approved` (owner) → `applied <commit>`; a rejected proposal is removed. Paths are relative to `docs/ipc_key/` and `docs/ipc_ex/`. No move recorded yet.

| Date | File | From | To | Source | Reason | SBS (`class_extra`) | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |

## A. Pāli and grammar content errors

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 16_class.md:229 | `bhante \| noun \| masc.voc.sg \| venerable sir \| √bhad×1 a (be good, lucky)` | DPD derives `bhante` from `bhavant` (√bhū). Flagged ROOT-MISMATCH by `verify_key.py --dpd`. Same at 17_class.md:671 and 20_class.md:454 (old A2) | `√bhū･1 a (be, become)` or leave the root empty | 8 |
| 16_class.md:44 | `vutti + assa \| vuttassa` | `i + a` normally gives `y` (`vutyassa`, the Kaccāyana example); `vuttassa` looks like the genitive of `vutta` (old A5) | verify; probably `vutyassa` | 6 |
| 16_class.md:56 | `nu + ayaṃ \| nāyaṃ` | Expected `nvāyaṃ` (`u + a > vā`, as in `kho + ayaṃ > khvāyaṃ` on line 59); `nāyaṃ` is `na + ayaṃ` (old A6) | verify | 5 |
| 17_class.md:516–518 | `evañcetaṃ \| - \| - \| even if this` / `\#ce \| ind \| - \| if` | AN10.61 `evañcetaṃ … vuccati, atha ca pana …` is usually resolved `evaṃ + ca + etaṃ` ("and though this is said") (old A11) | verify which fits AN 10.61: DPD has both `evaṃ + ce + etaṃ` ("even if this", the key's reading) and `evaṃ + ca + etaṃ` ("and this is the case") | 5 |
| 19_class.md:377–380 | `sīlakathāya \| noun \| fem.gen.sg (gen abs)` … `kacchamānāya \| prp pass \| fem.gen.sg (gen abs)` | Feminine `-āya` is also locative, and the usual absolute is the locative (cf. `abhikkantāya rattiyā … (loc abs)` at 430–431) (old A19) | verify; probably `fem.loc.sg (loc abs)` | 6 |
| 19_class.md:544 | `\#dūrā \| adj \| masc.nom.pl \| far away` | In `kīva dūr'ev'ime` the elided word is more likely the adverb `dūre` ("how far away") (old A20) | verify; `\#dūre \| ind \| adv` is possible (DPD has the adverb `dūre` beside the adjective `dūra`) | 6 |
| 20_class.md:645, 649 | `uttarimanussadhammā \| noun \| masc. \| superhuman attainments` / `\#dhammā \| noun \| masc.nom.pl \| states` | Case missing on the compound row; in `natthi … uttarimanussadhammā alamariyañāṇadassanaviseso` it is ablative singular ("beyond the human state"), not nom.pl. Row 632 is also one `\#` level too high (it belongs under `\#manussadhammā`) (old A22) | `masc.abl.sg`; `\#\#dhammā \| noun \| masc.abl.sg`; verify the case (DPD confirms the compound as masc, `uttari + manussadhamma`, which supports moving row 632 one level down). DPD: lists this MN12 sentence under the noun uttarimanussadhamma (masc) 'super-power', matching the key's reading; case not settled | 7 |
| 22_class.md:250 | `\#evaṃ \| ind \| \| thus` | `evāhaṃ` is `eva + ahaṃ`; the sandhi row (222) is glossed "I just" and the translation has "I just thought" (old A31) | `\#eva \| ind \| emph \| just`. DPD: evāhaṃ is sandhi evaṃ + ahaṃ (so I; thus I), so \#evaṃ stands | 9 |
| 22_class.md:495 | `sakhā \| noun \| masc.nom.pl \| companions` | DPD: `sakhā` is nom.sg of `sakha` (flagged IMPOSSIBLE). `\#ñāti (ca)` at 457 is also tagged `masc.nom.sg` inside a plural dvanda (old A34) | verify; `masc.nom.sg \| companion` (DPD: `sakha` masc, atta group; the inflection table is not in the headword output: DPD lookup) | 6 |
| 23_class.md:322 | `\#āvuso \| noun \| masc.voc.sg \| friends, brothers` | Singular tag with plural glosses (flagged IMPOSSIBLE; DPD: `ind`, voc sg and pl) (old A63) | `ind` (DPD: ind, voc sg & pl), or `masc.voc.pl`; as in class 16 | 8 |
| 24_class.md:192 | `addasā \| verb \| imperf.2nd.sg \| you saw \| √dis + a \> disa \> dasa (irreg)` | DPD knows `addasā` only as imperf 3rd sg (flagged IMPOSSIBLE); the address `samaṇa` makes the sense second person (old A68) | verify; note the form | 6 |
| 25_class.md:553 | `**tevijjā + ka**` | DPD: `tevijja + ka`, adjective "related to the three Vedas"; row 514 tags `tevijjaka` as a noun, "master of three vedas" (old A86) | `tevijja + ka` (DPD); DPD has the word as an adjective, so check the `noun` tag at 514. Done 2026-11-25 in ipc_key/25_class.md; left: noun tag of tevijjaka; DPD has tevijjaka as adj (related to the three Vedas) | 7 |
| 25_class.md:191–192 | `aveccappasādena \| noun \| masc.instr.sg \| with perfect clarity; absolute faith \| syntactical compound` / `\#avecca \| ind \| ger` | DPD: `kammadhāraya avecca + pasāda`, and `avecca` as `ind` (flagged IMPOSSIBLE). "syntactical compound" occurs only here (old A88) | owner decision | 6 |
| 26_class.md:103 | `anatthasañhito \| adj \| masc.nom.sg \| unprofitable; unbeneficial \| kammadhāraya` | Member gloss is "connected with" (100); DPD: `tatiyā tappurisa anatthena + saṃhita` (old A90) | `tatiyā tappurisa`. DPD: anatthasañhita (the key's spelling) is typed chaṭṭhī tappurisa anatthena + sañhita; anatthasaṃhita is tatiyā tappurisa. DPD is inconsistent, so not applied | 8 |
| 26_class.md:278 | `\#\#sat \| ind \| \| good; right; true` | `sat` in `sappurisa` is an adjective, not an indeclinable; `\#\#purisaṃ \| noun \| masc.` (261) has an accusative ending with a stem tag (old A93) | `adj`; `\#\#purisa` (DPD: `sappurisa` = kammadhāraya `sat + purisa`; `sat` itself was not looked up: DPD lookup). Done 2026-11-25 in ipc_key/26_class.md (\#\#purisaṃ → \#\#purisa); left: adj for sat. DPD: sat is ind (in comps, abbrev of santa) | 7 |
| 26_class.md:408 | `**vipanna + diṭṭhi + ī (taddhita)**` | The word in the verse is `vipannadiṭṭhi` with short `i`, and DPD gives no suffix (`kammadhāraya > bahubbīhi vipanna + diṭṭhi`) (old A95) | Remove the line, or `vipanna + diṭṭhi` (DPD) | 8 |
| 27_class.md:32 | `\#sat \| ind \| \| true; good` | `sat` in `sappurisa` is an adjective (see 26_class.md:260) (old A98) | `adj` (see 26_class.md:260; `sat` itself was not looked up: DPD lookup). DPD: sat is ind (in comps, abbrev of santa), not adj; not applied | 7 |
| 27_class.md:485 | `pāva \| verb \| perf.3rd.sg \| revealed, told of \| √vad + a + a` | The construction shows no source for the `pā-`; DPD: `pāv + a` (old A106) | `pāv + a` (DPD; root `√vad`) | 7 |
| 28_class.md:33 | `**maṅgalam'uttamaṃ** \| sandhi \| \| highest blessing \| kammadhāraya` | Two inflected words joined by sandhi (members 30–31 are both `nt.nom.sg`) given a compound type (old A108) | Remove the type | 8 |
| 28_class.md:49 | `**jarā** \| noun \| fem.abl.sg \| from old age \| √jar + ā` | The feminine ablative singular is `jarāya` (flagged IMPOSSIBLE); `yāva jarā` is a set phrase (old A116) | verify; note the form | 6 |
| 29_class.md:32 | `\#ragaṃ \| noun \| masc.acc.sg \| lust; passion (m.c. for rāgaṃ)` | The three accusatives are the names of Māra's daughters, as the translation (35) says; DPD: `ragā`, fem, "name of one of the three daughters of Death" (flagged IMPOSSIBLE as masc) (old A118) | `fem.acc.sg`; drop the m.c. note. Done 2026-11-25 in docs/ipc_key/29_class.md (fem.acc.sg); left: dropping the m.c. note (would delete a note) | 8 |
| 29_class.md:134 | `\#bhavūpapattiṃ \| noun \| fem.acc.sg \| rebirth (or re-arising) into existence \| kammadhāraya` | DPD: `dvanda bhava ca upapatti ca`, "state of being and rebirth" (old A120) | `dvanda`, "state of being and rebirth" (DPD: `bhava ca upapatti ca`). Done 2026-11-25 in docs/ipc_key/29_class.md (type dvanda); left: gloss and translation (131, 141) would replace existing text | 7 |
| 29_class.md:233 | `te \| pron \| nt.acc.pl \| them` | `te` is masculine (it resumes `vinicchayā`, masc); the neuter is `tāni`. Same for `ete \| pron \| nt.acc.pl` at 336 (old A123) | `masc.acc.pl`; verify. DPD: te is listed as nt nom/acc pl of ta as well as masc; te can resume yāni (nt), so nt.acc.pl stands | 7 |
| 29_class.md:775 | `\#vedaṃ \| noun \| nt.acc.sg \| knowledge; understanding` | `veda` is masculine in DPD (old A128) | `masc.acc.sg`. DPD: veda 3 is nt, 'knowledge; understanding' (the key's gloss); vedaṃ nt acc sg is valid | 8 |
| 29_class.md:478 | `\#āgā \| verb \| imperf.2nd.sg \| you have come \| ā +√gam +ā` | DPD knows `āgā` only as imperf 3rd sg (flagged IMPOSSIBLE); spaces missing in the construction. Same question for `n'āddakkhi \| verb \| aor.2nd.sg` (486), where the translation adds "(lit: he did not see)" (old A129) | verify; `ā + √gam + ā` | 6 |

## B. Tables, paradigms and lists that disagree with each other or themselves

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 16_class.md:103–105 | `samma'd'eva \| sandhi` / `\#sammā` / `\#eva` | The inserted consonant `d` has no row, while the first table writes `sammā + [d] + akkhāto` (line 23). Same for `puna'r'eva` (686), `sāsapo'r'iva` (764), `ta'y'idaṃ` (296) (old B7) | owner decision: show `[d]`, `[r]`, `[y]` or not | 6 |
| 16_class.md:362 | `sambhavesīnaṃ \| noun \| masc.gen.pl \| for those seeking birth` | Tag genitive, gloss dative ("for") (old B9) | `masc.dat.pl`, or gloss "of those seeking birth"; verify | 6 |
| 17_class.md:311 | `vihareyyan'ti` | Sentence has an apostrophe, the row (318) has `vihareyyanti` (old B11) | Same form in both | 9 |
| 17_class.md:171–173 | `tathārūpaṃ \| adj \| nt.acc.sg` / `\#rūpaṃ \| noun \| nt.acc.sg \| kind; type` | In `evarūpaṃ` (126) the same member is `adj \| fem.acc.sg \| of kind; of type` (old B16) | One treatment of the member `rūpa` in `tathārūpa` and `evarūpa`; `noun \| nt` fits (DPD types both as kammadhāraya with `rūpa`, and does not tag the member) | 7 |
| 17_class.md:461–462 | `tathā \| ind \| adv \| such` / `tathā \| ind \| adv \| such` | Repeated adverb split into two rows; `tato tato` at 646 is one `idiom` row (old B17) | One treatment; verify | 7 |
| 17_class.md:287–288 | `m'ānubyañjanaggāhī \| adj \| masc.nom.sg \| don't be [one] enticed by the details` / `\#mā \| ind \| neg` | Sandhi of `mā` + compound tagged as one adjective; the sandhi part and the compound members are mixed in one level of `\#` rows (old B18) | `sandhi` row, compound rows at `\#\#`; verify | 7 |
| 18_class.md:385 | `seyyathā'pi gunnaṃ` | Sentence has the apostrophe three times, the rows (371, 377, 383) have `seyyathāpi` (old B21) | Same form in both | 9 |
| 18_class.md:137 | `\#cetaso \| adj \| masc.nom.sg \| having an immeasurable mind` | Member row carries the gloss of the whole compound; same at 494 (`\#soto \| adj \| masc.nom.sg \| with applied ear`) (old B22) | `noun … mind`; `noun … ear`. DPD: cetasa is adj, in comps (with mind; having mind), not a noun; sota (ear) is nt, not masc | 8 |
| 18_class.md:125 | `byāpajjati \| verb \| pr.3rd.sg (+acc)` | The sentence construes it with the locative (`appiyarūpe rūpe`), like `adhimuccati … (+loc)` at 114 (old B23) | `(+loc)`, as the sentence has it; DPD lookup (the headword output gives no case) | 6 |
| 19_class.md:274 | `\#tathāgatena \| noun \| masc \| (by) Realised One; Buddha` | Inflected form with a stem tag; also 307, 399 (`\#samayaṃ \| noun \| masc`), 563 (`\#vitakkā [ca] \| noun \| masc.`). Items 1–6 tag such members fully (`\#saddhāya \| noun \| fem.instr.sg`, 141) (old B33) | `masc.instr.sg`, or the stem `tathāgata` | 8 |
| 19_class.md:275 | `\#pavedita \| pp \| -` | Items 7–13 and extra 6 give the last member as a bare stem with `-` (263, 272, 277, 282, 308, 315, 318, 407, 446, 449, 620, 623); items 1–6 and extras 1–5 give the inflected form (`\#pabbajitena \| pp \| masc.instr.sg`) (old B34) | One method | 8 |
| 19_class.md:223–225 | `\#samudaya` / `\#dhamma` / `\#anupassī` | Three members at one level here and at 221–223; nested (`\#`, `\#\#`, `\#\#\#`) for the third compound (228–233) and in the analysis lines 251–263 (old B37) | Nest all three; verify | 7 |
| 19_class.md:303 | `**atthaveda \< atthā + veda (pañcamī tappurisa)**` | Ablative written `atthā`, `dhammā` (293) here, `atthasmā`, `dhammasmā` in the table (271, 276) (old B39) | One form; verify | 6 |
| 19_class.md:26 | `aṭṭhiṃ + katvā \| aṭṭhiṃkatvā` | Written as two words in class 18 (`aṭṭhiṃ katvā \| idiom`, 18_class.md:484) (old B40) | one treatment: `aṭṭhiṃkatvā` as one word in class 18 as well (DPD headword: abs, comp vb). CST: suttas write aṭṭhiṃ katvā as two words; DPD has both the idiom aṭṭhiṃ katvā and aṭṭhiṃkatvā (comp vb) | 7 |
| 20_class.md:453 | `**visuddhamatta \< visuddha + atta (kammadhāraya)**` | The table (392–394) treats `visuddhamattānaṃ` as a sandhi of two accusatives (`visuddhaṃ` + `attānaṃ`); same for `vimuttamatta` (443 vs 396–398) (old B45) | One analysis | 8 |
| 20_class.md:18 | `\#cittaṃ \| noun \| nt.nom.sg \| a mind` | Last member of `abyāpannacitto`; in `byāpannacitto` (166) it is `\#citto \| noun \| masc.nom.sg` (old B46) | One form | 8 |
| 20_class.md:91, 188 | `abyayībhāva[^17]` / `[^17]: So also Ñāṇatusita, but puna(r) is an ind.` | The first sentence of the footnote is about `punakammāya` (line 97), but the marker is on `yathādhammaṃ` (old B54) | Move the marker, or split the note; verify | 6 |
| 20_class.md:234 | `pītisukhaṃ \| noun \| nt.acc.sg \| joy and happiness \| dvanda \> bahubbīhi` | Plain `dvanda` for the same word in the same formula at 19_class.md:583 (old B58) | `dvanda` (DPD: the noun is `dvanda`; `dvanda > bahubbīhi` is the adjective). DPD: pītisukha 2 (adj) is dvanda > bahubbīhi and here qualifies jhānaṃ (analysis line agrees); fix may be POS adj, not the type | 8 |
| 20_class.md:642 | `natthi \| verb \| pr.3rd.sg \| there is not` | Split as sandhi `na + atthi` in class 16 (532, 604) (old B59) | One treatment; verify | 7 |
| 21_class.md:197, 210 | `sataṃ saddhammamaññāya` / `saddhammam'aññāya \| sandhi` | Row has an apostrophe, the sentence has none (old B62) | Same in both | 9 |
| 21_class.md:52–53 | `khaṇ'ātītā \| noun \| masc.nom.pl \| … \| kammadhāraya\> bahubbīhi` / `\#khaṇaṃ \| noun \| masc.acc.sg` | An accusative first member means `dutiyā tappurisa`, not `kammadhāraya`; space missing before `\>` (old B64) | `dutiyā tappurisa \> bahubbīhi`. Done 2026-11-25 in 21_class.md (space before >); left: none. DPD: khaṇātīta is kammadhāraya > bahubbīhi (khaṇa + atīta), not dutiyā tappurisa | 8 |
| 21_class.md:458 | `tatreko \| adj \| masc.nom.sg \| there one` | Sandhi (`tatra + eko`) tagged `adj`; also 257 (`nāññamaññassa \| pron`), 385 (`idheva \| ind`), 418 (`nappaṭiggaṇhāti \| verb`), 526 (`natthī \| verb`) (old B69) | `sandhi`. Done 2026-11-25 in 21_class.md (tatreko, nāññamaññassa); left: idheva, nappaṭiggaṇhāti (no sub-rows), natthī (DPD: natthi is pr) | 8 |
| 22_class.md:140 | `sabbaṃ \| pron or ind \| nt.acc.sg \| all <br>entirely; completely` | Two readings in one row; the grammar cell fits only the pronoun. The translation uses "all suffering" (old B78) | One reading, or two rows; verify | 7 |
| 22_class.md:289 | `paññāyetha \| verb \| pass.opt.reflx.3rd.sg \| would be evident` | Three notations for the same form: `verb \| pass.opt.reflx.3rd.sg` (261, and `labbhetha` 321), `verb \| opt.reflx.3rd.sg` (357), `verb. pass \| opt.reflx.3rd.sg` (596) (old B84) | One notation | 9 |
| 22_class.md:361 | `mā ahesun'ti \| verb \| aor.3rd.pl \| may they not be` | `mā`, `ahesuṃ` and `iti` merged in one row tagged as a verb; elsewhere `mā` has its own row and `…'ti` is a sandhi row with sub-rows (old B86) | Split. DPD: mā ahesuṃ is an idiom (ind + aor), so a plain split is an owner call | 9 |
| 22_class.md:454–455 | `\#kiñci \| pron \| masc \| anything; something; some` / `\#mattaṃ \| noun \| masc.acc.sg \| amount; measure` | The same compound twelve rows below (432–433) has `\#kiñci \| ind \| \|` and `\#mattaṃ \| adj \| masc.acc.sg`. The compound is `nt.acc.sg` in both places, its member `masc.acc.sg` (old B87) | One analysis; `nt.acc.sg` | 9 |
| 23_class.md:47 | `**Please pay attention to the syntax: underline the subject, object(s), and predicate of the sentences**` | The key repeats the instruction but marks no subject, object or predicate anywhere; bold marks the prefixed words instead. No final full stop (27 has one) (old B93) | owner decision | 6 |
| 23_class.md:210 | `\#kicco \| noun (ptp) \| masc.nom.sg \| obligation (for); duty (for); work (for)` | Neuter member nouns given the compound's masculine ending: `kicco` here, `\#indriyo \| noun \| masc.nom.sg \| senses; mental faculties` at 206 (plural gloss too). `\#vutti \| noun \| fem.nom.sg` (203) and `\#sotaṃ` (355) keep their own gender (old B95) | One treatment | 8 |
| 23_class.md:301 | `**adhi + √kar + aṇa**` | In items 9–15 and extras 9–11 the constructions stand as bold lines under the table without naming the word they analyse; identical lines repeat (292 = 294) (old B98) | Name the word; verify | 7 |
| 23_class.md:699 | `ariyasāvako \| noun \| masc.nom.sg \| a noble disciple \| chaṭṭhī tappurisa<br>(or)<br>kammadhāraya` | Two types here, one (`chaṭṭhī tappurisa`) for the same word at 101; the member rows fit the tappurisa only. `<br>` in the type cell (old B103) | One treatment | 8 |
| 23_class.md:856 | `10. [MN107](https://s.dhamma.gift/mn/mn107/index.html) <br>cakkhunā rūpaṃ disvā mā nimittaggāhino ahuvattha` | Extra example 10 (812–863) repeats exercise item 13 (406–457) word for word: sentence, table, constructions, translation. The exercise file has it twice as well (ex 267, 530) (old B104) | owner decision: replace or remove | 9 |
| 23_class.md:808, 828 | `gahetvā sahasā asaṅkhāditvā ajjhohari` / `asaṅkhāditvā \| verb \| abs \| having not chewed; without having chewed` | The exercise (ex 504) has `**saṅkhāditvā**`, the opposite meaning ("having chewed"). The key row and translation follow `asaṅkhāditvā`. DPD has both headwords (old B156) | verify the reading in the source edition; same word in key and exercise. CST (s0302m.mul.txt SN 20.10): main text saṅkhāditvā; asaṃkhāditvā only as variant (katthaci). Exercise follows CST; key follows the variant | 8 |
| 23_class.md:49 | `so navaṃ santh'āgāraṃ **pavisati**, saddhiṃ mahesiyā brāhmaṇena ca **purohitena**.` | The exercise (ex 51) gives the long sentence (`so puratthimena nagarassa navaṃ santhāgāraṃ kārāpetvā kesamassuṃ **ohāretvā** kharājinaṃ **nivāsetvā** …`) with three more bold target verbs; the key analyses only this shortened sentence, so about 15 exercise words have no key (old B158) | Same sentence in both | 9 |
| 23_class.md:171; 26_class.md:62 | `(passati) dukkhaṃ dukkha**samuppādaṃ**` / `(addasa) **āsītikaṃ** vā **nāvutikaṃ** vā` | The key adds a supplied verb in brackets to the Pāli sentence; the exercise (ex 127, ex 50) does not have it, and it has no table row (old B159) | owner decision: in both, or in the translation only | 7 |
| 24_class.md:49 | `kumbh'ūpamaṃ \| adj \| masc.acc.sg \| like a clay pot \| kammadhāraya` | Adjective compounds typed without the bahubbīhi step: 44, 51 (DPD: `kammadhāraya > bahubbīhi`); with it elsewhere in the key. `(as bahubbīhi)` at 354 is a third notation (old B105) | `kammadhāraya \> bahubbīhi` (DPD: `kumbhūpama`, `nagarūpama`). Done 2026-11-25 in ipc_key/24_class.md (lines 49, 56); left: (as bahubbīhi) notation at aññatitthiyānaṃ, owner decision | 8 |
| 24_class.md:111 | `anaññātaññassāmī't'indriyaṃ \| sandhi \| nt.nom.sg \| the faculty that senses "I will know the unknown" \| kammadhāraya` | Sandhi row carrying grammar and a compound type (old B106) | Blank; or tag as noun; verify | 7 |
| 24_class.md:169, 171 | `khādanīyaṃ \| ptp \| nt.acc.sg \| uncooked food; food to be chewed` / `bhojanīyaṃ \| noun \| nt.acc.sg \| cooked food (lit: to be savored)` | Parallel words, `ptp` and `noun` (old B108) | One tag | 8 |
| 24_class.md:252, 256 | `kiṃsu \| pron \| nt.acc.sg \| what?` / `kissassu \| - \| - \| of which?` | `kiṃsu` as a pronoun (flagged IMPOSSIBLE; DPD: `ind`), unsplit; `kiṃ'sū` at 22_class.md:9 is a sandhi with `\#kiṃ` and `\#sū`. `kissassu` has sub-rows but `-` for pos (old B110) | `sandhi` in both. Done 2026-11-25 in ipc_key/24_class.md (kissassu as sandhi); left: kiṃsu. DPD: kiṃsu is ind, adv, comp (kiṃ + su), not a sandhi | 8 |
| 24_class.md:673–676 | `asaddhammassavanantissa \| sandhi \| \| "not hearing the pure teaching"` / `\#saddhamma \| noun \| masc \| true, good teaching` | Compound members stand directly under the sandhi row with no compound row; "pure" in the sandhi gloss, "true, good" in the member, "true" in the translation (old B116) | Add `\#asaddhammassavanaṃ`; one rendering; verify | 7 |
| 25_class.md:366 | `13. [SN35.241](https://s.dhamma.gift/sn/sn35/index.html#sn35.241) <br>evam'eva kho, bhikkhave, sace tumhe'pi na orimaṃ tīraṃ upagacchatha` | The same sentence is analysed at 22_class.md:522–547 with other tags: `evameva kho \| idiom` with sub-rows (here `ind`), `tumhepi \| sandhi` (here `pron`), `majjhe \| adj` (here `noun`, 362); "veer to" at 356, "veer towards" at 360 (old B123) | Align the two | 8 |
| 25_class.md:448 | `pubbarattā'pararattaṃ \| sandhi \| adv \|` | Apostrophe after `ā` in the table, before it in the sentence (`pubbaratt'āpararattaṃ`, 402); `\#bhāvanā'nuyogam` (432) ends in `m`, the other members in `ṃ` (old B124) | `pubbaratt'āpararattaṃ`. Done 2026-11-25 in ipc_key/25_class.md; left: \#bhāvanā'nuyogam ending in m | 9 |
| 25_class.md:533–538 | `aho \| ind \| excl \| I say! Oh!` / `aho vata re \| ind \| excl \| oh!` | Three rows for the first `aho vata re`, one merged row for the second and third (507, 512) (old B125) | One treatment; verify | 7 |
| 26_class.md:207 | `ottappiyaṃ \| noun \| nt.nom.sg \| fear of wrongdoing` | Secondary derivatives left without bold or construction although the task is to find all of them: `ottappiyaṃ` (191), `pārivattakā` (126), `upanāhī` (363), `thenakehi` (506), `dukkhito` (216) (old B129) | Add or state the selection; verify | 6 |
| 26_class.md:241 | `nacchādesi \| verb \| aor.3rd.sg \| it did not please` | Unsplit sandhi rows tagged as words: `nacchādesi` (224), `ajjatanām'iva \| adj` (286, has sub-rows), `natthi \| verb` (303), `cā'ti \| ind` (329), `muhuttam'pi \| ind` (398), `seyyathāpi \| ind` (493), `kiñ'c'āpi \| ind` (520), `idam'pi \| pron` (539) (old B130) | `sandhi` with sub-rows. Done 2026-11-25 in ipc_key/26_class.md (sandhi + sub-rows for ajjatanām'iva, cā'ti, muhuttam'pi, seyyathāpi, kiñ'c'āpi, idam'pi); left: nacchādesi, natthi. DPD lists both as single words (aor, pr) | 9 |
| 26_class.md:315, 319 | `bahubhāṇinaṃ \| adj \| masc.acc.sg \| who talks a lot \| kammadhāraya` / `\#mitabhāṇiṃ \| adj \| masc.acc.sg \| one who talks in measure \| dutiyā tappurisa` | Parallel compounds typed differently (DPD: kammadhāraya for both, with `> bahubbīhi` for the first); `\#bhāṇinaṃ` (296) and `\#\#bhāṇiṃ` (300) for the same stem (old B131) | One type | 8 |
| 26_class.md:490 | `\#ambilaggehi \| adj \| masc.instr/abl.pl \| predominantly sour \| kammadhāraya` | Four parallel compounds: the first is `instr/abl` and not bold, the others `instr` and bold (460, 465, 470); the third has no type (465) (old B135) | Align | 8 |
| 27_class.md:109–111 | `ekam'antaṃ \| sandhi \| \| to one side` / `\#eka \| card \| masc. \| one` | The first member of the sandhi is the inflected `ekaṃ`, given as a stem with a stem tag (old B137) | `\#ekaṃ \| adj \| masc.acc.sg`; verify | 7 |
| 27_class.md:476 | `pajahati \| verb \| pr.3rd.sg \| gives up; abandons \| pa + √hā + a + ti<br>with metrically lengthened ā` | The row has `pajahati`, the sentence (433) `pajahāti`. DPD lists `pajahāti` as an irregular form, not a metrical one. `<br>` in the cell (old B139) | `pajahāti`; verify the note. Done 2026-11-25 in ipc_key/27_class.md (word → pajahāti); left: the metrical note. DPD: pajahāti is an irregular form, not metrical | 8 |
| 27_class.md:482 | `diṭṭhī[^50] \| noun \| masc.nom.sg \| who has a view; who has the opinion` | Footnote 50 says the masculine reading "leaves the following pāva without a subject"; the translation (458) makes exactly this word the subject: "the one with view revealed him" (old B140) | Reword the footnote; verify | 7 |
| 27_class.md:384–386 | `na'y'idaṃ \| sandhi \| \| not this` / `\#idaṃ \| pron \| nt.nom.sg \| this` | Third treatment of `idaṃ` in `nayidaṃ` (see 22_class.md:255); the inserted `y` has no row, unlike `[r] inserted between vowels` at 427 (old B141) | One treatment; verify | 7 |
| 27_class.md:243, 259 | `kāmehi ritto **apurekkharāno**,` / `**apurekkharāno** \| prp \| masc.nom.sg` | The exercise (ex 180, 193) has `apurakkharāno`. The same verse in class 29 has `apurekkharāno` in key (650) and exercise. DPD has both headwords (old B157) | One spelling in key and exercise. CST: SN22.3 (s0303m) reads apurakkharāno (var. apurekkharāno sī.); the other copies of the verse read apurekkharāno | 8 |
| 28_class.md:417–418 | `tayo \| card \| masc.acc.pl \| three` / `sukhe \| noun \| nt.acc.pl \| comforts; pleasures` | Numeral masculine, its noun neuter (old B146) | One gender for numeral and noun; DPD has `sukha` as nt only, and `-e` is a masculine accusative plural ending: verify the form (inflection table: DPD lookup) | 6 |
| 29_class.md:91–93 | `etādisaṃ[^53] \| adj \| nt.acc.sg \| such as this; of this type \| kammadhāraya` / `\#ādisaṃ \| adj \| nt.nom.sg \| kind; quality` | The table analyses `eta + ādisa`; footnote 53 calls `ādisa` "a ghost word in DPD" and gives `etad + disa` (DPD: `alutta dutiyā tappurisa etaṃ + disa`). Member tagged `nt.nom.sg` under an accusative; `nt.acc.sg` at 139. Same conflict at 217: footnote 55 argues against the `masc.nom.pl` tag in the row (old B147) | Follow the footnote or drop it | 8 |
| 29_class.md:73 | `naṃ \| pron \| nt.acc.sg \| her` | Neuter tag, "her" in the gloss, "it" in the translation (76) (old B149) | One reading | 8 |
| 29_class.md:325 | `asīlatā(ya) \| noun \| fem.instr.sg \| without moral conduct` | The same line is analysed again at 412 with `asīlatā` and no `(ya)`; `sīlabbaten'āpi` is "also by" at 297 and "even by" at 386 (old B151) | One analysis | 8 |
| 29_class.md:378–380 | `iti māgaṇḍiyo \| sandhi \| \| "...[said] Māgaṇḍiya"` / `iti \| ind \| quotation mark \| ""` | Two separate words tagged as sandhi; the member rows have no `\#` (the same words at 220–221 are plain rows) (old B152) | Remove the sandhi row | 9 |
| 29_class.md:662, 674 | `apurekkharāno \| prp \| masc.nom.sg \| … \| na + pure + √kar + o + āna` / `kayirā \| verb \| opt.3rd.sg \| he should do; he should make \| √kar + o + eyya` | The same verse is analysed at 27_class.md:226–248 with other constructions (`na + pure + √kar + āna`, `√kar + iya + ā`) and glosses (`kathaṃ` "speech; talk" there, "argument; debate" here) (old B154) | Align the two | 8 |
| 29_class.md:241 | `ajjhatta-santī'ti yam'etam'atthaṃ` | Repeated verse lines differ in punctuation from the stanza block: 239 (no comma; 208 has one), 480 (no comma; 448), 494 (no full stop; 449), 719 (comma; 675 full stop); `māgaṇḍiyāti` at 446, 453 against `māgaṇḍiyā'ti` at 147, 267 (old B155) | Same text in both places. Done 2026-11-25 in docs/ipc_key/29_class.md and docs/ipc_ex/29_class.md (commas at 239, 480; full stop at 494, per stanza and CST); left: 719 vs 675 (CST has ;) and māgaṇḍiyāti vs māgaṇḍiyā'ti (apostrophe owner decision) | 8 |

## C. Translation and gloss problems

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 16_class.md:902 | `As soon as he saw the Fortunate One` | `bhagavā` is "the Blessed One" in the row (838), "the Buddha" at 404, 412 and 421, "the Fortunate One" here (old C2) | One rendering | 8 |
| 16_class.md:858 | `\#anusayānaṃ \| noun \| masc.gen.pl \| of underlying tendency` | Same word in one sentence glossed three ways and in the singular: "of underlying tendency" (815), "of sleeping tendency" (822, 829); compounds "latent tendencies" (813), "inherent tendency" (820), "dormant views" (827); translation "latent tendencies" (old C3) | One gloss, plural; verify | 7 |
| 16_class.md:391 | `But I also say, friends, that without reaching the end of the world, (there is) no ending of suffering.` | "also" has no source word; `na … vadāmi` is "I do not say" (old C4) | "But I do not say, friend, that there is an ending of suffering without having reached the end of the world."; verify | 6 |
| 17_class.md:357 | `a disciple of the Buddha reflects in this way` | Row 332 glosses `ariyasāvako` "a disciple of the noble one". `bhagavato` is "the Buddha's" at 322 but "of the Blessed One" in rows 308, 374 and translations 208, 380, 662 (old C5) | One rendering per term | 8 |
| 17_class.md:135 | `vadeyyaṃ \| verb \| opt.reflx.1st.sg \| I myself should say` | `-eyyaṃ` is the ordinary 1st sg optative; "myself" (also in the translation, line 137) over-translates the ending (old C6) | "I should say"; verify | 7 |
| 17_class.md:509 | `in this very fathom length body with its perception and intelligence (is) the world, the source of the world` | Does not follow the Pāli syntax (`lokañca paññāpemi` = "I declare the world …"); `samanake` is "with mind" in row 467, "intelligence" here (old C7) | "… that in this very fathom-long body, with its perception and mind, I declare the world, …"; verify | 6 |
| 18_class.md:80 | `[this is a case] relating to the community in the beginning and in the end.` | The row (74) glosses `saṅghādiseso` "offence requiring suspension"; member 77 "remains; remainder" does not give "in the end" (old C9) | One rendering in row and translation; DPD: "offence requiring communal rehabilitation" (`saṅgha + ādi + sesa`) | 7 |
| 18_class.md:286 | `"In this very body there is the solid state, the liquid state, the fire state and the air state."` | No `eva` in `atthi imasmiṃ kāye` ("very" belongs to `imameva kāyaṃ` earlier). Rows: `āpodhātu` "liquid state", `vāyodhātū'ti` "gaseous state" (267) vs "air state" here (old C10) | "In this body …"; one gloss per element; verify | 7 |
| 18_class.md:98 | `Whichever of these human beings [are] seers. (Thus said venerable Puṇṇaka)` | `ye` (row 85) not rendered; `isayo manujā` are two nominatives ("these seers and men"); full stop missing inside the bracket (old C13) | "Whatever seers and men here … (thus the venerable Puṇṇaka)"; verify | 6 |
| 18_class.md:210 | `One should touch unstable and firm beings with kindness` | Row 187 glosses `tasathāvarāni` "the moving and unmoving, lit. trembling and steady" (old C14) | One rendering; verify | 6 |
| 19_class.md:337 | `preached by the Such Become One` | `tathāgata` is "Realised One; Buddha" in the rows (262, 307), "the Buddha" at 285, "the Such Become One" here (old C15) | One rendering | 8 |
| 19_class.md:581 | `(source text uses past tense)[^15]` | The quoted sentence has present tense verbs (`ujjhāyanti khiyyanti vipācenti`, tagged `pr` in rows 552–554), and footnote 15 says the opposite ("The historical present can be translated in the past tense") (old C17) | Remove the bracket or reword: "(historical present)"; verify | 7 |
| 19_class.md:651 | `proliferations, perceptions and concepts regarding forms` | Row 612 glosses `papañcasaññāsaṅkhā` "proliferation of opinions, concepts and constructs; (or) classification of diverse perceptions"; three renderings of one compound (old C18) | Align with one of the analyses at 632–636; verify | 6 |
| 19_class.md:135 | `an individual, having personally experienced in this life directly knowing by himself the liberation of the mind without taints, liberation by wisdom, dwells having reached [this state].` | Hard to read; the same clause is translated more clearly at 16_class.md:125 (old C19) | Reword on the model of class 16; verify | 6 |
| 20_class.md:238 | `jhānaṃ \| noun \| nt.acc.sg \| stage of meditation` | "state of deep meditative calm" at 522 and 19_class.md:587; translation at 526 "fourth stage of meditation" against its own row 522 (old C20) | One gloss; verify | 7 |
| 20_class.md:229–230 | `savitakkaṃ \| adj \| nt.acc.sg \| with thinking` / `savicāraṃ \| … \| with discursive thought` | `vitakka`/`vicāra` are "thoughts"/"examinations" (19_class.md:562), "thinking"/"examining" (19_class.md:574–579) and "thinking"/"discursive thought" here (old C21) | One pair; verify | 7 |
| 20_class.md:242 | `joy and happiness born from solitude` | Row 224: "born from separation" (old C22) | One word; verify | 7 |
| 20_class.md:377 | `\#saṅghāṭidhāraṇa \| noun \| nt. \| wearing an outer robe` | `saṅghāṭi` is "patchwork robe" at 360, 362, 365 and in the translation, "outer robe" at 366–367 (old C24) | One gloss; verify | 7 |
| 20_class.md:316 | `an excess of speech is to be expected. When there is an abundance of talk` | `kathābāhulla` rendered two ways in one sentence (rows 299, 303 likewise) (old C25) | One rendering; verify | 7 |
| 20_class.md:80 | `[Even] if a fool associates closely with a wise person for the rest of his life` | "Even" is in the text (`api`, row 61, glossed "just; only"), so not a supplied word; row 57 says "as long as one lives", not "the rest of" (old C27) | "Even if … for his whole life"; `api` "even"; verify | 7 |
| 20_class.md:472 | `garlanded with aquatic plants; aquatic plant garland maker` | Translation 478 has "who wear moss garlands" (old C28) | One rendering; verify | 6 |
| 21_class.md:175 | `āgamaṃ \| verb \| aor.reflx.1st.sg \| I myself have come` | Reflexive endings translated literally throughout the class: "I myself" (165, 175, 291, 296, 319–321), "associate oneself" (191), "make oneself" (193), "one oneself gets" (459), "you could get yourself" (521). In verse these are ordinary middle forms (old C30) | owner decision; plain active in translations | 7 |
| 21_class.md:440 | `One stills thoughts and plans` | `vicāritāni` is "thought about; contemplated; investigated" (372), "examinations" in 17_class.md:613 for the same line (old C32) | One rendering; verify | 7 |
| 21_class.md:565 | `"Let the venerables regain what is your own; do not let what is your own get lost."` | Person switches ("the venerables … your"); row 492 "must try (to) (get back)" (old C33) | "Venerables, regain what is yours; …"; verify | 6 |
| 21_class.md:597 | `They wander around at peace, not opposing a view with views. In them, what could you get yourself` | `ye … tesu` ("those who … from them") is rendered as two independent sentences; `pana` and `idha` are not translated (old C34) | "But those who wander … not opposing a view with views, from them what could you get, Pasūra, …?"; verify | 6 |
| 22_class.md:36 | `Alas, you slept (lit: sleep) badly! Where do I (myself) sleep today?` | Follows the wrong tag at 18; `sessaṃ` is future (so tagged at 22, but glossed "I myself sleep") (old C35) | "Alas, I slept badly! Where will I sleep today?". Done 2026-11-25 in ipc_key/22_class.md (you slept > I slept; do I > will I); left: (lit: sleep) and (myself) kept, owner to decide | 9 |
| 22_class.md:98, 111 | `ādittato'haṃ \| sandhi \| \| I [am] as on fire` / `I am as on fire, [although] engaged in serenity; when will I see with wisdom this state for myself?` | `ādittato` ("as blazing") is the complement of `dacchaṃ`: "when will I … see this as blazing". Reading it as a predicate of `ahaṃ` forces the supplied "[although]" (old C36) | verify; "When will I, yoked to serenity, see this with wisdom as ablaze?" | 6 |
| 22_class.md:146 | `(They have seen) in what is non-self as 'non-self', they have perceived what is foul as foul.` | "in what is non-self as" is not English; tense changes from "saw" to "have perceived" within the verse; "Taking upon themselves" for a compound glossed "who have undertaken" (122) (old C37) | "(They saw) what is non-self as non-self, they saw the foul as foul. Having undertaken right view, …"; verify | 7 |
| 22_class.md:171 | `A person, restrained by conscience, exists somewhere in the world` | `koci` is "any; some(one)" (row 143), not "somewhere"; `bhadro` glossed "good; fortunate" (150), translated "fortunate horse" (old C38) | "Some person … exists in the world"; "good horse"; verify | 6 |
| 22_class.md:379, 390 | `asaṅkhataṃ \| pp (as noun) \| nt.nom.sg \| unfabricated` / `unmade and uncreated … the made and the created.` | Row glosses "unfabricated", "of the fabricated" (355); translation "uncreated", "the created" (old C43) | One rendering | 8 |
| 22_class.md:408, 418 | `devo \| noun \| masc.nom.sg \| rain cloud` / `and if the rain clouds would not provide thorough downpour from time to time` | Singular in the row, plural in the translation; "If there were no" for `nevassa` (row 366 "not even would be") (old C44) | Align; verify | 6 |
| 22_class.md:459 | `evañ'ca \| sandhi \| \| and if` | Gloss "and if"; members are "thus" and "and". The translation also drops "thus": "having said [this]" (old C45) | "and thus"; verify | 7 |
| 22_class.md:337 | `saṅkhārā \| noun \| masc.nom.pl \| mental intentions; thought processes` | Rows: "mental intentions" (307, 318, 323, 326, 330); translation (333): "mental processes" (old C47) | One rendering; verify | 6 |
| 23_class.md:414, 419 | `tathāgatassa \| noun \| masc.gen.sg \| of the Thus-Become-One` / `cover the body of the Tathagata, in worship of the Tathagata.**` | Row gloss and translation differ; `Tathagata` without diacritics (old C51) | One rendering; verify | 7 |
| 23_class.md:464 | `akusalā \| adj \| masc.nom.pl \| unhealthy` | "unhealthy" in the row (also 841), "unwholesome" in the translation (457), "unskillful" for the same word at 247 (old C52) | One rendering; verify | 7 |
| 23_class.md:590 | `\#api \| ind \| \| only; just` | In `attabyābādhāyapi` `api` is "also; even" ("could lead also to my own harm"); the translation (547) leaves it out. Same gloss in `seyyathā'pi` at 558 (old C54) | "also; even"; verify. Done 2026-11-25 in ipc_key/23_class.md (attabyābādhāyapi \#api now also; even); left: seyyathā'pi \#api (DPD seyyathāpi = just as) not changed | 7 |
| 23_class.md:978 | `the satisfaction as satisfaction, the danger as the danger, and the escape as the escape` | Article in two of three; "danger" for a word glossed "disadvantage" (884–887); "unsurpassed perfect enlightenment" against "the highest enlightenment" (904); `evaṃ` not translated (old C58) | Align; verify | 6 |
| 24_class.md:506 | `no \| pron \| 1st.dat.pl \| for us` | Plural "for us" / "we will have" (455) inside a first person singular reflection ("I will destroy … I will not cause"); the usual text of the formula has `me`. Key and exercise read `no` (old C64) | verify the reading. CST: MN107 reads yātrā ca me bhavissati (me, not no) | 6 |
| 24_class.md:681 | `And monks, lack of belief has a fuel, it is not fuel-less.` | `assaddhiyampāhaṃ … vadāmi` ("lack of faith too, I say, has …") loses "too" and "I say"; "lack of belief" for a word glossed "disbelief, lack of confidence" (old C65) | "Lack of faith too, monks, I say has a fuel"; verify | 7 |
| 25_class.md:30 | `the deities belonging to the (Heaven of the) Thirty Three proclaimed aloud.**` | `saddaṃ` (row 26) is not translated; comma missing after "Kings" (old C66) | "raised the cry"; verify | 6 |
| 25_class.md:273 | `bhavanti \| verb \| pr.3rd.pl \| there are, there will be` | "there are" at 249, "there are, there will be" at 259, future in the translation (264) (old C70) | One rendering; verify | 6 |
| 26_class.md:165 | `**And just as they would eat (or, were eating) the flesh of [their] son, they would beat their breasts` | `c'eva … ca` is "both … and" (row 140 "and just"), not "just as" (old C71) | "They would both eat the flesh of their son and beat their breasts"; verify | 7 |
| 26_class.md:603 | `by the truth of this statement, may you be well!**` | `suvatthi hotu` is "may there be well-being" (rows 545–546); commas missing in "by body speech or mind" (old C75) | "may there be well-being"; verify | 6 |
| 26_class.md:489, 509 | `**ambil**'aggehi'pi \| sandhi \| \| just predominantly sour` / `**khārikehi**'pi \| sandhi \| \| even hot` | `api` is "just" in the first four items and "even" in the last four, while every member row says "just"; the translation (487) has neither (old C76) | "also" throughout; verify | 6 |
| 27_class.md:121–123 | `oḷārikassa'pi \| sandhi \| \| even of gross` / `\#api \| ind \| \| but` | "even" in the sandhi row, "but" in the member row and in the translation (138) (old C77) | One rendering; verify | 7 |
| 27_class.md:359, 365 | `te \| pron \| 2nd.dat.sg \| by you` / `that you do not feel and could not be felt by you?**` | `na ca te hoti 'phuseyyan'ti` is "nor does it occur to you: 'I might feel [them]'"; row 340 has "I would myself touch". Opening quotation mark of the translation never closed (old C79) | "and of which you do not think 'I might feel them'"; verify | 7 |
| 27_class.md:427 | `should sit down or lie down hard on a bench or on a bed with detachable legs` | Order reversed against `mañcaṃ vā pīṭhaṃ vā` (bed, bench) (old C80) | "on a bed or a bench"; verify | 6 |
| 28_class.md:120 | `**The trees laden with pollen exude a sweet smell all around by means of flower pollen; the first month of the season, spring, [is] pleasant` | "pollen" translated twice; `paṭhamavasanto sukho utu` is "early spring is a pleasant season" (row 97: "first month of spring; early spring") (old C82) | "The trees, covered with flower pollen, exude a sweet smell all around; early spring is a pleasant season"; verify | 7 |
| 28_class.md:140 | `**One gives to a newcomer, one gives to a traveller, one gives to one who is ill, one gives during a famine.**` | `dānaṃ` ("a gift", rows 114–123) is not translated (old C85) | "One gives a gift to …"; verify | 6 |
| 29_class.md:307, 309 | `\#āha \| verb \| perf.3rd.sg \| it is said (i.e. I say; speak)` / `**also not by virtue and practice, do I speak of purity.**` | Third person tag, first person translation; the same line at 394–396 is "one speaks" (old C87) | One reading; verify | 7 |
| 29_class.md:735 | `**and unsullied by water and mud,**` | `ca` joins `jalena` and `paṅkena` ("by water and mud"); the first "and" is extra (old C88) | "unsullied by water and mud"; verify | 6 |
| 29_class.md:862 | `\#saññaṃ \| noun \| fem.acc.sg \| label; concept; idea; notion` | "and perception" in the sandhi row (855), "notion(s)" in the translation (864), "perception" for the same word at 829 (old C89) | One rendering; verify | 7 |

## D. English typos and grammar

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 16_class.md:410 | `Monks there are these two things. What two? Effort and tranquility.` | Comma missing after the vocative; `tranquility` here, `tranquillity` in row 392 (old D4) | "Monks, there are …"; one spelling. Done 2026-11-25 in 16_class.md (comma); left: tranquility/tranquillity spelling (UK/US owner decision) | 8 |
| 17_class.md:151 | `[like] a monkey wishing only for fruit in a forest grove.` | Translation starts in lower case; also 648 `thus like this chattering` (old D14) | Capital; verify | 6 |
| 18_class.md:452 | `"...hot season and so` | Quotation mark not closed (old D18) | Close or remove | 8 |
| 18_class.md:178 | `Monks, ill will is an obstruction` | `ill-will` in row 162 (old D21) | One spelling; verify | 7 |
| 18_class.md:312 | `With oneself truly well-tamed<br>one obtains a protector that is hard to get.` | Lines 1–3 of the verse start with a capital, line 4 does not (old D22) | One style; verify | 6 |
| 19_class.md:191 | `[^6]: as bahubbīhi, qualifying dhammā` | Footnotes 6, 7, 10, 12, 14 start in lower case and have no full stop; 3, 5, 9, 11, 13, 15 are full sentences (old D37) | One style; verify | 7 |
| 20_class.md:584 | `dreadlocked ascetics` | `dread-locked` in the translation (600) (old D43) | One spelling | 8 |
| 20_class.md:423 | `**for one who is happy delight arises.**` | Partial translations 411, 421, 439 start in lower case; 403 and 431 with a capital (old D45) | One style; verify | 7 |
| 20_class.md:283 | `[he speaks] reasonable, within a limit and [what is] advantageous.` | Ungrammatical (old D46) | "[he speaks words that are] reasoned, measured and beneficial"; verify | 6 |
| 20_class.md:468 | `from Western lands; belonging to the western district` | Capital W (also 478) (old D47) | lower case; verify | 6 |
| 21_class.md:189 | `"imperf. of pa5 + ✓vac;? or aor. of pa5 + avati2;?"` | `✓` (check mark) for `√`; `pa5`, `avati2` keep the source's superscript homonym numbers (old D51) | `√vac`; remove or superscript. Done 2026-11-25 in 21_class.md (√vac); left: pa5, avati2 homonym numbers | 8 |
| 21_class.md:457 | `they quarreled` | US spelling (also 420); UK elsewhere (`unskilful`, 367, 390) but `skillful` at 100 and 296 (old D52) | One spelling | 8 |
| 22_class.md:231 | `you won't go far from here, mind".**` | Full stop outside the closing quotation mark here and at 520; inside at 133, 333 (old D61) | One way; verify | 7 |
| 22_class.md:253 | `√an･1 a (breath, blow)` | Noun "breath" among verb meanings; same at 16_class.md:527, 530, 20_class.md:23, 21_class.md:66 (old D62) | DPD lookup; "breathe"; verify | 6 |
| 23_class.md:335 | `jhāyinomhāti \| sandhi \| \| we are meditators" \|` | Closing quotation mark with no opening one; also `I will sit"` at 732 (old D64) | Remove or pair | 9 |
| 23_class.md:443, 448 | `focusing on prominent features` / `focussing on the secondary characteristics` | Two spellings five rows apart (again at 820, 825); `misbehavior` (667, 670, 673) beside `realised` (907) (old D68) | owner decision (UK/US) | 8 |
| 23_class.md:607 | `[and] torture [him]....**` | Four dots; translations without a final full stop at 600; `" ...` at 547 (old D69) | `…` | 8 |
| 23_class.md:915 | `and as long as I, lit. how long - that long – and - I` | Hyphens and an en dash mixed in one gloss (old D70) | One dash | 8 |
| 24_class.md:181 | `ima designates what is nearest, accantasamipa, either physically or in thought` | `accantasamipa` for `accantasamīpa`; first person editorial note ("I did not note this earlier") (old D74) | `accantasamīpa`; owner decision on the voice. Done 2026-11-25 in ipc_key/24_class.md (accantasamīpa); left: owner decision on the first-person voice | 8 |
| 25_class.md:578 | `brāhmaṇo \| noun \| masc.nom.sg \| Brahman` | "Brahman" here and at 549; "brahmin" at 536 and in class 24 (old D90) | One spelling; verify | 7 |
| 26_class.md:291 | `who has entered a unalterable fixed course, entered the level of the superior man` | "a unalterable"; "superior man" for a compound glossed "honourable man" (258) (old D94) | "an unalterable"; one rendering. Done 2026-11-25 in ipc_key/26_class.md (an unalterable); left: one rendering for superior / honourable man | 9 |
| 27_class.md:133, 135 | `when practiced (lit: like gone along)` / `for (those who are) practising; lit. gone along` | "practiced" and "practising" in adjacent rows; "practice" as a verb at 138 (old D98) | owner decision (UK/US) | 8 |
| 27_class.md:146 | `ko jaññā maraṇaṃ suve,` | Quotation ends with a comma (old D99) | Full stop or `?` | 8 |
| 27_class.md:238 | `should be made to do by one of three rules[^44]:` | Not English (footnote 44 gives the readable version); the third of three parallel phrases drops the brackets: `according to a case` (old D100) | Use the footnote wording; verify | 7 |
| 28_class.md:308 | `tirelessly throughout the day and night, – it is, indeed, he` | Comma followed by a dash (old D106) | One mark | 8 |
| 28_class.md:173 | `mahābrahmā \| noun \| masc.nom.sg \| great God almighty; supreme spirit` | "God" here, "god" at 156, 159 and in the translation (181); "you're" at 331 (old D109) | One form; verify | 7 |
| 29_class.md:382 | `nor by knowledge, ([said] Māgaṇḍiya")**` | Closing quotation mark inside the bracket, with no opening one for it; "nor even by virtue and observance(s) that one speaks of purity" (396) has a stray "that" (old D112) | Fix | 8 |
| 29_class.md:781, 798 | `**He who has perfect knowledge [does] not by view, nor by thought**` / `**go to conceit, he is not made-of-that` | Sentence split so that neither half reads; line translations start with a capital at 544, 607, 690, 717, 775, 849 and in lower case elsewhere (old D116) | Reword; one convention; verify | 7 |

## E. Markdown defects that affect rendering

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 17_class.md:251 | `*[+m]*` | Italic note about the inserted `m` in the root column; nothing similar elsewhere (old E6) | owner decision (cf. `[d]` in class 16) | 7 |
| 18_class.md:600 | `aññen'eva pādaṃ karomī"ti.` | Closing `"` with no opening one (the inner quote uses `'…'`); row 589 repeats it (old E8) | `karomī'ti` or add the opening quote | 9 |
| 18_class.md:82 | `"ye kec'ime isayo manujā, (icc'āyasmā puṇṇako)` | Opening `"` never closed (old E9) | Remove or close | 9 |
| 18_class.md:226 | `**(the reading tathārūpassa also exists)**` | Note formatted like a translation line, between two halves of one table; same at 407 (`**vipallāsa = vi + pari \> …**`) (old E10) | Footnote or plain text; verify | 7 |
| 18_class.md:233 | `√su･4 ṇā (hear) (ssu in comps) +ta+ā` | Extra derivation note appended to the root cell (old E11) | Root only; verify | 7 |
| 19_class.md:402 | `āloko pātubhavissatī"ti?` | Closing `"` with no opening one; repeated in row 410 (old E13) | Add the opening quote or drop this one | 9 |
| 19_class.md:521 | `\#ceto (or)<br>\#cetaso \| noun (as adj) \| -<br>masc.gen.sg \| mind<br>of mind` | Two alternative rows stacked in one row with `<br>`; also 499 and 173 (`sattamī tappurisa<br>or <br>kammadhāraya`) (old E14) | Two rows, or a footnote; verify | 7 |
| 19_class.md:585 | `    **Bh. Bodhi puts it nicely: "The bahubbīhi is not a different kind of compound …"**` | Bold, indented continuation paragraph of footnote 13 (old E15) | Plain text; verify | 6 |
| 21_class.md:549 | `mā vo sakaṃ vinassā"ti.` | Closing `"` with no opening one (also row 499) (old E23) | Add or remove | 9 |
| 21_class.md:187–192 | `[^20]: Cone s.v. āha, āhu …` | Footnotes 20–24 are defined in one block after item 8 (old E25) | After their items; verify | 7 |
| 23_class.md:765 | `bhāsitaṃ \| noun or<br>pp \| nt.acc.sg \| utterance; saying<br>what is said` | `<br>` in the pos and gloss cells (old E32) | owner decision (`<br>`) | 7 |
| 23_class.md:274 | `[VIN5.4.7](https://s.dhamma.gift/vin/tv/pli-tv-kd14/index.html) tiṇavatthārakaṃ<br>` | A topic word after the reference, before the `<br>`; no other item has one (`verify_key.py`: "sentence word has no row") (old E58) | Remove, or put it in brackets; verify | 7 |
| 24_class.md:640 | `    **Cf. Syntax, p. 231: "The subjective Gen. can also be regarded` | A long quotation set wholly in bold, indented as a continuation of footnote 35. Footnotes 31–32 are defined after item 6, 33–35 after extra 4 (old E38) | Plain text; definitions after their items; verify | 7 |
| 24_class.md:629 | `√dis + a + **āvī**` | Bold inside the construction cell (not at 126); `bhuttāvī` (156) bold in the sentence, not in the table (old E39) | One way; verify | 7 |
| 25_class.md:91 | `***pema + anīya***` | Constructions are set in italics (15, 23, 98, 389, 406), partly in italics (44 `*tila* + \*a`), in bold italics (87, 89), in bold (166–172, 199–205) or plain (36, 60, 120, 391) (old E40) | One style | 8 |
| 25_class.md:143 | `    **Cf. Māgadhabhāsā, p. 128: "The future passive participle can also function as a verb` | Long quotations in bold, indented under footnotes 36 and 37 (137, 141); footnote 37 is in the first person ("which I have not seen elsewhere"); marker in the pos cell (`adj[^37]`, 115) (old E42) | Plain text; owner decision on the voice | 7 |
| 25_class.md:478 | `bhūta + pubba + aṃ[^38]` | A footnote in the construction cell whose whole text is "kammadhāraya" (496, defined after extra example 4) (old E43) | Put the type in the cell | 8 |
| 25_class.md:126 | `**dvayena** \| adj \| masc.instr.sg \| by twofold; dual; double \| dvi + \*a` | Target words are bold in the table here and in extra examples 3–4; not in items 1–4 (15, 23, 36, 65) or extras 1–2, though bold in the sentences (old E45) | One way; verify | 7 |
| 28_class.md:267 | `\#**rattā (ca)** \| noun \| nt.nom.pl \| nights and \| ratti + a` | Bold covers `(ca)`; bold before the `\#` at 140, 166, 168, 178, 353, 423, 435, after it at 94, 99, 169, 224, 246. `vasī` (175) bold in the table, not in the sentence (old E54) | One way | 8 |
| 28_class.md:451 | `is obtained; is found<br>(used here in pl.)` | `<br>` in the gloss cell (old E55) | owner decision (`<br>`) | 7 |
| 29_class.md:17 | `disvāna taṇhaṃ aratiṃ ragañ'ca,` | The stanza blocks (17–20, 78–81, 147–150, …) are four or six consecutive lines with no `<br>` and no trailing spaces, so Markdown joins them into one paragraph; the other classes use `<br>` (old E56) | verify in the built site | 7 |

## F. Convention drift

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 16_class.md:629 | `iti \| ind \| quotation mark \| ""` | Grammar of `iti` written four ways: `quote` (219), `quotation mark` (598), `-` (334, 419, 446, 496, 538, 564, 856), `adv` (232) (old F6) | One label | 8 |
| 16_class.md:427 | `na \| ind \| - \| not` | `na` is `neg` elsewhere (183, 363, 435); `-` at 411 and 533. In general items 9–21 and extra 7–8 fill empty grammar cells with `-`, items 1–8 leave them blank (old F7) | `neg`; one way to mark an empty cell. Done 2026-11-25 in 16_class.md (neg at both na rows); left: one way to mark an empty cell | 8 |
| 16_class.md:325 | `neso dhammo neso vinayo netaṃ satthusāsananti` | Items 1–8 and extra 1–6 mark sandhi with apostrophes in the sentence and in the rows (`c'eva`, `pan'etaṃ`); items 9–21 and extra 7–8 do not (`neso`, `cāhaṃ`, `esevanto`) (old F8) | owner decision | 8 |
| 16_class.md:136 | `iti'ss'ime \| sandhi \| ind+pron+pron` | Sandhi rows give the parts in column 3 at 133, 144, 167, 177, 211, 221, 234, 238, 646 …, leave it blank at 83, 95, 101, 107, 115, 198, 264 and in all of items 9–21 (old F10) | One style | 8 |
| 16_class.md:122–124 | `abhiññā[^1] \| verb \| ger` / `sacchikatvā \| verb \| abs` / `upasampajja \| verb \| ger` | `ger` and `abs` for the same form in consecutive rows (also `ger` 242; `abs` 369, 554, 558, 837) (old F11) | owner decision (gerund or absolutive) | 8 |
| 16_class.md:207 | `kammadhāraya > bahubbīhi` | `>` unescaped here and at 269, 272, 281; escaped `\>` at 699, 714, 715, 739 and in class 23 (old F12) | One form | 8 |
| 16_class.md:337 | `vi+√nī･1 a (lead, carry)` | Only root cell in the class with a prefix; `pabbajanti` (106), `vihaññati` (600), `nibbattati` (699) give the bare root (old F13) | `√nī･1 a (lead, carry)` | 8 |
| 16_class.md:323 | `(because of) having knowledge or rather (because of) having lifestyle` | Supplied words in round brackets here and at 377, 638, 733, 803; in square brackets at 158, 191, 285, 668, 750, 776 (old F15) | One bracket style | 8 |
| 16_class.md:452 | `dhārayissasi \| verb \| fut.2nd.sg \| you will hold; will keep; will carry \| \|` | Root cell empty for a plain verb; also `jaññā` (536), `\#amhi` (492), `\#atthi` (593, 597, 606), `sacchikatvā` (121) (old F18) | Fill or state that roots are optional; verify | 6 |
| 16_class.md:591 | `\#vītināmeyyaṃ \| verb \| opt.reflx.1st.sg` | The `-eyyaṃ` optative is tagged reflexive here (DPD does the same) but plain `opt.1st.sg` at 23_class.md:472 (`paccanubhaveyyaṃ`) (old F19) | One tag; verify | 6 |
| 16_class.md:325 | `[AN8.53](https://s.dhamma.gift/an/an8/index.html#an8.53) <br>` | Space before `<br>` in 136 of the 271 numbered sentences that have a `<br>`, none in 135; both in every class (27 and 28: 3 with, 29 without). Key and exercise differ in this at 23 items (old F119) | One form | 9 |
| 17_class.md:316 | `yamahaṃ \| - \| - \| whichever I` | Sandhi rows with `-` instead of `sandhi`: 305, 351, 468, 495, 668; `idappaccayā` (503) is a compound with `-` (old F20) | `sandhi`. Done 2026-11-25 in 17_class.md (sandhi for yamahaṃ, kiñhi, lokañca, evañcetaṃ, bhūtapubbāhaṃ); left: idappaccayā (compound, not sandhi) | 9 |
| 17_class.md:618 | `vi√har･1 a (live)` | Prefix in the root cell here and at 611 (`saṃ+ud√han･1 a`); bare root elsewhere (`vihareyyaṃ` 319, `uttiṇṇo` 112) (old F24) | Bare root | 8 |
| 17_class.md:413 | `<br>(Buddharakkhita): Mind precedes all mental states.` | A second, published translation inside the bold line, after `<br>`; at 426 `(Sujato)` without colon (old F25) | owner decision; one style | 8 |
| 17_class.md:511 | `'idappaccayā avijjā'ti` | Items 11–19 and extra 7–8 have no sandhi apostrophes, except 301 `vihareyyan'ti`, 450 `paṭipadan'ti` and 491 (old F27) | owner decision (see class 16) | 8 |
| 17_class.md:66 | `purisapuggalo \| noun \| masc.nom.sg \| individual person \| \|` | Compound type missing: class 17 gives it for only three compounds (462, 571, 676); class 16 gives it for all (old F28) | Fill, or state that it is optional; verify | 7 |
| 17_class.md:521 | `pass.pr.3rd.sg` | Voice before tense here and at 502; after tense at 606 (`pr.caus.3rd.sg`) (old F29) | One order; verify | 7 |
| 17_class.md:300 | `\#na \| prefix \| \| not, without` | Grammar of the negative prefix blank (171, 180, 290, 588) or `neg` (293, 585, 591) (old F31) | One form | 8 |
| 18_class.md:626 | `(lit.: with)` | Third form of the marker: `lit.` (187, 421, 484), `lit:` (421, 436), `lit.:` here (old F33) | One form | 9 |
| 18_class.md:246 | `vāyodhātū'ti` | Items 5–13 carry no sandhi apostrophes except here (and row 267), 175 `pakkho'ti`, 296 `rūpan'ti`, 362 (old F37) | owner decision (see class 16) | 8 |
| 18_class.md:115 | `n'ādhimuccati \| sandhi \| pr.3rd.sg` | Sandhi row with an inflection tag (also 267, 319); other sandhi rows have a blank or the parts (`ind+pron`) (old F38) | One style; verify | 7 |
| 18_class.md:251 | `puna \| ind \| - \| again` | Empty grammar cells are `-` in items 5–13 (237, 248, 279, 306, 371), blank in items 1–4 and the extras (515, 573, 587) (old F39) | One style | 8 |
| 18_class.md:75 | `saṅghādiseso \| noun \| masc.nom.sg \| offence requiring suspension \| \|` | Compound type given for 6 compounds only (187, 218, 323, 471, 475, 559) (old F40) | Fill or drop; verify | 7 |
| 19_class.md:333 | `bhaññamānesu \| prp pass \|` | Passive present participle is `prp pass` at 320 and 365, plain `prp` at 267 (`desiyamāne`) and 343 (`bhaññamāne`) (old F42) | One tag | 8 |
| 19_class.md:239 | `\#\#\#samudaya (ca)` | `(ca)` at 230, 231, 265, 266; `[ca]` at 530, 531, 563, 564, 584, 585 (old F43) | One bracket | 8 |
| 19_class.md:459 | `\#uṭṭhāya \| ind \| abs` | Absolutive is `verb \| abs` elsewhere (450, 456); `ger` at 58, 122, 126, 588 (old F44) | `verb \| abs`; owner decision ger/abs | 8 |
| 19_class.md:69 | `saṃ√idh･3 ya (succeed)` | Prefix in the root cell: 68, 170 (`ava√gāh`), 527 (`apa√kam`); bare root for `payojeyya` (62), `upasampajja` (126), `paṭikkanto` etc. (old F45) | Bare root | 8 |
| 19_class.md:251 | `**samudayadhamma \< samudaya + dhamma (kammadhāraya)**` | Items 7–13 and extra 6 add bold analysis lines under the translation (as the instruction at line 43 asks); items 1–6 and extras 1–5 give the type only in column 5; items 7–13 leave column 5 mostly empty (old F48) | One method; verify | 7 |
| 19_class.md:559 | `[VIN1.1.2]` | Vinaya label style differs from `VIN PAT PC 57` (class 18) (old F50) | owner decision | 6 |
| 20_class.md:40 | `āvuso \| ind \| voc.sg \| friend; brother` | Third way of tagging `āvuso`: `noun \| masc.voc.pl` (16_class.md:367, 17_class.md:458), `noun \| masc.voc.sg` (classes 23, 25, 27) (old F56) | One tag (DPD: `ind`). Done 2026-11-25 in 16_class.md and 17_class.md (ind ¦ voc.sg ¦ friend); 20_class.md already ind; left: classes 23, 25, 27 | 8 |
| 20_class.md:554 | `vi√cit･8 cha (think, intend)` | Prefix in the root cell: 95, 539, 540, 544, 547, 586, 598; bare root elsewhere in the class (old F57) | Bare root | 8 |
| 20_class.md:235 | `\#pīti (ca)` | `(ca)` at 228, 229, 588–590 (with `[and]` in the gloss); `[ca]` at 10, 11, 504, 505, 510, 513; `(+ca)` at 639, 640 (old F58) | One bracket | 8 |
| 20_class.md:186 | `Based on this, I would take the meaning of samaṇuddesa as … But: cum grano salis.` | Footnotes 16 and 17 are editorial notes in the first person ("I would take", "I wonder if") (old F60) | owner decision | 7 |
| 20_class.md:36 | `abyayībhāva (adverbial compound)` | Type explained in brackets here and at 58; not at 86, 92; `digu (numerical compound)` at 19_class.md:93 (old F61) | owner decision | 6 |
| 21_class.md:32 | `paṇītaṃ \| adj as noun \|` | `adj as noun` (30), `noun or adj` (68), `agent noun` (91, 151), `(agent) noun` (444); `adj (as noun)`, `noun (agent)` in class 20 (old F62) | One notation | 8 |
| 21_class.md:224 | `[UD5.10]` | `UD5.10` here and at 333 (exercise: `UD50`); `UD45` in classes 17 and 19 (old F64) | One label style | 8 |
| 21_class.md:194 | `sabbhireva **samāsetha**` | Items 9–16 and extra 4 have no sandhi apostrophes, except 184 `suggatin'ti`, 207 `gacche'ti`, 239 `n'ātimaññetha`, 267, 298, 357 (old F68) | owner decision (see class 16) | 8 |
| 22_class.md:171 | `**(lit:) A person` | `(lit:)` and `(Figuratively):` in one line: case and colon position differ (old F69) | One form | 8 |
| 22_class.md:204 | `na yito dūraṃ **gamissase** cittā'ti.` | Items 8–14 and extra examples 1, 4–6 have no sandhi apostrophes except `cittā'ti` (182) and `phāsuvihārañcā'ti` (472); items 1–7 and extras 2–3 have them. In extras 4 and 6 the rows add apostrophes the sentence lacks (`appābādhatañ'ca` 494, `mātā'ti` 597) (old F70) | owner decision (see class 16) | 8 |
| 22_class.md:233 | `kātabbaṃ **amaññissaṃ**.` | Target verbs are bold in items 8–14 and extras 4–6, not in items 1–7 or extras 1–3 (old F71) | One way; verify | 7 |
| 22_class.md:302 | `sace \| ind \| - \| if` | Empty grammar cell of indeclinables written `-` (273, 274, 324, 530, 593) or left blank (223, 292, 378, 412); `na` is `neg` (58), blank (350, 378) or `-` (593) (old F73) | One form | 8 |
| 22_class.md:436 | `abhi+ud√gam･1 a (go)` | Only root cell in the class with prefixes; `vinayetha` 26, `vipassati` 169, `upagacchatha` 537 give the bare root (class 21 writes `vi√nas` without `+`) (old F74) | `√gam･1 a (go)` | 8 |
| 22_class.md:493–494 | `\#ñāti (ca) \| noun \| masc.nom.sg \| family` / `\#mittā (ca)` | Dvanda members marked `(ca)` (457, 458, 628) or `(+ca)` (624, 625, 627) (old F75) | One form | 9 |
| 22_class.md:151; 26_class.md:560 | `asso bhadro kasām'iva` / `etena saccena suvatthi hotu` | No final full stop in the key sentence; the exercise has one (ex 93, ex 355). The reverse at 21:333 and 21:357 (full stop in the key, none in ex 237, 258) (old F122) | Same in both. Done 2026-11-25 in 22_class.md (full stop added to key); left: 26_class.md:516 | 8 |
| 23_class.md:281 | `\#patta \| pp \| nt \| reached \| √ap･4 uṇā (reach, attain)` | Three formats in one class: items 1–8 and extras 1–8 put the construction in column 5; items 9–15 and extras 9–11 put it in bold lines under the table; item 9 also has class 16–22 root cells (267, 275, 276, 280) (old F77) | One format | 9 |
| 23_class.md:315 | `idh'āvuso, dhammayogā bhikkhū jhāyī bhikkhū apasādenti, ime pana jhāyino'mhā, jhāyino'mhā'ti` | Sandhi apostrophes in the sentence but not in the rows (`idhāvuso` 304, `jhāyinomhā` 316). Same at 459 / 473, 508 / 532, 764 / 778, 865 / 869 (old F78) | owner decision (see class 16) | 9 |
| 23_class.md:795 | `**anādiya** \| verb \| ger \| not taking up \| na + √ādā + ya` | `ger` at 719, 749, 753; `abs` at 276, 412, 570, 744, 782 in the same class (old F79) | owner decision (ger / abs) | 9 |
| 23_class.md:442 | `mā \| ind \| prohib \| do not` | `prohib` here (also 418, 819, 824); `neg (+aor)` at 73, 77 (old F80) | One form | 8 |
| 23_class.md:160 | `**samāhito** \| pp (as adj.) \| masc.nom.sg` | `pp (as adj.)` with a full stop; `pp (as adj)` at 105, 116; `adj (pp)` at 212, 590, 655; `adj, comparative` at 562 (old F81) | One notation | 8 |
| 23_class.md:929 | `assādato \| noun \| masc.abl.sg \| as the satisfaction, enjoyment` | `-to` forms meaning "as …" are `ind \| adv` in class 22 (`aniccato`, `dukkhato`, 22_class.md:108, 113) and ablative nouns here (883, 887, 891) (old F82) | One treatment: `ind \| adv` in both classes; `assādato` is not a DPD headword, but DPD tags such `-to` forms as `ind, adv` (e.g. `momuhato`): DPD lookup | 6 |
| 23_class.md:41 | `**e.g. viññāṇaṃ : vi + √ñā + aṇa**` | Space before the colon (not at 29); root meaning "(to grasp)" at 35, "(know)" at 45 (old F84) | One form; verify | 7 |
| 24_class.md:25 | `**jāyetha** \| verb \| opt.reflx.pass.3rd.sg` | Order of tense, voice and mood varies: `opt.reflx.pass` (24), `pass.opt.reflx` (22_class.md:261), `pass.pr` (304) against `pr.pass` (23_class.md:130), `caus.pr` (239), `caus.fut` (438), `opt.caus` (509), `abs (caus)` (57) (old F86) | One order | 9 |
| 24_class.md:255 | `seti \| verb \| pr.3rd.sg \| he sleeps \| √sī + a \> se` | Constructions change form within the class: `√root + sign + ending` in items 1–9; base only (229, 391, 396, 447) or `base + ending` without the root (233 `soca + ti`, 239, 286, 301, 304, 596) from item 10; old root cells at 290, 368, 369 (old F87) | One form | 8 |
| 24_class.md:238 | `na \> a + vi + √bhaj + ta` | Negative written `na \> a` (215, 262, 339, 365, 366, 448, 586) or `na` (25, 28, 31, 34, 67, 81, 158, 535, 554, 598) (old F88) | One form | 8 |
| 24_class.md:285 | `abhibhuyya \| verb \| ger \| overcoming` | `ger` here; `abs` at 50, 57, 227, 365, 402; `ind \| abs` at 368 (old F89) | owner decision (ger / abs) | 9 |
| 24_class.md:304 | `**Whoever monks, would say thus, "**` | Items 12–15 split the table into parts with a translation after each; all other items have one table and one translation (old F90) | One layout; verify | 7 |
| 25_class.md:66 | `kaṇṇasukhā \| adj \| fem.nom.sg \| easy on the ear; pleasant to hear \| catutthī (dat) tappurisa` | `(dat)` added to the type here and at 70, 75 only; `(upapada)` at 412 (old F93) | One form; verify | 7 |
| 25_class.md:241 | `\#jāti ca \| noun \| fem. \| birth and` | Dvanda members marked `jāti ca` here (230–232), `(ca)` / `(+ca)` in classes 22–24; no `dvanda` label on 229 (old F95) | One form | 8 |
| 26_class.md:223 | `10. [MN39](https://s.dhamma.gift/mn/mn39/index.html) <br>ahaṃ kho pubbe ābādhiko ahosiṃ dukkhito bāḷhagilāno, bhattañca me nacchādesi` | Two formats in one class: items 1–9 and extra 1 bold the derivatives and give the construction in column 5; items 10–17 and extras 2–3 have no bold, write `taddhita` in column 5 and put the construction in a bold line under the table. Sandhi apostrophes stop in the sentences from item 10 but stay in the rows (`bhattañ'ca` 220, `porāṇam'etaṃ` 279, `avitakko'mhi` 343) (old F98) | One format | 9 |
| 26_class.md:437 | `**muhu + tta + aṃ (taddhita)**` | `(taddhita)` added to some construction lines (380, 406, 408, 508, 510), not to the others (old F99) | One form; verify | 7 |
| 26_class.md:569 | `kamma (irreg) \| noun \| nt.acc.sg \| action, deed` | Note on the form inside the word cell; the metrical `abhabba` (530, flagged IMPOSSIBLE as `masc.nom.sg`) has no note (old F102) | Note both the same way; verify | 7 |
| 26_class.md:18 | `akuhako \| (agent) noun \| masc.nom.sg \| who is honest; not deceitful \| na + √kuh + aka` | `(agent) noun`; plain `noun` for the agent nouns `dātā` (33) and `āvikattā` (432) (old F103) | One notation; verify | 7 |
| 27_class.md:395 | `paññāyetha \| verb \| opt.pass.reflx.3rd.sg` | A fifth order for this form (see 24_class.md:24); `phuseyyaṃ \| verb \| opt.reflx.1st.sg` at 341 against `paccanubhaveyyaṃ \| verb \| opt.1st.sg` at 23_class.md:472 (old F104) | One order | 9 |
| 27_class.md:249 | `pahāya \| verb \| ger \| leaving behind` | `ger` at 231, 244; `abs` at 103 (old F105) | owner decision (ger / abs) | 9 |
| 27_class.md:36 | `ariyasaccāni \| noun \| nt.acc.pl \| noble truths \| kammadhāraya[^39]` | An alternative compound type given in a footnote ("OR chaṭṭhī tappurisa"); in the cell itself at 23_class.md:661 (`(or)`) (old F107) | One way; verify | 7 |
| 27_class.md:494 | `[^46]: Although Cone has not reached the letter s yet` | A dated editorial remark in a footnote (old F108) | owner decision | 6 |
| 27_class.md:100 | `**sammodanīyaṃ** kathaṃ **sāraṇīyaṃ** vītisāretvā` | Bold target words in the sentence differ between key and exercise: bold only in the key at 56 items (22:232, 24:92, classes 25–28), only in the exercise at 19 items (class 18 items 5–12; class 23 from item 9), different spans at 11 items (22:182 and class 23, e.g. `kāya**duccaritena**` against `**kāyaduccaritena**` at 23:636) (old F120) | owner decision: bold the same words in both | 8 |
| 28_class.md:153 | `dīyittha \| verb \| aor.pass.reflx.3rd.sg \| was offered` | Tense first here and in `pr.pass.reflx` (397), voice in the middle; other orders in 24_class.md:24 (old F110) | One order | 8 |
| 28_class.md:249 | `\#**pasuto** \| pp (adj) \| masc.nom.sg (+loc)` | `pp (adj)`; `pp (as adj)` at 95, `adj (pp)` at 353, `noun (as adj)` at 270 (old F111) | One notation | 8 |
| 28_class.md:354 | `ubho \| pron \| nt.acc.dual \| both` | `dual` occurs only here (old F112) | `nt.acc.pl`; verify. DPD: inflection table tags ubho dual nom/acc (headword entry says nom & acc pl of ubha) | 7 |
| 29_class.md:504 | `momuhato \| ind \| adv (masc.abl.sg) \| as very foolish; as completely confused` | Third treatment of a `-to` form meaning "as …" (see 23_class.md:883) (old F115) | One treatment for the `-to` forms; this row agrees with DPD (`ind, adv, abl sg of momuha`), so use `ind \| adv` at 22_class.md:108, 113 and 23_class.md:883 as well | 7 |
| 29_class.md:179 | `niccheyya \| verb \| ger \| evaluating; discriminating` | `ger` throughout this class (177, 190, 235, 338, 339, 348, 460, 632, 666, 698); `abs` for `disvāna` at 28 (old F117) | owner decision (ger / abs) | 9 |

## G. Links

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 17_class.md:622 | `[ITI87](https://s.dhamma.gift/kn/iti/index.html)` | Itivuttaka link has no anchor; other KN links point to the sutta or vagga (`#ud5.5`, `#snp2.4`) (old G1) | Add the anchor; verify | 7 |
| 17_class.md:663 | `6. VV 52<br>` | Reference without a link (also in the exercise) (old G2) | owner decision | 6 |
| 21_class.md:399 | `[ITI87](https://s.dhamma.gift/kn/iti/index.html)` | No anchor (as at 17_class.md:598) (old G4) | Add the anchor; verify | 7 |
| 24_class.md:99 | `[ITI62](https://s.dhamma.gift/kn/iti/index.html)` | No anchor (as at 17_class.md:598 and 21_class.md:357) (old G5) | Add the anchor; verify | 7 |
| 24_class.md:396 | `[SN46.52](https://s.dhamma.gift/sn/sn46/index.html#sn46.52)/[53](https://s.dhamma.gift/sn/sn46/index.html#sn46.53)` | Double reference in the key; the exercise (ex 272) has `[SN46.53]` only (old G10) | One reference in both | 8 |
| 25_class.md:334 | `[ITI100](https://s.dhamma.gift/kn/iti/index.html)` | No anchor (as at 24_class.md:92) (old G7) | Add the anchor; verify | 7 |
| 28_class.md:405 | `[ITI76](https://s.dhamma.gift/kn/iti/index.html)` | No anchor (as at 24_class.md:92) (old G9) | Add the anchor; verify | 7 |

## H. Data to re-verify (forms, references, counts)

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 17_class.md:190 | `[UD45]` | Label is a running number (anchor `#ud5.5`); class 21 uses `UD5.10` for the same book (old H3) | One label style; verify | 7 |
| 18_class.md:385 | `[AN3.83](https://s.dhamma.gift/an/an3/index.html#an3.82)` | Label and anchor differ by one; also AN3.71 → `#an3.70` (499), AN3.51 → `#an3.50` (548) (old H5) | none if intended (two numbering systems); verify | 5 |
| 21_class.md:286 | `kiñci \| pron \| masc.acc.sg \| anyone` | Most editions of Kp 9 read `katthaci na kañci`; the exercise has `naṃ kiñci` too. The tag itself agrees with DPD (`kiñci` 3: masc & nt acc sg of `kaci`) (old A25) | verify the reading of Kp 9 | 5 |
| 22_class.md:151 | `yo nindaṃ apabodheti, asso bhadro kasām'iva` | The exercise (93) has `apabodhati`; DPD has both forms. Editions differ here (`niddaṃ` / `nindaṃ`, `apabodheti` / `appabodhati`) (old H8) | verify against the source edition; align key and exercise | 6 |
| 22_class.md:175 | `paccuppannañ'ca yaṃ dhammaṃ, tattha tattha vipassati.` | The usual reading of the verse is `yo dhammaṃ` ("whoever sees …"); `yaṃ` in key and exercise. Row 164 and the translation follow `yaṃ` (old H9) | verify the reading | 6 |
| 22_class.md:201 | `[TH206](https://s.dhamma.gift/kn/thag/index.html#thag5.1)` | The verse belongs to the ninth poem of the Fives (Vijitasena, Thag 5.9); the anchor is the start of the nipāta, as the link rule (`#thagN.1`) prescribes (old H10) | owner decision: `#thag5.9` if the site has the anchor | 6 |
| 23_class.md:120 | `**payata**pāṇi \| adj \| masc.nom.sg \| open-handed; freely giving (lit: stretched-out hand) \| kammadhāraya \> bahubbīhi` | DPD has the headword as `payatapāṇī` (nom.sg in `-ī`; flagged IMPOSSIBLE) and the type as plain kammadhāraya (old H12) | verify the reading (`payatapāṇi` / `payatapāṇī`); the DPD headword is `payatapāṇī`, type `kammadhāraya` | 6 |
| 23_class.md:198 | `**appagabbho** kulesu **ananugiddho**.` | The usual text of the verse has the sandhi `kulesvananugiddho`; here it is resolved (key and exercise) (old H13) | verify; note the resolution | 6 |
| 23_class.md:227 | `[TH257](https://s.dhamma.gift/kn/thag/index.html#thag16.1)` | The verse is from the tenth poem of the Twenties (Thag 16.10); `[TH251]` at 577 is from the fourth (16.4). Both anchors point to the start of the nipāta, as the link rule prescribes (old H14) | owner decision (see 22_class.md:182) | 6 |
| 23_class.md:434 | `13. [MN107](https://s.dhamma.gift/mn/mn107/index.html) <br>cakkhunā rūpaṃ disvā mā nimittaggāhino ahuvattha` | MN 107 has the singular `mā nimittaggāhī hohi`; the plural wording `nimittaggāhino ahuvattha` is that of SN 35.127. Same label at 812 and in the exercise. Judged from memory (old H15) | verify label and link | 6 |
| 24_class.md:272 | `[AN3.91](https://s.dhamma.gift/an/an3/index.html#an3.90)` | Label and anchor differ by one, also `[AN3.101]` → `#an3.100` at 267 (same in the exercise). Other labels follow the numbering of the anchors (old H16) | One numbering in the label. DPD sutta_info: AN3.91 and AN3.101 are the DPD/CST codes (SC 3.90, 3.100); every AN label in the key uses the DPD code with the SC anchor, so the labels are consistent; no change | 8 |
| 25_class.md:32 | `[TH257](https://s.dhamma.gift/kn/thag/index.html#thag16.1)` | The verse is from Thag 16.10; anchor at the start of the nipāta by the link rule (old H17) | owner decision (see 22_class.md:182) | 6 |
| 28_class.md:494 | `aṭṭha**padakatā** kesā, **nettā** **añjanamakkhitā**.` | The usual reading is `aṭṭhāpadakatā` (DPD has both headwords). `[TH251]` and `[TH133]` (232) land on the first poem of their nipāta, by the link rule (old H18) | verify the reading; owner decision on the anchors | 6 |
| 29_class.md:145 | `so it seems this is a ghost word in DPD.` | A statement about DPD in a footnote; DPD does list `ādisa` (adj, in comps, from `ādisati`) but derives `etādisa` from `etaṃ + disa` (old H19) | owner decision: keep, reword or remove | 7 |

## I. Further details on the material under review

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| 16_class.md:647 | `[DHP389](https://s.dhamma.gift/kn/dhp/index.html#dhp383)` | Label and anchor differ because the site anchors by vagga (also DHP407 → `#dhp383` at 752, DHP338 → `#dhp334` at 670, DHP62 → `#dhp60` at 586). This follows the dhp anchor rule in `kamma/tech.md` (`#dhpA`, first verse of the vagga), so it is not an error (old H1) | None | 8 |
| 16_class.md:876 | `[SNP7](https://s.dhamma.gift/kn/snp/index.html#snp1.7)` | Label style `SNP7` (running sutta number) next to `SNP62` → `#snp5.8` (line 294); the anchor uses vagga.sutta (old H2) | owner decision on label style | 5 |
| 17_class.md:416 | `[AN3.70](https://s.dhamma.gift/an/an3/index.html#an3.69)` | Label and anchor differ by one. The quoted text (`yadapi … alobho tadapi kusalamūlaṃ`) is the Mūla sutta, AN 3.69 in SuttaCentral numbering, so the anchor is right and the label follows another numbering (old H4) | None, or label `AN3.69`; verify | 7 |
| 21_class.md:511 | `[TH251](https://s.dhamma.gift/kn/thag/index.html#thag16.1)` | Label `TH251`; the verse is from the Raṭṭhapāla verses (Thag 16.4). Counting the poems of nipātas 1–15 (247) makes Thag 16.4 poem 251, so `TH251` is the running poem number and `#thag16.1` follows the `#thagN.1` rule in `kamma/tech.md` (old H7) | None, if the count holds; verify | 7 |

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
