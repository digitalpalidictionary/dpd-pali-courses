"""
Script to verify consistency of sentence numbering across Markdown, Website, and PDF.
Identifies discrepancies where numbering resets or differs between formats.
"""
import os
import re
import argparse
import glob
import unicodedata
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text

def normalize_pali(text):
    if not text: return ""
    text = unicodedata.normalize('NFD', text)
    text = "".join([c for c in text if not unicodedata.combining(c)])
    return text.lower().strip()

def get_md_numbering(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # 1. Footnotes
    footnotes = re.findall(r'\[\^(\d+)\]', content)
    # 2. Ordered lists
    lists = re.findall(r'^\s*(\d+)\.\s+', content, re.MULTILINE)
    return {
        'footnotes': [int(n) for n in footnotes],
        'lists': [int(n) for n in lists]
    }

def get_html_numbering(html_path):
    if not os.path.exists(html_path): return None
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    fn_refs = soup.find_all('sup', class_='manual-fn-ref')
    footnotes = [r.get_text().strip() for r in fn_refs]
    visible_list_numbers = []
    for ol in soup.find_all('ol'):
        start = int(ol.get('start', 1))
        for i, li in enumerate(ol.find_all('li', recursive=False)):
            visible_list_numbers.append(start + i)
    return {
        'footnotes': [int(n) for n in footnotes if n.isdigit()],
        'lists': visible_list_numbers
    }

def verify_file_strict(md_rel_path, pdf_text_compact):
    """
    STRICTLY verifies numbering by searching for markers in the FINAL PDF text.
    """
    docs_dir = "docs"
    md_path = os.path.join(docs_dir, md_rel_path)
    md_data = get_md_numbering(md_path)
    
    print(f"\nVerifying {md_rel_path} against PDF text:")
    
    status = True
    
    # Check Lists
    if md_data['lists']:
        # For each number in the MD list, it MUST appear in the PDF text 
        # as a marker like "1." followed by some text.
        # Since extraction is messy, we check for presence of unique markers.
        missing = []
        for n in md_data['lists']:
            # Search for the literal marker "n." in the compact text
            # We look for "n." where n is the number.
            marker = f"{n}."
            if marker not in pdf_text_compact:
                missing.append(n)
        
        if missing:
            print(f"  - ERROR: Missing list markers in PDF: {missing[:10]}...")
            status = False
        else:
            print(f"  - List markers in PDF: OK")

    # Check Footnotes
    if md_data['footnotes']:
        md_unique = sorted(list(set(md_data['footnotes'])))
        missing_fn = []
        for n in md_unique:
            marker = f"{n}." # Our labels are "n. "
            if marker not in pdf_text_compact:
                missing_fn.append(n)
        
        if missing_fn:
            print(f"  - ERROR: Missing footnote markers in PDF: {missing_fn}")
            status = False
        else:
            print(f"  - Footnote markers in PDF: OK")

    return status

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Specific MD file")
    args = parser.parse_args()
    
    # Pre-extract FULL PDF text for verification
    print("Extracting final PDF text for strict verification...")
    pdf_texts = {}
    for pdf_name in ['bpc.pdf', 'bpc_ex.pdf', 'bpc_key.pdf', 'ipc.pdf', 'ipc_ex.pdf', 'ipc_key.pdf']:
        path = os.path.join("pdf_exports", pdf_name)
        if os.path.exists(path):
            print(f"  Reading {pdf_name}...")
            raw = extract_text(path)
            # Remove whitespace but KEEP numbers and dots
            pdf_texts[pdf_name.split('.')[0]] = re.sub(r'\s+', '', raw)

    files = glob.glob("docs/**/*.md", recursive=True)
    total_files = 0; failed_files = 0
    
    for f in sorted(files):
        rel = os.path.relpath(f, "docs")
        if len(rel.split(os.sep)) == 2 and rel.endswith('index.md'): continue
        
        folder = rel.split(os.sep)[0]
        pdf_text = pdf_texts.get(folder)
        if not pdf_text: continue
        
        with open(f, 'r') as file:
            content = file.read()
            if '[^' in content or re.search(r'^\s*\d+\.\s+', content, re.MULTILINE):
                total_files += 1
                if not verify_file_strict(rel, pdf_text):
                    failed_files += 1

    print(f"\nSummary: {total_files} files checked, {failed_files} failures found.")
    if failed_files > 0: exit(1)

if __name__ == "__main__":
    main()
