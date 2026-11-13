# IPC audit — `docs/ipc/`

Date: 2026-11-13
Scope: all Markdown files under `docs/ipc/` (index + classes 16–28; 136 files, 8 437 lines, 3 694 table rows, as counted by `mech_checks.py`).
No file in `docs/` was modified. This is a findings list only.

This file replaces the audit of 2026-11-12 (started 2026-11-10), which was written before `kamma/audit/audit-guide.md` existed and without any DPD lookup. It is the result of two passes over every slice: a fresh read by the guide's full checklist, and a re-check of every row of the old audit. A row that comes from the old audit ends its `Problem` with `(old <id>)`; the ids were given to the old rows by category and order (`A1`, `A2`, …) when the old file was frozen.

Related to #6 Course enhancement with AI

## Method and limits

| Check | How | Result |
| --- | --- | --- |
| Freeze of the old audit | `git show HEAD:kamma/audit/ipc-audit.md` into `kamma/audit/scratch/ipc/old-audit.md`, each row of sections A–H numbered | 492 ids: A 72, B 61, C 60, D 82, E 41, F 121, G 0, H 55 |
| Mechanical checks | `uv run python kamma/audit/scripts/mech_checks.py docs/ipc --folder-footnotes --links-out kamma/audit/scratch/ipc/links.txt` | 2 table column mismatches, 24 index/H1 differences, footnotes 23 refs / 23 defs, 5 "raw HTML" lines (false positives), 1 file without a final newline (Mechanical detail, M1–M4) |
| Non-sutta links | `curl -s -o /dev/null -w '%{http_code}' -L --max-time 15 <url>` for each link not on `s.dhamma.gift` | 2 links: 1 returns 404 (row in G), 1 Google Form skipped (M5) |
| Sutta links | `uv run python scripts/check_sutta_links.py docs/ipc` | 37 links / 23 pages, all pass |
| Full read of every file | Line by line, by the main session, 10 class slices and 1 cross-file slice; the guide's "What to look for" list and categories A–I applied to each | Done; every slice file ends with its checklist note. 727 rows before the DPD round |
| Re-check of the old audit | Every old row kept, corrected or dropped, slice by slice | 415 old ids are carried by a row here; 77 were dropped, each with its reason (see "Old rows dropped") |
| DPD lookups | `uv run python kamma/audit/scripts/dpd_lookup.py <lemma> …`, run once over the 436 lemmas the reader had listed as suspicious | 217 rows waited for it: 123 dropped because DPD agrees with the text, 94 finalised against the DPD entry. 8 more rows that had not been marked as waiting were dropped for the same reason, and 1 was restored by the cross-check. 18 lemmas are not DPD headwords (M6) |
| Old-id accounting | Shell loop over the 492 ids: `grep -qF "(old $id)"` in the slice files, or `grep -q "^- $id "` in the dropped list | 0 missing, after the read and again after the DPD round |
| Cross-check with the key audit | One-off token match of the A, B and C rows against the rows of `ipc-key-audit.md` (3 199 candidate lines, 221 tokens), then a search of the key rows for every form, root and gloss that a row here deals with | 2 overlaps aligned (see "Cross-check with the key audit"); no other conflict found |
| Excerpt check | `uv run python kamma/audit/scripts/verify_rows.py docs/ipc …` on every slice file and on this file: each backtick excerpt in `Current` searched in the cited file within 2 lines of the cited line | OK 1037, FAIL 0 (slices and final); 0 rows with no source file |
| Merge | `uv run python kamma/audit/scripts/merge_audit.py kamma/audit/scratch/ipc/merge.toml` | This file |

Fresh-pass checklist (items the old audit had not applied): root spelling against DPD; `pati`/`paṭi` in analysis vs result; examples that do not illustrate their own heading; summary and reference tables against the lesson tables; paradigm cells; quoted verses (spelling, label vs link anchor); number statements against a count of the items; one word glossed in different ways; bold cutting a cluster or spanning `<br>`, quotes or full stops; `(*term)*`; list numbering; heading drift; hard wraps; lower-case sentence starts; the new mechanical items (footnotes, NBSP, zero-width and non-NFC characters, heading levels, convention counts); category I.

Not verified:

- The DPD lookups were deferred to one run: the reader listed what looked suspicious, and only those 436 lemmas were looked up. A form that did not look suspicious rests on the reader's knowledge of the language. That knowledge proved weak here: DPD agreed with the course text in more than half of the doubts. Each row carries a confidence score (1–10). Below 8, check DPD or the text before changing anything.
- `dpd_lookup.py` prints headwords: no inflection tables and no root meanings. Rows that say `DPD lookup` name a form, an inflection or a root gloss that the run could not settle.
- The number after a root in the lookup output is DPD's homonym number, not the root group.
- Where DPD and the course agree, the row was dropped even if another grammar analyses the word differently (`√ādā` as a root, `vaṇṇa` from `√var`, `manda` from `√mad`). DPD is the course's reference.
- Canonical wording was not compared with a text edition, and no Kaccāyana edition was consulted. Rows that depend on a reading say `verify`.
- The link checker proves that the page and anchor exist, not that the sentence is in that sutta. The Google Form link was not opened.
- The cross-check with the key audit works on shared words. A conflict that uses different words for the same form may have been missed.
- Rendered output (site, PDF, DOCX) was not built.

Paths below are relative to `docs/ipc/`. In `Current`, `\|` is a table pipe in the source, and ` / ` separates excerpts from different lines.

## Summary

| Category | idx–16 | 17 | 18 | 19–20 | 21–22 | 23 | 24–25 | 26–27 | 28a | 28b | cross | Total | Conf. ≥ 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A. Pāli and grammar content errors | 3 | 7 | 4 | 9 | 7 | 2 | 7 | 7 | 7 | 5 | 0 | 58 | 37 |
| B. Tables, paradigms and lists that disagree with each other or themselves | 12 | 5 | 8 | 11 | 9 | 4 | 10 | 7 | 9 | 5 | 1 | 81 | 33 |
| C. Translation and gloss problems | 16 | 7 | 6 | 11 | 2 | 6 | 10 | 11 | 7 | 4 | 2 | 82 | 26 |
| D. English typos and grammar | 11 | 9 | 11 | 14 | 11 | 7 | 9 | 6 | 11 | 5 | 0 | 94 | 62 |
| E. Markdown defects that affect rendering | 5 | 5 | 9 | 8 | 4 | 2 | 9 | 3 | 4 | 1 | 1 | 51 | 41 |
| F. Convention drift | 22 | 24 | 17 | 27 | 16 | 10 | 18 | 12 | 8 | 8 | 9 | 171 | 102 |
| G. Links | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 1 |
| H. Data to re-verify (forms, references, counts) | 9 | 5 | 2 | 6 | 3 | 2 | 4 | 1 | 2 | 1 | 1 | 36 | 2 |
| I. Further details on the material under review | 2 | 3 | 1 | 2 | 2 | 2 | 3 | 2 | 1 | 1 | 4 | 23 | 8 |
| **Total** | **80** | **65** | **58** | **88** | **54** | **35** | **70** | **49** | **49** | **31** | **18** | **597** | **312** |

A row often covers several locations, so the number of places to edit is higher than the row count.

Overall confidence: 9/10 that the quoted text is where the row says (scripted). 8/10 for categories D, E, F and G (visible in the source). 7/10 for A, B, C and H as a group: DPD was consulted for every form that looked doubtful, but no text edition was. Use the per-row score.

## Decisions for the owner

These are not decided in the audit; the rows say `owner decision`, or give both options:

- `# Homeless work` as the title of all 13 home-work pages: intended or not.
- `<br>` in table cells (136 occurrences) and `{: .align-right }` (4, in `class_20/5_ex.md`) versus the "no raw HTML in sources" rule.
- `Pāli` (53 times) or `Pāḷi` (once, class 18) in running text.
- One term for the `-tvā` / `-ya` form: `ger.` / gerund or `abs.` / absolutive. The key has the same drift (`ipc-key-audit.md`), so one decision serves both.
- Kaccāyana citation style (three styles; counts in the F row of the cross slice).
- UK or US spelling.
- The Pāli term in an H1: italic (classes 16, 17, 19, 21, 22) or plain (classes 18, 23).
- The right address for the dead link in `class_28/3_home_work.md:17`.
- The two numbering series in `class_17/index.md`.
- One fixed English rendering per sense for the terms that recur with several (`āsava`, `hirottappa`, `domanassa`, `bhagavā`, `tathāgata`); a short course glossary would hold them. The key audit asks the same for `bhagavā` and `tathāgata`.

## What the DPD round changed

The old audit and the fresh read both judged Pāli forms from memory. The lookup of 436 lemmas showed how often that fails:

- 123 of the 217 waiting rows were dropped: DPD has the form, root, construction or gloss that the course gives.
- 8 rows that had not been marked as waiting were dropped as well, when the lookup of a neighbouring form contradicted them. The main ones: `√ādā` is a DPD root (old A33 and A56, confidence 8 and 9); the course's split of `nī` (with verbs and their derivatives) and `nir` (in negative compounds) is DPD's own (old B35, F117).
- Roots that the reader took for spelling drift are separate roots in DPD: `√khan` (hurt) / `√khaṇ` (dig), `√saj` / `√sajj`, `√dah` / `√ḍah`, `√kas` / `√kass`, `√cit` / `√citt`, `√vaddh` / `√vaḍḍh`.
- Root spellings that do differ from DPD (12, listed in the B row of the cross slice): `√dhu`, `√veth`, `√bruh`, `√saṃk`, `√sikh`, `√bhu`, `√thamb`, `√tir`, `√path`, `√pal`, `√ghaṇḍ`, and `√sajj` in `visaṃsaṭṭha`.

Note for the BPC audit: the old IPC row A56 said "`√ādā` is not a root … same defect as BPC audit A20". DPD lists `√ādā` as a root (`ādāna` = `√ādā + ana`, `upādi` = `upa + √ādā + i`), so that BPC row deserves a second look before it is applied.

## Old rows dropped

77 of the 492 old ids have no row here. The first 11 were refuted by the DPD sample taken while planning (Phase 0); the other 66 by the DPD round.

- A8 — DPD supports the text: `abbhaya` is a DPD headword (Phase 0 lookup)
- A9 — DPD supports the text: `ekagghana` is a DPD headword (Phase 0 lookup)
- A16 — DPD supports the text: `nissaṭa` is `nī + √sar` in DPD (Phase 0 lookup)
- A19 — DPD supports the text for `dubbaṇṇa` (Phase 0 lookup)
- A35 — DPD supports the text: `nīyati` "departs" is a DPD headword (Phase 0 lookup)
- A36 — DPD supports the text: `anupekkhati` is `anu + pa + √ikkh` in DPD (Phase 0 lookup)
- A37 — DPD supports the text for `dubbaṇṇa` (Phase 0 lookup)
- A39 — DPD supports the text: `nessati` under `√nas` (Phase 0 lookup)
- A41 — DPD supports the text: `apihālu` (Phase 0 lookup)
- A47 — DPD supports the text: `satīmant` is a DPD headword (Phase 0 lookup)
- A51 — DPD supports the text: `sāraṇīya` under `√raj` (Phase 0 lookup)
- H4 — DPD supports the text: vocchijjati = vi + ud + chijja + ti
- C8 — DPD supports the text: sāttha = in meaning; in spirit; (or) with meaning
- C13 — DPD supports the text: suvuṭṭhita / suhuṭṭhita = good wake up; pleasant rising; uṭṭhita = stood up, got up
- H1 — DPD supports the text: nusi = nu + asi, nuttha = nu + ettha (sandhi headwords)
- H2 — DPD supports the text: vāpi 2 = ve + api
- A13 — DPD supports the text: pulliṅga is masc
- B12 — DPD supports the text: sañchavī = saṃ + chavi + ī
- C14 — DPD supports the text: abhikkamati 3 = comes; comes out; approaches
- H8 — DPD supports the text: purakkhata = pura + khata
- H9 — DPD supports the text: pariccaja masc, rejection; disapproval
- H10 — DPD supports the text: addasā is labelled imperf
- A14 — DPD supports the text: vicikicchati is from √cit (desid of vi √cit); only tikicchati is from √kit
- A18 — DPD supports the text: paṭiggaheti is a headword, and DPD constructions also write pati + …
- C21 — DPD supports the text: dibbati 1 = shines; radiates
- C23 — DPD supports the text: ciṇṇa 2 = completed; fulfilled
- F41 — DPD supports the text: the DPD constructions have the same stems without √ (bhava, lattha, so, akāsi)
- H12 — DPD supports the text: acapala = na > a + pa + √cal > capal + a
- H13 — DPD supports the text: visajja is a headword, ger of vissajjati, √sajj
- H16 — DPD supports the text: sajju = sa + √div > dyu > jju + u
- A21 — DPD supports the text: kathina is a headword beside kaṭhina
- C29 — DPD supports the text: sīlabbata = precepts and practices; ethics and observances; rites and rituals
- C33 — DPD supports the text: adhi 1 = towards; up to; above
- H18 — DPD supports the text: samāsa = saṃ + √ās + a
- H19 — DPD supports the text: rukkhamūlika is typed kammadhāraya > bahubbīhi
- H21 — DPD supports the text: rāgadosa 2.1 = rāga eva dosa, ruined by desire
- A32 — DPD supports the text: ghāteti is from √ghaṭ 1
- H25 — DPD supports the text: chindīyati is a headword, pass of chindati
- H29 — DPD supports the text: vacati is a headword
- H30 — DPD supports the text: ārambhati is a headword
- B33 — DPD supports the text: two roots, √khaṇ (dig; palikhaṇati) and √khan (hurt; khata 1.1)
- B34 — DPD supports the text: purakkhatvā = pura + khatvā, purakkhata = pura + khata
- C36 — DPD supports the text: avajānāti 1 = denies; disagrees; does not accept
- C37 — DPD supports the text: okappeti = suspects (of); has a hunch (about)
- C40 — DPD supports the text: nigghosa 1.1 adj = silent; soundless; quiet
- H31 — DPD supports the text: accayati is a headword
- H32 — DPD supports the text: adhiggaṇhāti 1 = acquires; gains; possesses
- H34 — DPD supports the text: sadattha 1.1 = sat + attha, highest good
- B39 — DPD supports the text: both bhāviyati and bhāvīyati are headwords
- H39 — DPD supports the text: pavutta 2.1 = pp of pavapati, shed; cast off
- H40 — DPD supports the text: jāpeti is caus of hāyati (√hā), vipāceti is from √vac
- H41 — DPD supports the text: ṭhapiyyati is a headword
- A52 — DPD supports the text: ghacca and ghātetāya are from √ghaṭ 1, saṅghātaniya = saṃ + √ghaṭ > ghāt + *aniya
- B46 — DPD supports the text: kosajja is from kusīta and is constructed ku > ko + √sad + *ya, so both derivations stand
- B52 — DPD supports the text: √gal 1, base gaḷa
- H46 — DPD supports the text: āyasmant = āyas + mant; venerable; respectable
- H47 — DPD supports the text: daṇḍapāṇī and hirīmant are headwords
- H48 — DPD supports the text: bahutthika is a headword
- H49 — DPD supports the text: nirāsā + sa, tapas + sī
- H50 — DPD supports the text: damatha = dama + tha
- H52 — DPD supports the text: pesiya is from √pis 1
- A59 — DPD supports the text: viyārabbha = vi + [y] + ā + √rabh + ta
- A65 — DPD supports the text: hita = √dhā > (da)h + ita
- A66 — DPD supports the text: manda = √mad + na
- A67 — DPD supports the text: vaṇṇa = √var + na
- A68 — DPD supports the text: √bil > vil
- A69 — DPD supports the text: paṭibhāna 1.1 = pati + √bhaṇ > bhāṇ + *a
- A70 — DPD supports the text: atthi 2.1 and jhāyi 1.1 are masc agent headwords
- C56 — DPD supports the text: sugata 1 = faring well; going well
- A63 — DPD supports the text: sukhī, bhāgī and rajja are built on the root; dussīlya = dur + √sīl + a + ya / dussīla + ya
- A71 — DPD supports the text: āhāraṇa is a headword (ā + √har > hār + *aṇa)
- A72 — DPD supports the text: aratī, tuṭṭhī and ussoḷhī are headwords
- B35 — DPD supports the text: nī with verbs and their derivatives (nibbindati, nikkhamati, nissaraṇa, nissaṭa), nir in negative compounds (nikkuha, nicchāta, nibbhoga, nirupadhi)
- F117 — DPD supports the text: nī with verbs and their derivatives (nibbindati, nikkhamati, nissaraṇa, nissaṭa), nir in negative compounds (nikkuha, nicchāta, nibbhoga, nirupadhi)
- A33 — DPD supports the text: √ādā is a DPD root (ādāna = √ādā + ana, upādi = upa + √ādā + i)
- A56 — DPD supports the text: √ādā is a DPD root (ādāna = √ādā + ana, upādi = upa + √ādā + i)
- F118 — DPD supports the text: vyākaraṇa and byādhi are the DPD headword spellings

## Fresh findings dropped after the DPD lookup

Fresh rows (no old id) that were written as "to confirm" during the read and dropped when DPD agreed with the text. They are listed so that the same doubts are not raised again:

- Sandhi and insertions as the lessons give them: `ajjatagge`, `tasmātiha`, `caturaṅgī`, `pāturahosi` (inserted `t`, `r`), `ajjaṇho`, `avijjākkhandha` (beside `avijjākhandha`), `punappunaṃ` (`punaṃ ca punaṃ ca`).
- Forms that are DPD headwords: `paṭiggaheti`, `vacati`, `ārambhati`, `chindīyati`, `samādhiyati`, `juhati`, `accayati`, `ṭhapiyyati`, `bhāviyati` and `bhāvīyati`, `paññapeti` and `paññāpeti`, `pāpurati` and `pārupeti`, `upaṭṭhapeti` and `upaṭṭhāpeti`, `veyaggha` and `veyyaggha`, `pahantvāna`, `visajja`, `pariccaja`, `patilīna`, `māraṇiya`, `āhāraṇa`, `aratī`, `tuṭṭhī`, `ussoḷhī`, `atthi` and `jhāyi` (masc agent nouns), `daṇḍapāṇī`, `hirīmant`, `bahutthika`, `āpas`, `thāmas`, `vāyas`, `bhūma`, `kathina` (beside `kaṭhina`).
- Roots and constructions that agree with DPD: `√ādā`; `√ghaṭ` for `ghāteti`, `ghacca`, `ghātetāya`; `√his` for `vihiṃsati` and `viheseti`; `√nadh`; `√badh`; `√dhū`; `√ḍaṃs` for `saṇḍāsa`; `√cit` for `vicikicchati`; `√vad` for `vattuṃ`; `√dah` for `daḷha`; `√mun` for `muta`; `√tij` for `tibba` and `tippa`; `√var` for `vaṇṇa`; `√mad` for `manda`; `√bil` for `āvila`; `√bhaṇ` for `paṭibhāna`; `√kat` for `kaṇṭaka`; `√buh` for `abbuhati`; `√kas` for `ukkaṃseti`; `√ās` for `samāsa`; `√yam` for `anuppavecchati`; `√chand` for `chādeti` "pleases"; `√dā` for `niddāyati`; `√dhā > (da)h + ita` for `hita`; `pura + khata` for `purakkhata`; `sat + attha` for `sadattha`; `abhi + pa + √atth` for `abhipatthayati`; `ni` in `nissayati`; `acapala` by metathesis; `sajju` from `√div`; `āyas + mant`; `dama + tha`; `tapas + sī`; `kati + yāyana`.
- Genders, parts of speech and compound types that agree with DPD: `pulliṅga` masc; `addasā` imperf; `āgāḷha` pp; `taccha` adj and nt; `kathika` as both a primary and a secondary derivative; `sukhī`, `bhāgī` and `rajja` built on the root; `rukkhamūlika` as `kammadhāraya > bahubbīhi`; `rāgadosa` as `rāga eva dosa`.
- Glosses that are DPD senses: `sāttha` "in meaning", `suvuṭṭhita` "good wake up", `svāgata` "mastered", `bhabba` "possible", `abhikkamati` "comes out", `nikkhitta` "discarded", `catugguṇa` "folded four times", `anuṭṭhita` "established", `anuddhaṃseti` "attacks", `accāyata`, `accāraddha`, `dibbati` "shines", `ciṇṇa` "completed", `dussati` "misbehaves", `āraddha` "aroused", `sīlabbata` "rites and rituals", `adhi` "up, towards", `thunāti` "praises", `khiyyati` "criticises", `avajānāti` "denies", `okappeti` "suspects", `nigghosa` "silent", `adhiggaṇhāti` "possesses", `parāmasati` "strokes", `sampayojeti` "quarrels", `vuṭṭha` "lived", `pavutta` "cast off", `jāpeti` "confiscates", `pasāda` "brightness", `sati` "memory", `sādhu` "goodness", `sugata` "going well", `kāra` "smith", `karaṇa` "helpful", `dhāraka` "remembering", `ratha` "pleasure".

## Cross-check with the key audit

The rows of this audit were compared with `ipc-key-audit.md` wherever both touch the same form, root or gloss. Two overlaps were aligned:

- `gahetabba` (`class_27/2_kicca.md:35`) and the key's `gahetvā` (`ipc_key/23_class.md:570`): both now say that `gahe` is an irregular base, which the sign `ṇhā` does not produce. The row here (old B51) had been dropped in the DPD round and was restored at confidence 6.
- `bhagavā` and `tathāgata`: the cross-slice C row here now names the key audit's rendering (`the Blessed One`, `ipc_key/24_class.md:209`).

Agreeing without change: `ger` / `abs` and UK / US spelling are owner decisions in both audits; `pāva` is a perfect of `vadati` in both; the prefix is `nī` in `parinibbuta` and `niccheyya` (key) and in the verbs of class 23 (here); `veyaggha` is the derived adjective in both; `samādhiyati` is a passive in both.

## A. Pāli and grammar content errors

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_16/4_vowel_2.md:19 | `vā paro asarūpo.` | Kaccāyana 13 reads `asarūpā` (ablative); checked from memory, not from a text (old A1) | `vā paro asarūpā`; verify against a Kaccāyana edition | 7 |
| class_16/7_vowel_5.md:49 | `**ī**sī` / `mah**e**sī` | The word for "sage" is `isi` (DPD has no `īsī` "sage"); `mahā + īsī > mahesī` is DPD's "queen; royal consort", and the "great sage" is `mahā + isi > mahesi` (old A2) | `mah**ā** \| **i**si \| mah**e**si` under `ā + i > e` (DPD: `isi` sage, `mahesi` = `mahā + isi`); or keep `īsī` / `mahesī` and gloss `queen \| chief queen` (DPD `mahesī` 1.1 = `mahā + īsī`) | 8 |
| class_16/10_vowel_8.md:69 | `s**a** \| **d**iṭṭhi \| sa**n**diṭṭhi` | Not an insertion between two vowels (the second word starts with `d`), against the rule on line 5; the bold `d` marks a consonant as the second vowel (old A3) | DPD gives `sa + [n] + diṭṭhi` ("one's own belief"), so the insertion is sound, but it stands before a consonant: note the exception to the rule on line 5, and bold only the inserted `n` | 7 |
| class_17/5_cons_3.md:15 | `pātimokkañ’ca saṃvaro` | The verse (Dhp 185, DN 14) reads `pātimokkhe ca saṃvaro`; `pātimokka` also lacks `kh` (old A4) | `pātimokkhe ca saṃvaro` | 9 |
| class_17/5_cons_3.md:21 | `diṭṭasute sīlavate mute vā` | Snp 4.5 reads `diṭṭhe sute`; `diṭṭa` lacks `ṭh` (old A5) | `diṭṭhe sute sīlavate mute vā` | 9 |
| class_17/7_cons_5.md:3 | `When **ti** follows a vowel, it becomes **cc**` | Direction reversed: `ti` becomes `cc` when a vowel follows it (all six examples) (old A6) | `When **ti** is followed by a vowel` | 9 |
| class_17/3_cons_1.md:151 | `pat**i** \| **ph**arati \| paṭi**pph**arati` | `pati` in column 1, `paṭi` in the result (old A7) | `paṭ**i**` | 9 |
| class_17/1_alphabet_analys.md:25 | `**8 Semi-Vowels (antaṭṭha)**` | `antaṭṭha` covers y r l v (ḷ); s, h and ṃ are not semi-vowels (old A11) | `8 ungrouped (avagga)`, or split the row; `antaṭṭha` is not a DPD headword: DPD lookup | 7 |
| class_17/9_nig_2.md:30 | `sa**ṃ** \| **g**ha \| sa**ṅ**gha` | `gha` is not a word, and the bold is on `g`, not `gh` (the heading row has `gh`) (old A12) | `√**gh**aṭ` in the second cell (DPD: `saṃ + √ghaṭ + a`), or another example; bold `gh` | 7 |
| class_17/3_cons_1.md:46, 107, 161, 193 | `sakuṇa**ggh**i \| masc. hawk` / `catu**tt**āla` / `cha**bb**assa \| nt. six years` / `diṭṭha**ss**uta` | DPD confirms all four forms, but `sakuṇagghi` is feminine there, not masculine | `sakuṇa**ggh**i \| fem. hawk` (DPD: fem) | 8 |
| class_18/6_as_sum.md:15 | `ni √sa**j** **y**a \| nisa**jj**a` | `nisajja` is `ni + √sad + ya` (d + y), not j + y (old A15) | `ni √sa**d** **y**a \| nisa**jj**a` under d + y (DPD: `ni + √sad + ya`), or use `vi √bha**j y**a \| vibha**jj**a` (the lesson example) for j + y | 9 |
| class_18/9_ex.md:11 | `duppativijjha` | `pati` should be `paṭi` in the result (old A17) | `duppaṭivijjha` (the DPD headword; `duppativijjha` is not in DPD) | 9 |
| class_18/4_as_na.md:19; class_18/6_as_sum.md:22 | `√tir + na` / `√ti**r n**a` | DPD gives the root as `√tar` (`√tar > tir + na`); `√tir` is the changed stem, not the root (old H14) | `√tar \> tir + na` in both places (DPD) | 8 |
| class_18/3_as_ta.md:58; class_18/4_as_na.md:9 | `vi + saṃ + √sajj + ta \| visaṃsa**ṭṭh**a \| pp. separated` / `abhi + √sand + na \| abhisa**nn**a \| pp. filled up` | DPD derives `visaṃsaṭṭha` from `√saj`, not `√sajj`; gloss "separate; disconnected" | `vi + saṃ + √saj + ta` (DPD root `√saj`); `abhisanna` is confirmed | 7 |
| class_19/4_tap.md:93 | `## sattāmī tappurisa` | Misspelt; line 147 has `sattamī` (old A20) | `sattamī` | 10 |
| class_19/2_kamm.md:125 | `pa + vagga \> pavagga (group of labial consonants)` | `pavagga` is "the p-group" (letter name + `vagga`), not the prefix `pa` + noun; a wrong example for `pa-ādi-pubba-pada` (old A22) | replace (e.g. `pa + vacana \> pāvacana`); DPD: `pavagga` = "p-series; group of labial consonants beginning with the letter p" | 8 |
| class_19/2_kamm.md:77, 79 | `tathāgato *viya* sīho` / `buddho *viya* nāgo` | Analysis reversed: the comparison is the second member, so `sīho viya tathāgato` (a Tathāgata like a lion) (old A23) | Swap the members in the analysis | 7 |
| class_19/4_tap.md:73 | `het**unā** samuppanna` | `hetunā` is instrumental; the row is under the ablative (old A24) | `het**uto**` / `het**usmā**`, or move to tatiyā | 8 |
| class_20/2_bahub.md:101 | `kammadāraya` | Misspelt (old A25) | `kammadhāraya` | 10 |
| class_20/2_bahub.md:95 | `musāvadaṃ` | Short `a` (old A26) | `musāvādaṃ` (DPD: `musāvāda`) | 9 |
| class_20/2_bahub.md:13, 17, 23 | `**bahubbīhī** janapado` / `what part of speech is bahubbīhī?` | Long `ī`; the compound is `bahubbīhi` (line 7; line 19 `bahubbīhismiṃ`) (old A28) | `bahubbīhi` (the DPD headword) | 7 |
| class_20/4_change_comp.md:6 | `\| akkhi \| eye \| akkha \| akkhadassa \| judge; lit. sees with eyes \|` | `akkhadassa` is usually explained from `akkha` (die, or lawsuit), not from `akkhi` (eye) | DPD lookup: DPD builds `akkhadassa` on `akkha` (`akkhehi + dassa`), not on `akkhi`; check which `akkha` is meant before keeping the row as an example of `akkhi > akkha` | 5 |
| class_19/4_tap.md:101, 123, 137 | `bhūm**iyaṃ** + ṭha \> bhūmaṭṭha` / `vaḷav**ābhi**ratha` / `bandhan**ā**mokkha` | `bhūmiyaṃ` is the locative of `bhūmi`; DPD builds `bhūmaṭṭha` on `bhūma`. `vaḷavābhiratha` and `bandhanāmokkha` are in DPD as alutta compounds | `bhūm**asmiṃ** + ṭha` (DPD: `bhūma + ṭha`, sattamī tappurisa `bhūmasmiṃ + ṭha`); the two alutta compounds are confirmed | 7 |
| class_21/3_pass_refl.md:31 | `Sanskrit - vācya**te**` | The Sanskrit passive of √vac is `ucyate` (old A27) | `ucya**te**` | 9 |
| class_22/3_root_groups.md:7, 9 | `## 1. bhuvādigaṇa (-a-)` / `Group 1 bhūvādigaṇa roots` | Two spellings two lines apart (old A29) | `bhūvādigaṇa` (the DPD headword; `bhuvādigaṇa` is not in DPD) | 9 |
| class_22/3_root_groups.md:74 | `ṭhā + ṭhā \> tiṭṭhā \| tiṭṭhāti` | The present is `tiṭṭhati` (4_irreg_base.md:26 has `tiṭṭha \| tiṭṭhati`) (old A30) | `tiṭṭha \| tiṭṭhati` (`tiṭṭhāti` is not in DPD) | 9 |
| class_22/3_root_groups.md:56 | `transformed to **ay** and **av** according to **vuddhi**` | `i > e > ay`, `u > o > av` is guṇa; vuddhi gives `āy` / `āv` (old A31) | `guṇa` | 8 |
| class_21/3_pass_refl.md:25 | `In Sanskrit, passive and intransitive verbs **must** take the attanopada endings` | True of the passive; not of intransitive verbs (`bhavati`, `gacchati` are parasmaipada) | Drop `and intransitive` | 7 |
| class_21/7_perf.md:9 | `Its opposite is **sammukhā**` | The grammatical opposite of `parokkha` is `paccakkha` (Kaccāyana 417–418, quoted on 7_perf.md:3 and 8_imperf.md:3) | `paccakkha` ("before the eyes"), or keep `sammukhā` as a second word | 6 |
| class_22/4_irreg_base.md:28, 30, 45, 60 | `\| **√var** \| pura \| pāpurati \|` / `\| **√yam** \| veccha \| anuppavecchati \|` / `\| **√bhā** \| bhāhi \| bhāhiti \|` / `\| **√pal** \| palehi \| palehiti \|` | DPD gives the root of `palehiti` as `√palā`, not `√pal`; `pāpurati` (`√var`), `anuppavecchati` (`√yam`) and `bhāhiti` (`√bhā`) agree with DPD | `**√palā**` for `palehiti` (DPD: fut of `paleti`, `√palā`); the other three are confirmed | 7 |
| class_23/13_nii.md:7 | `\| √veth \| to twist \| nibbeṭheti \|` | The root is `√veṭh` (17_pari.md:8) (old A34) | `√veṭh` (DPD) | 9 |
| class_23/5_anu.md:9 | `\| √bruh \| to increase \| anubrūhayati \|` | DPD gives the root as `√brūh` (old H33) | `√brūh` (DPD) | 9 |
| class_24/5_caus_pass.md:24 | `ñāpē` | `ē` with a macron is not a Pāli letter (old A38) | `ñāpe` | 10 |
| class_25/5_taddh_2.md:87 | `\| navā \| + \*ika \| n**ā**v**ika** \| sailor \|` | "Boat" is `nāvā` (old A40) | DPD lookup: the DPD headword for "ship" is `nāvā`, but its construction of `nāvika` also writes `navā > nāvā + *ika`; check before changing to `nāvā` | 6 |
| class_25/5_taddh_2.md:175 | `\| gaṅga \| + \*eyya \|` | The river is `gaṅgā` (old A42) | `gaṅgā` (DPD: `gaṅgā + eyya`) | 9 |
| class_25/5_taddh_2.md:217, 220 | `from Kasi` / `from Kasi village` | Diacritic missing (`Rājagaha` has it on line 218) (old A43) | `Kāsi` | 9 |
| class_25/2_nouns.md:24 | `\| √ādā \| to take, eat \| + na \| ādāna \| eating \|` | The suffix cell has `+ na`; DPD has `√ādā + ana`. The root `√ādā` and the gloss "eating" (sense 2) are as in DPD (old A44) | `+ ana` (DPD: `√ādā + ana`) | 7 |
| class_25/5_taddh_2.md:192, 197 | `\| dāra \| + ka \|` / `\| paṭā \| + ka \|` | `paṭā` is not a word: DPD derives `paṭāka` from `paṭa`. `dāraka` is `dāra + ka` in DPD as well (old H44) | `paṭa` (DPD: `paṭa + ka`); `dāra + ka` agrees with DPD | 8 |
| class_24/1_pass.md:56; class_24/2_irreg_pass.md:92, 94 | `\| √add \| to afflict \| iya \| a**ṭṭ**iya \| aṭṭiyati \|` / `\| m \| **vu**ttika \| livelihood \|` / `\| adj \| pa**bhu**ti \| beginning with \|` | `vuttika` is an adjective in DPD, not a masculine noun "livelihood" (that is `vutti`) | `\| adj \| **vu**ttika \| living (in comps) \|` (DPD: adj, "living; practising; being in some state"); the other two agree with DPD | 7 |
| class_26/3_state.md:59 | `**ā**ṇaṇ**ya**` | The first nasal should be dental: `anaṇa > ānaṇya`. DPD confirms `ānaṇya` (Phase 0) (old A45) | `**ā**naṇ**ya**` | 9 |
| class_26/3_state.md:81 | `**a**dhipat**eyya**` | The form is `ādhipateyya` (the `\*` suffix lengthens the first vowel). DPD confirms it (Phase 0) (old A46) | `**ā**dhipat**eyya**` | 9 |
| class_27/2_kicca.md:132 | `\| √labh \| + \*ya \| la**ddha** \| to be obtained \|` | `laddha` is the pp (`labh + ta`, class 18); the ptp is `labbha`. DPD confirms it (Phase 0) (old A48) | `la**bbha**` | 9 |
| class_27/2_kicca.md:123 | `\| √bhu \| + \*ya \| bh**abba** \|` | The root is `√bhū` (old A49) | `√bhū` | 9 |
| class_27/3_kita.md:78 | `\| √sikh \| **+ ita** \| sikkh**ita** \|` | The root is `√sikkh` (2_kicca.md:53) (old A50) | `√sikkh` | 9 |
| class_27/2_kicca.md:143 | `\| √saṃk \| + \*iya \| saṅk**iya** \|` | The root is usually written `√saṅk` (old A53) | `√saṅk` (DPD) | 8 |
| class_27/3_kita.md:101; class_18/4_as_na.md:19 | `\| √tir \| **+ na** \| nitthi**ṇṇa** \|` / `√tir + na` | `√tir` again: DPD gives the root as `√tar`; see the p03 row | `√tar` (DPD: `nī + √tar > tir > thir + na`), as in the class 18 row | 8 |
| class_28/1_kita_1.md:602 | `\| abhi √vah \| to carry \| + **\*ana** \| adhiv**ā**h**ana** \| carrying \|` | The prefix in column 1 is `abhi`; the result has `adhi` (old A54) | `adhi √vah` (DPD: `adhi + √vah > vāh + *ana`) | 9 |
| class_28/1_kita_1.md:54 | `\| √saj \| to cling \| **+ ta** \| visa**ta** \| attachment \|` | The prefix `vi` is missing from column 1. The form `visata` itself is confirmed by DPD (old A58) | `vi √saj` in column 1 (DPD: `vi + √saj + ta`, "attachment; clinging") | 8 |
| class_28/1_kita_1.md:426 | `\| √mar \| to die \| **+ aṇa** \| mār**aṇa** \| killing \|` | The root vowel is lengthened, so in the file's own notation this is `\*aṇa` (or the causative base `māre`); it sits under `mar**aṇa**` with the same analysis (old A60) | show the causative base: `māre \| + aṇa` (DPD: `māre + aṇa`, from `māreti`) | 7 |
| class_28/1_kita_1.md:489, 567, 292, 508 | `\| √nhā \| to bath \| **+ aka** \| nhāp**aka** \|` / `\| √ar \| to move, attain \| **+ anā** \| app**anā** \|` / `\| su √bhū \| to be \| **+ ita** \| subhāv**ita** \|` / `\| vi √dis \| to see \| **+ aka** \| vipass**aka** \|` | The forms are built on a causative or present base (`nhāpe`, `appe`, `bhāve`, `passa`); the table shows root + suffix only, so the extra `p`, `āv`, `pass` are unexplained (file 2: see p10) (old A61) | Add the base, as class 27 does (`√bhū \| \*e \| bhāve`) | 7 |
| class_28/1_kita_1.md:512 | `suffix **ī** (Sanskrit -in) is used to form **possessive adjectives**` | "Possessive" describes the taddhita `ī` (class_26/1_having.md:34). The kita `ī` forms agent or habitual-action adjectives (`jīvī`, `apacāyī`) (old A62) | `agent adjectives`, or explain the overlap | 6 |
| class_28/1_kita_1.md:528 | `\| √dus \| to be corrupt \| **+ ī** \| dūsī \| corrupter \|` | The root vowel is lengthened (`u > ū`), which the file marks elsewhere with `\*` (line 723 `**+ \*aka** \| d**ū**s**aka**`) (old A64) | `dūse \| + ī` (DPD: `dūse + ī`, from `dūseti`), or `+ \*ī` with `d**ū**s**ī**` | 6 |
| class_28/1_kita_1.md:106 | `\| √thamb \| to be stiff \| **+ a** \| thamb**a** \| pillar \|` | "Pillar" is `thambha` (class_18/9_ex.md:15 has `√thambh + ta \| thaddha`); `thamba` is "clump of grass" | `\| √thambh \| to be stiff \| **+ a** \| thambh**a** \| pillar \|` (DPD: `thambha` pillar; `thamba` is "clump of grass", also from `√thambh`) | 8 |
| class_28/2_kita_less.md:203 | `\| √kuṭ \| to be crooked \| **+ \*i** \| k**o**t**i** \| end, point \|` | Dental `t`; the word is `koṭi` (the root in the same row is `√kuṭ`) (old A55) | `k**o**ṭ**i**` (DPD: `koṭi`; `koti` is not in DPD) | 9 |
| class_28/2_kita_less.md:493 | `\| √dis \| to see \| **+ tāvī** \| dass**āvī** \| has seen \|` | `dassāvī` is not formed with `tāvī`; the bold itself shows `āvī`, a separate suffix in the list of 1_kita_1.md:32 (`avī āvī`), and class_24/6_app.md:25–29 teaches `root + āvī` beside `root + tāvī` (old A57) | Remove it from the tāvī table, or replace it with a real `-tāvī` form | 8 |
| class_28/2_kita_less.md:16, 18 | `\| √dis \| to see \| **+ tar** \| dasse**tar** \| guide \|` / `\| √ghaṭ \| to strike, kill \| **+ tar** \| ghāte**tar** \| killer \|` | The forms are built on the causative base (`dasse`, `ghāte`); the table shows root + suffix only (file 1: see p09) (old A61) | show the base: `dasse \| + tar`, `ghāte \| + tar` (DPD: `dasse + tar`, `ghāte + tar`); the root `√ghaṭ` agrees with DPD | 7 |
| class_28/2_kita_less.md:39, 371, 440 | `\| √path \| to go, move \| **+ u** \| puth**u** \|` / `\| √kur \| to sound \| **+ ala** \| kul**ala** \|` / `\| √ṭhā \| to stand \| **+ ara** \| thāv**ara** \|` | DPD gives the root of `puthu` as `√puth`, not `√path`. For `kulala` and `thāvara` the roots are as in DPD, but the change (`kur > kul`, inserted `v`) is not shown | `√puth` for `puthu` (DPD: `√puth + u`); `kulala` (`√kur > kul + ala`) and `thāvara` (`√ṭhā + [v] + ara`) agree with DPD | 8 |
| class_28/2_kita_less.md:55, 107, 466, 480 | `\| √ghaṇḍ \| to speak \| **+ u** \| nighaṇḍu \|` / `\| √ghar \| to burn \| **+ ma** \| gham**ma** \|` / `\| √khi \| to live \| + \***tta** \| kh**etta** \|` / `\| √kus \| to fill, enfold \| **+ \*ta** \| k**o**ṭṭha \|` | DPD derives `nighaṇḍu` from `√ganth` with the prefix `nir`, not from `√ghaṇḍ` | `nir √ganth` for `nighaṇḍu` (DPD: `nir + √ganth > gaṇḍh + u`); the other three roots agree with DPD | 7 |

## B. Tables, paradigms and lists that disagree with each other or themselves

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_16/10_vowel_8.md:5, 92, 101 | `**y v m d n t r l**` / `**ḷ (only with cha)**` / `**h (very rare)**` | The list has `l`, the section has `ḷ`; the section `h (very rare)` is not in the list (same on line 112 and in 12_vowel_ref_table.md:18) (old B1) | Align the list and the sections (`ḷ`, add `h`) | 8 |
| class_16/9_vowel_7.md:25; class_16/12_vowel_ref_table.md:41 | `s**va**haṃ` / `svahaṃ =` | The same pair `so + ahaṃ` gives `svāhaṃ` on line 5; `svahaṃ` is attested only as a metrical shortening (SN 4.23, quoted in class_17/5_cons_3.md:41) (old B2) | DPD has both `svahaṃ` and `svāhaṃ` (`so > sv + ahaṃ`); add a note on line 25 that both results occur (the short form in verse) | 6 |
| class_16/12_vowel_ref_table.md:17 | `**o** \| a+e` | `a + e > o` is taught in no lesson and is absent from the Alternative table (column a, row e holds only `e`, line 88) (old B3) | Remove `a+e`, or add the lesson example it stands for | 8 |
| class_16/12_vowel_ref_table.md:17 | `**ū** \| ū\<i` | `ū + i > ū` has no lesson example, and the Alternative table cell (column ū, row i, line 84) is empty (old B4) | Align the two tables | 7 |
| class_16/12_vowel_ref_table.md:7 | `**yā** \| i+a` | The lessons give `i+a > ya`, `i+ā > yā`, `ī+a > yā`; the Alternative table (column i, row a, line 82) has no `yā` (old B5) | Remove `i+a` under `yā`, or add the lesson example | 7 |
| class_16/12_vowel_ref_table.md:14 | `**ā** \| ā\<a` | The lesson (5_vowel_3.md:36) teaches `ā>+a` (elide and lengthen); the table lists `ā<a` and omits `ā>+a` (old B6) | `ā\>+a`, or list both | 6 |
| class_16/12_vowel_ref_table.md:9 | `\| \| \| **ī** \| ā\>+i` | Two empty cells split the **a** column; the `i\>a` row follows the gap on line 10 (old B7) | Move `i\>a` up so the column is contiguous | 8 |
| class_16/12_vowel_ref_table.md:5, 6, 9, 10 | `a\>a` / `a\<i` / `ā\>+i` / `i+\<a` | The notation (`>`, `<`, `+`) is never explained; there is no legend (old B8) | Add a one-line legend | 8 |
| class_16/12_vowel_ref_table.md:8, 84 | `**e** \| ā+i` / `\| **i** \| i a ā e \| i ā ī \|` | The reference table and the rule (7_vowel_5.md:9) give `ā + i > e`; the Alternative table cell (column ā, row i) has `i ā ī` without `e`. No lesson example for `ā + i > e` | Add `e` to the cell, or drop `ā+i` | 7 |
| class_16/13_home_work.md:20, 26 | `\| **na-** \| ind \| neg \| not \|` / `\| **na-** \| ind \| neg \| not[^2] \|` | The `na-` and `ahaṃ` rows appear twice (lines 20–21 and 26–27); the footnote does not clearly explain the repetition (old B9) | Clarify the footnote or drop one pair | 7 |
| index.md:67 | `- [Three Voices: Active, Reflexive and Passive](class_21/2_voices.md)` | `class_21/1_review_verbs.md` (Review of Verbs) is missing from the root index; it is in `class_21/index.md:3` (old B22) | Add the entry | 9 |
| index.md:15 | `- [Vowel Sandhi Reference Table](class_16/12_vowel_ref_table.md)` | The root index stops here; `class_16/index.md:15` also lists `13_home_work.md`. The root index leaves out the homework page of every class (13 pages), so this looks intended (see p11) | None, unless the owner wants the homework pages in the root index | 4 |
| class_17/1_alphabet_analys.md:49, 62 | `Unvoiced<br>(*aghosa*) \| Voiced<br>(*ghosavant*) \| \| \|` | The header cells do not sit over their columns: `Voiced` is above the unvoiced aspirates (old B10) | Reorder the cells (`Unvoiced \| \| Voiced \| \| \|`) | 9 |
| class_17/8_nig_1.md:29 | `catutthasmi**ṃ** \| \| **ṭh**āne` | The row sits in the dental `th` slot but repeats `ṭh` (line 26) (old B11) | An example with `th` | 9 |
| class_17/2_cons.md:5 | `There are three basic types of Consonant Sandhi` | Three types are listed (lines 7–11); the class then gives five possibilities (adds `so > sa`, `ti > cc`) (old B13) | Reword | 7 |
| class_17/17_nig_10.md:3 | `A **ṃ** may be inserted **before** a **vowel** or a **consonant**.` | All three examples (lines 15–17) are before a consonant; no vowel example | Add a vowel example, or drop "a vowel" | 6 |
| class_17/9_nig_2.md:50, 51 | `sa**ṃ** \| √ḍaṃs \> **ḍ**ās + \*a \| sa**ṇ**ḍāsa` / `sa**ṃ** \| **ṭh**āna \| sa**ṇ**ṭhāna` | The `ḍ` row stands before the `ṭh` rows; every other table follows the order of the letter row above it | Move the `ḍ` row below `ṭh` | 7 |
| class_18/8_as_misc.md:15 | `sat \| dhamma \| t + dh \> ddh \| saddhamma` | The row is in the `prefix \| root` table for ud-, dur-, nir-; `sat` is not a prefix and `dhamma` is not a root (old B14) | Move it out, or relabel the columns | 8 |
| class_18/10_irreg_masc.md:100, 102 | `ra**ññaṃ**<br>rāj**ānaṃ**<br>rāj**ūnaṃ**` / `ra**ññaṃ**<br>rāj**ūnaṃ**<br>rāj**ānaṃ**` | Dative plural and genitive plural list the same forms in a different order (old B15) | Same order | 8 |
| class_18/10_irreg_masc.md:44 | `**manase**` | Bold marks the Sanskrit forms that explain the Pāli ones; the Pāli dative is `manaso` (from `manasaḥ`, not bold), and `manase` has no Pāli reflex in the table above (old B16) | Bold `manasaḥ` instead | 7 |
| class_18/1_phonetic.md:23, 33 | `√bu**dh + t**a \> bu**dht**a \> bu**ddh**a (pp. known)` / `√la**bh + t**a \> la**bht**a \> la**ddh**a (pp. obtained)` | The same change (voiced aspirate + `t` > `ddh`) is "Progressive" on line 23 and "Reciprocal" on line 33 | Put both under one type | 7 |
| class_18/6_as_sum.md:12, 18, 31, 41 | `sāka**cch**ā` / `ka**ññ**ā` / `so**tth**i` / `**by**anta` | The summary uses examples that are in no lesson table of the class (also `nisajja` 15, `abhiruyha` 43), and it leaves out two lesson headings: `jj + t > ṭṭh` and `t + t > tt` (3_as_ta.md:53, 60) | Use lesson examples; add the two missing lines | 6 |
| class_18/6_as_sum.md:41 | `\| by \| vi \| **vi** anta \| **by**anta \|` | Not an assimilation of two consonants; the second column has `vi` where every other row has `x + y` | Remove the row, or `v + y` with a note | 7 |
| class_18/3_as_ta.md:50 | `ni + √mujj + ta \| nimu**gg**a \| pp. immersed` | A root in `jj` under the heading `j + t > gg`, while `jj + t > ṭṭh` has its own heading (line 53) | Heading `j / jj + t > gg`, or a note | 6 |
| class_18/6_as_sum.md:12 | `saṃ ka**th** **y**a ā \| sāka**cch**ā` | Split bold; the example is in the summary but not in the lesson (old H15) | construction confirmed by DPD (`saṃ > sā + √kath + yā`); join the bold and add the example to the lesson, or take it out of the summary | 6 |
| class_19/2_kamm.md:49, 51 | `\> sukatadukkaṭānaṃ` / `\> manāpāmanāpaṃ` | The result carries a case ending (gen. pl., acc.) while the inputs are stems; line 47 gives the stem (old B17) | Stem forms | 7 |
| class_19/4_tap.md:99 | `guh**āyaṃ** āsaya \> guhāsayaṃ` | The result ends in `-ṃ`; the input is `āsaya` (old B18) | `guhāsaya` | 7 |
| class_19/6_comp_rules.md:15, 19 | `masculine stems ending in **-ū, ā, ī**` / `cattālīsā + danta` | `cattālīsā` is a feminine numeral, not a masculine stem (old B19) | Reword the rule | 7 |
| class_19/6_comp_rules.md:37 | `dīgha + ratta + aṃ` | Rule 7 is about `ratti > ratta`; the example starts from `ratta` (old B20) | `dīgha + ratti \> dīgharattaṃ` | 7 |
| class_19/6_comp_rules.md:45 | `mātar + pitu \> māt**ā**pitaro` | `pitu` beside `pitar` (lines 43, 47); the `mātā-` form is not in the rule's list (line 39), which also names `petti-` without an example (old B21) | `mātar + pitar`; add `mātā-` to the rule and a `petti-` example | 8 |
| class_20/1_abya.md:42 | `\| **pura** \| before \| **aruṇā** \| from dawn \| **purāruṇā** \|` | The first member should be `purā` (the list on line 71 has `pure`) (old B23) | `**purā**` (DPD: `purā + aruṇa + ā`) | 9 |
| class_20/4_change_comp.md:11 | `\| go \| cow, cattle \| gavo \| jaraggavo \|` | The third column gives the compound form (stem) elsewhere; here the nominative `gavo` (old B24) | `gava \| jaraggava` (DPD: `jarā + gava`) | 7 |
| class_20/2_bahub.md:111, 129, 135, 141, 143 | `adjective **-a ending**` / `bahubhāṇī` / `cirappavāsī` / `ekavihārī` / `kālavādī` | Group 1 is defined by the `-a` ending; four of its examples end in `-ī` (old B25) | Reword the rule, or move the examples | 7 |
| class_19/2_kamm.md:117, 155 | `na \> **na / an / a / ana**` / `**na-** becomes **an-** before a vowel and **a-** before a consonant` | Four forms on line 117, two in rule 5; no example of `na-` kept or of `ana-` | Align the two statements; add examples | 6 |
| class_19/6_comp_rules.md:51 | `**dva- dvi- dve- di- du- duv-**` | Six forms are listed; the examples (lines 53–61) show five, none with `duv-` | Add a `duv-` example, or drop the form | 6 |
| class_20/3_mis.md:31 | `kāyagatāsati \< kāyagata + sati (kammadhāraya)` | The first member is feminine `kāyagatā` in the compound; the analysis gives the stem `kāyagata` without comment | `kāyagatā + sati` | 6 |
| class_21/6_opt.md:22 | `The forms shown in italics here and further in the conjugation tables only exist in grammar books.` | Later tables called theoretical (7_perf.md attanopada, 9_aor.md:35–37) are not italic (old B26) | Italicise them, or reword the footnote | 7 |
| class_21/8_imperf.md:7 | `events which happened before yesterday` | Line 5 translates the sutta as `starting from yesterday` (old B27) | `from yesterday backwards` | 8 |
| class_21/6_opt.md:20, 31 | `*damemase*` / `*nīyemase*` | The ending is not in the summary (10_sum.md:9, 46 give only `eyyāmhe`) (old B28) | verify; add to the summary or remove | 6 |
| class_22/2_cond.md:29 | `abhav**issiṃsu**` | The class 21 summary (10_sum.md:19, 51) gives `ssisu` (old B29) | verify against Kaccāyana 430; align | 8 |
| class_22/3_root_groups.md:56, 62 | `These roots **end in i ī u ū**` / `\| √pā \| a \| p**iva** \| pivati \| drinks \|` | `√pā` ends in `ā`, and `piva` is not an `ay` / `av` base (old B30) | Move it to the irregular bases (it is there, 4_irreg_base.md:23) | 8 |
| class_22/3_root_groups.md:41 | `the verbal terminations are added directly to the root` | The table still shows the sign `a` in column 2 (old B31) | Reword, or drop `a` | 7 |
| class_21/10_sum.md:27, 42 | `\| \| **3 paṭhama** \| **2 majjhima** \| **1 uttama** \| \| \| \|` | The person labels do not sit over their column pairs: `2 majjhima` is above the third-person plural, `1 uttama` above the second-person singular | `\| \| **3 paṭhama** \| \| **2 majjhima** \| \| **1 uttama** \| \|` | 9 |
| class_22/3_root_groups.md:65 | `\| √bhī \| a \| bh**āya** \| bhāyati \| fears \|` | The rule on line 56 gives `ay`; this base has `āy` with no comment | Add a note, or move to the irregular bases | 6 |
| class_22/3_root_groups.md:153 | `## 8. curādigaṇa (-e- -aya-)` | Two signs in the heading; all nine examples have `-e-`, none `-aya-` | Add an `-aya-` example (e.g. `corayati`) | 6 |
| class_23/9_ava.md:11; class_22/3_root_groups.md:131 | `\| √dhu \| to shake \| odhunāti \|` / `\| √dhū \| nā \| dhunā \| dhunāti \|` | The same root in two spellings (old B32) | `√dhū` in 9_ava.md:11 (DPD gives `√dhū` for both `odhunāti` and `dhunāti`) | 9 |
| class_23/4_adhi.md:14; class_23/15_pati.md:17 | `\| atta \| self \| ajjhattaṃ \| internally \|` / `\| √rūp \| to form \| patirūpaka \| resembling \|` | An adverb and an adjective in tables whose other rows are all `root \| meaning \| verb` | Move them below the tables as extra examples | 6 |
| class_23/21_nipata.md:61, 80 | `## pura- puro-` / `## tiro- tero-` | The heading names two forms; no example has `puro-` (lines 67–68), and `antarā-` (line 14) has none either | Add examples, or drop the form | 6 |
| class_23/21_nipata.md:101 | `## sat-` | `sat` is the participle stem of `santa` (class_19/2_kamm.md:143), not an adverb (*nipāta*); the page title is "Some Adverbs (nipāta) used as Prefixes" | Move to class 19/20, or widen the title | 6 |
| class_24/6_app.md:44 | `\| \| **Masculine** \| **Feminine** \| **Neuter** \| \| \| \|` | Seven columns (sg and pl × 3), but the three labels sit over columns 2–4, so `Feminine` is above masc. pl. and `Neuter` above fem. sg.; there is no sg/pl row (old B36) | `\| \| **Masculine** \| \| **Feminine** \| \| **Neuter** \| \|` plus a sg/pl row | 9 |
| class_24/6_app.md:50, 51, 52 | `dass**āvito**` / `dass**āvissa**` / `dass**āvini**` | The masculine and neuter columns should match in the oblique cases, but each lists a different set (`-āvito` only nt. abl., `-āvissa` only nt. gen., `-āvini` only masc. loc.); no voc. row (the class 18 tables have `8.voc`) (old B37) | Align the two columns | 8 |
| class_24/2_irreg_pass.md:25, 27 | `\| √ci \| to gather \| (ī)ya \|` / `\| √lu \| to reap \| (i)ya \|` | The same lengthening in two notations; `√su` appears again on lines 51–52 with plain `ya` (old B38) | One notation | 7 |
| class_24/4_irreg_caus.md:29 | `sivve \| visibbeti` | Base `sivve`, verb `sibbe-` (old B40) | `sibbe` (DPD: `vi + sibbe + ti`) | 8 |
| class_24/2_irreg_pass.md:93, 94 | `\| √**ph**ar \| to pervade \| pp \| **phu**ṭa \|` / `\| √**bha**r \| to support \| adj \| pa**bhu**ti \|` | Listed under `va \> vu`, but they are `pha > phu` and `bha > bhu` (old B41) | A separate heading, or a note | 6 |
| class_25/2_nouns.md:32 | `\| √sad \| to sink, sit, settle \| + \*a \| pasāda \|` | The prefix `pa` is not shown (line 21 has `pa + √vatt`) (old B42) | `pa + √sad` | 9 |
| class_25/4_taddh.md:23, 25, 31, 33 | `1.  sāmañña (general)` / `1.  apacc’attha` / `1.  saṅkhyā (numerical)` / `2.  bhāva (state of)` | The source numbers 1,1,1,1,1,2,3 show a lost nesting (sub-types under sāmañña); Markdown renders a flat 1–7 (old B43) | Nest the sub-items | 8 |
| class_25/5_taddh_2.md:1 | `# \*a (dyed with)` | The page that holds all the taddhita suffixes has the first suffix as its H1, so the indexes list the page as `\*a (dyed with)` (index.md:120, class_25/index.md:7) (old B44) | Give the page a title; make the suffix an H2 | 9 |
| class_25/1_deriv.md:7 | `These suffixes are called **Derivatives,**` | Derivatives are the resulting words, not the suffixes (line 9 uses the word that way; 4_taddh.md:19 again says "Secondary derivatives are suffixes") (old B45) | Reword | 6 |
| class_24/1_pass.md:53 | `\| √dhar+ \*e \| to carry \| iya \| dh**ā**riya \| dhāriyati[^20] \| is carried \|` | A causative passive in the plain `Root + iya` table, before causative passives are taught (5_caus_pass.md) | Move it, or add a note | 6 |
| class_26/4_ind.md:3, 7 | `## khattuṃ (times) adverbs of manner` / `+ kkhattuṃ` | The heading and the table spell the suffix differently (old B47) | One form | 8 |
| class_26/1_having.md:27, 31 | `### ila (having, possessing)` / `kumbh**īla**` | Suffix `ila`, result `īla` (old B48) | A note, or a separate suffix | 7 |
| class_26/1_having.md:45, 66, 80 | `### tana (belonging to) adjectives` / `### tara (comparative adjectives)` / `### tama (superlative adjectives)` | Not possession, but placed under `## Having & Possessing` (old B49) | Their own H2 | 6 |
| class_27/1_kitaka.md:15; class_27/2_kicca.md:161, 147, 149 | `\*tya` / `## tya (ptp)` / `## eyya (ptp)` / `\***ya** becomes **eyya**` | The star is present in one place and absent in the other (old B50) | One form | 7 |
| class_26/3_state.md:95, 100; class_25/5_taddh_2.md:41, 42 | `\| dvi \| + \*a \| dv**aya** \| two state, duality \|` / `\| ti \| + \*a \| t**aya** \| three state, triad \|` / `dv**aya** \| pair, couple` / `t**aya** \| group of three, triad` | `dvaya` and `taya` are listed under "state of" in class 26 and under "group of, collection" in class 25 | Keep them in one category | 6 |
| class_27/3_kita.md:39, 44 | `\| √dā \| dadā \| **+ māna** \| dada**māna** \|` / `\| √ñā \| jānā \| **+ māna** \| jāna**māna** \|` | The base ends in `ā`, the result has `a`; the shortening is not marked | Bold the changed vowel, or give the bases as `dada`, `jāna` | 6 |
| class_27/2_kicca.md:35 | `\| √gah \| ṇhā \| gahe \| + tabba \| gahe**tabba** \|` | The sign `ṇhā` does not itself give the base `gahe`. DPD has the same data (root sign `ṇhā`, construction `gahe + tabba`), and the key audit corrects `√gah + ṇhā + tvā` to `√gah \> gahe + tvā` (23_class.md:570) (old B51) | Mark `gahe` as an irregular base, as the key does at 23_class.md:802 (`gahe (irreg base)`) | 6 |
| class_28/1_kita_1.md:23, 24 | `\| 15 \| **+ \*ana** \| 151 \|` / `\| 16 \| **+ \*ī** \| 157 \|` | The ranking table is otherwise descending; 157 > 151. The sections (`\*ana` on line 570, `\*ī` on line 605) follow the same wrong order (old B53) | Swap rows 15 and 16 (and the sections), or correct a count | 9 |
| class_28/1_kita_1.md:258, 262 | `\| **pp** \| 1066 \|` / `\| **total** \| **1300** \|` | The parts (1066 + 110 + 105 + 20) add up to 1301, one more than the total (old B54) | Recount | 10 |
| class_28/1_kita_1.md:85, 159, 236, 303, 412, 649 | `\| **total** \| **1684** \|` / `\| **total** \| **1442** \|` / `\| **total** \| **1395** \|` / `\| **total** \| **1162** \|` / `\| **total** \| 265 \|` / `\| **total** \| 139 \|` | The parts add up to 1660, 1438, 1393, 1161, 264, 136. If minor categories were left out, no table says so; the other tables (`ta`, `na`, `ti`, `aka`, `ī`, `\*ana`, `\*ī`, `\*aka`) add up exactly (old B55) | Add an "other" row, or recount | 9 |
| class_28/1_kita_1.md:331, 553, 695 | `## māna` / `## anā` / `## \*aka` | Every other top-18 section has a description, a count table and examples. `māna` has no count table or examples; `anā` has no description or count table; `\*aka` has no description (old B56) | Complete to the common pattern | 8 |
| class_28/1_kita_1.md:566, 568 | `\| pa √atth \| to wish \| **+ anā** \| patth**anā** \| aspiration \|` / `\| pa √atth \| to wish for \| **+ anā** \| patth**anā** \| intention, wish \|` | The same word is listed twice in one table (old B57) | Merge | 9 |
| class_28/1_kita_1.md:672, 673 | `\| √kas \| to drag \| **+ i** \| kas**i** \| farming \|` / `\| √kas \| to plough \| **+ i** \| kas**i** \| farming \|` | Duplicate row; line 535 gives the root once as "to drag, plough" (old B58) | Merge | 9 |
| class_28/1_kita_1.md:181, 358, 397, 590 | `\| √sī \| to sleep \| **+ \*a** \| ās**aya** \|` / `\| √sad \| to sink \| **+ na** \| pasan**na** \|` / `\| √hu \| to offer \| **+ ti** \| āhu**ti** \|` / `\| √vis \| to enter \| **+ \*ana** \| niv**e**s**ana** \|` | The result has a prefix (`ā`, `pa`, `ā`, `ni`) that column 1 does not show; most rows of the file do show it (`ā √jīv`, `pa √hā`) (file 2: see p10) (old B59) | Add the prefix to column 1 | 8 |
| class_28/1_kita_1.md:229, 233 | `a tiny group of **passive present participles**, **nouns** and **adjectives**` / `\| **prp** \| 1378 \|` | "Passive present participles" has no row in the count table and no example (old B60) | Add or drop | 6 |
| class_28/1_kita_1.md:607, 613 | `is used to form a large group of **adjectives** and some **masculine agent nouns**` / `\| fem \| 5 \|` | The description leaves out the feminine nouns that the count table lists | Add `and a few feminine nouns` | 6 |
| class_28/2_kita_less.md:20, 35, 70, 127, 162, 227, 392, 496 | `\| √khā \| to tell \| **+ tar** \| akkhā**tar** \|` / `\| √bhañj \| to break \| **+ u** \| pabhaṅg**u** \|` / `\| √jan \| to be born \| **+ ya** \| ājañ**ña** \|` / `\| √kam \| to go \| **+ itar** \| upasaṅkam**itar** \|` / `\| √ud \| to be wet \| **+ ra** \| samud**da** \|` / `\| √car \| to act \| **+ iya** \| ācar**iya** \|` / `\| √mā \| to measure \| **+ tta** \| nimitta \|` / `\| √i \| to come \| **+ tāvī** \| abhisame**tāvī** \|` | Throughout file 2 the result has a prefix (or `na`) that column 1 does not show: also lines 37, 55, 56, 73, 83, 85, 130, 143, 179, 180, 186, 200, 201, 234, 236, 249–251, 273, 274, 325, 339, 351, 352, 407, 439, 492, 495, 516, 528, 529. File 1 mostly shows the prefix (old B59) | Add the prefix to column 1 | 8 |
| class_28/2_kita_less.md:367, 371 | `**+ ala neuter nouns and adjectives**` / `kul**ala** \| eagle; hawk` | `kulala` is masculine, and there is no neuter noun in the table; line 433 has `√kur … kurara \| eagle` as masculine (old B61) | `**+ ala masculine nouns and adjectives**` (DPD: `kulala` masc, `bahala` adj) | 8 |
| class_28/2_kita_less.md:263, 264, 265 | `\| √ar \| to move, attain \| **+ tha** \| at**tha** \| meaning \|` / `\| √ar \| to move, attain \| **+ tha** \| at**tha** \| benefit \|` / `\| √ar \| to move, attain \| **+ tha** \| at**tha** \| goal, purpose \|` | The same word in three rows, one per meaning (also `tapas` on lines 305–306); elsewhere several meanings share one row | One row | 7 |
| class_28/2_kita_less.md:297; class_18/10_irreg_masc.md:7 | `**+ as mano group masculine nouns**` / `**Declension of manas (mano) (masc & nt[^6])**` | The mano group is "masculine" here and "masc & nt" in class 18 | One statement | 6 |
| class_28/2_kita_less.md:488 | `suffix **tāvī** is used to form **active past participles**` | The only table in the two files without a bold caption line (`**+ tāvī …**`); only three sections of file 2 have a description sentence (164, 283, 482) | Add the caption | 6 |
| class_23/9_ava.md:11; class_27/3_kita.md:101 | `\| √dhu \| to shake \| odhunāti \|` / `\| √tir \| **+ na** \| nitthi**ṇṇa** \|` | Course-wide list of root spellings that differ from DPD; each has its own row in the class slices: `√dhu` (DPD `√dhū`), `√veth` (`√veṭh`), `√bruh` (`√brūh`), `√saṃk` (`√saṅk`), `√sikh` (`√sikkh`), `√bhu` (`√bhū`), `√thamb` (`√thambh`), `√tir` (`√tar`), `√path` (`√puth`), `√pal` (`√palā`), `√ghaṇḍ` (`√ganth`), and `√sajj` in `visaṃsaṭṭha` (`√saj`). DPD has two separate roots for `√khan` / `√khaṇ`, `√saj` / `√sajj`, `√dah` / `√ḍah`, `√kas` / `√kass`, `√cit` / `√citt` and `√vaddh` / `√vaḍḍh`, and it confirms `√his`, `√ghaṭ` (for `ghāteti`), `√nadh`, `√badh`, `√ādā` and the split of `nī` (verbs) and `nir` (negative compounds): those stand | Correct the twelve in one pass | 8 |

## C. Translation and gloss problems

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_16/3_vowel_1.md:60 | `these \| five \| these five` | Glosses swapped: `pañca` = five, `ime` = these (old C1) | `five \| these \| these five` | 10 |
| class_16/3_vowel_1.md:152 | `indeed \| thus \| thus indeed` | `etaṃ` = this, not thus (line 228 has `this`) (old C2) | `indeed \| this \| this indeed` | 9 |
| class_16/3_vowel_1.md:208 | `my \| these are \| these are my` | `atthi` is singular "there is" (old C3) | `my \| there is \| there is my` | 8 |
| class_16/3_vowel_1.md:110; class_16/9_vowel_7.md:64 | `ignorance \| defilement` / `honey \| extract \| honey liquor` | `āsava` is "effluent" on lines 47 and 51 of 3_vowel_1.md, "defilement" here, "extract" in 9_vowel_7.md (old C4) | One gloss for the mental `āsava`; `liquor` in `madhvāsava` | 8 |
| class_16/3_vowel_1.md:165 | `conscience \| shame in wrongdoing \| conscience and concern` | `ottappa` is glossed two ways in one row (old C5) | `concern` in the middle cell, to agree with the compound gloss (both wordings are DPD glosses: `ottappa` "regret; shame in wrongdoing; respect for others", `hirottappa` "conscience and concern") | 6 |
| class_16/3_vowel_1.md:154, 224, 226, 230 | `now \| just \| only now` / `all \| only \| all of them` / `before \| only \| only before` / `if \| only \| only if` | `eva` is "only" here and "just" in the rest of the file; `pubbeva` "only before" is odd (old C6) | `just`; `pubbeva` = "previously" | 6 |
| class_16/4_vowel_2.md:44; class_16/5_vowel_3.md:41 | `she \| just \| just that` / `she \| for him \| that for him` | The gloss of `sā` changes inside the row (old C7) | `that \| just \| just that`; `that \| for him \| that for him` | 7 |
| class_16/5_vowel_3.md:86 | `whoever \| here \| whoever here` | `yāni` is nt. pl. "whatever (things)", not "whoever" (old C9) | `whatever \| here \| whatever here` | 9 |
| class_16/5_vowel_3.md:52 | `unmindful \| not aware \| not mindful or aware` | `asati` and `asampajañña` are nouns (old C10) | `lack of mindfulness \| lack of clear comprehension \| lack of mindfulness and clear comprehension` (DPD: `asati` fem, `asampajañña` nt, both abstract nouns) | 8 |
| class_16/8_vowel_6.md:51 | `lit. who for whom` | `assa` = for him (old C11) | `lit. who for him` | 8 |
| class_16/9_vowel_7.md:26 | `then \| I \| so I` | `so` = that/he (5_vowel_3.md:70 has `that \| I \| that I`) (old C12) | `that \| I \| that I` | 7 |
| class_16/3_vowel_1.md:88 | `separating \| just \| just secluding oneself` | `vivicca` is "separating" in the first cell and "secluding oneself" in the result | One gloss | 6 |
| class_16/3_vowel_1.md:112 | `compassion \| accomplished \| full of compassion` | `āpanna` means "entered upon, fallen into", not "accomplished" | `possessed of` (DPD `āpanna` 2: possessed of; filled with; having; `dayāpanna`: compassionate; full of kindness) | 8 |
| class_16/3_vowel_1.md:125 | `great \| supernatural power \| great supernatural power` | `mahiddhika` is an adjective ("of great power"); the gloss is a noun, and `iddhika` (not a DPD headword; DPD analyses `mahā + iddhi + ka`) is not `iddhi` | `great \| having supernatural power \| of great supernatural power` (DPD: `mahiddhika` adj, "of great supernormal power") | 8 |
| class_16/3_vowel_1.md:179; class_16/4_vowel_2.md:60, 78; class_16/9_vowel_7.md:48 | `? \| today \| today? now?` / `are? \| you are \| are you?` / `what? \| here \| what here?` / `(?) \| today \| today?` | The particle `nu` is glossed four ways (`?`, `are?`, `what?`, `(?)`); "are?" and "what?" are not meanings of `nu` | One form, e.g. `(?)` | 7 |
| class_16/7_vowel_5.md:34 | `towards, over \| looks \| looks over` | `upekkhati` is "looks on (with equanimity)"; "looks over" suggests inspecting | `looks on` (DPD: looks on; is disinterested; is indifferent) | 8 |
| class_17/9_nig_2.md:51 | `nt. standing still` | `saṇṭhāna` = shape, configuration (old C15) | `nt. shape; form` (DPD senses: relenting; resting place; shape; form; appearance; no "standing still") | 7 |
| class_17/13_nig_6.md:26 | `whichever this` | `yadidaṃ` = namely, that is (old C16) | `namely; that is` (DPD) | 8 |
| class_17/15_nig_8.md:17 | `buddha’s teaching` | `buddhānaṃ` is gen. pl.; lower-case b (old C17) | `teaching of the Buddhas` | 8 |
| class_17/3_cons_1.md:75 | `pr. contemplates, thinks` | `pajjhāyati` is "broods, is dejected" | `pr. broods; is anxious` (DPD: broods; is anxious; is concerned; is overcome; derogatory) | 8 |
| class_17/3_cons_1.md:160 | `nt. mountain cave` | `giribbaja` is "mountain enclosure"; `vaja` is a pen, not a cave | `nt. mountain enclosure` (DPD: mountain enclosure; mountain amphitheater; valley; also the name of a former capital of Magadha) | 8 |
| class_17/12_nig_5.md:13; class_17/13_nig_6.md:28 | `ya**ññ**adeva \| whatever it is` / `ya**ññ**a**d**eva \| whatever at all` | The same form is glossed two ways, analysed two ways (`yaṃ + yad eva`, `yaṃ yaṃ + eva`) and bolded two ways | One analysis and gloss, or a cross-reference | 7 |
| class_17/16_nig_9.md:27 | `ka**ṃ** \| **a**si \| ka**ṃ**si \| who are you?` | `kaṃ` is accusative: DPD glosses `kaṃsi` (`kaṃ + asi`) as "(under) whom are you (ordained)?"; "who are you?" is `ko + asi > kosi` (old H11) | `(under) whom are you (ordained)?` (DPD), or replace the example with `ko \| asi \| kosi \| who are you?` | 8 |
| class_18/2_as_ya.md:58 | `pr. is free` | Passive: line 27 has `(is freed)` (old C18) | `pr. is freed` | 8 |
| class_18/10_irreg_masc.md:62 | `fire state` | `dhātu` = element (old C19) | `fire element` | 8 |
| class_18/1_phonetic.md:23; class_18/3_as_ta.md:78 | `(pp. known)` / `pp. woken up` | `buddha` is glossed two ways (old C20) | One gloss, or both in both places | 6 |
| class_18/2_as_ya.md:113 | `pr. is broken` | `ruppati` = is afflicted, is deformed (old C22) | `pr. is hurt; is afflicted` (DPD: is hurt; is oppressed; is afflicted; is deformed) | 7 |
| class_18/10_irreg_masc.md:29 | `metrics` | `chandas` = metre, prosody (old C24) | `metre` | 6 |
| class_18/3_as_ta.md:146 | `ptp. could be done` | `kattabba` is "should be done, to be done" | `ptp. should be done` | 7 |
| class_19/1_comp.md:43 | `(restrained **and** controlled **by** the precepts)` | `pātimokkha-saṃvara-saṃvuta` is "restrained by the restraint of the Pātimokkha"; there is no "and" (old C25) | `restrained **by** the restraint **of** the Pātimokkha` | 7 |
| class_19/4_tap.md:47 | `(worthy **for** the King)` | Idiom (old C26) | `worthy **of** a king` | 7 |
| class_19/4_tap.md:63 | `(wanting **to** distract)` | `cāveti` = makes fall away (old C27) | `wanting **to** make fall` (DPD `cāvetukāma`: wanting to make fall; wanting to make leave) | 7 |
| class_19/5_dvanda.md:55 | `shame and fear` | A third gloss of `hirottappa` in the course (class_16/3_vowel_1.md:165 has two others) (old C28) | `conscience and concern` (DPD; as class_16/3_vowel_1.md:165) | 7 |
| class_19/5_dvanda.md:54 | `pain and stress` | `domanassa` = mental distress (old C30) | `pain and distress` (DPD `domanassa`: (mental) suffering; distress) | 6 |
| class_19/4_tap.md:89 | `(destruction **of** the defilements)` | The gloss of `āsava` drifts (effluent / defilement) across classes 16, 19, 20 (class_20/2_bahub.md:245 has `effluents`) (old C31) | One gloss | 7 |
| class_20/1_abya.md:29 | `**tato** \| from` | `tato` = from that (line 73 has `from that`) (old C32) | `from that` | 8 |
| class_19/2_kamm.md:55, 57 | `## sambhāvanā-pubba-pada` / `(origin before word)` | `sambhāvanā` is "supposition, designation" (the member marked by `iti`), not "origin" | DPD lookup (DPD has only "honouring; esteeming; respecting" for `sambhāvanā`; the grammatical sense here is "supposition, designation", not "origin") | 5 |
| class_19/2_kamm.md:113, 159 | `na + kusala \> **a**kusala (unskilful)` / `e.g. na + kusala \> akusala (not skilful)` | The same example twice in one file with two glosses | One gloss | 7 |
| class_19/5_dvanda.md:67, 68; class_16/3_vowel_1.md:53 | `sayanāsanaṃ \| bed and seat` / `senāsanaṃ \| bedding and seating` / `bed \| seat \| lodging` | `senāsana` is glossed two ways across classes; beside `sayanāsana` the difference in the English is arbitrary | One gloss for `senāsana` | 6 |
| class_19/1_comp.md:7; class_19/5_dvanda.md:27; class_19/6_comp_rules.md:5 | `their vocative / dictionary / stem form / lemma` / `dictionary form (vocative singular)` / `**stem form** / dictionary form / vocative singular` | The stem is equated with the vocative singular three times; that holds only for `-a` stems (not `-ā`, `-ī`, `-ar`), and rule 4 of 6_comp_rules.md itself shows stems that differ | `stem form (dictionary form)` | 6 |
| class_22/3_root_groups.md:93 | `vindati \| feels, likes` | `vindati` = finds, gains (old C34) | `finds; gets` (DPD `vindati` 1.1) or `enjoys; experiences` (2.1); DPD has two roots `√vid` in group ṃa, so say which | 6 |
| class_22/4_irreg_base.md:48 | `paṭihaṅkhati \| will kill` | DPD: will destroy; will put an end (to); will terminate; "kill" is too narrow (old C35) | `will destroy; will put an end to` (DPD: fut of `paṭihanati`) | 6 |
| class_23/14_pa.md:14; class_17/3_cons_1.md:75 | `pajjhāyati \| is overcome; is anxious` / `pr. contemplates, thinks` | `pajjhāyati` is glossed two ways (old C38) | `pr. broods; is anxious` in class_17/3_cons_1.md:75 (the class 23 gloss agrees with DPD: broods; is anxious; is concerned; is overcome) | 8 |
| class_23/21_nipata.md:51 | `pātukaroti \| appears, manifests` | Transitive: "appears" is the intransitive sense (old C39) | `displays, manifests` (DPD: displays; manifests; shows; makes appear) | 7 |
| class_23/4_adhi.md:10; class_23/5_anu.md:14; class_23/2_aa.md:14; class_23/15_pati.md:13; class_23/9_ava.md:10; class_23/20_mixed_pref.md:10 | `√sī \| to lie down` / `√sī \| to sleep` / `√mant \| to invite` / `√mant \| to counsel` / `√ikkh \| to see` / `√ikkh \| to look` | The same root has different meanings from file to file (also `√vatt` to go on / to proceed, `√gah` to grasp / to take, `√pucch` to ask / to question, `√var` to cover / to obstruct, `√sad` to sink / to sit, `√lok` to look / to see, `√vid` to feel, like / to sense) (old F90) | one root meaning each in all files; the headword lookup does not print root meanings: DPD lookup (roots table) for the wording | 6 |
| class_23/8_abhi.md:10; class_23/17_pari.md:11 | `abhijānāti \| totally understands` / `parijānāti \| totally understands` | Two verbs with the same gloss | `abhijānāti \| directly knows` (DPD); the `parijānāti` gloss agrees with DPD (completely comprehends) | 7 |
| class_23/22_dur_su_nir.md:11; class_19/5_dvanda.md:54 | `domanassa \| mental suffering` / `dukkhadomanassaṃ \| pain and stress` | `domanassa` is glossed two ways across classes | One gloss | 6 |
| class_23/1_prefix.md:43 | `**o**harati (shaves, lit. takes down)` | "shaves" is not a DPD sense of `oharati` | `takes off (lit. takes down)` (DPD `oharati`: takes off or down; no "shaves") | 7 |
| class_24/1_pass.md:77 | `will be free` | Passive (old C41) | `will be freed` | 8 |
| class_24/2_irreg_pass.md:37 | `samanuyuñjiyati\* \| being cross-questioned` | A finite verb glossed as a participle (old C42) | `is cross-questioned` | 9 |
| class_24/5_caus_pass.md:72 | `nisīdāpīyati \| causes to be seated` | A causative passive: is caused to sit (old C43) | `is caused to sit down` | 9 |
| class_24/2_irreg_pass.md:7 | `sandassiyamāna \| being seen together` | = being shown, being instructed (a causative passive) (old C44) | `being taught; being instructed` (DPD) | 8 |
| class_24/1_pass.md:47 | `\| √vad \| to speak \| ya \| vajja \| vajjati \| is played \|` | The gloss needs its context (of a musical instrument) (old C45) | `is played (of a musical instrument)` (DPD) | 7 |
| class_25/2_nouns.md:45 | `māra \| death` | In the agent-noun table ("a person who does the action") (old C46) | `killer; Māra` | 7 |
| class_25/5_taddh_2.md:19 | `from God Vishnu` | The gloss column gives "from" + the base word; the base is `vasudeva`, and Vishnu is the derivative `vāsudeva` (old C47) | `from Vasudeva; God Vishnu` (DPD: `vāsudeva` "God Vishnu", from `vasudeva`) | 6 |
| class_24/5_caus_pass.md:65; class_20/2_bahub.md:245 | `the destruction of the defilements` / `whose effluents are destroyed` | `āsava` again glossed two ways (see the p01 and p04 rows) | One gloss | 7 |
| class_24/1_pass.md:46; class_18/2_as_ya.md:113 | `\| √rup \| to break \| ya \| ruppa \| ruppati \| is broken \|` / `pr. is broken` | `ruppati` is "is afflicted, is deformed"; see the p03 row | `is hurt; is afflicted` in both places (DPD: is hurt; is oppressed; is afflicted; is deformed) | 7 |
| class_24/1_pass.md:68 | `\| √tur \| to hurt \| īya \| turīya \| āturīyati \| is hurt \|` | The form is in DPD, with the meaning "becomes sick", not "is hurt" (old H38) | `becomes sick` (DPD: `āturīyati`, pass of `āturati`, "becomes sick; becomes hoarse") | 6 |
| class_26/1_having.md:50, 51 | `purā**tana** \| belonging to ancient` / `sanan**tana** \| belonging to ancient` | Ungrammatical gloss, twice (old C48) | `ancient, of old` | 7 |
| class_26/3_state.md:62 | `brahman state, celibacy` | `brahmañña` is brahmin-hood; celibacy is `brahmacariya` (old C49) | `brahmin state, holy life` (DPD: Brahmanhood; spiritual life; holy life) | 6 |
| class_26/3_state.md:99 | `t**ā**pas**a** \| austere state, ascetic` | `tāpasa` is a person, listed under "state of" (old C50) | regloss as `ascetic` and move it out of the "state" table (DPD: masc, "ascetic; hermit", from `tapas`) | 7 |
| class_26/4_ind.md:51 | `amu**tra** \| in such place,` | = in that place, there; trailing comma (old C51) | `in that place, there` | 8 |
| class_27/2_kicca.md:18 | `ga**ntabba** \| to be followed` | = to be gone (to) (old C52) | `to be gone` | 7 |
| class_27/2_kicca.md:72 | `pāṭides**anīya** \| to cause to be pointed out` | = to be confessed; the prefix `paṭi` is not shown (old C53) | `to be acknowledged` (DPD: should be acknowledged; to be admitted; `pati > pāṭi + dese + *anīya`) | 8 |
| class_27/2_kicca.md:167 | `ma**cca** \| to be dead` | = mortal; lit. bound to die (old C54) | `mortal` | 7 |
| class_26/3_state.md:64; class_23/22_dur_su_nir.md:11 | `d**o**mana**ssa** \| bad mind state, distress` / `domanassa \| mental suffering` | A further gloss of `domanassa` (see the p04 and p06 rows) | One gloss | 6 |
| class_26/4_ind.md:111 | `atta**to** \| as oneself` | In the texts `attato` is "as self" (doctrinal), not "as oneself" | `as self` | 6 |
| class_27/2_kicca.md:73; class_27/3_kita.md:9, 94 | `moh**anīya** \| to be deluded` / `añcha**nta** \| turning; cutting` / `h**īna** \| defeated, lost` | `mohanīya` is active in DPD ("able to cause delusion; deceptive"), not "to be deluded" | `moh**anīya** \| able to cause delusion` (DPD); the other two glosses agree with DPD | 7 |
| class_26/3_state.md:98 | `s**o**rat**a** \| mild state, politeness` | `sorata` is an adjective; the state is `soracca` (old H51) | regloss as `gentle, polite`, or replace the row with `sorata \| + \*ya \| soracca` (DPD: `sorata` adj; the state is `soracca`) | 7 |
| class_28/1_kita_1.md:587, 598 | `\| √i \| to come \| **+ \*ana** \| **ayana** \| way \|` / `\| parā √i \| to go \| + **\*ana** \| par**āyana** \|` | The same root is glossed two ways (file 2: see p10) (old C55) | `to go` throughout | 7 |
| class_28/1_kita_1.md:358 | `\| √sad \| to sink \| **+ na** \| pasan**na** \| believer \|` | "To sink" does not lead to "believer"; `pa + √sad` is "to be clear, pleased" (old C57) | `pa √sad` in column 1 (DPD: `pa + √sad + na`); the gloss `believer` is DPD sense 4 | 7 |
| class_28/1_kita_1.md:445, 428 | `āvar**aṇa** \| obstructed, blocked` / `āvar**aṇa** \| obstacle, blockage` | The adjective is active: "obstructing" (old C58) | `obstructing, blocking` (DPD `āvaraṇa` 1 adj) | 8 |
| class_28/1_kita_1.md:657, 659, 660 | `\| ni √dhā \| to place \|` / `\| pa ni √dhā \| to support \|` / `\| upa √dhā \| to support \|` | The same root has two glosses in adjacent rows (also line 270 `to support`, 658 `to place`) (old C59) | One gloss | 7 |
| class_28/1_kita_1.md:50, 392 | `\| √budh \| to wake up \| **+ ta** \| bud**dha** \|` / `\| √budh \| to know \| **+ ti** \| bud**dhi** \|` | Root gloss drift inside the file (also `√dis` to see / to point out, lines 394, 460; `√kuṭ` to be crooked / to be bent, 215, 675; `√pu` to purify / to cleanse, 712, 725; `√gaṇ` to add here, to calculate in class_25/2_nouns.md:46) | one gloss per root; root meanings are not in the headword lookup: DPD lookup (roots table) for the wording | 6 |
| class_28/1_kita_1.md:191; class_25/2_nouns.md:45 | `m**ā**r**a** \| Death` / `māra \| death` | The agent noun is glossed `Death` here and `death` in class 25 (see the p07 row) | `Māra; lit. killer` in both | 6 |
| class_28/1_kita_1.md:422; class_16/8_vowel_6.md:35 | `vyākar**aṇa** \| answer` / `grammar *(byākaraṇa)*` | Two glosses of `vyākaraṇa` across classes (both are meanings of the word) | Give both, or cross-reference | 5 |
| class_28/2_kita_less.md:496 | `\| √i \| to come \| **+ tāvī** \| abhisame**tāvī** \| has realised \|` | `√i` is "to go" in file 1 line 598 and in class 23 (file 1: see p09) (old C55) | `to go` | 7 |
| class_28/2_kita_less.md:406 | `m**e**tt**ā** \| lit. friendliness` | Only a "lit." gloss, with no primary meaning (compare `fire; lit. purifier`) (old C60) | `loving-kindness; lit. friendliness` | 7 |
| class_28/2_kita_less.md:18, 200 | `\| √ghaṭ \| to strike, kill \|` / `\| √ghaṭ \| to harm \| **+ \*i** \| nigh**ā**t**i** \| defeat, loss \|` | The same root is glossed two ways in one file (class_22/3_root_groups.md:157 has `kills, slays` for the verb) | one gloss for `√ghaṭ` in the file (DPD confirms the same root, `√ghaṭ` 1, for `ghātetar` and `nighāti`; root meanings are not in the headword lookup) | 6 |
| class_28/2_kita_less.md:91; class_27/2_kicca.md:125 | `dam**ma** \| young bull` / `da**mma** \| to be tamed, tamable` | Two meanings of `damma` with no cross-reference; the bold split also differs | Add `lit. to be tamed` | 5 |
| class_16/3_vowel_1.md:47; class_19/4_tap.md:89; class_16/9_vowel_7.md:64 | `sensual pleasure \| effluent \| effluent of sensual pleasure` / `(destruction **of** the defilements)` / `honey \| extract \| honey liquor` | Course-wide list of words with more than one gloss; each has its own row in the class slices: `āsava` (effluent, defilement, extract), `hirottappa` (three glosses), `domanassa` (four), `senāsana`, `buddha`, `pajjhāyati`, `ruppati`, `eva`, `nu`, `māra`, `vyākaraṇa`, `damma`, and the root meanings of class 23 and class 28 | One fixed gloss per sense, not per word (`āsava` "effluent" vs "extract" in `madhvāsava`; the two senses of `vyākaraṇa`); a short course glossary would hold them | 7 |
| class_21/9_aor.md:45; class_24/5_caus_pass.md:29; class_20/2_bahub.md:257 | `**addressed** the Blessed One in verse` / `in the community of monks by the Buddha”` / `Form is abandoned by the Realised One` | `bhagavā` is "the Blessed One" in class 21 and "the Buddha" in class 24; `tathāgata` is "Realised One" (twice) | One rendering each, the same as in the key: the key audit asks for `the Blessed One` (ipc_key 24_class.md:209) and one rendering of `tathāgata` (19_class.md:324) | 7 |

## D. English typos and grammar

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_16/2_vowel.md:11 | `Vowel Sandhi are :` | Space before the colon (old D1) | `are:` | 9 |
| class_16/3_vowel_1.md:7 | `and very common in Pāli` | Missing verb (old D2) | `and is very common` | 9 |
| class_16/4_vowel_2.md:35 | `thus/”` | Stray slash and quote mark (old D3) | `thus (end quote)` | 8 |
| class_16/7_vowel_5.md:70 | `not textual example` | Missing article (old D4) | `not a textual example` | 8 |
| class_16/10_vowel_8.md:45 | `ca **m**avajānāti,` | Stray trailing comma; also a space inside the sandhi result (old D5) | `ca**m**avajānāti` | 8 |
| class_16/12_vowel_ref_table.md:79 | `**1s letter**` | Typo (old D6) | `**1st letter**` | 9 |
| class_16/12_vowel_ref_table.md:93, 95 | `meets **a** result can be` / `meets **i** result can be` | Missing "the" (the first half of each sentence has it) (old D7) | `the result can be` | 9 |
| class_16/12_vowel_ref_table.md:99 | `apostrophe( ’ )` | Missing space (old D8) | `apostrophe ( ’ )` | 9 |
| class_16/12_vowel_ref_table.md:109 | `in **PTS** dictionary` | Missing article (old D9) | `in the **PTS** dictionary` | 8 |
| class_16/13_home_work.md:11 | `to help you also use Buddha’s Words or SuttaCentral` | Run-on, missing full stop (old D10) | `to help you. Also use …` | 9 |
| class_16/2_vowel.md:3 | `at the end of one part of speech meets the vowel at the beginning of another part of speech` | "Part of speech" means a word class (noun, verb); here a word or word element is meant | `one word or word part … another` | 6 |
| class_17/1_alphabet_analys.md:5 | `learn the alphabetical-order, it will` | Hyphen; comma splice (old D11) | `alphabetical order; it will` | 8 |
| class_17/1_alphabet_analys.md:3 | `So each week there will be given a little more information.` | Awkward (old D12) | `A little more information will be given each week.` | 7 |
| class_17/2_cons.md:3 | `consonant**. (or parts of a word)` | Bracket after the full stop (old D13) | Move it inside the sentence | 8 |
| class_17/7_cons_5.md:22 | `as you can see this mostly occurs` | No capital, comma or full stop (old D14) | `As you can see, this mostly occurs … **pati**.` | 8 |
| class_17/12_nig_5.md:18 | `**Counter-example:**` | Singular; four examples follow (old D15) | `**Counter-examples:**` | 9 |
| class_17/13_nig_6.md:30 | `this is influenced by the Sanskrit **yad tad etad** and **tam** **etam** etc` | No capital, no full stop; split bold (old D16) | `This is influenced by the Sanskrit **yad tad etad** and **tam etam** etc.` | 8 |
| class_17/15_nig_8.md:7 | `in verses` | A fragment on its own line (old D17) | `**ṃ** may be **elided** in verses.` | 8 |
| class_17/16_nig_9.md:31 | `with the meaning of a **like** or **as**` | Stray `a` (old D18) | `meaning of **like** or **as**` | 9 |
| class_17/1_alphabet_analys.md:7 | `Just to refresh your memory, there are 41 letters` | No colon or full stop (also 2_cons.md:5, 9_nig_2.md:11) | Add `:` | 7 |
| class_18/1_phonetic.md:7, 39, 83 | `2.  Adaption` / `**Adaption** occurs` / `Adaption` | The usual term is `Adaptation` (old D19) | `Adaptation` | 6 |
| class_18/1_phonetic.md:39 | `changes from the influence of another consonant` | Preposition; the sentence has no full stop (also lines 17, 45) (old D20) | `under the influence` | 7 |
| class_18/1_phonetic.md:63 | `**Aspiration** an -h- is added` | No verb or punctuation between term and definition (old D21) | `**Aspiration**: an -h- is added.` | 8 |
| class_18/1_phonetic.md:93 | `that can occur, let’s look` | Comma splice (old D22) | Full stop | 7 |
| class_18/7_mix_san.md:20 | `**Pāli1**` | Stray `1` (a lost footnote marker?) (old D23) | `**Pāli**` | 9 |
| class_18/8_as_misc.md:1 | `# Another consonant assimilation` | Ungrammatical title (also index.md:45, class_18/index.md:10) (old D24) | `Other Consonant Assimilations` | 8 |
| class_18/8_as_misc.md:3, 5 | `ud- ; dur- ; nir-` | Space before the semicolons (old D25) | `ud-, dur-, nir-` | 8 |
| class_18/8_as_misc.md:19 | `prefix(s)` | Plural (old D26) | `prefix(es)` | 8 |
| class_18/3_as_ta.md:7; class_18/4_as_na.md:3 | `**neuter nouns ending** in -ta` / `**neuter nouns ending** in -na, etc` | `ending` is inside the bold (not in the parallel phrases); `etc` without a full stop (old D27) | `**neuter nouns** ending in -ta, … etc.` | 8 |
| class_18/2_as_ya.md:7 | `Often a part of speech ending in **-i** can change to **-y**` | "Part of speech" for a word element (as in class_16/2_vowel.md:3) | `a word or prefix ending in **-i**` | 6 |
| class_18/8_as_misc.md:19 | `have a double consonant become one consonant` | A conjunct (`kr`, `sth`), not a doubled consonant, is meant | `a consonant cluster` | 6 |
| class_19/1_comp.md:39 | `combination of one or more of the above` | A complex compound needs two or more (old D28) | `two or more` | 8 |
| class_19/2_kamm.md:45 | `adjective + adjectives` | Plural (old D29) | `adjective + adjective` | 9 |
| class_19/2_kamm.md:53, 69, 91 | `they can be classified as *dvanda* type of compounds` / `can be classified as a *tappurisa* type of compounds` | Number disagreement; line 53 has no capital or full stop (old D30) | `as *tappurisa* compounds.` | 8 |
| class_19/2_kamm.md:63 | `**iti** ; **evaṃ**; **saṅkhāto** ; **hutvā**` | Irregular spaces before the semicolons (old D31) | `**iti**; **evaṃ**; **saṅkhāto**; **hutvā**` | 8 |
| class_19/3_digu.md:17 | `or as group` | Missing article (old D32) | `or as a group` | 9 |
| class_19/4_tap.md:51 | `(water **for** face)` | Missing article (old D33) | `for the face` | 7 |
| class_19/4_tap.md:103 | `(enjoying **in** the teaching)` | Idiom (old D34) | `delighting **in**` | 7 |
| class_19/6_comp_rules.md:3 | `noun, adjective, participles, pronoun` | A plural in a singular list (old D35) | `participle` | 9 |
| class_19/6_comp_rules.md:17 | `(blamed by wise)` | Missing article (4_tap.md:35 has `by** the wise`) (old D36) | `by the wise` | 8 |
| class_20/1_abya.md:17 | `an **adverb ending in an accusative case.**` | Wording; full stop inside the bold (old D37) | `an **adverb with an accusative ending**.` | 7 |
| class_20/1_abya.md:19 | `for whole life` | Missing article (old D38) | `for the whole of life` | 8 |
| class_20/1_abya.md:47 | `some grammatical books take them` | `grammatical books`; no capital or full stop (also 2_bahub.md:275 `Some grammatical sources`) (old D39) | `Some grammar books take them ….` | 7 |
| class_20/2_bahub.md:167 | `the negative of **sa-** are adjectives` | Subject–verb agreement (old D40) | `the opposite of **sa-** is **a-** (without)` | 7 |
| class_19/5_dvanda.md:21 | `occur in the **plural**, are taken **individually**, generally when they refer` | Run-on | `occur in the plural and are taken individually, generally when …` | 7 |
| class_21/2_voices.md:5, 7 | `Active voice: The man cut the tree` / `Passive: The tree is cut by the man.` | Tense mismatch with `chindati` and with the passive line; no full stop; `Passive` beside `Active voice` (old D41) | `Active voice: The man cuts the tree.` | 8 |
| class_21/3_pass_refl.md:17, 23 | `but practically the meaning is the same.` / `as usual with a few exceptions` | Lower-case sentence starts; no full stop on line 23 (old D42) | Capitals and full stops | 8 |
| class_21/3_pass_refl.md:33 | `either **parassapada** or **attanopada** verbal ending can be used` | Number (old D43) | `endings can be used` | 7 |
| class_21/3_pass_refl.md:43 | `What is the meaning of Pāli words **parassapada** and **attanopada.**` | A question without `?`; missing `the` (old D44) | `… of the Pāli words **parassapada** and **attanopada**?` | 9 |
| class_21/7_perf.md:13 | `But, modern grammars have given it the name of - **Perfect Past Tense,**` | Stray comma and dash (old D45) | `But modern grammars call it the **Perfect Past Tense**,` | 7 |
| class_21/7_perf.md:45 | `(to speak) - *different form of root √brū*. Has the following forms:` | Fragment (old D46) | `…, a different form of √brū, which has the following forms:` | 8 |
| class_21/9_aor.md:7 | `Ajja “means” today in Pāli.` | Quote marks on the wrong word (old D47) | `Ajja means “today” in Pāli.` | 9 |
| class_22/2_cond.md:7 | `The Conditional[^12], expressing future time relatively to something that is past` | The quotation is a fragment and has no quote marks (old D48) | Add quote marks, or complete the sentence | 7 |
| class_22/3_root_groups.md:129 | `knows, think` | Number (old D49) | `knows, thinks` | 9 |
| class_22/3_root_groups.md:37 | `from most common to less common` | Comparative (old D50) | `to least common` | 6 |
| class_21/7_perf.md:9 | `which means “face to face with, in the presence of”` | No full stop at the end of the paragraph | Add it | 8 |
| class_23/2_aa.md:18 | `while forms that have not been seen in the text` | The list is of meanings, not forms (old D51) | `meanings` | 7 |
| class_23/7_api.md:7 | `put over, closes, shuts` | Number (old D52) | `puts over` | 9 |
| class_23/8_abhi.md:3 | `particularity` | Should be an adverb like its neighbours (old D53) | `particularly` | 8 |
| class_23/10_ud.md:17 | `stands up, get out of` | Number (old D54) | `gets out of` | 9 |
| class_23/20_mixed_pref.md:6 | `sit down hard` | Third person `-s` missing; the gloss itself is DPD's ("sits down hard; sits heavily") (old D55) | `sits down hard` | 8 |
| class_23/22_dur_su_nir.md:1 | `# dur, su, nir & etc.` | `& etc.` (also index.md:105, class_23/index.md:24) (old D56) | `dur, su, nir, etc.` | 8 |
| class_23/21_nipata.md:3; class_23/22_dur_su_nir.md:3 | `but they are much less common` / `only with **nouns** and **adjectives**` | No full stop at the end of the paragraph (also 1_prefix.md:49, 53) | Add it | 8 |
| class_24/3_caus.md:29 | `great blowing winds **causes**` | Agreement (old D57) | `**cause**` | 9 |
| class_24/5_caus_pass.md:53 | `My good man did you not see` | Missing comma (old D58) | `My good man, did you not see` | 8 |
| class_24/6_app.md:42 | `is like **pakkhī**, in **feminine** like **nadī** and the **neuter** like **aṭṭhi**` | Broken parallelism; no full stop (old D59) | `the feminine like **nadī** and the neuter like **aṭṭhi**.` | 7 |
| class_25/1_deriv.md:3 | `are formed, now we take a look` | Comma splice (old D60) | Full stop | 7 |
| class_25/2_nouns.md:15 | `often translating with -ing` | Verb form (old D61) | `often translated with -ing` | 8 |
| class_25/3_anub.md:15, 17 | `the first vowel is *always* lengthened` / `Except when ...` | `always` is followed by three exceptions; guṇa (`bhuj > bhoga`) is not lengthening (old D62) | `is strengthened, except when …` | 7 |
| class_25/5_taddh_2.md:232 | `cats-eye` | Apostrophe (old D63) | `cat’s-eye` | 7 |
| class_25/6_home_work.md:5 | `please break-up every noun` | The verb is two words (old D64) | `break up` | 9 |
| class_24/1_pass.md:19 | `What is the subject(s) of this sentence?` | Number | `What is (are) the subject(s)` | 7 |
| class_26/2_numer.md:48, 54, 55; class_26/4_ind.md:81 | `consisting of hundred` / `consisting of thousand` / `in hundred ways` | Missing article (old D65) | `a hundred`, `a thousand` | 7 |
| class_26/3_state.md:9 | `nature, character,` | Trailing comma (old D66) | Remove it | 9 |
| class_26/3_state.md:7 | `sorrow-less-ness` | Hyphenation (old D67) | `sorrowlessness` | 6 |
| class_26/4_ind.md:17, 27 | `(in such way)` | Missing article (old D68) | `in such a way` | 7 |
| class_27/2_kicca.md:5, 7, 9 | `Please note in many of the examples that follow` / `just the **root** or **base** + **suffix** is being used,` / `but the same applies to **prefix** + **root** or **base** + **suffix**` | One sentence over three paragraphs, with no full stop (old D69) | One line | 6 |
| class_26/5_home_work.md:5 | `please break-up every noun or adjective` | The verb is two words (as class_25/6_home_work.md:5) | `break up` | 9 |
| class_28/1_kita_1.md:435 | `one who stealing` | Grammar (old D70) | `one who steals` | 10 |
| class_28/1_kita_1.md:641 | `is used to forming` | Grammar (old D71) | `is used to form` | 10 |
| class_28/1_kita_1.md:180, 200 | `to breath` | The verb is "breathe" (old D72) | `to breathe` | 10 |
| class_28/1_kita_1.md:489 | `\| √nhā \| to bath \| **+ aka** \| nhāp**aka** \| bathman \|` | The verb is "bathe"; "bathman" is not usual English (old D73) | `to bathe`; `bath attendant` | 8 |
| class_28/1_kita_1.md:422, 423 | `to do make` | Missing comma (old D74) | `to do, make` | 9 |
| class_28/1_kita_1.md:97 | `\| √kalah \| argue \|` | A root gloss without "to" (file 2: see p10) (old D75) | `to argue` | 9 |
| class_28/1_kita_1.md:333, 36 | `as we saw on the last class` / `As we saw last week` | Preposition; also "last week" on lines 36, 229, 347 (old D76) | `in the last class` (one phrase throughout) | 8 |
| class_28/1_kita_1.md:229 | `last week. it also forms` | Lower-case sentence start (old D77) | `It also forms` | 10 |
| class_28/1_kita_1.md:28 | `Here are most of *kita* suffixes in DPD` | Missing article and end punctuation (old D78) | `Here are most of the *kita* suffixes in DPD:` | 8 |
| class_28/1_kita_1.md:347 | `last week, can you think of an example?` | Comma splice (old D79) | `last week. Can you …` | 7 |
| class_28/1_kita_1.md:3 | `nouns, adjectives, substantives and participles` | "Nouns" and "substantives" are the same thing (also class_27/1_kitaka.md:13 and class_25/1_deriv.md:3) (old D80) | Drop one | 6 |
| class_28/2_kita_less.md:83 | `\| √puṇ \| be skilful, precise \|` | A root gloss without "to" (file 1: see p09) (old D75) | `to be skilful, precise` | 9 |
| class_28/3_home_work.md:5 | `Make note of all kita kicca and taddhita suffixes.` | Missing comma; the terms are italic elsewhere (old D81) | `*kita*, *kicca* and *taddhita* suffixes` | 7 |
| class_28/3_home_work.md:21 | `viewform), your corrections` | Comma splice (old D82) | Full stop | 7 |
| class_28/3_home_work.md:5 | `please break-up every word down to the prefixes` | `break-up` as a verb, and "up … down" together (class_27/4_home_work.md:5 has `break every word down`) | `break every word down` | 9 |
| class_28/2_kita_less.md:170, 289 | `suffix **ikā** is used to form feminine nouns and feminine agent nouns` / `suffix **āna**, as we saw last week, is used to form the **present participle**` | Lower-case sentence starts, no full stop (also line 488) | Capitals and full stops | 8 |

## E. Markdown defects that affect rendering

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_16/1_sandhi.md:55 | `(*vyañjana-sandhi)*` | The closing `*` is outside the bracket (line 53 has `(*sara-sandhi*)`) (old E1) | `(*vyañjana-sandhi*)` | 10 |
| class_16/3_vowel_1.md:5, 7 | `pacman-forward.png)it eats` / `backwards,![]` | No space between image and text (old E2) | Add the spaces | 9 |
| class_16/7_vowel_5.md:27 | `**kvac’āsavaṇṇaṃ** **lutte**.` | Bold split in two (old E3) | `**kvac’āsavaṇṇaṃ lutte**` | 8 |
| class_16/10_vowel_8.md:34 | `kālass’ev**a v**uṭṭhahanto` | Bold spans a space, and the sandhi result is written as two words | `kālass’eva**v**uṭṭhahanto` | 7 |
| class_16/2_vowel.md:1 | `# Vowel Sandhi *(sara-sandhi)*` | Italic includes the brackets; other headings and `1_sandhi.md:53` italicise only the term (index link text has no italics: mech-output) | `# Vowel Sandhi (*sara-sandhi*)` | 8 |
| class_17/3_cons_1.md:11; class_17/8_nig_1.md:11; class_17/10_nig_3.md:9 | `**para** **dvebhāvo ṭhāne**` / `**aṃ** **byañjane** **niggahitaṃ**` / `**vagg’antaṃ** **vā vagge**` | Bold split into pieces (old E4) | One bold span | 8 |
| class_17/3_cons_1.md:167, 168 | `**b**haya` / `**b**havika` | Bold on `b`; the heading is `vowel + bh` (old E5) | `**bh**aya`, `**bh**avika` | 9 |
| class_17/15_nig_8.md:18 | `ariya-<br>saccāna**ṃ**` | `<br>` and a hyphen inside a word (old E6) | owner decision (`<br>` in cells) | 7 |
| class_17/2_cons.md:1 | `# Consonant Sandhi (*vyañjana-sandhi)*` | The closing `*` is outside the bracket (mech-output: index link differs) | `(*vyañjana-sandhi*)` | 10 |
| class_17/9_nig_2.md:25 | `\| **k** \| **kh** \| **g** \| **gh** \| **ṅ** \|` | The letter row is a data row of five cells above rows whose cells mean something else (word, word, result, gloss); the same in the four tables below (lines 36, 49, 58, 69) | Put the letters in the heading line, e.g. `**ṃ + k kh g gh ṅ \> ṅ**` | 6 |
| class_18/1_phonetic.md:17 | `1.  **Assimilation** happens` | Follows the list of lines 5–15 with only blank lines between, so Markdown continues that list and renders it as item 7 (old E7) | Separate it with a paragraph or heading, or drop the numbers | 8 |
| class_18/2_as_ya.md:1, 3 | `# Phonetic changes of -y-` / `## Phonetic changes of -y-` | The same heading twice (old E8) | Remove the H2 | 9 |
| class_18/2_as_ya.md:33 | `\| \| √guh \| (to hide) \| **+ ya** \| guyha \| could be hidden \|` | The first data row is the table header (renders bold); all other tables have an empty header row (old E9) | Add an empty header row | 9 |
| class_18/5_as_sa.md:10 | `√bhuj + bhuj\> bubhuj` | Missing space before `\>` (old E10) | `bhuj \> bubhuj` | 9 |
| class_18/6_as_sum.md:7 | `tijti**j s**a ti` | Words run together, no `√`; the lesson has `titij + sa + ti` (old E11) | `titi**j s**a ti` | 8 |
| class_18/6_as_sum.md:18, 44 | `√k**an y**a ā` / `√**jal y**a` | The bold starts one or two letters early; it should mark only the two meeting consonants (old E12) | `√ka**n y**a ā`, `√ja**l y**a` | 9 |
| class_18/9_ex.md:10 | `√ādā + ta` | `+` where the other deconstruction answers have spaces; the root `√ādā` itself is a DPD root (old E13) | `√ādā ta` | 7 |
| class_18/11_ex.md:11, 24 | `\| \|` | A lone one-cell row after each table (mech-output: cols 1 != 4) (old E14) | Remove, or accept as a spacer | 7 |
| class_18/2_as_ya.md:44, 45 | `\| ā \| √gam \| (to go) \| + ya \| āga**mm**a \| arriving \| \|` | A seventh, empty column in this table only; `+ ya` is not bold as in the table above | Drop the empty column; bold `+ ya` | 7 |
| class_19/2_kamm.md:135 | `becomes **mahā, or**` | `, or` inside the bold (old E15) | `**mahā**, or` | 8 |
| class_19/2_kamm.md:141 | `mah**abb**haya` | The bold cuts `bbh` in two (old E16) | `maha**bbh**aya` | 9 |
| class_19/5_dvanda.md:25 | `brāhmaṇ**ānaṃ “of** ascetics` | One bold span runs from the Pāli ending across the quote mark into the English (old E17) | `**ānaṃ** “**of** ascetics` | 9 |
| class_20/2_bahub.md:19 | `viharāmi**.**` | Bold full stop (old E18) | `viharāmi.` | 9 |
| class_20/4_change_comp.md:10 | `*pañcagu[^9]*` | Footnote marker inside the italics (old E19) | `*pañcagu*[^9]` | 7 |
| class_20/5_ex.md:8, 13, 18, 23 | `{: .align-right }` | attr_list markup in the source; the only file in `docs/ipc` that has it (project rule: clean Markdown) (old E20) | owner decision | 7 |
| class_19/1_comp.md:1 | `# Compounds (*samāsa)*` | The closing `*` is outside the bracket (mech-output: index link differs) | `(*samāsa*)` | 10 |
| class_19/4_tap.md:65 | `*tuṃpaccaya* *tappurisa*` | Italic split in two | `*tuṃpaccaya tappurisa*` | 8 |
| class_21/4_pres.md:7, 9 | `(*parassapada)*` / `(*attanopada)*` | The closing `*` is outside the bracket (old E21) | `(*parassapada*)`, `(*attanopada*)` | 10 |
| class_21/6_opt.md:9 | `in the reflexive **voice and passive voice.**` | The bold starts mid-phrase (4_pres.md:9 has `**reflexive** **voice** … **passive voice**`) (old E22) | `**reflexive voice** and **passive voice**.` | 8 |
| class_21/8_imperf.md:20 | `agam**u<br>**agam**ū**` | The bold span closes after the `<br>` (old E23) | `agam**u**<br>agam**ū**` | 9 |
| class_22/3_root_groups.md:144 | `## 7. tanādigaṇa (-o- *-yira[^14]-*)` | A footnote marker inside italics inside a heading (old E24) | Move the marker out | 8 |
| class_23/23_home_work.md:5, 12 | `3.  In the exercises, break up every verb and participle into` / `e.g. viññāṇaṃ : vi + √ñā + aṇa vi + √ñā 5 nā (know) + aṇa + aṃ` | The continuation lines (6–14) are not indented under item 3; line 12 runs two analyses together; space before the colon (old E25) | Restructure | 8 |
| class_23/23_home_work.md:14 | `*object(s)* and \*predicate\*` | The escaped asterisks print literally; the intended styling is unclear (old E26) | verify the intent | 7 |
| class_24/1_pass.md:53 | `√dhar+ \*e` | Missing space (old E27) | `√dhar + \*e` | 9 |
| class_24/2_irreg_pass.md:11 | `Kacc 502, 493**.** **yamhi** **dā dhā mā ṭhā hā pā maha-math’ādīnam’ī**.` | Bold full stop; split bold (old E28) | One bold span | 9 |
| class_24/2_irreg_pass.md:34, 39 | `chindīyati[^22]` / `These bases (marked with \*) mostly exist in participle forms.` | The first row carries the footnote number in place of `\*`; the note repeats `[^20]` of 1_pass.md:58; `hiyyati\*` on line 46 is in another table (old E29) | `chindīyati\*`, and the note once | 8 |
| class_24/2_irreg_pass.md:82, 93 | `**√va**ḍḍh` / `√**ph**ar` | The bold includes `√`; bold on `ph`, not `pha` (old E30) | `√**va**ḍḍh`, `√**pha**r` | 9 |
| class_24/5_caus_pass.md:11, 15 | `\***e**` / `**\*āpe**` | `\*` is outside the bold in two items and inside it in two (old E31) | One form | 8 |
| class_25/1_deriv.md:13, 19 | `*dhātu + kita / kicca \> kitaka*` / `## *kitaka + taddhita \> taddhita*` | Parallel formulas: one is a paragraph, the other an H2 at the end of the file (old E32) | Both as paragraphs | 9 |
| class_25/3_anub.md:7 | `e.g. ṇ**a or \*a**` | The bold starts mid-word and covers `or` (old E33) | `**ṇa** or **\*a**` | 9 |
| class_25/5_taddh_2.md:84, 86, 108, 159, 160 | `g**ā**mi**ka**` / `m**ā**gadhi**ka**` / `s**ā**rīri**ka**` / `b**ā**hiy**a**` / `**ā**nuttariya` | The suffix bold is cut short or missing (`**ika**`, `**iya**` elsewhere) (old E34) | `g**ā**m**ika**` etc. | 9 |
| class_25/5_taddh_2.md:129 | `\| \| \| \| belonging to the ... \|` | The only table in the file with text in the header row; `...` | Move the phrase to the heading on line 127 | 6 |
| class_26/4_ind.md:9 | `**36 times**` | The only bold gloss in the table (old E35) | Remove the bold | 9 |
| class_26/3_state.md:75 | `t**accha**` | The bold cuts the word unlike its neighbours (`s**ā**ta**cca**`) (old E36) | `ta**ccha**` | 8 |
| class_27/3_kita.md:64, 65, 89 | `phuṭ**ṭha**` / `rat**ta**` / `bhin**na**` | The bold splits the assimilated cluster (cf. `ka**ṭṭha**`, `ma**tta**`, `chi**nna**`) (old E37) | `phu**ṭṭha**`, `ra**tta**`, `bhi**nna**` | 9 |
| class_28/1_kita_1.md:596 | `sabh**o**jan**a**` | The bold marks only the final `a`; the suffix is `ana` (line 597 has `ac**e**t**ana**`) (old E38) | `sabh**o**j**ana**` | 9 |
| class_28/1_kita_1.md:337 | `a large group **of past participles**` | `of` is inside the bold span (old E39) | `of **past participles**` | 9 |
| class_28/1_kita_1.md:527, 528 | `\| √gaves \| to seek \| **+ ī** \| gavesī \|` / `\| √dus \| to be corrupt \| **+ ī** \| dūsī \|` | The suffix is not bold in the result column (file 2: see p10) (old E40) | `gaves**ī**`, `dūs**ī**` | 9 |
| class_28/1_kita_1.md:412, 649, 702, 611 | `\| **total** \| 265 \|` / `\| **total** \| 139 \|` / `\| **total** \| 138 \|` / `\| adj \| 143 \|` | The total figure is not bold (it is bold in the other tables); the POS labels are not bold in the `\*ī` table (lines 611–613) (old E41) | Make them uniform | 9 |
| class_28/2_kita_less.md:54, 176, 186, 280, 351, 358, 384, 391, 433, 439, 479, 508, 515 | `\| √cakkh \| to see \| **+ u** \| cakkhu \|` / `jīvikā` / `upāsikā` / `vattha` / `ārādhika` / `kathika` / `hutta` / `satta` / `kurara` / `pabhassara` / `p**o**ta` / `m**ū**sikā` / `n**āy**ikā` | The suffix is not bold in the result column (also the neighbouring rows 55, 56, 177–180, 187, 281, 352, 359, 385, 392, 480, 509, 516; file 1: see p09) (old E40) | Bold the suffix, as in the rest of the file | 9 |
| class_20/5_ex.md:23 | `{: .align-right }` | The file ends without a final newline (mech_checks); the last line is this attribute line | Add the newline | 8 |

## F. Convention drift

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_16/1_sandhi.md:57 | `**Ṃ Sandhi** *niggahīta-sandhi* which` | No brackets, unlike items 1 and 2 (old F1) | `(*niggahīta-sandhi*)` | 9 |
| class_16/1_sandhi.md:39 | `wouldn’t = would not` | No bold on the elided letter, unlike lines 17–37 (old F2) | `would n**o**t` | 8 |
| class_16/1_sandhi.md:47 | `Why is there sandhi?` | Plain paragraph; the parallel question on line 11 is a `##` heading (old F3) | Make it a heading | 7 |
| class_16/1_sandhi.md:13 | `this is called **euphonic combination**` | Repeats line 5 (old F4) | Merge the two | 6 |
| class_16/2_vowel.md:13, 15 | `*lopa,*` / `*dīghaṃ,*` | Comma inside the italics; lines 17 and 19 have it outside (old F5) | `*lopa*,` | 8 |
| class_16/3_vowel_1.md:33, 48 | `pana \| **assa**` / `yena \| **āyasmā**` | The whole second word is bold and the first word has no bold; all other rows bold only the meeting vowels (old F6) | `pan**a** \| **a**ssa`, `yen**a** \| **ā**yasmā` | 9 |
| class_16/3_vowel_1.md:248; class_16/4_vowel_2.md:132; class_16/5_vowel_3.md:122; class_16/10_vowel_8.md:110 | `**Possibility \#1** ?` / `**Possibility \#2**?` / `**Possibility \#3 ?**` / `**what is Possibility \#8 ?**` | Four stylings of the recap question (old F7) | One form | 9 |
| class_16/3_vowel_1.md:11 | `a vowel before another vowel is sometimes elided` | Lower case, no full stop (also line 250); the other rule statements are sentences (old F8) | Capitalise, add a full stop | 8 |
| class_16/3_vowel_1.md:1, 9; class_16/4_vowel_2.md:1 | `# Elision of a Vowel` / `## Possibility \#1` / `# Possibility \#2 — Elision of the Following Vowel` | Possibilities 1, 3, 5, 8 are H2 under a topic H1; 2, 4, 6, 7, 9 are H1 (old F9) | One scheme | 8 |
| class_16/5_vowel_3.md:9 | `a![](../../assets/images/pacman-backwards.png)![](../../assets/images/arrow.png)a \> ā` | Not bold; the same line is bold in files 3, 4, 6 (old F10) | Bold | 8 |
| class_16/8_vowel_6.md:15 | `**together they become ya**` | Whole line bold; 9_vowel_7.md:15 bolds only the result (old F11) | `together they become **ya**` | 8 |
| class_16/10_vowel_8.md:32, 47 | `s**uva**tthi` / `saññ**īme**va` | Bold covers the neighbouring vowels; other rows bold only the inserted consonant (old F12) | `su**v**atthi`, `saññī**m**eva` | 8 |
| class_16/11_vowel_9.md:23 | `*sara-sandhi-niṭṭhitaṃ*` | The file ends without a "what is Possibility #9?" recap, unlike files 3–10 (old F13) | Add it, or accept | 6 |
| class_16/12_vowel_ref_table.md:119, 121, 123 | `aggi iva \> agg**î**va` | Source vowels not bold, unlike lines 111–117 (old F14) | Bold them | 8 |
| class_16/13_home_work.md:3, 11 | `1.  Please` / `1\. Find` | A real list and an escaped pseudo-list in one file (old F15) | One form | 7 |
| index.md:39, 45, 117 | `Phonetic changes of -y-` / `Another consonant assimilation` / `Types of nouns` | Sentence case (also lines 40–42); all other titles are Title Case (old F16) | Title Case | 8 |
| index.md:18; class_16/3_vowel_1.md:7; class_16/13_home_work.md:5, 42 | `Pāli Alphabet Analysis` / `very common in Pāli` / `“Grammar Pāli Class”` / `Māgadhabhāsā (pāḷi)` | `Pāli` in running text; the project name has `Pāḷi` (old F17) | owner decision | 6 |
| class_16/3_vowel_1.md:3 | `**forward** and **backwards** elision` | `forward` without `s`, `backwards` with (also lines 5 and 7) | `forward` / `backward`, or both with `s` | 6 |
| class_16/4_vowel_2.md:25 | `iti’ss**a** \| **i**me \| itiss**a**me` | Apostrophe in the source word, none in the result; no other row marks an earlier sandhi | `itiss**a**` | 7 |
| class_16/6_vowel_4.md:29, 52 | `this occurs with all words ending in **a + iti**` / `this occurs with all words ending in **u + iti**` | A prose note inside a table row, lower case, no full stop | Move below the table as a sentence | 7 |
| class_16/4_vowel_2.md:19; class_16/7_vowel_5.md:27; class_16/3_vowel_1.md:27 | `**vā paro asarūpo.**` / `**lutte**.` / `**sarā sare lopaṃ**` | Kaccāyana quotes end three ways: full stop inside the bold (6 files), outside it (7_vowel_5.md, 10_vowel_8.md:15), none (3_vowel_1.md, 8_vowel_6.md:17) | One form | 8 |
| class_16/10_vowel_8.md:5, 112; class_16/12_vowel_ref_table.md:99 | `**d r m y v.**` / `**d r m y v**.` / `**ŋ.**` | Full stop inside the bold on line 5 and in the ref table, outside it on line 112 | Full stop outside the bold | 8 |
| class_17/3_cons_1.md:11; class_17/4_cons_2.md:11; class_17/7_cons_5.md:11 | `**para** **dvebhāvo ṭhāne**` / `**para-dvebhāvo ṭhāne**` / `**para dvebhāvo ṭhāne.**` | The same sutta (28) written three ways (old F18) | One form | 9 |
| class_17/2_cons.md:7, 13; class_17/3_cons_1.md:1 | `Re-duplication` / `Re-duplication and shortening` / `Consonant Reduplication` | Spelling drift (old F19) | `Reduplication` | 9 |
| class_17/3_cons_1.md:21, 115, 22, 76 | `masc. impurity` / `m. breadth` / `fem. conception` / `f. covetousness` | Both sets of abbreviations are used (old F20) | One set | 9 |
| class_17/4_cons_2.md:22; class_17/3_cons_1.md:152 | `ger. understanding` / `abs. having shaken out` | Two labels for the same form (old F21) | `abs.` | 8 |
| class_17/7_cons_5.md:15 | `adj \| final, complete` | The POS is in its own column without a full stop (lines 15–20); the other tables of the class put `adj.` in the gloss cell (old F22) | One layout | 8 |
| class_17/3_cons_1.md:53, 114, 143, 167 | `n**a** \| **c**uta` / `**na** \| **th**addha` / `**na** \| **p**amāda` / `n**a** \| **b**haya` | The negative `na > a` is bolded two ways, and the change `na > a` is not shown (old F23) | One form, e.g. `na \> **a**` | 8 |
| class_17/4_cons_2.md:29 | `Counter-examples:` | Not bold; bold in every other file (old F24) | Bold | 9 |
| class_17/5_cons_3.md:51 | `pūj'ārahe` | Straight apostrophe; the rest of the class has `’` (old F25) | `pūj’ārahe` | 9 |
| class_17/6_cons_4.md:3, 57 | `**eso & n’eso**` / `or **neso**` | Apostrophe drift (old F26) | One form | 7 |
| class_17/6_cons_4.md:11 | `**esa** **m**aggo` | Split bold; lines 33, 35, 45 have `**esa m**aggo` (old F27) | `**esa m**aggo` | 8 |
| class_17/1_alphabet_analys.md:37, 67; class_17/9_nig_2.md:17, 45 | `Cerebral or Retroflex` / `Cerebral / Retroflex` / `**cerebral**` / `**ṃ + retroflex \> ṇ**` | Term drift (old F28) | One term | 8 |
| class_17/8_nig_1.md:44, 45, 46 | `**kh**itta \| saṃkhitta` / `**s**andati \| saṃsandati` / `**d**iṭṭhī \| evaṃdiṭṭhī` | The fourth column holds the joined form here and a translation in the rows above (old F29) | Add glosses | 7 |
| class_17/9_nig_2.md:70, 72, 73; class_17/10_nig_3.md:17 | `upa sa**ṃ**` / `abhi sa**ṃ**` / `paṭi sa**ṃ**` / `paṭi + sa**ṃ**` | `+` missing in 9_nig_2.md (old F30) | Add `+` | 8 |
| class_17/10_nig_3.md:15, 16 | `sa**ll**apati` / `sa**l**lekha` | Bold on `ll` in one row, on `l` in the next three (old F31) | One form | 9 |
| class_17/15_nig_8.md:17, 18 | `buddhān**a**sāsanaṃ` / `ariyasaccān**a** dassanaṃ` | Result joined in one row, spaced in the others (old F32) | One form (spaced, as in the texts) | 7 |
| class_17/3_cons_1.md:100; class_17/9_nig_2.md:43 | `(commentary example)` / `comm word` | Footnote wording drift (old F33) | One wording | 7 |
| class_17/19_home_work.md:14, 15 | `p12 - 14` / `p13-28` | Page-range style (old F34) | One style | 8 |
| class_17/index.md:5, 11 | `Possibility \#1 — Consonant Reduplication` / `Possibility \#2 — ṃ Becomes the Group Nasal` | Two numbering series (consonant 1–5, niggahīta 1–10) in one flat list; niggahīta #1 is hidden under `Niggahīta Sandhi` (old F35) | owner decision | 6 |
| class_17/8_nig_1.md:3; class_17/11_nig_4.md:3; class_17/12_nig_5.md:3 | `**beginning with a vowel or a consonant.**` / `**e,**` / `**y,**` | Full stop or comma inside the bold (also 11_nig_4.md:5, 16_nig_9.md:31 `**iva,**`) | Punctuation outside the bold | 8 |
| class_17/14_nig_7.md:9, 19 | `im**aṃ** + **a**haṃ \> im**ā**haṃ` / `ima**ṃ** \| **a**haṃ \| im**ā**haṃ` | Bold on `aṃ` in the lead example, on `ṃ` in the table | `ima**ṃ**` | 7 |
| class_17/12_nig_5.md:20; class_17/13_nig_6.md:34; class_17/9_nig_2.md:80 | `saṃ + yoga \> saṃyoga` / `ma**ṃ a**vadhi` / `saṃ khitta \> sa**ṃ**khitta` | Counter-examples are written four ways across the class: with or without bold, with or without `+`, with or without `\>` and a result | One form | 7 |
| class_17/1_alphabet_analys.md:35, 36 | `Guttural <br>(*kaṇṭhaja*)` / `Palatal<br>(*tāluja*)` | Space before `<br>` only after `Guttural` (also line 65) | Remove the space | 8 |
| class_17/19_home_work.md:5; class_16/13_home_work.md:3 | `3.  Reread this class` / `1.  Please re-read this lesson` | `Reread` / `re-read`, `class` / `lesson`, and a different order of the same homework items | One wording and order | 6 |
| class_17/1_alphabet_analys.md:73, 51 | `the un-aspirate of the letter kh` / `Unaspirates<br>(*sithila*)` | `un-aspirate` / `Unaspirates` | `unaspirate` | 7 |
| class_18/7_mix_san.md:36, 37 | `ud + a + √vadh \> badh + i` / `ud + a + √vah + i` | The step `v > b` is shown for `udabbadhi` only; DPD has it for `udabbahi` as well (`√vah > bah`) | roots confirmed by DPD; add the step in row 37: `ud + a + √vah \> bah + i` | 7 |
| class_18/1_phonetic.md:47, 61 | `(ger. descending)` / `(abs. having given up)` | `ger.` and `abs.` in one file; class 18 otherwise has `ger.` / gerund (2_as_ya.md:13) and `absolutive` once (3_as_ta.md:5), class 17 `abs.` (old F36) | One term course-wide | 9 |
| class_18/2_as_ya.md:5, 9 | `verbs of the **3rd** **conjugation**` / `**group 3 & passive verbs**` | Two names for the same thing; split bold (old F37) | One name | 7 |
| class_18/6_as_sum.md:8, 36 | `ni √mujj ta` / `√tij \> tip + ta \| tippa` | No bold in these rows; row 36 has `\>` and `+`, unlike the rest (old F38) | Match the other rows | 9 |
| class_18/7_mix_san.md:1 | `(vomissaka-sandhi)` | Not italic; the class 16 and 17 H1s italicise the Pāli term (old F39) | owner decision | 6 |
| class_18/7_mix_san.md:15, 16 | `a**ti** **e**ti` / `a**ti** **u**ṇha` | The following vowel is bold only in these two rows (old F40) | Remove the bold | 8 |
| class_18/10_irreg_masc.md:12 | `**mano**` | Whole word bold; elsewhere only the ending (old F42) | `man**o**` | 9 |
| class_18/10_irreg_masc.md:69, 76, 71, 72 | `g**avo**` / `gav**o**` / `go**hi**` / `gun**naṃ**` | The stem/ending split differs between cells of one paradigm (old F43) | One split | 9 |
| class_18/10_irreg_masc.md:65, 78 | `**Declension of go (masc) cow, cattle**` / `**Declension of atta (masc) - self**` | Dash drift (also line 93) (old F44) | One form | 8 |
| class_18/10_irreg_masc.md:20 | `dukkho'ti` | Straight apostrophe (old F45) | `dukkho’ti` | 9 |
| class_18/10_irreg_masc.md:22, 91 | `Similarly` / `similarly:` | Case and punctuation (old F46) | One form | 7 |
| class_18/10_irreg_masc.md:106, 110 | `**In summary:** for the **mano-group**, learn to recognize the compound form in **-o**` / `recognize them from context.` | The only hard-wrapped paragraph in the class (lines 106–110); it uses `—` (old F47) | One line | 7 |
| class_18/10_irreg_masc.md:3, 20 | `Beginner Pāli Course` / `classical Pāḷi grammars` | Both spellings in one file (old F48) | owner decision | 7 |
| class_18/10_irreg_masc.md:5 | `**manas**, **go, atta** and **rāja**` | Bold spans two words and a comma; no full stop | `**manas**, **go**, **atta** and **rāja**.` | 8 |
| class_18/11_ex.md:3; class_18/2_as_ya.md:64; class_17/8_nig_1.md:35; class_18/7_mix_san.md:33 | `Please analyze` / `analysing in detail` / `often practiced` / `practised` | US and UK spellings side by side | owner decision | 6 |
| class_18/4_as_na.md:22; class_18/1_phonetic.md:35 | `√jīr + na \| ji**ṇṇ**a \| pp. aged` / `ji**ṇṇ**a (adj. old)` | The same derivation is `pp.` in one file and `adj.` in the other | `pp.` in both (DPD: pp of `jīrati`) | 8 |
| class_18/2_as_ya.md:44, 130 | `āga**mm**a \| arriving` / `āga**mm**a \| ger. coming` | The same example twice in one file with two glosses; the first has no `ger.` | One gloss | 7 |
| class_19/2_kamm.md:7; class_19/3_digu.md:3; class_19/4_tap.md:5 | `*Kaccāyana 324.* dvipade` / `**Kaccāyana 325. saṅkhyāpubbo digu.**` / `Kaccāyana 326. ubhe tappurisā.` | Three stylings of the sutta citation in one class (also 5_dvanda.md:5; class_20/1_abya.md:5 and 2_bahub.md:267 are bold); classes 16–17 have `In Kaccāyana this is called (n) **…**` (old F49) | owner decision (Kaccāyana citation style) | 9 |
| class_19/2_kamm.md:7 | `tuly'ādhikaraṇe` | Straight apostrophe (old F50) | `tuly’ādhikaraṇe` | 9 |
| class_19/1_comp.md:15, 35 | `*kammadhāraya or* **adjectival** *(adjective + noun)*` / `*bahubbīhi* or **attributive** (meaning is different from the component words)` | The italics cover `or` and the bracket in items 1–5, not in 6–7 (old F51) | Italic only on the Pāli term | 9 |
| class_19/3_digu.md:1; class_19/4_tap.md:1; class_19/5_dvanda.md:1, 76, 88 | `# Digu-samāsa or` / `# Tappurisa-samāsa or` / `# Dvanda Samāsa or` / `*dvandasamāsa* occur` / `Dvandasamāsa also` | Hyphen and case drift in the H1s; the body also has `dvanda-samāsa` (5_dvanda.md:21) (old F52) | One form | 9 |
| class_19/4_tap.md:21, 31 | `## dutiyā-tappurisa (accusative case)` / `## tatiyā tappurisa (instrumental case)` | Hyphen only in the first heading (old F53) | One form | 9 |
| class_19/2_kamm.md:19, 23 | `mahant**o** puris**o** \>` / `thull**aṃ** + accay**aṃ** \>` | `+` between the members is present or absent at random (also throughout 4_tap.md) (old F54) | One form | 8 |
| class_19/2_kamm.md:3; class_19/4_tap.md:3 | `**“blackbird”**` / `“madhouse”` | The English example is bold in one file only (old F55) | One form | 8 |
| class_19/4_tap.md:75, 77 | `(born from seclusion)` / `(not risen out of the water)` | The case preposition is not bold, unlike the rest of the file (old F56) | Bold `from`, `out of` | 7 |
| class_19/6_comp_rules.md:17 | `viññugarahita` | The changed vowel is not bold, unlike lines 19 and 21 (old F57) | `viññ**u**garahita` | 8 |
| class_19/1_comp.md:3 | `saṃ + √ās + a` | No result (`\> samāsa`), unlike `saṃ + √dhā + i \> sandhi` in class 16 (old F58) | Add the result | 7 |
| class_19/3_digu.md:7; class_19/4_tap.md:11, 53, 81 | `digu is an example of a digu compound` / `tappurisa is an example of a tappurisa compound` / `all compounds with infinitive/dative + kāma are in this category` / `most common` | Many sentences start lower-case or lack a full stop (also 2_kamm.md:61, 5_dvanda.md:27, 43, all items of 6_comp_rules.md; class 20: 1_abya.md:7, 2_bahub.md:9–99, 269) (old F59) | Sentence case and full stops | 7 |
| class_19/8_home_work.md:13, 14 | `\| Duroiselle \| samāsa \|` / `\| Perniola \| samāsa \|` | No page numbers and no Māgadhabhāsā row, unlike classes 16–18 (class_20/6_home_work.md:13 gives chapters, also without Māgadhabhāsā) (old F60) | Add them | 6 |
| class_20/2_bahub.md:235 | `tvaṁ` | `ṁ`; the course has `ṃ` (the only other `ṁ` are the deliberate ones in class_16/12_vowel_ref_table.md) (old F61) | `tvaṃ` | 10 |
| class_20/2_bahub.md:125, 133 | `ādittasīso – (a man)` / `chinnasoto - (an arahant)` | En dash and hyphen mixed in one list (lines 125–183) (old F62) | One dash | 9 |
| class_20/2_bahub.md:267; class_20/3_mis.md:13; class_20/4_change_comp.md:21 | `aññapad'atthesu` / `devamānuse'ti` / `one's own` | Straight apostrophes (4_change_comp.md:21 has `one’s` and `one's` in one cell) (old F63) | `’` | 10 |
| class_20/2_bahub.md:103, 105 | `“who...”, “which…”, “that …”` / `“the man who….”` | Three or four dots, `...` and `…`, spacing (old F64) | `…` | 8 |
| class_20/2_bahub.md:7, 43 | `(noun. paddy)` / `(n. tree)` | Abbreviation drift (also line 25 `noun.`) (old F65) | `n.` | 8 |
| class_20/2_bahub.md:187, 191 | `\> acelaka` / `\> paṃsukūliko` | Stem in two results (also line 209), nominative in the others (old F66) | One form | 8 |
| class_20/1_abya.md:21; class_20/3_mis.md:9 | `**yāvajīvaṃ \> yāva + jīva + aṃ**` / `upekkhāsambojjhaṅga \< upekkhā + sambojjhaṅga` | Deconstruction is written with `\>` in one file and `\<` in the other (old F67) | `\<` | 8 |
| class_20/3_mis.md:7, 13 | `*[SN46.53](https://s.dhamma.gift/sn/sn46/index.html#sn46.53)*  akālo` / `*[MN53](https://s.dhamma.gift/mn/mn53/index.html)* **vijjācaraṇasampanno**` | Italic reference before the text (two spaces after it on lines 7 and 19); elsewhere `([REF](url))` after the text (old F68) | One form | 8 |
| class_20/4_change_comp.md:1 | `# Changes Of Certain Words In Compounds` | `Of` and `In` capitalised (also index.md:63, class_20/index.md:6) (old F69) | `Changes of Certain Words in Compounds` | 8 |
| class_20/4_change_comp.md:19, 20 | `\| saha \| with \| sa- \|` / `\| saka \| one’s own \| sa \|` | Hyphen drift (old F70) | One form | 7 |
| class_20/4_change_comp.md:23; class_16/7_vowel_5.md:70 | `Not a textual example` / `not textual example` | The same footnote worded two ways (old F71) | One wording | 8 |
| class_20/1_abya.md:9, 17 | `1.  the first member of these compounds` / `3.  The resulting compound` | Case of the list items (old F72) | Sentence case | 8 |
| class_19/1_comp.md:5; class_20/2_bahub.md:221, 263 | `**single** **unit**` / `**feminine** **nouns** take their **masculine** **forms**` / `**missing** **subject has to be understood.**` | Adjacent words bolded separately; on line 263 the bold also takes in the full stop | One bold span; full stop outside | 8 |
| class_19/4_tap.md:111, 121 | `**alutta dutiyā tappurisa - accusative (most common)**` / `**alutta tatiyā tappurisa - instrumental**` | The alutta sub-types are bold paragraphs with ` - `; the six types above them are `##` headings with the case in brackets | `### alutta dutiyā tappurisa (accusative case)` | 7 |
| class_20/1_abya.md:38 | `## Sometimes the original case ending is maintained` | A full sentence as a heading | Shorter heading, or a paragraph | 6 |
| class_21/4_pres.md:17; class_21/5_imp.md:17 | `\| \| **s** \| **pl** \|` / `\| \| **sg** \| **pl** \|` | The singular header is abbreviated two ways in one class (`s`: 4_pres, 6_opt, 9_aor, 10_sum; `sg`: 5_imp, 7_perf, 8_imperf) (old F73) | One form | 9 |
| class_21/4_pres.md:18, 27 | `hanan**te**` / `hañña**nte**` | The ending is split differently; it is `-ante` / `-nte` (old F74) | One split | 9 |
| class_21/4_pres.md:13; class_21/5_imp.md:13 | `<br>√han + a \> hana**` / `<br>(√sikkh + a \> sikkha)**` | The derivation in the table captions is with or without brackets (without: 4_pres.md:13, 22; 9_aor.md:21, 30) (old F75) | One form | 8 |
| class_21/10_sum.md:29, 44 | `\| vattamānā \| ti \|` / `\| **vattamānā** \| te \|` | The Parassapada table has plain labels (lines 27–36), the Attanopada table bold ones (42–51) (old F76) | One form | 9 |
| class_21/5_imp.md:5; class_21/4_pres.md:5; class_21/9_aor.md:5 | `“When a command, a wish, an unspecified time, imperative”` / `“present tense when present-time”` / `“when recent, aorist.”` | Capitalisation of the sutta glosses; 9_aor.md has a full stop inside the quotes (old F77) | One form | 7 |
| class_21/2_voices.md:73 | `[DHP131](https://s.dhamma.gift/kn/dhp/index.html#dhp129)` | The reference is on its own line before the verse; elsewhere `([REF](url))` after the verse (4_pres.md:35) (old F78) | One form | 7 |
| class_22/1_fut.md:13; class_22/2_cond.md:15; class_21/4_pres.md:13 | `**Future Reflexive “will go by oneself”` / `**Conditional Active “[if] would be; could have been”**` / `**Present Tense Attanopada “kills by oneself”` | The caption terms change between classes 21 (`Parassapada` / `Attanopada`) and 22 (`Active` / `Reflexive`) (old F79) | One scheme | 8 |
| class_22/1_fut.md:3; class_22/2_cond.md:3 | `Kaccāyana 421. **anāgate bhavissantī.**` / `Kaccāyana 422. kriy’ātipanne’tīte kālātipatti.` | The sutta is bold in one file only (class 21: all plain) (old F80) | owner decision (Kaccāyana citation style) | 9 |
| class_22/2_cond.md:19, 28; class_22/1_fut.md:17 | `\| \| sg \| pl \|` / `\| \| **sg** \| **pl** \|` | Header bold drift (old F81) | Bold | 9 |
| class_22/2_cond.md:9; class_22/3_root_groups.md:146 | `hadn't` / `It's in the traditional grammar books, but it's actually` | Straight apostrophes (old F82) | `’` | 9 |
| class_22/4_irreg_base.md:29; class_23/13_nii.md:8 | `is dis-enchanted` / `is disenchanted` | Hyphen drift (old F83) | `disenchanted` | 9 |
| class_22/4_irreg_base.md:20 | `he himself does` | The only gloss with a pronoun (old F84) | `does (for oneself)` | 7 |
| class_21/3_pass_refl.md:15, 29 | `cittaṃ samādhiya**te** – the mind` / `Pāli - vucca**ti**` | En dash and hyphen as separators in one file (also 2_voices.md:85, 7_perf.md:47–51) | One dash | 8 |
| class_21/11_home_work.md:13, 14; class_22/5_home_work.md:13 | `(para 405 - 438)` / `(p83 - 101)` / `(para 354 - 404)` | Spaced hyphen in ranges; class 16 has `p6-12` | One style (`–`) | 7 |
| class_21/2_voices.md:23, 51 | `the way the active voice is constructed is:` / `the middle voice is constructed using` | Lower-case sentence starts (also 10_sum.md:3 `from Kaccāyana:`) | Capitals | 8 |
| class_21/2_voices.md:63; class_21/5_imp.md:9; class_22/2_cond.md:11 | `**reflexive pronoun.**` / `**passive voice.**` / `**active and reflexive** **voice.**` | Full stop inside the bold; split bold | Full stop outside; one span | 8 |
| class_23/1_prefix.md:9, 21 | `(root – meaning – following along)` / `(root – meaning - obstructing)` | En dash and hyphen mixed (also line 33) (old F85) | One dash | 9 |
| class_23/1_prefix.md:25 | `e.g. √raj 3 ya (desire)` | The notation differs from lines 13 and 37 (`√bhā (to shine)`) (old F86) | `√raj (to desire)` | 7 |
| class_23/20_mixed_pref.md:22 | `sam + pati` | `saṃ` in every other row (old F87) | `saṃ + pati` | 9 |
| class_23/21_nipata.md:34 | `**in full view, in sight, in view, manifestly, visibly.**` | The only meaning line with a full stop; in files 2–19 only the main meanings are bold, here every line is fully bold (old F88) | Align | 8 |
| class_23/22_dur_su_nir.md:51 | `## kā- kad- ku` | Hyphen missing on `ku` (old F89) | `ku-` | 9 |
| class_23/1_prefix.md:7, 19 | `**1. dhātv’atth’ānuvattaka**` / `**2. dhātv’atthabādhaka**` | Elision apostrophe before `ānuvattaka`, none before `bādhaka` / `visesaka` (correct as sandhi marks, but the three names look unlike) | Accept, or write all three without apostrophes | 5 |
| class_23/1_prefix.md:1; class_23/21_nipata.md:1; class_21/4_pres.md:1 | `# Prefixes (upasagga)` / `# Some Adverbs (nipāta) used as Prefixes` / `# Present Tense (*vattamānā*)` | The Pāli term in the H1 is plain in classes 18 and 23, italic in classes 16, 17, 19, 21, 22; `used as` in lower case | owner decision (see the p03 row on 7_mix_san.md:1) | 6 |
| class_23/8_abhi.md:9; class_23/2_aa.md:7 | `offers; presents` / `plucks out, uproots` | Synonyms are separated by `;` in some rows and `,` in others (all files 2–20) | One separator | 6 |
| class_23/15_pati.md:14; class_23/19_sam.md:11; class_23/22_dur_su_nir.md:14 | `practices` / `recognizes` / `discolored` | US spellings (UK elsewhere: class_18/2_as_ya.md:64 `analysing`) (old F91) | owner decision | 6 |
| class_23/3_ati.md:3; class_23/18_vi.md:3 | `**beyond**, across, **over**` / `apart, away, without, separately` | Files 2–19 bold the commonest meanings; 18_vi.md (and 7_api.md apart from one word) has no bold | Bold the main meanings of `vi-` | 6 |
| class_24/5_caus_pass.md:7 | `"it is caused to be done"` / `"he causes (it) to be done,"` | Straight double quotes; line 5 has curly ones (old F92) | `“…”` | 10 |
| class_24/5_caus_pass.md:39; class_25/4_taddh.md:19 | `app'eva` / `noun's` | Straight apostrophes (old F93) | `’` | 9 |
| class_24/5_caus_pass.md:39, 27 | `[MN50](https://s.dhamma.gift/mn/mn50/index.html)` / `([MN65](https://s.dhamma.gift/mn/mn65/index.html) bhaddālisuttaṃ)` | A reference without brackets and sutta name (lines 51 and 63 have both) (old F94) | One form | 9 |
| class_24/3_caus.md:3; class_24/2_irreg_pass.md:11, 64 | `Kacc 438, 540.` / `Kacc 502, 493` / `Kacc 487, 478.` | Abbreviated here, and with two numbers; classes 19–22 have `Kaccāyana 414.` (old F95) | owner decision (Kaccāyana citation style) | 8 |
| class_24/2_irreg_pass.md:19; class_24/1_pass.md:58 | `Commentary example` / `These bases mostly exist in participle forms.` | A third wording for "commentary example" (class 17: `(commentary example)`, `comm word`) (old F96) | One wording | 8 |
| class_24/1_pass.md:27; class_24/6_app.md:23, 40 | `## How to form Passive Verbs` / `## How To Construct Active Past Participle` / `## How to Decline Active Past Participle` | Heading case drift (`form`, `To`) (old F97) | One style | 8 |
| class_24/6_app.md:46, 48; class_18/10_irreg_masc.md:11, 13 | `\| nom \|` / `\| instr \|` / `\| 1.nom \|` / `\| 3.inst \|` | The case labels differ between the declension tables (old F98) | One set | 8 |
| class_24/6_app.md:54, 56 | `**In summary:** the forms that actually occur are almost always masculine nominative:` / `pattern.` | A hard-wrapped paragraph (lines 54–56), as in class_18/10_irreg_masc.md:106–110 (old F99) | One line | 7 |
| class_24/2_irreg_pass.md:85 | `pā**vu**raṇaṃ` | The only form with a case ending in the table (old F100) | `pāvuraṇa` | 8 |
| class_24/2_irreg_pass.md:5; class_24/4_irreg_caus.md:5 | `\| √jan \| to produce \|` / `\| √jan \| to be born \|` | Root gloss drift (old F101) | one gloss in both files (root meanings are not in the headword lookup: DPD lookup for the wording) | 7 |
| class_25/5_taddh_2.md:48, 54 | `ka**ccāyana**` / `k**accāna**` | The bold split differs (old F102) | One split | 8 |
| class_25/5_taddh_2.md:11, 181, 100, 146 | `from family of Gotama` / `son of ascetic` / `belonging to community` / `belonging to a sect` | Articles are dropped in most glosses and kept in some (old F103) | One style | 6 |
| class_25/2_nouns.md:3, 39 | `1.  **concrete nouns** describe` / `4.  **agent noun** is a person` | Plural and singular mixed; lower-case list items (also lines 15, 26) (old F104) | One form | 7 |
| class_24/1_pass.md:29, 31 | `1\. Root + ya \> Passive Base` / `2\. Root + iya \> Passive Base` | Escaped pseudo-list (also 3_caus.md:21, 31, 45); 7_home_work.md has a real list | One form | 7 |
| class_24/6_app.md:3 | `**Active Past Participle or app.**` | The bold covers `or` and the full stop | `**Active Past Participle** or **app**.` | 8 |
| class_24/6_app.md:38; class_25/5_taddh_2.md:79 | `has realized` / `traveler` | US spellings (see the p03 and p06 rows) | owner decision | 6 |
| class_24/6_app.md:60; class_24/5_caus_pass.md:51 | `[SN3.13](https://s.dhamma.gift/sn/sn3/index.html#sn3.13) doṇapākasuttaṃ` / `([AN3.36](https://s.dhamma.gift/an/an3/index.html#an3.36) devadūtasuttaṃ)` | The reference stands before the text and without brackets in 6_app.md | One form | 7 |
| class_25/5_taddh_2.md:234 | `## tā (multitude of, collection of) feminine nouns` | The only suffix heading with extra words after the bracket | `## tā (multitude of, collection of)` | 6 |
| class_26/3_state.md:38; class_26/4_ind.md:108; class_27/3_kita.md:9; class_26/3_state.md:7 | `**+ tha**` / `**+ to**` / `**+ nta**` / `+ tā` | The suffix column is bold in some tables only (3_state.md:38–41, 4_ind.md:108–132, all of 3_kita.md) (old F105) | One form | 9 |
| class_26/4_ind.md:138, 139, 145, 146 | `**kahaṃ**` / `**tahaṃ**` / `**kuhiṃ**` / `**tahiṃ**` | Whole word bold; elsewhere only the suffix (old F106) | `ka**haṃ**` etc. | 9 |
| class_26/1_having.md:41, 60, 117; class_26/3_state.md:61, 64 | `daṇḍa pāṇi` / `na cakkhu` / `nir āsā` / `bahu suta` / `dur manas` | The members are separated by a space; class 25 has `+` (`jambu + nadī`) (old F107) | `+` | 8 |
| class_26/1_having.md:3, 5; class_25/4_taddh.md:29 | `(atthyattha)` / `(atthyatthataddhita)` / `atthy’attha` | Apostrophe drift (old F108) | One form | 7 |
| class_27/2_kicca.md:130 | `kha**jjaṃ**` | The only form with a case ending (old F109) | `kha**jja**` | 9 |
| class_27/1_kitaka.md:3, 7 | `**Primary derivatives**` / `**Secondary Derivatives**` | Case drift; line 7 has no full stop (old F110) | One form | 8 |
| class_27/2_kicca.md:37, 117; class_27/3_kita.md:103; class_26/1_having.md:126 | `what do you notice about all these words?` / `please note the small spelling differences` / `please **review** all the **sandhi**` / `what do you notice about these words?` | Lower-case sentence starts (also 2_kicca.md:66, 149) (old F111) | Capitals | 8 |
| class_27/3_kita.md:24, 28, 95, 98, 100 | `saddah**āna**` / `āsas**āna**` / `vippaki**ṇṇa**` / `uppa**nna**` / `nis**inna**` | The prefixes in the result are not shown in the root column (also 2_kicca.md:72, 97, 154 `āhun**eyya**`, 156) (old F112) | Add the prefix | 7 |
| class_26/3_state.md:3; class_26/1_having.md:34 | `## tā (state of) abstract feminine nouns` / `### ī (having, possessing) agent nouns` | Headings with a word class after the bracket in classes 26 (all of 3_state.md, 4_ind.md) and 25 (one); the other suffix headings stop at the bracket | One pattern | 6 |
| class_26/4_ind.md:7, 8; class_26/2_numer.md:40 | `many 100’s of times` / `6 times` / `consisting of two` | Numbers as digits in 4_ind.md, as words in 2_numer.md | One style | 6 |
| class_27/2_kicca.md:21, 22 | `ka**ttabba**` / `k**ātabba**` | The bold starts at the changed consonant in one row and at the vowel in the next | One split | 7 |
| class_27/2_kicca.md:3; class_27/1_kitaka.md:3, 17 | `**potential participles.**` / `**root or base.**` / `**kitaka.**` | Full stop inside the bold | Full stop outside | 8 |
| class_28/1_kita_1.md:596, 597 | `+ **\*ana**` | The suffix cell elsewhere is `**+ suffix**`, with the plus sign inside the bold (lines 596–603; file 2: see p10) (old F113) | `**+ \*ana**` | 9 |
| class_28/1_kita_1.md:607 | `suffix \***ī**` | The asterisk is outside the bold; elsewhere `**\*a**`, `**\*ana**` (old F114) | `**\*ī**` | 9 |
| class_28/1_kita_1.md:36, 78 | `suffix **ta** is the most common kita suffix.` / `suffix **a** is used to form a large group` | File 1 gives each suffix a description sentence and a POS breakdown; file 2 gives only `total`, with a description for three suffixes only, and has no intro paragraph (old F119) | Accept as design, or level up | 6 |
| class_28/1_kita_1.md:36, 152, 296, 379 | `suffix **ta** is the most common kita suffix.` / `suffix **\*a** forms a large group` / `suffix **ana** is used to form` / `suffix **ti** is used mostly to form` | The section openers start lower-case; about half end without a full stop (152, 296, 379, 405, 449, 472, 512, 572, 607, 641); `kita` is not italic on line 36 but is on lines 5 and 28 (old F120) | Sentence case, full stops, italic | 8 |
| class_28/1_kita_1.md:249, 250, 268 | `great, large, big` / `big; huge; large` / `heaven; lit. satisfied` | The gloss separators mix `,` and `;` (file 2: see p10) (old F121) | Uniform | 6 |
| class_28/1_kita_1.md:50, 355; class_27/3_kita.md:59 | `bud**dha**` / `jiṇ**ṇa**` / `ka**ṭṭha**` | Class 28 bolds only the second half of an assimilated cluster throughout (suffix part); class 27 bolds the whole cluster (see the p08 row on 3_kita.md:64) | One convention for both classes | 6 |
| class_28/1_kita_1.md:616, 521 | `**+ \*ī agent nouns**` / `**+ ī masculine agent nouns**` | Caption without `masculine` in this one table | `**+ \*ī masculine agent nouns**` | 7 |
| class_28/1_kita_1.md:78, 337 | `**neuter nouns.**` | Full stop inside the bold | Full stop outside | 8 |
| class_28/2_kita_less.md:419, 452, 466, 508, 528 | `+ \*u` / `+ yā` / `+ \***tta**` / `+ \*ikā` / `+ **tī**` | The suffix cell elsewhere is `**+ suffix**`; four variants here (file 1: see p09) (old F113) | `**+ \*u**` etc. | 9 |
| class_28/2_kita_less.md:400, 448, 475, 524 | `**\*ā feminine nouns**` / `**yā feminine nouns**` / `**\*ta masc nouns**` / `**tī feminine nouns**` | The captions lack the leading `+ ` that all the others have; `masc` is abbreviated only here (old F115) | `**+ \*ā feminine nouns**` etc.; `masculine` | 9 |
| class_28/2_kita_less.md:419 | `\| √dar \| to split \| + \*u \| d**ā**r**u** \| m \| wood, timber \|` | The only table with a sixth (POS) column; it has `m` where the count tables have `masc` (old F116) | Split into two five-column tables, or `masc` | 8 |
| class_28/2_kita_less.md:7, 170 | `\| **total** \| 95 \|` / `suffix **ikā** is used to form feminine nouns and feminine agent nouns` | File 2 gives only `total` per suffix and a description for three suffixes only; no intro paragraph (file 1: see p09) (old F119) | Accept as design, or level up | 6 |
| class_28/2_kita_less.md:177, 281 | `fly (smearer)` / `bank; shore` | A literal meaning in brackets (elsewhere `; lit. …`); `;` beside `,` as gloss separator (file 1: see p09) (old F121) | Uniform | 6 |
| class_28/2_kita_less.md:496; class_24/6_app.md:38 | `has realised` / `has realized` | The same gloss of `abhisametāvī` in UK and US spelling (also line 130 `memorizer`) | owner decision | 7 |
| class_28/2_kita_less.md:1; class_28/1_kita_1.md:1 | `# Less Frequent *kita*` / `# More Primary Derivatives` | Italic Pāli term in this H1 only (mech-output: the index link has no italics) | Accept, or `# Less Frequent Kita` | 6 |
| class_28/3_home_work.md:15; class_16/13_home_work.md:9 | `## How to progress with Pāli from here` / `## How to do the Homeless work` | Sentence-case headings beside `## Extra Reading` | Title Case | 6 |
| class_16/3_vowel_1.md:27; class_21/4_pres.md:3; class_24/3_caus.md:3 | `In Kaccāyana this is called (12) **sarā sare lopaṃ**` / `Kaccāyana 414. vattamānā paccuppanne.` / `Kacc 438, 540.` | Kaccāyana is cited three ways across the course: `In Kaccāyana this is called (n)` 23 times (classes 16–17), `Kaccāyana n.` 13 times (classes 19–22, in italic, bold and plain variants), `Kacc n, n.` 3 times (class 24). Classes 18, 23, 25–28 cite no sutta | owner decision (Kaccāyana citation style) | 8 |
| class_24/3_caus.md:53; class_18/1_phonetic.md:47 | `\| abs \| **bhāve**tvā \| having developed \|` / `(ger. descending)` | The `-tvā` / `-ya` form has two names across the course: `ger.` 11 times (class 18: 10, class 17: 1) and `gerund` 4 times; `abs.` twice (classes 17, 18), `abs` once (class 24), `absolutive` once (class 18) | owner decision (one term) | 8 |
| class_17/3_cons_1.md:21; class_24/2_irreg_pass.md:81; class_28/1_kita_1.md:43 | `masc. impurity` / `\| f \| **vu**ddhi \|` / `\| **masc** \| 92 \|` | Gender labels across the course: `masc.` 16 and `m.` 11, `fem.` 8 and `f.` 13 (class 17), bare `m` / `f` / `nt` (class 24), `masc` / `fem` / `nt` (class 28), `m.n.s` (class 16 homework) | One set of abbreviations | 7 |
| class_20/2_bahub.md:135; class_25/5_taddh_2.md:79; class_27/3_kita.md:78; class_17/8_nig_1.md:35 | `(a traveller)` / `traveler` / `trained, practised` / `often practiced in this way` | UK and US spellings side by side. US: `practiced` (2), `practices` (verb), `recognize(s)` (5), `analyze`, `discolored`, `traveler`, `realized`, `memorizer`. UK: `practised` (4), `recognise`, `analysing`, `traveller` (2), `realised`, `criticises`, `organised`, `honour`, `flavour`, `skilful` | owner decision (UK or US) | 8 |
| class_21/10_sum.md:44; class_17/15_nig_8.md:18 | `ante<br>re` / `ariya-<br>saccāna**ṃ**` | `<br>` occurs 136 times in classes 17, 18, 20, 21, 22 and 24 (mech_checks), against the "no raw HTML in sources" rule; `{: .align-right }` 4 times in class_20/5_ex.md | owner decision (`<br>` and `{: }` in sources) | 7 |
| class_16/8_vowel_6.md:62; class_21/7_perf.md:11; class_25/3_anub.md:17 | `this (...) of yours` / `“The ancient sages said...”` / `Except when ...` | Three full stops (7 times: classes 16, 20, 21, 25) beside the ellipsis character `…` (13 times: classes 20, 21, 24) | `…` | 8 |
| class_16/1_sandhi.md:13; class_21/2_voices.md:85; class_25/3_anub.md:15 | `**euphonic combination** — sounds merging` / `reflexive meaning - sometimes` / `Please note - when` | Sentence dashes are `—` in classes 16–18 (60 with the index titles), ` - ` in 37 places (classes 16–25) and `–` in 27 (classes 20, 21, 23) | One dash for each use | 7 |
| index.md:69; class_21/4_pres.md:1 | `- [Present Tense (vattamānā)](class_21/4_pres.md)` / `# Present Tense (*vattamānā*)` | mech_checks lists 24 index links whose text differs from the page H1. Three H1s have real markup defects (rows on class_16/2_vowel.md:1, class_17/2_cons.md:1, class_19/1_comp.md:1); in the other 9 pages (classes 21, 22, 28; root and class index each) the index only drops the italics | Accept, or add the italics to the link text | 5 |
| class_23/23_home_work.md:24; class_24/7_home_work.md:19; class_16/13_home_work.md:40 | `Verbal Prefixes 514 - 522 (p118-122)` / `Passive Voice (481-490)<br>Causative Verbs (491-497)` / `Vowel Sandhi p6-12` | The Extra Reading tables give references seven ways (page, paragraph, chapter; `p6-12`, `p12 - 14`, `(para 405 - 438)`, `(481-490)`, `Chapter 12`); the Perniola and Māgadhabhāsā rows stop after classes 22 and 18 | One reference style; state page or paragraph | 6 |

## G. Links

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_28/3_home_work.md:17 | `[**Advanced Pāli**](https://sasanarakkha.github.io/study-tools/pali-class/pali-class-adv.html)` | The link returns HTTP 404 (links-status.tsv, 2026-11-13) | Replace with the current address of the page | 10 |

## H. Data to re-verify (forms, references, counts)

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_16/7_vowel_5.md:42, 43 | `s**a** \| **√ī**r + ī \| s**e**rī` / `(with) \| to move \| independent; free` | `sa` in `serī` is "own, self", not "with" (old H3) | DPD lookup (DPD gives `sa + √īr + a + ī` "independent; free; autonomous" and does not gloss `sa`) | 5 |
| class_16/11_vowel_9.md:23 | `*sara-sandhi-niṭṭhitaṃ*` | `sandhi` is masculine; expect `niṭṭhito`, or two words (old H5) | verify | 5 |
| class_16/12_vowel_ref_table.md:65 | `yena midhekacco =` | A space inside a sandhi exercise item (old H6) | verify the intended form (`yenamidhekacco`) | 5 |
| class_16/3_vowel_1.md:178; class_16/9_vowel_7.md:47 | `n**u** \| **a**jja \| n**a**jja` / `n**u** \| **a**jja \| n**va**jja` | The same pair gives two results; `najja` is confirmed by DPD, `nvajja` is not | `najja` is a DPD sandhi headword (`nu + ajja`); `nvajja` is not in DPD: DPD lookup, or replace the example on 9_vowel_7.md:47 | 6 |
| class_16/7_vowel_5.md:35, 36 | `aññass**a** \| **i**va \| aññass**e**va` / `of another \| like \| like of another (person)` | `aññasseva` is normally `aññassa + eva`; a reading with `iva` needs its source | verify | 5 |
| class_16/8_vowel_6.md:25 | `pamutt**i** \| **a**tthi \| pamut**ya**tthi` | `tt` becomes `t` in the result without comment | verify the form; add a note on `tt > t` | 5 |
| class_16/10_vowel_8.md:67, 68 | `vutta atth**ā** \| **e**va \| vutt’atthā**n**eva` / `said meaning \| just \| the meanings have already been stated` | Looks like a commentarial phrase (`vuttatthāneva`, "already explained"), where `-āni + eva` and not an inserted `n` is likely | verify | 5 |
| class_16/13_home_work.md:15, 24 | `**nāhaṃ** bhabbo etarahi kāmāni paṭisevituṃ.` / `kāmāni \| n \| nt.ac.pl \| sensual pleasures` | The quoted wording was not checked against AN 5.57 (the link check proves only the anchor); `kāma` is masculine, so `nt.ac.pl` needs checking | verify the quotation against AN 5.57; DPD lists `kāma` as masc only: DPD lookup (inflection table) for `kāmāni` before changing the tag | 5 |
| class_16/8_vowel_6.md:58, 60 | `your \| I \| I your` / `my \| I \| I my` | `te` / `me` are glossed as genitives; in `tyāhaṃ`, `myāhaṃ` they may be dative or instrumental, depending on the source sentence | verify | 4 |
| class_17/5_cons_3.md:17 | `[DN16.14]` | The verse `anūpavādo anūpaghāto` is in DN 14 (and Dhp 185); the link goes to DN 16 (old H7) | verify; likely `DN14` with the DN 14 link | 8 |
| class_17/8_nig_1.md:11; class_17/17_nig_10.md:9 | `**niggahitaṃ**` / `**niggahitañ’ca.**` | Short `i` against `niggahīta` in the class title and prose. The Kaccāyana text itself may read `niggahitaṃ` (suttas 30, 37), so this may be a faithful quotation (old A10) | verify against a Kaccāyana edition (DPD has both `niggahita` and `niggahīta` as headwords for the letter ṃ, so the quotation may stand) | 4 |
| class_17/5_cons_3.md:27 | `nāsiṃsat**ī** lokamimaṃ parañ’cā’ti.` | Editions read `nāsīsati` / `nāsīsatī`; `nāsiṃsatī` not checked against AN 4.45 | verify the reading (`āsiṃsati` is a DPD headword, so the form itself is sound) | 4 |
| class_17/10_nig_3.md:9 | `in Rūpasiddhi under (49)` | The Rūpasiddhi number was not checked | verify | 4 |
| class_17/15_nig_8.md:19, 20 | `pares**a** pāva \| tells to others` / `vanasm**i** vānaro \| monkey in the forest` | Sources not identified; `pāva` is a perfect, glossed as a present | `told to others` (DPD: `pāva` is perf of `vadati`, "spoke (about); told (of)"); verify the sources | 6 |
| class_18/10_irreg_masc.md:63 | `vay**o**anuppatto` | Usually two words, `vayo anuppatto`, so not a compound in `-o` (old H17) | verify; replace with a compound | 6 |
| class_18/10_irreg_masc.md:91 | `similarly: asma, puma, bhasma, muddha, yuva, sakha etc.` | These nouns share some `-an` forms with `atta` but have their own irregular forms (`sakhā`, `pumā`, `yuvā`); "similarly" overstates it | verify; reword to "partly similar" | 5 |
| class_19/2_kamm.md:81 | `(see *APA* for a lot of examples)` | `APA` is not explained anywhere in the class (old H20) | Expand the abbreviation | 6 |
| class_20/5_ex.md:7 | `[AN3.80](https://s.dhamma.gift/an/an3/index.html#an3.79)` | Label and anchor disagree (old H22) | verify which sutta has the sentence | 8 |
| class_20/1_abya.md:68 | `\| paccūsa \| early \|` | A noun (dawn) in a list of prefixes and indeclinables (old H27) | mark it as a noun, or take it out of the list (DPD: `paccūsa` masc, "before dawn; early morning") | 6 |
| class_20/2_bahub.md:151 | `sapattabhāro – (a bird) carrying its own wings` | Listed under `sa- (with)` but glossed "own" (old H28) | move to `saka > sa` (DPD: `sa + patta + bhāra`, "carrying only one's wings"); DPD does not gloss `sa` itself: DPD lookup | 6 |
| class_20/4_change_comp.md:12, 13, 20, 21 | `jayampatikā` / `jānipatī` / `samātar \| own mother` / `sayasaṃvuta \| enclosed in one’s own opinion` | Forms and glosses to be confirmed | `jānipatī` is not a DPD headword: DPD lookup; the other three are confirmed by DPD | 5 |
| class_20/5_ex.md:12 | `[AN2.40]` | Not checked that the quoted sentence is in AN 2.40 (the link check proves only the anchor) | verify | 4 |
| class_21/9_aor.md:43 | `bhagavantaṃ gāthāya **ajjhabhāsatha** ([SN1.1](https://s.dhamma.gift/sn/sn1/index.html#sn1.1) etc.)` | The SN prose has `ajjhabhāsi`; `ajjhabhāsatha` is not confirmed at SN 1.1 (old H23) | verify the source | 7 |
| class_21/10_sum.md:5, 19 | `423, 426.` / `430, 373.` | The first numbers are Kaccāyana 423–430; the second numbers are not explained (another grammar?), `426` repeats (line 11) and `373` is out of sequence (old H24) | verify the numbers; name the second source | 7 |
| class_21/8_imperf.md:11 | `about **38** Tipiṭaka examples so far` | The count dates quickly (old H26) | Re-count in DPD, or drop the number | 5 |
| class_23/22_dur_su_nir.md:62, 63 | `\| ku \| √sad + ya \| kosajja \|` / `\| ku \| √kar + ya \| kukkucca \|` | `kukkucca` lacks the `ta` step that DPD shows; `kosajja` is as in DPD (old H35) | `\| ku \| √kar + ta + ya \| kukkucca \|` (DPD: `ku + √kar + ta + ya` / `kukkata + ya`); `kosajja` agrees with DPD (`ku > ko + √sad + *ya`) | 7 |
| class_23/22_dur_su_nir.md:3 | `**dur-** **su- nir-** as well as **sa- kā- kad- ku-** are not used with verbs` | `dur` and `su` are in the list of 20 upasagga (1_prefix.md:51); for `nir` the statement agrees with DPD (verbs take `nī`); split bold (old H36) | verify the statement | 6 |
| class_24/1_pass.md:79 | `\| pp \| vi**mucc**ita \| freed \|` | The usual pp is `vimutta` (old H37) | `vi**mutt**a` (DPD: pp of `vimuccati`; `vimuccita` is not in DPD) | 7 |
| class_25/3_anub.md:21 | `there is an aspirate consonant, e.g. ka**th**ā + \*ika \> ka**th**ika` | The rule is doubtful (`ratha > rathika` fits; `magadha > māgadha` has `dh` later in the word and still lengthens) (old H42) | verify the rule | 5 |
| class_25/5_taddh_2.md:94 | `v**e**nay**ika** \| vinaya student` | In the suttas `venayika` is "one who leads astray" (old H43) | `expert in Vinaya` (DPD sense 6); the other DPD senses are "annihilationist", "destroyer of tradition", "who should be taught a lesson" | 6 |
| class_24/6_app.md:62 | `doṇapākaṃ sudaṃ bhuñjati.` | Editions differ here (`doṇapākakuraṃ bhuñjati`); not checked against SN 3.13 | verify | 4 |
| class_27/2_kicca.md:68, 76, 85, 93, 101, 110 | `## \*anīya (ptp) \~17` / `## anīya (ptp) \~73` / `## \*aniya (ptp) \~3` / `## aniya (ptp) \~25` / `## aṇīya (ptp) \~28` / `## aṇiya (ptp) \~2` | Unexplained numbers in the headings (frequency counts?) (old H45) | Explain or remove | 7 |
| class_28/1_kita_1.md:3, 5 | `more than 150 suffixes of primary derivatives that are used to form more than 14000` / `The **first 18** account for **83%**` | The top-18 counts add up to 12 280, which is 83% of about 14 800, consistent with "more than 14000". All DPD-derived counts are a snapshot and were not recomputed (old H53) | Recompute from the current DPD database | 6 |
| class_28/1_kita_1.md:30 | `**ta a \*a nta ita ana māna na ti aṇa ā aka ī anā \*ana \*ī i \*aka tar u ya ma itar ra ikā \*i iya \*aṇa tha āna as \*anā ū ika ala tta \*ā \*u ara yā \*tta \*ta tāvī \*ikā tī**` | The bold marks the 45 suffixes covered in the two files (18 + 27); it matches the headings and their order. The meaning of the bold, and of `\*`, is not stated in this class (old H55) | Add one line of explanation, or point to class_25/3_anub.md | 7 |
| class_28/3_home_work.md:13 | `\| Duroiselle \| Primary Derivatives (574-578) \|` | The paragraph range is not confirmed against Duroiselle (the same range is given in class_27/4_home_work.md:14) (old H54) | verify | 5 |
| class_16/10_vowel_8.md:15; class_19/5_dvanda.md:5 | `(35) **ya va ma da na ta ra lā c’āgamā**` / `Kaccāyana 329. nāmānaṃ samuccayo dvando.` | All Kaccāyana numbers and wordings in the course (12–22, 25–35, 37–40, 319, 324–329, 414–419, 421–430, 438, 487, 502) agree with the reader's memory except `asarūpo` (p01) and possibly `niggahitaṃ` (p02); none was checked against an edition | verify against a Kaccāyana edition | 6 |

## I. Further details on the material under review

| Location | Current | Problem | Suggested | Conf. |
| --- | --- | --- | --- | --- |
| class_16/13_home_work.md:1, 9 | `# Homeless work` / `## How to do the Homeless work` | The title of all 13 homework pages (27 occurrences with the indexes) is a pun on "homework"; treated as intended | owner decision | 5 |
| class_16/12_vowel_ref_table.md:99, 103 | `Also note the use of the **ṁ**, **ṃ** or **ŋ.**` / `yaṁ taṁ santaṁ padaṁ abhisamecca` | The 5 `ṁ` that mech_checks counts in class 16 are here and are deliberate (they illustrate the chanting-book spelling) | None | 9 |
| class_17/8_nig_1.md:48 | `Why make a rule if it remains unchanged?` | A question with no answer in the file; presumably answered in class | Add one sentence, or leave for the teacher | 5 |
| class_17/5_cons_3.md:41; class_16/9_vowel_7.md:25 | `disā anudisā sv**a**haṃ` / `s**va**haṃ` | Class 17 gives `svahaṃ` as a metrical shortening (SN 4.23); class 16 gives it as a plain `o + a > va` example. See the p01 row on 9_vowel_7.md:25 | Mark the class 16 example as metrical, or replace it | 7 |
| class_17/6_cons_4.md:11, 45 | `**esa** **m**aggo visuddhiyā.` / `**esa m**aggo visuddhiyā.` | The same pāda is quoted twice (as Dhp 277 and Dhp 278); both labels are right | None, or drop one | 6 |
| class_18/7_mix_san.md:30, 32 | `paccabhāsi \| pati + a + √bhās + i` / `paccaññāsi \| pati + a + √ñā + si` | `pati` (not `paṭi`) is right here, since `pacc-` comes from `pati`; no finding, noted so that the `pati`/`paṭi` rows are not over-applied | None | 8 |
| class_20/1_abya.md:84 | `What makes a compound an abyayībhāva?` | The file ends with a question that has no answer (as class_17/8_nig_1.md:48) | Add one sentence, or leave for the teacher | 5 |
| class_19/2_kamm.md:5 | `(object / bearer)` | Presumably the literal meaning of `kamma-dhāraya`; it stands alone with no explanation | Add `lit.` and the Pāli parts | 5 |
| class_22/3_root_groups.md:141, 142 | `\| √tas \| ṇhā \| (taṇhā) \| (taṇhāti) \| thirsts \|` / `\| √us \| ṇhā \| (uṇhā) \| (uṇhāti) \| heats \|` | The brackets (presumably "theoretical, not found as verbs") are not explained | Add a note under the table | 6 |
| class_22/3_root_groups.md:121 | `As you can see, these are quite rare.` | Rare as a group (four roots), though `suṇāti` and `pāpuṇāti` are among the most common verbs; the sentence can mislead | `There are few roots in this group, but some are very common.` | 5 |
| class_23/22_dur_su_nir.md:43 | `\| √van \| to desire \| nibbana \| without craving \|` | Short `nibbana` (adjective) is easily read as a typo for `nibbāna` | form confirmed by DPD (`nibbana` adj, `nir + √van + a`); add `(adj.)` so that it is not read as a typo for `nibbāna` | 5 |
| class_23/13_nii.md:16; class_23/20_mixed_pref.md:10; class_23/22_dur_su_nir.md:14 | `\| √yā \| to go \| nīyati \| departs, leaves \|` / `\| anu + pa \| √ikkh \| to look \| anupekkhati \| inspects \|` / `\| √var \| to cover \| dubbaṇṇa \|` | The old audit called these three wrong; DPD supports the text in all three (Phase 0), so they are dropped | None | 9 |
| class_24/2_irreg_pass.md:11; class_21/10_sum.md:5 | `Kacc 502, 493` / `423, 426.` | The double numbers look like Kaccāyana + Rūpasiddhi numbers (class_17/10_nig_3.md:9 names Rūpasiddhi once). If so, the p05 row on 10_sum.md is only a labelling problem | Name the second source once | 5 |
| class_25/5_taddh_2.md:13; class_20/4_change_comp.md:15 | `\| jambu + nadī \| + \*a \| jamb**o**nad**a** \|` / `\| nadī \| river \| nada \| jambonada \|` | `jambonada` is explained as a taddhita in class 25 and as a change of `nadī` in compounds in class 20; both can stand, but neither refers to the other | Cross-reference | 5 |
| class_24/4_irreg_caus.md:22; class_25/5_taddh_2.md:62 | `\| √nas \| to be lost \| \*e \| nessa \| nessati \| will destroy \|` / `\| apihā \| + ālu \| apih**ālu** \| not full of envy \|` | The old audit called these two wrong; DPD supports the text (Phase 0), so they are dropped | None | 9 |
| class_26/1_having.md:95; class_27/2_kicca.md:108 | `\| sati \| + mant \| satī**mant** \| mindful \|` / `\| √raj \| + aṇīya \| sār**aṇīya** \| to be desired \|` | The old audit called these two wrong; DPD supports the text (Phase 0), so they are dropped | None | 9 |
| class_27/3_kita.md:90; class_18/4_as_na.md:20 | `c**i**ṇ**ṇa** \| done, practised` / `ci**ṇṇ**a \| pp. completed` | Class 27 has the gloss that the p03 row suggests for class 18 | Use `practised` in both | 7 |
| class_28/1_kita_1.md:658; class_16/1_sandhi.md:3 | `\| saṃ √dhā \| to place \| **+ i** \| sandh**i** \| sandhi; conjunction \|` / `saṃ + √dhā + i \> sandhi` | The two places agree; noted as a consistency check that passed | None | 9 |
| class_28/3_home_work.md:21 | `[feedback form](https://docs.google.com/forms/d/e/1FAIpQLSeCZ01pgGSYZDO7c1p7L5ciQfg1gEPIEx1g0RgPaCxSY_fQcg/viewform)` | Google Forms link: not checked by script (skipped in links-status.tsv) | Open it once by hand | 5 |
| class_17/5_cons_3.md:23; class_20/2_bahub.md:77; class_21/2_voices.md:73 | `([SNP43](https://s.dhamma.gift/kn/snp/index.html#snp4.5))` / `([TH261](https://s.dhamma.gift/kn/thag/index.html#thag18.1))` / `[DHP131](https://s.dhamma.gift/kn/dhp/index.html#dhp129)` | The labels use running numbers (`SNP43`, `TH261`, verse `DHP131`) and the anchors chapter numbers; this follows the link rules in `kamma/tech.md` and all 37 links pass `check_sutta_links.py`. A reader cannot tell from `SNP43` that Snp 4.5 is meant | None, or labels like `Snp 4.5` | 5 |
| index.md:135; class_28/index.md:5 | `- [Less Frequent kita](class_28/2_kita_less.md)` / `- [Homeless work](3_home_work.md)` | The root index leaves out the homework page of all 13 classes, so that is by design; the one page missing by mistake is `class_21/1_review_verbs.md` (p01) | None for the homework pages | 7 |
| class_16/12_vowel_ref_table.md:6 | `a\<i` | mech_checks reports "RAW HTML" on lines 6, 7, 10, 13, 14 of this file; these are escaped `\<` arrows, not HTML (false positive) | None | 9 |
| class_16/7_vowel_5.md:67; class_17/1_alphabet_analys.md:51 | `udak**o**mi[^1]` / `Nasals[^3]<br>(*nāsika*)` | Footnote ids run across the whole course (1–23, 23 references and 23 definitions, checked with `--folder-footnotes`), so a file that starts at `[^3]` is by design | None | 9 |

## Mechanical detail

Counts from `mech_checks.py docs/ipc --folder-footnotes`, the link checks and the DPD run. Items that are also rows in the tables above are marked.

### M1. Tables

- 3 694 table rows. 2 column mismatches: `class_18/11_ex.md:11` and `:24` (1 cell where the table has 4). Rows above.

### M2. Index link text vs page H1

24 differences, 12 pages, each reported twice (from the class index and from `index.md`):

- Three H1s have a markup defect in the italics (rows above): `class_16/2_vowel.md` (`*(sara-sandhi)*`), `class_17/2_cons.md` (`(*vyañjana-sandhi)*`), `class_19/1_comp.md` (`(*samāsa)*`).
- In the other 9 pages the index link only leaves out the italics of the Pāli term: `class_21/4_pres.md`, `5_imp.md`, `6_opt.md`, `7_perf.md`, `8_imperf.md`, `9_aor.md`; `class_22/1_fut.md`, `2_cond.md`; `class_28/2_kita_less.md`. One F row covers them.

### M3. Footnotes

- 23 references, 23 definitions, numbered across the whole folder (ids 1–23). No reference without a definition and no definition without a reference. A file that starts at `[^3]` is therefore by design.

### M4. Stray characters, headings, whitespace

- "RAW HTML" is reported on lines 6, 7, 10, 13 and 14 of `class_16/12_vowel_ref_table.md`. These are escaped `\<` and `\>` arrows, not HTML: false positives (row in I).
- No final newline: `class_20/5_ex.md` (row in E).
- Lines with a double space: 165.
- No tab, NBSP, zero-width, Cyrillic or non-NFC character, no heading-level defect and no odd `**` count was reported.

### M5. Links

- 44 external link occurrences, 39 unique. 37 are on `s.dhamma.gift` (23 pages); all pass `check_sutta_links.py`.
- `https://sasanarakkha.github.io/study-tools/pali-class/pali-class-adv.html` (`class_28/3_home_work.md:17`) returns 404. Row in G.
- The Google Form link in `class_28/3_home_work.md:21` was skipped.

### M6. DPD run

- 436 lemmas looked up in one run; output in 837 lines.
- 18 are not DPD headwords: `ajjaṇhe`, `ajjhabhāsatha`, `antaṭṭha`, `āpo`, `bhuvādigaṇa`, `daṇḍapāṇi`, `duppativijjha`, `iddhika`, `jānipati`, `kāmāni`, `koti`, `mātāpitu`, `nvajja`, `samādhīyati`, `sañchavi`, `thāma`, `tiṭṭhāti`, `vimuccita`. Most are inflected forms or the variant that was being compared with a headword; those that are course spellings (`bhuvādigaṇa`, `duppativijjha`, `koti`, `tiṭṭhāti`, `vimuccita`, `nvajja`, `jānipatī`, `antaṭṭha`) have rows.

### M7. Convention counts

| Item | Total | Where |
| --- | --- | --- |
| `ṁ` | 6 | class 16 (5), class 20 (1) |
| straight `'` | 11 | classes 17–20, 22, 24, 25 |
| curly `’` | 100 | classes 16–26 |
| straight `"` | 4 | class 24 |
| curly `“”` | 195 | all classes and the index |
| `<br>` | 136 | classes 17 (27), 18 (54), 20 (1), 21 (22), 22 (5), 24 (27) |
| `{:` | 4 | class 20 |
| `...` / `…` | 7 / 13 | `...` classes 16, 20, 21, 25; `…` classes 20, 21, 24 |
| ` - ` / `–` / `—` | 37 / 27 / 60 | ` - ` classes 16–23, 25; `–` classes 20, 21, 23; `—` classes 16–18 and the index |
| `Pāli` / `Pāḷi` | 53 / 1 | `Pāḷi` once, class 18 |
| `\>` | 525 | classes 16–27; no `→` |
| `lit.` / `lit:` | 39 / 0 | |

The Kaccāyana citation styles, the `ger.` / `abs.` terms, the gender abbreviations and the UK / US spellings are counted in the F rows of the cross slice.

### M8. Conventions of class 28 (carried from the old audit)

- Five-column tables with an empty header row: root, root gloss, `**+ suffix**`, result, gloss. Prefixes stand before the root without `+` (`pati ud √pad`).
- Strengthening suffixes carry an escaped asterisk (`\*a`, `\*ana`, `\*ī`); the asterisk is not explained in this class.
- In the result the suffix and any changed root vowel are bold (`bh**e**d**a**`).
- No Kaccāyana citations, sutta links or footnotes in class 28.
