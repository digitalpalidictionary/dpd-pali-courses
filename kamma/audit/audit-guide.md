# Material audit guide

Rules for auditing a folder of source material: usually a folder under `docs/`, sometimes a data file (e.g. a TSV). "Source" below means that folder or file; `<name>` is a short name for it (`ipc`, `ipc-key`, `pat`, `sutta`).

This guide and `kamma/audit/scripts/` are shared by several projects. They live in `dpd-pali-courses`; other projects hold symlinks to them. Run every command from the root of the project being audited: the scripts take all paths as arguments and never look at their own location.

## Scope and ground rules

- The audit is read-only. Never edit the source. The output is a findings list.
- One output file per source: `kamma/audit/<name>-audit.md`, or `kamma/audit/<name>-audit/<name>-audit.md` where the project keeps one folder per audit.
- No commits, no pushes.

## Process

1. **Mechanical checks first, by script, over the whole folder.** They are cheap and need no reading. `uv run python kamma/audit/scripts/mech_checks.py <folder>` covers:
   - local links and `#anchors`
   - external links: listed with `--links-out <file>`; check their HTTP status separately
   - index link text vs page H1, and every page listed in an index
   - table column counts
   - headings (missing, late or multiple H1, level jumps)
   - footnote references vs definitions (per file; add `--folder-footnotes` where ids are numbered across the whole folder)
   - stray characters (tabs, NBSP, zero-width, Cyrillic, non-NFC), odd `**`, trailing spaces, raw HTML other than `<br>`
   - counts for conventions: arrows, straight vs curly quotes, `ṁ` vs `ṃ`, `Pāli` vs `Pāḷi`, `<br>`, `{: … }` attribute markup

   Add the project's own checks where they exist (see Scripts → Project-specific checks).
2. **Line-by-line read, one slice at a time.** A slice is one or two files, about 500–1 000 lines. Print the files with line numbers and blank lines dropped (`grep -n "" file | grep -v "^[0-9]*:$"`).
   - **Check every suspicious Pāli form, grammar tag, root, compound type or gloss in DPD before writing it down.** Do not rely on memory. Run `uv run python kamma/audit/scripts/dpd_lookup.py <lemma> …` (read-only; needs a local `dpd.db`, path from `$DPD_DB`, default `/Users/deva/Documents/dpd-db/dpd.db`). It prints pos, grammar, root, compound type, construction and meaning per headword. Drop the finding if DPD agrees with the text; lower the confidence or put `DPD lookup` in `Suggested` if DPD is silent or ambiguous. Inflection for each entry is in `dpd_headword` table in clumn `inflections` and `inflections_html`.
3. **Save after every slice.** Write that slice's findings to its own file in `kamma/audit/scratch/` before reading the next slice.
4. **Verify the excerpts by script** once all slices are in: `uv run python kamma/audit/scripts/verify_rows.py <source root> kamma/audit/scratch/<slice files>`. Every backtick excerpt in `Current` must be found in the cited file within 2 lines of the cited line. Fix the rows that fail.
5. **Merge by script** into the final file: `uv run python kamma/audit/scripts/merge_audit.py kamma/audit/scratch/merge.toml`. It groups by category, keeps slice order and computes the summary table. Do not merge by hand. Then run step 4 once more on the final file.
6. **Delete `scratch/`** only after the final file is generated and checked by you.

## Limits and safety (learned the hard way)

- Do not run many subagents in parallel. Six strong-model readers at once drained the usage limit and five died with their output lost.
- The main session can read a whole source itself, slice by slice.
- If a subagent is used: one at a time, a cheaper model, and it returns findings as text. The main session saves them. Subagents cannot be relied on to write files.
- **!IMPORTANT!** The session scratchpad and agent transcripts do not survive a limit or a resume. Anything worth keeping goes into `kamma/audit/` immediately!
- Keep a short state note (done / not done) in `kamma/audit/scratch/STATE.md` and update it after each slice, so a restart knows where to resume.
- When a limit warning appears: stop, save, update the state note.

## Row format

Slice files (working format):

`| Cat | Location | Current | Problem | Suggested | Conf. |`

Final file: one table per category, `| Location | Current | Problem | Suggested | Conf. |`.

- **Location:** path relative to the source root plus line number(s), e.g. `class_17/5_cons_3.md:15`. For a single data file, the file name plus line (`patimokkha_word_by_word.tsv:5827`). For a second file in the same row, give its line number too, otherwise the excerpt check cannot confirm it.
- **Current:** verbatim from the source, in backticks, so it can be grep-checked. Never paraphrase inside backticks. Use `…` to skip text. A table pipe is written `¦` in slice files and converted to `\|` by the merge.
- **Suggested:** the exact replacement text or value, so the owner can accept it without further research. Pointing at a problem is not enough: a finding without a concrete suggestion (`(?)`, "check this", "unclear") cannot be approved or applied. Use `DPD lookup` / `verify` / `owner decision` only when the fix really cannot be known from the sources, and say what must be looked up or decided. If no clear suggestion can be made, put the row under category H, not A–F.
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
| I | Any further details, particularly concerning material under review. |

## What to look for

Content:
- Glosses swapped between columns, or one word glossed differently in different places (`āsava`, `hirottappa`, `buddha`).
- The same root spelt two ways (`√khan`/`√khaṇ`, `√dhu`/`√dhū`). See DPD roots for refferences.
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

## Recurring owner decisions (do not decide these in the audit)

- `<br>` in table cells and `{: .align-right }` versus the "no raw HTML in sources" rule.
- `Pāli` or `Pāḷi` in running text.
- Kaccāyana citation style.
- UK or US spelling.

## Scripts

All in `kamma/audit/scripts/`, with no project paths inside. Run them from the root of the project being audited (`uv run python kamma/audit/scripts/<script> …`).

- `dpd_lookup.py <lemma> …`: DPD headword lookup (see step 2). DB path from `$DPD_DB`.
- `mech_checks.py <folder> [--links-out <file>] [--folder-footnotes]`: the mechanical checks in step 1, over every `.md` file in the folder.
- `key_vs_ex.py <key folder> <exercise folder> [--glob "*_class.md"]`: compares the numbered sentences of a key with the same-named exercise files. Only for sources that have a key and an exercise folder.
- `verify_rows.py <source root> <audit file> …`: step 4. `<source root>` is the folder the Location paths are relative to. Takes slice files (6 columns) or a final file (5 columns). Pulls the backtick excerpts from `Current`, splits them on `…`, normalises spaces around pipes, and searches the cited file near the cited lines. Every number in `Location` that is not part of a file name counts as a cited line. Reports `NOT FOUND` and `WRONG LINE`, and the number of rows whose `Location` names no existing file; exits 1 on any failure.
- `merge_audit.py <merge.toml>`: step 5. Reads the slice files, groups rows by category, builds the summary table (count per category per slice, and count with confidence ≥ 8), and writes the final file around the hand-written parts. Rows with a wrong column count or an unknown category are listed as skipped. The config sits in `scratch/`; its paths are relative to its own folder:

  ```toml
  out = "../ipc-key-audit.md"        # final file
  head = "head.md"                   # optional: title, method, limits
  mid = "mid.md"                     # optional: goes after the summary (confidence, owner decisions)
  tail = "mechdetail.md"             # optional: goes last
  tail_title = "Mechanical detail"   # optional heading for the tail
  slices = [["16", "c16.md"], ["17–18", "c17-18.md"]]   # [summary column label, slice file], in order
  ```

  An optional `[titles]` table (`A = "A. …"`) replaces the default categories.

### Project-specific checks

These stay in their own project and are not shared:

- `dpd-pali-courses`: sutta links, `uv run python scripts/check_sutta_links.py docs/<course>`; for keys, the advisory report from `uv run python scripts/verify_key.py --course <course> --dpd --report <path>` (IMPOSSIBLE, NOT-FOUND, ROOT-MISMATCH rows).
