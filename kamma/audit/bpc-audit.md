# BPC audit — `docs/bpc/`

Date: 2026-11-13
Scope: all Markdown files under `docs/bpc/` (index + classes 1–14; 106 files, 5 289 lines, 1 838 table rows, as counted by `mech_checks.py`).
No file in `docs/` was modified. This is a findings list only.

This file replaces the audit of 2026-11-10, which was written before `kamma/audit/audit-guide.md` existed. It is the result of two passes over every slice: a fresh read by the guide's full checklist, and a re-check of every row of the old audit. A row that comes from the old audit ends its `Problem` with `(old <id>)`.

Related to #6 Course enhancement with AI

## Method and limits

| Check | How | Result |
| --- | --- | --- |
| Footnote numbering test | `grep -rhoE '^\[\^[0-9]+\]:' docs/bpc \| sort \| uniq -d` | Empty: ids are unique across the folder and rise across classes, so the footnote check ran folder-wide |
| Mechanical checks | `uv run python kamma/audit/scripts/mech_checks.py docs/bpc --folder-footnotes --links-out kamma/audit/scratch/bpc/links.txt` | Exit 0. 1 table column mismatch, 11 index/H1 differences, footnotes 28 refs / 28 defs, 10 stray-character and heading lines (Mechanical detail, M1–M4) |
| Non-sutta links | `curl -s -o /dev/null -w '%{http_code}' -L --max-time 15 <url>` for each of the 12 unique links not on `s.dhamma.gift` | 6 return 200, 2 return 404, 1 is a local server (000), 3 Google Docs/Forms links skipped (M5) |
| Sutta links | `uv run python scripts/check_sutta_links.py docs/bpc` | 82 links / 56 pages, all pass (exit 0) |
| Full read of every file | Line by line, by the main session, 10 class slices and 1 cross-file slice; the guide's "What to look for" list and categories A–I applied to each | Done; every slice file ends with its checklist note |
| Re-check of the old audit | Every row of the old D–H sections and the raw-HTML note re-checked against the source; the owner-reviewed sections A, B, C and the gloss list carried over | 83 old D–H ids all accounted for; 71 owner rows carried over (see "Owner decisions carried over") |
| DPD lookups | `uv run python kamma/audit/scripts/dpd_lookup.py <lemma> …`, run once over the 78 lemmas the reader had listed as suspicious | 54 rows waited for it: 34 dropped because DPD agrees with the text, 20 finalised against the DPD entry. 4 lemmas are not DPD headwords: `akkhobhiṇī`, `bhayati`, `cattālīsa`, `sappī` |
| Excerpt check | `uv run python kamma/audit/scripts/verify_rows.py docs/bpc …` on every slice file and on this file: each backtick excerpt in `Current` searched in the cited file within 2 lines of the cited line | 421 excerpts pass, 0 fail (rows with no source file found: 0) |
| Merge | `uv run python kamma/audit/scripts/merge_audit.py kamma/audit/scratch/bpc/merge.toml` | This file |

Fresh-pass checklist (items the old audit had not applied): root spelling against DPD roots; `pati`/`paṭi` in analysis vs result; examples that do not illustrate their own heading; summary tables against the lesson tables; paradigm cells; quoted verses (spelling, label vs link anchor); number statements against a count of the items; one word glossed in different ways; bold cutting a cluster or spanning `<br>`, quotes or full stops; `(*term)*`; list numbering; heading drift; hard wraps; lower-case sentence starts; the new mechanical items (footnotes, NBSP, zero-width and non-NFC characters, heading levels, convention counts); category I.

Not verified:

- The DPD lookups were deferred to one run, on the owner's instruction: the reader listed what looked suspicious, and only those 78 lemmas were looked up. A form that did not look suspicious rests on the reader's knowledge of the language. Each row carries a confidence score (1–10). Below 8, check DPD or the text before changing anything.
- `dpd_lookup.py` prints headwords, not inflection tables. Rows that say `verify against the DPD inflection table` (classes 5–10) could not be settled, and rows that say `DPD lookup` name a form that was not in the lookup run.
- The number after a root in the lookup output is DPD's homonym number, not the root group; root groups were judged from the conjugational sign.
- The two long word lists in `class_3/5_roots.md` (√bandh, line 27; √bhū, line 31) were not checked word by word. Three forms that looked odd (`bhāvetva`, `bhāvaniya`, `saṃbandho`) are DPD headwords.
- Canonical wording was not compared with a text edition. Rows that depend on a reading say `verify`.
- The link checker proves that the page and anchor exist, not that the sentence is in that sutta. The 3 Google links were not opened.
- The owner's decisions (the rows described under "Owner decisions carried over") were carried over word for word and not judged again.
- Rendered output (site, PDF, DOCX) was not built.

Paths below are relative to `docs/bpc/`. In `Current`, `\|` is a table pipe in the source.

## Summary

| Category | idx–2 | 3 | 4 | 5–6 | 7–8 | 9 | 10 | 11 | 12–13 | 14 | cross | Total | Conf. ≥ 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A. Pāli and grammar content errors | 3 | 8 | 3 | 4 | 8 | 3 | 6 | 12 | 4 | 4 | 0 | 55 | 32 |
| B. Tables, paradigms and lists that disagree with each other or themselves | 3 | 4 | 3 | 5 | 3 | 6 | 7 | 8 | 5 | 3 | 0 | 47 | 22 |
| C. Translation and gloss problems | 4 | 3 | 1 | 8 | 2 | 2 | 5 | 3 | 5 | 1 | 1 | 35 | 17 |
| D. English typos and grammar | 14 | 9 | 7 | 14 | 11 | 10 | 4 | 4 | 11 | 5 | 1 | 90 | 73 |
| E. Markdown defects that affect rendering | 8 | 6 | 6 | 5 | 3 | 1 | 12 | 5 | 9 | 6 | 2 | 63 | 50 |
| F. Convention drift | 3 | 3 | 3 | 4 | 6 | 3 | 5 | 4 | 4 | 4 | 19 | 58 | 38 |
| G. Links | 3 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 5 |
| H. Data to re-verify (forms, references, counts) | 1 | 0 | 0 | 2 | 3 | 1 | 0 | 0 | 2 | 2 | 0 | 11 | 1 |
| I. Further details on the material under review | 4 | 2 | 1 | 3 | 1 | 1 | 1 | 2 | 2 | 2 | 0 | 19 | 0 |
| **Total** | **43** | **35** | **25** | **46** | **37** | **27** | **40** | **38** | **42** | **27** | **23** | **383** | **238** |

A row often covers several locations, so the number of places to edit is higher than the row count.

Overall confidence: 9/10 that the quoted text is where the row says (scripted). 8/10 for categories D, E, F and G (visible in the source). 7/10 for A, B, C and H as a group: DPD was consulted for the forms that looked doubtful, but no text edition was. Use the per-row score.

## Owner decisions carried over

Sections A, B, C and the gloss list of the old audit had been reviewed by the owner. Every row the owner kept is carried over as a decision: its `Suggested` cell starts with the label `Owner` and a colon, followed by the owner's text, word for word. These rows were not judged again.

- 71 rows carry that label. They stand for 63 kept ids and 5 gloss items. Old B8 has three rows (classes 5, 8 and 11) and old B2 has two (classes 4 and 13), which gives the 3 extra rows.
- Kept ids, section A (36): A1, A4–A11, A16, A17, A21–A41, A44–A47.
- Kept ids, section B (14): B1–B3, B5–B10, B13–B17.
- Kept ids, section C (13): C1–C4, C6–C14.
- Gloss items, now C rows (5): *ottappa*, √sad, √dhā, *ka*, the monkey simile.

## Rejected by the owner

The owner deleted these 15 rows from the old audit. They are not reported, and a fresh finding that repeated one of them was discarded: A2, A3, A12, A13, A14, A15, A18, A19, A20, A42, A43, B4, B11, B12, C5.

## Old rows: reopened, corrected, dropped

- Reopened: none.
- Dropped: none. All 83 ids of the old sections D–H and the raw-HTML note have a row here.
- Corrected while re-checking (same id, different content): H5 (`avadhyai` is a root form, not an unrecognisable one), D15, D16, D19, D21 and F9 (moved to the right line or reworded), H6 (the number list; the forms for 40 still need a DPD lookup).

## Fresh findings dropped after the DPD lookup

34 fresh rows were written as "to confirm" during the read and dropped when DPD agreed with the text. They are listed here so that the same doubts are not raised again:

- Forms that exist in DPD: `uḍḍayati`, `bhāvetva`, `bhāvaniya`, `saṃbandha`, `samacintesi`, `ajjhāvasatar`, `sahitar`, `saritar`, `brūhetar`, `vedanāvant`, `ovariyāna`, `akātūna`, `sakha`, `byanti` (nt), `anupagamma` (beside `anupaggamma`), `akkhobhinī`, `paṭivisa`, `vibhajjeti`.
- Roots and signs that agree with DPD: √dhā (sign a), √his + ṃa, √muc + ya, √raj, √saj, √vid for `anuvicca`, √lu for `lāyati`, √nhā + ya, √namass, √ruc with `*e` for the causative `āroceti`, √cint for `cintetvā`.
- Genders and parts of speech that agree with DPD: `patta` "bowl" masc; `suci`, `gāmaṇi`, `kāsi` as masculine -i nouns; `phāsu` masc "ease"; `nandī` adj "who enjoys"; `sādiyati` as a passive.
- Glosses that are DPD senses: `siri` "splendour", `paricarati` "moves about", `āroceti` "explains", `āpajjati` "experiences", `dibbati` "shines", `dussati` "hates", `amu` "so and so", `mussati` "is forgotten".

## Decisions for the owner

These are not decided in the audit; the rows say `owner decision`:

- `<br>` in table cells and `{: … }` attribute markup versus the "no raw HTML in sources" rule (784 `<br>`, 78 `{:`). - [TODO] come back to it and find a way to replace with just natural readable text.
- How review pages mark the word under review (italics, bold or nothing). - bold Done for class 3 (italics → bold). Classes 4 and 8–14 mark no word: the word under review must be chosen before it can be bolded.
- class_13/2_adv/ - `Quick review: where do you find the -aṃ ending in Pāḷi grammar?` - the answer for that move to the footnote, so it is not visible at the beggining.

Part 2 of the findings: new rows, not yet seen by the owner. Sections D–I follow.

## A. Pāli and grammar content errors — new

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_10/6_loc_gen_abs.md:9 | `The **subject** of the sentence and the **participle** are in the locative **case**` | It is the subject of the absolute clause that is in the locative, not the subject of the sentence (in line 17 the sentence has its own subject). | "The subject of the clause and the participle…" | 7 |
| class_10/2_prp.md:94 | `\| √īr \| to move \| iriya \| iriy**āna** \| going around \|` | Root and base agree with DPD (*iriyati*, `√īr 1 a`, base iriya), and *esāna* (line 93) is in DPD. The participle *iriyāna* itself was not looked up. | DPD lookup (iriyāna) | 3 |
| class_11/5_home_work.md:25 | `na ca vokkama satthusāsanā vattanti` | The MN 122 text reads *vokkamma* (absolutive, double m). | `vokkamma` (DPD: ger of vokkamati, `vi + ud + √kam + ya`) | 8 |
| class_11/2_pp.md:53 | `\| vindati \| √vid \| to know \| + ita \| vidita \| known \|` | The row joins two verbs. In DPD *vindati* is "finds; gets" (`√vid 4`) and its pp *vidita* is "found"; *vidita* "known" is the pp of *vidati* (`√vid 2`). | Either `vidati \| √vid \| to know \| + ita \| vidita \| known`, or `vindati \| √vid \| to find \| + ita \| vidita \| found` | 7 |
| class_11/2_pp.md:156 | `seyyathāpi **suddhaṃ** vatthaṃ **apagataṃ** kāḷakaṃ …` | The text has the compound *apagatakāḷakaṃ* ("with stains gone"). Split into two words, `apagataṃ kāḷakaṃ` no longer agrees as shown, and the line is not marked `(simpl)`. | Restore the compound, or mark `(simpl)` | 6 |
| class_11/3_adj.md:22 | `\| √bal \| to be strong \| √bal + a \| bala \| strong \|` | *bala* is the noun "strength, power" (so glossed in class_6/4_subst.md line 11). DPD has it only as a neuter noun, not as an adjective "strong". (`samāna`, line 23, and `dhuva`, line 30, agree with DPD.) | Use an adjective for the example, or gloss `bala` as "strength" and mark it as a noun | 6 |
| class_14/3_caus_pass.md:21 | `\| ṭhape + īya \| ṭhāpīya \> ṭhapiyya \| ṭhapiyyati \|` | The base is `ṭhape` (short, previous row) but the next step shows `ṭhāpīya` with the long vowel back. | `ṭhapīya \> ṭhapiyya` (DPD: `√ṭhā *āpe īya`, base ṭhapiyya, with no long-vowel step) | 6 |

## B. Tables, paradigms and lists that disagree with each other or themselves — new

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_10/3_pron.md:61 | `\| 4.dat \| t**assā** \|` | *ta* fem dat/gen sg has `tassā` only; *ya* has `yassā, yāya` (line 180) and *ima* `assā, imissā, imāya` (line 135); the locative of *ta* itself has three forms incl. `tissaṃ`. | verify against the DPD inflection table (`tissā`, `tāya`) | 6 |
| class_10/3_pron.md:197 | `follow the same declension pattern as **ya***, (-a pron)* which is very similar` | The model pronoun is *ya* here and *ta* in the summary (line 238, `learn the **ta** declension by heart`). | Name one model | 7 |
| class_10/2_prp.md:132 | `\| 7.loc \| gaccha**mānāyaṃ**<br>gaccha**mānāya** \|` | Declared "like vedanā", whose table has the order `vedanāya, vedanāyaṃ` (class_7/2_fem_aa.md line 11). | Same order | 6 |
| class_11/3_adj.md:88 | `\| 8. voc \| uttar**ayo** \| uttar**iyo** \| uttar**īni**<br>uttar**ī** \|` | Further cells of the -i tables that differ from the noun tables they link to: voc pl masc `uttarayo` (noun: `aggī, aggayo`) and fem `uttariyo` (noun: `bhūmī, bhūmiyo`); neuter nom and voc sg `uttari, uttariṃ` (lines 67, 74; noun: `aṭṭhi`); loc pl `uttarīsu` only (line 87; nouns have short and long); abl sg order `-ismā, -imhā` (line 71; nouns `-imhā, -ismā`). | Follow the noun tables (as decided for old B10, B13) | 7 |
| class_11/3_adj.md:132 | `bah**uni**<br>bah**umhi**<br>bah**usmiṃ**` | Loc sg `-uni` for masculine and neuter; neither noun table has it (class_6/2_masc_u.md line 20 `bhikkhumhi, bhikkhusmiṃ`; class_9/2_nt.md line 118 `āyumhi, āyusmiṃ`). Neuter acc sg `bahu, bahuṃ` (line 127) also differs from the noun (`āyuṃ`). | Follow the noun tables | 7 |
| class_11/2_pp.md:87 | `In masculine like *buddha*, in feminine like *vedanā*, and neuter like *cittaṃ*.` | The course's masculine -a model is *nara* (class 2; class_10/2_prp.md line 107 says "like nara"). *buddha* has no table. Also two stems and one nominative. | "like *nara*, *vedanā*, *citta*" | 8 |
| class_11/3_adj.md:45 | `dīgh**āyaṃ**<br>dīgh**āya**` | Fem loc sg order reversed against the linked noun table (`vedanāya, vedanāyaṃ`) and against 2_pp.md line 112 (`gatāya, gatāyaṃ`). | Same order | 6 |
| class_13/3_pass_verb.md:124 | `\| 2nd \| dīy**o** \| dīy**ittha** \|` | The passive aorist table gives one form per cell, and not the same ones as the lesson table (class_4/10_aor.md lines 50–51): 2nd sg has only `-o` (lesson: `-i` first, then `-o`), 3rd pl only `-uṃ` (lesson: `-iṃsu` first). | 2nd sg `dīyi`, 3rd pl `dīyiṃsu` added or put first | 7 |
| class_12/3_card.md:184 | `\| 9 999 999 - 10 000000 \| \| ✔ \| \| ✔ \| (✔) \|` | `10 000000`: digit grouping broken. The header row above (line 176) mixes `**Mas.**`, `**fem.**`, `**Neut.**`. | `10 000 000`; `Masc.`, `Fem.`, `Neut.` | 9 |
| class_12/4_ordin.md:58 | `catutth**iyo**<br>catutth**ī**` | Voc pl order reversed against nom/acc pl (lines 51–52, `catutthī, catutthiyo`). The fem -ā loc sg (line 43, `paṭhamāyaṃ, paṭhamāya`) is also reversed against the noun table (`vedanāya, vedanāyaṃ`). | Same order as the noun tables | 6 |
| class_13/2_adv.md:25 | `\| añña \| adj \| another \| añña**tra** \| adv \| elsewhere \|` | *añña* is tagged `adj` here; class_10/3_pron.md lists it among the pronouns, and `sabba` in the next row is `pron`. | `pron` | 6 |
| class_14/3_caus_pass.md:13 | `**Here are some examples**` | One example follows (√ṭhā). | "Here is an example" | 7 |

## C. Translation and gloss problems — new

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_11/2_pp.md:158 | `lit. just like a **cleaned** cloth, **gone away** stains ...` | *suddha* is "clean, pure", not "cleaned". Three dots here, `…` in the Pāli line above. | "clean"; `…` | 6 |
| class_12/3_card.md:10 | `\| **dve** api jātiyo \| just **two** lives \|` | *api* is "even, also": "even two births". | "even **two** births" | 6 |
| class_14/2_caus_verb.md:73 | `A monk **could pour** water to the earth.` | *mattikā* is "clay, soil"; "pour water to" is not English. The same on line 79. | "could pour water on the soil" | 6 |
| class_10/2_prp.md:63 | `\| √khād \| to chew \| khāda \|` | The same root is glossed in two ways in different tables: √khād "to chew" / "to eat", √bandh "to bind" / "to tie", √vac "to say" / "to speak", √pucch "to ask" / "to question", √es "to seek" / "to look for", √labh "to get" / "to obtain", √kar "to do" / "to do, make"; √i is "(come, go)" in class 3, "(come)" in class 4 and "to come" in class 8. (√car, √dhā, √sad have their own rows.) | owner decision: one gloss per root, e.g. the DPD root meaning | 5 |

## D. English typos and grammar

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_10/3_pron.md:11 | `Not **everyone** will understand the dhamma` | No full stop, also on lines 13 and 17. | Add the full stops | 9 |
| class_10/2_prp.md:27 | `a man could see a **school of fish wandering around and remaining still.**` | Lower-case sentence start. | "A man…" | 8 |
| class_10/2_prp.md:37 | `There are 3 ways to form present participles` | No full stop or colon; also line 86 (`Dhammapada and Sutta Nipāta`) and footnote 25 (line 88). 5_emph.md line 17 and 6_loc_gen_abs.md line 23 end without one too. | Add punctuation | 8 |
| class_10/4_article.md:3 | `*A man* – here “a” is called the **indefinite article**, it refers to some unspecified man` | Comma splice, repeated on line 7. Line 3 has an en dash after the example, line 7 a hyphen. | "…article; it refers to…"; en dash in both | 7 |
| class_11/3_adj.md:179 | `Nouns and adjectives interchangeable unless proven otherwise from the context` | Verb and full stop missing. (old D36) | "Nouns and adjectives are interchangeable unless the context proves otherwise." | 9 |
| class_11/5_home_work.md:10 | `“**SBS kuṭi udāna**” based on sutta passages, describe particular qualities that should be developed and correspond to various names of [SBS kuṭis.](https://docs.google.com/spreadsheets/d/1JZPHwIzZv8kC92vjNc2Oy6VdQmwIRT23Ae1DUKersTU/)` | Not a complete sentence (no task verb for the student); the full stop is inside the link text. | "Write an “SBS kuṭi udāna”: based on sutta passages, describe…" | 8 |
| class_11/2_pp.md:18 | `In theory the formation of past participles is very easy, just add -**ta**, -**ita** or -**na** to the root.` | Comma splice. | "…is very easy: just add…" | 7 |
| class_11/2_pp.md:134 | `lit. thus - by me – **heard**` | Hyphen and en dash as the same separator; lines 136 and 144 have no full stop. | One dash; full stops | 8 |
| class_13/3_pass_verb.md:56 | `\| **√sād** \| to taste \| + iya \| **sādiya** \| **sādiya**ti \| enjoys;lit. is tasted \|` | No space after the semicolon. (DPD classes *sādiyati* as the passive of *sādeti*, so the example itself stands.) | `enjoys; lit. is tasted` | 7 |
| class_12/3_card.md:22-24 | `“*Good news*” : Almost each number has its own unique declensions and attributes,` … `so let’s have a closer look at them individually.` | One sentence split over two paragraphs; space before the colon; "Almost each". | "“*Good news*”: almost every number has … attributes, so let’s…" in one paragraph | 8 |
| class_12/3_card.md:172 | `## Summary of numbers gender and numbers` | Garbled heading. | "Summary of gender and number" | 9 |
| class_12/3_card.md:28 | `three genders; singular; agrees in gender and case` | Lower-case notes without full stop under every number heading (lines 28, 50, 64, 78, 92, 106, 126, 146, 160); lines 40, 44 and 46 start sentences in lower case; lines 230 and 232 have no full stop. | owner decision for the notes; capitals and full stops for the sentences | 7 |
| class_12/3_card.md:238 | `\| abbuda \| 1056 \| 1 00 000 000` | The long numbers are grouped unevenly at the front: `1 00 000…` (lines 236, 238), `1 0 000…` (line 241), `10 000…` (line 240). | Regular groups of three | 7 |
| class_13/2_adv.md:42 | `\| tatiya \| ordin \| third \| tatiy**aṃ** \| adv \| for third time \|` | Missing article. | "for the third time" | 9 |
| class_13/2_adv.md:3 | `Adverbs describe **how** or **when** an action is done, they give more information about the verb in the sentence.` | Comma splice. | "…is done; they give…" | 7 |
| class_13/3_pass_verb.md:48 | `Please refresh in memory the [“**assimilation of y**”](../class_4/7_basic_assim.md#basic-assim-y) from the Class 4.` | "refresh in memory"; "from the Class 4". (old D28) | "Please review … from Class 4." | 9 |
| class_13/3_pass_verb.md:7 | `I do not **cut** the tree` | No full stop; also lines 5, 21, 31, 143 and 4_pprp.md line 30. | Add punctuation | 8 |
| class_13/4_pprp.md:47 | `has both an *attanopada* and *parassapada* endings.` | Article with a plural. | "has both *attanopada* and *parassapada* endings." | 9 |
| class_12/6_home_work.md:10 | `“**SBS kuṭi udāna**” based on sutta passages, describe particular qualities that should be developed and correspond to various names of SBS kuṭis.` | Not a complete sentence (same in classes 11, 13, 14); here and in class 13 without the link that class 11 has. | As in the class 11 row; add the link | 8 |
| class_14/4_ptp.md:126 | `[^28]: This list is meant to show the vast number of ptp in the Cannon.` | Typo. (old D37) | "Canon" | 10 |
| class_14/4_ptp.md:9 | `like all the participles, they are **verbal adjectives**, they give more information about the noun they are describing.` | Comma splice; the same in 5_home_work.md line 23 (`feedback form](…), your corrections`). | "…adjectives: they give…" | 7 |
| class_14/3_caus_pass.md:9-11 | `onto the **causative** **base**` … `or, much more rarely, adding a causative suffix to a passive base` | One sentence split over two paragraphs, with no full stop at the end. | One paragraph | 7 |
| class_14/2_caus_verb.md:35 | `he **is** a monk` | Lower-case sentence starts on lines 35, 41 and 59; no full stop on lines 37, 47, 117, 161 and 4_ptp.md lines 3, 54. | Capitals and full stops | 8 |
| class_14/2_caus_verb.md:129 | `pācāpe**si**  pācāpe**tha**` | Double space. | Single space | 8 |
| class_4/7_basic_assim.md:1 | `# Some Basic Sandhi – The Assimilation of the Letter y  {: #basic-assim-y}` | Two spaces before the attribute (mech_checks reports the index title as different for this reason). | One space | 6 |

## E. Markdown defects that affect rendering

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_1/index.md:62-63 | `Optional:` … `-   Find 2-3 of your favorites` | The list follows `Optional:` with no blank line, so it is not parsed as a list. (old E6) | Blank line after `Optional:` | 8 |
| class_1/index.md:21-22 | `\- Vocab Pāli Class` … `\- Grammar Pāli Class` | Escaped hyphens inside a list item: the two lines print as running text with literal "-", not as a nested list. Lines 48–49 of the same page use a real nested list for the same two names. | Real nested list items | 8 |
| class_2/2_alphabet.md:44-45 | `**5 Cerebral or Retroflex Consonants <br>(muddhaja – produced at the top)**` … `These retroflex consonants have no English equivalents.` | Bold caption and paragraph with no blank line between them: they run together. The bold also spans a `<br>`. (old E7) | Blank line after the caption; caption on one line | 8 |
| class_2/4_home_work.md:7 | `\| **the man’s ox**<br>**бык человека** \|` | Row has 1 cell in a 5-column table (mech_checks: cols 1 != 5). (old E3) | Fill the row to 5 cells, or move the translation out of the table | 8 |
| class_2/3_decl_nouns.md:9 | `**8 cases.**` | Bold spans the full stop (or comma) here and on lines 42, 48, 50, 54, 64, 82, 84, 102, 112; lines 66, 70, 74, 122, 124 keep it outside. | Punctuation outside the bold | 8 |
| class_2/3_decl_nouns.md:50 | `goes **to** **the village.**` | Bold closed and reopened between two words. | `**to the village**.` | 8 |
| class_2/2_alphabet.md:14 | `b**ee,** tr**ee,** s**ee**` | Bold covers the commas. | `b**ee**, tr**ee**, s**ee**` | 8 |
| class_2/3_decl_nouns.md:138 | `names in ‑a take the same vocative as any a‑stem` | Two non-breaking hyphens (U+2011); the only ones in docs/bpc. Everything else uses the plain hyphen (`-a`). | Plain hyphens | 9 |
| class_3/2_conjug.md:19 | `\| --- \| --- \| --- \| --- \|` | A separator row in the table body prints as a row of dashes. (old E2) | Remove, or split into two tables | 9 |
| class_3/7_root_4.md:7 | `**ṇā** (**ṇo)[^10]** after a vowel` | Bold opens inside the bracket and closes after the footnote mark. (old E16) | `**ṇā** (**ṇo**)[^10]` | 9 |
| class_3/7_root_4.md:27 | `√ap (reach, attain) + u**ṇā** \> apuṇā` | Only `ṇā` is bold; the sign is `uṇā` (line 7 has `**uṇā**`). | `**uṇā**` | 9 |
| class_3/8_root_5.md:9 | `It has the conjugational sign **nā.**` | Bold spans the full stop; the same in 9_root_6.md line 7 (`**ṇhā.**`). 6_root_1.md line 19 has it outside. | `**nā**.` | 8 |
| class_3/11_histor_pr.md:3 | `are sometimes used to describe **past events**.  ` | Two trailing spaces force a line break inside the paragraph (mech_checks: TRAILING SPACE). Nowhere else in the class. | Remove the trailing spaces | 8 |
| class_3/10_root_8.md:17 | `1\. √cur (steal) + \*[^11]e \> c**o**re` | Escaped numbers `1\.` `2\.` `1\.` `2\.` (lines 17, 23, 27, 31) are plain text, not a list; the footnote mark sits between `*` and `e`. | owner decision (real list or plain labels); footnote mark after `e` | 6 |
| class_4/11_root_as.md:1 | `## Irregular verb √as (be)` | The file starts at H2 and has no H1 (mech_checks: NO/LATE H1); the same in 12_root_huu.md line 1. Every other page has one H1. (old E1) | `#` | 9 |
| class_4/7_basic_assim.md:43-44 | `**n + y \> ññ**  ` … `√ha**n** (kill) + **y**a + ti \> ha**ññ**ati (he is killed)` | Rule and example are joined by a trailing-space line break; every other rule on the page is followed by a blank line. (old E9) | Blank line after the rule | 9 |
| class_4/7_basic_assim.md:66 | `√si**v** (sew) + ya + ti \> si**vv**ati \> si**bb**ati (he sews)` | `ya` without the bold `y` on lines 66 and 68; all other examples have `**y**a`. | `**y**a` | 8 |
| class_4/4_vuddhi.md:84 | `**worth learning by heart.**` | Bold spans the full stop. In 7_basic_assim.md line 76 the full stop is a separate bold run (`**.**`). | Full stop outside the bold | 8 |
| class_4/2_dpr_tpr.md:31 | `\- Tipiṭaka Pāli Reader:` | Three paragraphs (lines 31, 33, 35) start with an escaped hyphen: they print as text with a literal "-", not as a list. | Real list | 8 |
| class_4/3_var_root_group.md:5 | `\| \| **Padarūpasiddhi**<br>**Buddhadatta** \|` | The column titles are the first body row under an empty header row. | Move them into the header row | 6 |
| class_5/3_future.md:13 | `Our bodily behaviour **should** **be** **purified**.` | Three separate bold runs for one phrase; the same on line 60 (`**causative** **verbs**`). | `**should be purified**` | 8 |
| class_5/3_future.md:23 | `by inserting *-***issa** between` | The hyphen is in italics, glued to the bold. | `**-issa**` | 8 |
| class_5/7_with.md:21 | `**saha** vatth**ehi[^17]** sobhati.` | The footnote mark is inside the bold. On line 15 the bold spans the full stop (`**accompanied by.**`); the same in class_6/5_and_or.md line 7 (`**ca.**`) and class_6/2_masc_u.md line 68 (bold comma in `ajjhāvasa**tar,**`). | Marks and punctuation outside the bold | 8 |
| class_5/2_pers_pron.md:64 | `\| **vo** \| you all, by you, for you, yours \| **893** \|` | In the other highlighted rows (lines 25, 26, 28, 35, 57, 60) the gloss is bold too. | Bold gloss | 7 |
| class_5/5_trans.md:43 | `kuṭṭhī nara**ṃ** odana**ṃ** yācati` | Only `ṃ` is bold; the other examples on the page bold the whole ending (`suriy**aṃ**`, `saṅgh**aṃ**`). | `nar**aṃ** odan**aṃ**` | 8 |
| class_8/4_adv_place.md:16 | `\| **-to** “from a place” \| \| \| \| \|` | The caption for the `-to` group is a table row inside the `-ttha` table; `-ttha` and `-hiṃ` are captions above their own tables. (old E4) | Caption above a separate table | 9 |
| class_8/3_fem.md:71 | `māt**uyā**<br>m**ātu**` | Bold marks the wrong part of the word; the genitive on line 73 has `māt**u**`. (old E17) | `māt**u**` | 9 |
| class_8/2_abs_ger.md:21 | `a **subordinate** **clause** and a **main** **clause**` | Bold closed and reopened between two words. | `**subordinate clause**`, `**main clause**` | 8 |
| class_9/2_nt.md:3-4 | `more than 17000 words in the current DPD database[^22].` … `[^22]: Relevant for 2025 year` | The footnote definition follows the paragraph with no blank line (the only such case; line 93 has one). | Blank line before the definition | 5 |
| class_10/2_prp.md:5 | `dīghaṃ vā **assasanto** “dīghaṃ assasāmī’ti pajānāti` | The opening double quote is never closed (the `’` is the sandhi apostrophe); the same on line 7. (old E13) | `“dīghaṃ assasāmī”ti`, or single quotes on both sides | 8 |
| class_10/2_prp.md:191 | `“I will breathe in **gladdening** the **mind” he trains,**` | Bold swallows the closing quote and "he trains,"; line 193 is correct. (old E14) | `**mind**” he trains,` | 9 |
| class_10/2_prp.md:148 | `**Masculine ending in -anta (**like bhagavant**)**` | Broken bold; the other five captions are `**…** (like …)`. (old E15) | `**Masculine ending in -anta** (like bhagavant)` | 9 |
| class_10/2_prp.md:144 | `\| 6.gen \| gaccham**ānassa** \|` | Bold starts one letter late; every other cell has `gaccha**mān…**`. (old E17) | `gaccha**mānassa**` | 9 |
| class_10/3_pron.md:63 | `t**āsaṃ**<br>**tāsānaṃ**` | Whole word bold instead of the ending; the same on line 222, and `**yāhi**` on lines 181 and 221. (old E17) | `t**āsānaṃ**`, `y**āhi**` | 9 |
| class_10/7_home_work.md:10-11 | `from class 10.` … `## Extra Reading` | The heading follows the list item with no blank line (the only homework page like this); some renderers read it as part of the list item. (old E5) | Blank line before the heading | 7 |
| class_10/3_pron.md:238-240 | `follow it with small` … `variations. For **ima**, memorize only the high-frequency forms: ayaṃ, imaṃ, idaṃ, iminā, imassa,` | Hard-wrapped paragraph (three source lines). | One line | 8 |
| class_10/3_pron.md:48 | `(literally: **in that in that)**` | Bold swallows the closing bracket. | `(literally: **in that in that**)` | 9 |
| class_10/3_pron.md:93 | `but with an initial *“***e***”*.` | Italic quote marks wrapped around a bold letter. | `an initial “**e**”.` | 7 |
| class_10/3_pron.md:108 | `a**ssa**<br>ima**ssa**` | The bold boundary for the same endings moves within the *ima* tables: `ima**ssa**`, `ima**mhā**` but `im**amhi**`, `im**asmiṃ**` (line 111) and `ima**mhi**` (line 159); `im**esaṃ**` (line 108) but `imes**aṃ**` (lines 156, 207, 233). | One boundary: `im**assa**`, `im**esaṃ**` | 8 |
| class_10/2_prp.md:15 | `**gender, case and number.**` | Bold spans the full stop; also lines 27, 205 and 207, and a comma on line 199 (`**not knowing health,**`). | Punctuation outside the bold | 8 |
| class_10/5_emph.md:7 | `tasmiṃ **eva** āsane **-** in that very seat; in that exact seat` | A bold hyphen as separator; lines 11 and 15 use a plain hyphen. On line 13 the note `(less common)` is inside the italics of the gloss. | En dash, not bold | 7 |
| class_11/3_adj.md:7-9 | `vatthaṃ (a cloth)` … `**parisuddhaṃ odātaṃ** vatthaṃ (a **clean white** cloth)` | Three example lines with no blank lines between them: they collapse into one paragraph. (old E8) | Blank lines between them | 9 |
| class_11/5_home_work.md:25 | `\> kathañcānanda, satthāraṃ sāvakā mittavatāya samudācaranti` | Escaped `>`: a literal ">" prints instead of a block quote. (old E12) | `>` | 8 |
| class_11/3_adj.md:24 | `√kam + *a + ka` | Unescaped asterisk here and on lines 25–26 (`*ana`, `*ī`); the rest of the course writes `\*`. It works only while each cell has a single `*`. (old E19) | `\*a` | 7 |
| class_11/3_adj.md:5 | `Adjectives are a class of words that give more information about a noun. ` | Trailing space (mech_checks). | Remove | 8 |
| class_11/2_pp.md:148 | `lit. there is **given,** there is **sacrificed**, there is **offered**` | Bold covers the first comma but not the second, on lines 148, 150 and 152. Line 142 has a bold full stop (`**by him.**`); 4_abl_sep.md line 13 too. | Punctuation outside the bold | 8 |
| class_12/3_card.md:138 | `I see **twenty men**   vīsatiṃ purise` | Three spaces used as a column separator: they collapse to one space. (old E10) | A two-column table, or a dash | 9 |
| class_12/3_card.md:73 | `\| 6.gen \| t**iṇṇaṃ**<br>**tiṇṇannaṃ** \|` | Whole word bold instead of the ending; line 71 has `t**iṇṇannaṃ**`. (old E17) | `t**iṇṇannaṃ**` | 9 |
| class_12/5_kahap.md:3 | `![](../../assets/images/kahapana.png)` | Image with empty alt text. (old E20) | Add alt text | 8 |
| class_12/3_card.md:136 | `vīsat**iyā**<br>vīsati**yaṃ**` | Bold boundary moves inside one cell; the same in `koṭ**iyā**<br>koṭi**yaṃ**` (line 170). | `vīsat**iyaṃ**`, `koṭ**iyaṃ**` | 8 |
| class_12/4_ordin.md:50 | `**Feminine<br>ā**` | Bold spans a `<br>`; the singular table (line 36) has `**Feminine ā**` on one line. | Same header in both tables | 8 |
| class_13/2_adv.md:19 | `\| bahu \| adj \| many \| bahuk**khattuṃ** \| adv \| many times \|` | Bold cuts the cluster: the suffix is `-kkhattuṃ`. | `bahu**kkhattuṃ**` | 8 |
| class_13/2_adv.md:5-7 | `kiṃ nu kho ahaṃ saṇikaṃ gacchāmi?` … `Why am I going **slowly**?` | The English adverb is bold, the Pāli one (`saṇikaṃ`) is not. | `**saṇikaṃ**` | 8 |
| class_13/3_pass_verb.md:71-72 | `typically have an agent in the **instrumental case**.  It is usually clear from` … `the contextual usage.` | Hard-wrapped paragraph, with a double space mid-sentence. The same wrap in 4_pprp.md lines 46–47. | One line | 8 |
| class_13/2_adv.md:91 | `**Pure Adverbs,** which are not formed` | Bold covers the comma; also `**nipātā,**` on line 93. Split bold in 3_pass_verb.md line 17 (`**passive** **base**`) and 4_pprp.md line 40 (`**reflexive** **verbs**`, `**middle** **voice**`). | Punctuation outside; one bold run per phrase | 8 |
| class_14/4_ptp.md:126-128 | `Don't worry if you can't read the end of it.` … `aññātabbaṃ (2), anubandhitabbaṃ (2), anubandhitabbo (5)` | Footnote 28 speaks of "this list", but the list is an ordinary body paragraph after the footnote definition: the list prints in the page, the note about it at the foot. (old E11) | Put the list inside the footnote, or the sentence above the list | 8 |
| class_14/4_ptp.md:105 | `pac**itabbānaṃ** <br> \|` | Trailing `<br>` at the end of a cell here and twice on line 109: an empty line inside the cell. (old E18) | Remove | 9 |
| class_14/2_caus_verb.md:31 | `1\. bhavati (active verb) “he is” is an intransitive verb` | A lone escaped `1\.` with no second item (line 37, the causative half, has none). | Remove `1\.` | 7 |
| class_14/2_caus_verb.md:137 | `How would you conjugate √**pac + \*e \> pāce**` | Bold starts after the root sign. On line 109 `*-\****e**` and on 3_caus_pass.md line 9 `*-***ya**` an italic hyphen is glued to the bold. | `**√pac + \*e \> pāce**`; `**-e**` | 7 |
| class_14/2_caus_verb.md:97 | `gets **strengthened,** **pat** \> **pāt**` | Bold covers the comma; line 43 a full stop (`**to be.**`), lines 49, 55, 61 too (`**carati.**`, `**cāreti.**`). | Punctuation outside the bold | 8 |
| class_14/3_caus_pass.md:54 | `\| caus pass pr \| bhāvīyati \| it is caused to be; it is developed \|` | No bold ending; every other verb row of the table has one. | `bhāviya**ti**` (with the owner decision on old A46) | 7 |
| class_2/3_decl_nouns.md:165 | `\| \| Singular \| Plural \|` | Column titles sit in the first body row under an empty header row, here and in most tables that have titles (the conjugation tables of classes 3–5, the pronoun and adjective tables, class_12/4_ordin.md). class_4/9_masc_i.md, class_4/11_root_as.md, class_9/2_nt.md (comparison tables) and class_12/3_card.md put them in the real header row. | Titles in the header row | 7 |
| class_14/5_home_work.md:23 | `will help us to improve the course for future students.` | No newline at the end of the file (mech_checks); the same in class_3/10_root_8.md. | Add the final newline | 6 |

## F. Convention drift

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_2/2_alphabet.md:26 | `**k**aruṇā \| (compassion) \| **k** \|` | The letter column is bold in the guttural, palatal, retroflex and dental tables (lines 26–63) and plain in the vowel, labial and "other" tables (lines 11–20, 69–88). | One style | 8 |
| class_2/2_alphabet.md:7 | `**8 Vowels (sara) a ā i ī u ū e o**` | Section captions on this page are bold paragraphs down to line 106, then H2 headings from line 113 (`## Double Consonants`). | owner decision | 6 |
| class_1/index.md:56 | `## Homeless work` | The three other H2 headings on the page carry an id (`{: #course-structure}` etc.); this one does not. | owner decision | 5 |
| class_3/12_help_with_ex.md:15 | `## The genitive case` | Heading case: line 3 `## Word Order` (title case), line 15 and line 23 `## Agreement between nouns (pronouns…) and verbs` (sentence case). | One style | 7 |
| class_3/14_home_work.md:23 | `A.K. Warder Introduction to Pāli` | No break between author and title; lines 24–25 and class_2/4_home_work.md have `<br>` there. | Same layout as the other rows | 7 |
| class_3/10_root_8.md:44 | `**Conjugation of -ati pr**` | The same caption as 3_preset.md line 21, here for the -ayati verbs; the first table on this page is `-eti pr`. Also the first table has pronouns (`so dhāre**ti**`), the second has none. | `-ayati pr`; pronouns in both or neither | 6 |
| class_4/10_aor.md:43 | `## 1st conjugation group & others` | "conjugation group" here and on line 54; the pages of classes 3–4 are titled "Root Group N", and line 7 of this page says "group 1 roots". | "Root group 1 & others" | 7 |
| class_4/10_aor.md:23 | `bhuñja + i \> bhuñji (he ate, enjoyed)` | The aorist ending is bold in the other examples (lines 11, 15, 27) and plain here. | `bhuñja + **i** \> bhuñj**i**` | 7 |
| class_4/13_home_work.md:12 | `A.K. Warder Introduction to Pāli` | No `<br>` between author and title (same as class_3/14_home_work.md); the other rows have it. | Same layout | 7 |
| class_5/5_trans.md:39 | `## Di-transitive verbs (dvikammaka “two objects”)` | Lower-case "verbs"; the two other H2 headings have "Verbs" (lines 3, 19). The H1 lists the three kinds in a different order from the page. | "Di-transitive Verbs" | 8 |
| class_6/4_subst.md:57 | `## Declension of *-ant masc*` | The only declension heading with italics and no anchor id (compare `## Declension of -ī masc {: #declension-of-i-masc_1}`). | Same pattern as the others | 7 |
| class_6/1_review.md:10 | `[AN8.53](https://s.dhamma.gift/an/an8/index.html#an8.53) simpl` | `simpl` without brackets here and on line 15; class 5 review has `(simpl)`. | `(simpl)` | 8 |
| class_5/6_say_no.md:30 | `**n'eva** tasmiṃ samaye dukkhaṃ vedanaṃ vedeti, **na** adukkham’asukhaṃ vedanaṃ vedeti` | Straight and curly apostrophe in the same sentence. | One kind | 8 |
| class_8/2_abs_ger.md:148 | `Examples: **disvāna ; vatvāna ; sutvāna ; ovariyāna ; akātūna**` | A space before each semicolon. (The forms *ovariyāna* and *akātūna* are in DPD.) | `disvāna; vatvāna; sutvāna; ovariyāna; akātūna` | 6 |
| class_8/2_abs_ger.md:11 | `1.  having approached, ...` | Three dots on lines 11, 17, 19; the ellipsis character on lines 13 and 15 of the same list. | `…` | 9 |
| class_8/2_abs_ger.md:105 | `### 5. -ya added to the root` | Headings 1–4 write the suffix without a hyphen (`### 1. tvā added to the root`), 5–7 with one. | One style | 8 |
| class_8/3_fem.md:62 | `## Feminine nouns mātu (mātar) and dhītu (dhītar)` | Lower-case "nouns"; the six other headings on the page have "Feminine Nouns". The heading names *dhītar* but no form of it follows. Anchor ids are on four of the seven sections only. | "Feminine Nouns"; ids on all or none | 7 |
| class_8/1_review.md:13 | `devaputto gāthaṃ abhāsi – "bhikkhu siyā jhāyī vimuttacitto"` | Straight double quotes here and on line 18, and in 2_abs_ger.md line 170; the class otherwise uses curly quotes. | Curly quotes | 8 |
| class_7/3_opt.md:75 | `([MN10.16](https://s.dhamma.gift/mn/mn10/index.html))` | Label with a section number; other MN labels are plain (`MN18`, `MN131`). | `MN10` | 6 |
| class_9/3_inf.md:58 | `### 4. bases ending in -e + tuṃ` | Headings 1–3 are `root + -tuṃ`, `root + -ituṃ`, `base + -ituṃ`; this one is plural, and the suffix has no hyphen. | `### 4. base ending in -e + -tuṃ` | 7 |
| class_9/1_review.md:10 | `[AN4.244](https://s.dhamma.gift/an/an4/index.html#an4.244) modified` | Three markers for the same thing in one review: `simpl` (line 5), `modified` (line 10), `very very modified` (line 15). | One marker, e.g. `(simpl)` | 8 |
| class_9/4_dat_purpose.md:1 | `# The dative of purpose` | "Dative of Purpose" with capitals on line 3, lower case in the title and on line 9. | One style | 6 |
| class_10/2_prp.md:25 | `**maccha-gumbaṃ** **carantaṃ** **tiṭṭhantaṃ**` | Hyphenated here, `macchagumbaṃ` four lines below (line 29). | One spelling | 9 |
| class_10/2_prp.md:51 | `**present participles ending in -nta**` | Lower-case caption, all bold (also line 69); line 84 has `Present participles ending in **-āna**`. | One style | 8 |
| class_10/2_prp.md:189 | `**abhippamodayaṃ** **cittaṃ** assasissāmī'ti sikkhati` | Straight apostrophes here; curly in the same page's first examples (lines 5, 7). Straight double quotes on line 213 and in 6_loc_gen_abs.md line 3. | Curly | 8 |
| class_10/2_prp.md:201 | `([MN75](https://s.dhamma.gift/mn/mn75/index.html) māgaṇḍiyasuttaṃ)` | Reference styles on one page: italic without brackets (lines 7, 17, 25), italic in brackets with the sutta name (lines 195, 209), plain in brackets (line 201). | One style | 8 |
| class_10/1_review.md:30 | `*[SN55.23](https://s.dhamma.gift/sn/sn55/index.html#sn55.23) godhasakkasutta*` | Sutta name as one word; the other five references have `… sutta` as a separate word. | "godhasakka sutta" | 7 |
| class_11/3_adj.md:38 | `**neuter** [(aṃ)](../class_9/2_nt.md#declension-of-neuter-nouns-ending-in-a)` | Header links of the adjective tables: plain here, bold from line 66 on (`[**(-i)**]`); `(aṃ)` and `(unī)` (line 153) have no hyphen; `(aṃ)` is a nominative while the others are stems. | `[**(-a)**]`, `[**(-unī)**]` | 8 |
| class_11/3_adj.md:60 | `\| 8. voc \| dīgh**ā** \|` | `8. voc` with a space here and on line 88; `8.voc` in the other six tables of the page. (old F1) | `8.voc` | 9 |
| class_11/2_pp.md:22 | `Until you learn more about Sandhi and Sanskrit roots` | "Sandhi" with a capital; "sandhi" on lines 20, 40 and 83. | "sandhi" | 8 |
| class_11/2_pp.md:24 | `There are, quite literally, thousands of examples...` | Three dots; also 4_abl_sep.md line 9. The class uses `…` elsewhere. | `…` | 8 |
| class_13/4_pprp.md:10 | `\| pass.pr \| labbhati \| it is got, is obtained \|` | `pass.pr` / `pass.prp` in the first table, `pass pr` / `pass prp` in the second (lines 27–28), which also has `passive base` in full. | One form | 9 |
| class_13/2_adv.md:47-51 | `1.  masculine, feminine, neuter acc s` … `3.  present participle masc nom. s.` | `acc s` without full stops, `nom. s.` with; the tables of this page use `adv`, `adj`, `noun`, and once `m` (line 64, `java \| m \| speed`) for a noun. | One abbreviation style; `noun` on line 64 | 8 |
| class_12/2_numb.md:9 | `\| 1. \| cardinal \| one, two, three, ... \|` | Three dots on lines 9, 10, 22, 24; `…` on line 28; "etc" on line 30. | `…` | 8 |
| class_12/1_review.md:13 | `"sabbehi me piyehi manāpehi nānā-bhāvo vinā-bhāvo"ti` | Straight double quotes; also 5_kahap.md line 19 (`"Cash"`). Line 5 has `simpl`, line 21 `(simpl)`; class_13/1_review.md line 5 has `(modif)`. | Curly quotes; one marker | 8 |
| class_14/4_ptp.md:15-31 | `to be` … `should be…` … `could be …` … `must be ...` … `suitable to be….` | Five ways of writing the ellipsis in one list (none, `…`, ` …`, ` ...`, `...`, `….`). | `…` throughout | 9 |
| class_14/4_ptp.md:42 | `\| vi + ā + √kar \| to answer \| vyākar**aṇīya** \| answered \|` | `vy-` here; the word list on line 128 has `by-` (`byākātabbā`, `byāharitabbaṃ`). | owner decision; one spelling | 7 |
| class_14/3_caus_pass.md:7 | `means "it is caused to be done" or, more rarely, "he causes it to be done,"` | Straight double quotes; line 5 has curly ones. Straight apostrophes on line 63 and in 4_ptp.md line 126. | Curly | 8 |
| class_14/3_caus_pass.md:29-33 | `1\. active present participle. e.g. karonta` … `2\. (passive) past participle e.g. kata` | Full stop before `e.g.` in item 1 only. | Same in all three | 7 |
| class_2/3_decl_nouns.md:166 | `\| 1. Nominative \| nar**o** \| nar**ā** \|` | Case labels in declension tables: `1. Nominative` (5 tables: class 2, class_4/9_masc_i.md, class_5/2_pers_pron.md), `1. nom` (2 tables), `1.nom` (59 tables); `3.inst` (49) against `3.instr` (10) and `3. instr` (2); `8. voc` with a space (4) against `8.voc` (37). (old F1) | One label set | 9 |
| class_4/9_masc_i.md:7 | `\| \| Singular \| Plural \|` | A Singular / Plural title row is present in the declension tables of classes 2 and 4 only; none of the 59 `1.nom` tables from class 5 on has one. (old F2) | owner decision: add everywhere or nowhere | 8 |
| class_3/3_preset.md:25 | `\| \| singular \| plural \| \| \|` | Conjugation tables: the title "plural" stands over the English gloss of the singular, and the plural columns have no title (16 tables: class 3 ×5, class_4/10_aor.md ×3, class_4/11_root_as.md ×3, class_4/12_root_huu.md ×3, class_5/3_future.md ×2). The pronouns *so / te* are shown in some tables and not in others; class_3/4_imper.md has no title row; the class 7 optative and class 13 passive tables have no English columns. (old F3) | `\| \| singular \| \| plural \| \|`; one layout | 8 |
| class_3/4_imper.md:15 | `\| 3rd \| vada**tu** \| he must speak \| vad**antu** \| they must speak \|` | The bold boundary of endings moves: `vada**tu**` / `vad**antu**` in one row; `gacche**yya**` (class 7) against `dīy**eyya**` (class 13); `sāvak**aṃ**` against `**sāvakena**` (class 2); see also the rows on class_10/3_pron.md line 108 and class_12/3_card.md line 136. (old F4) | One rule for where the ending starts | 8 |
| class_2/3_decl_nouns.md:60 | `**3. The Instrumental Case (tatiyā & karaṇa)**` | A section caption as a bold paragraph where its siblings are headings: cases 1, 2, 4–8 on this page are H2; in class_10/3_pron.md *eta* is H2 while *ta*, *ima*, *ya* are bold; in class_14/2_caus_verb.md Example 3 is bold while Examples 1 and 2 are H3. (old F5) | Headings in all three places | 9 |
| class_13/4_pprp.md:13 | `## How To Form Passive Present Participles (pprp)` | Heading capitalisation: "How to …" in 17 headings (classes 1–13), "How To …" in 7 (this page and class 14); class 14 also has "Transitive, Intransitive And Di-Transitive Verbs". Further: "Masculine Noun ending in -i" (class 4), "Masculine nouns ending in -ī" (class 5), "Feminine Nouns ending in -ā" (class 7); "Adverbs of time", "Adverbs of place". (old F6) | One capitalisation rule | 9 |
| class_4/6_root_3.md:1 | `# Root Group 3 – divādigaṇa` | En dash in the titles of groups 3 and 7, hyphen in groups 1, 2, 4, 5, 6 and 8 (and in both indexes). (old F7) | One dash | 9 |
| class_4/10_aor.md:25 | `√mant 8 aya (counsel, invite) \> mantaya` | Root notation: the group 8 sign is written `8 aya`, `8 e` (class_5/3_future.md, class_7/3_opt.md) and `8 \*e` (class_4/4_vuddhi.md, class_5/3_future.md); prefixes are joined with `+` everywhere except four rows of class_14/4_ptp.md (`abhi √nand`); `+ etc.` once (class_4/5_root_2.md) against `+ etc` six times; `**bhū 1 a (be)**` without √ and `√root` against `root` in class_14/3_caus_pass.md. (old F8) | One notation | 8 |
| class_6/4_subst.md:39 | `[SN1.1](https://s.dhamma.gift/sn/sn1/index.html#sn1.1) sā devatā **bhagavantaṃ** etad’avoca` | Reference placement and style: before the quote (class_6/4_subst.md, class_6/5_and_or.md, class_14/3_caus_pass.md); on its own line before it (class_5/7_with.md); after it in brackets (most pages); italic, with the sutta name (class 10 review, class_10/2_prp.md); bare after the quote (class_14/4_ptp.md). Labels with a section number (`DN3.15`, `DN5.2`, `DN9.6`, `DN14.14`, `DN16.11`, `DN16.27`, `DN22.18`, `MN10.16`) stand beside plain ones (`DN3`, `MN18`). Five review references have no link: `VIN PAT NID` (classes 3, 4, 11), `Uddissan'ādhiṭṭhānā` (class 5), `(buddhānussati formula)` (class 7). (old F10) | One style; links where a text exists | 8 |
| class_13/1_review.md:5 | `[SNP13](https://s.dhamma.gift/kn/snp/index.html#snp2.1) (modif)` | The "simplified" marker has five forms: `simpl` ×12, `(simpl)` ×6, `modified` ×2, `(modif)` ×1, `very very modified` ×1. (old F11) | `(simpl)` | 9 |
| class_5/6_say_no.md:14 | `[^16]: It frequently appears in text as **n'atthi**` | Sandhi apostrophe: curly `’` 41 times, straight `'` 21 times (all apostrophes: 44 against 23). Straight double quotes on 12 lines in 11 files (homework pages of classes 5–8, class_8/1_review.md, class_8/2_abs_ger.md, class_10/2_prp.md, class_10/6_loc_gen_abs.md, class_12/1_review.md, class_12/5_kahap.md, class_14/3_caus_pass.md); curly ones 316 times. (old F12) | Curly throughout | 9 |
| class_9/3_inf.md:88 | `\| alaṃ \| ind \| it is suitable (to) ; one is able (to) \|` | Abbreviations: `masc.`, `pr.`, `ind.` with full stops in class 2 (review list and vocabulary), `ind`, `adv`, `pr`, `masc`, `fem` without in class 9 and class 13; `acc s`, `nom. s.`, `sg`; `pass.pr` / `pass pr`; `BD`, `PED`, `sk` / `Sk` are never expanded. (old F13) | One abbreviation list, as in class_2/1_review.md | 8 |
| class_8/5_home_work.md:17 | `p105 - 110 (the gerund)` | Page ranges: `pN – N` ×18, `pN-N` ×9, `pN - N` ×7, `pN–N` ×1; "p… (topic)" in classes 2–11, "Topic (p…)" in classes 13–14. List markers: `1.␣␣` on 154 lines, `1.␣` on 33; escaped pseudo-lists (`1\.`, `\-`) on 29 lines in 9 files beside real lists. (old F14) | `pN–N`; one marker style | 9 |
| class_5/5_trans.md:7 | `bhikkh**u** paṭhav**iṃ** na khaṇati` | *paṭhavī* here, *pathavī* in class_4/2_dpr_tpr.md, class_8/3_fem.md and class_10/3_pron.md; `vy-` and `by-` on one page (class_14/4_ptp.md); compounds with and without hyphens (class_10/2_prp.md); one Pāli sentence with a capital (class_3/11_histor_pr.md, `*Atha kho bhagavā ārāmaṃ gacchati.*`). (old F15) | owner decision per item; `pathavī` | 8 |
| class_4/13_home_work.md:6 | `4. Learn conjugations and declensions from class 4 “Grammar Pāli Class”` | Homework pages: "from Anki Deck" stands before “Grammar Pāli Class” in class 3 only and is missing from class 4 on; `DPR / TPR` ×5, `DPR/TPR` ×2, `DPR, TPR` ×1; `2–5`, `2-5` (class 7), `up to 2–5` (class 9); `Optional:` (class 1) against `**Extra:**`; the SBS kuṭi link only in class 11; class 12 has no Extra Reading table. Duplicate footnotes: 14 = 15 = 19; 20 = 21; 22 = 23; 8 = 10; "mūla" in 14/15/19 against "Mūla" in 20/21. (old F16) | One wording; one footnote per fact | 8 |
| class_3/1_review.md:3 | `1.  saṅgho uposathaṃ *kareyya*` | Review pages mark the word under review in italics (class 3), in bold (classes 5–7) or not at all (classes 4, 8–14). | owner decision | 6 |
| class_2/2_alphabet.md:44 | `**5 Cerebral or Retroflex Consonants <br>(muddhaja – produced at the top)**` | Raw HTML: `<br>` is on 414 lines in 41 files (784 occurrences), all inside table cells except this one. `{: .align-right }` is used 60 times and `{: #id }` 18 times. This conflicts with the project rule "no raw HTML in the sources" but is the established way to stack forms in a cell. (old raw-HTML note) | owner decision: an explicit exception for `<br>` in cells, or a script-level solution | 8 |
| class_2/4_home_work.md:26 | `\| A Bhikkhu Māgadhabhāsā (Pāḷi) \| Corresponding chapters \|` | "Pāli" 125 times in running text; "Pāḷi" 12 times, all in this book title. Consistent as it stands. | owner decision | 5 |
| class_10/3_pron.md:239 | `memorize only the high-frequency forms` | Spelling mixes British (behaviour ×3, colour ×2, honoured, traveller, tranquillity, recognise ×2) and American (favorites, memorize ×2, recognize ×1). | owner decision | 7 |

## H. Data to re-verify (forms, references, counts)

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_2/2_alphabet.md:103 | `avadhy**ai** \| (disregards)<br>Pāli ujjhāyati` | The gloss is a finite verb ("disregards") but `avadhyai` is prefix + root (ava + √dhyai), not a verb form. The finite form would be *avadhyāyati*. The old audit called it "not a recognisable form"; it is the root form. (old H5) | `avadhyāyati`, or gloss it as a root ("to disregard"). DPD gives no Sanskrit form for *ujjhāyati*: verify | 5 |
| class_5/2_pers_pron.md:25 | `\| **ahaṃ** \| **I** \| **14232** \|` | `ahaṃ` 14 232 and `tvaṃ` 16 207 (line 56) in the four Nikāyas look too high next to `bhagavā` 4 803 from the same corpus (class_6/4_subst.md line 70) and next to `tuvaṃ` 32, `tayā` 44, `tava` 46. Not recomputed. (old H1) | verify the counts | 6 |
| class_6/5_and_or.md:7 | `[AN5.4](https://s.dhamma.gift/an/an5/index.html#an5.4) thero bhikkhu sabrahmacārīnaṃ piyo **ca** hoti manāpo **ca** garu **ca** bhāvanīyo **ca.**` | The wording belongs to the Thera suttas of AN 5 (around AN 5.81–88); AN 5.4 is a different sutta. Not checked against the text. | verify the reference | 6 |
| class_8/2_abs_ger.md:156 | `atha kho bhagavā pubbaṇhasamayaṃ **nivāsetvā** … sāvatthiṃ piṇḍāya pāvisi ([MN18](https://s.dhamma.gift/mn/mn18/index.html))` | MN 18 is set at Kapilavatthu (the Blessed One enters Kapilavatthu for alms), so the Sāvatthī wording does not belong to it. The same reference is on line 166. Not checked against the text. | verify the reference | 7 |
| class_8/2_abs_ger.md:162 | `typically ending in **-ya**, **-iya**, **-eyya**, etc.` | `-eyya` is the optative ending; which gerunds end in -eyya is not shown. | verify | 5 |
| class_7/1_review.md:10 | `[AN5.4](https://s.dhamma.gift/an/an5/index.html#an5.4) simpl` | Same doubtful reference as class_6/5_and_or.md line 7; also `simpl` without brackets. | verify the reference | 6 |
| class_9/2_nt.md:3 | `These are very common, more than 17000 words in the current DPD database[^22].` | class_2/3_decl_nouns.md gives 15 199 neuter nouns (2023 data) and this page "more than 17 000" (2025); neuter -i and -u together are 452 there, while line 91 here says `at most 400` for -u alone. The earlier table does not say it is out of date. Not recomputed. (old H2) | verify; one data year across the course | 7 |
| class_12/3_card.md:241 | `\| ababa \| 1076 \|` | The rows above rise in steps of seven (abbuda 10⁵⁶, nirabbuda 10⁶³, ahaha 10⁷⁰), which would make *ababa* 10⁷⁷. DPD also gives 10⁷⁶ (ababa 2), so the text follows DPD; the step is broken in both. | verify (text and the DPD entry) | 5 |
| class_12/3_card.md:186 | `These are the only numbers encountered in the Tipiṭaka that have been *actually* covered by DPD so far.` | The list that follows (lines 190–228) has no 17 or 19 although `sattarasa` is in the table above (line 121); the fraction `1/16 soḷasī` sits among the cardinals; 15 has two forms here (line 204) and three on line 119; `cattārīsa` / `cattālīsā` (line 213) end differently. (old H6) | Re-generate the list from DPD. DPD lookup for 40: the lookup found only `cattārīsa` (nt, a sutta-title word) and no headword `cattālīsa`; the forms in -ā were not looked up | 6 |
| class_14/4_ptp.md:124 | `reveals more than **1000** examples, some of which are used around **1000** times![^28]` | The list on line 128 has 556 entries and stops at *paṭi-* with `…`; its highest count is `gahetabbaṃ (223)`. Neither "more than 1000" nor "around 1000 times" can be seen in it. (old H3) | verify; give the real figures or the full list | 7 |
| class_14/4_ptp.md:128 | `asevitabbopi (1)` | The list contains unsegmented sandhi strings that are not single potential participles: `asevitabbopi`, `aviññātamajānitabbaṃ`, `cittamupanetabbaṃ`, `gāḷhamogāhitabbaṃ`, `hāsamabhijanetabbaṃ`, `nibbānamadhigantabbaṃ`, `nappaṭippassambhetabbāṭṭhārasakaṃ`, `naupasampādetabbekavīsativāro`, `niddisitabbāvayavena`. (old H4) | Remove or segment them | 8 |

## I. Further details on the material under review

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_11/4_abl_sep.md:1 | `# Ablative of Separation` | The page is about the suffix `-to` and its sense "as" (line 9); "separation" is not explained or shown beyond `rukkhato`. | owner decision: title "The suffix -to" | 5 |
| class_12/3_card.md:118 | `\| 14 \| *catuddasa*<br>cuddasa \|` | The first form is in italics here and on line 119 (`*pañcadasa*`), with no note on what the italics mean. | Add a note, or remove the italics | 5 |
| class_13/3_pass_verb.md:96-99 | `\| **√pad** \| pajja \| + iya \| **pajjiya** \| up**pajjiya**ti \| is brought into being \|` | A second table follows the first with no caption; from the roots it seems to hold the group 3 examples of point 5, the first table the group 2 ones. | Captions "group 2" / "group 3" | 5 |
| class_14/3_caus_pass.md:23 | `[VIN1.4.2.8](https://s.dhamma.gift/vin/tv/pli-tv-bu-vb-np/index.html#pli-tv-bu-vb-np18) āyasmato upanandassa` | The example has no translation; the other examples of the class do. | Add one | 6 |
| class_14/4_ptp.md:113 | `\| \| Masculine \| \| Feminine \| \| Neuter \| \|` | The two declension tables (lines 100, 113) have no caption (`-tabba`, `-anīya`) and no singular / plural labels over the paired columns. | Captions and sg / pl labels | 6 |

## Mechanical detail

Counts from `mech_checks.py docs/bpc --folder-footnotes` and the link checks. Items that are also rows in the tables above are marked.

### M1. Tables

- 1 838 table rows. 1 column mismatch: `class_2/4_home_work.md:7` (1 cell where the table has 5). It is a row above.

### M2. Index link text vs page H1

11 differences, in two groups:

- The H1 carries an attribute suffix that the index link does not: `class_4/7_basic_assim.md` (`{: #basic-assim-y}`), `class_6/3_masc_uu.md` (`{: #declension-of-u-masc}`), `class_7/2_fem_aa.md` (`{: #feminine-nouns-ending-in-a}`). Each is reported twice, from the class index and from `index.md`. These are not defects.
- The page has no H1: `class_4/11_root_as.md`, `class_4/12_root_huu.md` (also twice each). Rows above.
- `class_1/index.md:47`: link text `Basic Anki Decks`, H1 `Anki Decks` (`../../anki/index.md`).

### M3. Footnotes

- 28 references, 28 definitions, numbered across the whole folder. No reference without a definition and no definition without a reference.

### M4. Stray characters, headings, whitespace

- Cyrillic: `class_2/4_home_work.md` lines 5, 6 and 7 (a Russian gloss column). Row above.
- No or late H1: `class_4/11_root_as.md`, `class_4/12_root_huu.md`.
- Trailing space: `class_11/3_adj.md:5`, `class_3/11_histor_pr.md:3`, `class_4/7_basic_assim.md:43`.
- No final newline: `class_14/5_home_work.md`, `class_3/10_root_8.md`.
- Lines with a double space: 179.
- No tab, NBSP, zero-width or non-NFC character was reported.

### M6. Convention counts

| Item | Total | Where |
| --- | --- | --- |
| `ṁ` | 2 | class 2 |
| straight `'` | 23 | classes 1, 3, 5, 10, 11, 13, 14 (9 in class 5) |
| curly `’` | 44 | classes 1–8, 10–13 |
| curly `‘` | 4 | classes 2, 4, 11 |
| straight `"` | 34 | classes 5–8, 10, 12, 14 (10 each in classes 8 and 10) |
| curly `“”` | 316 | all classes and the index |
| `<br>` | 784 | classes 2–14 |
| `...` | 13 | classes 3, 8, 11, 12, 14 |
| `…` | 38 | most classes |
| ` - ` | 62 | most classes (15 in class 1, 11 in class 3) |
| `–` | 46 | most classes (14 in class 4) |
| `—` | 9 | classes 3, 6, 8, 10, 11 |
| `Pāli` | 125 | all classes |
| `Pāḷi` | 12 | one per class from class 2 on (a book title) |
| `{:` | 78 | all classes |
| `>` | 291 | classes 3–8, 11, 13, 14 |
| `→` | 0 | |
| `lit.` | 19 | classes 2–5, 8, 10, 11, 13, 14 |
| `lit:` | 0 | |
