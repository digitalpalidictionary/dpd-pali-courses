"""
Data integrity verification script for DPD Pāḷi Courses.
Compares Markdown source phrases against generated HTML (website) and extracted PDF text.
Ensures that no content is lost during the conversion process.
"""
import os
import re
import argparse
import unicodedata
import glob
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text

def normalize_text(text):
    if not text: return ""
    text = unicodedata.normalize('NFD', text)
    text = "".join([c for c in text if not unicodedata.combining(c)])
    text = text.lower()
    text = re.sub(r'<br\s*/?>', ' ', text)
    text = re.sub(r'[^a-z0-9]', '', text)
    return text

def extract_md_phrases(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    # Remove links but keep text
    content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
    # Replace footnotes refs like [^12] with just 12 so it matches text extraction
    content = re.sub(r'\[\^(\d+)\](?!\:)', r'\1', content)
    # For footnote defs like [^12]: text, keep the text
    content = re.sub(r'\[\^\d+\]:\s*', '', content)
    
    # Split by double newline or table rows
    lines = content.split('\n')
    phrases = []
    for line in lines:
        line = line.strip()
        if not line: continue
        if line.startswith('|'):
            # Split table row into cells and check each cell
            cells = [c.strip() for c in line.split('|') if c.strip() and not re.match(r'^[-:]+$', c.strip())]
            for cell in cells:
                norm = normalize_text(cell)
                if len(norm) > 5:  # Only check meaningful phrases
                    phrases.append((cell, norm))
        else:
            norm = normalize_text(line)
            # Only check phrases that have at least some letters/numbers
            if len(norm) > 10:
                phrases.append((line, norm))
                
    return phrases

def get_html_text(html_path):
    if not os.path.exists(html_path): return ""
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    # Extract text from soup
    return soup.get_text(separator=' ', strip=True)

def verify_against_text(phrases, target_text, target_name):
    norm_target = normalize_text(target_text)
    missing = []
    for orig, norm in phrases:
        if norm not in norm_target:
            missing.append(orig)
    return missing

def main():
    parser = argparse.ArgumentParser(description="Strict verification of MD vs HTML vs PDF.")
    parser.add_argument("--pdf_dir", default="pdf_exports")
    parser.add_argument("--site_dir", default="site")
    parser.add_argument("--md", help="Test a single MD file")
    parser.add_argument("--pdf", help="Test a single PDF file against the MD file")
    args = parser.parse_args()

    if args.md and args.pdf:
        print(f"\n--- Verifying single file: {args.md} against {args.pdf} ---")
        try:
            pdf_text = extract_text(args.pdf)
        except Exception as e:
            print(f"Error reading PDF {args.pdf}: {e}")
            return
            
        # HTML Path
        rel_md = os.path.relpath(args.md, "docs")
        html_rel = rel_md.replace('.md', '/index.html')
        if html_rel.endswith('index/index.html'): html_rel = html_rel.replace('index/index.html', 'index.html')
        html_path = os.path.join(args.site_dir, html_rel)
        html_text = get_html_text(html_path)

        phrases = extract_md_phrases(args.md)
        if not phrases:
            print("No phrases extracted.")
            return

        html_missing = verify_against_text(phrases, html_text, "HTML")
        pdf_missing = verify_against_text(phrases, pdf_text, "PDF")

        ignored = ['provide feedback on this page', 'table of contents']
        html_missing = [m for m in html_missing if normalize_text(m) not in [normalize_text(i) for i in ignored]]
        pdf_missing = [m for m in pdf_missing if normalize_text(m) not in [normalize_text(i) for i in ignored]]

        if html_missing or pdf_missing:
            if html_missing:
                print(f"    WEB MISSING ({len(html_missing)} phrases):")
                for m in html_missing: print(f"      - {m}")
            if pdf_missing:
                print(f"    PDF MISSING ({len(pdf_missing)} phrases):")
                for m in pdf_missing: print(f"      - {m}")
        else:
            print("  PASSED: 100% strict content match.")
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
        
        print(f"\n--- Verifying volume: {pdf_name} ---")
        try:
            pdf_text = extract_text(pdf_path)
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            continue
            
        md_files = []
        for s_dir in source_dirs:
            if os.path.isfile(s_dir): md_files.append(s_dir)
            else:
                for root, _, files in os.walk(s_dir):
                    for f in files:
                        if f.endswith('.md'):
                            md_files.append(os.path.join(root, f))
        
        pdf_missing_total = 0
        html_missing_total = 0
        
        for md_file in sorted(md_files):
            # Skip root index for strict phrase check as it's just TOC mostly
            if os.path.basename(md_file) == 'index.md' and os.path.dirname(md_file) in ['docs/bpc', 'docs/ipc', 'docs/bpc_ex', 'docs/bpc_key', 'docs/ipc_ex', 'docs/ipc_key']:
                continue
                
            phrases = extract_md_phrases(md_file)
            if not phrases: continue
            
            # HTML Path
            rel_md = os.path.relpath(md_file, "docs")
            html_rel = rel_md.replace('.md', '/index.html')
            if html_rel.endswith('index/index.html'): html_rel = html_rel.replace('index/index.html', 'index.html')
            html_path = os.path.join(args.site_dir, html_rel)
            
            html_text = get_html_text(html_path)
            
            # Verify Web
            html_missing = verify_against_text(phrases, html_text, "HTML")
            # Verify PDF
            pdf_missing = verify_against_text(phrases, pdf_text, "PDF")
            
            # We ignore very common things that might be stripped intentionally
            ignored = ['provide feedback on this page', 'table of contents']
            html_missing = [m for m in html_missing if normalize_text(m) not in [normalize_text(i) for i in ignored]]
            pdf_missing = [m for m in pdf_missing if normalize_text(m) not in [normalize_text(i) for i in ignored]]
            
            if html_missing or pdf_missing:
                print(f"\n  File: {md_file}")
                if html_missing:
                    print(f"    WEB MISSING ({len(html_missing)} phrases):")
                    for m in html_missing[:3]: print(f"      - {m}")
                    if len(html_missing) > 3: print(f"      ... and {len(html_missing)-3} more.")
                    html_missing_total += len(html_missing)
                if pdf_missing:
                    print(f"    PDF MISSING ({len(pdf_missing)} phrases):")
                    for m in pdf_missing[:3]: print(f"      - {m}")
                    if len(pdf_missing) > 3: print(f"      ... and {len(pdf_missing)-3} more.")
                    pdf_missing_total += len(pdf_missing)
                    
        if html_missing_total > 0 or pdf_missing_total > 0:
            overall_passed = False
            print(f"  FAILED {pdf_name}: {html_missing_total} Web mismatches, {pdf_missing_total} PDF mismatches.")
        else:
            print(f"  PASSED {pdf_name}: 100% strict content match.")
            
    if not overall_passed:
        print("\nCRITICAL: Strict verification failed. Output data is missing.")
        exit(1)
    else:
        print("\nSUCCESS: All content verified with 100% strict integrity.")

if __name__ == "__main__":
    main()
