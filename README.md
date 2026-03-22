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
- `tools/ssg/`: Custom scripts and assets used for building the static site.
- `mkdocs.yaml`: Configuration for the MkDocs static site generator.

## Static Site Generation

The website is built using [MkDocs](https://www.mkdocs.org/) with the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme. It serves as the primary way to interact with the course materials.

## Document Generation (PDF & DOCX)

In addition to the static website, this project can generate high-quality PDF and Word (`.docx`) documents for offline study and editing. These documents are generated directly from the same Markdown source files used for the website, ensuring consistency across all formats.

### PDF Generation

The PDF generation is handled by `scripts/generate_pdfs.py` using [WeasyPrint](https://weasyprint.org/).

- **Shared Styling**: The PDF generator uses the same CSS variables and stylesheets as the website, providing a unified look and feel.
- **Content Cleaning**: UI elements like navigation buttons, cross-references, and feedback forms are automatically stripped during the conversion process.

### DOCX Generation

The Word document generation is handled by `scripts/generate_docx.py` using [Pandoc](https://pandoc.org/).

- **Visual Parity**: The DOCX generator aims for visual parity with the PDF output, including Table of Contents and consistent typography.
- **Editable Format**: Provides a flexible format for users who wish to add their own notes or modify the course materials.

### Generating Documents Locally

1. **Install Dependencies**:
   - For PDF: Ensure you have `weasyprint` and its system dependencies installed.
   - For DOCX: Ensure you have [Pandoc](https://pandoc.org/installing.html) installed on your system.
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

- **`generate_pdfs.py`**: The primary script for creating PDF volumes from the course materials.
  - Usage: `uv run python scripts/generate_pdfs.py`

- **`generate_docx.py`**: The primary script for creating Word (.docx) volumes from the course materials.
  - Usage: `uv run python scripts/generate_docx.py`

- **`check_renumber.py`**: Automatically detects and corrects the numbering of Pāḷi sentences in exercise and answer key files.
  - Usage: `uv run python scripts/check_renumber.py`

- **`compare_docs.py`**: Compares the current Markdown files against an older Git commit to detect potential data loss.
  - Usage: `uv run python scripts/compare_docs.py`

- **`update_media_links.py`**: Updates media links and paths within the Markdown files to ensure they are correctly resolved in the static website.

- **`generate_mkdocs_yaml.py`**: A helper script to generate or update the `mkdocs.yaml` configuration based on the files in `docs/`.

## Local Development

This project uses `uv` for Python dependency management.

1. **Install uv**: Follow the instructions at [astral.sh/uv](https://astral.sh/uv).
2. **Install Dependencies**:
   ```bash
   uv sync
   ```
3. **Build and Serve Website Locally**:
   ```bash
   uv run mkdocs serve
   ```
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
