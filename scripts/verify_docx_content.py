"""
Verification tool for DOCX content integrity.
Compares text extracted from generated Word documents with source Markdown.
"""
import os
import sys
import re
from docx import Document
import yaml

def get_docx_text(path):
    """Extracts text from a .docx file."""
    doc = Document(path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                full_text.append(cell.text)
    return "\n".join(full_text)

def verify_docx(docx_path, original_md_paths):
    """Verifies that the docx contains content from all original markdown files."""
    if not os.path.exists(docx_path):
        print(f"Error: {docx_path} not found.")
        return False
        
    docx_text = get_docx_text(docx_path)
    # Basic cleaning of docx text for comparison
    docx_text_clean = docx_text.replace("\n", " ").replace("  ", " ")
    # Strip footnote markers from docx text if they were not converted
    docx_text_clean = re.sub(r'\[\^[^\]]+\]', '', docx_text_clean)
    
    missing_files = []
    for md_path in original_md_paths:
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Basic check for key fragments
            # We take some unique-ish lines from the MD
            lines = [l.strip() for l in content.split("\n") if len(l.strip()) > 20 and not l.strip().startswith("<")]
            
            found = False
            for line in lines[:5]: # Check first 5 significant lines
                # Remove MD formatting: links, bold, italics, footnotes
                clean_line = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', line) # links
                clean_line = re.sub(r'\*\*([^*]+)\*\*', r'\1', clean_line) # bold
                clean_line = re.sub(r'\*([^*]+)\*', r'\1', clean_line) # italics
                clean_line = re.sub(r'__([^_]+)__', r'\1', clean_line) # bold
                clean_line = re.sub(r'_([^_]+)_', r'\1', clean_line) # italics
                clean_line = re.sub(r'\[\^[^\]]+\]', '', clean_line) # footnotes
                clean_line = re.sub(r'^\s*(\d+\.|[-*+])\s+', '', clean_line) # list markers
                clean_line = clean_line.replace("<br>", "").replace("&nbsp;", " ").strip()
                
                if clean_line in docx_text_clean:
                    found = True
                    break
            
            if not found and lines:
                missing_files.append(md_path)
                
    if missing_files:
        print(f"Verification failed for {docx_path}. Missing content from:")
        for f in missing_files:
            print(f"  - {f}")
        return False
    else:
        print(f"Verification successful for {docx_path}.")
        return True

def main():
    docs_dir = "docs"
    docx_dir = "docx_exports"
    
    # We'll use the same logic as the generator to find files
    mkdocs_yaml_path = "mkdocs.yaml"
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
            
    all_success = True
    for folder, files in f_by_dir.items():
        docx_path = os.path.join(docx_dir, f"{folder}.docx")
        if os.path.exists(docx_path):
            if not verify_docx(docx_path, files):
                all_success = False
                
    if not all_success:
        sys.exit(1)

if __name__ == '__main__':
    main()
