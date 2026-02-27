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

The website is built using [MkDocs](https://www.mkdocs.org/) with the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme.

### Local Development

This project uses `uv` for Python dependency management.

1. **Install uv**: Follow the instructions at [astral.sh/uv](https://astral.sh/uv).
2. **Install Dependencies**:
   ```bash
   uv sync
   ```
3. **Build and Serve Locally**:
   ```bash
   uv run mkdocs serve
   ```
   The site will be available at `http://127.0.0.1:8000`.

### Automated Deployment

The website is automatically built and deployed to the `gh-pages` branch whenever changes are pushed to the `main` branch. This is handled by a GitHub Action defined in `.github/workflows/deploy_site.yaml`.

The build pipeline performs the following steps:
1. Generates directory indexes using `tools/ssg/scripts/generate_indexes.py`.
2. Updates CSS and styling via `tools/ssg/scripts/update_css.py`.
3. Builds the static HTML site using `mkdocs build`.
4. Deploys the resulting `site/` directory to the `gh-pages` branch.

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
