"""
Script to generate PDF course materials from Markdown source files using WeasyPrint.
It applies course-specific styling, cleans UI elements, and handles footnote reformatting.
"""
import argparse
import os
import time
import yaml
import markdown
import re
import subprocess
import sys
from pathlib import Path
from bs4 import BeautifulSoup
from tools.printer import printer as pr

# Ensure Homebrew libraries are found on macOS
if sys.platform == "darwin":
    homebrew_lib = "/opt/homebrew/lib"
    if os.path.exists(homebrew_lib):
        if "DYLD_LIBRARY_PATH" in os.environ:
            os.environ["DYLD_LIBRARY_PATH"] = f"{homebrew_lib}:{os.environ['DYLD_LIBRARY_PATH']}"
        else:
            os.environ["DYLD_LIBRARY_PATH"] = homebrew_lib

FOLDER_NAMES = {
    'bpc': 'Beginner Pāḷi Course (BPC)',
    'bpc_ex': 'Beginner Pāḷi Course (BPC) - Exercises',
    'bpc_key': 'Beginner Pāḷi Course (BPC) - Answer Key',
    'ipc': 'Intermediate Pāḷi Course (IPC)',
    'ipc_ex': 'Intermediate Pāḷi Course (IPC) - Exercises',
    'ipc_key': 'Intermediate Pāḷi Course (IPC) - Answer Key',
}

def clean_markdown_content(content):
    """Remove UI elements not suitable for PDF."""
    content = re.sub(r'<div class="nav-links">.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class="feedback">.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<a[^>]+class="(prev|previous|next|cross)"[^>]*>.*?</a>', '', content)
    return content

def fix_internal_links(html_content):
    """Converts relative links to internal PDF anchors."""
    soup = BeautifulSoup(html_content, 'html.parser')
    for a in soup.find_all('a', href=True):
        href = str(a['href'])
        if ('.md' in href) and not href.startswith('http'):
            file_part = href.split('#')[0] if '#' in href else href
            anchor_id = os.path.basename(file_part).replace('.', '_')
            a['href'] = f"#{anchor_id}"
    return str(soup)

def fix_list_numbering(html_content):
    """Uses .manual-list-start markers to fix ordered list numbering in HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    for marker in soup.find_all('div', class_='manual-list-start'):
        start_val = str(marker.get('data-start') or '1')
        next_ol = marker.find_next_sibling('ol')
        if next_ol:
            next_ol['start'] = start_val
            reset_val = int(start_val) - 1
            next_ol['style'] = f"counter-reset: list-item {reset_val};"
        marker.decompose()
    return str(soup)

def pre_process_content(text):
    """Protects source footnote and list markers from renumbering."""
    # Collapse 3+ blank lines FIRST, before repl_def/repl_list inject extra newlines.
    # This prevents their injected newlines from triggering spurious <br> insertion.
    def repl_newlines(m):
        count = m.group(0).count('\n')
        if count > 2:
            return '\n\n' + '<br>\n' * (count - 2)
        return m.group(0)
    text = re.sub(r'\n{3,}', repl_newlines, text)

    def repl_def(m):
        prefix = m.group(1)
        fn_num = m.group(2)
        content = m.group(3).strip()
        return f"\n<div class='manual-fn-def' data-fn='{fn_num}' markdown='1'>\n\n{prefix}{content}\n\n</div>\n\n"
    pattern = r'^([ \t*_]*)\[\^(\d+)\]:\s*(.*?)(?=\n[ \t]*\n|\n[ \t]*[-*_]{3,}|\n[ \t]*#|\n\[\^|\Z)'
    text = re.sub(pattern, repl_def, text, flags=re.MULTILINE | re.DOTALL)
    text = re.sub(r'\[\^(\d+)\]', r"<sup class='manual-fn-ref' data-fn='\1'>\1</sup>", text)
    def repl_list(m):
        num = m.group(1)
        return f"\n<div class='manual-list-start' data-start='{num}'></div>\n\n{num}. "
    text = re.sub(r'^\s*(\d+)\.\s+', repl_list, text, flags=re.MULTILINE)

    # Remove <br> tags immediately before table rows so tables parse correctly
    text = re.sub(r'(<br>\n)+(\|)', r'\n\2', text)

    return text

def mark_wide_tables(html_content: str, col_threshold: int = 7, row_threshold: int = 12) -> str:
    """Add sizing and layout classes to tables based on column count and row count."""
    soup = BeautifulSoup(html_content, 'html.parser')
    for table in soup.find_all('table'):
        first_row = table.find('tr')
        if not first_row:
            continue
        cols = len(first_row.find_all(['td', 'th']))
        rows = len(table.find_all('tr'))
        classes = list(table.get('class') or [])
        if cols >= col_threshold:
            text_len = len(table.get_text())
            effective_cols = cols
            if text_len > 800 and cols < 10:
                effective_cols = cols + 1
            capped = min(effective_cols, 10)
            classes += ['wide-table', f'cols-{capped}']
        if rows > row_threshold:
            classes.append('long-table')
        if classes:
            table['class'] = " ".join(classes)
    return str(soup)


def equalize_table_columns(html_content: str) -> str:
    """Set explicit equal-width on every cell so WeasyPrint renders truly equal columns."""
    soup = BeautifulSoup(html_content, 'html.parser')
    for table in soup.find_all('table'):
        first_row = table.find('tr')
        if not first_row:
            continue
        n = len(first_row.find_all(['td', 'th']))
        if n < 2:
            continue
        col_width = f"{100 / n:.4f}%"
        for cell in table.find_all(['td', 'th']):
            cell['style'] = f"width: {col_width};"
    return str(soup)


def remove_empty_thead(html_content):
    """Removes thead elements where all th cells are empty, preventing double borders."""
    soup = BeautifulSoup(html_content, 'html.parser')
    for thead in soup.find_all('thead'):
        th_cells = thead.find_all('th')
        if th_cells and all(not th.get_text(strip=True) for th in th_cells):
            thead.decompose()
    return str(soup)

def process_footnotes_for_pdf(html_content):
    """Moves manual footnote definitions into WeasyPrint-compatible floats with bidirectional links.
    Also marks standalone image paragraphs in the same pass to avoid an extra parse cycle."""
    soup = BeautifulSoup(html_content, 'html.parser')
    # Mark standalone image paragraphs (single <img>, no other content)
    for p in soup.find_all('p'):
        meaningful = [c for c in p.children
                      if getattr(c, 'name', None) or str(c).strip()]
        if len(meaningful) == 1 and getattr(meaningful[0], 'name', None) == 'img':
            existing = p.get('class') or []
            if isinstance(existing, list):
                existing = ' '.join(str(c) for c in existing)
            p['class'] = f"{existing} standalone-image".strip()
    defs = {d['data-fn']: d for d in soup.find_all('div', class_='manual-fn-def')}
    for ref in soup.find_all('sup', class_='manual-fn-ref'):
        fn_num = ref['data-fn']
        ref['id'] = f"fnref-{fn_num}"
        a_link = soup.new_tag('a', href=f"#fn-{fn_num}")
        a_link.string = str(fn_num)
        ref.clear()
        ref.append(a_link)
        if fn_num in defs:
            new_span = soup.new_tag('span', attrs={'class': 'pdf-footnote', 'id': f"fn-{fn_num}"})
            label = soup.new_tag('b', attrs={'class': 'pdf-footnote-label'})
            label.string = f"{fn_num}. "
            new_span.append(label)
            fn_soup = BeautifulSoup(defs[fn_num].decode_contents(), 'html.parser')
            for p in fn_soup.find_all('p'):
                p.unwrap()
            new_span.append(fn_soup)
            backref = soup.new_tag('a', href=f"#fnref-{fn_num}", attrs={'class': 'pdf-footnote-backref'})
            backref.string = ' ↩'
            new_span.append(backref)
            ref.insert_after(new_span)
    for d in defs.values():
        d.decompose()
    # Hoist pdf-footnote spans out of <strong> — float:footnote fails inside strong
    for strong in soup.find_all('strong'):
        fn_spans = strong.find_all('span', class_='pdf-footnote')
        for fn_span in reversed(fn_spans):
            fn_span.extract()
            strong.insert_after(fn_span)
    return str(soup)

def post_process_html(html_content: str) -> str:
    """Single-pass HTML post-processor — replaces 5 separate BeautifulSoup parse/serialize cycles
    with one, dramatically reducing processing time on large course documents."""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Fix internal .md links → PDF anchors
    for a in soup.find_all('a', href=True):
        href = str(a['href'])
        if '.md' in href and not href.startswith('http'):
            file_part = href.split('#')[0] if '#' in href else href
            basename = os.path.basename(file_part)
            if basename == 'index.md':
                # Preserve parent dir to avoid collision (class_1/index.md → class_1_index_md)
                parts = [p for p in file_part.replace('\\', '/').split('/') if p and p != '..']
                anchor_id = '_'.join(parts).replace('.', '_')
            else:
                anchor_id = basename.replace('.', '_')
            a['href'] = f"#{anchor_id}"

    # Fix ordered list start numbers via manual-list-start markers
    for marker in soup.find_all('div', class_='manual-list-start'):
        start_val = str(marker.get('data-start') or '1')
        next_ol = marker.find_next_sibling('ol')
        if next_ol:
            next_ol['start'] = start_val
            next_ol['style'] = f"counter-reset: list-item {int(start_val) - 1};"
        marker.decompose()

    # Remove empty thead (prevents double border on headerless tables)
    for thead in soup.find_all('thead'):
        th_cells = thead.find_all('th')
        if th_cells and all(not th.get_text(strip=True) for th in th_cells):
            thead.decompose()

    # Mark wide/long tables with sizing classes
    for table in soup.find_all('table'):
        first_row = table.find('tr')
        if not first_row:
            continue
        cols = len(first_row.find_all(['td', 'th']))
        rows = len(table.find_all('tr'))
        classes = list(table.get('class') or [])
        if cols >= 7:
            effective_cols = cols + 1 if len(table.get_text()) > 800 and cols < 10 else cols
            classes += ['wide-table', f'cols-{min(effective_cols, 10)}']
        if rows > 12:
            classes.append('long-table')
        if classes:
            table['class'] = ' '.join(classes)

    # Mark standalone image paragraphs (single <img>, no other content)
    for p in soup.find_all('p'):
        meaningful = [c for c in p.children
                      if getattr(c, 'name', None) or str(c).strip()]
        if len(meaningful) == 1 and getattr(meaningful[0], 'name', None) == 'img':
            existing = p.get('class') or []
            if isinstance(existing, list):
                existing = ' '.join(str(c) for c in existing)
            p['class'] = f"{existing} standalone-image".strip()

    # Process footnotes: WeasyPrint floats + bidirectional links
    defs = {d['data-fn']: d for d in soup.find_all('div', class_='manual-fn-def')}
    for ref in soup.find_all('sup', class_='manual-fn-ref'):
        fn_num = ref['data-fn']
        ref['id'] = f"fnref-{fn_num}"
        a_link = soup.new_tag('a', href=f"#fn-{fn_num}")
        a_link.string = str(fn_num)
        ref.clear()
        ref.append(a_link)
        if fn_num in defs:
            new_span = soup.new_tag('span', attrs={'class': 'pdf-footnote', 'id': f"fn-{fn_num}"})
            label = soup.new_tag('b', attrs={'class': 'pdf-footnote-label'})
            label.string = f"{fn_num}. "
            new_span.append(label)
            fn_soup = BeautifulSoup(defs[fn_num].decode_contents(), 'html.parser')
            for fp in fn_soup.find_all('p'):
                fp.unwrap()
            new_span.append(fn_soup)
            backref = soup.new_tag('a', href=f"#fnref-{fn_num}", attrs={'class': 'pdf-footnote-backref'})
            backref.string = ' ↩'
            new_span.append(backref)
            ref.insert_after(new_span)
    for d in defs.values():
        d.decompose()
    for strong in soup.find_all('strong'):
        fn_spans = strong.find_all('span', class_='pdf-footnote')
        for fn_span in reversed(fn_spans):
            fn_span.extract()
            strong.insert_after(fn_span)

    return str(soup)

def resolve_image_paths(content: str, file_path: str) -> str:
    """Convert relative image paths to absolute so WeasyPrint can find them."""
    file_dir = os.path.dirname(os.path.abspath(file_path))
    def replacer(match):
        alt, src = match.group(1), match.group(2)
        if not src.startswith('http') and not os.path.isabs(src):
            src = os.path.normpath(os.path.join(file_dir, src))
        return f'![{alt}]({src})'
    return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replacer, content)


def build_html_document(title, files_data, title_md_content="", literature_md_content="", folder_type="", root_index_content=""):
    md = markdown.Markdown(extensions=['toc', 'tables', 'fenced_code', 'attr_list', 'sane_lists', 'md_in_html', 'nl2br'])

    def conv(t): return md.convert(pre_process_content(t))

    title_html = f'<div class="pdf-title-page"><h1>{title}</h1></div>'
    about_html = f'<div class="pdf-about-page">{conv(title_md_content)}</div>' if title_md_content else ""
    lit_html = f'<div class="pdf-literature-page">{conv(literature_md_content)}</div>' if literature_md_content else ""

    full_course_html = ""
    for file_path, content in files_data:
        is_idx = os.path.basename(file_path) == 'index.md'
        c = clean_markdown_content(content)
        c = resolve_image_paths(c, file_path)
        
        # We NO LONGER strip Class X headings for ex/key, as requested.
        # This allows Class X Exercises and Class X Extra to appear in TOC.
        # We only strip them if they are redundant with the index.md Class X heading in LESSONS (bpc/ipc).
        if not is_idx and not (folder_type.endswith('_ex') or folder_type.endswith('_key')):
            c = re.sub(r'^# Class \d+.*?\n', '', c, flags=re.MULTILINE)

        md.reset()
        topic_html = md.convert(pre_process_content(c))
        # Shift heading levels only for bpc/ipc which have a class→topic hierarchy.
        # ex/key folders have flat class files — their h1s stay at h1 so they appear
        # as top-level bookmarks alongside "Table of Contents".
        if not is_idx and folder_type in ('bpc', 'ipc'):
            topic_html = re.sub(r'<(/?)h([1-5])', lambda m: f'<{m.group(1)}h{int(m.group(2))+1}', topic_html)
        if is_idx:
            # Use parent dir + filename so class_1/index.md → class_1_index_md (not all "index_md")
            parent = os.path.basename(os.path.dirname(file_path))
            file_id = f"{parent}_index_md"
        else:
            file_id = os.path.basename(file_path).replace('.', '_')
        div_class = 'pdf-class-header' if is_idx else 'pdf-topic-page'
        full_course_html += f"<div class='{div_class}' id='{file_id}'>{topic_html}</div>"
    
    md.reset()
    if root_index_content:
        # For lessons, use the provided root index content.
        # Wrap with an id so PDF internal links can target the TOC page.
        toc_html = f'<div class="pdf-toc-page" id="toc-page">{md.convert(pre_process_content(root_index_content))}</div>'
    else:
        # For ex and key, generate TOC from full merged content to capture all headings
        all_md = ""
        for file_path, content in files_data:
            all_md += pre_process_content(clean_markdown_content(content)) + "\n\n"
        md.convert(all_md)
        toc = getattr(md, 'toc', '')
        toc_html = f'<div class="pdf-toc-page"><h1>Table of Contents</h1>{toc}</div>'
    
    full_body_html = f"{title_html}{about_html}{lit_html}{toc_html}<div class='content'>{full_course_html}</div>"
    full_body_html = post_process_html(full_body_html)
    if folder_type in ('bpc_ex', 'ipc_ex'):
        full_body_html = equalize_table_columns(full_body_html)

    body_class = f' class="{folder_type}"' if folder_type else ""
    return f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>{title}</title><style>.pdf-title-page, .pdf-about-page, .pdf-literature-page, .pdf-toc-page, .pdf-class-header, .pdf-topic-page {{ page-break-before: always; }} .pdf-title-page {{ page-break-before: avoid; }} .manual-list-start {{ display: none; }} p:not(.standalone-image) img, td img, li img {{ height: 1em; width: auto; vertical-align: middle; }} .standalone-image {{ text-align: center; margin: 1em 0; }} .standalone-image img {{ height: auto !important; width: auto !important; max-width: 90%; display: block; margin: 0 auto; }} sup.manual-fn-ref a {{ text-decoration: none; color: inherit; }} .pdf-footnote-backref {{ font-style: normal; text-decoration: none; color: inherit; margin-left: 0.2em; }}</style></head><body{body_class}>{full_body_html}</body></html>"

def get_markdown_files(docs_dir: str):
    mkdocs_yaml_path = "mkdocs.yaml"
    if not os.path.exists(mkdocs_yaml_path):
        mkdocs_yaml_path = os.path.join(os.path.dirname(__file__), "..", "mkdocs.yaml")
    with open(mkdocs_yaml_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    def ext(item, d, files):
        if isinstance(item, str):
            if item.endswith('.md'):
                files.append(os.path.join(d, item))
        elif isinstance(item, list):
            for i in item:
                ext(i, d, files)
        elif isinstance(item, dict):
            for k, v in item.items():
                ext(v, d, files)
    all_files = []
    ext(config.get("nav", []), docs_dir, all_files)
    folders = ['bpc', 'bpc_ex', 'bpc_key', 'ipc', 'ipc_ex', 'ipc_key']
    f_by_dir = {f: [] for f in folders}
    for file_path in all_files:
        rel = os.path.relpath(file_path, docs_dir)
        folder = rel.split(os.sep)[0]
        if folder in f_by_dir and os.path.exists(file_path):
            f_by_dir[folder].append(file_path)
    return f_by_dir

def generate_pdf(html_content, output_pdf, css_paths=None):
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
    font_config = FontConfiguration()
    css_objs = [CSS(filename=p, font_config=font_config) for p in (css_paths or []) if os.path.exists(p)]
    HTML(string=html_content, base_url=os.path.abspath(".")).write_pdf(output_pdf, stylesheets=css_objs, font_config=font_config)

def deduplicate_vocab_table(content: str, seen_words: set[str]) -> str:
    """Filter vocab table rows whose Pāḷi word (col 1) was seen in a prior class file."""
    lines = content.splitlines(keepends=True)
    out: list[str] = []
    in_table = False
    header_done = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('|') and not in_table:
            in_table = True
            header_done = False
            out.append(line)
            continue
        if in_table and stripped.startswith('|'):
            if not header_done and not stripped.replace(' ', '').strip('|-:'):
                header_done = True
                out.append(line)
                continue
            if header_done:
                # Use regex to split only on unescaped pipes
                cols = [c.strip() for c in re.split(r"(?<!\\)\|", stripped.strip("|"))]
                word = cols[0] if cols else ''
                # Handle pipe-escaped word: word\|1 -> word|1
                word = word.replace('\\|', '|')
                if word in seen_words:
                    continue
                seen_words.add(word)
            out.append(line)
        else:
            if not stripped:
                in_table = False
                header_done = False
            out.append(line)
    return ''.join(out)


def generate_reference_pdfs(docs_dir: str, output_dir: str, css_paths: list[str], target: str | None = None) -> None:
    """Generate PDFs for generated vocabulary and abbreviations."""
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
    font_config = FontConfiguration()
    css_objs = [CSS(filename=p, font_config=font_config) for p in css_paths if os.path.exists(p)]
    md = markdown.Markdown(extensions=['toc', 'tables', 'fenced_code', 'attr_list', 'sane_lists', 'md_in_html', 'nl2br'])

    # 1. Vocab PDF
    if not target or target == "vocab":
        pr.green("vocab pdf")
        vocab_files = sorted(Path(docs_dir).joinpath("generated/vocab").glob("class-*.md"))
        if vocab_files:
            combined_html = ""
            seen_words: set[str] = set()
            for i, file_path in enumerate(vocab_files):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                c = deduplicate_vocab_table(content, seen_words)
                c = clean_markdown_content(c)
                c = pre_process_content(c)
                md.reset()
                html_fragment = md.convert(c)
                page_break = '<div style="page-break-before: always;"></div>' if i > 0 else ""
                combined_html += f'{page_break}<div class="pdf-topic-page">{html_fragment}</div>'
            
            full_html = f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Vocabulary</title></head><body>{post_process_html(combined_html)}</body></html>"
            try:
                HTML(string=full_html, base_url=os.path.abspath(".")).write_pdf(
                    os.path.join(output_dir, "vocab.pdf"), 
                    stylesheets=css_objs, 
                    font_config=font_config
                )
                pr.yes("ok")
            except Exception as e:
                pr.no(str(e))
        else:
            pr.no("no vocab files")

    # 2. Abbreviations PDF
    if not target or target == "abbreviations":
        pr.green("abbrev pdf")
        abbrev_file = Path(docs_dir) / "generated/abbreviations.md"
        if abbrev_file.exists():
            with open(abbrev_file, "r", encoding="utf-8") as f:
                content = f.read()
            c = clean_markdown_content(content)
            c = pre_process_content(c)
            md.reset()
            html_fragment = md.convert(c)
            full_html = f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Abbreviations</title></head><body>{post_process_html(html_fragment)}</body></html>"
            try:
                HTML(string=full_html, base_url=os.path.abspath(".")).write_pdf(
                    os.path.join(output_dir, "abbreviations.pdf"), 
                    stylesheets=css_objs, 
                    font_config=font_config
                )
                pr.yes("ok")
            except Exception as e:
                pr.no(str(e))
        else:
            pr.no("abbreviations.md not found")

def main():
    parser = argparse.ArgumentParser(description="Generate PDF course materials")
    parser.add_argument("folder", nargs="?", choices=list(FOLDER_NAMES.keys()) + ["vocab", "abbreviations"],
                        help="Generate only this folder (default: all)")
    parser.add_argument("--html-only", action="store_true",
                        help="Dump intermediate HTML to pdf_exports/<folder>_debug.html, skip WeasyPrint")
    args = parser.parse_args()

    docs_dir = "docs"
    output_dir = "pdf_exports"
    css_paths = ["identity/dpd-pdf-fonts.css", "identity/dpd-variables.css", "identity/dpd.css", "identity/extra.css"]
    
    # Existing course generation
    f_by_dir = get_markdown_files(docs_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    if args.folder not in ["vocab", "abbreviations"]:
        with open(os.path.join(docs_dir, "about.md"), "r", encoding="utf-8") as f:
            title_c = f.read()
        with open(os.path.join(docs_dir, "literature.md"), "r", encoding="utf-8") as f:
            lit_c = f.read()
            
        for fld, files in f_by_dir.items():
            if args.folder and fld != args.folder:
                continue
            if not files:
                continue
            pr.green(f"Generating {fld}")
            data = []
            for file_path in files:
                rel = os.path.relpath(file_path, docs_dir)
                if len(rel.split(os.sep)) == 2 and rel.endswith('index.md'):
                    continue
                with open(file_path, "r", encoding="utf-8") as f:
                    data.append((file_path, f.read()))
            ri_path = os.path.join(docs_dir, fld, "index.md")
            ri_c = ""
            if fld in ['bpc', 'ipc'] and os.path.exists(ri_path):
                with open(ri_path, "r", encoding="utf-8") as f:
                    ri_c = f.read()

            t_html_start = time.time()
            html = build_html_document(FOLDER_NAMES.get(fld, fld), data, title_c if fld in ['bpc', 'ipc'] else "", lit_c if fld in ['bpc', 'ipc'] else "", fld, root_index_content=ri_c)
            html_t = time.time() - t_html_start

            if args.html_only:
                debug_path = os.path.join(output_dir, f"{fld}_debug.html")
                with open(debug_path, "w", encoding="utf-8") as f:
                    f.write(html)
                pr.yes(f"html {html_t:.1f}s → {debug_path}")
            else:
                generate_pdf(html, os.path.join(output_dir, f"{fld}.pdf"), css_paths=css_paths)
                pr.yes("ok")

    # Reference generation
    if not args.html_only:
        if not args.folder or args.folder in ["vocab", "abbreviations"]:
            if not args.folder:
                generate_reference_pdfs(docs_dir, output_dir, css_paths)
            elif args.folder == "vocab":
                generate_reference_pdfs(docs_dir, output_dir, css_paths, target="vocab")
            elif args.folder == "abbreviations":
                generate_reference_pdfs(docs_dir, output_dir, css_paths, target="abbreviations")

    if not args.html_only and not args.folder:
        subprocess.run(["uv", "run", "python", "scripts/verify_numbering.py"], check=False)

    if not args.html_only and not args.folder:
        subprocess.run(["uv", "run", "python", "scripts/verify_numbering.py"], check=False)

if __name__ == '__main__':
    main()
