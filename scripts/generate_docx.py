"""
Script to generate Word (.docx) documents from Markdown source using Pandoc.
Maintains visual parity with PDF output for offline study.
"""
import os
import yaml
import markdown
import re
import subprocess
import pypandoc
from bs4 import BeautifulSoup
import argparse

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

def clean_markdown_content(content):
    """Remove UI elements not suitable for DOCX."""
    content = re.sub(r'<div class="nav-links">.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class="feedback">.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<a[^>]+class="(prev|previous|next|cross)"[^>]*>.*?</a>', '', content)
    return content

def fix_internal_links(content):
    """Converts relative links to internal PDF/DOCX anchors."""
    # Matches [Link](path/to/file.md#anchor)
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

def aggregate_markdown(title, files_data, about_content="", lit_content=""):
    """Combines multiple Markdown files into one."""
    aggregated = f"# {title}\n\n"
    if about_content:
        aggregated += f"{about_content}\n\n"
    if lit_content:
        aggregated += f"{lit_content}\n\n"
        
    for file_path, content in files_data:
        # is_idx = os.path.basename(file_path) == 'index.md'
        c = clean_markdown_content(content)
        
        # User requested keeping the Class X headers in DOCX
        # if not is_idx:
        #     c = re.sub(r'^# Class \d+.*?\n', '', c, flags=re.MULTILINE)
        
        c = fix_internal_links(c)
        
        # Add a bookmark/anchor for the file
        anchor_id = os.path.basename(file_path).replace('.', '_')
        aggregated += f"[]{{#{anchor_id}}}\n\n"
        aggregated += f"{c}\n\n"
        
    return aggregated

def generate_docx(aggregated_md, output_docx):
    """Converts aggregated markdown to .docx using pypandoc."""
    pypandoc.convert_text(
        aggregated_md,
        'docx',
        format='markdown',
        outputfile=output_docx,
        extra_args=[
            '--toc',
            '--standalone',
            '--toc-depth=2',
            '--resource-path=docs:docs/assets/images:.'
        ]
    )

def get_markdown_files(docs_dir: str):
    mkdocs_yaml_path = "mkdocs.yaml"
    if not os.path.exists(mkdocs_yaml_path):
        mkdocs_yaml_path = os.path.join(os.path.dirname(__file__), "..", "mkdocs.yaml")
    
    with open(mkdocs_yaml_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    def extract_nav(item, base_dir, file_list):
        if isinstance(item, str):
            if item.endswith('.md'):
                file_list.append(os.path.join(base_dir, item))
        elif isinstance(item, list):
            for i in item:
                extract_nav(i, base_dir, file_list)
        elif isinstance(item, dict):
            for v in item.values():
                extract_nav(v, base_dir, file_list)

    all_files = []
    extract_nav(config.get("nav", []), docs_dir, all_files)
    
    folders = ['bpc', 'bpc_ex', 'bpc_key', 'ipc', 'ipc_ex', 'ipc_key']
    f_by_dir = {f: [] for f in folders}
    
    for file_path in all_files:
        rel = os.path.relpath(file_path, docs_dir)
        folder = rel.split(os.sep)[0]
        if folder in f_by_dir and os.path.exists(file_path):
            f_by_dir[folder].append(file_path)
    
    return f_by_dir

def main():
    parser = argparse.ArgumentParser(description="Generate .docx from course markdown.")
    parser.add_argument("--folder", help="Specific folder to generate (e.g., bpc_ex)")
    args = parser.parse_args()

    docs_dir = "docs"
    f_by_dir = get_markdown_files(docs_dir)
    
    # Read common materials
    about_path = os.path.join(docs_dir, "about.md")
    lit_path = os.path.join(docs_dir, "literature.md")
    
    about_c = open(about_path, "r", encoding="utf-8").read() if os.path.exists(about_path) else ""
    lit_c = open(lit_path, "r", encoding="utf-8").read() if os.path.exists(lit_path) else ""
    
    for fld, files in f_by_dir.items():
        if not files:
            continue
        
        if args.folder and fld != args.folder:
            continue
            
        print(f"Processing {fld}...")
        data = []
        for file_path in files:
            rel = os.path.relpath(file_path, docs_dir)
            # Skip root index files as they are often redundant or handled separately
            if len(rel.split(os.sep)) == 2 and rel.endswith('index.md'):
                continue
            with open(file_path, "r", encoding="utf-8") as f:
                data.append((file_path, f.read()))
        
        # Generate aggregated markdown
        title = FOLDER_NAMES.get(fld, fld)
        # Use about/lit only for BPC to match PDF exporter
        agg_md = aggregate_markdown(
            title, 
            data, 
            about_content=about_c if fld == 'bpc' else "", 
            lit_content=lit_c if fld == 'bpc' else ""
        )
        
        if not os.path.exists("docx_exports"):
            os.makedirs("docx_exports")
            
        output_file = os.path.join("docx_exports", f"{fld}.docx")
        generate_docx(agg_md, output_file)
        print(f"Generated {output_file}")

if __name__ == '__main__':
    main()
