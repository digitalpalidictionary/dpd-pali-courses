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
    - `hooks/`: Custom MkDocs hooks for automated processing.
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

## Maintenance Scripts

This repository includes several Python scripts to maintain and clean the Pāḷi course Markdown source files. These scripts are located in the `scripts/` directory and can be run using `uv run python scripts/<script_name>.py`.

- **`verify_strict.py`**: Compares phrases from Markdown files against the generated HTML and PDF to ensure 100% data integrity and catch rendering issues. Run it only after freshly exporting all data. Can run only for some specific folders.
  - Usage: `uv run python scripts/verify_strict.py`

- **`compare_md_sources.py`**: Compares the current Markdown files against an older Git commit to detect potential data loss.
  - Usage: `uv run python scripts/compare_md_sources.py`

- **`pre_proccessing.sh`**: Bash which inlude all testing and verification, and preproccessing for building website, pdf, docs.

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
