
import os
import re
import sys

# Add the project root to sys.path to import tools.link_generator
sys.path.append(os.path.abspath(os.getcwd()))

try:
    from tools.link_generator import generate_link
except ImportError:
    print("Error: Could not import generate_link from tools.link_generator.")
    sys.exit(1)

# Base prefixes
BOOKS = [
    "MN", "DN", "SN", "AN", "KHP", "DHP", "SNP", 
    "UD", "ITI", "THI", "TH", "VIN", "PA", "SA", 
    "NP", "PC", "PD", "SE", "AS", "SK"
]

# Sub-prefixes for Vinaya Patimokkha
PAT_SUB = ["PA", "SA", "NP", "PC", "PD", "SE", "AS", "SK", "AN"]
VIN_PAT_PREFIXES = [f"VIN PAT {p}" for p in PAT_SUB]

# All prefixes, longest first to ensure greedy matching. 
# "VIN PAT" is added at the end of prefixes to be matched last.
ALL_PREFIXES = sorted(VIN_PAT_PREFIXES + BOOKS, key=len, reverse=True) + ["VIN PAT"]

# Regex pattern
PREFIX_PATTERN = r"(" + "|".join(re.escape(p) for p in ALL_PREFIXES) + r")(?:\s?(\d+(\.\d+)*))?"

def unify_format(prefix, number):
    """Unifies the format. No space except for VIN PAT."""
    # Standardize SK to SE for link_generator compatibility
    if prefix.endswith(" SK"):
        prefix = prefix.replace(" SK", " SE")
    elif prefix == "SK":
        prefix = "SE"
    
    if number:
        if prefix.startswith("VIN PAT"):
            return f"{prefix} {number}"
        return f"{prefix}{number}"
    return prefix

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Unify partial VIN PAT links: VIN PAT [SA12](url) -> [VIN PAT SA12](url)
    def unify_partial_vin(m):
        text = m.group(2)
        url = m.group(3)
        # Verify if text is a reference from BOOKS
        BOOKS_PATTERN = r"(" + "|".join(re.escape(p) for p in BOOKS) + r")(?:\s?(\d+(\.\d+)*))?"
        ref_match = re.search(BOOKS_PATTERN, text)
        if ref_match:
            p = ref_match.group(1)
            n = ref_match.group(2)
            unified = unify_format(f"VIN PAT {p}", n)
            return f"[{unified}]({url})"
        return m.group(0)

    # Search for "VIN PAT [Ref](URL)"
    new_content = re.sub(r"(VIN PAT)\s*\[([^\]]+)\]\((https://find\.dhamma\.gift/bw/[^\)]+)\)", unify_partial_vin, content)

    # 2. Fix references inside existing links
    def fix_link_text(m):
        link_text = m.group(1)
        url = m.group(2)
        ref_match = re.search(PREFIX_PATTERN, link_text)
        if ref_match:
            p = ref_match.group(1)
            n = ref_match.group(2)
            if not n and p != "ITI":
                return m.group(0)
            unified = unify_format(p, n)
            if link_text != unified:
                return f"[{unified}]({url})"
        return m.group(0)

    new_content = re.sub(r"\[([^\]]+)\]\((https://find\.dhamma\.gift/bw/[^\)]+)\)", fix_link_text, new_content)

    # 3. Fix bare references and add links
    final_lines = []
    BARE_PREFIX_PATTERN = r"\b" + PREFIX_PATTERN + r"\b"
    
    for line in new_content.splitlines():
        def line_replace(m):
            prefix = m.group(1)
            number = m.group(2)
            pos = m.start()
            line_str = m.string
            
            if not number and prefix != "ITI":
                return m.group(0)
            if line_str[:pos].count('`') % 2 != 0:
                return m.group(0)
            
            links = list(re.finditer(r"\[.*?\]\(.*?\)|\[.*?\]", line_str))
            for l in links:
                if l.start() <= pos < l.end():
                    return m.group(0)
            
            unified = unify_format(prefix, number)
            url = generate_link(unified)
            if url:
                return f"[{unified}]({url})"
            return unified

        new_line = re.sub(BARE_PREFIX_PATTERN, line_replace, line)
        final_lines.append(new_line)
    
    final_content_str = "\n".join(final_lines)
    if content != final_content_str:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(final_content_str)
        return True
    return False

def main():
    docs_dir = "docs"
    files_updated = 0
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                if process_file(os.path.join(root, file)):
                    files_updated += 1
    print(f"Total files updated: {files_updated}")

if __name__ == "__main__":
    main()
