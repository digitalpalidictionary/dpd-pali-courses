# Course audit guide

Rules for auditing a course folder under `docs/` (e.g. `docs/ipc/`, `docs/bpc/`). Written after the IPC audit (2026-11-10 to 2026-11-12), from what worked and what failed there.

## Scope and ground rules

- The audit is read-only. Never edit `docs/`. The output is a findings list.
- One output file per course: `kamma/draft/audit/<course>-audit.md`. Use `bpc-audit.md` and `ipc-audit.md` as templates.
- Exercises and keys (`*_ex`, `*_key`) are separate audits.
- No commits, no pushes.

## Process

1. **Mechanical checks first, by script, over the whole folder.** They are cheap and need no reading:
   - sutta links: `uv run python scripts/check_sutta_links.py docs/<course>`
   - other external links (HTTP status)
   - local links and `#anchors`
   - index link text vs page H1, and every page listed in an index
   - table column counts
   - footnote references vs definitions (ids are numbered across the whole course, not per file)
   - counts for conventions: arrows, straight vs curly quotes, `ṁ` vs `ṃ`, `Pāli` vs `Pāḷi`, raw HTML (`<br>`), `{: … }` attribute markup
2. **Line-by-line read, one slice at a time.** A slice is one or two classes, about 500–1 000 lines. Print the files with line numbers and blank lines dropped (`grep -n "" file | grep -v "^[0-9]*:$"`).
3. **Save after every slice.** Write that slice's findings to its own file in `kamma/draft/audit/scratch/` before reading the next slice.
4. **Verify the excerpts by script** once all slices are in: every backtick excerpt in `Current` must be found in the cited file within 2 lines of the cited line. Fix the rows that fail.
5. **Merge by script** into the final file: group by category, keep class order, compute the summary table. Do not merge by hand.
6. **Delete `scratch/`** only after the final file is generated and checked.

## Limits and safety (learned the hard way)

- Do not run many subagents in parallel. Six strong-model readers at once drained the usage limit and five died with their output lost.
- The main session can read a whole course itself: 12 classes (about 7 000 lines) fitted in one session, slice by slice.
- If a subagent is used: one at a time, a cheaper model, and it returns findings as text. The main session saves them. Subagents cannot be relied on to write files.
- The session scratchpad and agent transcripts do not survive a limit or a resume. Anything worth keeping goes into `kamma/draft/audit/` immediately.
- Keep a short state note (done / not done) in the draft folder and update it after each slice, so a restart knows where to resume.
- When a limit warning appears: stop, save, update the state note.

## Row format

Slice files (working format):

`| Cat | Location | Current | Problem | Suggested | Conf. |`

Final file: one table per category, `| Location | Current | Problem | Suggested | Conf. |`.

- **Location:** path relative to the course folder plus line number(s), e.g. `class_17/5_cons_3.md:15`. For a second file in the same row, give its line number too, otherwise the excerpt check cannot confirm it.
- **Current:** verbatim from the source, in backticks, so it can be grep-checked. Never paraphrase inside backticks. Use `…` to skip text. A table pipe is written `¦` in slice files and converted to `\|` by the merge.
- **Suggested:** the fix, or `DPD lookup` / `verify` / `owner decision` when the fix is not known.
- **Conf.:** 1–10. Below 8 means "check before changing".

## Categories

| Cat | What goes in |
| --- | --- |
| A | Pāli and grammar content errors: wrong form, wrong root, wrong rule, misspelt term |
| B | Tables, paradigms and lists that disagree with each other or with themselves |
| C | Translation and gloss problems |
| D | English typos and grammar |
| E | Markdown defects that change rendering: misplaced `*`, split or misplaced bold, header rows, list numbering |
| F | Convention drift: same thing written two ways |
| G | Links |
| H | Data to re-verify: doubtful forms, sutta references, sutta numbers, counts |

## What to look for (patterns that recurred in IPC)

Content:
- Glosses swapped between columns, or one word glossed differently in different classes (`āsava`, `hirottappa`, `buddha`).
- The same root spelt two ways (`√khan`/`√khaṇ`, `√dhu`/`√dhū`) or a prefix inside the root sign (`√ādā`).
- `pati` in the analysis column, `paṭi` in the result.
- An example that does not illustrate its own heading or rule.
- Summary or reference tables that do not match the lesson tables they summarise.
- Paradigm cells: masculine vs neuter columns listing different sets, same forms in different order, missing rows.
- Quoted verses: check spelling against the known text, and that the reference label matches the link anchor.
- Statements with numbers ("three types", "9 kinds", "20 prefixes"): count the items that follow.

Format:
- Italic or bold closing on the wrong side of a bracket: `(*term)*`.
- Bold that cuts a consonant cluster (`phuṭ**ṭha**`), covers a neighbouring letter, or spans a `<br>`, a quote mark or a full stop.
- A table whose first data row is the header row; header labels not above their columns.
- Numbered lists: `1.` after a blank line continues the previous list; `1,1,1,2,3` renders flat.
- Straight apostrophes and quotes among curly ones; `ṁ` among `ṃ`; `-` vs `–`; `...` vs `…`.
- Abbreviation drift: `m.`/`masc.`, `s`/`sg`, `ger.`/`abs.`, `inst`/`instr`.
- Heading drift: case, hyphens, the same level used for different things, a page whose H1 is its first sub-item.
- Lower-case sentence starts and missing full stops in prose lines.
- Hard-wrapped paragraphs.

## What the audit must state it did not do

- Pāli forms judged from knowledge, not from the DPD database, unless lookups were actually run.
- Kaccāyana numbers and wording, if checked from memory.
- Link checks prove the URL exists, not that the quotation is in that sutta.
- Frequency counts not recomputed.
- Rendered site / PDF / DOCX not built.
- Which findings came from a subagent and were not re-judged.

## Recurring owner decisions (do not decide these in the audit)

- `# Homeless work` as the home-work page title.
- `<br>` in table cells and `{: .align-right }` versus the "no raw HTML in sources" rule.
- `Pāli` or `Pāḷi` in running text.
- gerund or absolutive.
- Kaccāyana citation style.
- UK or US spelling.

## Scripts used for IPC

Three one-off scripts are kept in `kamma/draft/audit/scripts/`. They have IPC paths and the `scratch/` slice layout hardcoded, so adjust them for another course:

- `ipc-audit-mech.py`: the mechanical checks in step 1.
- `verify_rows.py`: step 4. Parses the rows, pulls backtick excerpts from `Current`, splits them on `…`, normalises spaces around pipes, and searches the cited file near the cited lines. Reports `NOT FOUND` and `WRONG LINE`.
- `merge_audit.py`: step 5. Reads the slice files, groups rows by category, builds the summary table (count per category per slice, and count with confidence ≥ 8), and writes the final file around a hand-written head (method and limits) and mid (confidence, owner decisions).
