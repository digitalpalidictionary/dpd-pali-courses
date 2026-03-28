"""
Script to generate PDF course materials from Markdown source files using WeasyPrint.
It applies course-specific styling, cleans UI elements, and handles footnote reformatting.
"""
import os
import yaml
import markdown
import re
import subprocess
import sys
from bs4 import BeautifulSoup

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
    def repl_def(m):
        prefix = m.group(1); fn_num = m.group(2); content = m.group(3).strip()
        return f"\n<div class='manual-fn-def' data-fn='{fn_num}' markdown='1'>\n\n{prefix}{content}\n\n</div>\n\n"
    pattern = r'^([ \t*_]*)\[\^(\d+)\]:\s*(.*?)(?=\n[ \t]*\n|\n[ \t]*[-*_]{3,}|\n[ \t]*#|\n\[\^|\Z)'
    text = re.sub(pattern, repl_def, text, flags=re.MULTILINE | re.DOTALL)
    text = re.sub(r'\[\^(\d+)\]', r"<sup class='manual-fn-ref' data-fn='\1'>\1</sup>", text)
    def repl_list(m):
        num = m.group(1)
        return f"\n<div class='manual-list-start' data-start='{num}'></div>\n\n{num}. "
    text = re.sub(r'^\s*(\d+)\.\s+', repl_list, text, flags=re.MULTILINE)

    def repl_newlines(m):
        count = m.group(0).count('\n')
        if count > 2:
            return '\n\n' + '<br>\n' * (count - 2)
        return m.group(0)
    text = re.sub(r'\n{3,}', repl_newlines, text)
    
    return text

def process_footnotes_for_pdf(html_content):
    """Moves manual footnote definitions into WeasyPrint-compatible floats."""
    soup = BeautifulSoup(html_content, 'html.parser')
    defs = {d['data-fn']: d for d in soup.find_all('div', class_='manual-fn-def')}
    for ref in soup.find_all('sup', class_='manual-fn-ref'):
        fn_num = ref['data-fn']
        if fn_num in defs:
            new_span = soup.new_tag('span', attrs={'class': 'pdf-footnote'})
            label = soup.new_tag('b', attrs={'class': 'pdf-footnote-label'}); label.string = f"{fn_num}. "
            new_span.append(label)
            fn_soup = BeautifulSoup(defs[fn_num].decode_contents(), 'html.parser')
            for p in fn_soup.find_all('p'): p.unwrap()
            new_span.append(fn_soup); ref.insert_after(new_span)
    for d in defs.values(): d.decompose()
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
        file_id = os.path.basename(file_path).replace('.', '_')
        div_class = 'pdf-class-header' if is_idx else 'pdf-topic-page'
        full_course_html += f"<div class='{div_class}' id='{file_id}'>{topic_html}</div>"
    
    md.reset()
    if root_index_content:
        # For lessons, use the provided root index content
        toc_html = f'<div class="pdf-toc-page">{md.convert(pre_process_content(root_index_content))}</div>'
    else:
        # For ex and key, generate TOC from full merged content to capture all headings
        all_md = ""
        for file_path, content in files_data:
            all_md += pre_process_content(clean_markdown_content(content)) + "\n\n"
        md.convert(all_md)
        toc = getattr(md, 'toc', '')
        toc_html = f'<div class="pdf-toc-page"><h1>Table of Contents</h1>{toc}</div>'
    
    full_body_html = f"{title_html}{about_html}{lit_html}{toc_html}<div class='content'>{full_course_html}</div>"
    full_body_html = fix_internal_links(full_body_html)
    full_body_html = fix_list_numbering(full_body_html)
    full_body_html = process_footnotes_for_pdf(full_body_html)
    
    return f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>{title}</title><style>.pdf-title-page, .pdf-about-page, .pdf-literature-page, .pdf-toc-page, .pdf-class-header, .pdf-topic-page {{ page-break-before: always; }} .pdf-title-page {{ page-break-before: avoid; }} .pdf-footnote-label {{ font-weight: bold; margin-right: 0.3em; }} .pdf-footnote {{ float: footnote; font-size: 0.9em; font-style: italic; }} .manual-list-start {{ display: none; }} p img, td img, li img {{ height: 1em; width: auto; vertical-align: middle; }}</style></head><body>{full_body_html}</body></html>"

def get_markdown_files(docs_dir: str):
    mkdocs_yaml_path = "mkdocs.yaml"
    if not os.path.exists(mkdocs_yaml_path): mkdocs_yaml_path = os.path.join(os.path.dirname(__file__), "..", "mkdocs.yaml")
    with open(mkdocs_yaml_path, "r", encoding="utf-8") as f: config = yaml.safe_load(f)
    def ext(item, d, l):
        if isinstance(item, str):
            if item.endswith('.md'): l.append(os.path.join(d, item))
        elif isinstance(item, list):
            for i in item: ext(i, d, l)
        elif isinstance(item, dict):
            for k, v in item.items(): ext(v, d, l)
    all_files = []
    ext(config.get("nav", []), docs_dir, all_files)
    folders = ['bpc', 'bpc_ex', 'bpc_key', 'ipc', 'ipc_ex', 'ipc_key']
    f_by_dir = {f: [] for f in folders}
    for file_path in all_files:
        rel = os.path.relpath(file_path, docs_dir); folder = rel.split(os.sep)[0]
        if folder in f_by_dir and os.path.exists(file_path): f_by_dir[folder].append(file_path)
    return f_by_dir

def generate_pdf(html_content, output_pdf, css_paths=None):
    from weasyprint import HTML, CSS
    css_objs = [CSS(filename=p) for p in (css_paths or []) if os.path.exists(p)]
    HTML(string=html_content, base_url=os.path.abspath(".")).write_pdf(output_pdf, stylesheets=css_objs)

def main():
    docs_dir = "docs"
    css_paths = ["identity/dpd-variables.css", "identity/dpd.css", "identity/extra.css"]
    with open(os.path.join(docs_dir, "about.md"), "r", encoding="utf-8") as f: title_c = f.read()
    with open(os.path.join(docs_dir, "literature.md"), "r", encoding="utf-8") as f: lit_c = f.read()
    f_by_dir = get_markdown_files(docs_dir)
    for fld, files in f_by_dir.items():
        if not files: continue
        print(f"Processing {fld}...")
        data = []
        for file_path in files:
            rel = os.path.relpath(file_path, docs_dir)
            if len(rel.split(os.sep)) == 2 and rel.endswith('index.md'): continue
            with open(file_path, "r", encoding="utf-8") as f: data.append((file_path, f.read()))
        ri_path = os.path.join(docs_dir, fld, "index.md")
        # ONLY use root_index for bpc and ipc (lessons), NOT for ex or key
        ri_c = ""
        if fld in ['bpc', 'ipc'] and os.path.exists(ri_path):
            ri_c = open(ri_path, "r", encoding="utf-8").read()
            
        html = build_html_document(FOLDER_NAMES.get(fld, fld), data, title_c if fld in ['bpc', 'ipc'] else "", lit_c if fld in ['bpc', 'ipc'] else "", fld, root_index_content=ri_c)
        if not os.path.exists("pdf_exports"): os.makedirs("pdf_exports")
        generate_pdf(html, os.path.join("pdf_exports", f"{fld}.pdf"), css_paths=css_paths)

    print("\nRunning numbering verification...")
    try: subprocess.run(["uv", "run", "python", "scripts/verify_numbering.py"], check=True)
    except Exception as e: print(f"Verification failed: {e}")

if __name__ == '__main__':
    main()
