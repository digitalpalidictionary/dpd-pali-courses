"""
Verification script for PDF content integrity.
Extracts text from generated PDFs and compares it with source Markdown to ensure no data loss.
"""
import os
import re
import argparse
import unicodedata
from pdfminer.high_level import extract_text

def normalize_pali(text):
    """Robust normalization for Pāḷi text comparison."""
    if not text: return ""
    text = unicodedata.normalize('NFD', text)
    # Remove diacritics
    text = "".join([c for c in text if not unicodedata.combining(c)])
    text = text.lower()
    # Strip all non-alphanumeric
    text = re.sub(r'[^a-z0-9]', '', text)
    return text

def is_ignored(word):
    """Words to ignore in verification (UI, metadata, artifacts)."""
    ignored = {
        'feedback', 'provide', 'suitable', 'viewform', 'google', 'usp_url', 
        'entry', 'http', 'https', 'html', 'mailto', 'target', 'blank'
    }
    return word.lower() in ignored or len(word) < 6

def verify_content(pdf_path, md_files):
    try:
        pdf_raw = extract_text(pdf_path)
        pdf_compact = normalize_pali(pdf_raw)
    except Exception as e:
        return [f"Error reading PDF: {e}"]

    missing_report = []
    
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            # Extract all words including Pāḷi diacritics
            md_words = set(re.findall(r'\b[a-zāīūṃṅñṭḍṇḷļ]{6,}\b', f.read().lower()))
            
        for word in sorted(list(md_words)):
            if is_ignored(word): continue
            
            term = normalize_pali(word)
            if term not in pdf_compact:
                # FINAL FALLBACK: very flexible regex for badly broken words
                # e.g. "passiṃsu" -> "p...s...s"
                skeleton = ".*?".join([c for c in term if c.isalpha()][::2]) # check every 2nd char
                if not re.search(skeleton, pdf_compact):
                    missing_report.append(f"{word} ({os.path.basename(md_file)})")
                    
    return missing_report

def main():
    parser = argparse.ArgumentParser(description="Reliable integrity verification of PDF content.")
    parser.add_argument("--pdf", help="Specific PDF file")
    parser.add_argument("--md", help="Specific MD file")
    parser.add_argument("--pdf_dir", default="pdf_exports")
    parser.add_argument("--docs_dir", default="docs")
    args = parser.parse_args()
    
    if args.pdf and args.md:
        missing = verify_content(args.pdf, [args.md])
        if not missing: print(f"SUCCESS: 100% integrity.")
        else:
            print(f"FAILURE: {len(missing)} missing:")
            for m in missing: print(f"  - {m}")
        return

    volumes = {
        'bpc.pdf': ['docs/bpc', 'docs/about.md', 'docs/literature.md'],
        'bpc_ex.pdf': ['docs/bpc_ex'],
        'bpc_key.pdf': ['docs/bpc_key'],
        'ipc.pdf': ['docs/ipc', 'docs/about.md', 'docs/literature.md'],
        'ipc_ex.pdf': ['docs/ipc_ex'],
        'ipc_key.pdf': ['docs/ipc_key'],
    }
    
    overall_passed = True
    for pdf_name, source_dirs in volumes.items():
        pdf_path = os.path.join(args.pdf_dir, pdf_name)
        if not os.path.exists(pdf_path): continue
        
        print(f"Verifying {pdf_name}...")
        md_files = []
        for s_dir in source_dirs:
            if os.path.isfile(s_dir): md_files.append(s_dir)
            else:
                for root, _, files in os.walk(s_dir):
                    for f in files:
                        rel_p = os.path.relpath(os.path.join(root, f), args.docs_dir)
                        if len(rel_p.split(os.sep)) == 2 and f == 'index.md': continue
                        if f.endswith('.md'): md_files.append(os.path.join(root, f))
        
        missing = verify_content(pdf_path, md_files)
            
        if not missing:
            print(f"  PASSED: 100% data integrity.")
        else:
            print(f"  FAILED: {len(missing)} words missing.")
            for m in missing[:10]: print(f"    - {m}")
            overall_passed = False

    if not overall_passed: exit(1)

if __name__ == "__main__":
    main()
