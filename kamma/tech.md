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

## What the output looks like
- A searchable website at [digitalpalidictionary.github.io/dpd-pali-courses/](https://digitalpalidictionary.github.io/dpd-pali-courses/).
- PDF course volumes in `pdf_exports/`.
- DOCX course documents in `docx_exports/`.
