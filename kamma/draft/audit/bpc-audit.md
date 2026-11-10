# BPC audit — `docs/bpc/`

Date: 2026-11-10
Scope: all 105 Markdown files under `docs/bpc/` (index + classes 1–14, 5 287 lines).
No file in `docs/` was modified. This is a findings list only.

## Method and limits

| Check | How | Result |
| --- | --- | --- |
| Full read of every file | Manual, line by line | Done |
| Sutta links (`s.dhamma.gift`) | `uv run python scripts/check_sutta_links.py docs/bpc` | 82 links / 56 pages, all pass |
| Other external links | HTTP status request per URL | 2 dead, 1 unreachable by design (see G) |
| Local links and `#anchors` | grep of targets against files and `{: #id}` definitions | All resolve |
| Index titles vs page headings | Scripted comparison (root index and 13 class indexes) | All match; every page is listed |
| Table column counts | Scripted | 1 mismatch (see E) |
| Arithmetic in data tables | Recomputed | Correct (see H) |

Not verified:

- Pāli forms were checked against my own knowledge of the grammar, not against the DPD database. Each grammar finding carries a confidence score (1–10). Anything below 8 needs a DPD lookup before it is changed.
- The link checker proves that a URL and anchor exist, not that the quoted sentence really is in that sutta. Citations were not checked against the texts.
- Frequency counts (class 2, 5, 6, 8) could not be recomputed here.
- Rendered output (site, PDF, DOCX) was not built. Format findings are from the source, with the likely rendering effect stated.
- Exercises and keys (`bpc_ex`, `bpc_key`) are out of scope.

Paths below are relative to `docs/bpc/`.

## Summary

| Section | Findings |
| --- | --- |
| A. Pāli and grammar content errors | 47 |
| B. Paradigm tables that disagree with each other | 17 |
| C. Translation and gloss problems | 14 |
| D. English typos and grammar | 37 |
| E. Markdown defects that affect rendering | 20 |
| F. Cross-file convention drift | 16 |
| G. Links | 4 |
| H. Data to re-verify | 6 |

Overall confidence in the audit: 8/10 for sections D–G (mechanical, verifiable in the source), 7/10 for A–C (missing: DPD confirmation of the individual forms flagged below 8).

The highest-value fixes are in A and B: they are what a student will memorise wrongly.

---

## A. Pāli and grammar content errors

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| A1 | `class_2/2_alphabet.md:111` | `diṣṭa (seen)` | Sanskrit for "seen" is *dṛṣṭa*. *diṣṭa* means "shown, appointed". | `dṛṣṭa (seen)`, or keep *diṣṭa* with its real meaning | 8 |
| A2 | `class_3/5_roots.md:27` | `paṭibhanda`, `upanibhandha`, `nibadhana` | Probable misspellings in the √bandh list. `upanibandha` is already listed, so `upanibhandha` is a duplicate with a misplaced *h*. | `paṭibandha`; delete or correct the other two after a DPD check | 7 |
| A3 | `class_3/5_roots.md:31` | `vibhūsana`, `anubhutta` under √bhū | *vibhūsana* is from √bhūs (adorn); *anubhutta* is from √bhuj. | Remove from the √bhū list | 7 |
| A4 | `class_3/7_root_4.md:7` vs `:31` | Rule: "ṇā (ṇo) after a vowel, uṇā after a consonant". Example: `√sak + ṇo > sakko` | √sak ends in a consonant, so the example breaks the rule just stated. | Add a note that √sak takes ṇo with assimilation (k + ṇ > kk), or reword the rule | 7 |
| A5 | `class_3/8_root_5.md:1-5`, `index.md:17` vs `class_4/3_var_root_group.md:10` | `√ki` / `kiyādigaṇa = ki + ādi + gaṇa` vs `√kī + nā` | Same root spelled two ways. | Pick one (√kī is the usual citation form) | 9 |
| A6 | `class_3/9_root_6.md:13-15` | `√tas (thirst) + ṇhā > taṇhā` | Shown as an example of the group 6 conjugational sign, but *taṇhā* is a noun, not a verbal base. | Remove, or mark clearly as a noun formation | 6 |
| A7 | `class_3/13_tricky_base.md:9` | `√sad (sit) + a > sīda + ti > nisīdati` | Prefix *ni* is missing from the derivation. Compare `:19`, which writes `pa + √hā`. | `ni + √sad + a > …` | 9 |
| A8 | `class_3/13_tricky_base.md:13` | `sayati (vuddhi)` | ī > ay is guṇa by the course's own table (`class_4/4_vuddhi.md:90-91`); vuddhi would be *āy*. | `(guṇa)` | 8 |
| A9 | `class_4/5_root_2.md:17` | `bhunja + ti` | Missing diacritic. | `bhuñja + ti` | 10 |
| A10 | `class_4/7_basic_assim.md:3`, `:19-23`, `:39`, `:44` | "how verbs from group 3 get formed", followed by *bhijjati, khajjati, chijjati, rujjhati, haññati* | These are passives of roots from other groups (√khād is group 1, √rudh is group 2). Only the last line of the page mentions the passive. | Split the examples into "group 3" and "passive ya", or state up front that both are shown | 7 |
| A11 | `class_5/4_masc_ii.md:7` | "Many of these agent nouns…" | -ī nouns here are possessives ("has X"). "Agent noun" is the term the course uses for -tar in `class_6/2_masc_u.md:31`. | "possessive nouns" | 7 |
| A12 | `class_5/5_trans.md:41` | `√pis (send)` | √pis is "grind, crush". *peseti* (send) is not from it. | Check DPD for the root of *peseti* | 6 |
| A13 | `class_5/6_say_no.md:50-54` | "mā + imperative … `mā pamādā attha`" | The source reads *mā pamādattha*, which is an aorist 2nd plural, so it illustrates mā + aorist. The split *pamādā attha* is not a valid simplification. | Replace with a real mā + imperative example | 7 |
| A14 | `class_6/2_masc_u.md:45` | `√dhar + tar > dhātar` | *dhātar* is from √dhā. | Check DPD; replace the row | 6 |
| A15 | `class_6/3_masc_uu.md:12`, `class_11/3_adj.md:157` | dat `viduno`; gen `viduno, vidussa` | Dative and genitive singular should be identical. | Add `vidussa` to the dative | 8 |
| A16 | `class_7/4_pali_lists.md:4` | `Dhātumañjūsa` | Title is feminine. | `Dhātumañjūsā` | 8 |
| A17 | `class_8/2_abs_ger.md:3` | "one of the most common forms of verbal adjectives … has no declensions" | An absolutive is not an adjective. | "verbal forms" | 7 |
| A18 | `class_8/2_abs_ger.md:9`, `:105-118`, `:150-170` | Title equates Absolutive / Gerund. Line 9: "The gerund denotes a completed or continuing action". Table 5 translates every -ya form as "having …". The last section then says -tvā = completed (absolutive), -ya = ongoing (gerund). | The page contradicts its own closing distinction. | Use one term until the distinction section, and make table 5 glosses consistent with it | 8 |
| A19 | `class_8/2_abs_ger.md:67` | `√vad + tvā > vatvā` | *vatvā* is traditionally √vac + tvā. | Check DPD | 6 |
| A20 | `class_8/2_abs_ger.md:115`, `class_10/2_prp.md:92`, `class_14/4_ptp.md:62` | `√ādā` | Not a root. It is ā + √dā; the same tables write `ā + √ñā` and `pa + √hā`. | `ā + √dā` | 9 |
| A21 | `class_8/2_abs_ger.md:99` | `chind + itvā` | Base is given as `chinda` in the same row; the other rows write the full base. | `chinda + itvā` | 9 |
| A22 | `class_8/2_abs_ger.md:128-131` | `abhi + sam + √i`, `saṃ + √i`, `anu + vid` | *sam* / *saṃ* mixed; √ missing before *vid*. | `saṃ` in both; `anu + √vid` | 9 |
| A23 | `class_8/3_fem.md:22` | `brahmaṇa`, `brahmaṇī` | Short first vowel. The rest of the course has *brāhmaṇo*, *brāhmaṇā*. | `brāhmaṇa`, `brāhmaṇī` | 9 |
| A24 | `class_8/3_fem.md:104` | `sappī` (serpent) | The usual masculine is *sappa*; also the only row with no bold ending. | Check DPD; replace the row if *sappī* is not attested | 6 |
| A25 | `class_9/3_inf.md:39` | `√bhind + ituṃ` | √bhind is not a root. Root is √bhid, base *bhinda*, so the row belongs in section 3 (base + -ituṃ). | Move to section 3 as `√bhid, bhinda` | 9 |
| A26 | `class_9/3_inf.md:48` | "Very rarely, the infinitive can be formed by … the base" | The page's opening example *passituṃ* is this type, as are *bhuñjituṃ*, *pivituṃ*. | Drop "Very rarely" | 6 |
| A27 | `class_10/2_prp.md:158` | masc -anta loc sg `gacchante, gacchantamhi, gacchantasmiṃ` | Declared "like bhagavant", whose table has `bhagavati` (`class_6/4_subst.md:67`). | Add `gacchati` | 7 |
| A28 | `class_10/2_prp.md:161` | "Feminine ending in -ntī (like nadī)" | *nadī* is never introduced. The course model for -ī feminine is *kumārī*. | "(like kumārī)" | 9 |
| A29 | `class_10/2_prp.md:185` | neuter voc pl `gacchanto, gacchantā` | Masculine forms copied into the neuter table. | `gacchantāni` | 8 |
| A30 | `class_10/3_pron.md:242-275` | Heading "in the nominative case", rows `amu`, `sa`, `aññatara`, `añña` | These four are stems; the others are nominatives (*sabbo*, *itaro*). | Give nominatives throughout, or drop the heading claim | 8 |
| A31 | `class_11/2_pp.md:14`, `:30`, `:32`, `:36` | "the past participle is passive in meaning", with *bhūta*, *gata*, *mata* | Intransitive past participles are active in sense. | "usually passive; active for intransitive verbs" | 7 |
| A32 | `class_11/2_pp.md:52` | `ṭhahati … + ita > ṭhita` | *ṭhita* is ṭhā + ta (ā > i), so it belongs in table 1. The course uses *tiṭṭhati* everywhere else. | Move; use *tiṭṭhati* | 7 |
| A33 | `class_11/2_pp.md:64` | `parisedati … sede` | The base *sede* is causative, so the verb should be *parisedeti*. | Check DPD | 6 |
| A34 | `class_11/2_pp.md:74` | `jirati` | Short vowel; the root in the same row is √jīr. | `jīrati` | 9 |
| A35 | `class_11/2_pp.md:75` | `khīna` | Dental n. | `khīṇa` | 9 |
| A36 | `class_11/2_pp.md:76` | `muyhati … + na > mūḷha` | *mūḷha* is muh + ta, not + na. | Move to table 1 | 8 |
| A37 | `class_11/3_adj.md:73`, `:101`, `:132` | `uttariyāṃ`, `ātāpiniyāṃ`, `bahuyāṃ` | Long ā before ṃ. Correct in `:160` (`viduniyaṃ`) and in `class_8/3_fem.md`. | `-iyaṃ`, `-iniyaṃ`, `-uyaṃ` | 9 |
| A38 | `class_11/3_adj.md:118`; `:168`, `:169`, `:175` | nt voc pl `ātāpinī`; nt pl `viduni` | First looks like a feminine form; second has a short vowel (compare `bahūni`, `āyūni`). | `ātāpīni`; `vidūni` | 8 / 7 |

Further items in classes 12–14:

| # | Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- | --- |
| A39 | `class_12/3_card.md:13` | `pañca-kāma-guṇāni` | *kāmaguṇa* is masculine; `class_13/1_review.md:13` has `pañca kāmaguṇā`. | `pañca kāmaguṇā` | 7 |
| A40 | `class_12/3_card.md:104` | heading `aṭṭharasa` | Table below has `aṭṭhārasa`. | `aṭṭhārasa` | 9 |
| A41 | `class_12/3_card.md:236-241` | `1014`, `1042`, `1056`, `1063`, `1070`, `1076` | Superscripts lost: these are 10¹⁴ … 10⁷⁶ but now read as ordinary numbers. Zero counts in column 3 are correct (verified). | Write `10^14` etc. | 9 |
| A42 | `class_13/3_pass_verb.md:37` | `√badh` | Elsewhere `√bandh` (`class_3/5_roots.md:25`, `class_9/3_inf.md:37`, `class_14/4_ptp.md:65`). | `√bandh` | 8 |
| A43 | `class_13/3_pass_verb.md:149` | `uddissati` "it is pointed up" | Attestation of this passive is doubtful. | Check DPD; replace the pair if not attested | 6 |
| A44 | `class_13/4_pprp.md:11`, `:17`, `:28` | Rule: "passive base + māna". Examples: `labbhanta`, `muccanta` | The rule names only -māna but the tables also give -nta forms. | Add -nta to the rule, or remove the -nta forms | 8 |
| A45 | `class_14/2_caus_verb.md:167` | `√sam + *e > sāme > sāmeti` | The causative is normally *sameti*, without lengthening. | Check DPD | 6 |
| A46 | `class_14/3_caus_pass.md:53-55` | `bhāviya`, `bhāvīyati`, `bhāviyamāna` | i / ī alternate in three consecutive rows. | Use one form | 8 |
| A47 | `class_14/3_caus_pass.md:57-61` | "How To Form Causative Passive Present Participle" | Formula stops at the causative passive base. The "+ māna" step is missing. | Add the third line | 9 |

## B. Paradigm tables that disagree with each other

A student who compares two tables for the same word will find different forms.

| # | Locations | Difference |
| --- | --- | --- |
| B1 | `class_6/2_masc_u.md:87-90` vs `:103-106` | *bhātar* plural. Stand-alone table: inst/abl `bhātūhi`, dat/gen `bhātūnaṃ`. Comparison table: `bhātarehi, bhātūhi` and `bhātarānaṃ, bhātānaṃ, bhātūnaṃ`. |
| B2 | `class_4/10_aor.md:52` vs `:65`, `class_4/11_root_as.md:33`, `class_13/3_pass_verb.md:125` | Aorist 1st pl: *paci* table gives only `-imhā`; the others give `-imha` (and `-imhā`). |
| B3 | `class_10/3_pron.md:37` vs `:204` | *ta* masc nom sg: `so` vs `so, sa`. |
| B4 | `class_10/3_pron.md:40`, `:42`, `:207`, `:209` vs `:82`, `:84` | *ta* dat/gen pl: masculine `tesaṃ` only; neuter `tesaṃ, tesānaṃ`. |
| B5 | `class_10/3_pron.md:107`, `:155` vs `:206`, `:232` | *ima* inst sg: `iminā` vs `iminā, anena`. |
| B6 | `class_10/3_pron.md:189` vs `:230` | *ya* nt nom sg: `yaṃ, yad` vs `yaṃ`. |
| B7 | `class_10/3_pron.md:183` vs `:223` | *ya* fem loc sg: `yassaṃ, yāyaṃ, yāya` vs `yassaṃ, yāyaṃ`. |
| B8 | `class_5/4_masc_ii.md:39`, `class_8/3_fem.md:45` vs `class_11/3_adj.md:102`, `class_12/4_ordin.md:44` | Vocative sg of -ī stems: `pakkhī`, `kumārī` vs `ātāpi`, `catutthi / catutthī`. Standard grammars give the short vowel. |
| B9 | `class_5/4_masc_ii.md:36` vs `class_11/3_adj.md:99` | -ī masc abl sg: without and with `-ismā`. |
| B10 | `class_4/9_masc_i.md:15`, `class_9/2_nt.md:73` vs `class_11/3_adj.md:73` | Loc sg `-ini`: noun tables give it to the neuter only; the adjective table gives it to the masculine only. |
| B11 | `class_11/3_adj.md:70` vs `:72` | -i adj dat sg `uttarino`; gen sg `uttarino, uttarissa`. |
| B12 | `class_11/3_adj.md:84` vs `:86`; `:114` vs `:116`; `:171` vs `:173` | Dat pl and gen pl differ within one table (`-inaṃ` / `-unnaṃ` in one case only). |
| B13 | `class_8/3_fem.md:7` vs `class_11/3_adj.md:81` | -i fem nom pl: `bhūmī, bhūmiyo` vs `uttariyo` only. |
| B14 | `class_9/2_nt.md:112` vs `:125` | *āyu* nom sg: `āyu, āyuṃ` vs `āyuṃ, āyu` (second unbolded). |
| B15 | `class_14/4_ptp.md:106`, `:119` | Neuter abl sg lists `-to`; masculine does not, in both tables. |
| B16 | `class_7/3_opt.md:51` vs `class_14/2_caus_verb.md:135` | Optative 1st sg `-eyyaṃ` is used in class 14 but is absent from the class 7 table. Class 14 also lists seven forms for six slots, out of order. |
| B17 | `class_2/3_decl_nouns.md:114` vs `class_3/12_help_with_ex.md:17` | Genitive "usually comes before" vs "always comes before". |

## C. Translation and gloss problems

| # | Location | Current | Problem / suggested | Conf. |
| --- | --- | --- | --- | --- |
| C1 | `class_2/3_decl_nouns.md:102-108` | "The lay devotee **walks** from the residence" / `gacchati` | The vocabulary on the same page has *carati* = walks, *gacchati* = goes. Use "goes". | 9 |
| C2 | `class_6/5_and_or.md:13-15` | `ajā eḷakā ca` / "sheep and goats" | Order reversed: *ajā* = goats, *eḷakā* = sheep. | 9 |
| C3 | `class_6/4_subst.md:43-45` | `dakkhanti` / "see" | Future: "will see". | 7 |
| C4 | `class_7/3_opt.md:39` | `āhareyyāmi` "I could eat" | *āharati* is "bring". "I could bring". | 9 |
| C5 | `class_7/3_opt.md:5` | wish: "he **wants to** go" | An optative wish is "may he go". | 7 |
| C6 | `class_8/4_adv_place.md:34` | "that is delightful place" | "that is a delightful place". | 10 |
| C7 | `class_9/3_inf.md:90` | *jegucchī* "who disgusted (to)" | Garbled gloss. | 9 |
| C8 | `class_9/4_dat_purpose.md:5-7` | Bold on `upasaṅkamituṃ` / "to approach" | The page teaches the dative of purpose, so the bold belongs on `dassanāya` / "to see". | 9 |
| C9 | `class_10/3_pron.md:270` | *aññatara* "a certain, the" | Truncated gloss. | 8 |
| C10 | `class_10/3_pron.md:272-273` | *kataro* and *katamo* both "which (of the many)?" | *katara* is "which of two". | 8 |
| C11 | `class_10/5_emph.md:11` | `dissanti … suyyanti` / "is seen as well as heard" | Plural: "are seen as well as heard". | 9 |
| C12 | `class_11/2_pp.md:30` | *bhūta* "became" | Participle: "become, been". | 8 |
| C13 | `class_13/2_adv.md:75` | *ajjatana* "modern" | "of today", parallel to *svātana* "of tomorrow" in the row above. | 7 |
| C14 | `class_13/3_pass_verb.md:149` | *uddisati* "he points up" | "points out". | 8 |

Glosses that vary for the same item (pick one each): *ottappa* "remorse" (`class_2/2_alphabet.md:19`) vs "regret" (`class_5/4_masc_ii.md:26`); √sad "sit" vs "sink" (`class_11/2_pp.md:77`); √dhā "to place" vs "to hold" (`class_13/3_pass_verb.md:54`, `:64`); *ka* "adj" vs "pron" (`class_13/2_adv.md:20`, `:27`); the monkey simile translated two ways (`class_10/2_prp.md:19`, `:207`).

## D. English typos and grammar

| # | Location | Current | Suggested |
| --- | --- | --- | --- |
| D1 | `class_1/index.md:3` | `Pāli ?` | `Pāli?` (same at `class_9/5_yava_tava.md:13` "before ?") |
| D2 | `class_1/index.md:28` | "Meant a humorous element." | "Meant as a humorous element." (compare `class_12/5_kahap.md:21`) |
| D3 | `class_1/index.md:43` | "Golden Dictionary" | "GoldenDict" |
| D4 | `class_1/index.md:63` | "2-3 of your favorites and most inspiring sentences" | "2–3 of your favourite and most inspiring sentences" |
| D5 | `class_2/3_decl_nouns.md:3` | "gender, number and the case" | "gender, number and case" |
| D6 | `class_2/3_decl_nouns.md:112` | `**‘s.**` | `**’s.**` (opening quote used as apostrophe) |
| D7 | `class_2/3_decl_nouns.md:190` | "Please note that dictionary often has" | "the dictionary" |
| D8 | `class_3/2_conjug.md:24`, `class_3/3_preset.md:10` | "in details" | "in detail" |
| D9 | `class_3/3_preset.md:8` | "Middle or Reflective Voice" | "Reflexive" (as in `class_13/4_pprp.md:40`) |
| D10 | `class_3/13_tricky_base.md:5-15` | "(sanskrit)" | "(Sanskrit)" |
| D11 | `class_3/14_home_work.md:23` | "(7th conjugation group" | Close the parenthesis |
| D12 | `class_4/2_dpr_tpr.md:5` | "Here link to some useful videos … answers for those questions" | "Here is a link to … answers to these questions" |
| D13 | `class_4/3_var_root_group.md:5` | "Kaccāyana (7th CE)" | "7th century CE" |
| D14 | `class_4/4_vuddhi.md:82` | "karoti \> (he does, makes)" | Remove the stray `\>` |
| D15 | `class_4/7_basic_assim.md:27` | "he is existing" | "it exists; is found" |
| D16 | `class_5/3_future.md:7` | "Brahmans will do …." | Three dots; "Brahmans" vs "Brahman" vs "brahmin" should be unified |
| D17 | `class_5/3_future.md:76` | 2nd pl "you will develop" | "you all will develop" (also `class_7/3_opt.md:60` "you could be") |
| D18 | `class_5/4_masc_ii.md:5` | "In the PED dictionary" | "In the PED" |
| D19 | `class_5/5_trans.md:17` | "Tathagata" | "Tathāgata" |
| D20 | `class_5/6_say_no.md:36` | "Ratthapāla" | "Raṭṭhapāla" |
| D21 | `class_5/7_with.md:3` | "In Pāli only the instrumental case can express…" | "the instrumental case alone can express…" (current wording reads as an exclusive claim) |
| D22 | `class_6/2_masc_u.md:27` | "These can be also be found … eg." | "These can also be found … e.g." |
| D23 | `class_6/2_masc_u.md:29` | "the Sanskrit equivalent, ending in **-tṛ**." | Sentence fragment; join to the previous sentence |
| D24 | `class_6/3_masc_uu.md:3` | "formed from the **ññū** (knower) and **gū** (goer) ;" | "formed with the suffixes … ;" and remove the space before the semicolon |
| D25 | `class_7/3_opt.md:63` | "highly used!" | "very frequently used" |
| D26 | `class_7/5_home_work.md:17` | "Optative tense" | "Optative mood" |
| D27 | `class_8/2_abs_ger.md:39` | "Absolutive ending in **tvā** are" | "Absolutives ending in" |
| D28 | `class_8/2_abs_ger.md:107`, `class_13/3_pass_verb.md:48` | "from the Class 4" | "from Class 4" |
| D29 | `class_8/4_adv_place.md:22` | "from all every direction" | "from every direction" |
| D30 | `class_9/2_nt.md:4`, `:93` | "Relevant for 2025 year" | "for the year 2025" |
| D31 | `class_9/2_nt.md:51` | "These are very rare, there are only few of them" | "These are very rare; there are only a few of them" |
| D32 | `class_9/3_inf.md:17` | "infintive" | "infinitive" |
| D33 | `class_9/3_inf.md:33`, `:48` | "can be formed by added the suffix" | "by adding" |
| D34 | `class_9/4_dat_purpose.md:15` | "Sāvatthi" | "Sāvatthī" (as in `class_8/2_abs_ger.md:158`) |
| D35 | `class_9/6_adv_inter.md:1`, `class_9/index.md:8`, `index.md:67` | "Adverbs & Indeclinable" | "Indeclinables" |
| D36 | `class_11/3_adj.md:179` | "Nouns and adjectives interchangeable unless…" | "are interchangeable … ." |
| D37 | `class_14/4_ptp.md:126` | "in the Cannon" | "Canon" |

Smaller items: `class_12/3_card.md:22` "Almost each number" → "Almost every number"; `class_12/3_card.md:172` "Summary of numbers gender and numbers" → "Summary of gender and number"; `class_13/2_adv.md:42` "for third time" → "for the third time"; `class_13/4_pprp.md:47` "both an *attanopada* and *parassapada* endings" → "both *attanopada* and *parassapada* endings"; `class_13/3_pass_verb.md:48` "Please refresh in memory" → "Please review"; `class_11/5_home_work.md:10` (and classes 12–14) the "SBS kuṭi udāna" item is not a complete sentence.

Missing sentence-final punctuation or lower-case sentence starts are frequent (for example `class_2/3_decl_nouns.md:11`, `:76`; `class_3/5_roots.md:3`, `:7`; `class_4/10_aor.md:7`, `:19`, `:29`; `class_8/3_fem.md:30`, `:60`, `:64`; `class_10/3_pron.md:11-17`; `class_12/3_card.md:28`, `:40`, `:46`). Spelling mixes British ("behaviour", "colour") and American ("favorites").

## E. Markdown defects that affect rendering

| # | Location | Defect | Likely effect |
| --- | --- | --- | --- |
| E1 | `class_4/11_root_as.md:1`, `class_4/12_root_huu.md:1` | File starts with `##`; no H1. Every other page has exactly one H1. | Page title and navigation hierarchy differ |
| E2 | `class_3/2_conjug.md:19` | `| --- | --- | --- | --- |` in the table body | A literal row of dashes |
| E3 | `class_2/4_home_work.md:7` | Row has 1 cell in a 5-column table | Depends on the table-fixing script; `class_3/12_help_with_ex.md:34` does the same job with four cells |
| E4 | `class_8/4_adv_place.md:16` | `**-to** “from a place”` is a table row, while `-ttha` and `-hiṃ` are separate captions with their own tables | Sub-heading buried mid-table |
| E5 | `class_10/7_home_work.md:11` | `## Extra Reading` follows a list item with no blank line | Heading is parsed inside the list item |
| E6 | `class_1/index.md:62-63` | List follows `Optional:` with no blank line | Not parsed as a list |
| E7 | `class_2/2_alphabet.md:44-45` | Bold caption and paragraph with no blank line between | Run together |
| E8 | `class_11/3_adj.md:7-9` | Three example lines with no blank lines or breaks | Collapse into one line |
| E9 | `class_4/7_basic_assim.md:43-44` | Rule and example joined by a trailing-space break; every other rule on the page uses a blank line | Different spacing for this one rule |
| E10 | `class_12/3_card.md:138` | Three spaces used as a column separator | Collapses to one space |
| E11 | `class_14/4_ptp.md:126-128` | Footnote 28 says "This list is meant to show…", but the list is an ordinary paragraph after the footnote definition | The list prints in the body; the note about it prints at the foot of the page |
| E12 | `class_11/5_home_work.md:25` | `\>` at line start | A literal ">" instead of a block quote |
| E13 | `class_10/2_prp.md:5`, `:7` | `“dīghaṃ assasāmī’ti` | Opening double quote closed by a single quote |
| E14 | `class_10/2_prp.md:191` | `“I will breathe in **gladdening** the **mind” he trains,**` | Bold swallows the closing quote and "he trains,"; line 193 is correct |
| E15 | `class_10/2_prp.md:148` | `**Masculine ending in -anta (**like bhagavant**)**` | Broken bold; the other five captions are `**…** (like …)` |
| E16 | `class_3/7_root_4.md:7` | `**ṇā** (**ṇo)[^10]**` | Bold opens inside the parenthesis and closes after the footnote |
| E17 | `class_8/3_fem.md:71`; `class_10/2_prp.md:144`; `class_10/3_pron.md:63`, `:181`, `:221`, `:222`; `class_12/3_card.md:73` | `m**ātu**`, `gaccham**ānassa**`, `**tāsānaṃ**`, `**yāhi**`, `**tiṇṇannaṃ**` | Bold marks the wrong part of the word |
| E18 | `class_14/4_ptp.md:105`, `:109` | Trailing `<br>` at the end of three cells | Empty line inside the cell |
| E19 | `class_11/3_adj.md:24-26` | `*a`, `*ana`, `*ī` with an unescaped asterisk | Works today only because each line has a single `*`; everywhere else it is `\*` |
| E20 | `class_12/5_kahap.md:3` | Image has empty alt text | No description for screen readers or when the image fails |

Also: hard-wrapped paragraphs in `class_10/3_pron.md:238-240`, `class_13/3_pass_verb.md:71-72`, `class_13/4_pprp.md:46-47` (nowhere else in the course); trailing whitespace in `class_3/11_histor_pr.md:3`, `class_4/7_basic_assim.md:43`, `class_11/3_adj.md:5`; runs of blank lines in `class_4/9_masc_i.md:19-20`, `class_4/12_root_huu.md:10-12`, `:20-22`, `class_11/3_adj.md:14-15`, `:32-33`, `:119-120`, `class_14/5_home_work.md:19-20`.

### Raw HTML

`<br>` appears on 414 lines in 41 files. All but one (`class_2/2_alphabet.md:44`, inside a bold caption) are inside table cells. This conflicts with the project rule "NEVER use raw HTML … in the source files". It is clearly the established way to stack forms in a cell, so this is a policy decision rather than a list of defects: either the rule gets an explicit exception for `<br>` in table cells, or the tables need a script-level solution.

## F. Cross-file convention drift

| # | Item | Variants found |
| --- | --- | --- |
| F1 | Case labels in declension tables | `1. Nominative` (classes 2, 4, 5 pronouns); `1. nom` / `3. instr` (class 5 -ī, class 6 bhikkhu); `1.nom` / `3.inst` (49 tables); `3.instr` (class 12 and two class 5–6 tables, 12 in all); `8. voc` with a space (`class_11/3_adj.md:60`, `:88`) |
| F2 | Singular / plural header row | Present in classes 2 and 4; absent in almost every declension table from class 5 on |
| F3 | Conjugation tables | Header puts "plural" over the English column (`class_3/3_preset.md:25`, `7_root_4.md:39`, `8_root_5.md:27`, `10_root_8.md:39`, `:48`, `class_4/10_aor.md:49`, `class_5/3_future.md:55`). Pronouns *so / te* shown in some tables and not others. Class 7 optative and class 13 passive tables have no English columns |
| F4 | Bold boundary of endings | `vada**ti**` vs `vad**antu**`; `gacche**yya**` (class 7) vs `dīy**eyya**` (class 13); `ima**ssa**` vs `im**esaṃ**` vs `imes**aṃ**`; `vīsat**iyā**` vs `vīsati**yaṃ**`; `sāvak**aṃ**` vs `**sāvakena**` |
| F5 | Section captions | Sometimes a heading, sometimes a bold paragraph, on the same page: `class_2/3_decl_nouns.md:60` ("3. The Instrumental Case" is bold, cases 1, 2, 4–8 are H2); `class_10/3_pron.md:87` (*eta* is H2; *ta*, *ima*, *ya* are bold); `class_14/2_caus_verb.md:67` (Example 3 is bold; 1 and 2 are H3) |
| F6 | Heading capitalisation | "How to form …" (classes 2–13) vs "How To Form …" (`class_13/4_pprp.md`, all of class 14). "Masculine Noun ending in -i" (class 4) vs "Masculine nouns ending in -ī" vs "Feminine Nouns ending in -ā" |
| F7 | Root group titles | Hyphen for groups 1, 2, 4, 5, 6, 8; en dash for groups 3 and 7. "Root Group 8", "group 8", "8th conjugation group" all used |
| F8 | Root notation | `√dhar 8 \*e` vs `√mant 8 aya` vs `√dis 8 e`; `abhi + √nand` vs `abhi √nand` (`class_14/4_ptp.md:60-64`); `+ etc` vs `+ etc.`; `**bhū 1 a (be)**` without √ (`class_14/3_caus_pass.md:43`) |
| F9 | Grade terminology | guṇa is called "strengthened", "medium" and "strong"; vuddhi is "lengthened", "strong" and "long" (`class_4/4_vuddhi.md:3`, `:5`, `:67`, `:88`). `class_14/2_caus_verb.md:97` calls a > ā "strengthened" |
| F10 | Citation placement and style | After the quote in parentheses (most pages); before the quote (`class_6/4_subst.md`, `class_6/5_and_or.md`, `class_14/3_caus_pass.md`); on its own line (`class_5/7_with.md:17`); italic with sutta name (class 10 review and `2_prp.md`); bare (`class_14/4_ptp.md:5`). Reviews in classes 3 and 4 leave "VIN PAT NID" unlinked |
| F11 | "Simplified" marker | `(simpl)` ×10, `simpl` ×9, `modified` ×2, `(modif)` ×1, `very very modified` ×1 |
| F12 | Apostrophes and quotes | Sandhi apostrophe: curly `’` 41 times, straight `'` 21 times. Double quotes: curly on 132 lines, straight on 12 (homework pages of classes 5–8, `class_8/1_review.md`, `class_10/6_loc_gen_abs.md`, `class_12/1_review.md`, `class_12/5_kahap.md`, `class_14/3_caus_pass.md`) |
| F13 | Abbreviations | `masc.` / `pr.` with full stops (class 2) vs `ind`, `adv`, `pr`, `card`, `m` without (`class_9/3_inf.md:88-104`, `class_13/2_adv.md`); `acc s`, `nom. s.` vs `sg`; `pass.pr` vs `pass pr`; `BD`, `sk`, `Sk` never expanded |
| F14 | Page ranges and list markers | `p1-9`, `p10 – 13`, `p105 - 110`, `p85–87`; "p… (topic)" vs "Topic (p…)" in class 13–14; `1.␣␣` vs `1.␣`; escaped pseudo-lists (`1\.`, `\-`) alongside real lists |
| F15 | Spelling of Pāli words | *paṭhaviṃ* (`class_5/5_trans.md:7`) vs *pathavī* (`class_4/2_dpr_tpr.md:13`, `class_8/3_fem.md:32`, `class_10/3_pron.md:145`); *vy-* (`class_14/4_ptp.md:42`) vs *by-* (`:128`); compounds hyphenated or not (`maccha-gumbaṃ` and `macchagumbaṃ` four lines apart in `class_10/2_prp.md:25`, `:29`); capitalised Pāli sentence only at `class_3/11_histor_pr.md:10` |
| F16 | Homework pages | "from Anki Deck" present in classes 1–3, missing before “Grammar Pāli Class” from class 4 on; "DPR/TPR" vs "DPR / TPR"; "2-5" vs "2–5" vs "up to 2–5"; "Extra:" vs "Optional:"; the SBS kuṭi link only in class 11; class 12 has no Extra Reading table; three sets of word-for-word duplicate footnotes (14 = 15 = 19; 20 = 21; 22 = 23), with "mūla" / "Mūla" varying between the first two sets |

"Pāli" is used 125 times. "Pāḷi" appears 12 times, all in the book title "A Bhikkhu Māgadhabhāsā (Pāḷi)", so that is consistent.

## G. Links

| # | Location | Link | Status |
| --- | --- | --- | --- |
| G1 | `class_1/index.md:52` | `sasanarakkha.github.io/study-tools/anki-decks/sbs-pali-english-vocab.html` | 404 |
| G2 | `class_1/index.md:53` | `sasanarakkha.github.io/study-tools/anki-decks/patimokkha-word-by-word.html` | 404 |
| G3 | `class_1/index.md:54` | `http://filesrv1:8083/home/index.html` | Local-network host; unreachable for any reader outside that network |
| G4 | `class_6/3_masc_uu.md:1`, `class_5/4_masc_ii.md:28` | Anchors `#declension-of-u-masc` (on the -ū page, same id as the -u page) and `#declension-of-i-masc_1` (on the -ī page) | They resolve, but the ids name the wrong declension. `class_8/3_fem.md` already uses the `-ii` / `-uni` pattern |

Passing: all 82 `s.dhamma.gift` links; `dpdict.net`, `docs.ankiweb.net`, `digitalpalireader.online`, `americanmonk.org`, YouTube and Wikipedia (HTTP 200); all local file links, including the two into `docs/ipc/class_18/` and the vocabulary pages; all `#anchor` targets. The Google Docs and Forms links were not requested.

`class_4/13_home_work.md:4` mentions "video find-words-dpr.mkv" with no link to it.

## H. Data to re-verify

| # | Location | Concern | Conf. |
| --- | --- | --- | --- |
| H1 | `class_5/2_pers_pron.md:25`, `:56-61` | `ahaṃ` 14 232 and `tvaṃ` 16 207 in the four Nikāyas look too high next to `bhagavā` 4 803 from the same corpus (`class_6/4_subst.md:70`) and next to `tayā` 44, `tava` 46, `tuvaṃ` 32. | 6 |
| H2 | `class_2/3_decl_nouns.md:183-185` vs `class_9/2_nt.md:3`, `:91` | Neuter nouns: 15 199 (2023) vs "more than 17 000" (2025); neuter -i and -u together 452 vs "-u … at most 400". Different years, but the page does not say the earlier table is out of date. | 7 |
| H3 | `class_14/4_ptp.md:124` | "some of which are used around 1000 times". The highest count in the list as printed is `gahetabbaṃ (223)`. The list stops at *paṭi-*, so this could not be settled. | 6 |
| H4 | `class_14/4_ptp.md:128` | The list contains unsegmented sandhi strings that are not single potential participles: `asevitabbopi`, `aviññātamajānitabbaṃ`, `cittamupanetabbaṃ`, `gāḷhamogāhitabbaṃ`, `hāsamabhijanetabbaṃ`, `nibbānamadhigantabbaṃ`, `nappaṭippassambhetabbāṭṭhārasakaṃ`, `naupasampādetabbekavīsativāro`, `niddisitabbāvayavena`. | 8 |
| H5 | `class_2/2_alphabet.md:103` | `avadhyai (disregards)` is not a recognisable Sanskrit finite verb form. | 6 |
| H6 | `class_12/3_card.md:186-228` | "the only numbers … covered by DPD so far": 17 and 19 are absent although 17 is in the table above; the fraction `1/16 soḷasī` sits in a list of cardinals; 15 is given as two forms here and three at `:119`; `cattārīsa` / `cattālīsā` end differently. | 7 |

Arithmetic that was checked and is correct: masculine 11 834 + 1 549 = 13 383 and 88 %; neuter 14 747 + 452 = 15 199 and 97 % (`class_2/3_decl_nouns.md:179-186`); zero counts for the six large numbers (`class_12/3_card.md:236-241`).

## Suggested order of work

1. Section A items with confidence 9–10 and all of section D: unambiguous, small edits.
2. Section B: decide the canonical form set per paradigm (DPD inflection templates), then align every table.
3. Section A items below 8 and section H: look each one up in DPD first.
4. Sections E and G: format and link repairs.
5. Section F: agree the conventions once, then apply them, preferably by script.

Every edit to `docs/` must keep the data-preservation rule: corrections change a form or move a row, they do not delete content.
