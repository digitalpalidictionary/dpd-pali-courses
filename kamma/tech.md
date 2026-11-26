# Tech Notes: DPD Pāḷi Courses

## Tools & Platforms
- **Languages:** Python (version 3.12 or higher).
- **Dependency Management:** `uv` is used for Python dependencies.
- **Static Site Generator:** MkDocs with the Material for MkDocs theme.
- **Document Generation:** WeasyPrint for PDF generation and Pandoc for DOCX documents.
- **Version Control & CI/CD:** Git and GitHub Actions for automated building and deployment.

## Who This Is For
- **Target Users:** Students of the Digital Pāḷi Dictionary (DPD) courses and general Pāḷi students.
- **Maintainers:** Contributors who update course content, fix bugs in generation scripts, and maintain the website.

## Constraints
- **Content Integrity:** Data preservation is critical; never remove data from `docs/` or cause loss during conversion.
- **Parity:** Maintain consistent formatting and numbering (footnotes, lists) across website, PDF, and DOCX formats.
- **Clean Markdown:** Source files must be user-friendly, avoid raw HTML, and rely on scripts/hooks for complex formatting.
- **Performance:** Ensure high accessibility and fast load times for the static website.

### Mid-table sub-header rows (added November 2026)
A data table that needs a grouped heading part-way down must not carry it as a body row (`| **label** | | ... |`); such a row renders as a stray near-empty line and breaks the row grouping in the PDF and DOCX. Instead close the table and restart: blank line, `**label**`, blank line, then a new table that begins with an empty header row of the same column count and its `| --- |` separator (precedent: `docs/ipc/class_17/3_cons_1.md`). If the sub-header is the first body row directly under an empty header row, put the bold line above the existing table and drop the row, so no empty one-row table is created. This is a manual editing convention only — `scripts/fixing_tables.py` does not fix it, because the exercise and answer files contain look-alike rows (`docs/ipc_ex/23_class.md`, `docs/ipc_ex/24_class.md`, `docs/bpc_ex/2_class.md`, `docs/ipc/class_18/11_ex.md`, a homework row in each course) that must stay as rows.

## Key verification (added November 2026)
`kamma/edits/scripts/verify_key.py` checks the answer keys (`docs/bpc_key/`, `docs/ipc_key/`) against the exercise files and the tag vocabulary. It is read-only on `docs/` and mandatory before any commit touching `docs/bpc_key/`, `docs/bpc_ex/`, `docs/ipc_key/` or `docs/ipc_ex/` (AGENTS.md → Key Verification); it must exit 0.

Two layers:
- **Structural (gating, exit 1 on any error):** key-vs-exercise numbering, POS and grammar tag vocabulary, root-cell format, IPC compound-type spelling, stray characters. Word-coverage is warnings only and never affects the exit code.
- **`--dpd` (advisory, never gates):** every row's form/tag/root checked against the local DPD SQLite DB, bucketed IMPOSSIBLE / AMBIGUOUS / CONFIRMED / NOT-FOUND / ROOT-MISMATCH / EXAMPLE-CONFLICT / SKIPPED (EXAMPLE-CONFLICT: a DPD headword quotes the key sentence in `example_1`/`example_2` and the key's POS/grammar disagrees with it) and written to a sorted TSV (`temp/key_dpd_report.tsv` by default; `temp/` is git-ignored). The DB lives outside the repo at `/Users/deva/Documents/dpd-db/dpd.db` (2.4 GB, machine-local), so `--dpd` is local-only — other machines pass a path.

Conventions to respect when extending it: the tag vocabulary lives as data (sets/regex constants at the top of the script), so new tags are added there rather than in check logic; the TSV columns and `row_key` format (`course/file/section/item/word/occ`) are a contract with the sentence-review threads, so a column change must update any consumer's spec. Feature rows are meant to be verified by fixture tests in `tests/test_verify_key.py` (`tests/` is git-ignored in this repo — the tests are local).

### Sentence-level review of the keys (added November 2026)
The `--dpd` buckets still leave rows DPD alone cannot settle, so a human/agent pass judges each one against its sentence and translation. The tool's usage, buckets, report columns, `row_key` rules and key-table gotchas are documented in the docstring at the top of `kamma/edits/scripts/verify_key.py`; the read-only review process is `kamma/audit/audit-guide.md` (output `kamma/audit/<course>-key-audit.md`). Standing rules from the first run (BPC + IPC, 2026-11-05): report **errors only** — a tag that is a valid reading of the form stays untouched, so no `UNDECIDED` verdicts and no notes lists; the single approval file is the only thing the user reviews; nothing in `docs/` changes until the user confirms it.

## Sutta links (added November 2026)
All sutta/Vinaya references link to `https://s.dhamma.gift/...` (the old `find.dhamma.gift/bw/` host is dead; GitHub #9). Rules live in `scripts/rewrite_sutta_links.py` (`map_url`): mn/dn -> `/mn/mnN/index.html`; sn/an -> `/sn|an/<book>/index.html#<id>`; snp, ud, kp, dhp, thag, thig, iti under `/kn/...` (dhp anchor `#dhpA`, tha/thi `#thagN.1`/`#thigN.1`); Vinaya under `/vin/tv/pli-tv-...` (old `bu-vb-sn` = new `ss`; `bu-vb-an` = `as`, page only; `bu-pt.html#pr|sg|np|pc|pd|sk` = `pli-tv-bu-pm3|4|6|7|8|9`; `vi/kd.html` is resolved from the link text, `VIN4.n` -> kd n, `VIN5.n` -> kd 10+n). Re-verify after any change with `uv run python scripts/check_sutta_links.py` (network; large pages, first run takes minutes, then cached). The site resolves anchors with JavaScript, so the checker accepts `<id>/0` too (dhp).

## Clean markup conventions (added November 2026)
The six English course folders hold plain Markdown only: no raw `<br>` and no kramdown/attr_list `{: … }`. `scripts/convert_br_markup.py` converts stray markup back to these shapes and runs in both preprocessing scripts.

- **Stacked table cell:** the authoring rule (spaced ` / ` = line break in a cell) is in `AGENTS.md` → Project Principles. This is the one piece of layout logic shared by all three pipelines — `tools/clean_markup.py:stack_table_cells`, called by `tools/markup_hook.py` (web), `generate_pdfs.pre_process_content`, and `generate_docx.aggregate_markdown` (which emits a real `<w:br/>` via an openxml snippet). Stacking is scoped to the six course folders: `docs/generated/` is exporter output where ` / ` is ordinary prose (e.g. `(should / could / may / might)` in `abbreviations.md`), so the hook and the reference PDF builds pass `stack_cells=False` there.
- **Exercise / key header:** `29. [DN16.27](…) (simpl)` on one line, the sentence on the next, indented to the list content (3 spaces for `N. `, 4 for `NN. `). `verify_key.parse_doc` appends that indented line to the item's sentence.
- **Right-aligned attribution:** the authoring rule (a paragraph starting with `— ` = right-aligned attribution) is in `AGENTS.md` → Project Principles. `tools/clean_markup.py:mark_attributions` adds `{: .align-right }` at render time for web and PDF (CSS: `identity/extra.css` → `.align-right`); DOCX right-aligns the paragraph in `post_process_docx` instead.
- **Heading ids:** never written in the source. The `toc` extension generates the slug; a link fragment must match `markdown.extensions.toc.slugify(heading text, "-")`.

## Frequency and DPD counts (added November 2026)
`scripts/check_frequencies.py` (GitHub #7) recomputes every quoted frequency and DPD count; definitions live in its module docstring.
- **Unique-words rule:** a DPD count is distinct `clean(lemma_1)` over rows with `meaning_1 != ''` (`clean` strips the homonym number); roots are counted directly.
- **Corpus counts:** exact-form counts from `cst_file_freq.json` over the Mūla files of a section (`NIK4`, `VIN`, `DN`…`KN`); absolutive counts keep only forms that are DPD `abs`/`ger` headwords.
- **Kita (IPC class 28):** primary-derivative rows only (`suffix`, `root_key`, one-line `construction`, six POS); a section total is the sum of its POS rows. `--write` ranks all 45 sections, keeps the top 18 on `1_kita_1.md`, and gives every section the same POS table with a bold total row (adding it where missing), and rebuilds the ranking table and the suffix lists; a content guard aborts if any other line would change.
- **Year footnotes:** every data footnote ends with `This data is relevant for the year YYYY.`; `--write` sets the current year and renumbers footnotes.

## Resources
- Original course materials from Google Docs (as reference).
- DPD CSS and JavaScript assets in `identity/`.
- `identity/courses-variables.css`: course colours live only here (loaded after `dpd-variables.css`); the course primary is DPD's `--primary-alt`. Never edit `dpd-variables.css` or `dpd.css`; they mirror upstream DPD.
- `identity/assets/`: `courses-logo.svg` (DPD's `dpd` letter paths on a `#0077cc` disc, one file for both schemes) and `courses-favicon.png` (96×96 RGBA), published at `assets/`. Re-render the favicon after changing the logo (Fish, repo root; `src` is relative to `temp/`, which is gitignored):
  `echo "<body style='margin:0;background:transparent'><img src='../identity/assets/courses-logo.svg' width=96 height=96 style='display:block'>" > temp/fav.html`
  `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --default-background-color=00000000 --window-size=96,96 --screenshot=identity/assets/courses-favicon.png "file://"(pwd)"/temp/fav.html"`
- Palette: three entries in `generate_mkdocs_yaml.py`, automatic first (`material/brightness-auto`, "A"). The toggle cycles auto → light → dark; Material remembers the choice in `localStorage` (`__palette`).
- Dark-mode images: any `-b.png`/`-d.png` pair, in any folder, is swapped by `identity/theme-images.js`; every other content image is dimmed (`brightness(.85)`) by a rule in `identity/extra.css`, except pacman/arrow. To give a new image a real dark version, add it as a `-b.png`/`-d.png` pair and link the `-b.png`.
- Project scripts for maintenance and generation in `scripts/`.
- Static Inter TTFs at `../website_example/identity_dpd/fonts/` (outside the repo, local only).

## What the output looks like
- A searchable website at [digitalpalidictionary.github.io/dpd-pali-courses/](https://digitalpalidictionary.github.io/dpd-pali-courses/).
- PDF course volumes in `pdf_exports/`.
- DOCX course documents in `docx_exports/`.
- Release archives (per-course PDF/DOCX zips) attached to GitHub Releases by `release_class.yaml`.

`mkdocs.yaml` is generated (`generate_mkdocs_yaml.py`) and gitignored. The website scripts, `pdf_preprocessing.sh` and both workflows regenerate it first; a bare `generate_pdfs.py`/`generate_docx.py` run on a fresh clone needs the generator run once.
