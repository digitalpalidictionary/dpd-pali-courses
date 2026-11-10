# IPC audit — `docs/ipc/` (PARTIAL DRAFT)

Date: 2026-11-11 (work started 2026-11-10)
Scope: 136 Markdown files under `docs/ipc/` (index + classes 16–28, 8 437 lines).
No file in `docs/` was modified.

**Status: INCOMPLETE.** Only two parts are done: the mechanical checks (section M) and the line-by-line read of class 28 (sections A–H, class 28 only). Classes 16–27 and the root `docs/ipc/index.md` have **not** been read line by line. Five of six reader subagents died on the usage limit and their partial output was lost. See `ipc-audit-handoff.md` for what remains.

Paths are relative to `docs/ipc/`. Pāli forms were judged from the reader's own knowledge, not DPD; anything with confidence below 8 needs a DPD lookup before it is changed. Class 28 findings are the reader's and have **not** been grep-verified against the files by me.

---

## M. Mechanical checks (run centrally, whole of `docs/ipc/`)

Script: `ipc-audit-mech.py` (same folder). Read-only.

| Check | Result |
| --- | --- |
| Sutta links (`uv run python scripts/check_sutta_links.py docs/ipc`) | 37 links / 23 pages, all pass |
| Local links and `#anchors` | No broken link, no unresolved anchor |
| Other external links | 2 found. `class_28/3_home_work.md:17` `https://sasanarakkha.github.io/study-tools/pali-class/pali-class-adv.html` returns **404** (dead). `class_28/3_home_work.md:21` Google feedback form returns 200 |
| Index titles vs page H1 | Every page is listed in an index. Link-text vs H1 mismatches in 24 places, all one pattern: the H1 carries italics or misplaced `*` that the index link text does not (list below) |
| Table column counts | 2 hits, both `class_18/11_ex.md:11` and `:24` (`\| \|` one-cell row closing a table; the table is 4 columns) |
| Footnote refs vs definitions | Consistent in all files; ids 1–23 present |
| Heading jumps, multiple H1, headings without a space, odd `**` count, tabs, zero-width characters, non-NFC | None reported |
| File without final newline | `class_20/5_ex.md` |

### M1. Index link text vs H1 (all 24)

| Index line | Link text | Page H1 |
| --- | --- | --- |
| `index.md:5`, `class_16/index.md:4` | `Vowel Sandhi (sara-sandhi)` | `Vowel Sandhi *(sara-sandhi)*` |
| `index.md:19`, `class_17/index.md:4` | `Consonant Sandhi (vyañjana-sandhi)` | `Consonant Sandhi (*vyañjana-sandhi)*` (italic closes after the bracket: misplaced `*`) |
| `index.md:51`, `class_19/index.md:3` | `Compounds (samāsa)` | `Compounds (*samāsa)*` (same misplaced `*`) |
| `index.md:69-74`, `class_21/index.md:6-11` | `Present Tense (vattamānā)`, `Imperative (pañcamī)`, `Optative (sattamī)`, `Perfect Past Tense (parokkhā)`, `Imperfect Past Tense (hiyyattanī)`, `Aorist (ajjatanī)` | same with `*term*` italics |
| `index.md:78-79`, `class_22/index.md:3-4` | `Future Tense (bhavissantī)`, `Conditional Tense (kālātipatti)` | same with `*term*` italics |
| `index.md:135`, `class_28/index.md:4` | `Less Frequent kita` | `Less Frequent *kita*` |

The two misplaced-`*` H1s (`class_17/2_cons.md`, `class_19/1_comp.md`) are real defects; the rest are only italic markup that the index drops.

### M2. Raw HTML in sources

Project rule: no raw HTML in `.md` sources. Only `<br>` is used (414 occurrences in `docs/bpc`; the count for `docs/ipc` was not taken). `scripts/generate_pdfs.py` has special handling for `<br>` next to tables, so it is a known pipeline convention; flagging it as a rule deviation for the owner to decide. Files with `<br>`:

`class_17/1_alphabet_analys.md`, `class_17/15_nig_8.md`, `class_17/19_home_work.md`, `class_18/10_irreg_masc.md`, `class_20/1_abya.md`, `class_21/4_pres.md`, `5_imp.md`, `6_opt.md`, `7_perf.md`, `8_imperf.md`, `9_aor.md`, `10_sum.md`, `class_22/1_fut.md`, `2_cond.md`, `class_24/5_caus_pass.md`, `6_app.md`, `7_home_work.md`, `class_16/13_home_work.md`, `class_18/12_home_work.md` (home-work tables).

False positives of my regex (backslash-escaped `\<` `\>` arrows in `class_16/12_vowel_ref_table.md:6-14`) are not HTML.

### M3. Convention counts (whole slice)

| Item | Count / finding |
| --- | --- |
| Arrow | `\>` (escaped) 472 times; no `→`, `=>` or `->` |
| Quotes | curly `“` 295; straight `'` 11 and `"` 4. Straight-quote lines: `class_17/5_cons_3.md:51`, `class_19/2_kamm.md:7`, `class_20/2_bahub.md:267`, `class_22/2_cond.md:9`, `class_22/3_root_groups.md:146`, `class_24/5_caus_pass.md:7`, `:39`, `class_25/4_taddh.md:19` (several are apostrophe-as-sandhi-mark inside Pāli, which is deliberate) |
| "Pāli" spelling | `Pāli` 53; `Pāḷi` 1 (`class_18/10_irreg_masc.md:20` footnote 6); `pāḷi` 3 (the `Māgadhabhāsā (pāḷi)` rows in `class_16/13_home_work.md:42`, `class_17/19_home_work.md:16`, `class_18/12_home_work.md:15`); `pāli` 1 (`class_18/8_as_misc.md:21`); `pali` 5 (all in `pari- pali-` or URL) |
| `sam +` vs `saṃ +` | `saṃ +` 23; `sam +` 3 (`class_18/2_as_ya.md:131` `√sam`, `class_18/3_as_ta.md:122` `√sam`, `class_23/20_mixed_pref.md:22` `sam + pati`). The first two are the root √sam and are legitimate; the third is the prefix and is the drift |
| Home-work page title | `# Homeless work` in 13 IPC pages and 26 BPC pages. Looks systematic (also in indexes). Probably a typo for "Homework"; intentional status unknown |
| `pari- pali-` | `class_23/17_pari.md:1`, `class_23/index.md:19`, `index.md:100`: title says `pari- pali-` (two spellings of the same prefix); intentional likely, not confirmed |
| Kaccāyana citation | Style `*Kaccāyana 324.*` (rule number) appears for rules 319, 324–326, 329, 414–422; other pages say `Kaccāyana` in prose only. Not checked for correctness of the numbers |

---

## CLASS 28 — line-by-line read (reader findings, unverified by me)

Files read in full: `class_28/1_kita_1.md` (725), `2_kita_less.md` (530), `3_home_work.md` (21), `index.md` (5). Counts: A 19, B 9, C 6, D 13, E 4, F 9, H 3.

### A. Pāli and grammar content errors

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| `class_28/1_kita_1.md:602` | `abhi √vah \| to carry \| + **\*ana** \| adhiv**ā**h**ana**` | Prefix in column 1 is *abhi*; the result has *adhi*. | `adhi √vah` | 9 |
| `class_28/2_kita_less.md:203` | `k**o**t**i** \| end, point` | Dental *t*; the word is *koṭi* (root √kuṭ in the same row). | `k**o**ṭ**i**` | 9 |
| `class_28/1_kita_1.md:655`, `class_28/2_kita_less.md:13` | `upa √ādā`; `√ādā \| to take, seize` | √ādā is not a root; it is ā + √dā (same defect as BPC audit A20). | `upa ā √dā`; `ā √dā` | 9 |
| `class_28/2_kita_less.md:493` | `√dis \| to see \| **+ tāvī** \| dass**āvī** \| has seen` | *dassāvī* is not formed with *tāvī*; the bolding shows *āvī*, a separate suffix in the list at `1_kita_1.md:32` (`avī āvī`). | Remove from the tāvī table or replace with a real -tāvī form | 8 |
| `class_28/1_kita_1.md:54` | `√saj \| to cling \| **+ ta** \| visa**ta** \| attachment` | √saj + ta gives *-satta*; *visata* is normally vi + √sar ("spread"). Prefix *vi* also missing from column 1. | Check DPD: `vi √saj … visat**ta**` | 7 |
| `class_28/1_kita_1.md:53` | `vi ā √rabh \| to begin \| **+ ta** \| viyārab**bha** \| effort` | √rabh + ta gives *-raddha*; *-rabbha* is the result of + ya. | Check DPD (suffix or form) | 6 |
| `class_28/1_kita_1.md:426` | `√mar \| to die \| **+ aṇa** \| mār**aṇa** \| killing` | Root vowel lengthened, so by the file's own notation this is `\*aṇa` (or causative base *māre*). Sits under `mar**aṇa**` with the same analysis. | Move to `\*aṇa` or show causative base; check DPD | 7 |
| `class_28/1_kita_1.md:489`, `:567`; `class_28/2_kita_less.md:16`, `:18` | `√nhā … nhāp**aka**`; `√ar … app**anā**`; `√dis … dasse**tar**`; `√ghaṭ … ghāte**tar**` | Forms are built on the causative base (*nhāpe*, *appe*, *dasse*, *ghāte*); table shows root + suffix only, so the extra *p* / *e* is unexplained. | Add the causative base or a note | 6 |
| `class_28/1_kita_1.md:512` | `suffix **ī** (Sanskrit -in) is used to form **possessive adjectives**` | "Possessive" describes the taddhita *ī*. Kita *ī* forms agent / habitual-action adjectives (*jīvī*, *apacāyī*). | "agent adjectives", or explain the overlap | 6 |
| `class_28/1_kita_1.md:526`; `class_28/2_kita_less.md:84`, `:85` | `√sukh \| to please \| **+ ī** \| sukh**ī**`; `√rāj … raj**ja**`; `√sīl … dussīl**ya**` | Usually analysed as taddhita (sukha + ī, rāja + ṇya, dussīla + ṇya), listed here as kita. | Check DPD; leave if DPD treats them as kita | 5 |
| `class_28/1_kita_1.md:528` | `√dus \| to be corrupt \| **+ ī** \| dūsī \| corrupter` | Root vowel lengthened (u > ū), which the file marks elsewhere with `\*` (compare `:723` `**+ \*aka** \| d**ū**s**aka**`). | `+ \*ī`, `d**ū**s**ī**`; check DPD | 6 |
| `class_28/1_kita_1.md:270` | `√dhā \| to support \| **+ ita** \| h**ita** \| friend` | *hita* is normally dhā + ta (dh > h, ā > i), not + ita. | Check DPD | 5 |
| `class_28/1_kita_1.md:356` | `√mad \| to be drunk \| **+ na** \| ma**nda** \| fool` | mad + na would not regularly give *manda* (usually √mand). | Check DPD | 5 |
| `class_28/1_kita_1.md:359`, `:373` | `√var \| to cover \| **+ na** \| vaṇ**ṇa**`; `su √var … suvaṇ**ṇa**` | *vaṇṇa* is usually referred to √vaṇṇ. | Check DPD | 4 |
| `class_28/1_kita_1.md:139` | `ā √bil \| to break \| **+ a** \| āvil**a** \| unclear` | Root written with *b*, result with *v*; compare `:125` `√bil … bil**a**`. | Check DPD (√bil vs √vil) | 5 |
| `class_28/1_kita_1.md:201` | `pati √bhaṇ \| to speak \| **+ \*a** \| paṭibh**ā**n**a**` | Root has retroflex *ṇ*, result dental *n*; *paṭibhāna* often referred to paṭi + √bhā. | Check DPD | 5 |
| `class_28/1_kita_1.md:656`, `:663` | `atth**i** \| seeker`; `jhāy**i** \| meditator` | Short -i masculine agent forms; usual forms *atthī*, *jhāyī* (the latter already at `:525` under `+ ī`). | Check DPD; remove `:663` if only a variant of `:525` | 5 |
| `class_28/2_kita_less.md:249` | `√har \| to bring \| **+ \*aṇa** \| āh**ā**r**aṇa** \| bringing` | Usual noun is *āharaṇa* (short a), which would be plain `aṇa`. | Check DPD | 5 |
| `class_28/2_kita_less.md:528`, `:530` | `ara**tī**`, `tuṭ**ṭhī**` | Usual forms *arati*, *tuṭṭhi* (short i, suffix *ti*). Long-ī forms need confirming as headwords. | Check DPD | 5 |

### B. Tables and lists that disagree with each other or themselves

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| `class_28/1_kita_1.md:23-24` | `\| 15 \| **+ \*ana** \| 151 \|` / `\| 16 \| **+ \*ī** \| 157 \|` | Ranking table otherwise descending; 157 > 151. Sections (`\*ana` at `:570`, `\*ī` at `:605`) follow the same wrong order. | Swap rows 15 and 16 (and the sections), or correct a count | 9 |
| `class_28/1_kita_1.md:256-262` | `1066` / `110` / `105` / `20` / `**1300**` | Parts sum to 1301, one more than the total. | Recount | 10 |
| `class_28/1_kita_1.md:80-85`, `:154-159`, `:231-236`, `:298-303`, `:407-412`, `:643-649` | totals `**1684**`, `**1442**`, `**1395**`, `**1162**`, `265`, `139` | Parts sum to 1660, 1438, 1393, 1161, 264, 136. If minor categories were dropped no table says so; the other eight tables add up exactly. | Add an "other" row or recount | 9 |
| `class_28/1_kita_1.md:331-333`, `:553-555`, `:695-697` | `## māna`, `## anā`, `## \*aka` | Every other top-18 section has description + count table + examples. *māna* has no count table or examples; *anā* has no description or count table; *\*aka* has no description. | Complete to the common pattern | 8 |
| `class_28/1_kita_1.md:566`, `:568` | `pa √atth \| to wish \| … patth**anā** \| aspiration` / `pa √atth \| to wish for \| … patth**anā** \| intention, wish` | Same word listed twice in one table. | Merge | 9 |
| `class_28/1_kita_1.md:672-673` | `√kas \| to drag \| **+ i** \| kas**i** \| farming` / `√kas \| to plough \| **+ i** \| kas**i** \| farming` | Duplicate row. `:535` gives the root once as "to drag, plough". | Merge | 9 |
| `class_28/1_kita_1.md:181`, `:358`, `:397`, `:590`; `class_28/2_kita_less.md` throughout (e.g. `:20`, `:35`, `:37`, `:70`, `:73`, `:126`, `:127`, `:130`, `:143`, `:162`, `:179`, `:186`, `:200`, `:227`, `:249`, `:273`, `:339`, `:351`, `:392`, `:407`, `:439`, `:492`, `:495`, `:496`, `:516`, `:528`) | e.g. `√sī \| to sleep \| **+ \*a** \| ās**aya**`; `√khā \| to tell \| **+ tar** \| akkhā**tar**` | `1_kita_1.md` normally writes prefixes before the root (`ā √jīv`, `pati ud √pad`, `na ni √vis`). These rows, and every prefixed word in `2_kita_less.md`, omit them, so root + suffix does not give the stated word. | Add prefixes in column 1 | 8 |
| `class_28/1_kita_1.md:229` vs `:231-236` | `a tiny group of **passive present participles**, **nouns** and **adjectives**` | "Passive present participles" has no row in the count table and no example. | Add or drop | 6 |
| `class_28/2_kita_less.md:367`, `:371` | `**+ ala neuter nouns and adjectives**` … `kul**ala** \| eagle; hawk` | *kulala* is masculine; no neuter noun in the table. `:433` has `√kur … kurara \| eagle` as masculine. | "masculine nouns and adjectives" | 7 |

### C. Translation and gloss problems

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| `class_28/1_kita_1.md:587` vs `:598`; `class_28/2_kita_less.md:496` | `√i \| to come`; `parā √i \| to go`; `√i \| to come` | Same root glossed two ways. | "to go" throughout | 7 |
| `class_28/1_kita_1.md:73` | `suga**ta** \| going well` | *gata* is past: "gone well, well-gone". | "well-gone" | 7 |
| `class_28/1_kita_1.md:358` | `√sad \| to sink \| **+ na** \| pasan**na** \| believer` | "to sink" does not lead to "believer"; pa + √sad is "to be clear, pleased". | Adjust root gloss (and add `pa`) | 6 |
| `class_28/1_kita_1.md:445` | `āvar**aṇa** \| obstructed, blocked` | Adjective is active: "obstructing". `:428` glosses the noun as "obstacle". | "obstructing, blocking"; check DPD | 6 |
| `class_28/1_kita_1.md:657-661` | `ni √dhā \| to place`, `saṃ √dhā \| to place`, `pa ni √dhā \| to support`, `upa √dhā \| to support` | Same root, two glosses in adjacent rows. | One gloss | 7 |
| `class_28/2_kita_less.md:406` | `m**e**tt**ā** \| lit. friendliness` | Only a "lit." gloss, no primary meaning (compare `fire; lit. purifier`). | "loving-kindness; lit. friendliness" | 7 |

### D. English typos and grammar

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| `class_28/1_kita_1.md:435` | `one who stealing` | Grammar. | "one who steals" | 10 |
| `class_28/1_kita_1.md:641` | `is used to forming` | Grammar. | "is used to form" | 10 |
| `class_28/1_kita_1.md:180`, `:200` | `to breath` | Verb is "breathe". | "to breathe" | 10 |
| `class_28/1_kita_1.md:489` | `to bath` … `bathman` | Verb is "bathe"; "bathman" is not usual English. | "to bathe"; "bath attendant" | 8 |
| `class_28/1_kita_1.md:422`, `:423` | `to do make` | Missing comma. | "to do, make" | 9 |
| `class_28/1_kita_1.md:97`; `class_28/2_kita_less.md:83` | `√kalah \| argue`; `be skilful, precise` | Only root glosses without "to". | "to argue"; "to be skilful, precise" | 9 |
| `class_28/1_kita_1.md:333` | `as we saw on the last class` | Preposition. Also "last week" at `:36`, `:229`, `:347` and `2_kita_less.md:289`. | "in the last class" (one phrase throughout) | 8 |
| `class_28/1_kita_1.md:229` | `last week. it also forms` | Lower-case sentence start. | "It also forms" | 10 |
| `class_28/1_kita_1.md:28` | `Here are most of *kita* suffixes in DPD` | Missing article and end punctuation. | "Here are most of the *kita* suffixes in DPD:" | 8 |
| `class_28/1_kita_1.md:347` | `last week, can you think of an example?` | Comma splice. | "last week. Can you …" | 7 |
| `class_28/1_kita_1.md:3` | `nouns, adjectives, substantives and participles` | "nouns" and "substantives" are the same thing. | Drop one | 6 |
| `class_28/3_home_work.md:5` | `kita kicca and taddhita suffixes` | Missing comma; terms italic elsewhere. | "*kita*, *kicca* and *taddhita* suffixes" | 7 |
| `class_28/3_home_work.md:21` | `viewform), your corrections` | Comma splice. | Full stop | 7 |

### E. Markdown defects that affect rendering

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| `class_28/1_kita_1.md:596` | `sabh**o**jan**a**` | Bold marks only the final *a*; suffix is *ana* (compare `:597` `ac**e**t**ana**`). | `sabh**o**j**ana**` | 9 |
| `class_28/1_kita_1.md:337` | `a large group **of past participles**` | "of" inside the bold span. | `of **past participles**` | 9 |
| `class_28/1_kita_1.md:527-528`; `class_28/2_kita_less.md:54-56`, `:176-180`, `:186-187`, `:280-281`, `:351-352`, `:358-359`, `:384-385`, `:391-392`, `:433`, `:439`, `:479-480`, `:508-509`, `:515-516` | e.g. `gavesī`, `cakkhu`, `jīvikā`, `vattha`, `hutta`, `p**o**ta`, `m**ū**sikā` | Suffix not bolded in the result column (or only the changed vowel), unlike all other rows. | Bold the suffix | 9 |
| `class_28/1_kita_1.md:412`, `:649`, `:702`; `:611-613` | `\| **total** \| 265 \|`; `\| adj \| 143 \|` | Total figure not bold (bold in other tables); POS labels not bold in the `\*ī` table. | Make uniform | 9 |

No raw HTML, heading-level jumps, footnotes or column-count mismatches in class 28. The `\*u` table at `2_kita_less.md:417-420` has 6 columns but is internally consistent (see F).

### F. Convention drift

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| `class_28/1_kita_1.md:596-603`; `class_28/2_kita_less.md:419-420`, `:452-454`, `:466-467`, `:508-509`, `:528-530` | `+ **\*ana**`, `+ \*u`, `+ yā`, `+ \***tta**`, `+ \*ikā`, `+ **tī**` | Suffix cell elsewhere is `**+ suffix**` (plus sign inside the bold). Four variants here. | `**+ \*ana**` etc. | 9 |
| `class_28/1_kita_1.md:607` | `suffix \***ī**` | Asterisk outside the bold; elsewhere `**\*a**`, `**\*ana**`. | `**\*ī**` | 9 |
| `class_28/2_kita_less.md:400`, `:448`, `:475`, `:524` | `**\*ā feminine nouns**`, `**yā feminine nouns**`, `**\*ta masc nouns**`, `**tī feminine nouns**` | Captions lack the leading `+ ` used everywhere else; `masc` abbreviated only here. | `**+ \*ā feminine nouns**` etc.; "masculine" | 9 |
| `class_28/2_kita_less.md:417-420` | `\| √dar \| to split \| + \*u \| d**ā**r**u** \| m \| wood, timber \|` | Only table with a sixth (POS) column; uses `m` where the slice's abbreviation is `masc`. | Split into two 5-column tables or use `masc` | 8 |
| `class_28/1_kita_1.md:61`, `:427` vs `:74`, `:220`, `:692` | `nī √as`, `nī √sar` vs `nir √chā`, `nir √bhuj`, `nir upa √dhā` | Same prefix written `nī` and `nir`. | One form (check which DPD uses) | 7 |
| `class_28/1_kita_1.md:422` vs `:661` | `vyākar**aṇa**` vs `byādh**i**` | `vi ā` gives *vy-* in one row, *by-* in the other. | One spelling | 7 |
| `class_28/1_kita_1.md` vs `class_28/2_kita_less.md` | — | File 1 gives each suffix a description sentence and POS breakdown; file 2 gives only `total`, with a description only for `ikā`, `āna`, `tāvī`. File 2 has no intro paragraph; the tāvī table (`:490`) has no bold caption. | Accept as design or level up | 6 |
| `class_28/1_kita_1.md:36`, `:78`, `:152`, … (every section opener) | `suffix **ta** is the most common kita suffix.` | Openers start lower-case; about half end without a full stop (`:152`, `:296`, `:379`, `:405`, `:449`, `:472`, `:512`, `:572`, `:607`, `:641`); `kita` not italic at `:36` but italic at `:5`, `:28`. | Uniform | 8 |
| `class_28/1_kita_1.md:249-250`, `:268`; `class_28/2_kita_less.md:177` | `great, large, big` / `big; huge; large`; `fly (smearer)` vs `heaven; lit. satisfied` | Gloss separators mix `,` and `;`; literal meaning given both as `(…)` and `; lit. …`. | Uniform | 6 |

### H. Data to re-verify

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| `class_28/1_kita_1.md:3-5` | `more than 150 suffixes`, `more than 14000`, `**first 18** account for **83%**` | Top-18 counts sum to 12 280, which is 83% of about 14 800, consistent with "more than 14000". All DPD-derived counts are a snapshot and could not be recomputed. | Recompute from current DPD DB | 6 |
| `class_28/3_home_work.md:13` | `Duroiselle \| Primary Derivatives (574-578)` | Paragraph range not confirmed against Duroiselle (reader recalls kita section starting at §575). | Verify | 5 |
| `class_28/1_kita_1.md:30-32` | bold list `ta a \*a … tī` | Bold marks the 45 suffixes covered in the two files (18 + 27); matches headings and order. Meaning of bold and of `\*` is not stated anywhere in this class. | Add one line of explanation or point to where `\*` is defined | 7 |

### Conventions observed in class 28

- No arrows used. Everything is 5-column tables with an empty header row: `| root | root gloss | **+ suffix** | result | gloss |`.
- Roots `√xxx`; prefixes space-separated before the root with no `+` (`pati ud √pad`, `na ni √vis`, `saṃ √tan`); `saṃ` always with niggahīta.
- Strengthening suffixes are written with an escaped asterisk (`\*a`, `\*ana`, `\*ī`), not defined in this class.
- Result words: suffix and any changed root vowel bold (`bh**e**d**a**`, `bud**dha**`).
- Root glosses "to + verb", lower-case, comma-separated.
- Count-table POS abbreviations: `pp`, `prp`, `adj`, `masc`, `nt`, `fem`, `total` (bold).
- Sub-table captions are bold paragraphs, not headings; section headings are `## <suffix>`.
- Section openers lower-case: `suffix **x** is used to form …`.
- No Kaccāyana citations, sutta links or footnotes in class 28.
- Home-work page: title `# Homeless work`; numbered list `1.  ` (two spaces); extra reading as 2-column headerless table.
- Back-references: both "last week" and "on the last class".
- Class index is a plain bullet list; link text drops the italics of the page title.

---

## NOT AUDITED (no findings exist for these)

`index.md`; `class_16/*`; `class_17/*`; `class_18/*`; `class_19/*`; `class_20/*`; `class_21/*`; `class_22/*`; `class_23/*`; `class_24/*`; `class_25/*`; `class_26/*`; `class_27/*`. Absence of findings above means "not read", not "clean".
