# DPD Pāḷi Courses — Website Architecture: Unified Technical Analysis

This document is the authoritative, unified technical analysis of how the DPD Pāḷi Courses website is built, structured, rendered, and made interactive. It is concerned exclusively with **how things work**, not with the linguistic or pedagogical content of the course materials.

The term **"identity"** in this project means **visual site identity** — branding, colors, layout overrides, and browser-side behavior. It has nothing to do with user authentication, login, or accounts. There is no backend, no database, no server-side rendering.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Technology Stack](#2-technology-stack)
3. [Directory Structure](#3-directory-structure)
4. [Course & Content Organization](#4-course--content-organization)
5. [Build Pipeline — Pre-Processing](#5-build-pipeline--pre-processing)
6. [Build Pipeline — MkDocs Rendering](#6-build-pipeline--mkdocs-rendering)
7. [CI/CD Deployment](#7-cicd-deployment)
8. [Local Development](#8-local-development)
9. [mkdocs.yaml — Configuration Central](#9-mkdocsyaml--configuration-central)
10. [Navigation Architecture — 4 Layers](#10-navigation-architecture--4-layers)
11. [Heading Structure & TOC](#11-heading-structure--toc)
12. [Identity Folder: CSS Architecture](#12-identity-folder-css-architecture)
13. [Identity Folder: JavaScript](#13-identity-folder-javascript)
14. [Footnote System — End to End](#14-footnote-system--end-to-end)
15. [List Numbering System](#15-list-numbering-system)
16. [Table System](#16-table-system)
17. [Images & Theme Awareness](#17-images--theme-awareness)
18. [Dark/Light Mode Mechanics](#18-darklight-mode-mechanics)
19. [Generated Content](#19-generated-content)
20. [Complete Request-Response Cycle](#20-complete-request-response-cycle)
21. [How Every Clickable Element Works](#21-how-every-clickable-element-works)
22. [What is Authored vs Generated vs Transformed](#22-what-is-authored-vs-generated-vs-transformed)
23. [Architecture Diagram](#23-architecture-diagram)
24. [Limitations & Risks](#24-limitations--risks)
25. [Master File Map](#25-master-file-map)

---

## 1. Executive Summary

The site is a **fully static** MkDocs website. There is no server, no backend, no database query at request time. Every page is pre-built HTML served from GitHub Pages.

The key architectural insight is that the site is built by **layering**:

1. **Source content** — Markdown files in `docs/`, authored by humans
2. **Pre-processing** — Python scripts that mutate and repair those Markdown files before MkDocs sees them
3. **MkDocs rendering** — Converts Markdown to HTML using the Material theme and configured extensions
4. **Hook layer** — Python hooks that intercept and modify content during MkDocs rendering
5. **Identity layer** — Custom CSS and JavaScript in `identity/` that reshape the rendered output visually and interactively
6. **Client-side enhancements** — JavaScript that runs in the browser after the static page loads, adding tooltips, sorting, image swapping, and title linkability

None of these layers is optional. The final site behavior is a product of all six working together.

---

## 2. Technology Stack

| Component | Technology | Version / Notes |
|-----------|-----------|-----------------|
| Static Site Generator | MkDocs | v1.6+ |
| Theme | Material for MkDocs | v9.5+ |
| Package Manager | `uv` (Astral) | `uv add`, `uv run` — never `pip` |
| Markdown Extensions | pymdownx suite | highlight, inlinehilite, snippets, superfences |
| CSS Custom Properties | `identity/dpd-variables.css` | Project's color/shadow source of truth |
| JavaScript (client-side) | Custom JS in `identity/` | No framework — vanilla JS |
| Deployment | GitHub Pages via GitHub Actions | `peaceiris/actions-gh-pages@v4` |
| Live site URL | `https://digitalpalidictionary.github.io/dpd-pali-courses/` | |

---

## 3. Directory Structure

```
dpd-pali-courses/
│
├── docs/                    # Markdown source content (the entire site content tree)
│   ├── index.md             # Homepage
│   ├── about.md
│   ├── downloads.md
│   ├── literature.md
│   ├── bpc/                 # Beginner Pāḷi Course lesson folders
│   ├── bpc_ex/              # BPC exercise files
│   ├── bpc_key/             # BPC answer key files
│   ├── ipc/                 # Intermediate Pāḷi Course lesson folders
│   ├── ipc_ex/              # IPC exercise files
│   ├── ipc_key/             # IPC answer key files
│   ├── anki/                # Anki deck documentation
│   ├── assets/              # Images and static assets
│   │   └── images/          # All image files used in content
│   └── generated/           # Auto-generated content (vocab, abbreviations)
│       └── vocab/           # Per-class vocabulary pages
│
├── identity/                # Custom theme overrides — CSS + JS
│   ├── dpd-variables.css    # CSS custom properties (colors, shadows)
│   ├── dpd.css              # Content-component styles (tables, buttons, tooltips)
│   ├── extra.css            # Material theme shell overrides (layout, dark/light mode)
│   ├── dpd-pdf-fonts.css    # PDF-specific font definitions
│   ├── footnotes.js         # Tooltip behavior, list numbering, title linking
│   ├── search_order.js      # Search result prioritization
│   ├── tablesort-all.js     # Sortable table headers
│   └── theme-images.js      # Light/dark image swapping
│
├── tools/                   # Python MkDocs hooks (run during mkdocs build)
│   ├── footnote_hook.py     # Protects footnotes and list numbering during rendering
│   ├── nav_hook.py          # Injects prev/next, exercise links, feedback links
│   ├── paths.py             # Centralized path management
│   └── printer.py           # Console output formatting (pr.green, pr.yes, etc.)
│
├── scripts/                 # Pre-processing and generation scripts
│   ├── web_preprocessing.sh # Orchestrates all pre-processing steps
│   ├── generate_mkdocs_yaml.py  # Regenerates nav tree from filesystem
│   ├── generate_indexes.py      # Writes section/class index pages
│   ├── renumber_footnotes.py    # Keeps footnote numbers sequential
│   ├── check_renumber.py        # Detects/fixes list numbering issues
│   ├── clean_dead_links.py      # Removes broken links from index pages
│   ├── fix_heading_hierarchy.py # Normalizes heading levels
│   ├── fixing_tables.py         # Normalizes Markdown table formatting
│   ├── update_css.py            # Syncs CSS variables
│   └── cl/                      # CLI scripts (must be chmod +x)
│       └── pali-build-website   # Local dev launcher
│
├── mkdocs.yaml              # Main configuration (nav, theme, extensions, hooks)
├── site/                    # Generated static HTML output (not committed)
└── .github/
    └── workflows/
        ├── deploy_site.yaml     # CI/CD: auto-deploy on push to main
        └── release_class.yaml  # Release pipeline for document exports
```

---

## 4. Course & Content Organization

### 4.1 Lesson Folders

```
docs/bpc/
├── index.md              ← generated section hub (lists all classes)
├── class_1/
│   └── index.md          ← class hub (generated)
├── class_2/
│   ├── index.md          ← class hub (generated)
│   ├── 1_review.md
│   ├── 2_alphabet.md
│   ├── 3_decl_nouns.md
│   └── 4_home_work.md
└── ... class_3 through class_14

docs/ipc/
├── index.md
└── class_16 through class_28/
```

**BPC**: 14 lesson folders (`class_1` – `class_14`)
**IPC**: 13 lesson folders (`class_16` – `class_28`)

### 4.2 Exercise & Key Files

```
docs/bpc_ex/    ← 15 exercise files (1_class.md through 15_class.md)
docs/bpc_key/   ← answer key files
docs/ipc_ex/    ← 14 exercise files (16_class.md through 29_class.md)
docs/ipc_key/   ← answer key files
```

Note: Exercise files extend one class beyond the lesson folders (BPC has exercises for class 15; IPC has exercises for class 29), but there are no corresponding lesson folders for those.

### 4.3 Page Naming Convention

Files inside a class folder are numbered with a prefix that determines their sort order:
```
1_review.md
2_alphabet.md
3_decl_nouns.md
10_aor.md        ← numeric sort required (not lexical: "10" > "2")
```

The `generate_mkdocs_yaml.py` script uses numeric sorting for this reason (see §5.1).

### 4.4 Generated Reference

```
docs/generated/
├── abbreviations.md           ← generated from dpd-db
└── vocab/
    ├── index.md
    ├── class-02.md
    └── ... class-29.md
```

---

## 5. Build Pipeline — Pre-Processing

### 5.1 Overview

The website is **not** built by running `mkdocs build` alone. The real build chain starts with:

```bash
./scripts/web_preprocessing.sh
```

This script runs 8 Python scripts **in strict order**, each of which **mutates the Markdown source files** before MkDocs sees them.

### 5.2 Script Sequence and Why Order Matters

```
scripts/web_preprocessing.sh
│
├── 1. generate_mkdocs_yaml.py      ← must run FIRST (rebuilds nav tree)
├── 2. check_renumber.py            ← before MkDocs sees ordered lists
├── 3. renumber_footnotes.py        ← before MkDocs processes footnote syntax
├── 4. clean_dead_links.py          ← after nav is known, before index generation
├── 5. fix_heading_hierarchy.py     ← before TOC plugin reads headings
├── 6. fixing_tables.py             ← before Markdown tables are parsed
├── 7. generate_indexes.py          ← depends on fixed headings and clean links
└── 8. update_css.py                ← syncs CSS variables before site build
```

**Why ordering matters:**
- `generate_mkdocs_yaml.py` must run early because everything else depends on a valid nav tree
- `renumber_footnotes.py` must run before MkDocs sees the Markdown, or footnote numbers propagate incorrectly into HTML
- `fix_heading_hierarchy.py` must run before `generate_indexes.py`, which extracts headings for link labels
- `clean_dead_links.py` must run before `generate_indexes.py` to prevent dead links from appearing in generated indexes

### 5.3 Script Details

#### `generate_mkdocs_yaml.py`

Regenerates the entire `nav:` section of `mkdocs.yaml` from the filesystem. It does three important things:

1. **Extracts page labels from headings** — `get_first_heading()` reads the first `#` heading from each `.md` file, strips leading numbers and attribute lists like `{#anchor}`, and uses the cleaned human-readable title as the nav label. This means nav labels are derived from content, not duplicated manually.

2. **Numeric sorting** — `get_files_sorted()` sorts filenames like `1_review.md`, `2_alphabet.md`, `10_aor.md` in numeric order rather than lexical order. Without this, `10_...` would sort before `2_...`.

3. **Builds nested nav groups** — `build_class_nav()` scans `docs/bpc/` and `docs/ipc/` for `class_*` folders and constructs nested structures: Lessons Index → Class 1 → Class 2 → (subpages for each). This mechanism produces the hierarchical sidebar menu.

4. **Handles all content types** — The same script also generates nav for exercises (`bpc_ex/`, `ipc_ex/`), answer keys (`bpc_key/`, `ipc_key/`), Anki docs, and reference pages (abbreviations, vocabulary).

The nav tree in `mkdocs.yaml` is therefore a **hybrid**:
- Fixed top-level site pages (Home, About, Downloads, Literature)
- Filesystem-scanned course pages (generated)
- Generated reference pages

#### `check_renumber.py`

Detects and fixes ordered list numbering inconsistencies in exercise files. Ensures that lists that were interrupted (by tables, code blocks, or other block elements) have their numbering corrected.

#### `renumber_footnotes.py`

Renumbers all footnotes (`[^1]`, `[^2]`, etc.) sequentially across all files in course order (BPC Class 1 → Class 2 → ... → IPC Class 16 → ...). This prevents duplicate footnote numbers across pages.

#### `clean_dead_links.py`

Scans index pages and removes any list entries that point to `.md` files that no longer exist. Prevents broken navigation items.

#### `fix_heading_hierarchy.py`

Does two things:
1. If the first non-empty line is bold text like `**Class 1**`, it converts it to `# Class 1`
2. If a page skips heading levels (e.g., jumps from `#` to `###` without an intervening `##`), it reduces the skipped level to make the sequence continuous

This runs before the TOC plugin and before `generate_indexes.py` so that both see a consistent heading structure.

#### `fixing_tables.py`

Normalizes Markdown table formatting: cell padding, separator rows, stripping extra whitespace. Also strips empty cells (handled further by `footnote_hook.py` at render time).

#### `generate_indexes.py`

Creates `index.md` landing pages for every major section and class. Specifically:

- Writes section hubs: `docs/bpc/index.md`, `docs/ipc/index.md`, `docs/bpc_ex/index.md`, etc.
- Writes class hubs: `docs/bpc/class_2/index.md`, `docs/ipc/class_17/index.md`, etc.
- Derives link labels from the first heading in each page (using `get_first_heading()`)
- **Intentionally skips** certain pages from main index listings via `should_skip_in_main_index()`: pages whose headings or filenames imply "review", "homework", "content/title/literature"
- Preserves class-order navigation: class index pages link to previous/next class index pages, while lesson pages stay inside their own class for prev/next calculation

#### `update_css.py`

Syncs CSS variable definitions from source configurations into `identity/dpd-variables.css`. Ensures the variable file is always in sync with the project's color configuration before the site is built.

---

## 6. Build Pipeline — MkDocs Rendering

### 6.1 The MkDocs Hook Pipeline

After pre-processing, MkDocs processes each page through this exact sequence:

```
Markdown source (.md)
    │
    ▼ on_page_markdown() — tools/footnote_hook.py
    │  • Converts [^N] → <sup class='manual-fn-ref' data-fn='N'>N</sup>
    │  • Converts [^N]: text → <div class='manual-fn-def' data-fn='N'>text</div>
    │  • Inserts <div class='manual-list-start' data-start='N'> before numbered list items
    │  • Converts 3+ newlines → <br> tags
    │  • Injects &nbsp; into empty table cells
    │
    ▼ on_page_markdown() — tools/nav_hook.py
    │  • Strips any hardcoded <div class="nav-links"> blocks from Markdown source
    │
    ▼ Markdown Extensions (pymdownx, toc, tables, attr_list, md_in_html, nl2br)
    │  • toc generates heading IDs and permalink anchors
    │  • tables renders | pipe tables to HTML <table>
    │  • attr_list enables {#id .class} syntax on elements
    │  • nl2br turns single newlines into <br>
    │  • pymdownx.highlight adds syntax-highlighted code blocks
    │  • pymdownx.snippets enables file inclusion syntax
    │
    ▼ Material Theme Templates
    │  • Applies full page shell: header, sidebar, tabs, TOC, footer
    │  • Injects theme CSS and JS references
    │
    ▼ on_post_page() — tools/nav_hook.py
    │  • Reads page.previous_page, page.next_page from MkDocs nav state
    │  • Generates relative URLs with get_relative_url()
    │  • Injects <div class="nav-links"> block before </body>
    │    containing: ← Previous, Next →, Go to Exercises, Feedback link
    │
    ▼ on_post_page() — tools/footnote_hook.py
    │  • Uses BeautifulSoup to find div.manual-list-start markers
    │  • Sets <ol start="N"> on the next sibling <ol> element
    │  • Hides the marker div
    │
    ▼ Final HTML output → site/ directory
```

### 6.2 Hooks Configuration in mkdocs.yaml

```yaml
hooks:
  - tools/footnote_hook.py
  - tools/nav_hook.py
```

Hooks are loaded at MkDocs startup. Changing a hook file requires a manual restart of the dev server (live reload does not pick up hook changes).

### 6.3 Markdown Extensions in Use

| Extension | What It Does |
|-----------|-------------|
| `attr_list` | Enables `{#id .class key=value}` syntax on any element |
| `toc` (permalink: true, baselevel: 2) | Generates TOC sidebar, adds `§` permalink links to headings, shifts heading levels by 1 |
| `pymdownx.highlight` (anchor_linenums: true) | Syntax-highlighted code blocks with anchor line numbers |
| `pymdownx.inlinehilite` | Inline code syntax highlighting |
| `pymdownx.snippets` | `--8<-- "file.md"` include/embed syntax |
| `pymdownx.superfences` | Enables nested fenced code blocks |
| `tables` | Standard Markdown pipe table → HTML `<table>` |
| `md_in_html` | Allows Markdown inside raw HTML blocks |
| `nl2br` | Single newlines become `<br>` tags |

---

## 7. CI/CD Deployment

### 7.1 deploy_site.yaml

**Trigger:** Push to `main` branch (when `docs/**`, `mkdocs.yaml`, `identity/**`, or `scripts/**` change)

**Steps:**
1. Checkout repository (`actions/checkout@v4`)
2. Install Python 3.12 (`actions/setup-python@v5`)
3. Install `uv`
4. `uv sync` — install project dependencies from `pyproject.toml`/`uv.lock`
5. `bash scripts/web_preprocessing.sh` — all 8 pre-processing scripts
6. `uv run mkdocs gh-deploy` — builds `site/` and pushes to `gh-pages` branch via `peaceiris/actions-gh-pages@v4`

The live site is deployed to: `https://digitalpalidictionary.github.io/dpd-pali-courses/`

### 7.2 release_class.yaml

**Trigger:** Manual dispatch or on release creation

Handles document export artifacts (PDFs, DOCX). Not covered in this analysis (website-only scope).

---

## 8. Local Development

### 8.1 What `pali-build-website` Does

The script `scripts/cl/pali-build-website`:
1. Resolves the project root directory
2. Runs `scripts/regenerate_pages.sh` — fetches the latest vocab/abbreviations content from the external `dpd-db` repository and writes it to `docs/generated/`
3. Runs `scripts/web_preprocessing.sh` — all 8 pre-processing scripts
4. Launches `uv run mkdocs serve` on `http://127.0.0.1:8000`

So the full local dev chain is: **regenerate external pages → preprocess → serve**.

### 8.2 What Triggers Live Reload vs Manual Restart

| Changed File | Dev Server Behavior |
|---|---|
| `docs/**/*.md` | Automatic live reload |
| `identity/*.css` | Automatic live reload |
| `identity/*.js` | Automatic live reload |
| `mkdocs.yaml` | Manual restart required |
| `tools/*.py` (hooks) | Manual restart required — hooks are loaded at startup |
| `scripts/*.py` (preprocessors) | No effect — must re-run preprocessing manually then restart |

---

## 9. mkdocs.yaml — Configuration Central

### 9.1 Core Settings

```yaml
docs_dir: docs          # Source Markdown files
site_dir: site          # Generated static HTML output
theme:
  name: material        # Material for MkDocs theme
  custom_dir: identity  # Overrides from identity/ folder
```

The `custom_dir: identity` setting tells Material to use `identity/` as a theme overlay directory. Any file in `identity/` that matches a theme template path overrides the built-in theme file.

### 9.2 Theme Features

```yaml
theme:
  features:
    - navigation.tabs         # First nav level becomes horizontal tab bar
    - navigation.tabs.sticky  # Tab bar stays visible while scrolling
    - navigation.top          # "Back to top" button
    - navigation.indexes      # Index pages act as section hubs (clickable + expandable)
    - content.code.copy       # Copy button on code blocks
```

### 9.3 CSS and JS Loading

```yaml
extra_css:
  - dpd.css           # Loaded 1st: content component styles
  - dpd-variables.css # Loaded 2nd: CSS custom properties
  - extra.css         # Loaded 3rd: theme overrides (must be last to take precedence)

extra_javascript:
  - footnotes.js       # Footnote tooltips, list correction, title linking
  - search_order.js    # Search result reordering
  - tablesort-all.js   # Table header sorting
  - theme-images.js    # Light/dark image swapping
```

These files are served from `identity/` (because `custom_dir: identity`).

### 9.4 Palette Configuration

```yaml
palette:
  - media: '(prefers-color-scheme: light)'
    scheme: default
    primary: brown
    accent: orange
    toggle:
      icon: material/brightness-7
      name: Switch to dark mode
  - media: '(prefers-color-scheme: dark)'
    scheme: slate
    primary: brown
    accent: orange
    toggle:
      icon: material/brightness-4
      name: Switch to light mode
```

This defines two named color schemes. Material uses `data-md-color-scheme="default"` or `"slate"` on `<body>` to switch between them. `extra.css` intercepts these attribute values to inject custom colors.

### 9.5 Hooks Registration

```yaml
hooks:
  - tools/footnote_hook.py
  - tools/nav_hook.py
```

---

## 10. Navigation Architecture — 4 Layers

The site uses four distinct and separate navigation mechanisms. Each has a different job.

### 10.1 Global Navigation (Tabs + Sidebar)

**Mechanism:** Direct output of MkDocs Material rendering the `nav:` tree from `mkdocs.yaml`.

- The first level of `nav:` becomes **horizontal tabs** in the header because `navigation.tabs` is enabled
- Deeper levels become a **hierarchical sidebar tree** (`<ul>` lists of `<a>` links)
- Clicking a leaf item navigates to that page (standard `<a href="...">`)
- Clicking a section node (e.g., "Lessons") expands its children in the sidebar
- Because `navigation.indexes` is enabled, section nodes that have an `index.md` are both navigable (clicking goes to the index page) AND expandable (shows children)
- No custom code is involved — this is entirely the Material theme rendering the nav config

**HTML structure produced by Material:**
```html
<nav class="md-tabs">
  <ul class="md-tabs__list">
    <li class="md-tabs__item">
      <a class="md-tabs__link" href="bpc/">Beginner Course (BPC)</a>
    </li>
  </ul>
</nav>

<nav class="md-nav md-nav--primary">
  <ul class="md-nav__list">
    <li class="md-nav__item md-nav__item--nested">
      <a class="md-nav__link">Lessons</a>
      <ul class="md-nav__list">...</ul>
    </li>
  </ul>
</nav>
```

### 10.2 Local Navigation (Prev/Next Buttons)

**Mechanism:** Generated at render time by `tools/nav_hook.py` in its `on_post_page()` hook.

**How it works:**
1. MkDocs maintains an internal ordered page list based on the `nav:` tree sequence
2. The hook reads `page.previous_page` and `page.next_page` from MkDocs' page object
3. Converts them to relative URLs using `get_relative_url(page_url, current_page_url)`
4. Constructs an HTML block and injects it before `</body>` in the final HTML output

**Generated HTML:**
```html
<div class="nav-links">
  <a href="../1_review/" class="prev">← Review</a>
  <a href="../3_decl_nouns/" class="next">Declension of Nouns →</a>
  ...
</div>
```

**Key detail:** The hook also strips any hardcoded `<div class="nav-links">` blocks from Markdown source in `on_page_markdown()` before rendering. This means if old nav blocks exist in source files, they are removed and regenerated fresh each build.

### 10.3 Context Navigation (Exercises + Feedback)

**Mechanism:** Also `tools/nav_hook.py`, injected in the same `<div class="nav-links">` block.

**Exercise cross-link:**
- The hook inspects the current page's source path
- If the path matches `bpc/class_(\d+)` or `ipc/class_(\d+)` (regex), it extracts the class number
- Constructs the exercise URL: `bpc_ex/{class_num}_class/` or `ipc_ex/{class_num}_class/`
- Appends: `<div class="cross"><a href="bpc_ex/2_class/">Go to Exercises</a></div>`

**Feedback link:**
- Constructs a Google Forms URL with pre-filled fields:
  - Course name (BPC or IPC), derived from path
  - Page path (e.g., `bpc/class_2/3_decl_nouns`)
- Appends: `<div class="feedback"><a href="https://docs.google.com/forms/d/e/...&entry.957833742=BPC&entry.390426412=bpc/class_2/3_decl_nouns" target="_blank">Provide feedback on this page</a></div>`

The logic is path-based, not heading-based. The exercise link appears automatically on any page matching the class path pattern.

### 10.4 In-Page Navigation (TOC + Heading Anchors)

**Mechanism:** MkDocs `toc` Markdown extension.

```yaml
markdown_extensions:
  - toc:
      permalink: true   # Adds § anchor link beside each heading
      baselevel: 2      # Shifts all source headings down by 1 level in HTML
```

**What this produces:**
- Each heading gets an `id` attribute generated from its text (slugified)
- A `<a class="headerlink" href="#slug">§</a>` link is appended to each heading
- The right-side TOC panel contains `<a href="#slug">` links to each heading

**`permalink: true` result:**
```html
<h2 id="course-structure">
  Course Structure
  <a class="headerlink" href="#course-structure" title="Permanent link">§</a>
</h2>
```

The TOC sidebar:
```html
<nav class="md-toc">
  <ul class="md-toc__list">
    <li class="md-toc__item">
      <a href="#course-structure" class="md-toc__link">Course Structure</a>
    </li>
  </ul>
</nav>
```

---

## 11. Heading Structure & TOC

### 11.1 Source Heading Levels

```
# Page Title      → one per file (h1 in Markdown, becomes h2 in HTML due to baselevel:2)
## Major Section  → main content sections
### Sub-section   → nested within sections
#### Rarely used
```

### 11.2 The baselevel:2 Shift

`toc: baselevel: 2` causes all headings to render one level lower in HTML:
- Source `#` → `<h2>` in HTML
- Source `##` → `<h3>` in HTML

**Why this matters:** MkDocs Material injects its own `<h1>` from the page title. Without the baselevel shift, source `#` headings would conflict with the theme's `<h1>`, creating duplicate H1 elements.

### 11.3 H1 Hidden in CSS

`identity/extra.css` hides `.md-content h1`:
```css
.md-content h1 { display: none; }
```

This means:
- MkDocs still generates the semantic H1 (for metadata and accessibility)
- The browser does not display the duplicated visual H1 at the top of content
- The page heading comes from the TOC/title system, not from a visible `<h1>` in the body

### 11.4 Heading Normalization Script

`fix_heading_hierarchy.py` runs before MkDocs and does:
1. **Bold-to-heading conversion**: If the first non-empty line is `**Class 1**`, converts it to `# Class 1`
2. **Level continuity enforcement**: If a page skips levels (e.g., `#` → `###`), the skipped level is reduced to make the sequence continuous (no gaps)

---

## 12. Identity Folder: CSS Architecture

### 12.1 Three-File CSS System

The CSS is split across three files loaded in this order:

| File | Role | Scope |
|------|------|-------|
| `dpd.css` | Content component styles | Styles for tables, buttons, and DPD-specific inline elements inside articles |
| `dpd-variables.css` | CSS custom properties | `:root` variables: colors, shadows, frequency heatmap scale |
| `extra.css` | Material theme overrides | Shell layout, dark/light mode color remapping, header, typography, print |

**Why this order:** `extra.css` loads last and has the highest specificity, allowing it to override both the content styles and Material's default rules.

### 12.2 dpd-variables.css — Color Source of Truth

Defines all CSS custom properties used across the site. Changing a color here propagates everywhere without touching other files.

```css
:root {
  /* Mode backgrounds */
  --light: hsl(198, 100%, 95%);
  --dark:  hsl(198, 100%, 5%);

  /* Primary accent (blue) */
  --primary:     hsl(198, 100%, 50%);
  --primary-alt: hsl(205, 100%, 40%);
  --primary-text: hsl(205, 79%, 48%);

  /* Box shadows */
  --shadow-default: 2px 2px 4px hsla(0, 0%, 20%, 0.4);
  --shadow-hover:   2px 2px 4px hsla(0, 0%, 20%, 0.5);

  /* Grayscale */
  --gray:             hsl(0, 0%, 50%);
  --gray-light:       hsl(0, 0%, 75%);
  --gray-dark:        hsl(0, 0%, 25%);
  --gray-transparent: hsla(0, 0%, 50%, 0.25);

  /* Secondary accent (green — used for help sections) */
  --secondary: hsl(158, 100%, 35%);

  /* Frequency heatmap (0 = transparent, 10 = strong color) */
  --freq0:  hsla(198, 90%, 50%, 0.1);
  --freq1:  hsla(200, 90%, 50%, 0.2);
  --freq2:  hsla(202, 90%, 50%, 0.3);
  /* ... through --freq10 */
}
```

### 12.3 dpd.css — Content Components

This file styles the **objects inside article content**, not the page shell. Key components:

**DPD Box** (`div.dpd`) — framed block with primary-color border:
```css
div.dpd {
  border: 2px solid var(--primary);
  border-radius: 7px;
  padding: 3px 7px;
}
```

**DPD Button** (`a.dpd-button`):
```css
a.dpd-button {
  background-color: var(--primary);
  border: 1px solid var(--primary);
  border-radius: 7px;
  color: var(--dark);
  cursor: pointer;
  display: inline-block;
  font-size: 80%;
  padding: 2px 5px;
  text-decoration: none;
  box-shadow: var(--shadow-default);
}
a.dpd-button:hover {
  box-shadow: var(--shadow-hover);
  border: 1px solid var(--primary-alt);
  background-color: var(--primary-alt);
  color: var(--light);
}
```

**Play Button** (`a.dpd-button.play`) — inline flex with SVG icon:
```css
a.dpd-button.play {
  display: inline-flex;
  justify-content: center;
  align-items: center;
}
a.dpd-button.play svg {
  width: 1em; height: 1em;
  fill: var(--dark); stroke: var(--dark);
}
```

**Small Play Button** (`a.dpd-button.play.small`) — circular:
```css
a.dpd-button.play.small {
  width: 1.1em; height: 1.1em;
  border-radius: 50%;
  background-color: var(--dark);
  border: 1px solid var(--dark);
}
```

**CSS-only Tooltip** (via `data-title` attribute):
```css
[data-title]:hover::after {
  content: attr(data-title);
  position: absolute;
  bottom: 125%;
  background-color: var(--primary);
  /* ... */
}
```

**Custom heading style** (`p.heading`):
```css
p.heading {
  margin: 0px 0px;
  padding: 2px 0px;
}
```

**Table classes defined in dpd.css:**
- `.inflection` — Verb/noun paradigm tables
- `.grammar` — Grammar reference tables
- `.grammar_dict` — Dictionary-style grammar entries
- `.family` — Word family tables
- `.root_info` — Verbal root information
- `.root_matrix` — Root grouping matrix
- `.variants` — Variant form tables
- `.freq` — Frequency heatmap tables
- `.sutta_link` — Sutta cross-reference links
- `.sutta-info` — Sutta metadata tables
- `.button-box` — Container for action button groups

### 12.4 extra.css — Material Theme Override Layer

This is the most powerful CSS file in the project. It overrides Material's shell-level behavior.

**Dark/Light mode color remapping:**
```css
[data-md-color-scheme="default"] {
  --md-primary-fg-color: var(--primary);
  --md-default-bg-color: var(--light);
  /* ... overrides all Material color variables */
}
[data-md-color-scheme="slate"] {
  --md-primary-fg-color: var(--primary);
  --md-default-bg-color: var(--dark);
  /* ... */
}
```
Material provides the scheme toggle mechanism; `extra.css` fills in the actual palette values.

**Logo per theme (CSS content swap):**
```css
[data-md-color-scheme="default"] .md-logo img {
  content: url("../assets/dpd-logo.svg");
  background-color: var(--light);
  padding: 1px;
  border-radius: 50%;
}
[data-md-color-scheme="slate"] .md-logo img {
  content: url("../assets/dpd-logo-dark.svg");
  background-color: var(--dark);
  padding: 1px;
  border-radius: 50%;
}
```

**Compressed header (26px):**
```css
.md-header { height: 26px; }
```
Design choice: minimize chrome, maximize content viewport.

**Typography scale:**
```css
.md-typeset { font-size: 1rem; }
```
Larger than Material's default (~0.8rem) for readability of educational content.

**H1 suppression:**
```css
.md-content h1 { display: none; }
```

**Full-width tables:**
```css
.md-typeset table:not([class]),
.md-typeset table.grammar,
.md-typeset table.inflection {
  width: 100% !important;
  display: table !important;
  table-layout: auto !important;
  border-collapse: collapse !important;
  border-top: 1px solid var(--gray) !important;
  border-bottom: 1px solid var(--gray) !important;
}
```

**Hidden table headers** (for content-only tables):
```css
.md-typeset table.no-header thead { display: none !important; }
```

**Nav-links block layout:**
```css
.nav-links {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  margin-top: 2em;
  padding-top: 1em;
  border-top: 1px solid var(--md-default-fg-color--lightest);
}
.nav-links .prev { margin-right: auto; }
.nav-links .next { margin-left: auto; text-align: right; }
.nav-links .cross,
.nav-links .feedback { width: 100%; text-align: center; margin-top: 1em; }
.nav-links a { color: var(--md-typeset-a-color); text-decoration: none; }
.nav-links a:hover { color: var(--md-accent-fg-color); text-decoration: underline; }
```

**Image styling:**
```css
/* Framed standalone images */
.md-typeset p:has(> img:only-child) { text-align: center; }
.md-typeset p:has(> img:only-child) img {
  display: block !important;
  max-width: 90% !important;
  margin: 0 auto !important;
}

/* Inline grammar symbol images */
img[src*="pacman"], img[src*="arrow"] {
  display: inline-block !important;
  height: 1.5em !important;
  width: auto !important;
  vertical-align: middle !important;
  margin: 0 0.2em !important;
}
```

**Footnote tooltip CSS (screen media):**
```css
@media screen {
  .footnote, .footnotes, .manual-fn-def { display: none; }
  .footnote-wrapper { position: relative; display: inline-block; }
  .footnote-tooltip {
    visibility: hidden;
    position: absolute;
    background-color: var(--light-shade);
    border: 1px solid var(--primary);
    border-radius: 6px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    width: max-content;
    max-width: 350px;
    z-index: 1000;
  }
  .footnote-tooltip::after {
    content: "";
    position: absolute;
    top: 100%;
    left: 50%;
    border-width: 5px;
    border-style: solid;
    border-color: var(--primary) transparent transparent transparent;
  }
}
```

---

## 13. Identity Folder: JavaScript

### 13.1 footnotes.js

This is the most complex client-side file. It runs on `DOMContentLoaded` and has **four distinct responsibilities**:

#### Responsibility 1: Footnote Tooltip System

For each `sup.manual-fn-ref` element on the page:
1. Finds the matching `div.manual-fn-def` by comparing `data-fn` attribute values
2. Wraps the `<sup>` in a `span.footnote-wrapper`
3. Creates a `div.footnote-tooltip` populated with the footnote content (number + text)
4. Binds `mouseenter` → show tooltip, `mouseleave` → hide tooltip

**Positioning algorithm (runtime layout):**
- Measures the reference element's position (`getBoundingClientRect()`)
- Measures the tooltip's size
- If tooltip would overflow the top of the viewport, adds class `.tooltip-bottom` and positions it below the reference instead of above
- This is an explicit runtime spatial calculation, not just a CSS hover effect

#### Responsibility 2: List Numbering Correction (Browser-side Fallback)

Iterates over all `.manual-list-start` elements (inserted by `footnote_hook.py`):
```javascript
document.querySelectorAll(".manual-list-start").forEach(marker => {
  const startVal = marker.getAttribute("data-start");
  let next = marker.nextElementSibling;
  while (next && next.tagName !== "OL") {
    next = next.nextElementSibling;
  }
  if (next && next.tagName === "OL") {
    next.setAttribute("start", startVal);
  }
});
```
This is a fallback that reinforces the Python-side `on_post_page()` correction, ensuring the `start` attribute is always set correctly even if the BeautifulSoup pass misses an edge case.

#### Responsibility 3: Clickable Site Title

Material already makes the logo clickable. This code also makes the text title clickable:
```javascript
const logoLink = document.querySelector("a.md-header__button.md-logo");
const titleEllipsis = document.querySelector(".md-header__title .md-ellipsis");
if (titleEllipsis && logoLink) {
  const link = document.createElement("a");
  link.href = logoLink.href;  // copies homepage URL from the logo link
  link.style.cssText = "color:inherit;text-decoration:none;cursor:pointer;";
  titleEllipsis.parentNode.replaceChild(link, titleEllipsis);
  link.appendChild(titleEllipsis);
}
```
This is DOM surgery performed after Material has rendered the header. It is not achievable by changing `mkdocs.yaml` or the Markdown source.

### 13.2 search_order.js

**Mechanism:** Uses a `MutationObserver` to watch for search result DOM changes. When search results are injected into the DOM by MkDocs' Lunr.js search, the observer fires and re-sorts the result list.

**Priority order:**
1. `bpc/` (lesson content — highest priority)
2. `ipc/` (lesson content)
3. `bpc_key/` (answer keys)
4. `ipc_key/` (answer keys)

The sort is purely presentational — it does not change the underlying relevance scores. It ensures that if a query matches both a lesson and its answer key, the lesson appears first.

### 13.3 tablesort-all.js

Integrates the **Tablesort** library, attaching it to every table in the article:
```javascript
document$.subscribe(function() {
  var tables = document.querySelectorAll("article table");
  tables.forEach(function(table) {
    new Tablesort(table);
  });
});
```

- Makes all `<th>` headers clickable for sorting
- Supports numeric sorting (currency, percentages) via Tablesort's number plugin
- To disable sorting on a specific column: `data-sort-method="none"` attribute on the `<th>`
- Uses `document$.subscribe` (Material's RxJS observable) to re-initialize after client-side navigation

### 13.4 theme-images.js

**Mechanism:** Uses a `MutationObserver` on `document.body` watching for `data-md-color-scheme` attribute changes.

```javascript
function applyTheme(scheme) {
  var dark = scheme === 'slate';
  document.querySelectorAll('img[src]').forEach(function(img) {
    var src = img.getAttribute('src');
    if (!src) return;
    if (dark && src.endsWith('-b.png')) {
      img.setAttribute('src', src.slice(0, -6) + '-d.png');
    } else if (!dark && src.endsWith('-d.png')) {
      img.setAttribute('src', src.slice(0, -6) + '-b.png');
    }
  });
}
```

**Convention:** Image filenames ending `-b.png` = bright/light mode; `-d.png` = dark mode. When the theme switches, all matching images are swapped in place without a page reload.

---

## 14. Footnote System — End to End

The footnote system is custom because the standard MkDocs/Markdown footnote output doesn't provide enough control for three requirements: (1) stable source numbers, (2) hover tooltips on the web, (3) float footnotes for PDF rendering.

### 14.1 Source Syntax

Standard Markdown footnote syntax:
```markdown
The lion eats the disciple.[^1]

[^1]: This is the footnote definition.
```

### 14.2 Pre-Processing (renumber_footnotes.py)

Before MkDocs sees the files, `renumber_footnotes.py` ensures all footnotes are numbered sequentially across the entire course in reading order. This happens in `web_preprocessing.sh`.

### 14.3 Hook Pre-Processing (footnote_hook.py → on_page_markdown)

The hook intercepts the raw Markdown string before MkDocs processes it:

**Footnote references** `[^1]` → raw HTML:
```html
<sup class='manual-fn-ref' data-fn='1'>1</sup>
```

**Footnote definitions** `[^1]: text` → raw HTML:
```html
<div class='manual-fn-def' data-fn='1' markdown='1'>text</div>
```

These are injected as raw HTML so MkDocs passes them through unchanged instead of processing them as Markdown footnotes.

### 14.4 HTML Rendering

The `<sup>` and `<div>` markers pass through MkDocs' Markdown extensions unchanged and appear in the final HTML. The `div.manual-fn-def` elements are hidden by `extra.css` (`.manual-fn-def { display: none; }`).

### 14.5 Client-Side Tooltip Generation (footnotes.js)

On `DOMContentLoaded`:
1. Finds all `sup.manual-fn-ref` elements
2. For each, locates `div.manual-fn-def[data-fn="N"]` with matching number
3. Wraps `<sup>` in `<span class="footnote-wrapper">`
4. Creates `<div class="footnote-tooltip">` with content: `<b>N.</b> [definition text]`
5. On `mouseenter`: measures positions, chooses above/below placement, makes tooltip visible
6. On `mouseleave`: hides tooltip

### 14.6 Why the Duplication Between Python and JS

- Python (`footnote_hook.py`) converts syntax before HTML is generated — necessary for the static HTML to contain the right marker structure
- JavaScript (`footnotes.js`) handles the tooltip behavior at browser runtime — can't be done statically
- The separation allows the same markers to be used by the PDF pipeline for a different rendering path

---

## 15. List Numbering System

### 15.1 The Problem

Markdown parsers restart ordered list numbering when lists are interrupted by block elements (tables, code blocks, horizontal rules):
```markdown
1. First item
2. Second item

| Table | Here |
|---|---|

3. Third item    ← Markdown parser resets this to "1."
```

### 15.2 Three-Layer Solution

**Layer 1 — Marker Insertion (footnote_hook.py → on_page_markdown):**

Detects `N. ` pattern at line start, inserts a marker before it:
```html
<div class='manual-list-start' data-start='3'></div>

3. Third item
```

**Layer 2 — HTML Correction (footnote_hook.py → on_post_page):**

After MkDocs renders HTML, uses BeautifulSoup:
1. Finds each `div.manual-list-start` marker
2. Finds the next `<ol>` sibling element
3. Sets `<ol start="3">` attribute
4. Hides the marker div (`style="display:none"`)

**Layer 3 — Browser Fallback (footnotes.js):**

Repeats the correction in the browser for any cases the Python pass missed:
```javascript
document.querySelectorAll(".manual-list-start").forEach(marker => {
  const startVal = marker.getAttribute("data-start");
  let next = marker.nextElementSibling;
  while (next && next.tagName !== "OL") next = next.nextElementSibling;
  if (next?.tagName === "OL") next.setAttribute("start", startVal);
});
```

The duplication is intentional: Python handles the static HTML, JavaScript handles any browser-rendering edge cases.

---

## 16. Table System

### 16.1 Table Types

| CSS Class | Name | Behavior |
|-----------|------|----------|
| (none / default) | Standard | Full-width, bordered top/bottom, sortable |
| `.grammar` | Grammar | No outer border, bold label column |
| `.grammar_dict` | Dictionary grammar | Minimal padding, no borders |
| `.inflection` | Paradigm table | Rounded cell corners, header row highlighted |
| `.freq` | Frequency heatmap | Color-coded cells by frequency grade |
| `.sutta-info` | Sutta metadata | No border, left-aligned labels |
| `.family` | Word family | Compact display |
| `.root_info` | Root information | Root-specific layout |
| `.root_matrix` | Root matrix | Grouped root display |
| `.variants` | Variant forms | Minimal |
| `.no-header` | Headerless table | `thead` hidden via `display: none !important` |

### 16.2 Inflection Table CSS

```css
table.inflection {
  border-radius: 7px;
  border-collapse: separate;
}
table.inflection td, table.inflection th {
  border-radius: 7px;
  border: 1px solid var(--gray);
}
table.inflection tr:first-child th:first-child {
  border-top-left-radius: 7px;
}
```

### 16.3 Frequency Heatmap Table CSS

Cells are styled with CSS variables from `dpd-variables.css`:
```css
table.freq td.gr0 { border-color: var(--freq0); color: transparent; }
table.freq td.gr1 { background-color: var(--freq1); border-color: var(--freq1); }
table.freq td.gr2 { background-color: var(--freq2); border-color: var(--freq2); }
/* ... through gr10 */
```

### 16.4 Pre-Processing: fixing_tables.py

Runs before MkDocs. Normalizes:
- Cell padding (consistent whitespace around `|`)
- Separator rows (`|---|---|` formatting)
- Strips extra whitespace

### 16.5 Hook: Empty Cell Injection (footnote_hook.py)

During `on_page_markdown()`, the hook injects `&nbsp;` into empty Markdown table cells to prevent rendering artifacts in the HTML output.

### 16.6 Sortable Tables (tablesort-all.js)

Every `<th>` in every `article table` gets a click listener via Tablesort. No per-table configuration needed. To opt out of sorting on a specific column, add `data-sort-method="none"` to its `<th>`.

---

## 17. Images & Theme Awareness

### 17.1 Image Storage

All images: `docs/assets/images/`

Known image files and their purpose:
- `arrow.png` — Navigation/direction indicator (used inline in grammar explanations)
- `pacman-forward.png` / `pacman-backwards.png` — Grammar direction markers (used inline)
- `kahapana.png` — Currency illustration
- `anki/*.png` — Anki deck screenshots (for Anki documentation pages)

### 17.2 Light/Dark Image Convention

Images that need to change appearance between light and dark mode use a suffix convention:
- `*-b.png` = bright (light mode) version
- `*-d.png` = dark (dark mode) version

`theme-images.js` swaps `src` attributes automatically when the color scheme changes. The same Markdown source works for both modes — no conditional markup needed.

### 17.3 Inline Images

Grammar symbol images (`pacman`, `arrow`) must render inline alongside text. `extra.css` enforces this:
```css
img[src*="pacman"], img[src*="arrow"] {
  display: inline-block !important;
  height: 1.5em !important;
  width: auto !important;
  vertical-align: middle !important;
  margin: 0 0.2em !important;
}
```

### 17.4 Standalone Images

When an image is the only child of a paragraph, `extra.css` centers and constrains it:
```css
@media screen {
  .md-typeset p:has(> img:only-child) { text-align: center; }
  .md-typeset p:has(> img:only-child) img {
    display: block !important;
    max-width: 90% !important;
    margin: 0 auto !important;
  }
}
```

---

## 18. Dark/Light Mode Mechanics

### 18.1 Toggle Mechanism (Material Theme)

1. `mkdocs.yaml` defines two named palettes (`default` = light, `slate` = dark)
2. Material renders two radio `<input>` elements and a toggle button (sun/moon icon) in the header
3. Clicking the toggle flips which radio is checked
4. Material's JavaScript updates `data-md-color-scheme` on `<body>` to `"default"` or `"slate"`
5. User preference is stored in `localStorage`

**HTML structure:**
```html
<input class="md-option" data-md-color-scheme="default" id="__palette_0" name="__palette" type="radio">
<label class="md-header__button md-icon" for="__palette_1" title="Switch to dark mode">...icon...</label>
<input class="md-option" data-md-color-scheme="slate" id="__palette_1" name="__palette" type="radio">
```

### 18.2 CSS Response (extra.css)

`extra.css` uses attribute selectors to remap Material's CSS custom properties:
```css
[data-md-color-scheme="default"] {
  --md-primary-fg-color: var(--primary);
  --md-default-bg-color: var(--light);
  /* ... all Material vars overridden */
}
[data-md-color-scheme="slate"] {
  --md-primary-fg-color: var(--primary);
  --md-default-bg-color: var(--dark);
  /* ... */
}
```

### 18.3 Logo Swap (extra.css)

The logo file itself changes via CSS `content` property:
```css
[data-md-color-scheme="default"] .md-logo img {
  content: url("../assets/dpd-logo.svg");
}
[data-md-color-scheme="slate"] .md-logo img {
  content: url("../assets/dpd-logo-dark.svg");
}
```

### 18.4 Image Swap (theme-images.js)

A `MutationObserver` watches `document.body` for `data-md-color-scheme` attribute mutations. On change, it scans all `img[src]` elements and swaps `-b.png` ↔ `-d.png` in place.

---

## 19. Generated Content

### 19.1 Vocabulary Pages

Generated by `scripts/export/vocab_abbrev_pali_course.py` (from the external `dpd-db` repository). Output: one Markdown file per class in `docs/generated/vocab/` (e.g., `class-02.md` through `class-29.md`). Each contains vocabulary tables with frequency data used to produce `.freq` heatmap tables.

This generation runs via `scripts/regenerate_pages.sh` (called by `pali-build-website` for local dev).

### 19.2 Abbreviations Page

Also generated by `vocab_abbrev_pali_course.py`. Output: `docs/generated/abbreviations.md`. Referenced in `mkdocs.yaml` under Reference → Abbreviations.

### 19.3 Class Index Pages (generate_indexes.py)

The class hub pages (`docs/bpc/class_N/index.md`) and section hubs (`docs/bpc/index.md`, etc.) are all generated, not hand-curated.

**How class index pages are generated:**
1. Script scans each `class_*` folder
2. Reads the first heading from each file (`get_first_heading()`)
3. Skips "review", "homework", and "index/title/literature" pages via `should_skip_in_main_index()`
4. Writes an `index.md` with a link list using semantic page titles (not filenames) as link text
5. Special-cases class index pages for prev/next: a class index links to the previous/next class index, not the surrounding individual lesson pages

### 19.4 MkDocs YAML Nav (generate_mkdocs_yaml.py)

The entire `nav:` section of `mkdocs.yaml` is regenerated on each preprocessing run. It is not hand-maintained.

---

## 20. Complete Request-Response Cycle

When a user visits a page (e.g., "The Alphabet & Pronunciation"):

1. Browser requests `/bpc/class_2/2_alphabet/index.html` from GitHub Pages CDN
2. GitHub Pages serves the pre-built static HTML file
3. Browser parses HTML and loads:
   - Material theme CSS (from CDN or bundled)
   - `dpd-variables.css`, `dpd.css`, `extra.css` (from `identity/`)
4. Browser renders the page — Material's CSS applies layout, custom CSS applies overrides
5. `DOMContentLoaded` fires — JavaScript executes:
   - `footnotes.js`: scans for `sup.manual-fn-ref`, builds tooltip wrappers, corrects list numbering, wraps site title
   - `tablesort-all.js`: attaches Tablesort to all `article table` elements
   - `theme-images.js`: initializes `MutationObserver` on `body`, applies current scheme to images
   - `search_order.js`: initializes `MutationObserver` on search result container
6. Page is fully interactive

**Annotated HTML skeleton of a rendered page:**
```html
<html>
<head>
  <link href="../../dpd-variables.css" rel="stylesheet">
  <link href="../../dpd.css" rel="stylesheet">
  <link href="../../extra.css" rel="stylesheet">
</head>
<body data-md-color-scheme="default">

  <!-- Header: logo (clickable), title (JS-made clickable), search, dark mode toggle -->
  <header class="md-header" style="height:26px;">
    <a class="md-header__button md-logo" href="../../../">...</a>
    <div class="md-header__title">
      <div class="md-ellipsis">DPD Pāḷi Courses</div>  <!-- JS wraps this in <a> -->
    </div>
    <div class="md-search">...</div>
  </header>

  <!-- Horizontal navigation tabs -->
  <nav class="md-tabs">
    <ul class="md-tabs__list">
      <li class="md-tabs__item">
        <a class="md-tabs__link" href="../../../bpc/">Beginner Course (BPC)</a>
      </li>
    </ul>
  </nav>

  <!-- Sidebar tree -->
  <nav class="md-nav md-nav--primary">
    <ul class="md-nav__list">...</ul>
  </nav>

  <!-- Main content area -->
  <main class="md-main">
    <article class="md-content__inner md-typeset">
      <!-- h1 hidden by CSS, h2+ from baselevel:2 shift -->
      <h1 style="display:none">The Alphabet & Pronunciation</h1>
      <h2 id="overview">Overview
        <a class="headerlink" href="#overview">§</a>
      </h2>
      <p>...</p>
      <table class="inflection">...</table>
      <!-- Footnote reference (from footnote_hook.py) -->
      <sup class="manual-fn-ref" data-fn="2">2</sup>
      <!-- Hidden footnote definition (shown as JS tooltip) -->
      <div class="manual-fn-def" data-fn="2" style="display:none">...</div>
    </article>
  </main>

  <!-- Navigation buttons (injected by nav_hook.py) -->
  <div class="nav-links">
    <a href="../1_review/" class="prev">← Review</a>
    <a href="../3_decl_nouns/" class="next">Declension of Nouns →</a>
    <div class="cross"><a href="../../../../bpc_ex/2_class/">Go to Exercises</a></div>
    <div class="feedback">
      <a href="https://docs.google.com/forms/d/e/...&entry.957833742=BPC&entry.390426412=bpc/class_2/2_alphabet"
         target="_blank">Provide feedback on this page</a>
    </div>
  </div>

  <!-- Client-side scripts -->
  <script src="../../footnotes.js"></script>
  <script src="../../search_order.js"></script>
  <script src="../../tablesort-all.js"></script>
  <script src="../../theme-images.js"></script>
</body>
</html>
```

---

## 21. How Every Clickable Element Works

| Element | Mechanism | Where It's Created |
|---------|-----------|-------------------|
| Top navigation tabs | Material theme renders first-level `nav:` entries as `<a>` in `.md-tabs__list` | `mkdocs.yaml` nav + Material |
| Sidebar nav items | Material renders full `nav:` tree as nested `<ul><li><a>` | `mkdocs.yaml` nav + Material |
| Section index pages (expandable + navigable) | `navigation.indexes` feature: index pages act as both link target and expander | `mkdocs.yaml` feature flag |
| Prev/Next page buttons | `nav_hook.py` injects `<a class="prev/next">` in `on_post_page()` from `page.previous_page`/`page.next_page` | `tools/nav_hook.py` |
| Go to Exercises link | `nav_hook.py` detects `bpc/class_N` path regex, constructs `bpc_ex/N_class/` URL | `tools/nav_hook.py` |
| Feedback link | `nav_hook.py` builds Google Forms URL with pre-filled course + page fields | `tools/nav_hook.py` |
| In-page TOC links | `toc` extension generates `#slug` href for each heading in right-side panel | `mkdocs.yaml` toc extension |
| Heading permalink (§) | `toc: permalink: true` adds `<a class="headerlink" href="#slug">` beside each heading | `mkdocs.yaml` toc extension |
| Table sort headers | `tablesort-all.js` attaches Tablesort `click` listener to every `<th>` in `article table` | `identity/tablesort-all.js` |
| Dark/light mode toggle | Material's built-in toggle button switches `data-md-color-scheme` on `<body>` | Material theme |
| Footnote tooltips | `footnotes.js` creates tooltip `<div>` on `mouseenter`, removes on `mouseleave` | `identity/footnotes.js` |
| Site title | `footnotes.js` wraps `.md-header__title .md-ellipsis` in `<a href="/">` on `DOMContentLoaded` | `identity/footnotes.js` |
| Logo | Material theme renders `<a class="md-header__button md-logo">` pointing to site root | Material theme |
| Search input | Material's built-in Lunr.js search, activated by clicking search box or pressing `/` | Material theme + `plugins: [search]` |

---

## 22. What is Authored vs Generated vs Transformed

### Authored directly in `docs/`
- Lesson content (text, explanations, examples)
- Grammar tables and exercises
- Answer keys
- Landing pages (`about.md`, `downloads.md`, etc.)
- Anki documentation pages

### Generated before build (by pre-processing scripts)
- `mkdocs.yaml` `nav:` section — regenerated by `generate_mkdocs_yaml.py` from filesystem
- Section index pages (`docs/bpc/index.md`, etc.) — written by `generate_indexes.py`
- Class hub pages (`docs/bpc/class_N/index.md`) — written by `generate_indexes.py`
- Vocabulary pages (`docs/generated/vocab/`) — from external `dpd-db` repo
- Abbreviations page (`docs/generated/abbreviations.md`) — from external `dpd-db` repo
- Footnote numbering (repaired in-place by `renumber_footnotes.py`)
- Heading hierarchy (repaired in-place by `fix_heading_hierarchy.py`)
- Dead link removal (by `clean_dead_links.py`)

### Generated during MkDocs rendering (build-time)
- All HTML pages in `site/`
- TOC heading anchors (IDs and permalink links)
- Material theme shell (header, sidebar, tabs, TOC panel)
- Code copy buttons
- Search index (`search/search_index.json`)
- Prev/Next/Exercise/Feedback navigation blocks (by `nav_hook.py`)
- List `start` attribute corrections (by `footnote_hook.py` + BeautifulSoup)

### Generated/activated after HTML loads (client-side, browser runtime)
- Footnote tooltip wrappers and hover behavior (`footnotes.js`)
- List numbering browser-side fallback (`footnotes.js`)
- Clickable site title (`footnotes.js`)
- Table sorting behavior (`tablesort-all.js`)
- Theme-aware image swapping (`theme-images.js`)
- Search result priority ordering (`search_order.js`)
- Dark/light mode state (Material JS + `localStorage`)

---

## 23. Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                        SOURCE MATERIALS                          │
│  docs/bpc/*.md   docs/ipc/*.md   docs/generated/*.md             │
│  docs/bpc_ex/*.md  docs/ipc_ex/*.md  docs/about.md  etc.        │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                   PRE-PROCESSING PIPELINE                        │
│                  (scripts/web_preprocessing.sh)                  │
│                                                                  │
│  1. generate_mkdocs_yaml.py  → Regenerates mkdocs.yaml nav       │
│  2. check_renumber.py        → Fixes ordered list numbering      │
│  3. renumber_footnotes.py    → Sequential footnote numbers       │
│  4. clean_dead_links.py      → Removes broken links              │
│  5. fix_heading_hierarchy.py → Normalizes heading levels         │
│  6. fixing_tables.py         → Cleans table formatting           │
│  7. generate_indexes.py      → Creates index.md pages            │
│  8. update_css.py            → Syncs CSS variables               │
│                                                                  │
│  NOTE: Scripts mutate docs/ source files in place                │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                       MKDOCS BUILD                               │
│                   (uv run mkdocs build)                          │
│                                                                  │
│  Per-page pipeline:                                              │
│   ├── footnote_hook.py (on_page_markdown)                        │
│   │     [^N] → <sup manual-fn-ref>                              │
│   │     [^N]: → <div manual-fn-def>                             │
│   │     N. → <div manual-list-start>                            │
│   ├── nav_hook.py (on_page_markdown)                             │
│   │     strips hardcoded nav-links from MD source               │
│   ├── Markdown Extensions                                        │
│   │     toc, tables, attr_list, pymdownx, nl2br                 │
│   ├── Material Theme Templates                                   │
│   │     header, sidebar, tabs, TOC panel, footer                │
│   ├── nav_hook.py (on_post_page)                                 │
│   │     injects nav-links: prev, next, exercises, feedback      │
│   └── footnote_hook.py (on_post_page)                           │
│         BeautifulSoup: sets <ol start="N">                      │
│                                                                  │
│  Output: site/**/*.html + site/assets/**                         │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                       DEPLOYMENT                                 │
│              (.github/workflows/deploy_site.yaml)               │
│  Push to main → GitHub Actions → gh-pages branch → GitHub Pages │
│  Live: https://digitalpalidictionary.github.io/dpd-pali-courses/ │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                   BROWSER RUNTIME (CLIENT-SIDE)                  │
│                  identity/*.css + identity/*.js                  │
│                                                                  │
│  CSS:                                                            │
│   ├── dpd-variables.css  color variables                        │
│   ├── dpd.css            content components                     │
│   └── extra.css          Material theme overrides               │
│                                                                  │
│  JS (on DOMContentLoaded):                                       │
│   ├── footnotes.js       tooltip system + list fix + title link  │
│   ├── tablesort-all.js   sortable table headers                 │
│   ├── theme-images.js    light/dark image swap (MutationObserver)│
│   └── search_order.js    search result reordering (MutationObserver)│
└──────────────────────────────────────────────────────────────────┘
```

---

## 24. Limitations & Risks

### 24.1 Path-Convention Dependency

The nav generation, cross-link detection, and exercise URL construction all assume specific folder naming patterns:
- `bpc/class_N` and `ipc/class_N` for lessons
- `bpc_ex/N_class` and `ipc_ex/N_class` for exercises

If the folder structure is renamed or reorganized, these regex-based path assumptions in `nav_hook.py` and `generate_mkdocs_yaml.py` will break or produce wrong URLs.

### 24.2 Regex-Based Markdown Pre-Processing is Fragile

`footnote_hook.py` uses regex to detect footnote patterns and list numbers in raw Markdown. If source files use unusual formatting (e.g., footnote references inside code blocks, or numbered items that aren't list items), the patterns may over-match or under-match.

### 24.3 Site Title Clickability is DOM Surgery

The title link in `footnotes.js` is created by replacing a DOM node after Material has rendered the page. It relies on Material's internal CSS class names (`.md-header__title`, `.md-ellipsis`). If Material for MkDocs changes its HTML structure in a future version, this code will silently stop working.

### 24.4 `extra.css` Has Wide Blast Radius

`extra.css` simultaneously handles:
- Color theme definitions
- Layout (header height, content width)
- Typography scale
- Table behavior
- Navigation block styling
- Print/PDF layout

Changes to `extra.css` affect the entire site. There is no isolation between concerns.

### 24.5 Search Ordering is Presentation-Only

`search_order.js` reorders results in the DOM but does not affect the underlying Lunr.js relevance scores. If Material changes how it injects search results into the DOM, the `MutationObserver` callback may fire at the wrong time or observe the wrong node.

### 24.6 Build Scripts Mutate Source Files

Several pre-processing scripts rewrite `.md` files in `docs/` in place. This means:
- Running preprocessing twice is not always idempotent (e.g., renumbering footnotes)
- The order of scripts matters and cannot be changed without testing
- A bug in a preprocessing script can corrupt source content

### 24.7 Hook Changes Require Dev Server Restart

`tools/footnote_hook.py` and `tools/nav_hook.py` are loaded at MkDocs startup. The live dev server's file watcher does not reload hooks. This creates a gap between the edit-reload cycle for hooks vs. content files.

---

## 25. Master File Map

| Path | Role |
|------|------|
| `mkdocs.yaml` | Site configuration: nav, theme features, extensions, hooks, CSS/JS assets |
| `docs/` | All Markdown source content |
| `docs/bpc/class_N/` | BPC lesson folders (class_1 through class_14) |
| `docs/ipc/class_N/` | IPC lesson folders (class_16 through class_28) |
| `docs/bpc_ex/` | BPC exercise files (1_class.md through 15_class.md) |
| `docs/ipc_ex/` | IPC exercise files (16_class.md through 29_class.md) |
| `docs/bpc_key/`, `docs/ipc_key/` | Answer key files |
| `docs/generated/vocab/` | Generated per-class vocabulary pages |
| `docs/generated/abbreviations.md` | Generated abbreviations reference |
| `docs/assets/images/` | All image assets (including `-b.png`/`-d.png` theme pairs) |
| `identity/dpd-variables.css` | CSS custom property definitions — color/shadow source of truth |
| `identity/dpd.css` | Content component styles: tables, buttons, tooltips, DPD-specific elements |
| `identity/extra.css` | Material theme shell overrides: dark/light mode, layout, header, typography, print |
| `identity/dpd-pdf-fonts.css` | PDF-specific font definitions |
| `identity/footnotes.js` | Footnote tooltip system, list numbering correction, site title linking |
| `identity/search_order.js` | Search result priority reordering (MutationObserver) |
| `identity/tablesort-all.js` | Attaches Tablesort library to all article tables |
| `identity/theme-images.js` | Swaps `-b.png`/`-d.png` image variants on scheme change (MutationObserver) |
| `tools/footnote_hook.py` | MkDocs hook: converts footnotes/lists to protected markers; fixes `<ol start>` |
| `tools/nav_hook.py` | MkDocs hook: injects prev/next/exercise/feedback nav block |
| `tools/paths.py` | Centralized path constants for scripts |
| `tools/printer.py` | Console output: `pr.green()`, `pr.yes()`, `pr.no()`, `pr.warning()` |
| `scripts/web_preprocessing.sh` | Orchestrates all 8 pre-processing scripts in order |
| `scripts/generate_mkdocs_yaml.py` | Regenerates `mkdocs.yaml` nav from filesystem + headings |
| `scripts/generate_indexes.py` | Writes section and class `index.md` hub pages |
| `scripts/renumber_footnotes.py` | Renumbers footnotes sequentially across entire course |
| `scripts/check_renumber.py` | Detects and fixes ordered list numbering inconsistencies |
| `scripts/clean_dead_links.py` | Removes broken links from index pages |
| `scripts/fix_heading_hierarchy.py` | Normalizes heading levels; converts bold first-lines to `#` |
| `scripts/fixing_tables.py` | Normalizes Markdown table cell padding and separators |
| `scripts/update_css.py` | Syncs CSS variable values to `identity/dpd-variables.css` |
| `scripts/regenerate_pages.sh` | Fetches latest vocab/abbreviations from external `dpd-db` repo |
| `scripts/cl/pali-build-website` | Local dev launcher: regenerate → preprocess → `mkdocs serve` |
| `.github/workflows/deploy_site.yaml` | CI/CD: auto-deploy to GitHub Pages on push to `main` |
| `.github/workflows/release_class.yaml` | Release pipeline for document exports |
| `site/` | Generated static HTML output (not committed to repo) |
