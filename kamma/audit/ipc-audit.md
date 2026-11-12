# IPC audit — `docs/ipc/`

Date: 2026-11-12 (started 2026-11-10)
Scope: all 136 Markdown files under `docs/ipc/` (index + classes 16–28, 8 437 lines).
No file in `docs/` was modified. This is a findings list only.

## Method and limits

| Check | How | Result |
| --- | --- | --- |
| Full read of every file | Line by line. Classes 16–27 and `index.md` by the main session; class 28 by a reader subagent | Done |
| Excerpt check | Script: every backtick excerpt in `Current` searched in the cited file within 2 lines of the cited line | 746 pass. 10 fail, all explained: they quote a second file or class that the row names without a line number |
| Sutta links (`s.dhamma.gift`) | `uv run python scripts/check_sutta_links.py docs/ipc` | 37 links / 23 pages, all pass |
| Other external links | HTTP status per URL | 1 dead: `class_28/3_home_work.md:17` (`…/pali-class/pali-class-adv.html`, 404) |
| Local links and `#anchors` | Scripted | All resolve |
| Index titles vs page H1 | Scripted | 24 mismatches, one pattern (see Mechanical detail, M1) |
| Table column counts, footnotes | Scripted | 2 one-cell rows (`class_18/11_ex.md:11`, `:24`); footnote ids 1–23 consistent |

Not verified:

- Pāli forms were judged from my own knowledge, not from the DPD database. Anything with confidence below 8 needs a DPD lookup before it is changed. No DPD lookup was run.
- Kaccāyana sutta numbers and wording were checked from memory only.
- The link checker proves the URL and anchor exist, not that the quoted sentence is in that sutta.
- Frequency counts (class 21, class 28) were not recomputed.
- Rendered output (site, PDF, DOCX) was not built.
- Exercises and keys (`ipc_ex`, `ipc_key`) are out of scope.
- Class 28 findings are the subagent's; I checked that their excerpts exist, not their judgement.

Paths below are relative to `docs/ipc/`. In `Current`, `\|` is a table pipe in the source.

## Summary

| Category | index + 16 | 17 | 18 | 19 | 20–21 | 22–23 | 24–25 | 26–27 | 28 | Total | Conf. ≥ 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A. Pāli and grammar content errors | 3 | 10 | 6 | 5 | 4 | 9 | 7 | 9 | 19 | 72 | 41 |
| B. Tables, paradigms and lists that disagree with each other or themselves | 9 | 4 | 3 | 5 | 7 | 7 | 10 | 7 | 9 | 61 | 30 |
| C. Translation and gloss problems | 13 | 4 | 7 | 7 | 2 | 7 | 7 | 7 | 6 | 60 | 17 |
| D. English typos and grammar | 10 | 8 | 9 | 9 | 11 | 9 | 8 | 5 | 13 | 82 | 56 |
| E. Markdown defects that affect rendering | 3 | 3 | 8 | 3 | 6 | 3 | 8 | 3 | 4 | 41 | 36 |
| F. Convention drift | 17 | 18 | 13 | 12 | 18 | 13 | 13 | 8 | 9 | 121 | 85 |
| G. Links | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| H. Data to re-verify (forms, references, counts) | 6 | 5 | 6 | 4 | 7 | 8 | 8 | 8 | 3 | 55 | 2 |
| **Total** | **61** | **52** | **52** | **45** | **55** | **56** | **61** | **47** | **63** | **492** | **267** |

Overall confidence: 9/10 that the quoted text is where the row says (scripted). 8/10 for categories D, E, F (visible in the source). 6–7/10 for A, B, C, H as a group, because no Pāli form was checked against DPD; use the per-row score.

## Decisions for the owner

- Is `# Homeless work` intentional? It is the title of all 13 IPC home-work pages and of the BPC ones.
- Are `<br>` tags in table cells acceptable under the "no raw HTML" rule? 76 lines in `docs/ipc` use them and the PDF script handles them. Same question for `{: .align-right }` in `class_20/5_ex.md`.
- `Pāli` (53 times) or `Pāḷi` in running text.
- One term for the `-tvā`/`-ya` form: `ger.`/gerund (class 18) or `abs.`/absolutive (classes 17, 24).
- One style for Kaccāyana citations (five styles are in use, see F).
- UK or US spelling.
- The correct URL for the dead link in `class_28/3_home_work.md:17`.

## A. Pāli and grammar content errors

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_16/4_vowel_2.md:19 | `vā paro asarūpo.` | Kaccāyana 13 reads `asarūpā` (ablative) | `vā paro asarūpā` | 8 |
| class_16/7_vowel_5.md:49 | `**ī**sī` / `mah**e**sī` | Word for "sage" is `isi`; `mahā + isi > mahesi`. `mahesī` = chief queen. Heading `ā…ī > e` then also wrong for this example | `mah**ā** + **i**si > mah**e**si` under `ā + i > e` | 8 |
| class_16/10_vowel_8.md:69 | `**d**iṭṭhi` / `sa**n**diṭṭhi` | Not an insertion between two vowels (follows consonant d), contradicts the rule on line 5; bold on `d` marks a consonant as the "second vowel" | Remove, or move to niggahīta sandhi (`saṃ + diṭṭhi`) | 7 |
| class_17/5_cons_3.md:15 | `pātimokkañ’ca saṃvaro` | Verse (Dhp 185 / DN 14) reads `pātimokkhe ca saṃvaro`; `pātimokka` also lacks `kh` | `pātimokkhe ca saṃvaro` | 9 |
| class_17/5_cons_3.md:21 | `diṭṭasute sīlavate mute vā` | Snp 4.5 reads `diṭṭhe sute`; `diṭṭa` lacks `ṭh` | `diṭṭhe sute sīlavate mute vā` | 9 |
| class_17/7_cons_5.md:3 | `When **ti** follows a vowel, it becomes **cc**` | Direction reversed: `ti` becomes `cc` when a vowel follows it (all six examples) | `When **ti** is followed by a vowel` | 9 |
| class_17/3_cons_1.md:151 | `pat**i**` … `paṭi**pph**arati` | `pati` in column 1, `paṭi` in the result | `paṭ**i**` | 9 |
| class_17/3_cons_1.md:167 | `a**bbh**aya` | Normal form is `abhaya` (no reduplication) | DPD lookup; replace example | 7 |
| class_17/3_cons_1.md:47 | `eka**ggh**ana` | Normal form is `ekaghana` (Dhp 81) | DPD lookup | 7 |
| class_17/8_nig_1.md:11; 17_nig_10.md:9 | `niggahitaṃ` / `niggahitañ’ca` | Short `i`; the class title and all prose use `niggahīta` | verify against Kaccāyana 30, 37 | 7 |
| class_17/1_alphabet_analys.md:25 | `**8 Semi-Vowels (antaṭṭha)**` | `antaṭṭha` covers y r l v (ḷ); s, h, ṃ are not semi-vowels | `8 ungrouped (avagga)` or split | 7 |
| class_17/9_nig_2.md:30 | `**g**ha` | `gha` is not a word; bold on `g` not `gh` | `√han > gha` or other example | 7 |
| class_17/10_nig_3.md:18 | `m. masculine gender` | `pulliṅga` is nt. (`liṅga` nt.) | DPD lookup | 7 |
| class_18/5_as_sa.md:17 | `vi + √cit + cit \> cikit + sa + ti` | `vicikicchati` is from `√kit` (as line 16 and 6_as_sum.md:11 `ciki**t s**a`); `cit + cit > cikit` is not a reduplication of √cit | `vi + √kit + kit \> cikit + sa + ti` | 8 |
| class_18/6_as_sum.md:15 | `ni √sa**j** **y**a \| nisa**jj**a` | `nisajja` = `ni + √sad + ya` (d + y), not j + y | use `vi √bha**j y**a \| vibha**jj**a` | 8 |
| class_18/9_ex.md:19 | `nī + √sar + ta \| nissaṭa` | Prefix is `nir`/`nis`, not `nī` | `nir + √sar + ta` | 8 |
| class_18/9_ex.md:11 | `duppativijjha` | `pati` should be `paṭi` in the result | `duppaṭivijjha` | 8 |
| class_18/8_as_misc.md:25–26 | `pati` … `paṭi**gg**aheti`, `paṭi**ss**uṇāti` | Prefix column `pati`, result `paṭi`; `paṭiggaheti` not confirmed (usual pr. `paṭiggaṇhāti`) | align; DPD lookup | 7 |
| class_18/4_as_na.md:21 | `dur + √var + na \| dubba**ṇṇ**a` | `dubbaṇṇa` = `dur + vaṇṇa` (noun), not a `-na` participle of √var | replace example | 7 |
| class_19/4_tap.md:93 | `## sattāmī tappurisa` | Misspelt; line 147 has `sattamī` | `sattamī` | 10 |
| class_19/4_tap.md:45 | `kathin**assa** dussaṃ \> kathin**a**dussaṃ (cloth **for** the Kathina)` | Pāli is `kaṭhina` (retroflex) | `kaṭhin…`, `Kaṭhina` | 9 |
| class_19/2_kamm.md:125 | `pa + vagga \> pavagga (group of labial consonants)` | `pavagga` is "the p-group" (letter name + vagga), not prefix `pa` + noun; wrong example for `pa-ādi-pubba-pada` | replace (e.g. `pa + vacana > pāvacana`) | 9 |
| class_19/2_kamm.md:77, 79 | `tathāgato *viya* sīho`, `buddho *viya* nāgo` | Analysis reversed: the comparison is the second member, so `sīho viya tathāgato` (Tathāgata like a lion) | swap | 8 |
| class_19/4_tap.md:73 | `het**unā** samuppanna` | `hetunā` is instrumental, listed under ablative | `het**uto**`/`het**usmā**` or move to tatiyā | 8 |
| class_20/2_bahub.md:101 | `kammadāraya` | Misspelt | `kammadhāraya` | 10 |
| class_20/2_bahub.md:95 | `musāvadaṃ` | Short `a` | `musāvādaṃ` | 9 |
| class_21/3_pass_refl.md:31 | `Sanskrit - vācya**te**` | Sanskrit passive of √vac is `ucyate` | `ucya**te**` | 9 |
| class_20/2_bahub.md:13, 17, 23 | `**bahubbīhī** janapado` | Long `ī`; the compound is `bahubbīhi` (line 7, line 19 `bahubbīhismiṃ`) | `bahubbīhi` | 7 |
| class_22/3_root_groups.md:7 vs 9 | `bhuvādigaṇa` vs `bhūvādigaṇa` | Two spellings two lines apart | `bhūvādigaṇa` | 9 |
| class_22/3_root_groups.md:74 | `tiṭṭhā \| tiṭṭhāti` | Present is `tiṭṭhati` (4_irreg_base.md:26 has `tiṭṭha \| tiṭṭhati`) | `tiṭṭha \| tiṭṭhati` | 9 |
| class_22/3_root_groups.md:56 | `transformed to **ay** and **av** according to **vuddhi**` | `i > e > ay`, `u > o > av` is guṇa; vuddhi gives `āy`/`āv` | `guṇa` | 8 |
| class_22/3_root_groups.md:157 | `√ghaṭ \| e \| ghāte \| ghāteti \| kills, slays` | `√ghaṭ` = strive (`ghaṭeti`); `ghāteti` is from `√ghāt`/√han | `√ghāt` | 8 |
| class_22/3_root_groups.md:100; class_23/11_upa.md:8; 17_pari.md:14 | `√ādā` | Prefix `ā` inside the root sign (also class_18/9_ex.md:10) | `ā + √dā` | 8 |
| class_23/13_nii.md:7 | `√veth` | Root is `√veṭh` (17_pari.md:8) | `√veṭh` | 9 |
| class_23/13_nii.md:16 | `√yā \| to go \| nīyati \| departs, leaves` | `nīyati` is the passive of `neti`; "departs" is `niyyāti` | `niyyāti` | 8 |
| class_23/20_mixed_pref.md:10 | `anu + pa \| √ikkh \| to look \| anupekkhati` | `anupekkhati` = `anu + upa + √ikkh` | `anu + upa` | 8 |
| class_23/22_dur_su_nir.md:14 | `√var \| to cover \| dubbaṇṇa` | `dubbaṇṇa` = `dur + vaṇṇa` (same issue as class_18/4_as_na.md:21) | `vaṇṇa` | 7 |
| class_24/5_caus_pass.md:24 | `ñāpē` | `ē` with macron is not a Pāli letter | `ñāpe` | 10 |
| class_24/4_irreg_caus.md:22 | `√nas \| to be lost \| \*e \| nessa \| nessati \| will destroy` | `nessati` is the future of `neti` (√nī); causative of √nas is `nāseti` | verify, replace | 7 |
| class_25/5_taddh_2.md:87 | `navā \| + \*ika \| n**ā**v**ika**` | Boat is `nāvā` | `nāvā` | 9 |
| class_25/5_taddh_2.md:62 | `apihā \| + ālu \| apih**ālu** \| not full of envy` | Analysis is `a + pihā + ālu`; `apihā` is not the base | `pihā \| + ālu \| pihālu \| full of envy` or show `a +` | 8 |
| class_25/5_taddh_2.md:175 | `gaṅga \| + \*eyya` | River is `gaṅgā` | `gaṅgā` | 8 |
| class_25/5_taddh_2.md:217, 220 | `from Kasi`, `from Kasi village` | Diacritic missing (`Rājagaha` has it on line 218) | `Kāsi` | 9 |
| class_25/2_nouns.md:24 | `√ādā \| to take, eat \| + na \| ādāna \| eating` | `ādāna` = `ā + √dā + ana`, "taking, grasping"; `√ādā` again has the prefix inside the root sign | fix | 7 |
| class_26/3_state.md:59 | `**ā**ṇaṇ**ya**` | First nasal should be dental: `anaṇa > ānaṇya` | `**ā**naṇ**ya**` | 9 |
| class_26/3_state.md:81 | `**a**dhipat**eyya**` | Standard form is `ādhipateyya` (the `\*` suffix lengthens) | `**ā**dhipat**eyya**` | 8 |
| class_26/1_having.md:95 | `sati \| + mant \| satī**mant**` | Regular form is `satimant`; `satīmant` is metri causa (class_17/5_cons_3.md:31) | `sati**mant**` | 8 |
| class_27/2_kicca.md:132 | `√labh \| + \*ya \| la**ddha** \| to be obtained` | `laddha` is the pp (`labh + ta`, class 18); ptp is `labbha` | `la**bbha**` | 9 |
| class_27/2_kicca.md:123 | `√bhu` | Root is `√bhū` | `√bhū` | 9 |
| class_27/3_kita.md:78 | `√sikh` | Root is `√sikkh` (2_kicca.md:53) | `√sikkh` | 9 |
| class_27/2_kicca.md:108 | `√raj \| + aṇīya \| sār**aṇīya** \| to be desired` | `sāraṇīya` is not from √raj (√sar "remember" / `sārāṇīya`) | DPD lookup, replace | 7 |
| class_27/2_kicca.md:90, 127, 174 | `√ghaṭ` … `saṅghāt**aniya**`, `gha**cca**`, `ghāte**tāya**` | `ghacca`, `ghātetāya` are from `√ghāt`/√han (same issue as class_22/3_root_groups.md:157); `saṅghātaniya` has dental `t` against retroflex root | DPD lookup | 7 |
| class_27/2_kicca.md:143 | `√saṃk` | Root usually written `√saṅk` | `√saṅk` | 7 |
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

## B. Tables, paradigms and lists that disagree with each other or themselves

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_16/10_vowel_8.md:5 | `**y v m d n t r l**` | List has `l`, table section is `ḷ`; section `h (very rare)` is not in the list (also line 112 and ref table line 18) | Align list and sections (`ḷ`, add `h`) | 8 |
| class_16/9_vowel_7.md:25 | `s**va**haṃ` | Same pair `so + ahaṃ` gives `svāhaṃ` on line 5; `svahaṃ` (short) doubtful; also in 12_vowel_ref_table.md:41 | Verify in DPD; likely `svāhaṃ` | 6 |
| class_16/12_vowel_ref_table.md:17 | `**o** \| a+e` | `a + e > o` is not taught in any lesson and absent from the Alternative table (col a, row e = `e`) | Verify; probably remove | 8 |
| class_16/12_vowel_ref_table.md:17 | `**ū** \| ū\<i` | `ū + i > ū` has no lesson example and the Alternative table cell (col ū, row i) is empty | Align the two tables | 7 |
| class_16/12_vowel_ref_table.md:7 | `**yā** \| i+a` | Lessons give `i+a > ya`, `i+ā > yā`, `ī+a > yā`; Alternative table (col i, row a) has no `yā` | Align the two tables | 6 |
| class_16/12_vowel_ref_table.md:14 | `**ā** \| ā\<a` | Lesson (5_vowel_3.md:36) teaches `ā>+a` (elide + lengthen); table lists `ā<a` and omits `ā>+a` | Verify notation | 6 |
| class_16/12_vowel_ref_table.md:9 | row starts with two empty cells | Empty cells split the **a** column (`i>a` row follows the gap) | Move `i\>a` up, keep column contiguous | 8 |
| class_16/12_vowel_ref_table.md:5–13 | `a\>a`, `a\<i`, `ā\>+i`, `i+\<a` | Notation (`>`, `<`, `+`) is never explained; no legend | Add one-line legend | 8 |
| class_16/13_home_work.md:26 | `**na-** \| ind \| neg \| not[^2]` | `na-`/`ahaṃ` rows appear twice (lines 20–21 and 26–27); footnote text does not clearly explain the repetition | Clarify or drop duplicate rows | 7 |
| class_17/1_alphabet_analys.md:49, 62 | `Unvoiced<br>(*aghosa*) \| Voiced<br>(*ghosavant*) \| \| \|` | Header cells do not sit over their columns: `Voiced` is above the unvoiced aspirates column | reorder cells (`Unvoiced \| \| Voiced \| \| \|`) | 9 |
| class_17/8_nig_1.md:29 | `catutthasmi**ṃ** \| \| **ṭh**āne` | Row sits in the dental `th` slot but repeats `ṭh` (line 26) | example with `th` | 9 |
| class_17/9_nig_2.md:38 | `**ch**avi` … `sa**ñ**chavī` | `chavi` vs `chavī` | align | 8 |
| class_17/2_cons.md:5–11 | `three basic types` | Lists 3 types; the class then gives 5 possibilities (incl. so > sa, ti > cc) | reword | 7 |
| class_18/8_as_misc.md:15 | `sat \| dhamma \| t + dh \> ddh \| saddhamma` | Row is in the `prefix \| root` table for ud-/dur-/nir-; `sat` is not a prefix, `dhamma` not a root | move out or relabel | 8 |
| class_18/10_irreg_masc.md:100 vs 102 | `ra**ññaṃ**<br>rāj**ānaṃ**<br>rāj**ūnaṃ**` vs `ra**ññaṃ**<br>rāj**ūnaṃ**<br>rāj**ānaṃ**` | Dat pl and gen pl list the same forms in different order | same order | 8 |
| class_18/10_irreg_masc.md:44 | `**manase**` | Bold marks forms that explain the Pāli; Pāli dat is `manaso` (from `manasaḥ`, not bold), `manase` has no Pāli reflex in the table above | bold `manasaḥ` instead | 7 |
| class_19/2_kamm.md:49, 51 | `\> sukatadukkaṭānaṃ`, `\> manāpāmanāpaṃ` | Result carries a case ending (gen. pl., acc.) while inputs are stems; line 47 gives the stem | stem forms | 7 |
| class_19/4_tap.md:99 | `guh**āyaṃ** āsaya \> guhāsayaṃ` | Result ends in `-ṃ`, input `āsaya` | `guhāsaya` | 7 |
| class_19/6_comp_rules.md:15, 19 | `masculine stems ending in **-ū, ā, ī**` / `cattālīsā + danta` | `cattālīsā` is a feminine numeral, not a masculine stem | reword rule | 7 |
| class_19/6_comp_rules.md:37 | `dīgha + ratta + aṃ` | Rule 7 is about `ratti > ratta`; example starts from `ratta` | `dīgha + ratti \> dīgharattaṃ` | 7 |
| class_19/6_comp_rules.md:45 | `mātar + pitu \> māt**ā**pitaro` | `pitu` beside `pitar` (lines 43, 47); `mātā-` form not in the rule's list | `mātar + pitar` | 8 |
| index.md:66–67 | Class 21 list starts with `Three Voices` | `class_21/1_review_verbs.md` (Review of Verbs) is missing from the root index; it is in `class_21/index.md:3` | add entry | 9 |
| class_20/1_abya.md:42 | `**pura** \| before \| **aruṇā** \| … \| **purāruṇā**` | First member should be `purā` (list on line 71 has `pure`) | `purā` | 7 |
| class_20/4_change_comp.md:11 | `go \| cow, cattle \| gavo \| jaraggavo` | Column gives the compound form (stem) elsewhere; here nominative `gavo` | `gava \| jaraggava` | 7 |
| class_20/2_bahub.md:111 vs 129, 135, 141, 143 | `adjective **-a ending**` / `bahubhāṇī`, `cirappavāsī`, `ekavihārī`, `kālavādī` | Group 1 is defined as `-a` ending; four examples end in `-ī` | reword rule or move examples | 7 |
| class_21/6_opt.md:22 | `forms shown in italics here and further in the conjugation tables only exist in grammar books` | Later tables called theoretical (7_perf.md attanopada, 9_aor.md:35–37) are not italic | italicise or reword | 7 |
| class_21/8_imperf.md:7 | `events which happened before yesterday` | Line 5 translates the sutta as `starting from yesterday` | `from yesterday backwards` | 8 |
| class_21/6_opt.md:20, 31 | `*damemase*`, `*nīyemase*` | Ending not in the summary (10_sum.md:9, 46 give only `eyyāmhe`) | verify | 6 |
| class_22/2_cond.md:29 | `abhav**issiṃsu**` | Class 21 summary (10_sum.md:19, 51) gives `ssisu` | verify, align | 8 |
| class_22/3_root_groups.md:56, 62 | `end in i ī u ū` / `√pā \| a \| p**iva**` | `√pā` ends in `ā` and `piva` is not an ay/av base | move to irregular bases (it is there, 4_irreg_base.md:23) | 8 |
| class_22/3_root_groups.md:41 | `the verbal terminations are added directly to the root` | Table still shows the sign `a` in column 2 | reword or drop `a` | 7 |
| class_23/9_ava.md:11 vs class_22/3_root_groups.md:131 | `√dhu` vs `√dhū` | Same root, two spellings | one form | 7 |
| class_23/17_pari.md:7 vs class_18/3_as_ta.md:88 | `√khaṇ` vs `√khan` | Same root, two spellings | one form | 8 |
| class_23/21_nipata.md:67–68 | `khatvā`, `khata` | Not words; base is `katvā`, `kata` (`puras + kata`) | `katvā`, `kata` | 7 |
| class_23/13_nii.md (whole) | `# nī-` | 8 of 10 examples show `ni` + doubled consonant (`nibbindati`, `nikkhamati` …), i.e. `nir-`; 22_dur_su_nir.md has a separate `nir-` said to be "not used with verbs" | reconcile `nī-`/`nir-` | 6 |
| class_24/6_app.md:44 | `\| \| **Masculine** \| **Feminine** \| **Neuter** \| \| \| \|` | Seven columns (sg/pl ×3) but the three labels sit over columns 2–4, so `Feminine` is above masc. pl. and `Neuter` above fem. sg.; no sg/pl row | `\| \| **Masculine** \| \| **Feminine** \| \| **Neuter** \| \|` + sg/pl row | 9 |
| class_24/6_app.md:49–52 | `dass**āvissa**` only in nt. gen.; `dass**āvito**` only in nt. abl.; `dass**āvini**` only in masc. loc. | Masc. and nt. columns should match in oblique cases but each lists a different set; no voc. row (class 18 tables have `8.voc`) | align | 8 |
| class_24/2_irreg_pass.md:25–28 | `(ī)ya` (√ci, √ji) vs `(i)ya` (√lu, √su) | Same lengthening, two notations; √su appears again on lines 51–52 with plain `ya` | one notation | 7 |
| class_24/5_caus_pass.md:61 vs 63 | `bhāvīya \| bhāvīyati` vs `**bhāviyamānā**` | Long `ī` in the table, short `i` in the sutta example and in 3_caus.md:55 | align | 7 |
| class_24/4_irreg_caus.md:29 | `sivve \| visibbeti` | Base `sivve`, verb `sibbe-` | `sibbe` | 8 |
| class_24/2_irreg_pass.md:93–94 | `√**ph**ar … **phu**ṭa`, `√**bha**r … pa**bhu**ti` | Listed under `va \> vu` but are `pha > phu`, `bha > bhu` | separate heading or note | 6 |
| class_25/2_nouns.md:32 | `√sad \| … \| + \*a \| pasāda` | Prefix `pa` not shown (line 21 has `pa + √vatt`) | `pa + √sad` | 9 |
| class_25/4_taddh.md:23–35 | `1.  sāmañña` … `1.  apacc’attha` … `1.  saṅkhyā` / `2.  bhāva` / `3.  abyaya` | Source numbers 1,1,1,1,1,2,3 show a lost nesting (four sub-types under sāmañña); Markdown renders a flat 1–7 | nest the sub-items | 8 |
| class_25/5_taddh_2.md:1 | `# \*a (dyed with)` | The page that holds all taddhita suffixes has the first suffix as its H1, so indexes list the page as `\*a (dyed with)` (index.md:120, class_25/index.md:7) | give page a title, make suffix an H2 | 9 |
| class_25/1_deriv.md:7 | `These suffixes are called **Derivatives,**` | Derivatives are the resulting words, not the suffixes (line 9 uses it that way) | reword | 6 |
| class_26/3_state.md:67 vs class_23/22_dur_su_nir.md:62 | `kusīta \| + \*ya \| k**o**sa**jja**` vs `ku \| √sad + ya \| kosajja` | Two different derivations of `kosajja` in the course | keep `kusīta + \*ya` | 8 |
| class_26/4_ind.md:3 vs 7–15 | `## khattuṃ (times)` vs `+ kkhattuṃ` | Heading and table spell the suffix differently | one form | 8 |
| class_26/1_having.md:27, 31 | `### ila` / `kumbh**īla**` | Suffix `ila`, result `īla` | note or separate | 7 |
| class_26/1_having.md:45, 66, 80 | `### tana (belonging to)`, `### tara (comparative adjectives)`, `### tama (superlative adjectives)` | Not possession, but placed under `## Having & Possessing` | own H2 | 6 |
| class_27/1_kitaka.md:15 vs 2_kicca.md:161 | `\*tya` vs `## tya (ptp)` | Star present/absent; likewise `## eyya` vs `\***ya** becomes **eyya**` | one form | 7 |
| class_27/2_kicca.md:35 | `√gah \| ṇhā \| gahe` | Sign `ṇhā` does not give base `gahe` | `\*e`? verify | 7 |
| class_27/3_kita.md:12 | `√gal \| gaḷa` | Root `l`, base `ḷ` | one form | 7 |
| `class_28/1_kita_1.md:23-24` | `\| 15 \| **+ \*ana** \| 151 \|` / `\| 16 \| **+ \*ī** \| 157 \|` | Ranking table otherwise descending; 157 > 151. Sections (`\*ana` at `:570`, `\*ī` at `:605`) follow the same wrong order. | Swap rows 15 and 16 (and the sections), or correct a count | 9 |
| `class_28/1_kita_1.md:256-262` | `1066` / `110` / `105` / `20` / `**1300**` | Parts sum to 1301, one more than the total. | Recount | 10 |
| `class_28/1_kita_1.md:80-85`, `:154-159`, `:231-236`, `:298-303`, `:407-412`, `:643-649` | totals `**1684**`, `**1442**`, `**1395**`, `**1162**`, `265`, `139` | Parts sum to 1660, 1438, 1393, 1161, 264, 136. If minor categories were dropped no table says so; the other eight tables add up exactly. | Add an "other" row or recount | 9 |
| `class_28/1_kita_1.md:331-333`, `:553-555`, `:695-697` | `## māna`, `## anā`, `## \*aka` | Every other top-18 section has description + count table + examples. *māna* has no count table or examples; *anā* has no description or count table; *\*aka* has no description. | Complete to the common pattern | 8 |
| `class_28/1_kita_1.md:566`, `:568` | `pa √atth \| to wish \| … patth**anā** \| aspiration` / `pa √atth \| to wish for \| … patth**anā** \| intention, wish` | Same word listed twice in one table. | Merge | 9 |
| `class_28/1_kita_1.md:672-673` | `√kas \| to drag \| **+ i** \| kas**i** \| farming` / `√kas \| to plough \| **+ i** \| kas**i** \| farming` | Duplicate row. `:535` gives the root once as "to drag, plough". | Merge | 9 |
| `class_28/1_kita_1.md:181`, `:358`, `:397`, `:590`; `class_28/2_kita_less.md` throughout (e.g. `:20`, `:35`, `:37`, `:70`, `:73`, `:126`, `:127`, `:130`, `:143`, `:162`, `:179`, `:186`, `:200`, `:227`, `:249`, `:273`, `:339`, `:351`, `:392`, `:407`, `:439`, `:492`, `:495`, `:496`, `:516`, `:528`) | e.g. `√sī \| to sleep \| **+ \*a** \| ās**aya**`; `√khā \| to tell \| **+ tar** \| akkhā**tar**` | `1_kita_1.md` normally writes prefixes before the root (`ā √jīv`, `pati ud √pad`, `na ni √vis`). These rows, and every prefixed word in `2_kita_less.md`, omit them, so root + suffix does not give the stated word. | Add prefixes in column 1 | 8 |
| `class_28/1_kita_1.md:229` vs `:231-236` | `a tiny group of **passive present participles**, **nouns** and **adjectives**` | "Passive present participles" has no row in the count table and no example. | Add or drop | 6 |
| `class_28/2_kita_less.md:367`, `:371` | `**+ ala neuter nouns and adjectives**` … `kul**ala** \| eagle; hawk` | *kulala* is masculine; no neuter noun in the table. `:433` has `√kur … kurara \| eagle` as masculine. | "masculine nouns and adjectives" | 7 |

## C. Translation and gloss problems

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_16/3_vowel_1.md:60 | `these \| five \| these five` | Glosses swapped: `pañca` = five, `ime` = these | `five \| these \| these five` | 10 |
| class_16/3_vowel_1.md:152 | `indeed \| thus \| thus indeed` | `etaṃ` = this, not thus | `indeed \| this \| this indeed` | 9 |
| class_16/3_vowel_1.md:208 | `my \| these are \| these are my` | `atthi` is singular "there is" | `my \| there is \| there is my / I have` | 8 |
| class_16/3_vowel_1.md:110 | `ignorance \| defilement` | `āsava` is "effluent" on lines 47, 51 of the same file | One gloss for `āsava` | 8 |
| class_16/3_vowel_1.md:165 | `conscience \| shame in wrongdoing \| conscience and concern` | `ottappa` glossed two ways in one row | One gloss | 7 |
| class_16/3_vowel_1.md:224–230 | `only` | `eva` = "only" here, "just" in the rest of the file; `pubbeva` "only before" is odd | `just`; `pubbeva` = "previously" | 6 |
| class_16/4_vowel_2.md:44 | `she \| just \| just that` | Gloss of `sā` changes inside the row | `just she` or `that \| just \| just that` | 7 |
| class_16/5_vowel_3.md:32 | `with \| meaning \| in meaning` | `sāttha` = with meaning, meaningful | `with meaning` | 8 |
| class_16/5_vowel_3.md:86 | `whoever \| here \| whoever here` | `yāni` is nt. pl. "whatever (things)", not "whoever" | `whatever \| here \| whatever here` | 9 |
| class_16/5_vowel_3.md:52 | `unmindful \| not aware` | `asati`, `asampajañña` are nouns | `unmindfulness \| lack of awareness` | 6 |
| class_16/8_vowel_6.md:51 | `lit. who for whom` | `assa` = for him | `lit. who for him` | 8 |
| class_16/9_vowel_7.md:26 | `then \| I \| so I` | `so` = that/he (cf. 5_vowel_3.md:70 `that \| I \| that I`) | `that \| I \| that I` | 7 |
| class_16/10_vowel_8.md:37, 106 | `good wake up` | Unidiomatic; `uṭṭhita` glossed `stood up` (37) and `got up` (106) | `well risen`; one gloss | 7 |
| class_17/3_cons_1.md:20 | `pr. comes out` | `abhikkamati` = goes forward, advances | `pr. goes forward` | 7 |
| class_17/9_nig_2.md:51 | `nt. standing still` | `saṇṭhāna` = shape, configuration | DPD lookup | 7 |
| class_17/13_nig_6.md:26 | `whichever this` | `yadidaṃ` = namely, that is | `namely; lit. which this` | 7 |
| class_17/15_nig_8.md:17 | `buddha’s teaching` | `buddhānaṃ` is gen. pl.; lower-case b | `teaching of the Buddhas` | 8 |
| class_18/2_as_ya.md:58 | `pr. is free` | Passive: line 27 has `(is freed)` | `pr. is freed` | 8 |
| class_18/10_irreg_masc.md:62 | `fire state` | `dhātu` = element | `fire element` | 8 |
| class_18/1_phonetic.md:23 vs 3_as_ta.md:78 | `(pp. known)` vs `pp. woken up` | `buddha` glossed two ways | one gloss | 6 |
| class_18/2_as_ya.md:144 | `pr. shines` | `dibbati` = plays, amuses oneself | DPD lookup | 6 |
| class_18/2_as_ya.md:113 | `pr. is broken` | `ruppati` = is afflicted, is deformed | DPD lookup | 6 |
| class_18/4_as_na.md:20 | `pp. completed` | `ciṇṇa` = practised, performed | DPD lookup | 6 |
| class_18/10_irreg_masc.md:29 | `metrics` | `chandas` = metre, prosody | `metre` | 6 |
| class_19/1_comp.md:43 | `(restrained **and** controlled **by** the precepts)` | `pātimokkha-saṃvara-saṃvuta` = restrained by the restraint of the Pātimokkha; no "and" | fix | 7 |
| class_19/4_tap.md:47 | `(worthy **for** the King)` | Idiom | `worthy **of** a king` | 7 |
| class_19/4_tap.md:63 | `(wanting **to** distract)` | `cāveti` = make fall away | DPD lookup | 6 |
| class_19/5_dvanda.md:55 | `shame and fear` | Third gloss of `hirottappa` in the course (class_16/3_vowel_1.md:165 has two others) | one gloss | 7 |
| class_19/5_dvanda.md:69 | `rites and rituals` | `sīla` + `vata` = precepts and observances | DPD lookup | 7 |
| class_19/5_dvanda.md:54 | `pain and stress` | `domanassa` = mental distress | `pain and distress` | 6 |
| class_19/4_tap.md:89 | `(destruction **of** the defilements)` | `āsava` gloss drifts (effluent / defilement) across classes 16, 19 | one gloss | 7 |
| class_20/1_abya.md:29 | `**tato** \| from` | `tato` = from that (line 73 has `from that`) | `from that` | 8 |
| class_20/1_abya.md:54 | `adhi- \| up, towards` | `adhi` = over, above | DPD lookup | 6 |
| class_22/3_root_groups.md:93 | `vindati \| feels, likes` | `vindati` = finds, gains | DPD lookup | 7 |
| class_22/4_irreg_base.md:48 | `paṭihaṅkhati \| will kill` | = will ward off, will repel | DPD lookup | 7 |
| class_23/9_ava.md:7 | `avajānāti \| denies` | = despises (class_16/10_vowel_8.md:46 `and despises`) | `despises` | 8 |
| class_23/9_ava.md:12 | `okappeti \| suspects` | = trusts, relies on | DPD lookup | 7 |
| class_23/14_pa.md:14 vs class_17/3_cons_1.md:75 | `is overcome; is anxious` vs `pr. contemplates, thinks` | `pajjhāyati` glossed two ways | one gloss | 7 |
| class_23/21_nipata.md:51 | `pātukaroti \| appears, manifests` | Transitive: makes appear, reveals | `makes manifest` | 8 |
| class_23/22_dur_su_nir.md:46 | `nigghosa \| silent` | `nigghosa` usually = noise, shout | DPD lookup | 7 |
| class_24/1_pass.md:77 | `will be free` | Passive | `will be freed` | 8 |
| class_24/2_irreg_pass.md:37 | `samanuyuñjiyati\* \| being cross-questioned` | Finite verb glossed as participle | `is cross-questioned` | 9 |
| class_24/5_caus_pass.md:72 | `nisīdāpīyati \| causes to be seated` | Causative passive = is caused to sit | `is caused to sit down` | 9 |
| class_24/2_irreg_pass.md:7 | `sandassiyamāna \| being seen together` | = being shown / instructed | DPD lookup | 7 |
| class_24/1_pass.md:47 | `√vad \| to speak \| … \| vajjati \| is played` | Gloss needs context (of a musical instrument) | `is played (music)` | 7 |
| class_25/2_nouns.md:45 | `māra \| death` | In the agent-noun table ("a person who does the action") | `killer; Māra` | 7 |
| class_25/5_taddh_2.md:19 | `from God Vishnu` | `vāsudeva` = son of Vasudeva | verify | 6 |
| class_26/1_having.md:50–51 | `belonging to ancient` | Ungrammatical gloss, twice | `ancient, of old` | 7 |
| class_26/3_state.md:62 | `brahman state, celibacy` | `brahmañña` = brahmin-hood; celibacy is `brahmacariya` | fix | 7 |
| class_26/3_state.md:99 | `t**ā**pas**a** \| austere state, ascetic` | `tāpasa` is a person, listed under "state of" | move or regloss | 7 |
| class_26/4_ind.md:51 | `amu**tra** \| in such place,` | = in that place, there; trailing comma | `in that place, there` | 8 |
| class_27/2_kicca.md:18 | `ga**ntabba** \| to be followed` | = to be gone (to) | `to be gone` | 7 |
| class_27/2_kicca.md:72 | `pāṭides**anīya** \| to cause to be pointed out` | = to be confessed; prefix `paṭi` not shown | fix | 7 |
| class_27/2_kicca.md:167 | `ma**cca** \| to be dead` | = mortal; lit. bound to die | `mortal` | 7 |
| `class_28/1_kita_1.md:587` vs `:598`; `class_28/2_kita_less.md:496` | `√i \| to come`; `parā √i \| to go`; `√i \| to come` | Same root glossed two ways. | "to go" throughout | 7 |
| `class_28/1_kita_1.md:73` | `suga**ta** \| going well` | *gata* is past: "gone well, well-gone". | "well-gone" | 7 |
| `class_28/1_kita_1.md:358` | `√sad \| to sink \| **+ na** \| pasan**na** \| believer` | "to sink" does not lead to "believer"; pa + √sad is "to be clear, pleased". | Adjust root gloss (and add `pa`) | 6 |
| `class_28/1_kita_1.md:445` | `āvar**aṇa** \| obstructed, blocked` | Adjective is active: "obstructing". `:428` glosses the noun as "obstacle". | "obstructing, blocking"; check DPD | 6 |
| `class_28/1_kita_1.md:657-661` | `ni √dhā \| to place`, `saṃ √dhā \| to place`, `pa ni √dhā \| to support`, `upa √dhā \| to support` | Same root, two glosses in adjacent rows. | One gloss | 7 |
| `class_28/2_kita_less.md:406` | `m**e**tt**ā** \| lit. friendliness` | Only a "lit." gloss, no primary meaning (compare `fire; lit. purifier`). | "loving-kindness; lit. friendliness" | 7 |

## D. English typos and grammar

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_16/2_vowel.md:11 | `Vowel Sandhi are :` | Space before colon | `are:` | 9 |
| class_16/3_vowel_1.md:7 | `and very common in Pāli` | Missing verb | `and is very common` | 9 |
| class_16/4_vowel_2.md:35 | `thus/”` | Stray slash + quote | `thus / ”` or `(end quote)` | 8 |
| class_16/7_vowel_5.md:70 | `not textual example` | Missing article | `not a textual example` | 8 |
| class_16/10_vowel_8.md:45 | `ca **m**avajānāti,` | Stray trailing comma | remove comma | 9 |
| class_16/12_vowel_ref_table.md:79 | `**1s letter**` | Typo | `**1st letter**` | 9 |
| class_16/12_vowel_ref_table.md:93, 95 | `meets **a** result can be` / `meets **i** result can be` | Missing "the" (first half of each sentence has it) | `the result can be` | 9 |
| class_16/12_vowel_ref_table.md:99 | `apostrophe( ’ )` | Missing space | `apostrophe ( ’ )` | 9 |
| class_16/12_vowel_ref_table.md:109 | `in **PTS** dictionary` | Missing article | `in the **PTS** dictionary` | 8 |
| class_16/13_home_work.md:11 | `to help you also use Buddha’s Words or SuttaCentral` | Run-on, missing full stop | `to help you. Also use …` | 9 |
| class_17/1_alphabet_analys.md:5 | `learn the alphabetical-order, it will` | Hyphen; comma splice | `alphabetical order; it will` | 8 |
| class_17/1_alphabet_analys.md:3 | `So each week there will be given a little more information.` | Awkward | `A little more information will be given each week.` | 7 |
| class_17/2_cons.md:3 | `consonant**. (or parts of a word)` | Parenthesis after the full stop | move inside sentence | 8 |
| class_17/7_cons_5.md:22 | `as you can see this mostly occurs` | No capital, comma, or full stop | fix | 8 |
| class_17/12_nig_5.md:18 | `**Counter-example:**` | Singular, four examples follow | `Counter-examples:` | 9 |
| class_17/13_nig_6.md:30 | `this is influenced by the Sanskrit **yad tad etad** and **tam** **etam** etc` | No capital / full stop; split bold | fix | 8 |
| class_17/15_nig_8.md:7 | `in verses` | Fragment on its own line | `…may be elided in verses.` | 8 |
| class_17/16_nig_9.md:31 | `with the meaning of a **like** or **as**` | Stray `a` | `meaning of **like** or **as**` | 9 |
| class_18/1_phonetic.md:7, 39, 83 | `Adaption` | Usual term is `Adaptation` | `Adaptation` | 6 |
| class_18/1_phonetic.md:39 | `changes from the influence of another consonant` | Preposition; sentence has no full stop (also lines 17, 45) | `under the influence` | 7 |
| class_18/1_phonetic.md:63 | `**Aspiration** an -h- is added` | No verb/punctuation between term and definition | `**Aspiration**: an -h- is added.` | 8 |
| class_18/1_phonetic.md:93 | `that can occur, let’s look` | Comma splice | full stop | 7 |
| class_18/7_mix_san.md:20 | `**Pāli1**` | Stray `1` (lost footnote marker?) | `**Pāli**` | 9 |
| class_18/8_as_misc.md:1 | `Another consonant assimilation` | Ungrammatical title (also index.md:45, class_18/index.md:10) | `Other Consonant Assimilations` | 8 |
| class_18/8_as_misc.md:3, 5 | `ud- ; dur- ; nir-` | Space before semicolons | `ud-, dur-, nir-` | 8 |
| class_18/8_as_misc.md:19 | `prefix(s)` | Plural | `prefix(es)` | 8 |
| class_18/3_as_ta.md:7; 4_as_na.md:3 | `**neuter nouns ending** in -ta, … etc` | `ending` inside the bold (not in parallel phrases); `etc` without full stop | `**neuter nouns** ending in -ta, … etc.` | 8 |
| class_19/1_comp.md:39 | `combination of one or more of the above` | A complex compound needs two or more | `two or more` | 8 |
| class_19/2_kamm.md:45 | `adjective + adjectives` | Plural | `adjective + adjective` | 9 |
| class_19/2_kamm.md:53, 69, 91 | `can be classified as a *tappurisa* type of compounds` | Number disagreement; line 53 no capital/full stop | `as *tappurisa* compounds` | 8 |
| class_19/2_kamm.md:63 | `**iti** ; **evaṃ**; **saṅkhāto** ; **hutvā**` | Irregular spaces before semicolons | `**iti**; **evaṃ**; …` | 8 |
| class_19/3_digu.md:17 | `or as group` | Missing article | `or as a group` | 9 |
| class_19/4_tap.md:51 | `(water **for** face)` | Missing article | `for the face` | 7 |
| class_19/4_tap.md:103 | `(enjoying **in** the teaching)` | Idiom | `delighting **in**` | 7 |
| class_19/6_comp_rules.md:3 | `noun, adjective, participles, pronoun` | Plural in a singular list | `participle` | 9 |
| class_19/6_comp_rules.md:17 | `(blamed by wise)` | Missing article (4_tap.md:35 has `by the wise`) | `by the wise` | 8 |
| class_20/1_abya.md:17 | `an **adverb ending in an accusative case.**` | Wording | `an adverb with an accusative ending` | 7 |
| class_20/1_abya.md:19 | `for whole life` | Missing article | `for the whole of life` | 8 |
| class_20/1_abya.md:47 | `some grammatical books take them` | `grammatical books`; no capital/full stop | `Some grammar books take them …` | 7 |
| class_20/2_bahub.md:167 | `the negative of **sa-** are adjectives` | Subject–verb agreement | `the opposite of **sa-** is **a-** (without)` | 7 |
| class_21/2_voices.md:5, 7 | `Active voice: The man cut the tree` / `Passive: The tree is cut by the man.` | Tense mismatch with `chindati` and with the passive line; no full stop; `Passive` vs `Active voice` | `Active voice: The man cuts the tree.` | 8 |
| class_21/3_pass_refl.md:17, 23 | `but practically the meaning is the same.` / `as usual with a few exceptions` | Lower-case sentence starts; no full stop on 23 | fix | 8 |
| class_21/3_pass_refl.md:33 | `either **parassapada** or **attanopada** verbal ending can be used` | Number | `endings can be used` | 7 |
| class_21/3_pass_refl.md:43 | `What is the meaning of Pāli words **parassapada** and **attanopada.**` | Question without `?`; missing `the` | `…of the Pāli words … **attanopada**?` | 9 |
| class_21/7_perf.md:13 | `But, modern grammars have given it the name of - **Perfect Past Tense,**` | Stray comma and dash | `But modern grammars call it the **Perfect Past Tense**,` | 7 |
| class_21/7_perf.md:45 | `(to speak) - *different form of root √brū*. Has the following forms:` | Fragment | `…, a different form of √brū, which has the following forms:` | 8 |
| class_21/9_aor.md:7 | `Ajja “means” today in Pāli.` | Quotes on the wrong word | `Ajja means “today” in Pāli.` | 9 |
| class_22/2_cond.md:7 | `The Conditional[^12], expressing future time relatively to something that is past, … (Charles Duroiselle)` | Quotation is a fragment and has no quote marks | add quotes / complete | 7 |
| class_22/3_root_groups.md:129 | `knows, think` | Number | `knows, thinks` | 9 |
| class_22/3_root_groups.md:37 | `from most common to less common` | Comparative | `to least common` | 6 |
| class_23/2_aa.md:18 | `while forms that have not been seen in the text` | The list is of meanings, not forms | `meanings` | 7 |
| class_23/7_api.md:7 | `put over, closes, shuts` | Number | `puts over` | 9 |
| class_23/8_abhi.md:3 | `particularity` | Should be an adverb like its neighbours | `particularly` | 8 |
| class_23/10_ud.md:17 | `stands up, get out of` | Number | `gets out of` | 9 |
| class_23/20_mixed_pref.md:6 | `sit down hard` | Number; odd gloss | `sits down (near)` | 8 |
| class_23/22_dur_su_nir.md:1 | `dur, su, nir & etc.` | `& etc.` (also index.md:105, class_23/index.md:24) | `dur, su, nir, etc.` | 8 |
| class_24/3_caus.md:29 | `great blowing winds **causes**` | Agreement | `**cause**` | 9 |
| class_24/5_caus_pass.md:53 | `My good man did you not see` | Missing comma | `My good man, did you not see` | 8 |
| class_24/6_app.md:42 | `is like **pakkhī**, in **feminine** like **nadī** and the **neuter** like **aṭṭhi**` | Broken parallelism; no full stop | `the feminine like …, the neuter like … .` | 7 |
| class_25/1_deriv.md:3 | `are formed, now we take a look` | Comma splice | full stop | 7 |
| class_25/2_nouns.md:15 | `often translating with -ing` | Verb form | `often translated with -ing` | 8 |
| class_25/3_anub.md:15, 17 | `the first vowel is *always* lengthened` … `Except when ...` | `always` followed by three exceptions; guṇa (bhuj > bhoga) is not lengthening | `is strengthened, except when …` | 7 |
| class_25/5_taddh_2.md:232 | `cats-eye` | Apostrophe | `cat’s-eye` | 7 |
| class_25/6_home_work.md:5 | `please break-up every noun` | Verb is two words | `break up` | 9 |
| class_26/2_numer.md:48, 54, 55; 4_ind.md:81 | `consisting of hundred`, `consisting of thousand`, `in hundred ways` | Missing article | `a hundred`, `a thousand` | 7 |
| class_26/3_state.md:9 | `nature, character,` | Trailing comma | remove | 9 |
| class_26/3_state.md:7 | `sorrow-less-ness` | Hyphenation | `sorrowlessness` | 6 |
| class_26/4_ind.md:17, 27 | `(in such way)` | Missing article | `in such a way` | 7 |
| class_27/2_kicca.md:5–9 | `Please note in many of the examples that follow` / `just the …` / `but the same applies …` | One sentence over three paragraphs, no full stop | one line | 6 |
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

## E. Markdown defects that affect rendering

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_16/1_sandhi.md:55 | `(*vyañjana-sandhi)*` | Closing `*` outside the parenthesis (line 53 has `(*sara-sandhi*)`) | `(*vyañjana-sandhi*)` | 10 |
| class_16/3_vowel_1.md:5, 7 | `pacman-forward.png)it eats` / `backwards,![]` | No space between image and text | add spaces | 9 |
| class_16/7_vowel_5.md:27 | `**kvac’āsavaṇṇaṃ** **lutte**.` | Bold split in two | `**kvac’āsavaṇṇaṃ lutte**` | 8 |
| class_17/3_cons_1.md:11; 8_nig_1.md:11; 10_nig_3.md:9 | `**para** **dvebhāvo ṭhāne**`, `**aṃ** **byañjane** **niggahitaṃ**`, `**vagg’antaṃ** **vā vagge**` | Bold split into pieces | one bold span | 8 |
| class_17/3_cons_1.md:167–168 | `**b**haya`, `**b**havika` | Bold on `b`, heading is `vowel + bh` | `**bh**aya`, `**bh**avika` | 9 |
| class_17/15_nig_8.md:18 | `ariya-<br>saccāna**ṃ**` | `<br>` and hyphen inside a word | owner decision (see M2) | 7 |
| class_18/1_phonetic.md:17 | `1.  **Assimilation** happens` | Follows the list of lines 5–15 with only blank lines between, so Markdown continues that list and renders it as item 7 | separate with a heading/paragraph or drop numbers | 8 |
| class_18/2_as_ya.md:1, 3 | `# Phonetic changes of -y-` / `## Phonetic changes of -y-` | Same heading twice | remove H2 | 9 |
| class_18/2_as_ya.md:33–34 | `\| \| √guh \| (to hide) \| **+ ya** \| guyha \| could be hidden \|` then `--- ` | First data row is the table header (renders bold); all other tables use an empty header row | add empty header row | 9 |
| class_18/5_as_sa.md:10 | `√bhuj + bhuj\> bubhuj` | Missing space before `\>` | `bhuj \> bubhuj` | 9 |
| class_18/6_as_sum.md:7 | `tijti**j s**a ti` | Words run together, no `√`; lesson has `titij + sa + ti` | `titi**j s**a ti` | 8 |
| class_18/6_as_sum.md:18, 44 | `√k**an y**a ā`, `√**jal y**a` | Bold starts one/two letters early; should mark only the two meeting consonants | `√ka**n y**a ā`, `√ja**l y**a` | 9 |
| class_18/9_ex.md:10 | `√ādā + ta` | Prefix inside the root sign; `+` used while other deconstruction answers use spaces | `ā √dā ta` | 8 |
| class_18/11_ex.md:11, 24 | `\| \|` | Lone one-cell row after each table | remove or accept (spacer?) | 7 |
| class_19/2_kamm.md:135 | `becomes **mahā, or**` | `, or` inside the bold | `**mahā**, or` | 8 |
| class_19/2_kamm.md:141 | `mah**abb**haya` | Bold cuts `bbh` in two | `maha**bbh**aya` | 9 |
| class_19/5_dvanda.md:25 | `brāhmaṇ**ānaṃ “of** ascetics` | One bold span runs from the Pāli ending across the quote mark into the English | `**ānaṃ** “**of** ascetics` | 9 |
| class_20/2_bahub.md:19 | `viharāmi**.**` | Bold full stop | `viharāmi.` | 9 |
| class_20/4_change_comp.md:10 | `*pañcagu[^9]*` | Footnote marker inside italics | `*pañcagu*[^9]` | 7 |
| class_20/5_ex.md:8, 13, 18, 23 | `{: .align-right }` | attr_list markup in the source; only file in `docs/ipc` that uses it (project rule: clean Markdown) | owner decision | 7 |
| class_21/4_pres.md:7, 9 | `(*parassapada)*`, `(*attanopada)*` | Closing `*` outside the parenthesis | `(*parassapada*)`, `(*attanopada*)` | 10 |
| class_21/6_opt.md:9 | `in the reflexive **voice and passive voice.**` | Bold starts mid-phrase (4_pres.md:9 has `**reflexive** **voice** … **passive voice**`) | `**reflexive voice** and **passive voice**.` | 8 |
| class_21/8_imperf.md:20 | `agam**u<br>**agam**ū**` | Bold span closes after the `<br>` | `agam**u**<br>agam**ū**` | 9 |
| class_22/3_root_groups.md:144 | `## 7. tanādigaṇa (-o- *-yira[^14]-*)` | Footnote marker inside italics inside a heading | move marker out | 8 |
| class_23/23_home_work.md:5–12 | `3.  In the exercises, break up … into` + unindented lines | Continuation lines are not indented under item 3; line 12 runs two analyses together (`vi + √ñā + aṇa vi + √ñā 5 nā (know) + aṇa + aṃ`); space before colon | restructure | 8 |
| class_23/23_home_work.md:14 | `*object(s)* and \*predicate\*` | Escaped asterisks print literally; intended styling unclear | verify intent | 7 |
| class_24/1_pass.md:53 | `√dhar+ \*e` | Missing space | `√dhar + \*e` | 9 |
| class_24/2_irreg_pass.md:11 | `Kacc 502, 493**.** **yamhi** **dā dhā …**` | Bold full stop; split bold | one bold span | 9 |
| class_24/2_irreg_pass.md:34, 39 | `chindīyati[^22]` / `These bases (marked with \*)` | First row carries the footnote number instead of `\*`; note duplicates `[^20]` in 1_pass.md:58 | `chindīyati\*` + note once | 8 |
| class_24/2_irreg_pass.md:82, 93 | `**√va**ḍḍh`, `√**ph**ar` | Bold includes `√`; bold on `ph` instead of `pha` | `√**va**ḍḍh`, `√**pha**r` | 9 |
| class_24/5_caus_pass.md:11, 15 | `(\***e** \| \***aya** \| **\*āpe** \| **\*āpaya**)` | `\*` outside the bold in two items, inside in two | one form | 8 |
| class_25/1_deriv.md:13 vs 19 | `*dhātu + kita / kicca \> kitaka*` vs `## *kitaka + taddhita \> taddhita*` | Parallel formulas: one paragraph, one H2 at the end of the file | both paragraphs | 9 |
| class_25/3_anub.md:7 | `e.g. ṇ**a or \*a**` | Bold starts mid-word and covers `or` | `**ṇa** or **\*a**` | 9 |
| class_25/5_taddh_2.md:84, 86, 108, 159, 160 | `g**ā**mi**ka**`, `m**ā**gadhi**ka**`, `s**ā**rīri**ka**`, `b**ā**hiy**a**`, `**ā**nuttariya` | Suffix bold cut short or missing (`**ika**`, `**iya**` elsewhere) | `g**ā**m**ika**` etc. | 9 |
| class_26/4_ind.md:9 | `**36 times**` | Only bold gloss in the table | unbold | 9 |
| class_26/3_state.md:75 | `t**accha**` | Bold cuts the word unlike neighbours (`s**ā**ta**cca**`) | `ta**ccha**` | 8 |
| class_27/3_kita.md:64, 65, 89 | `phuṭ**ṭha**`, `rat**ta**`, `bhin**na**` | Bold splits the assimilated cluster (cf. `ka**ṭṭha**`, `ma**tta**`, `chi**nna**`) | `phu**ṭṭha**`, `ra**tta**`, `bhi**nna**` | 9 |
| `class_28/1_kita_1.md:596` | `sabh**o**jan**a**` | Bold marks only the final *a*; suffix is *ana* (compare `:597` `ac**e**t**ana**`). | `sabh**o**j**ana**` | 9 |
| `class_28/1_kita_1.md:337` | `a large group **of past participles**` | "of" inside the bold span. | `of **past participles**` | 9 |
| `class_28/1_kita_1.md:527-528`; `class_28/2_kita_less.md:54-56`, `:176-180`, `:186-187`, `:280-281`, `:351-352`, `:358-359`, `:384-385`, `:391-392`, `:433`, `:439`, `:479-480`, `:508-509`, `:515-516` | e.g. `gavesī`, `cakkhu`, `jīvikā`, `vattha`, `hutta`, `p**o**ta`, `m**ū**sikā` | Suffix not bolded in the result column (or only the changed vowel), unlike all other rows. | Bold the suffix | 9 |
| `class_28/1_kita_1.md:412`, `:649`, `:702`; `:611-613` | `\| **total** \| 265 \|`; `\| adj \| 143 \|` | Total figure not bold (bold in other tables); POS labels not bold in the `\*ī` table. | Make uniform | 9 |

## F. Convention drift

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_16/1_sandhi.md:57 | `**Ṃ Sandhi** *niggahīta-sandhi* which` | No parentheses, unlike items 1 and 2 | `(*niggahīta-sandhi*)` | 9 |
| class_16/1_sandhi.md:39–43 | `wouldn’t = would not` | No bold on elided letters, unlike lines 17–37 | `would n**o**t` | 8 |
| class_16/1_sandhi.md:47 | `Why is there sandhi?` | Plain paragraph; parallel question on line 11 is `##` | make heading | 7 |
| class_16/1_sandhi.md:13 | `this is called **euphonic combination**` | Repeats line 5 | merge | 6 |
| class_16/2_vowel.md:13–15 | `*lopa,*` `*dīghaṃ,*` | Comma inside italics; lines 17, 19 have it outside | `*lopa*,` | 8 |
| class_16/3_vowel_1.md:33, 48 | `pana \| **assa**` / `yena \| **āyasmā**` | Whole word bold and first word unbolded; all other rows bold only the meeting vowels | `pan**a** \| **a**ssa`, `yen**a** \| **ā**yasmā` | 9 |
| class_16/3_vowel_1.md:248 etc. | `**Possibility \#1** ?` / `**Possibility \#2**?` / `**Possibility \#3 ?**` / `**what is Possibility \#8 ?**` | Four different stylings of the recap question (files 3–10) | one form | 9 |
| class_16/3_vowel_1.md:11 | `a vowel before another vowel is sometimes elided` | Lower case, no full stop; other rule statements are sentences | capitalise + full stop | 8 |
| class_16 file structure | `# Elision of a Vowel` + `## Possibility \#1` vs `# Possibility \#2 — …` | Possibilities 1, 3, 5, 8 are H2 under a topic H1; 2, 4, 6, 7, 9 are H1 | one scheme | 8 |
| class_16/5_vowel_3.md:9 | `a![](…)a \> ā` | Not bold; the same line is bold in files 3, 4, 6 | bold | 8 |
| class_16/8_vowel_6.md:15 | `**together they become ya**` | Whole line bold; 9_vowel_7.md:15 bolds only the result | `together they become **ya**` | 8 |
| class_16/10_vowel_8.md:32, 47 | `s**uva**tthi` / `saññ**īme**va` | Bold covers neighbouring vowels; other rows bold only the inserted consonant | `su**v**atthi`, `saññī**m**eva` | 8 |
| class_16/11_vowel_9.md | (end of file) | No "what is Possibility #9?" recap, unlike 1–8 | add or accept | 6 |
| class_16/12_vowel_ref_table.md:119–123 | `aggi iva \> agg**î**va` | Source vowels not bold, unlike lines 111–117 | bold | 8 |
| class_16/13_home_work.md:3–7 vs 11–34 | `1.  Please` vs `1\. Find` | Real list vs escaped pseudo-list in one file | one form | 7 |
| index.md:39–42, 45, 117 | `Phonetic changes of -y-`, `Another consonant assimilation`, `Types of nouns` | Sentence case; all other titles are Title Case | Title Case | 8 |
| index.md:18; class_16/3_vowel_1.md:7; 13_home_work.md:5–6, 32 | `Pāli` | Project name uses `Pāḷi` (13_home_work.md:42 has `pāḷi`) | owner decision | 6 |
| class_17/3_cons_1.md:11; 4_cons_2.md:11; 7_cons_5.md:11 | `para dvebhāvo` / `para-dvebhāvo` / `para dvebhāvo ṭhāne.` | Same sutta (28) written three ways | one form | 9 |
| class_17/2_cons.md:7, 13 vs 3_cons_1.md:1 | `Re-duplication` vs `Reduplication` | Spelling drift | `Reduplication` | 9 |
| class_17/3_cons_1.md (whole) | `masc.`/`m.`, `fem.`/`f.` | Both abbreviations used (e.g. lines 21, 115; 22, 76) | one set | 9 |
| class_17/4_cons_2.md:22 vs 3_cons_1.md:152 | `ger.` vs `abs.` | Two labels for the same form | `abs.` | 8 |
| class_17/7_cons_5.md:15–20 | `adj \| final, complete` | POS in its own column without full stop; other tables in the class put `adj.` in the gloss cell | one layout | 8 |
| class_17/3_cons_1.md:53, 114, 143, 167 | `n**a**` / `**na**` | Negative `na > a` bolded two ways; the change `na > a` is not shown | one form, e.g. `na \> **a**` | 8 |
| class_17/4_cons_2.md:29 | `Counter-examples:` | Not bold; bold in every other file | bold | 9 |
| class_17/5_cons_3.md:51 | `pūj'ārahe` | Straight apostrophe; rest of class uses `’` | `pūj’ārahe` | 9 |
| class_17/6_cons_4.md:3 vs 57 | `n’eso` vs `neso` | Apostrophe drift | one form | 7 |
| class_17/6_cons_4.md:11 | `**esa** **m**aggo` | Split bold; lines 33, 35, 45 have `**esa m**aggo` | one form | 8 |
| class_17/1_alphabet_analys.md:37, 67; 9_nig_2.md:17, 45 | `Cerebral or Retroflex` / `Cerebral / Retroflex` / `cerebral` / `retroflex` | Term drift | one term | 8 |
| class_17/8_nig_1.md:44–46 | `saṃkhitta` (4th column) | Column holds joined form here, translation in rows above | add glosses | 7 |
| class_17/9_nig_2.md:70, 72, 73 vs 10_nig_3.md:17 | `upa sa**ṃ**` vs `paṭi + sa**ṃ**` | `+` missing | add `+` | 8 |
| class_17/10_nig_3.md:15–18 | `sa**ll**apati` vs `sa**l**lekha` | Bold on `ll` vs `l` | one form | 9 |
| class_17/15_nig_8.md:17–18 | `buddhān**a**sāsanaṃ` vs `ariyasaccān**a** dassanaṃ` | Joined vs spaced result | one form | 7 |
| class_17/3_cons_1.md:100; 9_nig_2.md:43 | `(commentary example)` / `comm word` | Footnote wording drift | one wording | 7 |
| class_17/19_home_work.md:14–15 | `p12 - 14` vs `p13-28` | Page-range style | one style | 8 |
| class_17/index.md | `Possibility \#2 — …` twice | Two numbering series (consonant 1–5, niggahīta 1–10) in one flat list; niggahīta #1 hidden under `Niggahīta Sandhi` | owner decision | 6 |
| class_18/1_phonetic.md:47 vs 61 | `(ger. descending)` vs `(abs. having given up)` | `ger.` and `abs.` in one file; class 18 otherwise uses `ger.`/gerund, class 17 `abs.` | one term course-wide | 9 |
| class_18/2_as_ya.md:5 vs 9 | `verbs of the **3rd** **conjugation**` vs `group 3` | Two names; split bold | one name | 7 |
| class_18/6_as_sum.md:8, 36 | `ni √mujj ta`, `√tij \> tip + ta \| tippa` | No bold in these rows; row 36 uses `\>` and `+` unlike the rest | match other rows | 9 |
| class_18/7_mix_san.md:1 | `(vomissaka-sandhi)` | Not italic; class 16/17 H1s italicise the Pāli term | owner decision | 6 |
| class_18/7_mix_san.md:15–16 | `a**ti** **e**ti` | Following vowel bold only in these two rows | unbold | 8 |
| class_18/7_mix_san.md:26, 31, 34, 35 | `bhava`, `lattha`, `so`, `kā` | No `√` / root form, other rows have `√root` | `√bhū`, `√labh`, `√su`, `√kar` | 8 |
| class_18/10_irreg_masc.md:12 | `**mano**` | Whole word bold; elsewhere only the ending | `man**o**` | 9 |
| class_18/10_irreg_masc.md:69–76 | `g**avo**` vs `gav**o**`; `go**hi**`, `gun**naṃ**` | Stem/ending split differs between cells of the same paradigm | one split | 9 |
| class_18/10_irreg_masc.md:65 vs 78, 93 | `go (masc) cow, cattle` vs `atta (masc) - self` | Dash drift | one form | 8 |
| class_18/10_irreg_masc.md:20 | `dukkho'ti` | Straight apostrophe | `dukkho’ti` | 9 |
| class_18/10_irreg_masc.md:22 vs 91 | `Similarly` vs `similarly:` | Case/punctuation | one form | 7 |
| class_18/10_irreg_masc.md:106–110 | hard-wrapped summary paragraph | Only hard-wrapped paragraph in the class; uses `—` | one line | 7 |
| class_18/10_irreg_masc.md:3 vs 20 | `Pāli` vs `Pāḷi` | Both spellings in one file | owner decision | 7 |
| class_19/2_kamm.md:7; 3_digu.md:3; 4_tap.md:5; 5_dvanda.md:5 | `*Kaccāyana 324.* dvipade…` / `**Kaccāyana 325. saṅkhyāpubbo digu.**` / `Kaccāyana 326. ubhe tappurisā.` | Three stylings of the sutta citation in one class; classes 16–17 use `In Kaccāyana this is called (n) **…**` | one style | 9 |
| class_19/2_kamm.md:7 | `tuly'ādhikaraṇe` | Straight apostrophe | `tuly’ādhikaraṇe` | 9 |
| class_19/1_comp.md:15–31 vs 35–39 | `*kammadhāraya or* **adjectival** *(adjective + noun)*` vs `*bahubbīhi* or **attributive** (meaning…)` | Italics cover `or` and the parenthesis in items 1–5, not in 6–7 | italic only on the Pāli term | 9 |
| class_19/3_digu.md:1; 4_tap.md:1; 5_dvanda.md:1 | `Digu-samāsa`, `Tappurisa-samāsa`, `Dvanda Samāsa` | Hyphen/case drift in H1s; body has `dvanda-samāsa`, `*dvandasamāsa*`, `Dvandasamāsa` (5_dvanda.md:21, 76, 88) | one form | 9 |
| class_19/4_tap.md:21 vs 31–107 | `## dutiyā-tappurisa` vs `## tatiyā tappurisa` | Hyphen only in the first heading | one form | 9 |
| class_19/2_kamm.md:19–27; 4_tap.md passim | `mahant**o** puris**o** \>` vs `thull**aṃ** + accay**aṃ** \>` | `+` between members present or absent at random | one form | 8 |
| class_19/2_kamm.md:3 vs 4_tap.md:3 | `**“blackbird”**` vs `“madhouse”` | English example bold in one file only | one form | 8 |
| class_19/4_tap.md:75, 77 | `(born from seclusion)`, `(not risen out of the water)` | Case preposition not bold, unlike the rest of the file | bold `from`, `out of` | 7 |
| class_19/6_comp_rules.md:17 | `viññugarahita` | Changed vowel not bold, unlike lines 19, 21 | `viññ**u**garahita` | 8 |
| class_19/1_comp.md:3 | `saṃ + √ās + a` | No result (`\> samāsa`), unlike `saṃ + √dhā + i \> sandhi` in class 16 | add result | 7 |
| class_19 (several files) | `digu is an example…`, `tappurisa is an example…`, `most common`, `all compounds with…` | Many sentences start lower-case / lack full stops | sentence case | 7 |
| class_19/8_home_work.md:13–14 | `Duroiselle \| samāsa` | No page numbers and no Māgadhabhāsā row, unlike classes 16–18 | add | 6 |
| class_20/2_bahub.md:235 | `tvaṁ` | `ṁ`; the course uses `ṃ` (only other `ṁ` is the deliberate chanting-book example in class_16/12_vowel_ref_table.md:103) | `tvaṃ` | 10 |
| class_20/2_bahub.md:125–183 | `ādittasīso – (a man)` vs `chinnasoto - (an arahant)` | En dash and hyphen mixed in one list | one dash | 9 |
| class_20/2_bahub.md:267; 3_mis.md:13; 4_change_comp.md:21 | `aññapad'atthesu`, `devamānuse'ti`, `one's own` | Straight apostrophes (4_change_comp.md:21 has `one’s` and `one's` in one cell) | `’` | 10 |
| class_20/2_bahub.md:103, 105 | `“who...”, “which…”, “that …”`, `“the man who….”` | Three/four dots, `...` vs `…`, spacing | `…` | 8 |
| class_20/2_bahub.md:7, 25 vs 43 | `(noun. paddy)` vs `(n. tree)` | Abbreviation drift | `n.` | 8 |
| class_20/2_bahub.md:187–213 | `\> acelaka` vs `\> paṃsukūliko` | Stem vs nominative in results | one form | 8 |
| class_20/1_abya.md:21 vs 3_mis.md:9–33 | `**yāvajīvaṃ \> yāva + jīva + aṃ**` vs `upekkhāsambojjhaṅga \< upekkhā + sambojjhaṅga` | Deconstruction written with `\>` in one file, `\<` in the other | `\<` | 8 |
| class_20/3_mis.md:7, 13, 19, 25 | `*[SN46.53](…)*  akālo` | Italic reference before the text (two spaces after on 7, 19); elsewhere `([REF](url))` after the text | one form | 8 |
| class_20/4_change_comp.md:1 | `Changes Of Certain Words In Compounds` | `Of`, `In` capitalised (also index.md:63, class_20/index.md:6) | `Changes of Certain Words in Compounds` | 8 |
| class_20/4_change_comp.md:19 vs 20 | `sa-` vs `sa` | Hyphen drift | one form | 7 |
| class_20/4_change_comp.md:23 vs class_16/7_vowel_5.md:70 | `Not a textual example` vs `not textual example` | Same footnote worded two ways | one wording | 8 |
| class_20/1_abya.md:9, 13 vs 17 | `the first member…`, `the second member…` vs `The resulting…` | Case of list items | sentence case | 8 |
| class_21/4_pres.md:17; 6_opt.md:17; 9_aor.md:25 vs 5_imp.md:17; 7_perf.md:29; 8_imperf.md:19 | `**s**` vs `**sg**` | Singular header abbreviated two ways in one class | one form | 9 |
| class_21/4_pres.md:18 vs 27 | `hanan**te**` vs `hañña**nte**` | Ending split differently; ending is `-ante`/`-nte` | one split | 9 |
| class_21/4_pres.md:13, 22; 9_aor.md:21, 30 vs 5_imp.md:13 etc. | `<br>√han + a \> hana**` vs `<br>(√sikkh + a \> sikkha)**` | Derivation with/without parentheses in table captions | one form | 8 |
| class_21/10_sum.md:27–36 vs 42–51 | `\| vattamānā \| ti \|` vs `\| **vattamānā** \| te \|` | Parassapada table labels plain, Attanopada table labels bold | one form | 9 |
| class_21/5_imp.md:5 vs 4_pres.md:5 | `“When a command…”` vs `“present tense when…”` | Capitalisation of sutta glosses; 9_aor.md:5 has a full stop inside | one form | 7 |
| class_21/2_voices.md:73 | `[DHP131](…)` on its own line before the verse | Elsewhere `([REF](url))` after the verse | one form | 7 |
| class_22/1_fut.md:13, 22; 2_cond.md:15, 24 vs class 21 captions | `Future Reflexive`, `Conditional Active` vs `Present Tense Attanopada` | Caption terminology changes between classes 21 and 22 | one scheme | 8 |
| class_22/1_fut.md:3 vs 2_cond.md:3 | `Kaccāyana 421. **anāgate bhavissantī.**` vs `Kaccāyana 422. kriy’ātipanne’tīte kālātipatti.` | Sutta bold in one file only (class 21 all plain) | one form | 9 |
| class_22/2_cond.md:19, 28 vs 1_fut.md:17 | `\| \| sg \| pl \|` vs `\| \| **sg** \| **pl** \|` | Header bold drift | bold | 9 |
| class_22/2_cond.md:9; 3_root_groups.md:146 | `hadn't`, `It's`, `it's` | Straight apostrophes | `’` | 9 |
| class_22/4_irreg_base.md:29 vs class_23/13_nii.md:8 | `is dis-enchanted` vs `is disenchanted` | Hyphen drift | `disenchanted` | 9 |
| class_22/4_irreg_base.md:20 | `he himself does` | Only gloss with a pronoun | `does (for oneself)` | 7 |
| class_23/1_prefix.md:9, 21, 33 | `(root – meaning – following along)` vs `(root – meaning - obstructing)` | En dash and hyphen mixed | one dash | 9 |
| class_23/1_prefix.md:25 | `√raj 3 ya (desire)` | Notation differs from lines 13, 37 (`√bhā (to shine)`) | `√raj (to desire)` | 7 |
| class_23/20_mixed_pref.md:22 | `sam + pati` | `saṃ` in every other row | `saṃ + pati` | 9 |
| class_23/21_nipata.md:34 | `**in full view, …, visibly.**` | Only meaning line with a full stop; in files 2–19 only the main meanings are bold, here every line is fully bold | align | 8 |
| class_23/22_dur_su_nir.md:51 | `## kā- kad- ku` | Hyphen missing on `ku` | `ku-` | 9 |
| class_23 files 2–20 | `√vatt \| to go on` / `to proceed`; `√sī \| to lie down` / `to sleep`; `√lok \| to look` / `to see`; `√sad \| to sink` / `to sit`; `√gah \| to grasp` / `to take`; `√mant \| to invite` / `to counsel` | Root glosses vary from file to file | one gloss per root | 7 |
| course-wide | `practices` (class_23/15_pati.md:14), `discolored` (22_dur_su_nir.md:14), `recognize` vs `practised`, `recognise`, `analyses` | US and UK spelling mixed | owner decision | 7 |
| class_24/5_caus_pass.md:7 | `"it is caused to be done"`, `"he causes (it) to be done,"` | Straight double quotes; line 5 has curly | `“…”` | 10 |
| class_24/5_caus_pass.md:39; class_25/4_taddh.md:19 | `app'eva`, `noun's` | Straight apostrophes | `’` | 9 |
| class_24/5_caus_pass.md:39 vs 27, 51, 63 | `[MN50](…)` vs `([MN65](…) bhaddālisuttaṃ)` | Reference without parentheses and sutta name | one form | 9 |
| class_24/3_caus.md:3; 2_irreg_pass.md:11, 64 vs classes 19–22 | `Kacc 438, 540.` vs `Kaccāyana 414.` | Abbreviated here, two numbers | one form | 8 |
| class_24/1_pass.md:58; 2_irreg_pass.md:19, 60 | `Commentary example` | Third wording (class 17: `(commentary example)`, `comm word`) | one wording | 8 |
| class_24/1_pass.md:27; 6_app.md:23, 40 | `## How to form Passive Verbs`, `## How To Construct Active Past Participle`, `## How to Decline Active Past Participle` | Heading case drift (`form`, `To`) | one style | 8 |
| class_24/6_app.md:46–52 vs class_18/10_irreg_masc.md | `nom`, `instr` vs `1.nom`, `3.inst` | Case labels differ between declension tables | one set | 8 |
| class_24/6_app.md:54–56 | hard-wrapped summary paragraph | Same as class_18/10_irreg_masc.md:106–110 | one line | 7 |
| class_24/2_irreg_pass.md:85 | `pā**vu**raṇaṃ` | Only form with a case ending in the table | `pāvuraṇa` | 8 |
| class_24/2_irreg_pass.md:5; 4_irreg_caus.md:5 | `√jan \| to produce` vs `√jan \| to be born` | Root gloss drift | one gloss | 7 |
| class_25/5_taddh_2.md:48 vs 54 | `ka**ccāyana**` vs `k**accāna**` | Bold split differs | one split | 8 |
| class_25/5_taddh_2.md (many rows) | `from family of Gotama`, `son of ascetic`, `belonging to community` | Articles dropped in most glosses, kept in some (`from a city`, `belonging to a sect`) | one style | 6 |
| class_25/2_nouns.md:3, 15, 26, 39 | `**concrete nouns** describe` vs `**agent noun** is` | Plural/singular and lower-case list items | one form | 7 |
| class_26/3_state.md:38–41; 4_ind.md:108–132; class_27/3_kita.md (all) vs other tables | `**+ tha**`, `**+ to**`, `**+ nta**` vs `+ tā`, `+ tabba` | Suffix column bold in some tables only | one form | 9 |
| class_26/4_ind.md:138–146 | `**kahaṃ**`, `**tahaṃ**`, `**kuhiṃ**`, `**tahiṃ**` | Whole word bold; elsewhere only the suffix | `ka**haṃ**` etc. | 9 |
| class_26/1_having.md:41, 58–64, 117; 3_state.md:47, 61, 64, 65, 74 | `daṇḍa pāṇi`, `na cakkhu`, `nir āsā`, `bahu suta`, `dur manas` | Members separated by a space; class 25 uses `+` (`jambu + nadī`) | `+` | 8 |
| class_26/1_having.md:3, 5 vs class_25/4_taddh.md:29 | `(atthyattha)`, `(atthyatthataddhita)` vs `atthy’attha` | Apostrophe drift | one form | 7 |
| class_27/2_kicca.md:130 | `kha**jjaṃ**` | Only form with a case ending | `kha**jja**` | 9 |
| class_27/1_kitaka.md:3 vs 7 | `**Primary derivatives**` vs `**Secondary Derivatives**` | Case drift; line 7 no full stop | one form | 8 |
| class_27/2_kicca.md:37, 66, 117; 3_kita.md:103; class_26/1_having.md:126 | `what do you notice about these words?`, `please note …`, `please **review** …` | Lower-case sentence starts | capitalise | 8 |
| class_27/3_kita.md:24, 28, 95–101 | `saddah**āna**`, `āsas**āna**`, `vippaki**ṇṇa**`, `uppa**nna**`, `nis**inna**` | Prefixes in the result are not shown in the root column | add prefix | 7 |
| `class_28/1_kita_1.md:596-603`; `class_28/2_kita_less.md:419-420`, `:452-454`, `:466-467`, `:508-509`, `:528-530` | `+ **\*ana**`, `+ \*u`, `+ yā`, `+ \***tta**`, `+ \*ikā`, `+ **tī**` | Suffix cell elsewhere is `**+ suffix**` (plus sign inside the bold). Four variants here. | `**+ \*ana**` etc. | 9 |
| `class_28/1_kita_1.md:607` | `suffix \***ī**` | Asterisk outside the bold; elsewhere `**\*a**`, `**\*ana**`. | `**\*ī**` | 9 |
| `class_28/2_kita_less.md:400`, `:448`, `:475`, `:524` | `**\*ā feminine nouns**`, `**yā feminine nouns**`, `**\*ta masc nouns**`, `**tī feminine nouns**` | Captions lack the leading `+ ` used everywhere else; `masc` abbreviated only here. | `**+ \*ā feminine nouns**` etc.; "masculine" | 9 |
| `class_28/2_kita_less.md:417-420` | `\| √dar \| to split \| + \*u \| d**ā**r**u** \| m \| wood, timber \|` | Only table with a sixth (POS) column; uses `m` where the slice's abbreviation is `masc`. | Split into two 5-column tables or use `masc` | 8 |
| `class_28/1_kita_1.md:61`, `:427` vs `:74`, `:220`, `:692` | `nī √as`, `nī √sar` vs `nir √chā`, `nir √bhuj`, `nir upa √dhā` | Same prefix written `nī` and `nir`. | One form (check which DPD uses) | 7 |
| `class_28/1_kita_1.md:422` vs `:661` | `vyākar**aṇa**` vs `byādh**i**` | `vi ā` gives *vy-* in one row, *by-* in the other. | One spelling | 7 |
| `class_28/1_kita_1.md` vs `class_28/2_kita_less.md` | — | File 1 gives each suffix a description sentence and POS breakdown; file 2 gives only `total`, with a description only for `ikā`, `āna`, `tāvī`. File 2 has no intro paragraph; the tāvī table (`:490`) has no bold caption. | Accept as design or level up | 6 |
| `class_28/1_kita_1.md:36`, `:78`, `:152`, … (every section opener) | `suffix **ta** is the most common kita suffix.` | Openers start lower-case; about half end without a full stop (`:152`, `:296`, `:379`, `:405`, `:449`, `:472`, `:512`, `:572`, `:607`, `:641`); `kita` not italic at `:36` but italic at `:5`, `:28`. | Uniform | 8 |
| `class_28/1_kita_1.md:249-250`, `:268`; `class_28/2_kita_less.md:177` | `great, large, big` / `big; huge; large`; `fly (smearer)` vs `heaven; lit. satisfied` | Gloss separators mix `,` and `;`; literal meaning given both as `(…)` and `; lit. …`. | Uniform | 6 |

## G. Links

None beyond what is listed in the Method table.

## H. Data to re-verify (forms, references, counts)

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_16/4_vowel_2.md:59, 77 | `n**u**si`, `n**u**ttha` | Forms not confirmed (`nu + asi`, `nu + ettha`) | DPD lookup | 5 |
| class_16/5_vowel_3.md:62 | `v**e**` + `**a**pi` > `v**ā**pi` | `vāpi` is normally `vā + api` | DPD lookup | 6 |
| class_16/7_vowel_5.md:42 | `s**a**` `(with)` + `**√ī**r + ī` | `sa` in `serī` is "own/self", not "with" | DPD lookup | 6 |
| class_16/7_vowel_5.md:76 | `v**i**` + `**u**cchijjati` | `vocchijjati` is usually `vi + ava + chijjati` | DPD lookup | 6 |
| class_16/11_vowel_9.md:23 | `*sara-sandhi-niṭṭhitaṃ*` | `sandhi` is masculine; expect `niṭṭhito` or two words | verify | 5 |
| class_16/12_vowel_ref_table.md:65 | `yena midhekacco =` | Space inside a sandhi exercise item | verify intended | 5 |
| class_17/5_cons_3.md:17 | `[DN16.14]` | Verse `anūpavādo anūpaghāto` is in DN 14 (and Dhp 185) | verify reference | 8 |
| class_17/3_cons_1.md:31 | `pur**a**` + `**kh**ata` | `purakkhata` is `puras + kata` | DPD lookup | 6 |
| class_17/3_cons_1.md:54 | `pari**cc**aja` `masc. rejection` | Form not confirmed (`pariccāga`?) | DPD lookup | 6 |
| class_17/3_cons_1.md:123 | `imperf. saw` | `addasā` usually labelled aor. | DPD lookup | 5 |
| class_17/16_nig_9.md:27 | `ka**ṃ**si` `who are you?` | `kaṃ` is acc.; form not confirmed | DPD lookup | 5 |
| class_18/1_phonetic.md:49 | `na + **pa** + √**cal** + a \> a**pac**ala \> a**cap**ala` | Derivation of `acapala` by metathesis not confirmed | DPD lookup | 5 |
| class_18/2_as_ya.md:45 | `visajja` | Usual form `vissajja` | DPD lookup | 5 |
| class_18/4_as_na.md:19 | `√tir + na` | Root usually given as `√tar` | DPD lookup | 6 |
| class_18/6_as_sum.md:12 | `saṃ ka**th** **y**a ā \| sāka**cch**ā` | `sākacchā` = `saha + kathā`? Not in the lesson | DPD lookup | 6 |
| class_18/7_mix_san.md:6 | `sa √div \> dyu \> **jj**u` | Derivation of `sajju` not confirmed | DPD lookup | 5 |
| class_18/10_irreg_masc.md:63 | `vay**o**anuppatto` | Usually two words `vayo anuppatto` | verify | 6 |
| class_19/1_comp.md:3 | `√ās` | Root of `samāsa` is usually `√as` (throw) | DPD lookup | 6 |
| class_19/1_comp.md:37 | `rukkhamūlika` | An `-ika` taddhita derivative, given as the bahubbīhi example | verify | 5 |
| class_19/2_kamm.md:81 | `(see *APA* for a lot of examples)` | `APA` is not explained anywhere in the class | expand | 6 |
| class_19/2_kamm.md:89 | `rāga *eva* dosa \> rāgadosa (lust just corruption \> corrupted by lust)` | `rāgadosa` is normally a dvanda (lust and hate) | verify | 6 |
| class_20/5_ex.md:7 | `[AN3.80](…#an3.79)` | Label and anchor disagree | verify | 8 |
| class_21/9_aor.md:43 | `bhagavantaṃ gāthāya **ajjhabhāsatha** ([SN1.1](…) etc.)` | SN prose has `ajjhabhāsi`; `ajjhabhāsatha` not confirmed at SN 1.1 | verify source | 7 |
| class_21/10_sum.md:5, 19 | `423, 426.` / `430, 373.` | Second sutta numbers: `426` repeats (line 11) and `373` is out of sequence | verify numbers | 7 |
| class_21/2_voices.md:13 | `chindīyati` | Usual passive is `chijjati` (used in class 18) | DPD lookup | 6 |
| class_21/8_imperf.md:11 | `about **38** Tipiṭaka examples so far` | Count dates quickly | re-check against DPD | 5 |
| class_20/1_abya.md:68 | `paccūsa \| early` | Noun (dawn) in a list of prefixes and indeclinables | verify | 5 |
| class_20/2_bahub.md:151 | `sapattabhāro – (a bird) carrying its own wings` | Listed under `sa- (with)` but glossed "own" | verify | 6 |
| class_22/3_root_groups.md:26 | `vacati` | Present of √vac not confirmed in this form | DPD lookup | 6 |
| class_22/4_irreg_base.md:24 | `ārambhati` | Usual present `ārabhati` | DPD lookup | 6 |
| class_23/3_ati.md:7 | `accayati` | Usual form `acceti` | DPD lookup | 6 |
| class_23/4_adhi.md:8 | `adhiggaṇhāti \| possesses, owns` | Form and gloss not confirmed | DPD lookup | 6 |
| class_23/5_anu.md:9 | `√bruh` | Root usually `√brūh` | DPD lookup | 6 |
| class_23/21_nipata.md:107 | `sat \| attha \| sadattha` | `sadattha` may be `sa(ka) + attha` | DPD lookup | 6 |
| class_23/22_dur_su_nir.md:62–63 | `ku \| √sad + ya \| kosajja`, `ku \| √kar + ya \| kukkucca` | Usually `kusīta + ya`, `kukata + ya` | DPD lookup | 6 |
| class_23/22_dur_su_nir.md:3 | `**dur-** **su- nir-** … are not used with verbs` | `dur`, `su` are in the list of 20 upasagga (1_prefix.md:51); `nir` forms verbs in 13_nii.md | verify statement | 6 |
| class_24/1_pass.md:79 | `vi**mucc**ita` | Usual pp is `vimutta` | DPD lookup | 6 |
| class_24/1_pass.md:68 | `āturīyati` | Form not confirmed | DPD lookup | 5 |
| class_24/2_irreg_pass.md:83 | `pa**vu**tta \| cast off` | Meaning for √vap "sow" not confirmed | DPD lookup | 5 |
| class_24/4_irreg_caus.md:15, 33 | `√hā … jāpeti \| confiscates`, `√vac … vipāceti \| spreads about` | Root attributions not confirmed | DPD lookup | 6 |
| class_24/5_caus_pass.md:71 | `ṭhapiyya \| ṭhapiyyati` | Form not confirmed | DPD lookup | 5 |
| class_25/3_anub.md:21 | `there is an aspirate consonant, e.g. ka**th**ā + \*ika \> ka**th**ika` | Rule doubtful (`ratha > rathika` fits, `magadha > māgadha` has `dh` later) | verify rule | 5 |
| class_25/5_taddh_2.md:94 | `v**e**nay**ika** \| vinaya student` | In the suttas `venayika` = one who leads astray | DPD lookup | 6 |
| class_25/5_taddh_2.md:192, 197 | `dāra \| + ka`, `paṭā \| + ka` | `dāra` = wife; `paṭā` not a word | DPD lookup | 6 |
| class_27/2_kicca.md:68–110 | `## \*anīya (ptp) \~17`, `\~73`, `\~3`, `\~25`, `\~28`, `\~2` | Unexplained numbers in headings (frequency counts?) | explain or remove | 7 |
| class_26/1_having.md:96 | `āyas \| + mant \| āyas**mant** \| respectable` | Usually `āyu + mant`; gloss "venerable" | DPD lookup | 7 |
| class_26/1_having.md:41, 93 | `daṇḍapāṇ**ī**`, `hirī**mant**` | Usual forms `daṇḍapāṇi`, `hirimant` | DPD lookup | 6 |
| class_26/1_having.md:59 | `bahutthi**ka**` | Sandhi of `bahu + itthi` not confirmed | DPD lookup | 5 |
| class_26/1_having.md:117, 123 | `nir āsā \| + sa \| nirāsā**sa**`, `tapas \| + sī \| tapa**ssī**` | Suffix analyses not confirmed (`nir + āsāsa`; `tapas + vī`) | DPD lookup | 6 |
| class_26/3_state.md:38–41 | `dama \| **+ tha** \| dama**tha**` | `-atha` forms are usually primary derivatives (`√dam + atha`) | verify | 6 |
| class_26/3_state.md:98 | `s**o**rat**a** \| mild state, politeness` | `sorata` is an adjective; the state is `soracca` | DPD lookup | 6 |
| class_27/2_kicca.md:145 | `√pis \| + \*iya \| p**e**s**iya** \| to be sent` | Root attribution not confirmed | DPD lookup | 5 |
| `class_28/1_kita_1.md:3-5` | `more than 150 suffixes`, `more than 14000`, `**first 18** account for **83%**` | Top-18 counts sum to 12 280, which is 83% of about 14 800, consistent with "more than 14000". All DPD-derived counts are a snapshot and could not be recomputed. | Recompute from current DPD DB | 6 |
| `class_28/3_home_work.md:13` | `Duroiselle \| Primary Derivatives (574-578)` | Paragraph range not confirmed against Duroiselle (reader recalls kita section starting at §575). | Verify | 5 |
| `class_28/1_kita_1.md:30-32` | bold list `ta a \*a … tī` | Bold marks the 45 suffixes covered in the two files (18 + 27); matches headings and order. Meaning of bold and of `\*` is not stated anywhere in this class. | Add one line of explanation or point to where `\*` is defined | 7 |

## Mechanical detail

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

## Notes carried from the read

- Footnotes are numbered across classes (`[^1]`, `[^2]` in class 16, `[^3]`–`[^5]` in class 17), so a file starting at `[^3]` is by design.
- `svahaṃ` (class 16 finding, conf. 6) is attested as metri causa in class_17/5_cons_3.md:41 (SN 4.23); in class 16 it is presented as ordinary sandhi.

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

