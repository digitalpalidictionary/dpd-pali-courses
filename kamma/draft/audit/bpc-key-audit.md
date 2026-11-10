# BPC key audit — `docs/bpc_key/`

Date: 2026-11-10
Scope: all 16 Markdown files under `docs/bpc_key/` (index + classes 1–15, 8 235 lines, 3 474 table rows).
No file in `docs/` was modified. This is a findings list only.

## Method and limits

| Check | How | Result |
| --- | --- | --- |
| Project verifier | `uv run python scripts/verify_key.py` | Exit 0. Numbering, POS vocabulary, grammar vocabulary, root format, stray characters: 0 errors. Word coverage: 465 warnings (sandhi and compound splits; the real gaps are listed in Part 2) |
| Table structure, characters, whitespace, punctuation | Scripted over all 15 class files | Section A |
| Key sentence vs exercise sentence | Scripted diff of all 438 items against `docs/bpc_ex/` | Section B |
| Sutta links | `uv run python scripts/check_sutta_links.py docs/bpc_key` | 219 links / 104 pages, all pass |
| Citation labels | Key vs exercise label and URL, scripted; wording vs source for part of the folder | Section C |
| Root column | Every Root cell compared with `dpd.db` (root, verb mark, group, sign, gloss) | Section D |
| Tag notation | Scripted tally of every POS / Grammar combination | Section E |
| Word forms vs DPD | `verify_key.py --dpd` (advisory), report written outside the repo | Section F |
| Line-by-line reading | All 8 235 lines, by seven parallel reader agents; their main findings were then re-checked against the source lines and DPD | Part 2 |

Not verified:

- Pāli grammar findings in Part 2 rest on knowledge of the language plus DPD lookups for gender, part of speech and root. Each carries a confidence score (1–10). Below 8, check DPD or the text before changing anything.
- Canonical wording was compared with the local SuttaCentral text only for classes 1–4, 7–8 and 14. For the other classes, rows that depend on a reading say "check text". CST, which the course may follow, was not consulted at all.
- The link checker proves that a page and anchor exist, not that the sentence is in that sutta. Only the citations listed in section C were examined; the rest are unchecked.
- Section D accepts a Root cell if it matches any DPD headword the form resolves to, so a root that belongs to a homonym of the word in the sentence can pass unnoticed (D4 and 7.14 were found by reading, not by the script). 35 forms are not in DPD's lookup table and were not checked.
- The 2 087 "ambiguous" rows of the DPD form check were not reviewed one by one.
- Rendered output (site, PDF, DOCX) was not built.
- `docs/bpc_ex/` was read only where it differs from the key. Exercise-side errors found on the way are in section B.

## Summary

| Section | Rows |
| --- | --- |
| A. Structure and Markdown | 17 |
| B. Key sentences against the exercises | 15 |
| C. Citations | 20 |
| D. Root column against DPD | 25 |
| E. Notation drift | 19 |
| F. Advisory DPD form check | 11 |
| Part 2. Line-by-line reading (classes 1–15) | 262 |

A row often covers several locations, so the number of places to edit is several times higher.

Overall confidence in the audit: 9/10 for sections A, B, D, E (scripted and reproducible), 8/10 for C, 7/10 for Part 2 (missing: a text check of the "check text" rows against the edition the course follows, and a native-level review of the translation rewordings, which are suggestions, not corrections).

Highest-value fixes, in order:

1. Wrong or impossible grammar tags a student will copy: `9:334` (9.5), `6:548` (6.6), `9:182` (9.6), `2:221-222` (2.3, 2.4), `4:204` (4.7), `11:170-172` (11.7), `8:376` (8.4), `14:807` (14.7), `15:192`/`15:230` (15.3), `13:88` (13.7), `12:462`/`12:466` (12.1).
2. Sentence, table and translation out of step: `6:28` (6.1), `5:584` (5.2), `13:537` (13.1), `9:59` (9.1), `14:478` (14.18), `14:453` (14.1), `5:551` (5.1), `15:155` (15.1).
3. Translations that say the opposite or lose the point: `13:633` (13.16), `10:445` (10.8), `14:585` (14.19), `9:191-192` (9.13).
4. Wrong citations: C5, C6, C16, C17, C18, and the key/exercise disagreements C1–C4, C7, C8.
5. Wrong roots: D1 (`bhante`, 12 rows), D3, D4, D5, 7.14.
6. Stray characters: A5 (Cyrillic "с"), A6 (`ṁ`), F1, F3.
7. Section E as a single normalisation pass, ideally enforced by extending `verify_key.py`, since its tag vocabulary currently accepts all the variants.

---

## Part 1 — Cross-file checks (scripted)

Locations are `N:LINE` = `docs/bpc_key/N_class.md`, line `LINE`.

### A. Structure and Markdown

| # | Location | Finding | Suggested |
| --- | --- | --- | --- |
| A1 | all files | Numbering, column counts and tag vocabulary are clean: 0 numbering gaps, 0 column-count mismatches, every item has a table and a bold translation, no unclosed bold. | — |
| A2 | `1`, `15` | No `## Class N Extra` section (classes 2–14 all have one). | Confirm intended |
| A3 | `3:1-2` | No blank line between the `# Class 3 Key to Exercises` heading and item 1 (every other file has one). | Add blank line |
| A4 | `11:527` | Whitespace-only line (single space) before the Extra heading. Only trailing whitespace in the folder. | Empty line |
| A5 | `13:412` | `ye сa dūre`: the "с" is Cyrillic U+0441, not Latin "c". Breaks search and DPD lookup. | `ye ca dūre` |
| A6 | `11:511`, `11:523`, `12:437`, `12:448`, `12:462`, `12:466` | Niggahīta written `ṁ` (6 times) against `ṃ` everywhere else. | `ṃ` |
| A7 | `6:11`, `9:153`, `10:11`, `12:103`, `13:47`, `13:93` (table); `3:57`, `3:62`, `4:211`, `9:392`, `10:293`, `11:611`, `14:715`, `14:735`, `15:251-257`, `15:343`, `15:364`, `15:405`, `15:419` (text) | Curly opening quote `‘` (25 in the folder) paired with a straight `'` close, or used as an elision mark (`‘ti`, `‘pi`, `jānāmī‘ti`). No `’` exists in the folder. `14:735` has a doubled `‘‘`. | Straight `'` throughout |
| A8 | `15:25`, `15:112`, `15:191` | A sentence (`katame pañca?`, `katamehi tīhi?`, `katamehi pañcahi?`) is placed as the first table row with four empty cells. | Move above the table |
| A9 | `8:568`, `8:570` | `ca` rows with empty POS and empty Grammar. | `ind` / `conj` |
| A10 | `10:678`, `10:680` | `(or)` entered in the Pāli column as a pseudo-word to carry an alternative parse. | Use the in-cell `(or)` pattern of `10:377` |
| A11 | 64 table rows, e.g. `6:292`, `7:462`, `9:79`, `10:272`, `10:519-528`, `11:466`, `11:469`, `13:207`, `13:247`, `13:280`, `14:267`, `15:183`, `15:243`, `15:360`, `15:424` | Raw `<br>` inside table cells (POS, Grammar and Pāli columns). The project rule is no raw HTML in sources. The per-item `<br>` between citation and sentence is a separate, folder-wide convention. | Decide; if kept, document it |
| A12 | `9:68`, `9:103`, `10:443`, `10:659`, `11:68`, `11:76`, `11:212`, `11:220`, `12:131`, `12:133`, `12:161`, `5:9`, and class 15 throughout (`15:27`, `15:45`, `15:65`, `15:84`, `15:160`, …) | Sentence punctuation kept inside the Pāli cell (`samudayāya.`, `tumhākaṃ,`, `kho,`). Classes 2–8 and 13 strip it. | Strip |
| A13 | `8:538`, `9:95`, `13:141` | Space before punctuation (`non-disappearance ,`; `pañha-vyākaraṇāni .`; `jātiyā … ,`). | Remove space |
| A14 | `5:413`, `6:175`, `10:636`, `11:341` | Two dots `..` where an ellipsis is meant (the folder has 56 `…`); `12:281` has `….`; `12:437` and `3:318` use three ASCII dots. | `…` |
| A15 | 438 items | The gap between citation, `(simpl)` and `<br>` is written five ways: `) <br>`, `)<br>`, `) (simpl) <br>`, `) (simpl)<br>`, `)(simpl) <br>` (`11:274`). | One form |
| A16 | translations | 82 translations end without final punctuation and 59 start lower-case. Most are deliberate fragments of a split sentence, but the choice is not uniform inside one item (e.g. `10:23` "Or knowing" vs `10:32` "or, not seeing"). | Pick a rule for split sentences |
| A17 | `6:50`, `13:74`, `14:123`, `15:3` | Notes or sub-headings (`This is a common Pāli idiom.`, `passive verbs:`, `Potential Participles`, `Translation Assignment`) formatted in bold exactly like a sentence translation. | Plain text or a heading |

### B. Key sentences against `docs/bpc_ex/`

Compared after stripping bold, footnotes, quote style and spacing. 438 items; 0 items missing on either side. Differences in sandhi apostrophes only (about 30 items, e.g. `10:3`, `13:97`, `14:136`) are not listed.

| # | Key | Exercise | Difference | Suggested |
| --- | --- | --- | --- | --- |
| B1 | `4:24` | `bpc_ex/4:26` | Word order: key `abhisaṅkharoti kāyena kusalaṃ`, exercise `kāyena kusalaṃ abhisaṅkharoti`; exercise is marked `(simpl)`, key is not. | Align |
| B2 | `4:269` | `ex/4:253` | Exercise has `saccaṃ mayaṃ bhavantaṃ…`; key drops `mayaṃ`. | Align |
| B3 | `4:34` | `ex/4:37` | Key ends `taṇḍulā'ti`, exercise `taṇḍulā (honti)`. | Align |
| B4 | `4:113` | `ex/4:110` | Key `samaṇā amhā'ti`, exercise `"samaṇā amha" iti`; key table row is `amha-` (`4:118`). | Align |
| B5 | `4:304`, `5:601`, `10:325`, `13:31` | `ex/4:286`, `ex/5:556`, `ex/10:275`, `ex/13:22` | `(simpl)` on one side only. | Align |
| B6 | `5:3` | `ex/5:3` | Exercise `viññāṇaṃ, bhikkhave, na (hoti) tumhākaṃ`; key `viññāṇaṃ na tumhākaṃ`. | Align |
| B7 | `6:3` | `ex/6:3` | Different sentence end (exercise adds `"bhadante"ti`) and different citation, see C1. | Align |
| B8 | `9:59` | `ex/9:45` | Key adds `katamāni tīṇi?`, which is neither in the exercise nor in the key's table or translation. | Drop from the key sentence, or add rows |
| B9 | `9:95` | `ex/9:73` | Key `pañha-vyākaraṇāni`, exercise `pañhabyākaraṇāni`. | One spelling |
| B10 | `9:681` | `ex/9:633` | Key `paramaṃ`; exercise has the typo `paraṃaṃ` (exercise-side error). | Fix exercise |
| B11 | `10:136` | `ex/10:113` | Key `na ca kiñci loke`, exercise `na kiñci loke`. | Align |
| B12 | `11:530` | `ex/11:444` | Key `sammāsaṅkappagocarā`, exercise `sammāsaṅkappe gocarā`. | Align |
| B13 | `12:377` | `ex/12:312` | Key `ko ca āhāro`; exercise has the typo `ahāro` (exercise-side error). | Fix exercise |
| B14 | `13:31` | `ex/13:22` | Key `gaccheyyāmi'ti`, exercise `gaccheyyāmī'ti`. | `gaccheyyāmī'ti` |
| B15 | `10:539` | `ex/10:477` | Exercise uses `ṁ` twice where the key has `ṃ` (exercise-side). | Fix exercise |

### C. Citations

All 219 `s.dhamma.gift` links pass `scripts/check_sutta_links.py`. That proves the page and anchor exist, not that the sentence is there.

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| C1 | `6:3` vs `ex/6:3` | key `DN2.9`, exercise `SN22.59` | Same item, two sources. | Check the text; make both agree | 8 |
| C2 | `6:39` vs `ex/6:35` | key `DN16.7`, exercise `DN16.17` | Label differs by a digit. | Make both agree | 8 |
| C3 | `6:52` vs `ex/6:47` | key `VIN1.2.12` → `pli-tv-bu-vb-ss12`; exercise `VIN PAT SA 12` → `pli-tv-bu-pm4` | Same rule cited to two different texts and in two label styles. | Make both agree | 8 |
| C4 | `6:68` vs `ex/6:64` | key `MN152`, exercise `MN19` | The closing formula is in both suttas; the two files should name the same one. | Make both agree | 8 |
| C5 | `6:82` vs `ex/6:79` | key `SNP9` → `#snp1.9`; exercise `SNP8` → `#snp1.8` | `ye keci pāṇabhūtatthi` is the Mettasutta, Snp 1.8; the key itself cites it as `SNP8` at `6:353`. | Key → `SNP8`, `#snp1.8` | 9 |
| C6 | `6:276` vs `ex/6:286` | key `DHP277` → `#dhp273`; exercise `DHP185` → `#dhp179` | `sabbe dhammā anattā` is Dhp 279. Both files are wrong, in different ways. | `DHP279` in both (anchor `#dhp273`) | 9 |
| C7 | `14:125` vs `ex/14:109` | key `AN3.83` → `#an3.82`; exercise `AN4.73` | Two different suttas. | Check the text; make both agree | 7 |
| C8 | `11:17` vs `ex/11:16` | key `VIN0` (no link); exercise `[VIN1.0](…pli-tv-bu-vb-pj1)` | Key lost the link and has a truncated label. Same label, also unlinked, at `9:3`. | Use the exercise's form in both | 9 |
| C9 | `2:68`, `3:308`, `5:49`, `8:101`, `8:331`, `13:373`, `14:302` | `VIN PAT NID nidānuddeso`, `VIN`, `UD-a 43`, `DNa2.3`, `VIN PAT SA`, `APA 3`, `VIN PAT NID` | Unlinked references; `VIN`, `VIN PAT SA` and `APA 3` are too vague to locate. Commentary references (`UD-a`, `DNa`) cannot be linked on the site. | Add precise references where a link exists | 7 |
| C10 | `1:3`, `2:102-311` (13 items) | no citation | Class 1 item and 13 class 2 phrase items carry no source at all. | Confirm intended | 5 |
| C11 | `9:526`, `9:550`, `10:312`, `13:477`, `2:14` | `TH251`, `TH257` → `#thag16.1` | Label gives the thera number, anchor always points to the first poem of the nipāta (Raṭṭhapāla is Thag 16.4, Pārāpariya 16.10). Same pattern as the Dhp anchors (vagga start). | Confirm the site has no finer anchor | 5 |
| C12 | `11:61` | `[ITI111](…/kn/iti/index.html)` | Only KN link with no anchor. | Add the anchor if the site has one | 6 |
| C13 | labels | `DHP012`, `DHP026`, `DHP085`, `DHP086` vs `DHP130`, `DHP277` | Zero-padded and unpadded Dhp numbers. | One form | 6 |
| C14 | labels | `VIN1.2.12`, `VIN1.0`, `VIN0` vs `VIN PAT SA 12` | Two label systems for Vinaya (7 vs 52 uses). | One form | 6 |
| C15 | `6:28`, `6:199`, `13:269`, `7:154` | `DN11.6`, `AN10.71`, `MN10.18`, `MN10.16` | Readers could not place the quoted wording in the cited sutta (saṅgha formula in DN11; `thero bhikkhu … piyo ca hoti` is AN5 wording; the expanded truths passage and `na maraṇadhammā assāma` are in DN22, and in MN10 only in the Burmese edition). | Verify | 4 |
| C16 | `14:244` | `[DN16.11](…/dn/dn16/index.html)` | `evañca kho eso, bhikkhu, pañho pucchitabbo` is in DN11 (Kevaṭṭa), confirmed in the local SuttaCentral text. Label and URL are both wrong. | `[DN11](…/dn/dn11/index.html)` | 9 |
| C17 | `4:367` | `[DHP183](…#dhp179)` | `nibbindati dukkhe, esa maggo visuddhiyā` is Dhp 277–279 (file `dhp273-289` in the local SuttaCentral text). Label and anchor are both wrong. Same verse as C6. | `DHP277`, `#dhp273` | 9 |
| C18 | `4:200` | `DHP153` | `gahakāraka diṭṭhosi` is verse 154; `10:744` cites verse 153 (`anekajātisaṃsāraṃ`) correctly. | `DHP154` | 7 |
| C19 | `2:236`, `2:245`, `4:259`, `3:166` | `SN12.41`; `MN39 … aparena samayena buddho`; `SN46.53`; `MN2.4 … paṭisevāmi` | Partial text searches did not find the wording in the cited sutta (`vinipātaṃ nirayaṃ` is in SN12.70; MN39 has `baddho`, not `buddho`; the SN46 phrase is in 46.52 and 46.54; MN2 has 3rd person and the item is not `(simpl)`). Leads, not confirmed. | Verify | 4 |
| C20 | labels | `DN16.21` (used for two passages at `9:233`, `9:267` and again at `14:406`), `DN23.20`, `DN14.4`, `MN2.2`, `MN2.8`, `DN22.1`… | The sub-numbers after DN/MN do not match SuttaCentral segment numbers, and the scheme is not stated anywhere. 47 labels carry one. | State the numbering scheme | 5 |

### D. Root column against the DPD database

The Root column follows DPD (`root` + verb mark `･`/`×` + group + the headword's sign + root gloss). Each of the 1 772 non-empty Root cells was compared with every DPD headword the word form resolves to (`dpd.db` of 2026-11-09). 1 633 match exactly; 35 forms are not in the lookup table. The rest:

| # | Location | Current | DPD | Kind | Conf. |
| --- | --- | --- | --- | --- | --- |
| D1 | `6:488`, `7:473`, `8:600`, `9:349`, `9:460`, `9:651`, `10:308`, `11:517`, `12:482`, `13:127`, `15:263`, `15:268` | `bhante` → `√bhad×1 a (be good, lucky)` | `bhante`: `√bhū･1 a (be, become)` | Wrong root (12 rows) | 8 |
| D2 | `6:291`, `9:285`, `9:466` | `maggo/maggaṃ` → `√magg･8 \*e` | `√magg･1 a (seek, search)` | Group and sign | 8 |
| D3 | `9:363` | `saggaṃ` → `√gam･1 a (go)` | `sagga`: `√sar×1 a (shine)` or `√sajj･1 a` | Wrong root (copied from the `sugatiṃ` row above) | 9 |
| D4 | `10:467` | `sametu` "let him agree" → `√sam･3 \*e (be calm, tired)` | `sameti 2.2` "agrees": `√i･1 a (come, go)`; `√sam` is `sameti 1.1` "calms" (correct at `13:505`) | Wrong homonym | 9 |
| D5 | `10:454` | `ādiyamāno` → `√dā･1 a (give)` | `√ādā･3 ya (take, seize)` (as in the same key at `10:152`) | Wrong root | 9 |
| D6 | `10:160`, `10:166` | `paritassati`, `aparitassaṃ` → `√tas･3 ya (be agitated)` | `√tas･1 ya (tremble, fear)` | Group and gloss | 8 |
| D7 | `14:651` | `virājiya` → `√raj･3 ya (desire)` | `√raj･1 \*e (colour)` | Group, sign, gloss | 7 |
| D8 | `14:562`, `14:571` | `sāditabbaṃ`, `sādiyeyya` → `√sād･1` | `√sād･8` | Group | 8 |
| D9 | `15:181`, `15:243` | `anavajjā` → `√vad･1 a (say, speak)`; `ananuvajjā` → `√vad･8 \*e (salute, praise)` | DPD has it the other way round (`anavajja` √vad 8, `ananuvajja` √vad 1), and `15:241`/`15:183` follow DPD. The same word therefore gets two roots inside one item. DPD's own split of the two words is worth raising upstream. | Inconsistent | 8 |
| D10 | `8:577`, `10:535` | `uparujjhati`, `nirujjhati` → `√rudh･2 ṃa` | `√rudh･2 ya` (as at `8:572`, `13:283`) | Sign | 8 |
| D11 | `11:495` | `vimuttasmiṃ` → `√muc･2 ya` | `√muc･2 ṃa` | Sign | 8 |
| D12 | `14:774` | `bhedanāya` → `√bhid･2 ṃa` | `√bhid･2 \*e` | Sign | 7 |
| D13 | `7:270`, `8:57` | `anāgataṃ`, `upasaṅkami` → `\*e` | `√gam･1 a`, `√kam･1 a` | Sign (not causatives) | 8 |
| D14 | `5:45` | `gamissāmi` → `√gam･1 \*e (go)` | `gamissati`: `√gam･1 a`. Only resolves to `\*e` through an unrelated causative headword. | Sign | 7 |
| D15 | `10:490` | `uddharāpeyya` → `√dhar･1 a` | `√dhar･1 \*āpe` | Sign | 8 |
| D16 | `9:119`, `15:383`, `9:632` | `vicikicchituṃ`, `vicikicchati`, `jegucchī` → sign `cha` | sign `sa` | Sign | 7 |
| D17 | `14:378` | `sandissanti` → `√dis･1 iya` | `√dis･1 ya` | Sign | 7 |
| D18 | `13:297`, `14:267`, `14:370`, `14:476`, `14:835`, `14:837`; `14:372` | `ṃa + iya`, `\*e + iya`, `\*āpe + iya`; `\*e iya` | `ṃa iya`, `\*e iya`, `\*āpe iya` (no `+`) | Notation: seven compound signs, six with `+`, one without | 9 |
| D19 | `14:294`, `14:296` | `√sic･2 ṃa (sprinkle, pour)+ ṃa \> siñca+eyya`; `√sic･2 ṃa + \*āpe (sprinkle, pour)\> siñcāpe (caus)+eyya` | `√sic･2 ṃa (sprinkle, pour)` | Free-form derivation inside the Root cell; only two cells in the folder do this | 8 |
| D20 | `9:177`, `10:440`, `11:184`, `12:526`, `13:513` (`samaṇo` `√sam･3`); `11:253`, `12:192`, `13:390`, `15:218` (`mettā` `√mitt･1`); `12:571` (`bhusaṃ`) | `･` | DPD now marks these roots `×` (no verb) | Verb mark out of date (10 rows) | 6 |
| D21 | 17 rows: `5:66`, `5:158`, `8:51`, `8:262`, `8:476`, `8:620`, `9:21`, `9:560`, `11:170`, `11:172`, `11:336`, `11:640`, `12:492`, `13:423`, `13:425`, `14:463`, `14:484` | `×` | DPD now marks these roots `･` | Verb mark out of date | 6 |
| D22 | 65 rows, e.g. `5:68`, `7:461`, `8:622`, `11:309`, `12:346`, `14:277` | `(be mad, intoxicated)`, `(cut, steal)`, `(cut)`, `(breath, blow)`, `(destroy, exhaust)` | `(be mad, be intoxicated)`, `(cut, divide)`, `(breathe, blow)`, `(exhaust, destroy)` | Root gloss differs from current DPD wording. Mostly DPD rewording since the keys were written; `(cut, steal)` and `(breath…)` are real improvements to pick up. `√chid` appears with three glosses in the keys (`cut` / `cut, steal`). | 7 |
| D23 | `5:120`, `5:132`, `10:195-243` | `√sas･1 a (breath)` | Same in DPD (`√sas 1 … breath`) | DPD-side: noun where a verb gloss is expected. Raise upstream. | 6 |
| D24 | folder | `×` vs `･` | DPD `root_has_verb` mark | The meaning of `×` is not explained anywhere in `docs/bpc`, `docs/bpc_ex` or `docs/bpc_key`. | 8 |
| D25 | many | empty Root cell | — | The same word has a root in one row and none in another: `ānanda` (`5:81` vs `6:45`), `medhāvī` (`6:317` vs `6:529`), `asi`/`attha` (`5:579`, `5:559`) vs `atthi` (`6:88`), `saṅgha` (`5:420` vs `6:255`), `atthi`/`assa`/`assu` (`11:35`, `11:228-232`, `12:634` vs `12:529`, `11:115`), `khamo` (`15:44` vs `15:36`), `dukkhaṃ` (`15:372` vs `15:368`), `samannāgatā` (`15:235` vs `15:104`), `kulāni` (`13:347` vs `13:367`), `oḷāriko` (`12:143` vs `11:331`), `bhikkhu`, `cittaṃ`, `bhavissati`, `n'atthi` in class 10 (`10:180`, `10:275`, `10:286-289`, `10:330`, `10:338`, `10:577`, `10:656`). | 7 |

Homonymous roots (`√har` carry / take / live, `√vid` ×4, `√dis` ×2, `√car` ×2, `√as` be / eat, `√kaṅkh` ×2) look like conflicts in the key because DPD's homonym number is dropped, but each matches DPD and is not an error.

### E. Notation drift across the folder

Counts are table rows. None of these is wrong in itself; each is the same thing written several ways.

| # | Item | Variants found | Suggested |
| --- | --- | --- | --- |
| E1 | Table header | Full header on the first table of each section only; an empty header row on the other 543 tables. Consistent, but relies on a build hook. | Confirm intended |
| E2 | Governed case | round `(+acc)` ×39, square `[+acc]` ×36, bare `+acc` ×4; sometimes after a `<br>`, and in the English column at `4:185` | One form |
| E3 | Absolute constructions | `(loc abs)` / `(gen abs)` ×37, `[loc abs]` ×14, `(loc.abs)` ×4, `<br>loc abs` ×2; at `10:275` it sits in the English column | One form |
| E4 | End of quotation | `+end quote` ×5, `+endquote` ×8, `+ endquote` ×2, `+ end quote` ×2, `+ quote` ×4, `+quotation marks` ×1, `adv, quote` ×1; a separate `iti`/`'ti` row ×21; in the English column at `11:496`; nothing at `11:609`, `11:620`, `13:229`, `15:245` | One form |
| E5 | Passive / causative POS | `verb.pass` ×16, `verb. pass` ×9, `verb.caus` ×13, `verb. caus` ×8, `verb. caus.pass` ×2, `prp. pass` ×9, `prp.pass` ×1, `prp.<br>pass`, `prp caus pass` ×2, `prp caus. pass.`, `prp.<br>caus.pass`, `ptp.caus` ×2, `ptp caus pass`; inside Grammar instead at `13:351` (`pr.pass.3rd.pl`), `14:537` (`pr.caus.3rd.pl`). Plain `verb` for the same forms in classes 3–12 (`paripūreti` `3:97` vs `14:15`; `abhisandeti` `10:121` vs `14:13`; `parimuccati` `6:23` vs `13:148`; `vuccati` `9:303` vs `14:792`; `nirujjhati` `10:535` vs `13:284`). | One form; decide whether classes before 13 get the label |
| E6 | Participle used as adjective | `adj (pp)` ×4, `adj [pp]` ×2, `adj<br>[pp]`, `pp [adj]`, `adj (\<ptp)`, `adj(\<ptp)`, `adj, <br>(\<ptp)` ×2, `adj<br>(ptp)` | One form |
| E7 | Interrogative pronoun | `pron interr` ×4, `pron, interr`, `pron.<br>interr`, `pron<br>interr`; plain `pron` elsewhere (`ko` ×3) | `pron` + `interr` in Grammar |
| E8 | Stray POS values | `adj.` (`5:145`, `13:449`), `noun (comp)` (`5:346`), `adj, comp` (`11:543`), `proper noun` ×1, `ind<br>(comp)` (`10:272`), `pron+noun [idiom]`, `pron+verb` | Fold into the standard set |
| E9 | Indeclinable Grammar cell | `ca`: `conj` ×80, empty ×4, `adv` (`11:650`), `ind` (`15:348`). `vā`: `conj` ×57, `-` ×13, empty ×7, `disj` ×2. `kho`: `emph` ×33, `ind` ×4, `-` ×2, `adv` (`8:411`), empty. `eva`: `emph` ×20, `ind` ×3, empty. `api`: `ind` ×9, `-` ×7, `emph`, `adv`, empty. `evaṃ`: `adv` ×20, `emph` ×4. `pana`: `conj` ×4, `ind` ×4, `-`, empty. `ce`: `cond` ×7, `ind` ×4, empty ×2. `hi`: `emph` ×9, `adv`, `-`. 25 `ind` rows have an empty Grammar cell and 36 have `-`. | One tag per particle |
| E10 | Infinitive POS | `verb \| inf` ×18; `ind \| inf` ×3 (`9:87`, `9:117`, `9:708`) | `verb` |
| E11 | `āvuso` / `bhante` | `āvuso \| ind \| voc.sg` (`5:589`, `14:348`), `ind \| voc.sg or voc.pl` (`8:412`, `10:594`); `bhante \| noun \| masc.voc.sg` ×14. DPD has `āvuso` as `ind`. | `ind` with a plain note, or treat both alike |
| E12 | Fixed phrases | `atha kho`: `ind \| adv` ×5, `idiom \| ind` ×2, `ind \|` (empty) ×2, `ind \| ind`, and split into `atha` "after" + `kho` "that" at `9:191-192`. `evam'eva`: `idiom \| ind` ×2, `idiom \| adv+ind`, `sandhi \| adv+ind`, `ind \| adv+ind`. `seyyathāpi`: `pron+adv+ind` ×9, `-`, empty. `kiṃ nu kho` / `nu kho`: `idiom`, `ind`, or three separate rows (`13:35` vs `13:167-169`, same sutta). `yo pana bhikkhu`: three Grammar cells (`7:342`, `8:294`, `14:286`). `n'eva`/`neva`: four tags. `c'eva`: `sandhi \| ind+ind`, `ind \| ind+ind`, `ind \| ind+emph`. | One analysis per phrase |
| E13 | Compound members | Grammar `-` ×17 (class 2), empty ×4, `nt`/`masc`/`fem` ×5, `masc.` ×3, `masc (in comp)`, `masc. (in comp)`, full `masc.nom.sg` on a stem (`11:51`, `11:55`, `12:159`); stems written `rāga-`, `sammā -` (`1:11`, space before the hyphen), `adhicittam-`, `atītam-`, `divasaṃ-`, `ca-` | One form |
| E14 | Hyphen in table, none in sentence | `6:34` `sāvaka-saṅgho`, `8:42` `nāma-gottāni`, `10:119` `viveka-jena`, `13:25` `pāda-talehi`, `15:95` `yathā-dhammaṃ` (vs `yathādhammaṃ` at `15:118`) | Match the sentence |
| E15 | Literal-meaning note | `lit.`, `lit:`, `(lit: …)`, `[lit: …]`, `[lit:made a vehicle]`, `Lit:` | One form |
| E16 | Supplied words | `[your]` (majority) vs `(his)`, `(done)`, `(He)`, `(like)`, `(a helper)`, `(The Buddha)`, `(there)` | Square brackets |
| E17 | Gloss separator | comma (`consciousness, awareness`) vs semicolon (`rapture; delight`), often both inside one file | One separator |
| E18 | Recurring English terms | `dhammavinaya`: 5 renderings; `brāhmaṇa`: Brahman / brahmin / priest / holy man / "Monk" (`5:629`); `samaṇa`: ascetic / recluse / monk; `mettā`: goodwill / friendliness / loving-kindness; `Venerable sir` / `venerable sir` / `Venerable Sir`; `Ananda`, `Sariputta`, `Mogallana`, `Kalamas`, `Brahma` without diacritics next to `Ānanda`, `Sāriputta`; US and UK spelling mixed (`honor`/`honour`, `behavior`, `practiced`, `flavour`, `offence`) | Glossary + one spelling |
| E19 | Same word, different POS | `parisuddho` pp/adj (`5:32`, `5:344`); `āyasmato` noun/adj (`3:290`, `6:44`); `sabba` adj/pron (`5:269`, `6:280`); `ekaṃ` card/adj (`12:11`, `12:195`); `eko` card/adj (`12:295`, `9:669`); `tayo` card/adj (`14:62`); `adassāvī` noun/adj in one sentence (`11:387`, `11:398`); `pariyāyena` ind/noun in one sentence (`12:233`, `12:244`); `āgatā`/`anāgatā` adj/pp (`7:418-423`, `11:147`, `11:635`); `yathābhūtaṃ` `ind \| adv` (`3:63`) vs `adj \| masc.acc.sg` (`15:299`, `15:318`; DPD: `ind`); `bālo` adj/noun; `subhāsitā` pp vs `dubbhāsitā` adj (`15:177`, `15:180`) | One POS per word and function |

### F. Advisory DPD form check (`verify_key.py --dpd`)

3 474 rows: 1 123 confirmed, 1 079 skipped, 2 087 "ambiguous" (the tag is one of several DPD readings; not errors). Of the 29 rows DPD cannot reconcile, these are real:

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| F1 | `7:216` | `ananda \| noun \| masc.voc.sg \| Ananda` | Short first vowel in the Pāli cell. | `ānanda`, `Ānanda` | 9 |
| F2 | `4:253` | `paggaṇhahi \| imp.2nd.sg` | Imperative is `paggaṇhāhi` (long ā). | `paggaṇhāhi` (check the sentence line too) | 8 |
| F3 | `6:421`, `6:428` | `tam naraṃ` / `tam` | Plain `m` on a free-standing word. | `taṃ` | 9 |
| F4 | `4:47` | `tilā \| noun \| masc.nom.pl` | `tila` is neuter in DPD. | `nt.nom.pl` | 6 |
| F5 | `14:497` | `dukkhasamudayaṃ \| noun \| nt.nom.sg` | `dukkhasamudaya` is masculine; `-aṃ` is acc.sg, or nom.sg only if taken as a neuter adjective (the gloss says "noun acting as an adjective"). | `adj \| nt.nom.sg`, or re-tag | 6 |
| F6 | `12:239` | `chattiṃsa \| card \| fem.nom.pl` | DPD lemma is `chattiṃsā`, fem. sg. | `fem.nom.sg`; check the spelling | 6 |
| F7 | `12:458` | `vīsati \| card \| fem.acc.sg` | acc.sg would be `vīsatiṃ`; the form is nominative. | Re-tag or note | 5 |
| F8 | `13:364` | `munī \| noun \| masc.nom.sg` | `munī` is nom.pl by form; nom.sg only as metrical lengthening. | Add a note "(metrical)" | 5 |
| F9 | `15:438` | `ubho \| pron \| masc.acc.pl` | DPD tags `ubho` as dual. | Leave, or note | 3 |
| F10 | `8:359` vs `15:270` | `hotī"ti` / `hoti"ti` | Sandhi vowel lengthened in one, not the other; sentence at `15:251` has `hotī"ti`. | `hotī"ti` | 7 |
| F11 | `6:147`, `8:160`, `14:30` | `avoca`, `etadavoca \| aor.3rd.sg` | DPD lists `avoca` only as reflexive aorist. Not an error for a beginner key. | Leave | 2 |

The others are DPD limits, not key errors (`catutthaṃ` fem agreeing with `disaṃ`, optatives in `-eyyāmi`, words with `'ti` attached).

---

## Part 2 — Line-by-line reading

Every line of classes 1–15 was read for Pāli forms, tags, glosses and translations. Findings that depend on a root, gender or part of speech were checked against DPD, and anything DPD contradicts was removed (e.g. `uddharati` √dhar, `taṇhā` `√tas･6 ṇhā`, `viharati` `√har (live)`, `gandha` √ghā, `tassa` as `ind`, `sandhāvissaṃ` aor, `accagamā` imperf, `pātimokkha`/`mano`/`kucchi` masc, all of which follow DPD). For classes 1–4, 7–8 and 14 readings were compared with the local SuttaCentral text; for classes 5–6, 9–13 and 15 the canonical readings were recalled, not looked up, and those rows are marked "check text".

Pure notation drift is in section E and is not repeated per class. Numbering is `class.n`; a row that covers two classes takes the number of the first.

### Classes 1–4

Classes 1–4 have no Root column.

#### Sentence and table

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| 4.1 | `4:249`, `4:253` | `paggaṇhahi \| imp.2nd.sg` | Not a valid form (short a before `-hi`); not in DPD. AN4.48 itself reads `paggaṇhe` (opt). Same as F2. | `paggaṇhāhi` | 9 |
| 4.2 | `4:103`, `4:107-108` | `byādhi dhammo amhi`; rows `byādhi \| noun \| masc.nom.sg`, `dhammo \| noun \| masc.nom.sg \| nature` | The source has the compound `byādhidhammomhi` (DPD `byādhidhamma` adj; the exercise writes `byādhi-dhammo`). The first member is tagged as a nominative. | `byādhi-dhammo`; member untagged for case; compound `adj` | 7 |
| 4.3 | `4:118` | `amha-` | The hyphen marks compound stems elsewhere; here it is on a finite verb shortened in sandhi. | `amha` | 6 |
| 4.4 | `4:141`, `4:149` | `panūda` | SN2.8 / Dhp 383 read `panuda`. DPD lists `panūda` as a variant. Check text. | `panuda` | 5 |
| 4.5 | `4:50` | `(honti) \| verb \| pr.3rd.pl` | A row for a word that is not in the key sentence (it is in the exercise, see B3). | Align with B3 | 6 |
| 4.6 | `4:72`, `4:74` | `upasaṅkami,`, `nisīdi.` | Punctuation inside the Pāli cells. | Strip | 8 |
| 2.1 | `2:80` vs `2:84` | `itipi` / `iti'pi` | Sentence and table differ. | One spelling | 8 |
| 2.2 | `2:42`, `2:46` | `uttarissa \| adj \| masc.gen.sg` | A constructed gen.sg of `uttari`, not in DPD; the usual analysis of `uttarimanussadhamma` is `uttari` (ind, "beyond") + `manussadhamma`. | Review the analysis | 5 |
| 3.1 | `3:51-52`, `3:83` | `sabba-rasaṃ`, `dhamma-raso`, `joti-pālaṃ` | Hyphenated in the table only (`3:47`, `3:78`). | Match | 6 |
| 3.2 | `3:318` | `pucchasi — "... diṭṭhiyo loke uppajjanti…` | Quote never closed; `...` and `…` in one line. | Close; one style | 8 |
| 1.1 | `1:11-12` vs `2:88` | `sammā -` + `sambuddhassa` vs `sammāsambuddho` | The same compound is split in class 1 and whole in class 2; space before the hyphen. | One treatment; `sammā-` | 7 |

#### Tags

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| 2.3 | `2:221` | `dukkhehi \| noun \| masc.instr.pl<br>masc.abl.pl` | `dukkha` is neuter (tagged nt at `4:193`). | `nt` | 9 |
| 2.4 | `2:222` | `domanassehi \| noun \| masc.instr.pl<br>masc.abl.pl` | `domanassa` is neuter (DPD). | `nt` | 9 |
| 4.7 | `4:204` | `gahassa \| noun \| masc.gen.sg \| of a house` | `gaha` "house" is neuter (DPD `gaha 2`); masc `gaha` is "grip", "planet". | `nt.gen.sg` | 8 |
| 4.8 | `4:47` | `tilā \| noun \| masc.nom.pl` | DPD has `tila` as nt only; `ime tilā` in the text shows masculine concord. Same as F4. | Check | 5 |
| 4.9 | `4:299`, `4:313` vs `4:335`, `4:206`, `3:40`, `3:119` | `sukhitā \| adj`, `vissuto \| adj` vs `upaddutā`, `diṭṭho`, `ṭhito`, `sitā \| pp` | DPD gives both as pp. | `pp` | 5 |
| 2.5 | `2:315` | `proper noun` | Only Kassapa gets this POS; other names are `noun`. | `noun` | 8 |

#### Glosses and translations

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| 2.6 | `2:367` | `ābādhāya \| masc.dat.sg \| to sufferings` | Plural gloss for a singular; the translation has "to suffering". | "to affliction" | 8 |
| 2.7 | `2:25` | "At the foot of a tree in a forest" | `rukkhānaṃ` is gen.pl (table: "of trees"). | "At the feet of trees" | 7 |
| 2.8 | `2:49`, `2:207-210` | `worthy of an enlightened`; `with recluse`, `with brahmin`, `with deity` | Truncated gloss; missing articles. | Complete | 7 |
| 2.9 | `2:100` vs `2:89` | "endowed with wisdom and ethical conduct" vs "knowledge and conduct" | Gloss and translation differ. | Align | 6 |
| 2.10 | `2:222`, `2:347`, `2:351`, `2:342` | `domanassa`: distresses / depression / displeasure; `jarā`: old age / aging | Three renderings in one file; "there is" supplied without brackets at `2:351`. | Align | 5 |
| 2.11 | `2:8`, `2:12` | `kira \| indeed, truly`; "has indeed arisen" | In SN10.8 `kira` is hearsay (DPD `kira 2` "it is said"). | "it is said" | 4 |
| 2.12 | `2:211`, `2:213`, `2:309`, `2:315`, `2:318` | `Mara`; "of the Gotama"; "of the Kassapa" | Missing diacritic; article before a proper name. | `Māra`; "of Gotama" | 9 |
| 3.3 | `3:110` | "He experiences pleasure by means of the body." | `ca` untranslated. | "And he…" | 6 |
| 3.4 | `3:351`, `4:325` | `bhāsitassa … statement`; `samādhissa … stillness, composure` | Genitive glosses without "of" (neighbours have it). | Add "of" | 6 |
| 3.5 | `3:316` | "You see that offence." | In the Vinaya this is a question. | "Do you see that offence?" | 4 |
| 3.6 | `3:43`, `3:84` vs `3:87`, `3:134`, `3:278`, `3:354` | `he attains.`; "Brahman" / "(brahmin)"; "conducive for"; `come now! let's!`; "Sāriputta. (so that…)" | Stray full stop in a cell; two spellings; idiom; punctuation. | Fix | 8 |
| 4.10 | `4:20`, `4:22` | `I am reborn; I go towards`; "I go towards a good destination" | `upapajjati` = "is reborn in"; the weaker sense was chosen. | "I am reborn in a good destination, a heavenly world" | 6 |
| 4.11 | `4:145`, `4:152` | `cross, lit. cut`; "Cross the stream" | `chinda` is "cut"; "cross" is `tarati`. | "Cut the stream" | 6 |
| 4.12 | `4:236` | "some noblemen [and] brahmins" | `ca` is in the sentence and table; no brackets needed. | "and" | 8 |
| 4.13 | `4:361`, `4:358` vs `4:365` | `pessako … messenger`; "merchant" vs "a trader" | In MN98's list the sense is "servant" (DPD `pessaka 2`); gloss and translation differ. | "servant"; align | 6 |
| 4.14 | `4:32`, `4:377`, `4:424-427`, `4:302` | "He does good deeds"; "disenchanted in suffering"; "It was a thought of the recluse."; "happy (and) free from disease" | Singular `kusalaṃ`; idiom "with"; `ahu` + gen is "the recluse had"; order reversed. | Fix | 5 |
| 4.15 | `4:83`, `4:88`, `4:312`, `4:318`, `4:314`, `4:209`, `4:49` | `Rahula`; `Angulimāla`; `The Buddha` in a gloss; "O, Builder of a house"; `dehusked rice"` | Diacritics; capitals; stray quote. | Fix | 9 |
| 4.16 | `2:78`, `3:134`, `4:236` vs `3:340`, `4:282`, `4:302`, `4:318`; `3:19`, `3:30` vs `4:185` | `[and]` vs `(and)`, `(about)`, `(for)`; `[+gen]` in Grammar vs `(+acc)` in the English column | Bracket style and column vary. | One form | 7 |

### Classes 7–8

#### Sentence and table

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| 7.1 | `7:210`, `7:216` | `siyā kho pana ananda`; `ananda` | Short first vowel (source: `panānanda`). Same as F1. | `ānanda` | 9 |
| 7.2 | `7:66` vs `7:70`; `7:408`, `7:417` | `kin'ti` / `kinti`; Grammar `pron+ind` vs `interr` | Sentence and table differ; same word tagged two ways. | `kin'ti`; one tag | 8 |
| 7.3 | `7:291` vs `7:295-303` | `kupitā vā anattamanā vā` | Second `vā` has no row (other items list each one, `7:125-129`). | Add | 7 |
| 7.4 | `7:144`, `7:150` vs `7:307`, `7:318` | `anāgatamaddhānaṃ` / `anāgatam'addhānaṃ` | Same phrase, same sutta. | One spelling | 8 |
| 7.5 | `7:166`, `7:170` vs `8:238`, `8:242`, `13:44` | `yaṃnūn'āhaṃ` (`ind+pron.1st.nom.sg`) / `yan'nūn'āhaṃ` (`pron+ind+pron.1st.nom.sg`) | Two spellings and two analyses of one idiom. | One | 8 |
| 7.6 | `7:32` | `mallā,` | Comma in the Pāli cell. | Strip | 7 |
| 7.7 | `7:179`, `7:188` | `avaṅkatā \| adj … not dishonest` | Not in SN12.22 in the SuttaCentral text; DPD's sense is a fem. abstract noun "straightness". Item is `(simpl)`. Check text. | Check | 4 |
| 8.1 | `8:614`, `8:626` | `nārīsu` | Dhp 284 reads `nārisu` (short i, metre); not marked `(simpl)`. Check text. | `nārisu` | 6 |
| 8.2 | `8:348`, `8:359` | `phāsu hotī"ti`; `hotī"ti` | Closing quote with no opening quote; double quote inside a table word. | Add `"`; `hotī'ti` | 6 |
| 8.3 | `8:31` vs `8:40`; `8:116` vs `8:138` | `nāmagottāni` / `nāma-gottāni`; `abhijjhādomanassaṃ` / `abhijjhā-domanassaṃ` | Hyphen in the table only. | Match | 6 |

#### Tags

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| 8.4 | `8:376-377` | `dakkhiṇena \| adj \| masc.instr.sg`; `passena \| noun \| nt.instr.sg \| with the right side…` | The adjective must agree with its noun; "right" also sits in the gloss of `passena`. | `nt.instr.sg`; "with the side" | 8 |
| 7.8 | `7:455` | `āpā \| noun \| masc.nom.pl` | DPD: `āpa` nt (and `āpas` masc). | Check; `nt.nom.pl` | 5 |
| 7.9 | `7:441` vs `8:601` | `koci'd'eva \| ind \| pron+ind` vs `idiom \| pron+ind` | A declined pronoun agreeing with `paccayo`; two POS. | `pron \| masc.nom.sg` | 6 |
| 7.10 | `7:267` | `atītaṃ \| adj \| masc.acc.sg \| the past` | Used as a noun; DPD `atīta` "the past" is nt. | `noun \| nt.acc.sg` | 5 |
| 7.11 | `7:482` | `assavanatā \| noun \| fem.instr.sg (+gen)` | `-tā` is not an instrumental ending; usually explained as an ablative of cause. | `fem.abl.sg`; check | 4 |
| 7.12 | `7:462` | `kissa \| pron.<br>interr \| masc.dat.sg \| for what reason?; why?` | Neuter fits "why"; markup in the POS cell. | `pron \| nt.dat.sg` | 5 |
| 7.13 | `7:295`, `7:456`, `8:545` vs `7:386` | `ce \| ind \| ind` vs `cond` | Two labels. | `cond` | 7 |
| 8.5 | `8:206` | `aññataro \| adj` | DPD: pron; `aññaṃ`, `anaññaṃ`, `ekaccassa` are `pron` here. | `pron` | 6 |
| 8.6 | `8:339` | `vīsatigaṇo \| noun \| group of twenty` | Bahubbīhi qualifying `bhikkhusaṅgho` (DPD: adj). | `adj` | 6 |
| 8.7 | `8:234` | `dūramaṃ \| adj \| masc.acc.sg [+loc]` | No masc acc noun to agree with; predicate of the `yattha` clause. | `nt.nom.sg` | 5 |
| 8.8 | `8:495` | note "can be taken as a noun masc instr sg" on `abhikkantavaṇṇā` | Instr.sg of `vaṇṇa` would be `-vaṇṇena`; `-ā` is ablative. | Reword | 4 |
| 7.14 | `7:333` | `gāhaṃ \| noun \| masc.acc.sg \| hiding place \| √gah･6 ṇhā (grasp)` | "Hideaway; lair" is DPD `gāha 2.2`, from `√gāh` (dive, plunge); `√gah` belongs to `gāha 1` "seizure". | `√gāh･1 a (dive, plunge)` | 8 |

#### Glosses and translations

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| 7.15 | `7:362` vs `7:361`, `7:364` | `upāsikāyo … female disciples` | "lay" missing. | "female lay disciples" | 7 |
| 7.16 | `7:289` | "which I am grasping [and] would not be with faults" | `upādiyamāno` is subordinate to `assaṃ`. | "which, grasping [it], I would not be with faults" | 6 |
| 7.17 | `7:225` | "And now there could be, Ananda, for you it would occur like this" | `siyā` and `assa` both rendered; broken sentence. | "Now, Ānanda, it could be that it would occur to you thus:" | 5 |
| 7.18 | `7:121`, `7:131` | `rājāno … king's men` | Nom.pl "kings". | "kings [i.e. the king's men]" | 5 |
| 7.19 | `7:431` | "Bhikkhus, the monks will establish…" | Same word rendered two ways; the quoted clause is a question in the Pāli. | "Monks…"; phrase as a question | 5 |
| 7.20 | `7:484`, `7:466` | `parihāyanti … wasting away; decreasing`; "What one could do with a well, if there always would be water?; Having cut off the craving from the source" | Participle gloss for a finite verb; word order; `?;`; `taṇhāya` is tagged gen (`7:459`) but translated as object. | Fix | 6 |
| 7.21 | `7:35`, `7:321`, `7:374`, `7:454`, `7:37`, `7:115` | `was extinguished""`; unclosed `"may I be…`; `[dat or purpse]`; "with well"; no full stop; lower-case start | Typos. | Fix | 9 |
| 7.22 | `7:34`, `7:37`, `7:45`, `7:51`, `7:216`, `7:225`, `8:79`, `8:162`, `8:48`, `8:59` | `Kusinara`, `Vesali`, `Ananda`, `The Great Mogallana` | Names without diacritics; "Mogallana" misspelt (`7:84` has "Moggallāna"). | Fix | 8 |
| 8.9 | `8:42` | "The great rivers, upon reaching the mighty ocean, they give up (their) old names." | `-gottāni` dropped; redundant "they". | "…give up (their) former names and family names." | 7 |
| 8.10 | `8:448` | "…[the sequence] of that man's mothers' mothers would not even be exhausted." | `bhikkhave` omitted. | Add "monks" | 7 |
| 8.11 | `8:636` | "of a man enamoured with regard to women, just that long he [is] like…" | `paṭibaddhamano` is nominative and agrees with `so`, not with gen `narassa`. | "…just that long he [is] enamoured, like a suckling calf towards [its] mother." | 7 |
| 8.12 | `8:329` | "This monk who speaks according to the Dhamma, and this monk who…, speaks according to…" | Three coordinated predications turned into one relative clause. | "This monk is one who speaks according to the Dhamma, …" | 6 |
| 8.13 | `8:367`, `8:361` | "having done this just for that reason, [and] no other"; `eva … thus; just` | "having made just this the reason"; `eva` is not "thus". | Fix | 6 |
| 8.14 | `8:538`, `8:527` | "…for the continuance, non-disappearance , increase and fulfillment by development, maturity, of wholesome qualities…" | Order garbled; `bhāvanāya` tagged dat but translated "by". | Reorder | 6 |
| 8.15 | `8:417` vs `8:414`, `8:425`; `8:468`; `8:560` vs `8:553` | `sabbanimittānaṃ … of all objects` vs `animitta` "signless"; `mahattarī … older than`; "can set aside" vs "should set aside" | Same stem two ways; stray "than"; modality. | Align | 4 |
| 8.16 | `8:363`, `8:112`, `8:114`, `8:304`, `8:470`, `8:138` | `having done[something]`; `it stayed.`; "Senior nun grabbed…"; "of man's intention to a woman…"; missing commas; `&` | Typos and articles. | Fix | 7 |


### Classes 5–6

#### Sentence and table

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| 5.1 | `5:551`, `5:558-559` | `mā pamādaṃ attha`; rows `pamādaṃ \| noun \| masc.acc.sg`, `attha \| verb \| imp.2nd.pl \| you all must be` | MN19 reads `mā pamādattha`, one aorist 2nd pl of `pamajjati` (compare `pamādo \| aor.2nd.sg` at `5:620`). Split into noun + imperative it says "be negligence". The same split is in `bpc/class_5/6_say_no.md` (A13 of the BPC audit). | `mā pamādattha`; one row, `aor.2nd.pl` | 8 |
| 5.2 | `5:584` vs `5:588-597` | `na me tayā saddhiṃ kathā vā nisajjā vā` | `tayā` has no table row. | Add `tayā \| pron \| 2nd.instr.sg \| with you` | 9 |
| 5.3 | `5:9` | `tumhākaṃ,` | Comma carried into the cell. | `tumhākaṃ` | 8 |
| 5.4 | `5:287` | `"alaṃ, gāmaṇi. mā maṃ etaṃ pucchi` | Opening quotation mark never closed. | Remove `"` | 8 |
| 6.1 | `6:28` vs `6:35`, `6:37` | `esa bhagavato sāvakasaṅgho` | The table has a row `āhuneyyo` and the translation says "is worthy of offerings", but the word is not in the sentence. | Add `āhuneyyo` to the sentence | 9 |
| 6.2 | `6:353` vs `6:364` | `sukhit'attā` / `sukhitattā` | Sentence and table differ. | One form | 8 |
| 6.3 | `6:353`, `6:358` | `sukhino vā khemino hontu`; `vā \| conj \| or` | Snp 1.8 reads `sukhinova` = `sukhino va` (emphatic), not "or". Check text. | `va \| ind \| emph`; "happy and safe" | 6 |
| 6.4 | `6:410`, `6:415` | `bāhu-pacālakaṃ` | Hyphen inside the word; Sekhiya reads `bāhuppacālakaṃ`. Check text. | `bāhuppacālakaṃ` | 6 |
| 6.5 | `6:296` vs `6:300-304`; `6:535` vs `6:539-549` | three `ca` in the sentence, one row; second `ca` missing | Repeated particles have a row elsewhere (`6:207-214`). | Add rows | 5 |

#### Tags

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| 5.5 | `5:530`, `5:536` | `kadariyaṃ \| noun \| nt.acc.sg \| stinginess`; "conquer liar by truth" | In Dhp 223 it parallels `alikavādinaṃ`, a person. DPD has both `kadariya 1` adj "miserly" and `kadariya 2` nt "miserliness". | `adj \| masc.acc.sg \| the miser`; "conquer the miser by giving, the liar by truth" | 7 |
| 5.6 | `5:295` | `etaṃ \| pron \| masc.acc.sg` | The thing asked about; neuter. | `nt.acc.sg` | 6 |
| 5.7 | `5:305` | `no \| pron \| 1st.acc.pl \| us` | The translation (`5:313`) says "to us". | `1st.dat.pl` | 5 |
| 5.8 | `5:596` | `phāsu \| noun \| masc.nom.sg` | DPD allows masc noun, adj and ind; as predicate of `hoti` the adjective is the natural reading. `10:476` has `ind \| adv`. | Leave or `adj`; align with `10:476` | 4 |
| 6.6 | `6:548` | `mānaṃ \| noun \| nt.acc.sg \| pride; conceit` | `māna` "conceit" is masculine (DPD `māna 1.1`); the neuter `māna 2.1` is "measure". | `masc.acc.sg` | 9 |
| 6.7 | `6:157`, `6:159` | `dakkhanti \| verb \| pr.3rd.pl \| see` | In `cakkhumanto rūpāni dakkhanti` the usual reading is future. DPD has both `dakkhati 1` pr and `dakkhati 2` fut. | `fut.3rd.pl \| will see`, or keep with a note | 6 |
| 6.8 | `6:88` | `atthi \| verb \| pr.3rd.pl \| there are` | `atthi` is 3rd sg in form, here with a plural subject. | `pr.3rd.sg` + note | 6 |
| 6.9 | `6:269` vs `6:211` | `garuṃ \| noun \| masc.acc.sg \| respect` vs `garu \| adj` | DPD has `garu 5` masc "respect", so the tag is defensible; the two rows read differently only because of the idiom `garuṃ karoti`. | Leave; consider an idiom row | 3 |

#### Glosses and translations

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| 5.9 | `5:380`, `5:383` | `the corpse; dead body`; "on the dead body of the Tathāgata" | In DN16 the flowers fall on the living Tathāgata. | "body" | 7 |
| 5.10 | `5:381`, `5:383` | `okiranti … are sprinkled on`; "Flowers are sprinkled on" | Passive gloss for an active verb (DPD: "sprinkles; scatters down"). | "they scatter down on" | 6 |
| 5.11 | `5:629` | "you must make [your] mind unified!" | Second `jhāne` untranslated. | "…unified in meditation!" | 7 |
| 5.12 | `5:618`, `5:629` | `brāhmaṇa`; "Monk, don't be careless" | `brāhmaṇa` rendered "Monk". | "Brahmin" | 6 |
| 5.13 | `5:106`, `5:112` | `hell; no good fortune`; "leads to no good fortune" | The translation uses the etymological gloss and loses the contrast with `sugati`. | "leads to hell" | 6 |
| 5.14 | `5:72`, `5:74` | `for decoration, for bulk`; "nor for physical appearance" | "for bulk" does not fit `vibhūsana`; the translation matches neither gloss. | "for decoration; for beautification" | 5 |
| 5.15 | `5:549` | "It is enough for deluding a fool not one seeking Nibbāna." | The contrast is unmarked. | "…a fool, [but] not one seeking…" | 7 |
| 5.16 | `5:582` | "You are truly for us equal to the Brahma." | Word order; article; diacritic. | "Truly, for us you are equal to Brahmā." | 6 |
| 5.17 | `5:35-37` vs `5:347-349` | "should be purified" vs "will be pure/purified" | Same MN39 construction, two modalities. | "will be" | 6 |
| 5.18 | `5:273`, `5:324` | "Whatever conversation was with wandering ascetics"; "Services (done) on us could be of great fruits." | Ungrammatical; future rendered "could be". | "Whatever conversation there was with…"; "…for us will be of great fruit." | 6 |
| 6.10 | `6:342`, `6:344` vs `5:168` | `hirimanto … conscientious`, `ottappino … feeling shame`; class 5 has `ottappino … conscientious` | The two glosses look swapped in class 6 (DPD `ottappī`: "afraid of wrong; conscientious"). | `hirimanto` "having a sense of shame"; `ottappino` "conscientious" | 8 |
| 6.11 | `6:533` | "…who sees fault, he is (like) one who points out the treasure." | Comma splice; `nidhīnaṃ` is gen.pl (so `6:524`). | "…who sees faults, like one who points out treasures." | 6 |
| 6.12 | `6:542`, `6:551` | `atho … and then; after that` | `atho` here is "and also", not temporal. | "and also towards the eldest brother" | 5 |
| 6.13 | `6:408` | "would approach [there], cause an alteration in a robe…" | Futures (glossed "will…") rendered "would"; no "and". | "will approach and…" | 5 |
| 6.14 | `6:450` | "the support of the wife and son" | Pāli order is son, then wife. | "supporting son and wife" | 5 |
| 6.15 | `6:465` | "Just make an effort today" | `eva` qualifies `ajja`. | "this very day" | 5 |
| 6.16 | `6:390`, `6:155`, `6:87` | `you must minister; enjoy`; `lit: one having eyes quality`; `lit. breathing being` | "enjoy" does not fit; unidiomatic; number. | "attend on"; "lit. possessing eyes"; "breathing beings" | 6 |
| 6.17 | `6:45`, `6:46`, `6:48` | `ānanda` (English column); `this[thought]`; "Venerable Ananda" with no full stop | Lower-case name without dative sense; missing space; missing diacritic. | `to Ānanda`; `this [thought]`; "…venerable Ānanda." | 9 |
| 6.18 | `5:95`, `5:99`, `5:578` | `Sariputta`, `Brahma` | Missing diacritics (`Sāriputta` at `5:433`). | Add | 9 |
| 6.19 | `5:320`, `6:378-380`, `5:190`, `6:322` | `for us; \|`; "conducive for"; comma between subject and verb twice | Trailing semicolon; idiom is "conducive to" (so `5:447`). | Fix | 7 |

### Classes 9–10

#### Sentence and table

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| 9.1 | `9:59`, `9:61-70` | `… samudayāya. katamāni tīṇi?` | The question is in the sentence but not in the table, the translation or the exercise (B8). Item 6 (`9:104-107`) does include its `katamāni cattāri`. | Remove, or add rows and "What three?" | 9 |
| 9.2 | `9:72` vs `9:85-87` | `kallaṃ nu taṃ samanupassituṃ` | `nu` has no row. | Add `nu \| ind \| interr` | 9 |
| 9.3 | `9:628` vs `9:632-640` | four `vā`, three rows | Final `vā` missing. | Add | 7 |
| 9.4 | `9:585`, `9:600-601` | `vatthuṃ desanāya` | The Pātimokkha has the compound `vatthudesanāya`; split without `(simpl)`. Check text. | Mark `(simpl)` | 4 |
| 10.1 | `10:342`, `10:349` | `khuddaṃ samācare` | The Mettasutta reads `khuddamācare` = `khuddaṃ ācare`; the `m` appears to have been read as `sam-`. Both `ācarati` and `samācarati` exist. Check text. | `khuddaṃ ācare` | 7 |
| 10.2 | `10:744`, `10:748` | `anekajāti saṃsāraṃ`; `anekajāti \| adj \| masc.nom.sg` | A compound written as two words; the first member cannot be nom.sg. | `anekajātisaṃsāraṃ`, or tag as a compound member | 8 |
| 10.3 | `10:666` vs `10:676-677` | `yāvat'āssa` / `yāvatā-` + `assa` | Apostrophe placement implies a different split from the table. | Match | 5 |

#### Tags

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| 9.5 | `9:334` | `ajjhāvasatā \| noun \| masc.nom.sg [+acc] \| one who is domestically settled` | Present participle, instrumental singular (agent of `na sukaraṃ … carituṃ`). Nominative is impossible for `-atā`; DPD has `ajjhāvasanta` prp. | `prp \| masc.instr.sg [+acc] \| by one living in` | 9 |
| 9.6 | `9:182` | `dassanāya \| noun \| masc.dat.sg` | `dassana` is neuter. | `nt.dat.sg` | 9 |
| 9.7 | `9:76-79`, `9:373` | `yaṃ / aniccaṃ / dukkhaṃ / vipariṇāmadhammaṃ \| nt.acc.sg`; `yaṃ \| nt.acc.sg` | Nominal relative clauses ("whatever is impermanent…", "what is not yours"); nominative. Only `taṃ` is the object. | `nt.nom.sg` | 7 |
| 9.8 | `9:260-262` | `anupubbasikkhā`, `-kiriyā`, `-paṭipadā \| fem.acc.pl` | With `sakkā … paññapetuṃ` the logical object is nominative singular; the translation (`9:265`) is singular. | `fem.nom.sg` | 7 |
| 9.9 | `9:555-558` | `parikkhāre`, `bhesajje`, `paccaye \| acc.pl` | They depend on `ussukā` (+loc); the verse continues with a locative. | `loc.sg` "in regard to" | 6 |
| 9.10 | `9:463` | `tassa \| pron \| masc.gen.sg \| of that` | `tassa me` = "to me (being such)", agreeing with `me`. | `masc.dat.sg` | 6 |
| 9.11 | `9:404`, `9:445` | `kiṃ \| ind \| interr` | Predicate / object pronoun ("what am I?", `taṃ kiṃ maññasi`); tagged `pron` at `9:692`. | `pron \| nt.nom.sg` / `nt.acc.sg` | 5 |
| 9.12 | `9:85` | `kallaṃ \| ind \| -` | DPD `kalla 1.4` adj "proper"; predicate nt.nom.sg. | `adj \| nt.nom.sg` | 5 |
| 10.4 | `10:273` | `sahatthā \| ind \| masc.instr.sg` | POS `ind` with a case tag; DPD: `ind`. | `ind \| adv` | 8 |
| 10.5 | `10:519-520`, `10:527-528` | `imasmiṃ`, `sati`, `asati \| masc.loc.sg` | Same referent is neuter in `idaṃ`, `imassa` (`10:521`, `10:523`, `10:532`). | `nt.loc.sg` | 7 |
| 10.6 | `10:141`, `10:396` | `evaṃ \| ind \| emph` | `adv` in the same sentence (`10:398`). | `adv` | 8 |
| 10.7 | `10:365` | `purato \| ind \| prep` | Parallel `pacchato` (`10:363`) is `adv`. | `adv` | 6 |

#### Glosses and translations

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| 9.13 | `9:191-192` | `atha \| ind \| ind \| after`; `kho \| ind \| ind \| that` | `kho` does not mean "that"; "after that" was split across the two words. `9:127` treats `atha kho` as one unit. | One row, "and then" | 9 |
| 9.14 | `9:367` | "Is the Blessed One, the Arahant, …" | `bhante` and `pana` untranslated. | Add "venerable sir" | 8 |
| 9.15 | `9:486` | "But because form is not self, therefore it leads to oppression." | `bhikkhave` omitted; "oppression" is the "lit." gloss, not the primary "illness" (`9:483`). | "…form, monks, is not self, form leads to affliction" | 8 |
| 9.16 | `9:564` | "They were not overly zealously desiring medicines and requisites for life." | `paccaye` omitted; order changed. | Add "supports" | 7 |
| 9.17 | `9:663` | "I, too, will myself be able to make safety." | `api` goes with `ekam'ekena`; `attānaṃ sotthiṃ kātuṃ` = "to make myself safe". | Reword | 6 |
| 9.18 | `9:674`, `9:679` | `anissito`: "independent" | In context "unsupported"; "independent" hides why he cannot cross. | "unsupported" | 6 |
| 9.19 | `9:213` | "in the slightest fault … [by] undertaking the training precepts" | `vajjesu` plural; locative `sikkhāpadesu` lost; "precepts" vs gloss "rules". | "in the slightest faults … train in the training rules" | 5 |
| 9.20 | `9:417`, `9:421`, `9:581`, `9:544` | "have come"; "it will be"; `vaḍḍhati … increase`; "actions; deed" | Number / person agreement. | "has come"; "he will be"; "increases"; "deeds" | 7 |
| 9.21 | `9:542` | "any states o existence" | Typo. | "of" | 10 |
| 9.22 | `9:178`, `9:116`, `9:121`, `9:30`, `9:138-199` | `gotama`; "Kalamas"; "Son of Sari"; "Sāvatthi" | Lower-case name; missing diacritics; stem is `Sāvatthī`. | Fix | 7 |
| 9.23 | `9:244`, `9:11` vs `9:447` | "for the comfort of"; "Brahman" vs "brahmin" | Stray "of"; two spellings. | Fix | 7 |
| 10.8 | `10:445` | "One who has gone forth certainly does not harm another, a monk is not troubling another." | Subject and predicate inverted. Dhp 184: one who harms another is no renunciant; one troubling another is no ascetic. | Rephrase | 8 |
| 10.9 | `10:704` | "Thus, having heard here, …" | Nothing means "thus"; `ito` is "from here" (so `10:688`). | "Having heard from here…" | 8 |
| 10.10 | `10:219` | "Just like a monkey…" | `bhikkhave` omitted; forest/woodland in reverse order. | Add "monks" | 8 |
| 10.11 | `10:405` | "The mind of him who sees and knows…" | Order reversed (`jānato … passato`); both `evaṃ` dropped. | "who knows thus, sees thus" | 7 |
| 10.12 | `10:636` | "When a monk having desire for sense pleasure internally.." | `idha, bhikkhave` dropped; `santaṃ` agrees with `kāmacchandaṃ`; no "when" in the Pāli. | "Here, monks, a monk [knows] sensual desire [when] present internally…" | 7 |
| 10.13 | `10:274`, `10:278` | "it can be carried" / "it could be carried" | Plural ptp of obligation. | "they are to be carried" | 6 |
| 10.14 | `10:334`, `10:340` | "by means of seeing; considering" | Instrumental of agent with `alaṃ`: "for one who considers… it is fitting to strive". | Re-gloss | 6 |
| 10.15 | `10:168-171`, `10:160-166` | `eva \| just; thus`; "completely quenched" vs "attains final liberation"; "perturbed" vs "shaking" | `eva` is not "thus"; gloss and translation disagree. | Align | 6 |
| 10.16 | `10:10` vs `10:19-38` | `āha … he had said` | Pluperfect once; "he said" three times. | "he said" | 8 |
| 10.17 | `10:693`, `10:691` vs `10:695`, `10:521-534` | `imesaṃ … of those`; `amutra` "there" / "in such-and-such place"; `idaṃ` "that; lit. this" / "this" / "that" | `imesaṃ` is "these" (`10:699`); same word two ways in one sentence. | Align | 6 |
| 10.18 | `10:758`, `10:428`, `10:384` | "searching the builder of this house"; "this is my instruction to them"; `āpajjati` "for arousing" | "for"; "this" not in the Pāli; `evarūpī` untranslated; `āpajjati` is "engages in". | Reword | 6 |
| 10.19 | `10:142`, `10:389`, `10:555`, `10:722`, `10:356`, `10:733`, `10:740` | "not seeing perceiving"; "When one investigating…"; "How many staying awake…"; "wise would reprove"; "cross over", "run along" | Missing separator; ungrammatical; missing article; bare verbs for an adjective and a 3rd sg verb. | Fix | 7 |

### Classes 11–12

#### Sentence and table

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| 12.1 | `12:462`, `12:466` | `vassaṁ \| noun \| nt.acc.sg \| year` (twice) | The sentence (`12:437`) has `cattārīsaṃ api vassāni` and `paññāsaṃ api vassāni`. The two rows are copies of `12:448`. | `vassāni \| nt.acc.pl \| years` | 9 |
| 12.2 | `12:94-120` | — | Both `bhikkhave` in the sentence lack a row; every other item lists it. | Add | 7 |
| 12.3 | `12:339`, `12:345` | `caturāsītīnaṃ … fem.dat.pl` | A plural of a decade numeral; not in DPD's inflections. The text has `caturāsītiyā pāṇasahassānaṃ`. Check text. | `caturāsītiyā` | 6 |
| 12.4 | `12:358`, `12:369` | `samanta'pāsādiko` | Apostrophe where nothing is elided. | `samantapāsādiko` | 6 |
| 11.1 | `11:237` vs `11:241`; `11:461` vs `11:471`; `12:48` vs `12:62` | `seyyathā'pi` / `seyyathāpi`; `vigat'ūpakkilese` / `vigatūpakkilese`; `evam'eva kho` / `evameva kho` | Sentence and table differ. | Match | 8 |
| 11.2 | `11:487`, `11:504` | `'khīṇā jāti…`; `\| 'khīṇā \|` | Opening quote never closed, and carried into the cell. | Remove | 7 |
| 11.3 | `11:577` | `diṭṭhiṭṭhānaṃ, — so loko … ṭhassāmī'ti, — nanu` | Comma plus dash twice; closing `'ti` with no opening quote. | Tidy | 6 |
| 11.4 | `11:624`, `11:638` | `eta'r'ahi` | Unusual split of `etarahi`. | `etarahi` | 5 |
| 11.5 | `11:427`, `11:437` | `opanayiko` | DPD has both `opanayika` and `opaneyyika`; CST reads `opaneyyiko`. Check which edition the course follows. | Leave or align | 4 |
| 11.6 | `11:237`, `11:409`, `12:339`, `12:377`, `12:94` | reworded sentences | Rewritten against the canon but not marked `(simpl)`. Check text. | Add `(simpl)` | 5 |

#### Tags

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| 11.7 | `11:170`, `11:172` | `ujū`, `suhujū \| adj \| masc.nom.pl` | The subject is singular (`sakko … suvaco cassa`); `-ū` is metrical lengthening. | `masc.nom.sg` | 9 |
| 11.8 | `11:566` | `maṃ \| pron \| masc.acc.sg` | Personal pronouns carry person, not gender (`1st.gen.sg` elsewhere). | `1st.acc.sg` | 9 |
| 11.9 | `11:650` | `ca \| ind \| adv` | `conj` in 80 other rows. | `conj` | 9 |
| 11.10 | `11:662-663`, `11:665` | `dheyyaṃ`, `suduttaraṃ \| nt.nom.sg`; "…the far shore; the realm of death, extremely difficult to cross." | No nominative role; it is the object crossed. The translation leaves it dangling. | `nt.acc.sg`; "will go beyond the realm of death, so hard to cross" | 6 |
| 11.11 | `11:50-56` | `ādittacelo \| noun`, `āditta- \| pp \| masc.nom.sg`, `-celo \| adj` | Bahubbīhi glossed adjectivally but tagged `noun`; its members get `pp … nom.sg` and `adj`, the reverse of what they are. | Compound `adj`; members untagged for case | 6 |
| 11.12 | `11:253` | `mettāya \| noun \| fem.instr.sg` | In apposition to `cetovimuttiyā` in the loc abs. | `fem.loc.sg (loc abs)` | 5 |
| 11.13 | `11:584` | `attaniye \| adj \| masc.loc.sg` | Substantive "what belongs to self"; neuter. | `nt.loc.sg` | 5 |
| 11.14 | `11:203-211`, `11:363-373` vs `11:422`, `11:520` | `aniccato \| ind \| adv` vs `paṭilābhato`, `accayato \| noun \| masc.abl.sg` | The same "-to = as X" construction tagged two ways. | One | 6 |
| 12.5 | `12:416` vs `12:87` | `satehi \| adj \| masc.instr.pl` vs `noun \| nt.instr.pl` | DPD `sata 2.1` is `card`. | `card` or `noun \| nt.instr.pl` | 7 |
| 12.6 | `12:654`, `12:660` | `bhagavā \| masc.nom.sg`; "May the Blessed One tell [us]" | The verb is `brūhi`, imp.2nd.sg; this is an address. | `masc.voc.sg`; "Tell [us] …, Blessed One" | 6 |
| 12.7 | `12:657` | `parābhavato \| noun \| masc.abl.sg \| for/of the downfall` | Gloss is gen/dat, tag is abl. Usually gen.sg of the prp ("of one who is declining"); DPD has the verb `parābhavati`. | `prp \| masc.gen.sg` | 6 |
| 12.8 | `12:605-607`, `12:618` | `vanappagumbe`, `phussit'agge \| masc.loc.sg` | The translation treats it as the subject of the simile. | Tag and translation should agree | 5 |
| 12.9 | `12:593-597` | `pārājikena … nt`, `saṅghādisesena … masc`, `pācittiyena … masc` | Three parallel terms with different genders. DPD: `pārājika` nt, `saṅghādisesa` masc, `pācittiya` nt. | `pācittiyena` → `nt` | 6 |
| 12.10 | `12:110`, `12:492` | `yena \| ind \| adv`; `sarena \| ind \| adv` | A relative pronoun and an instrumental noun tagged as adverbs. | `pron \| masc.instr.sg`; `noun \| masc.instr.sg` | 5 |

#### Glosses and translations

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| 11.15 | `11:611` | "‘that which the world [is] the self (world = self); …" | Garbled; `so loko so attā` = "that [which is] the world, that [is] the self"; the third `so` is untranslated. | Reword | 7 |
| 11.16 | `11:425` | "For one perceiving acquisition as a personal acquisition of forms…" | Genitive chain attached to the wrong noun; "personal" has no source. | "For one regarding the acquisition of forms … as an acquisition" | 6 |
| 11.17 | `11:306` vs `11:319` | `tāni … these` | "those" (so the translation). | "those" | 7 |
| 11.18 | `11:66` | `hoti … there is; there was` | "there was" is not present tense. | Remove | 6 |
| 11.19 | `11:367`, `11:376` | "as an arrow; a dagger" / "as a dagger" | `salla` is a dart. | "as a dart" | 6 |
| 11.20 | `11:674`, `11:628-636`, `11:569`, `11:146` | `yassa … of which; whoever`; `ye … which`; `sāsane … the teachings`; `adhunā … soon, recently` | Genitive "whose"; persons take "who"; loc.sg without "in"; "soon" is wrong. | Fix | 6 |
| 11.21 | `11:341`, `11:178`, `11:29` | "near or far away"; "straight, upright"; "about Venerable Gotama" | Order reversed; `su-` lost; `taṃ` untranslated. | Fix | 5 |
| 11.22 | `11:141`, `11:151` | `ānanda` (English column); "Ananda, … [who] recently come" | Lower-case; diacritic; grammar. | "Ānanda … [who have] recently come" | 9 |
| 11.23 | `11:15`, `11:119`, `11:477`, `11:319`, `11:665`, `11:258`, `11:609`, `11:620` | "Bhikkhus you should…"; "imagine if…"; "pliable workable"; "conducive for"; "whoever acting according to"; `[lit:made a vehicle]`; stray `"` in two gloss cells | Punctuation and grammar. "Bhikkhus" is "Monks" everywhere else. | Fix | 8 |
| 12.11 | `12:29` vs `12:9` | "I recollected manifold past lives" | Verb is present (`anussarāmi`, glossed "I remember"). | "I recollect" | 7 |
| 12.12 | `12:375` | "Surely, a monk endowed with…" | `bhikkhave` untranslated. | Add "monks" | 8 |
| 12.13 | `12:618`, `12:610` | "(The Buddha) taught the sublime teaching,<br>leading to the highest Nibbāna, for the benefit."; `gimhe … in heat; hot` | `tath'ūpamaṃ` untranslated; `paramaṃ` attached to Nibbāna; "first heat of the hot month" for `paṭhamasmiṃ gimhe`. | "so too he taught the sublime teaching leading to Nibbāna, for the highest benefit"; "in the first month of summer" | 6 |
| 12.14 | `12:599` | "having then seen that should speak" | "then" has no source; `tam'enaṃ` is "him" (so the table). | "having seen him, should speak…" | 6 |
| 12.15 | `12:87`, `12:347` | "with one hundred monks"; "for one thousand" | Plural forms (`-satehi`, `sahassānaṃ`). | "hundreds"; "thousands" | 6 |
| 12.16 | `12:12-27`, `12:235`, `12:447-461` | `api`: "just only", "just two" …; "only" and "even" in one sentence; dropped in `12:235` | `pi` is "also / even", not limiting. | "also; even" | 6 |
| 12.17 | `12:536`, `12:281`, `12:46` | "I will clarify"; "knowledge and vision were not"; "there could be hen's eggs" | Present tense; singular; unbracketed supply. | Fix | 5 |
| 12.18 | `12:222`, `12:135`, `12:281` | "Some monks and brahmins who speaking thus, holding such view…"; "…noble truths, which four?"; `aspects….` | Ungrammatical; comma splice; ellipsis plus full stop. | Fix | 8 |
| 12.19 | `12:454-460` | `three (3)` … `forty (40)` | Digits in brackets in this item only. | Remove, or apply everywhere | 5 |

### Classes 13 and 15

#### Sentence and table

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| 13.1 | `13:537` vs `13:546-548` | `yathābālaṃ yathāmūḷhaṃ yathāakusalaṃ` | `yathāakusalaṃ` has no row; the translation (`13:557`) has "so unskilfully". | Add row | 10 |
| 13.2 | `13:187`, `13:191` | `ce bhikkhuṃ aññe bhikkhū …` | The rule reads `tañce bhikkhuṃ`; enclitic `ce` cannot open a sentence, and the translation still supplies "[that]". Not marked `(simpl)`. Check text. | `tañ'ce bhikkhuṃ` + `taṃ` row | 6 |
| 13.3 | `13:187`, `13:210` | `bhiyyo'ti` | The rule continues `bhiyyo, na ca tassa bhikkhuno…`; the `'ti` and closing quote are not in it. Check text. | `bhiyyo` | 5 |
| 13.4 | `13:439`, `13:449` | `supatiṭṭhitā \| adj.` | Khp 7 in CST reads `suppatiṭṭhitā`; DPD has both lemmas. Stray full stop in POS. Check text. | `suppatiṭṭhitā`; `adj` | 5 |
| 13.5 | `13:458`, `13:288` | `chakkhattuṃ paramaṃ`; `evam'pi kho bhikkhu tehi bhikkhūhi` | Compound split / sentence abridged without `(simpl)` (items 2, 4, 7 are marked). Check text. | Mark `(simpl)` | 5 |
| 13.6 | `13:582` | `na tena tato tvaṃ … dukkhassā"ti.` | Comma missing after the second `na tena` (the parallel has one); `"ti` with no opening quote. | Add comma | 6 |
| 15.1 | `15:155-160` | table has only `imehi`, `kho,` | Six words of the sentence (`bhikkhave, tīhi dhammehi samannāgato bālo veditabbo`) have no row; items 1 and 3 repeat their closing sentence in full. | Add rows or a note | 7 |
| 15.2 | `15:9`, `15:95` vs `15:166`, `15:253-255`; `15:249` | bold source paragraph in items 1–2, plain in 3–4; `(paragraph N)` note missing on item 4 | Layout differs between the four items of the assignment. | One layout | 7 |

#### Tags

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| 13.7 | `13:88` | `vinassantu \| verb.pass \| imp.3rd.pl \| may they be destroyed` | `vinassati` is an active group-3 verb (DPD: `pr`), as the row's own root `3 ya` says. | `verb`; "may they perish" | 9 |
| 13.8 | `13:283-284` vs `15:373-374`, `10:535` | `nirujjhamānā \| prp. pass`, `nirujjhati \| verb. pass \| is ceased` vs `prp`, `verb \| ceases` | DPD: `nirujjhati` `pr`, "ceases". Passive in class 13 only; "is ceased" is not English. | `verb`; "ceases" | 8 |
| 13.9 | `13:320` | `saṃvijjamānā \| prp. pass` | DPD: `saṃvijjati` `pr` "exists". | `prp` | 7 |
| 13.10 | `13:563`, `13:570` | `jayaṃ \| noun \| nt.nom.sg \| victory`; "Victory generates ill-will" | DPD does list a neuter `jaya`, so the tag is possible. The commentary on Dhp 201 reads it as the prp (`jayanto`), "the victor", which pairs with `jito` "the conquered one" in the next line. | `prp \| masc.nom.sg`; "The victor breeds enmity" | 6 |
| 13.11 | `13:351` vs `13:343` | `dissanti \| verb \| pr.pass.3rd.pl` vs `verb.pass \| pr.3rd.pl` | Same word, same sentence. | `verb.pass \| pr.3rd.pl` | 9 |
| 13.12 | `13:225-226`, `13:231` | `tasmiṃ … vante \| masc.loc.sg (loc abs) \| when vomited`; "after that man has vomited" | The vomited thing is the food (nt); a locative of reference with `assa` ("would that man have a desire for that vomit?"). The translation makes the man the agent. | `nt.loc.sg`; reword | 6 |
| 13.13 | `13:528`, `13:532-533` | `āturānaṃ … dat.pl`; `sallaviddhānaṃ`, `ruppataṃ … gen.pl (gen abs)` | Three words describing the same people get two cases; the "gen abs" has no separate subject. | Same case; drop "(gen abs)" | 5 |
| 13.14 | `13:167` vs `13:35` | `kiṃ \| pron \| nt.nom.sg \| why` | Adverbial "why" is not nominative; the same phrase is `ind` at `13:35`. | `ind \| interr` | 5 |
| 13.15 | `13:401-404` | `uddhaṃ`, `adho`, `tiriyaṃ \| ind \| prep` | Free adverbs here. | `adv` | 4 |
| 15.3 | `15:192`, `15:230` | `katamehi`, `imehi \| pron \| masc.instr.pl` | They qualify `aṅgehi`, tagged nt (`15:172-174`, `15:234`). Copied from item 2, where the referent `dhammehi` is masc. | `nt.instr.pl` | 8 |
| 15.4 | `15:299`, `15:318` | `yathābhūtaṃ \| adj \| masc.acc.sg` | DPD: `ind`; adverbial gloss; `ind \| adv` at `3:63`. | `ind \| adv` | 7 |
| 15.5 | `15:358` vs `15:424` | `n'ādhiṭṭhāti \| pr.3rd.sg` | Contains the negative but lacks `+neg`. | Add | 6 |
| 15.6 | `15:218` | `metta- \| adj \| masc (in comp)` | A gender on an adjective stem whose head (`cittena`) is nt. | `in comp` | 6 |

#### Glosses and translations

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| 13.16 | `13:633` | "[are] neither not here, nor in another world" | Double negative reverses the sense. | "neither here, nor in another world" | 9 |
| 13.17 | `13:286` | "for what [is] pleasant and enticing in the world there, this craving, …is ceasing, is ceased" | `yaṃ` is nominative, no "for"; adjective order swapped against the table; see 13.8. | "Whatever in the world is enticing and pleasant: here this craving, being abandoned, is abandoned; here, ceasing, it ceases." | 7 |
| 13.18 | `13:475` | "(a helper) should come up with that robe cloth" | In NP 10 the subject of `abhinipphādeyya` is the monk who stands silently; the translation invents another subject. | "…he should get that robe cloth produced" | 6 |
| 13.19 | `13:148` vs `13:156`; `13:151` vs `13:161` | "he is released" / "he is completely freed" | Same `parimuccati` in one sentence. | One rendering | 7 |
| 13.20 | `13:29` vs `13:25`; `13:19` vs `13:12` | "with the entire sole of [his] foot"; "in a balanced manner" vs "evenly" | Plural in the Pāli and the gloss; `samaṃ` rendered two ways. | "soles of [his] feet"; "evenly" | 6 |
| 13.21 | `13:223`, `13:321`, `13:229` | `tassa … for this`; `lokasmiṃ … the world`; `assā'ti … would he` | "that"; locative without "in"; fragment with no end-quote note. | Fix | 6 |
| 13.22 | `13:516`, `13:427` | "He [is one] who makes subside evil deeds …; because of the subsiding completely"; "seen or unseen … far away or near" | `ca` dropped and `sabbaso` moved to the second clause; table has `ca`, translation "or". | Reword | 5 |
| 13.23 | `13:129`, `13:131` | "is lead"; "by what is the world lead?" | Past participle is "led". | "led" | 10 |
| 13.24 | `13:69`, `13:300`, `13:329`, `13:505`, `13:507`, `13:516`, `13:535` | "advises, admonish"; "that; that"; "who lies" (pl. row); "make subside"; "miniscule"; "; What indeed" | Typos and agreement. | "admonishes"; "that"; "who lie"; "makes subside"; "minuscule"; lower-case | 8 |
| 15.7 | `15:147`, `15:153` | "when another person is pointing out a fault" | `accayaṃ deseti` = "confesses a transgression"; "pointing out" reads as criticism of the fool. | "when another is confessing a fault" | 7 |
| 15.8 | `15:362` | "does not grasp, does not get involved, with engagement …" | Verb order reversed against the Pāli and the table (`15:355`, `15:357`); stray comma. | "does not get involved with, does not grasp, that engagement…" | 7 |
| 15.9 | `15:65` | `gacchati, … he gets; lit. goes` | The subject is neuter "what has been eaten…". | "it goes (to)" | 7 |
| 15.10 | `15:265`, `15:272` vs `15:397` | `kittāvatā … in what way` | The correlative `ettāvatā` is "to this extent". | "to what extent" | 6 |
| 15.11 | `15:309`, `15:328` | "Certainly, for one seeing …" | Vocative `kaccāna` omitted twice; translated at `15:341`, `15:403`. | Add "Kaccāna" | 6 |
| 15.12 | `15:187` vs `15:247`; `15:174` vs `15:234` | "five factors" vs "these five qualities" | `aṅgehi` rendered two ways in the opening and closing sentence. | One | 6 |
| 15.13 | `15:137`, `15:355`, `15:357` | `redress, fix, make amends`; `engage in`; `grasp` | Bare verbs for pr.3rd.sg (other rows inflect). | "redresses…" | 7 |
| 15.14 | `15:43`, `15:72`, `15:201`, `15:442`, `15:290`, `15:272` | trailing comma; trailing full stops in gloss cells; `Thus- Gone`; `duality–on`; `"right view?"` | Punctuation. | Fix | 8 |

### Class 14

Quotations in this class were compared with the local SuttaCentral Mahāsaṅgīti text (`dpd-db/resources/sc-data`).

#### Sentence and table

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| 14.1 | `14:453`, `14:458-459` | `āhāre paṭikūlasaññāya paricitena`; rows `paṭikūlasaññāya \| fem.instr.sg`, `paricitena` | AN7.49 has one compound, `paṭikūlasaññāparicitena`; the key splits it and creates an inflected `paṭikūlasaññāya`. Not marked `(simpl)`. | Restore the compound; rows `paṭikūlasaññā-` + `paricitena` | 8 |
| 14.2 | `14:302`, `14:315-316`; `14:527`; `14:633` | `sampajānamusāvādo assa hoti`; `evaṃ assa`; `rāgaṃ ca dosaṃ ca, avijjaṃ ca` | The sources have `-vādassa`, `evamassa`, `rāgañca dosañca avijjañca`. Sandhi is resolved silently here, while the same file writes `kathañ'ca` (`14:170`), `evañ'ca` (`14:244`). | One convention | 6 |
| 14.3 | `14:125` vs `14:129`; `14:20` vs `14:30` | `tasmātiha` / `tasmā't'iha`; `etad'avoca` / `etadavoca` | Sentence and table differ. | Match | 5 |
| 14.4 | `14:527`, `14:537` | `pabbājentī"ti` | Double quote as the quote mark inside a word; elsewhere an apostrophe (`paññāpessatī'ti`, `14:342`). | `pabbājentī'ti` | 8 |
| 14.5 | `14:91`, `14:248`, `14:262` | `ca-`, `evaṃ-`, `cattāro-` | Trailing hyphen on sandhi-split words that are not compound members. | Drop | 6 |
| 14.6 | `14:787`, `14:802` | `acchejji` | The linked text (MN2) reads `acchecchi`; DPD lists `acchejji` as a variant. | Leave or note | 3 |

#### Tags

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| 14.7 | `14:807` | `mān'ābhisamayā \| noun \| masc.instr.sg \| by means of a complete comprehension of conceit` | `-ā` on a masculine a-stem is ablative (so `amanasikārā \| masc.abl.sg` at `14:612`). | `masc.abl.sg`; "through / because of…" | 8 |
| 14.8 | `14:415`, `14:425` | `abhiññā \| adj \| masc.nom.pl \| with direct knowledge` | Tagged as an adjective of `dhammā`, but glossed and translated adverbially. DPD `abhiññā 3` is a gerund "directly knowing". | `verb \| abs` | 7 |
| 14.9 | `14:166` vs `14:163` | `akāsi \| aor.2nd.sg`; subject `āyasmā \| masc.nom.sg` | A nominative subject takes the 3rd person (polite address). | `aor.3rd.sg` | 7 |
| 14.10 | `14:62` | `tayo \| adj \| masc.acc.pl` | Every other numeral is `card`. | `card` | 8 |
| 14.11 | `14:328` | `vassānaṃ \| noun \| masc.gen.pl \| of years` | "Year" is neuter (DPD `vassa 1.3`); masc is "rain". | `nt.gen.pl` | 6 |
| 14.12 | `14:348`, `14:361` | `āvuso \| ind \| voc.sg \| friend` | In MN18 a group of monks is addressed. | "friends" | 6 |
| 14.13 | `14:296`, `14:537` vs `14:534`, `14:338` | `siñcāpeyya \| verb \| opt.caus.3rd.sg`; `pabbājentī"ti \| verb \| pr.caus.3rd.pl` | "caus" inside Grammar; the same word three rows earlier is `verb. caus \| pr.3rd.pl`. | `verb.caus` | 9 |
| 14.14 | `14:835`, `14:837`, `14:691` | `vuṭṭhāpiyamānaṃ`, `saṃvesiyamānaṃ \| prp`; `ārādhayiṃsu \| verb` | Causative passives / a causative (per their own Root cells) without the label that `14:267`, `14:370`, `14:804` carry. | Add label | 7 |
| 14.15 | `14:218` | `adhicittam- \| noun \| nt` | An accusative (`adhicittaṃ + anuyutta`), not a bare stem. | `nt.acc.sg` | 5 |
| 14.16 | `14:27` | `uttaraṃ \| … \| Uttara; lit. higher \| √tar･1 a (cross)` | The name is the comparative `ud + tara` (DPD `uttara 2`, no root); `√tar` belongs to `uttara 1` "crossing over". | Empty root | 7 |
| 14.17 | `14:61` | `kumārassa \| √kumār×8 \*e (play)` | DPD's `kumāra` has no root. | Empty root | 6 |

#### Glosses and translations

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| 14.18 | `14:478` | "[his] mind withdraws from, bends back from, rolls back from craving for tastes," | `na sampasāriyati` (rows `14:475-476`) is not translated. | Add "[and] is not drawn towards it" | 9 |
| 14.19 | `14:585` | `asevitabbe … should not be associated with; should be followed` | Negation missing in the second gloss. | "should not be followed" | 9 |
| 14.20 | `14:42`, `14:51`, `14:441` | "You should develop wholesome qualities." / "It is possible to develop…" / "As long as monks will not make known…" | `bhikkhave` omitted in all three; `ca` dropped in the last. | Add "monks" | 8 |
| 14.21 | `14:32` | "And then, having had summoned a young brahmin Uttara, Payasi, the young nobleman, said this." | Ungrammatical; diacritics. | "And then Pāyāsi the young nobleman, having had the young brahmin Uttara summoned, said this." | 8 |
| 14.22 | `14:18` | "He causes this very body to overflow, to flow around, to fill up all around, to suffuse with the joy and happiness born from separation…" | `parippharati` is not causative (`14:16`); "body … to suffuse" reverses the sense; "happiness / separation" against the glosses "ease", "solitude". | "He drenches, soaks, fills and suffuses this very body with the joy and ease born of solitude." | 6 |
| 14.23 | `14:451` | "they will practise accepting the training rules as they had been formulated." | The third condition of the `yāvakīvaṃ` clause reads as a main clause; wrong tense. | "[and] will proceed having undertaken the training rules as formulated," | 6 |
| 14.24 | `14:156` vs `14:154`; `14:631` | "the underlying tendency"; "and even taints that have arisen" | `anusayānaṃ` is plural; `c'eva … ca` is "both … and". | Fix | 6 |
| 14.25 | `14:603` vs `14:590`; `14:667` vs `14:671` | `dhamme` as "things" and "practices" in one sentence; "words and letters" vs "words and phrases" | Gloss and translation differ. | Align | 7 |
| 14.26 | `14:496`, `14:494` | `pan'idaṃ \| ind+pron \| moreover`; `taṃ … this` | `idaṃ` lost in the gloss; `taṃ` glossed "this" to compensate. | "moreover this"; "that" | 6 |
| 14.27 | `14:98`, `14:372`, `14:375`, `14:378`, `14:310`, `14:356`, `14:296`, `14:795`, `14:728` | "investigate; examine"; "being cause to see together"; singular glosses on 3rd pl verbs; "causing to be heard along"; "lit. causes to know" (future); "should cause pour"; "who restrained"; "with no patron; owner" | Bare verbs, typos, voice and tense of the literal notes. | Fix | 7 |
| 14.28 | `14:276-280`, `14:623-658`, `14:795`; `14:369-376` vs `14:675`; `14:298` vs `14:573`; `14:551-564` | `āsava`: impurities / effluents / taints; "scripture(s)" vs "discourse(s)"; `pācittiyaṃ`: "a case" vs "an offence"; four wordings for the two robes | Same word, several renderings. | Align | 6 |
| 14.29 | `14:25`, `14:59-66`, `14:777`, `14:658`, `14:179`, `14:174`, `14:671` | `Payasi`, `Bandhuma`, `Vipassi`; `"monk, this is…`; unclosed `"Having abandoned…`; `understood.` in a cell; `how!?`; "not … nor" | Diacritics, capitals, punctuation. | Fix | 7 |
| 14.30 | `14:286` vs `14:306-308`, `14:507-509`; `14:24`, `14:57` vs `14:686-687`; `14:91-92`, `14:374`, `14:622` | `yo pana bhikkhu`, `atha kho`, `c'eva` | Each analysed two or three ways inside one file (see E12). | One | 8 |
