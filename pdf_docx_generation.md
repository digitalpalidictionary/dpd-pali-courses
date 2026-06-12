# PDF & DOCX Generation Pipeline — Technical Reference

This document is the complete technical reference for how the PDF and DOCX export pipeline works. It covers every stage from raw Markdown source through to the final rendered file. It is written so that the system can be reproduced in a new project whose folder structure mirrors `docs/bpc_key/`.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Folder Structure & Input Files](#2-folder-structure--input-files)
3. [Shared Pre-Processing Logic](#3-shared-pre-processing-logic)
4. [PDF Pipeline — generate_pdfs.py](#4-pdf-pipeline--generate_pdfspy)
5. [DOCX Pipeline — generate_docx.py](#5-docx-pipeline--generate_docxpy)
6. [CSS Styling for PDF](#6-css-styling-for-pdf)
7. [Font Setup](#7-font-setup)
8. [How Footnotes Work in PDF](#8-how-footnotes-work-in-pdf)
9. [How List Numbering Works](#9-how-list-numbering-works)
10. [How Tables Are Handled](#10-how-tables-are-handled)
11. [How Images Are Handled](#11-how-images-are-handled)
12. [Internal Links](#12-internal-links)
13. [TOC Generation](#13-toc-generation)
14. [File-Type Specific Behaviors](#14-file-type-specific-behaviors)
15. [Running the Scripts](#15-running-the-scripts)
16. [Porting to a New Project](#16-porting-to-a-new-project)

---

## 1. Overview

Both generators share the same pattern:

```
mkdocs.yaml nav: section
        │
        ▼
Read Markdown files in order (bpc_key/, bpc_ex/, etc.)
        │
        ▼
Pre-process: protect footnotes + list markers, resolve image paths
        │
        ▼
Convert Markdown → HTML  (python-markdown or Pandoc)
        │
        ▼
Post-process HTML: fix list start attrs, fix internal links,
                   remove empty thead, mark wide tables,
                   convert footnote defs → WeasyPrint floats
        │
        ▼
Apply CSS  →  WeasyPrint / Pandoc  →  PDF / DOCX
```

There is no MkDocs involved. Both scripts read the `nav:` section of `mkdocs.yaml` only to discover file order, then process the Markdown files directly and independently of the website build.

---

## 2. Folder Structure & Input Files

### 2.1 Folder names and their PDF titles

```python
FOLDER_NAMES = {
    'bpc':     'Beginner Pāḷi Course (BPC)',
    'bpc_ex':  'Beginner Pāḷi Course (BPC) - Exercises',
    'bpc_key': 'Beginner Pāḷi Course (BPC) - Answer Key',
    'ipc':     'Intermediate Pāḷi Course (IPC)',
    'ipc_ex':  'Intermediate Pāḷi Course (IPC) - Exercises',
    'ipc_key': 'Intermediate Pāḷi Course (IPC) - Answer Key',
}
```

### 2.2 How files are discovered

The script reads `mkdocs.yaml`, parses the `nav:` tree recursively, and collects every `.md` path whose top-level folder matches one of the six folder names above:

```python
def get_markdown_files(docs_dir):
    with open("mkdocs.yaml") as f:
        config = yaml.safe_load(f)
    # recursive traversal of nav: dict/list structure
    # returns dict: { 'bpc': [path, ...], 'bpc_key': [path, ...], ... }
```

**Consequence:** The order of files in the PDF exactly matches the order in `mkdocs.yaml`. If `mkdocs.yaml` nav is regenerated (e.g. by `generate_mkdocs_yaml.py`), the PDF order updates automatically.

### 2.3 Which files are skipped

For the PDF builder (`generate_pdfs.py`):
- The top-level `index.md` of each folder (e.g. `docs/bpc_key/index.md`) is excluded. That file is a navigation list page, not content.
- Detection: `len(rel.split(os.sep)) == 2 and rel.endswith('index.md')` — i.e., files exactly one folder deep with filename `index.md`.

For the DOCX builder (`generate_docx.py`):
- `_ex` and `_key` folders: all `index.md` files (any depth matching `os.path.basename == 'index.md'`) are skipped.
- `bpc` / `ipc` lesson folders: class-level `index.md` files are NOT skipped — they provide the chapter structure page.

---

## 3. Shared Pre-Processing Logic

Both scripts share identical pre-processing logic (duplicated in each file) before any Markdown is converted.

### 3.1 `clean_markdown_content(content)`

Strips website UI elements that have no meaning in a PDF:

```python
content = re.sub(r'<div class="nav-links">.*?</div>', '', content, flags=re.DOTALL)
content = re.sub(r'<div class="feedback">.*?</div>', '', content, flags=re.DOTALL)
content = re.sub(r'<a[^>]+class="(prev|previous|next|cross)"[^>]*>.*?</a>', '', content)
```

These blocks are injected by `tools/nav_hook.py` during the website build. They must be removed before PDF/DOCX processing because they contain website-relative URLs.

### 3.2 `pre_process_content(text)` — PDF only

This function transforms raw Markdown into Markdown-with-raw-HTML-markers. It is the most critical pre-processing step. It has four parts, which must run in this exact order:

#### Part 1: Collapse excess blank lines

```python
def repl_newlines(m):
    count = m.group(0).count('\n')
    if count > 2:
        return '\n\n' + '<br>\n' * (count - 2)
    return m.group(0)
text = re.sub(r'\n{3,}', repl_newlines, text)
```

Must run FIRST because the footnote definition replacement injects extra blank lines, and without this pre-collapse, those injected lines would re-trigger `<br>` insertion on a second pass.

#### Part 2: Protect footnote definitions `[^N]: text`

```python
pattern = r'^([ \t*_]*)\[\^(\d+)\]:\s*(.*?)(?=\n[ \t]*\n|\n[ \t]*[-*_]{3,}|\n[ \t]*#|\n\[\^|\Z)'
text = re.sub(pattern, repl_def, text, flags=re.MULTILINE | re.DOTALL)
```

Transforms:
```
[^1]: This is the footnote text.
```
Into:
```html
<div class='manual-fn-def' data-fn='1' markdown='1'>

This is the footnote text.

</div>
```

The `markdown='1'` attribute tells python-markdown's `md_in_html` extension to still process the inner content as Markdown.

#### Part 3: Protect footnote references `[^N]`

```python
text = re.sub(r'\[\^(\d+)\]', r"<sup class='manual-fn-ref' data-fn='\1'>\1</sup>", text)
```

Transforms `[^1]` → `<sup class='manual-fn-ref' data-fn='1'>1</sup>` before python-markdown can interpret it as a standard footnote.

#### Part 4: Insert list start markers

```python
def repl_list(m):
    num = m.group(1)
    return f"\n<div class='manual-list-start' data-start='{num}'></div>\n\n{num}. "
text = re.sub(r'^\s*(\d+)\.\s+', repl_list, text, flags=re.MULTILINE)
```

Before every numbered list item, inserts a `<div class='manual-list-start' data-start='N'>` marker. This is used by the post-processor to set `<ol start="N">` on the rendered `<ol>` element — which allows ordered lists to continue numbering across interrupting block elements (tables, code blocks).

#### Part 5: Remove `<br>` before table rows

```python
text = re.sub(r'(<br>\n)+(\|)', r'\n\2', text)
```

Cleans up any `<br>` tags immediately before Markdown table rows, which would cause the table parser to fail.

### 3.3 `resolve_image_paths(content, file_path)` — PDF only

Converts relative Markdown image paths to absolute filesystem paths:

```python
def replacer(match):
    alt, src = match.group(1), match.group(2)
    if not src.startswith('http') and not os.path.isabs(src):
        src = os.path.normpath(os.path.join(file_dir, src))
    return f'![{alt}]({src})'
return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replacer, content)
```

WeasyPrint cannot resolve relative paths from the Markdown source location; it needs absolute paths. DOCX uses `--resource-path` in Pandoc instead.

---

## 4. PDF Pipeline — generate_pdfs.py

### 4.1 Markdown → HTML conversion

Uses `python-markdown` with these extensions:

```python
md = markdown.Markdown(extensions=[
    'toc',          # generates TOC; also used to drive the PDF TOC page
    'tables',       # pipe tables → <table>
    'fenced_code',  # ``` fenced code blocks
    'attr_list',    # {#id .class} attribute syntax on elements
    'sane_lists',   # prevents list continuation across blank lines
    'md_in_html',   # allows Markdown inside raw HTML divs (e.g. manual-fn-def)
    'nl2br',        # single newlines → <br>
])
```

**Important:** `md.reset()` must be called between conversions of different files, or the TOC state accumulates across files.

### 4.2 `build_html_document()` — main assembly function

Assembles the entire PDF HTML from all files. For `bpc_key` and `bpc_ex`, the call signature is:

```python
html = build_html_document(
    title="Beginner Pāḷi Course (BPC) - Answer Key",
    files_data=[(file_path, content), ...],
    title_md_content="",      # empty for key/ex (only bpc/ipc get about page)
    literature_md_content="", # empty for key/ex
    folder_type="bpc_key",
    root_index_content=""     # empty for key/ex (only bpc/ipc get lesson TOC)
)
```

The assembled HTML structure is:

```html
<!doctype html>
<html lang='en'>
<head>
  <meta charset='utf-8'>
  <title>Beginner Pāḷi Course (BPC) - Answer Key</title>
  <style>
    /* inline emergency styles: page-break-before on all .pdf-* sections,
       manual-list-start hidden, inline image sizing, footnote link colors */
  </style>
</head>
<body class="bpc_key">
  <div class="pdf-title-page"><h1>Beginner Pāḷi Course (BPC) - Answer Key</h1></div>
  <div class="pdf-toc-page">  <!-- generated TOC (see §13) -->
    <h1>Table of Contents</h1>
    <nav>...</nav>
  </div>
  <div class="content">
    <div class="pdf-topic-page" id="1_class_md">...HTML for 1_class.md...</div>
    <div class="pdf-topic-page" id="2_class_md">...HTML for 2_class.md...</div>
    ...
  </div>
</body>
</html>
```

### 4.3 Heading level shift — lessons only

For `bpc` and `ipc` lesson folders (not `bpc_key`, `bpc_ex`, `ipc_key`, `ipc_ex`), non-index file headings are shifted down one level after conversion:

```python
if not is_idx and folder_type in ('bpc', 'ipc'):
    topic_html = re.sub(
        r'<(/?)h([1-5])',
        lambda m: f'<{m.group(1)}h{int(m.group(2))+1}',
        topic_html
    )
```

This creates a two-level hierarchy: class index is `h1`, topic pages start at `h2`. For `bpc_key`, `ipc_key`, `bpc_ex`, `ipc_ex`, headings are NOT shifted — the files' own `h1` headings stay at `h1` so they become top-level PDF bookmarks.

### 4.4 `post_process_html()` — single-pass BeautifulSoup post-processor

Runs on the full assembled HTML in one BeautifulSoup parse. It does five things:

1. **Fix internal `.md` links** → PDF anchor IDs (see §12)
2. **Fix list start numbers** → sets `<ol start="N">` from `.manual-list-start` markers (see §9)
3. **Remove empty `<thead>`** → prevents double borders on headerless tables
4. **Mark wide/long tables** → adds `.wide-table .cols-N` and `.long-table` classes (see §10)
5. **Process footnotes** → converts `manual-fn-def` divs to WeasyPrint `float: footnote` spans (see §8)

### 4.5 Column equalization — `bpc_ex` / `ipc_ex` only

After `post_process_html()`, exercise PDFs get a second pass:

```python
if folder_type in ('bpc_ex', 'ipc_ex'):
    full_body_html = equalize_table_columns(full_body_html)
```

This sets explicit equal-percentage widths on every `<td>` and `<th>` in every table:

```python
col_width = f"{100 / n:.4f}%"
for cell in table.find_all(['td', 'th']):
    cell['style'] = f"width: {col_width};"
```

WeasyPrint's auto column-width algorithm distributes space unevenly for exercise tables. Explicit equal widths override this.

### 4.6 `generate_pdf()` — WeasyPrint call

```python
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

font_config = FontConfiguration()
css_objs = [CSS(filename=p, font_config=font_config) for p in css_paths if os.path.exists(p)]
HTML(string=html_content, base_url=os.path.abspath(".")).write_pdf(
    output_pdf,
    stylesheets=css_objs,
    font_config=font_config
)
```

CSS files applied in this order:
1. `identity/dpd-pdf-fonts.css` — font-face declarations
2. `identity/dpd-variables.css` — CSS custom properties (colors)
3. `identity/dpd.css` — content component styles
4. `identity/extra.css` — PDF-specific rules inside `@media print`

`base_url=os.path.abspath(".")` tells WeasyPrint to resolve all relative URL references (including image `src` after path resolution, and CSS `url()` references) from the project root.

### 4.7 macOS library path fix

```python
if sys.platform == "darwin":
    homebrew_lib = "/opt/homebrew/lib"
    if os.path.exists(homebrew_lib):
        os.environ["DYLD_LIBRARY_PATH"] = homebrew_lib + ":" + ...
```

WeasyPrint on macOS requires Homebrew-installed Pango/Cairo. This must be set before importing WeasyPrint.

---

## 5. DOCX Pipeline — generate_docx.py

### 5.1 Conversion engine

Uses **Pandoc** via `pypandoc.convert_text()`. Pandoc handles Markdown → DOCX natively, with better heading/table fidelity than python-markdown → WeasyPrint for Word format.

### 5.2 `aggregate_markdown()` — file assembly

Combines all files for a folder into one Markdown string:

```python
aggregated = f"# {title}\n\n"
# optional about + literature (bpc/ipc only)
# optional manual TOC (ex/key only — see §13)

for i, (file_path, content) in enumerate(files_data):
    c = clean_markdown_content(content)
    c = fix_internal_links(c)          # .md links → #anchor
    c = preprocess_inline_images(c)    # adds {height=18px} to inline images

    if i > 0 and needs_file_pagebreaks:
        aggregated += PAGEBREAK        # OpenXML page break

    if is_ex:
        c = insert_h2_page_breaks(c)   # page break before each ## heading

    anchor_id = os.path.basename(file_path).replace('.', '_')
    aggregated += f"[]{{#{anchor_id}}}\n\n"  # Pandoc anchor for internal links
    aggregated += f"{c}\n\n"
```

**Page break constant:**
```python
PAGEBREAK = '\n\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n'
```

This uses Pandoc's raw OpenXML pass-through — it inserts a Word native page break that survives the DOCX round-trip.

### 5.3 `preprocess_inline_images(content)`

```python
return re.sub(
    r'(!\[[^\]]*\]\([^)]+\))(?!\{)',
    r'\1{height=18px}',
    content
)
```

Adds `{height=18px}` to every image that doesn't already have an attribute block. In DOCX, grammar symbol images (pacman, arrows) must render inline at text height. Pandoc's `attr_list` handles this.

### 5.4 `insert_h2_page_breaks(content)` — `_ex` files only

Inserts a page break before every `## ` heading in exercise files:

```python
for line in lines:
    if re.match(r'^## ', line):
        result.extend(['', '```{=openxml}', '<w:p><w:r><w:br w:type="page"/></w:r></w:p>', '```', ''])
    result.append(line)
```

Exercise files use `##` headings for each class. A page break before each class section makes the DOCX printable with clean separation.

### 5.5 `generate_docx()` — Pandoc call

```python
extra_args = ['--standalone', '--resource-path=docs:docs/assets/images:.']
if use_pandoc_toc:   # bpc/ipc only
    extra_args += ['--toc', '--toc-depth=2']

pypandoc.convert_text(
    aggregated_md,
    'docx',
    format='markdown',
    outputfile=output_docx,
    extra_args=extra_args
)
```

- `--standalone`: produce a complete DOCX file (with styles), not a fragment
- `--resource-path`: tells Pandoc where to look for images
- `--toc` / `--toc-depth=2`: Pandoc-native clickable TOC field (Word updates it on open); only used for lesson folders, not `_ex`/`_key` which use the manually-built TOC

### 5.6 `post_process_docx()` — python-docx fixes

After Pandoc generates the DOCX:

```python
doc = Document(docx_path)

# _ex only: merge last row of exercise tables (single-cell footer rows)
if folder.endswith('_ex'):
    for table in doc.tables:
        last_row = table.rows[-1]
        non_empty = sum(1 for c in last_row.cells if c.text.strip())
        if non_empty <= 1:
            last_row.cells[0].merge(last_row.cells[-1])

# Force Word to update the TOC field on first open
update_fields = OxmlElement('w:updateFields')
update_fields.set(qn('w:val'), 'true')
doc.settings.element.append(update_fields)

doc.save(docx_path)
```

The `w:updateFields` trick is necessary because Pandoc generates a `TOC` field placeholder; without it, Word shows an empty TOC until the user manually presses F9.

---

## 6. CSS Styling for PDF

WeasyPrint applies CSS to the generated HTML using the CSS Paged Media specification. The rules are organized across four files loaded in order:

### 6.1 Loading order (matters for cascade)

```python
css_paths = [
    "identity/dpd-pdf-fonts.css",  # 1st: fonts must register before use
    "identity/dpd-variables.css",  # 2nd: CSS custom properties
    "identity/dpd.css",            # 3rd: content components
    "identity/extra.css",          # 4th: overrides + @media print rules
]
```

### 6.2 `@media print` block in `extra.css`

All PDF-specific rules live inside `@media print { }`. WeasyPrint renders everything as "print" media, so these rules apply; the website's `@media screen` rules do not apply.

**Page margins:**
```css
@page {
    margin-left: 10mm;
    margin-right: 10mm;
    @footnote {
        border-top: 1px solid black;
        padding-top: 0.5em;
        text-align: left;
    }
}
```

**Footnote float:**
```css
.pdf-footnote {
    float: footnote;     /* WeasyPrint CSS Paged Media extension */
    font-size: 0.9em;
    font-style: italic;
    font-weight: normal !important;
    line-height: 1.2;
}
.pdf-footnote::footnote-call,
.pdf-footnote::footnote-marker { content: ""; }  /* hide auto-generated markers */
```

**Table page-break rules:**
```css
table { break-inside: avoid; break-before: avoid; }
table.long-table { break-inside: auto; }   /* 12+ row tables may split */

/* ex/key: all tables flow freely */
body.bpc_key table, body.ipc_key table,
body.bpc_ex table, body.ipc_ex table {
    break-inside: auto;
    break-before: auto;
}
```

**Wide table font scaling** (graduated by column count):
```css
.content table.cols-7 td, .content table.cols-7 th  { font-size: 0.9rem !important; padding: 4px 3px !important; }
.content table.cols-8 td, .content table.cols-8 th  { font-size: 0.85rem !important; padding: 3px 2px !important; }
.content table.cols-9 td, .content table.cols-9 th  { font-size: 0.8rem !important; padding: 3px 2px !important; }
.content table.cols-10 td, .content table.cols-10 th { font-size: 0.7rem !important; padding: 3px 2px !important; }
```

**Body class controls folder-specific overrides.** The `<body>` tag gets `class="bpc_key"`, `class="bpc_ex"`, etc. This allows CSS selectors like `body.bpc_ex table td { text-align: left !important; }` to apply only to exercise PDFs.

**Bookmark exclusions** — prevents front-matter headings from appearing in the PDF bookmark sidebar:
```css
.pdf-title-page h1,
.pdf-about-page h2, .pdf-about-page h3,
.pdf-literature-page h2, .pdf-literature-page h3,
.pdf-toc-page h2, .pdf-toc-page h3 { bookmark-level: none; }
```

### 6.3 CSS custom properties (`dpd-variables.css`)

All colors are defined as CSS custom properties on `:root`. WeasyPrint supports CSS variables.
Key variables for content:
- `--primary`: main accent color (blue hue), used for borders, links, header cells
- `--light` / `--dark`: background and text color extremes
- `--gray`, `--gray-transparent`: border and divider colors

---

## 7. Font Setup

### 7.1 Why static TTF files are required

WeasyPrint uses Pango/Cairo for text rendering. The variable font (`Inter[wght].ttf`) causes two bugs:
1. **CMap corruption** of composed Unicode characters (ṭ, ṃ, ḷ, ā, etc.) — characters essential for Pāḷi text
2. **OpenType ligature copy/paste issues** in the generated PDF

The fix is to register static (non-variable) TTF instances for each weight/style:

```css
/* identity/dpd-pdf-fonts.css */
@font-face {
    font-family: "Inter";
    src: url("path/to/Inter-Regular.ttf") format("truetype");
    font-weight: 400; font-style: normal;
}
@font-face {
    font-family: "Inter";
    src: url("path/to/Inter-Bold.ttf") format("truetype");
    font-weight: 700; font-style: normal;
}
@font-face {
    font-family: "Inter";
    src: url("path/to/Inter-Italic.ttf") format("truetype");
    font-weight: 400; font-style: italic;
}
@font-face {
    font-family: "Inter";
    src: url("path/to/Inter-BoldItalic.ttf") format("truetype");
    font-weight: 700; font-style: italic;
}

body {
    font-variant-ligatures: none;
    font-feature-settings: "liga" 0, "clig" 0;  /* disable ligatures globally */
}
```

The `dpd.css` sets `font-family: "Inter", sans-serif` on `body`.

### 7.2 Font file location

In this project the fonts are at `../website_example/identity_dpd/fonts/Inter-*.ttf` relative to the CSS file. In a new project, place the four TTF files anywhere accessible and update the `url()` paths in `dpd-pdf-fonts.css` accordingly.

---

## 8. How Footnotes Work in PDF

### 8.1 Source syntax

Standard Markdown footnote syntax in source files:

```markdown
The lion eats the disciple.[^1]

[^1]: This is the footnote text.
```

### 8.2 Pre-processing transform (Python, before Markdown conversion)

`pre_process_content()` converts the source before `python-markdown` sees it:

- `[^1]` → `<sup class='manual-fn-ref' data-fn='1'>1</sup>`
- `[^1]: text` → `<div class='manual-fn-def' data-fn='1' markdown='1'>text</div>`

These raw HTML elements pass through `python-markdown` unchanged (because they are injected as raw HTML). The `markdown='1'` attribute allows `md_in_html` to process the footnote definition body as Markdown.

### 8.3 Post-processing transform (BeautifulSoup, after Markdown conversion)

`post_process_html()` performs these transforms:

**Step 1** — Add bidirectional IDs to references:
```html
<sup class='manual-fn-ref' data-fn='1' id='fnref-1'><a href='#fn-1'>1</a></sup>
```

**Step 2** — Convert each `div.manual-fn-def` to a WeasyPrint float span, inserted immediately after its reference `<sup>`:
```html
<span class='pdf-footnote' id='fn-1'>
  <b class='pdf-footnote-label'>1. </b>
  This is the footnote text.
  <a href='#fnref-1' class='pdf-footnote-backref'> ↩</a>
</span>
```

**Step 3** — Remove all original `div.manual-fn-def` elements (they have been converted).

**Step 4** — Hoist footnote spans out of `<strong>` wrappers:
```python
for strong in soup.find_all('strong'):
    fn_spans = strong.find_all('span', class_='pdf-footnote')
    for fn_span in reversed(fn_spans):
        fn_span.extract()
        strong.insert_after(fn_span)
```
WeasyPrint cannot float an element that is a descendant of `<strong>`. If a footnote reference appears inside bold text, the `<span class='pdf-footnote'>` must be moved outside the `<strong>` or it will be rendered inline instead of as a page footnote.

### 8.4 CSS rendering

```css
@media print {
    .pdf-footnote { float: footnote; }  /* CSS Paged Media spec */
}
```

WeasyPrint collects all `float: footnote` elements and renders them in the `@footnote` area at the bottom of each page, automatically managing overflow across pages.

---

## 9. How List Numbering Works

### 9.1 The problem

Markdown parsers (including python-markdown) reset ordered list numbering when a list is interrupted by a block element:

```markdown
1. First item
2. Second item

| table | here |
|---|---|

3. Third item    ← parser renders this as "1." again
```

### 9.2 The solution

**Pre-processing** inserts a marker div before every list item:

```python
# Input:  "3. Third item"
# Output: "<div class='manual-list-start' data-start='3'></div>\n\n3. Third item"
```

**Post-processing** (BeautifulSoup) finds each marker and sets `<ol start="N">`:

```python
for marker in soup.find_all('div', class_='manual-list-start'):
    start_val = str(marker.get('data-start') or '1')
    next_ol = marker.find_next_sibling('ol')
    if next_ol:
        next_ol['start'] = start_val
        next_ol['style'] = f"counter-reset: list-item {int(start_val) - 1};"
    marker.decompose()
```

Both the `start` attribute and the `counter-reset` style are set. WeasyPrint uses CSS counters internally and needs both.

---

## 10. How Tables Are Handled

### 10.1 Table class system

Table CSS classes (set in Markdown source with `{.classname}` attribute syntax):

| Class | Appearance |
|---|---|
| (none) | Full-width, top/bottom border only |
| `.grammar` | No border, label column in primary color, left-aligned |
| `.inflection` | Rounded cells, primary-color header borders |
| `.freq` | Color-coded cells by frequency grade (heatmap) |
| `.no-header` | `thead` hidden |
| `.sutta-info` | No border, left-aligned labels |
| `.family` | Compact, no outer border |

### 10.2 Wide table detection

`post_process_html()` inspects every table and adds classes based on column/row count:

```python
cols = len(first_row.find_all(['td', 'th']))
rows = len(table.find_all('tr'))

if cols >= 7:
    # For text-heavy tables with cols < 10, count one extra to trigger larger scaling
    effective_cols = cols + 1 if len(table.get_text()) > 800 and cols < 10 else cols
    capped = min(effective_cols, 10)
    classes += ['wide-table', f'cols-{capped}']

if rows > 12:
    classes.append('long-table')
```

The CSS in `extra.css @media print` then scales font size down for wide tables (`.cols-7` through `.cols-10`) so they fit within the page width.

### 10.3 Empty `<thead>` removal

Some tables have a header row that is entirely empty (e.g., tables using `.no-header` in source). python-markdown still generates a `<thead>` with empty `<th>` cells, creating a double top border. The post-processor removes it:

```python
for thead in soup.find_all('thead'):
    th_cells = thead.find_all('th')
    if th_cells and all(not th.get_text(strip=True) for th in th_cells):
        thead.decompose()
```

### 10.4 Column equalization (exercise PDFs only)

After all other post-processing, exercise PDFs run `equalize_table_columns()` which sets `width: X%` on every cell, where X = 100 / column_count. This forces WeasyPrint to distribute columns equally regardless of content width.

---

## 11. How Images Are Handled

### 11.1 Inline vs. standalone distinction

Images are classified into two rendering categories:

**Inline images** (grammar symbols: pacman, arrows) — appear inside text, must render at text height:
- CSS: `height: 1.5em; width: auto; vertical-align: middle;` on the web
- In PDF inline CSS: `p:not(.standalone-image) img, td img, li img { height: 1em; width: auto; vertical-align: middle; }`
- In DOCX: `preprocess_inline_images()` adds `{height=18px}` attribute

**Standalone images** (diagrams, screenshots) — alone in their paragraph, must render centered at full size:
- PDF: `post_process_html()` adds class `standalone-image` to any `<p>` containing exactly one `<img>` with no other content
- CSS: `.standalone-image img { max-width: 90%; display: block; margin: 0 auto; }`

### 11.2 Path resolution for PDF

`resolve_image_paths()` converts relative Markdown image paths to absolute filesystem paths before conversion. WeasyPrint needs absolute paths because it does not know the Markdown file's location. `base_url=os.path.abspath(".")` is also set on the WeasyPrint HTML call as a secondary fallback.

### 11.3 Path resolution for DOCX

Pandoc uses `--resource-path=docs:docs/assets/images:.` — a colon-separated list of directories to search for images. The images are expected to live in `docs/assets/images/`.

---

## 12. Internal Links

Source files may contain Markdown links to other `.md` files:
```markdown
[See Class 2](../class_2/index.md)
```

These relative web paths are meaningless in a PDF/DOCX. Both pipelines convert them to internal anchor references.

**PDF** (`post_process_html()` via BeautifulSoup):
```python
if '.md' in href and not href.startswith('http'):
    file_part = href.split('#')[0]
    if os.path.basename(file_part) == 'index.md':
        # class_1/index.md → class_1_index_md (avoids all index files colliding)
        parts = [p for p in file_part.replace('\\', '/').split('/') if p and p != '..']
        anchor_id = '_'.join(parts).replace('.', '_')
    else:
        anchor_id = os.path.basename(file_part).replace('.', '_')
    a['href'] = f"#{anchor_id}"
```

**DOCX** (`fix_internal_links()` on raw Markdown):
```python
anchor_id = os.path.basename(file_part).replace('.', '_')
return f"[{text}](#{anchor_id})"
```

Each content `<div>` in the PDF and each file block in the DOCX is given a matching `id` / anchor derived from the filename: `1_class.md` → `id="1_class_md"`.

---

## 13. TOC Generation

### 13.1 Lesson folders (`bpc`, `ipc`) — PDF

Uses the pre-existing `docs/bpc/index.md` as the TOC page (it is a manually/auto-generated index of all lessons):

```python
if fld in ['bpc', 'ipc'] and os.path.exists(ri_path):
    with open(ri_path) as f:
        ri_c = f.read()
# passed to build_html_document as root_index_content=ri_c
```

This index page becomes `<div class="pdf-toc-page" id="toc-page">`.

### 13.2 Key and exercise folders (`bpc_key`, `bpc_ex`, etc.) — PDF

No pre-existing index is used. The TOC is generated programmatically by running python-markdown's `toc` extension over all content concatenated together:

```python
all_md = ""
for file_path, content in files_data:
    all_md += pre_process_content(clean_markdown_content(content)) + "\n\n"
md.convert(all_md)
toc = getattr(md, 'toc', '')
toc_html = f'<div class="pdf-toc-page"><h1>Table of Contents</h1>{toc}</div>'
```

python-markdown's `toc` extension collects all headings during conversion and exposes them as `md.toc` (an HTML `<nav>` containing nested `<ul>/<li>/<a>` links).

### 13.3 Key and exercise folders — DOCX

Uses a manually-built TOC from headings in the source (because Pandoc's `--toc` flag produces inconsistent output for flat folder structures):

```python
def build_manual_toc(files_data):
    lines = ['# Table of Contents', '']
    for _file_path, content in files_data:
        for line in content.split('\n'):
            m = re.match(r'^(#{1,2}) (.+)', line)
            if m:
                level = len(m.group(1))
                text = re.sub(r'\s*\{[^}]+\}\s*$', '', m.group(2).strip())
                slug = make_heading_slug(text)
                indent = '    ' if level == 2 else ''
                lines.append(f'{indent}- [{text}](#{slug})')
    return '\n'.join(lines)
```

`make_heading_slug()` replicates Pandoc's heading ID generation algorithm (lowercase, strip punctuation, spaces → hyphens, strip leading non-letters).

### 13.4 Lesson folders (`bpc`, `ipc`) — DOCX

Uses Pandoc's built-in `--toc --toc-depth=2`. Pandoc generates a Word TOC field that updates automatically when the DOCX is opened. `post_process_docx()` sets `w:updateFields` to force this update on first open.

---

## 14. File-Type Specific Behaviors

### 14.1 `bpc_key` / `ipc_key` (answer keys)

- No about/literature page
- No root index TOC — generated programmatically from headings
- Headings NOT shifted (stay at `h1`, `h2`, etc. as authored)
- No `# Class N` heading stripping
- Table page breaks: `break-inside: auto; break-before: auto` (tables flow freely across pages)
- DOCX: folder-level `index.md` skipped; no `## ` page breaks

### 14.2 `bpc_ex` / `ipc_ex` (exercises)

All of the above, plus:
- PDF: column equalization (`equalize_table_columns`)
- PDF: `text-align: left` forced on all table cells (`body.bpc_ex table td`)
- DOCX: page break inserted before every `## ` heading
- DOCX: last-row single-cell merge applied to exercise tables

### 14.3 `bpc` / `ipc` (lessons)

- About page (`docs/about.md`) included
- Literature page (`docs/literature.md`) included
- Root index (`docs/bpc/index.md`) used as PDF TOC
- Headings in non-index files shifted down one level
- `# Class N` headings stripped from non-index files (class index provides it)
- Tables: normal `break-inside: avoid` (tables don't split unless `.long-table`)

---

## 15. Running the Scripts

```bash
# Generate all PDFs
uv run python scripts/generate_pdfs.py

# Generate one folder
uv run python scripts/generate_pdfs.py bpc_key

# HTML debug output (skip WeasyPrint, write intermediate HTML)
uv run python scripts/generate_pdfs.py bpc_key --html-only

# Generate all DOCX
uv run python scripts/generate_docx.py

# Generate one folder
uv run python scripts/generate_docx.py --folder bpc_key
```

Output directories:
- `pdf_exports/bpc_key.pdf`
- `docx_exports/bpc_key.docx`

After full generation, `scripts/verify_numbering.py` and `scripts/verify_docx_content.py` run automatically to check for numbering or content issues.

---

## 16. Porting to a New Project

Minimum requirements to replicate this pipeline for a new project with a `docs/bpc_key/`-style folder:

### 16.1 Python dependencies

```
weasyprint
python-markdown
beautifulsoup4
pyyaml
pypandoc
python-docx
```

### 16.2 Files to copy

| File | Purpose |
|---|---|
| `scripts/generate_pdfs.py` | PDF generator |
| `scripts/generate_docx.py` | DOCX generator |
| `identity/dpd-pdf-fonts.css` | Font registration |
| `identity/dpd-variables.css` | CSS custom properties |
| `identity/dpd.css` | Content component styles |
| `identity/extra.css` | PDF-specific `@media print` rules |
| Font TTF files (4×) | Inter Regular/Bold/Italic/BoldItalic |

### 16.3 Required font path update

In `dpd-pdf-fonts.css`, update `url()` paths to point to where you place the `.ttf` files.

### 16.4 `mkdocs.yaml` nav structure

The scripts read `mkdocs.yaml` to discover file order. The `nav:` section must include the folder's files. If the new project does not use MkDocs, replace `get_markdown_files()` with a function that returns `{'bpc_key': [sorted list of .md file paths]}` directly.

### 16.5 Folder naming

The scripts match folders by exact name from `FOLDER_NAMES`. If your folder is named differently, add it to `FOLDER_NAMES` in both scripts.

### 16.6 What the source `.md` files must NOT contain

- Raw HTML `<div class="nav-links">` blocks (stripped by `clean_markdown_content`)
- Absolute image paths (they are resolved from the file's directory)
- `[^N]` footnote syntax will be intercepted and converted — do not pre-convert them

### 16.7 macOS WeasyPrint dependencies

```bash
brew install pango cairo gdk-pixbuf libffi
```

Set `DYLD_LIBRARY_PATH=/opt/homebrew/lib` before running (the script does this automatically on darwin).
