"""
Script to generate Word (.docx) documents from Markdown source using Pandoc.
Maintains visual parity with PDF output for offline study.
"""
import os
import yaml
import re
import subprocess
import pypandoc
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import argparse
from tools.printer import printer as pr

# Ensure pandoc is available
try:
    pypandoc.get_pandoc_version()
except OSError:
    print("Pandoc not found. Downloading...")
    pypandoc.download_pandoc()

FOLDER_NAMES = {
    'bpc': 'Beginner Pāḷi Course (BPC)',
    'bpc_ex': 'Beginner Pāḷi Course (BPC) - Exercises',
    'bpc_key': 'Beginner Pāḷi Course (BPC) - Answer Key',
    'ipc': 'Intermediate Pāḷi Course (IPC)',
    'ipc_ex': 'Intermediate Pāḷi Course (IPC) - Exercises',
    'ipc_key': 'Intermediate Pāḷi Course (IPC) - Answer Key',
}

PAGEBREAK = '\n\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n'


def clean_markdown_content(content: str) -> str:
    """Remove UI elements not suitable for DOCX."""
    content = re.sub(r'<div class="nav-links">.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class="feedback">.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<a[^>]+class="(prev|previous|next|cross)"[^>]*>.*?</a>', '', content)
    return content


def fix_internal_links(content: str) -> str:
    """Converts relative links to internal PDF/DOCX anchors."""
    def replacer(match):
        text = match.group(1)
        href = match.group(2)
        if ('.md' in href) and not href.startswith('http'):
            file_part = href.split('#')[0] if '#' in href else href
            anchor_id = os.path.basename(file_part).replace('.', '_')
            return f"[{text}](#{anchor_id})"
        return match.group(0)

    pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
    return re.sub(pattern, replacer, content)


def preprocess_inline_images(content: str) -> str:
    """Add height attribute to inline images so they render at symbol size in DOCX."""
    return re.sub(
        r'(!\[[^\]]*\]\([^)]+\))(?!\{)',
        r'\1{height=18px}',
        content
    )


def insert_h2_page_breaks(content: str) -> str:
    """Insert page breaks before ## headings in _ex files."""
    lines = content.split('\n')
    result = []
    for line in lines:
        if re.match(r'^## ', line):
            result.extend(['', '```{=openxml}', '<w:p><w:r><w:br w:type="page"/></w:r></w:p>', '```', ''])
        result.append(line)
    return '\n'.join(result)


def make_heading_slug(text: str) -> str:
    """Convert heading text to Pandoc's auto-generated header identifier."""
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)  # strip links
    text = re.sub(r'[*_`#]', '', text)                      # strip emphasis/code
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)                    # remove punctuation
    text = re.sub(r'\s+', '-', text.strip())                # spaces → hyphens
    text = re.sub(r'^[^a-z]+', '', text)                    # remove leading non-letters
    return text or 'section'


def build_manual_toc(files_data: list[tuple[str, str]]) -> str:
    """Build a Table of Contents from H1 and H2 headings across all source files."""
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
    lines.append('')
    return '\n'.join(lines)


def aggregate_markdown(title: str, files_data: list[tuple[str, str]], folder: str = '', about_content: str = "", lit_content: str = "") -> str:
    """Combines multiple Markdown files into one."""
    aggregated = f"# {title}\n\n"
    if about_content:
        aggregated += f"{about_content}\n\n"
    if lit_content:
        aggregated += f"{lit_content}\n\n"

    # _ex and _key: inject a manually-built TOC so it renders correctly in all viewers
    if folder.endswith(('_ex', '_key')):
        aggregated += build_manual_toc(files_data) + PAGEBREAK

    needs_file_pagebreaks = folder in ('bpc', 'ipc') or folder.endswith(('_ex', '_key'))
    is_ex = folder.endswith('_ex')

    for i, (file_path, content) in enumerate(files_data):
        c = clean_markdown_content(content)
        c = fix_internal_links(c)
        c = preprocess_inline_images(c)

        if i > 0 and needs_file_pagebreaks:
            aggregated += PAGEBREAK

        if is_ex:
            c = insert_h2_page_breaks(c)

        anchor_id = os.path.basename(file_path).replace('.', '_')
        aggregated += f"[]{{#{anchor_id}}}\n\n"
        aggregated += f"{c}\n\n"

    return aggregated


def generate_docx(aggregated_md: str, output_docx: str, folder: str = '') -> None:
    """Converts aggregated markdown to .docx using pypandoc."""
    # _ex and _key use a manually-built TOC; bpc and ipc use Pandoc's field-based TOC
    use_pandoc_toc = not folder.endswith(('_ex', '_key'))
    extra_args = ['--standalone', '--resource-path=docs:docs/assets/images:.']
    if use_pandoc_toc:
        extra_args += ['--toc', '--toc-depth=2']
    pypandoc.convert_text(
        aggregated_md,
        'docx',
        format='markdown',
        outputfile=output_docx,
        extra_args=extra_args
    )


def post_process_docx(docx_path: str, folder: str) -> None:
    """Post-process DOCX: merge exercise table footer rows and force field updates."""
    doc = Document(docx_path)

    if folder.endswith('_ex'):
        for table in doc.tables:
            if len(table.rows) < 2:
                continue
            last_row = table.rows[-1]
            if len(last_row.cells) <= 1:
                continue
            non_empty = sum(1 for c in last_row.cells if c.text.strip())
            if non_empty <= 1:
                last_row.cells[0].merge(last_row.cells[-1])

    update_fields = OxmlElement('w:updateFields')
    update_fields.set(qn('w:val'), 'true')
    doc.settings.element.append(update_fields)

    doc.save(docx_path)


def get_markdown_files(docs_dir: str) -> dict[str, list[str]]:
    mkdocs_yaml_path = "mkdocs.yaml"
    if not os.path.exists(mkdocs_yaml_path):
        mkdocs_yaml_path = os.path.join(os.path.dirname(__file__), "..", "mkdocs.yaml")

    with open(mkdocs_yaml_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    def extract_nav(item: object, base_dir: str, file_list: list[str]) -> None:
        if isinstance(item, str):
            if item.endswith('.md'):
                file_list.append(os.path.join(base_dir, item))
        elif isinstance(item, list):
            for i in item:
                extract_nav(i, base_dir, file_list)
        elif isinstance(item, dict):
            for v in item.values():
                extract_nav(v, base_dir, file_list)

    all_files: list[str] = []
    extract_nav(config.get("nav", []), docs_dir, all_files)

    folders = ['bpc', 'bpc_ex', 'bpc_key', 'ipc', 'ipc_ex', 'ipc_key']
    f_by_dir: dict[str, list[str]] = {f: [] for f in folders}

    for file_path in all_files:
        rel = os.path.relpath(file_path, docs_dir)
        folder = rel.split(os.sep)[0]
        if folder in f_by_dir and os.path.exists(file_path):
            f_by_dir[folder].append(file_path)

    return f_by_dir


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


def generate_reference_docx(docs_dir: str, output_dir: str, target: str | None = None) -> None:
    """Generate DOCX for generated vocabulary and abbreviations."""
    from pathlib import Path

    # 1. Vocab DOCX
    if not target or target == "vocab":
        pr.green("vocab docx")
        vocab_files = sorted(Path(docs_dir).joinpath("generated/vocab").glob("class-*.md"))
        if vocab_files:
            combined_md = ""
            seen_words: set[str] = set()
            for i, file_path in enumerate(vocab_files):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                c = deduplicate_vocab_table(content, seen_words)
                c = clean_markdown_content(c)
                if i > 0:
                    combined_md += PAGEBREAK
                combined_md += f"{c}\n\n"
            
            output_file = os.path.join(output_dir, "vocab.docx")
            try:
                pypandoc.convert_text(
                    combined_md,
                    'docx',
                    format='markdown',
                    outputfile=output_file,
                    extra_args=['--standalone', '--resource-path=docs:docs/assets/images:.']
                )
                pr.yes("ok")
            except Exception as e:
                pr.no(str(e))
        else:
            pr.no("no vocab files")

    # 2. Abbreviations DOCX
    if not target or target == "abbreviations":
        pr.green("abbrev docx")
        abbrev_file = Path(docs_dir) / "generated/abbreviations.md"
        if abbrev_file.exists():
            with open(abbrev_file, "r", encoding="utf-8") as f:
                content = f.read()
            c = clean_markdown_content(content)
            output_file = os.path.join(output_dir, "abbreviations.docx")
            try:
                pypandoc.convert_text(
                    c,
                    'docx',
                    format='markdown',
                    outputfile=output_file,
                    extra_args=['--standalone', '--resource-path=docs:docs/assets/images:.']
                )
                pr.yes("ok")
            except Exception as e:
                pr.no(str(e))
        else:
            pr.no("abbreviations.md not found")

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate .docx from course markdown.")
    parser.add_argument("--folder", choices=list(FOLDER_NAMES.keys()) + ["vocab", "abbreviations"],
                        help="Specific folder to generate (e.g., bpc_ex)")
    args = parser.parse_args()

    docs_dir = "docs"
    output_dir = "docx_exports"
    f_by_dir = get_markdown_files(docs_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if args.folder not in ["vocab", "abbreviations"]:
        about_path = os.path.join(docs_dir, "about.md")
        lit_path = os.path.join(docs_dir, "literature.md")

        about_c = open(about_path, "r", encoding="utf-8").read() if os.path.exists(about_path) else ""
        lit_c = open(lit_path, "r", encoding="utf-8").read() if os.path.exists(lit_path) else ""

        for fld, files in f_by_dir.items():
            if not files:
                continue

            if args.folder and fld != args.folder:
                continue

            pr.green(f"Generating {fld}")
            data = []
            for file_path in files:
                # _ex and _key: skip folder-level index.md (it's a navigation list, not content)
                if fld.endswith(('_ex', '_key')) and os.path.basename(file_path) == 'index.md':
                    continue
                with open(file_path, "r", encoding="utf-8") as f:
                    data.append((file_path, f.read()))

            title = FOLDER_NAMES.get(fld, fld)
            agg_md = aggregate_markdown(
                title,
                data,
                folder=fld,
                about_content=about_c if fld in ('bpc', 'ipc') else "",
                lit_content=lit_c if fld in ('bpc', 'ipc') else ""
            )

            output_file = os.path.join(output_dir, f"{fld}.docx")
            generate_docx(agg_md, output_file, folder=fld)
            post_process_docx(output_file, fld)
            pr.yes("ok")

    # Reference generation
    if not args.folder or args.folder in ["vocab", "abbreviations"]:
        if not args.folder:
            generate_reference_docx(docs_dir, output_dir)
        elif args.folder == "vocab":
            generate_reference_docx(docs_dir, output_dir, target="vocab")
        elif args.folder == "abbreviations":
            generate_reference_docx(docs_dir, output_dir, target="abbreviations")

    if not args.folder:
        subprocess.run(["uv", "run", "python", "scripts/verify_docx_content.py"], check=False)


if __name__ == '__main__':
    main()
