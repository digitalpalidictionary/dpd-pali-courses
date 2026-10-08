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

## Resources
- Original course materials from Google Docs (as reference).
- DPD CSS and JavaScript assets in `identity/`.
- Project scripts for maintenance and generation in `scripts/`.
- Static Inter TTFs at `../website_example/identity_dpd/fonts/` (outside the repo, local only).
- Noto Sans Devanagari static TTFs + OFL licence vendored in `identity/fonts/` (committed, so CI renders Hindi).

## What the output looks like
- A searchable website at [digitalpalidictionary.github.io/dpd-pali-courses/](https://digitalpalidictionary.github.io/dpd-pali-courses/).
- PDF course volumes in `pdf_exports/`.
- DOCX course documents in `docx_exports/`.
- Release archives (per-course PDF/DOCX zips) attached to GitHub Releases by `release_class.yaml`. Hindi is not released yet.

## Multi-language support (added October 2026)
Translations live in mirror folders that copy the English structure exactly (`docs/bpc_hi/`, `docs/bpc_hi_ex/`, `docs/bpc_hi_key/`; IPC Hindi would follow the same pattern). The Hindi sources currently contain the English text as a translation base.

Folder names are hard-coded in several places — a new language must be registered in ALL of:
- `scripts/generate_pdfs.py` — `FOLDER_NAMES`, lesson/ex folder checks (`bpc`, `bpc_ex` lists), `folders` list
- `scripts/generate_docx.py` — same set as PDF script
- `scripts/generate_mkdocs_yaml.py` — `extra.unpublished_nav` + `exclude_docs` while unpublished; `nav` once published
- `scripts/generate_indexes.py` — `sections` list (two places) and display labels
- `scripts/renumber_footnotes.py` and `scripts/check_renumber.py` — `target_dirs`
- `scripts/verify_pdf_content.py`, `scripts/verify_docx_content.py`, `scripts/verify_numbering.py` — volume/folder lists
- `identity/extra.css` — `body.<folder>_ex` / `body.<folder>_key` print table rules
- `tools/nav_hook.py` — lesson → exercises "Go to Exercises" link
- `.github/workflows/release_class.yaml` — archive names and release files (only when publishing)
- `justfile` — a translator build recipe like `hindi`

`mkdocs.yaml` is generated (`generate_mkdocs_yaml.py`) and gitignored. The website scripts, `pdf_preprocessing.sh`, `just hindi` and both workflows regenerate it first; a bare `generate_pdfs.py`/`generate_docx.py` run on a fresh clone needs the generator run once.

Translator build: `just hindi` (root `justfile`) regenerates `mkdocs.yaml` and the section indexes, then builds only the three `bpc_hi*` PDFs and DOCX files. `generate_indexes.py` rewrites every section index but is deterministic, so it only changes the Hindi ones when Hindi headings change. Without the out-of-repo Inter TTFs, Latin/Pāḷi text falls back to a system font; Devanagari uses the vendored Noto fonts. The Noto `@font-face` rules carry a Devanagari `unicode-range`, because the TTF also has ASCII digits and punctuation that would otherwise render in Noto whenever Inter is missing (CI release PDFs included).

Translator workflow (Windows, non-technical): the translator works only through Google Antigravity (Gemini Pro). On the `hindi` branch, `AGENTS.md` holds the assistant's instructions: setup, translating, building and pushing to `hindi`. The build is `just hindi` with `WEASYPRINT_DLL_DIRECTORIES=C:\msys64\ucrt64\bin` (Pango from MSYS2); the justfile sets `windows-shell` to PowerShell. Windows-safety rules for scripts the recipe runs: build nav/link paths with `posixpath` / `.as_posix()`, write generated files with `newline="\n"`, pass image paths to WeasyPrint as `file://` URIs. `.gitattributes` stores text as LF. `release_class.yaml` runs on `main` only, and both workflows ignore Hindi-only changes. The Windows setup is untested on a real Windows machine as of October 2026.

### Unpublished translations
A translation stays off the website and out of releases until it is finished:
- `generate_mkdocs_yaml.py` puts its menu under `extra.unpublished_nav` (MkDocs ignores it) and adds its folders to `exclude_docs`, so `mkdocs build` skips those pages.
- `generate_pdfs.py`, `generate_docx.py` and `verify_docx_content.py` read `nav` + `extra.unpublished_nav`, so local PDF/DOCX builds still include it. CI also builds them, but `release_class.yaml` does not zip them.

To publish Hindi BPC:
1. In `generate_mkdocs_yaml.py`, move the `Beginner Course Hindi (BPC-HI)` entry from `extra.unpublished_nav` into `nav` (after the English BPC), and delete the three `bpc_hi` patterns from `exclude_docs`.
2. In `release_class.yaml`, add env `BPC_HI_PDF_ARCHIVE: beginner_pali_course_hindi_pdfs.zip` and `BPC_HI_DOCX_ARCHIVE: beginner_pali_course_hindi_exercises_docx.zip`; zip `bpc_hi.pdf bpc_hi_ex.pdf bpc_hi_key.pdf` and `bpc_hi_ex.docx bpc_hi_key.docx` next to the BPC lines; add a "Beginner Pāli Course (Hindi)" block to the release body and both archives to `files:`.
3. Remove the `!docs/bpc_hi*/**` path ignores from `release_class.yaml` and `deploy_site.yaml`.
4. Add the Hindi downloads to `README.md` and `docs/downloads.md`.
5. Consider adding `bpc_hi/` to the priority list in `identity/search_order.js` and a Hindi course name in the `tools/nav_hook.py` feedback link.

Font rule: the body font stack is `"Inter", "Noto Sans Devanagari", sans-serif` (`identity/dpd.css`), with `@font-face` registrations in `identity/dpd-pdf-fonts.css`. Any new script (Bengali, Sinhala, Thai…) needs its static TTFs vendored in `identity/fonts/` and registered the same way — variable fonts corrupt Pāḷi diacritics in WeasyPrint.

Verification shortcut: render a Devanagari + Pāḷi smoke-test string through the four `identity/*.css` files with WeasyPrint and check `pdffonts` output shows the expected fonts embedded.
