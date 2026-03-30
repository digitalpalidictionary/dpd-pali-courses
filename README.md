# DPD Pāḷi Courses

This repository contains the source materials for the Digital Pāḷi Dictionary (DPD) Pāḷi courses, transformed from original Google Docs into a modern, searchable static website.

## Repository Contents

- `docs/`: Markdown source files for all course materials.
    - `bpc/`: Beginner Pāḷi Course (BPC) lessons.
    - `bpc_ex/`: BPC Exercises.
    - `bpc_key/`: BPC Answer Keys.
    - `ipc/`: Intermediate Pāḷi Course (IPC) lessons.
    - `ipc_ex/`: IPC Exercises.
    - `ipc_key/`: IPC Answer Keys.
- `identity/`: DPD CSS and JavaScript assets used for the website and document generation.
- `scripts/`: Regularly used maintenance and generation scripts (runnable with `uv run`).
- `tools/`: Python modules used by scripts (imports only).
- `mkdocs.yaml`: Configuration for the MkDocs static site generator.

## Static Site Generation

The website is built using [MkDocs](https://www.mkdocs.org/) with the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme. It serves as the primary way to interact with the course materials.

### Document Generation (PDF & DOCX)

In addition to the static website, this project can generate high-quality PDF and Word (`.docx`) documents for offline study and editing. These documents are generated directly from the same Markdown source files used for the website, ensuring consistency across all formats.

#### System Dependencies

To generate documents locally, you must install the following system-level dependencies:

**macOS (using [Homebrew](https://brew.sh/)):**
```bash
# For PDF generation (WeasyPrint dependencies)
brew install weasyprint
# or 
brew install pango libffi

# For DOCX generation (Pandoc)
brew install pandoc
```

**Linux (Ubuntu/Debian):**
```bash
# For PDF generation
sudo apt-get install python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0

# For DOCX generation
sudo apt-get install pandoc
```

### Generating Documents Locally

1. **Install Python Dependencies**:
   Ensure your local environment is up to date:
   ```bash
   uv sync
   ```
2. **Run the Scripts**:
   ```bash
   # Generate PDFs
   uv run python scripts/generate_pdfs.py

   # Generate DOCX
   uv run python scripts/generate_docx.py
   ```
   The generated files will be placed in the `pdf_exports/` and `docx_exports/` directories respectively.

## Maintenance & Generation Scripts

All scripts are located in the `scripts/` directory and can be run using `uv run python scripts/<script_name>.py` (for Python scripts) or `uv run bash scripts/<script_name>.sh` (for shell scripts).

### Quick Start Commands

**Build the website locally:**
```bash
./scripts/cl/pali-build-website
```

**Generate PDFs and DOCX documents:**
```bash
./scripts/cl/pali-build-pdf-doc
```

### Content Verification & Validation

- **`verify_sources.py`**: Interactive source verification tool that compares original (old) DOCX materials against generated DOCX and PDF outputs. Helps identify discrepancies between source and generated formats.
  - Usage: `uv run python scripts/verify_sources.py`

- **`verify_pdf_content.py`**: Extracts text from generated PDFs and compares with source Markdown to ensure no data loss during PDF generation.
  - Usage: `uv run python scripts/verify_pdf_content.py`

- **`verify_docx_content.py`**: Verification tool for DOCX content integrity. Compares text extracted from generated Word documents with source Markdown.
  - Usage: `uv run python scripts/verify_docx_content.py`

- **`verify_numbering.py`**: Verifies consistency of sentence numbering (footnotes, lists) across Markdown, website, and PDF. Identifies discrepancies where numbering resets or differs between formats.
  - Usage: `uv run python scripts/verify_numbering.py`

- **`compare_md_sources.py`**: Compares current Markdown files against an older Git commit to detect potential data loss or regressions in course content.
  - Usage: `uv run python scripts/compare_md_sources.py [--commit <hash>]`

### Document Generation

- **`generate_pdfs.py`**: Generates high-quality PDF course materials from Markdown source files using WeasyPrint. Applies course-specific styling, cleans UI elements, and handles footnote reformatting. Output goes to `pdf_exports/`.
  - Usage: `uv run python scripts/generate_pdfs.py`

- **`generate_docx.py`**: Generates Word (.docx) documents from Markdown source using Pandoc. Maintains visual parity with PDF output for offline study. Output goes to `docx_exports/`.
  - Usage: `uv run python scripts/generate_docx.py`

### Content Cleanup & Maintenance

- **`renumber_footnotes.py`**: Renumbers footnotes sequentially across all files in a course folder. The counter starts at 1 and continues across files in course order, correcting duplicate numbers and out-of-order references automatically.
  - Usage: `uv run python scripts/renumber_footnotes.py [--dry-run]`

- **`check_renumber.py`**: Detects and corrects numbering inconsistencies in Pāḷi sentence lists. Supports dry-run and automatic re-numbering of exercises and answer keys.
  - Usage: `uv run python scripts/check_renumber.py [--dry-run]`

- **`clean_dead_links.py`**: Finds and removes dead links in Markdown files. Specifically targets list items in index files that link to removed `.md` files.
  - Usage: `uv run python scripts/clean_dead_links.py`

### Site & Metadata Generation

- **`generate_mkdocs_yaml.py`**: Helper script to update `mkdocs.yaml` based on course folder structure. Automatically generates the navigation section using headings from Markdown files.
  - Usage: `uv run python scripts/generate_mkdocs_yaml.py`

- **`generate_indexes.py`**: Generates `index.md` pages for course categories, creating a Table of Contents based on individual lesson headings.
  - Usage: `uv run python scripts/generate_indexes.py`

- **`update_css.py`**: Synchronizes CSS variables from source configurations to the Identity stylesheet directory.
  - Usage: `uv run python scripts/update_css.py`

### Pre-Processing Workflows

Pre-processing scripts run a series of checks and corrections before building the website or documents:

- **`web_preprocessing.sh`**: Runs all pre-processing steps required before building the MkDocs website (generates metadata, renumbers content, cleans links, updates CSS).
  - Usage: `uv run bash scripts/web_preprocessing.sh`

- **`pdf_preprocessing.sh`**: Runs pre-processing steps required before generating PDF and DOCX documents.
  - Usage: `uv run bash scripts/pdf_preprocessing.sh`

### Utilities & Legacy Tools

- **`download_all_materials.py`**: Downloads old source materials from Google Docs as a ZIP archive. Facilitates keeping Markdown source files in sync with original (old) sources if needed (for reference/backup purposes).
  - Usage: `uv run python scripts/download_all_materials.py`

## Local Development

This project uses `uv` for Python dependency management.

1. **Install uv**: Follow the instructions at [astral.sh/uv](https://astral.sh/uv).
2. **Install Dependencies**:
   ```bash
   uv sync
   ```
3. **Build and Serve Website Locally**:
   We recommend using the included unified build script, which handles metadata generation, renumbering, and starting the local server:
   ```bash
   ./scripts/cl/pali-build-website
   ```
   *To run this from anywhere on your system, add `scripts/cl/` to your PATH (e.g., `fish_add_path /path/to/dpd-pali-courses/scripts/cl` in Fish).*
   
   The site will be available at `http://127.0.0.1:8000`.

4. **Generate Documents Locally**:
   ```bash
   uv run python scripts/generate_pdfs.py
   uv run python scripts/generate_docx.py
   ```

## Automated Deployment & Generation

The website, PDF volumes, and DOCX volumes are automatically updated whenever changes are pushed to the `main` branch.

- **Website Deployment**: Handled by `.github/workflows/deploy_site.yaml`.
- **Document Generation**: Handled by a unified workflow that generates both PDF and DOCX artifacts and publishes them to the latest GitHub Release.

---

## Useful Links (Original Sources)

*Note: These Google Docs are the original sources. They will be removed once the Markdown conversion and website are fully verified.*

### Project Management
- [GitHub Project](https://github.com/orgs/digitalpalidictionary/projects/2)
- [Design Brief](https://github.com/digitalpalidictionary/dpd-pali-courses/issues/1)

### Beginner Pāḷi Course
- [Beginner Pāḷi Course (Google Doc)](https://docs.google.com/document/d/1FOKjmABrz6reeFDBWwpjDq1_J3m83-bd1TMXPcgEHmY/)
- [Beginner Pāḷi Course Exercises (Google Doc)](https://docs.google.com/document/d/1jqKL8Nlghi1T2m9y0BAN17yk2Na-34fFan1tMI4mrGw/)
- [Beginner Pāḷi Course Key (Google Doc)](https://docs.google.com/document/d/1AX4wqoVokRfTfr89EKxHPC1Yb80HKa2sqxX4q-nofso/)
- [Beginner Pāḷi Course: Vocabulary](https://sasanarakkha.github.io/study-tools/pali-class/vocab/vocab_bpc.html)

### Intermediate Pāḷi Course
- [Intermediate Pāḷi Course (Google Doc)](https://docs.google.com/document/d/1qsYPFOifOUN2HIbFCH7kaglJyI2CVd9MH9A6Kt9rSxg/)
- [Intermediate Pāḷi Course Exercises (Google Doc)](https://docs.google.com/document/d/15x3PRqzW5VRuFQSJ-oOvKOZ2y1tNIgwYdhDWd-plHRI/)
- [Intermediate Pāḷi Course Key (Google Doc)](https://docs.google.com/document/d/1AXSKpmYYuiinQYTBJ133rMZJc53qbZSLr_7UE-syofg/)
- [Intermediate Pāḷi Course: Vocabulary](https://sasanarakkha.github.io/study-tools/pali-class/vocab/vocab_ipc.html)
