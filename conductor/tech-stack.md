# Tech Stack

## Programming Languages
- **Python:** Used for document processing, downloading materials, and automation scripts.
- **Markdown:** The primary language for all course content, exercises, and keys.

## Infrastructure & Automation
- **GitHub Actions:** Handles automated workflows, such as release creation and potentially static site generation.
- **uv:** Python package and environment manager.
- **Git:** Version control for all source materials and project documentation.

## Content Management
- **MkDocs:** Static site generator for building the course website.
- **Material for MkDocs:** The primary theme used for the website's visual identity.

## Maintenance Tools
- **`check_renumber.py`**: Automated script to ensure sequential Pāḷi sentence numbering in exercise and key files.
**vocab_abbrev_pali_course.py** (in `dpd-db`): Generates Markdown vocabulary and abbreviation pages from the DPD database.
**tablesort**: JS library for sortable tables on the website.
**theme-images.js**: Custom JS for switching between dark and light image variants.

## Dependencies (Python)
- `requests`: For handling external data and document downloads.
- `zipfile`, `os`, `re`: Standard libraries for file management and text processing.
- `mkdocs`, `mkdocs-material`: For building the documentation site.
- `weasyprint`, `markdown`: For HTML to PDF generation.
- `pypandoc`: For Markdown to DOCX generation.
- `python-docx`: For post-processing DOCX documents.

